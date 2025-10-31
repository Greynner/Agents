import os
import pandas as pd
import modal
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from fastapi import Request
from fastapi.responses import JSONResponse
import requests
import json
import traceback
from datetime import datetime, timezone
from typing import Dict, Any, Optional

# =====================
# CONFIGURACIÓN DOPPLER + VARIABLES DE ENTORNO
# =====================
# Doppler inyecta variables de entorno, dotenv como fallback
load_dotenv()

# Variables de entorno (desde Doppler o .env)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AXIOM_API_TOKEN = os.getenv("AXIOM_API_TOKEN")
AXIOM_ORG_ID = os.getenv("AXIOM_ORG_ID")
AXIOM_DATASET = os.getenv("AXIOM_DATASET", "hannah-qa-agent")
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")

if not OPENAI_API_KEY:
    print("⚠️ Advertencia: OPENAI_API_KEY no está configurada. Usa Doppler o un archivo .env")

# =====================
# LOGGER AXIOM
# =====================
class AxiomLogger:
    """Clase para enviar logs a Axiom"""
    
    def __init__(self):
        self.api_token = AXIOM_API_TOKEN
        self.org_id = AXIOM_ORG_ID
        self.dataset = AXIOM_DATASET
        self.environment = ENVIRONMENT
        self.ingest_url = f"https://api.axiom.co/v1/datasets/{self.dataset}/ingest"
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_token}',
            'X-Axiom-Org-Id': self.org_id
        } if self.api_token and self.org_id else None
    
    def log(self, level: str, message: str, metadata: Optional[Dict] = None) -> bool:
        """Envía un log a Axiom"""
        if not self.api_token or not self.org_id or not self.headers:
            print(f"[{level}] {message}")
            return False
        
        try:
            log_data = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "level": level.upper(),
                "message": message,
                "source": "hannah_qa_agent_v3",
                "environment": self.environment,
                "metadata": metadata or {}
            }
            
            response = requests.post(
                self.ingest_url,
                headers=self.headers,
                json=[log_data],
                timeout=5
            )
            
            if response.status_code == 200:
                return True
            else:
                print(f"⚠️ Error enviando log a Axiom: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error en logging: {str(e)}")
            return False
    
    def log_info(self, message: str, metadata: Optional[Dict] = None) -> bool:
        """Log de información"""
        return self.log("INFO", message, metadata)
    
    def log_error(self, message: str, error: Exception = None, context: Optional[Dict] = None) -> bool:
        """Log de error con detalles"""
        metadata = context or {}
        if error:
            metadata.update({
                "error_type": type(error).__name__,
                "error_message": str(error),
                "traceback": traceback.format_exc()
            })
        return self.log("ERROR", message, metadata)
    
    def log_warning(self, message: str, metadata: Optional[Dict] = None) -> bool:
        """Log de advertencia"""
        return self.log("WARN", message, metadata)

# Instancia global del logger
axiom_logger = AxiomLogger()

# =====================
# CONFIGURACIÓN MODAL
# =====================
# Imagen base con todas las dependencias
image = modal.Image.debian_slim().pip_install(
    "openai>=1.0.0",
    "pandas>=2.0.0",
    "openpyxl",
    "fastapi",
    "requests",
    "python-dotenv",
)

# Crea la app de Modal
app = modal.App("hannah-qa-agent-v3", image=image)

# =====================
# FUNCIÓN PRINCIPAL - GENERAR PRUEBAS
# =====================
@app.function(secrets=[modal.Secret.from_name("qa-agent-secrets")])
def generate_test_matrix_and_gherkin(requirement: str):
    """
    Hannah 🌸 - Genera matriz de pruebas y casos Gherkin desde Modal
    Integra OpenAI + Axiom logging
    """
    try:
        # Inicializar cliente OpenAI (usa secretos de Modal/Doppler)
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        axiom_logger.log_info(f"Generando casos para requerimiento: {requirement[:100]}...")
        
        # Prompt mejorado de Hannah
        SYSTEM_PROMPT = """
        Eres Hannah 🌸, una QA Engineer Senior especializada en automatización de pruebas.
        Tu tarea es analizar un requerimiento y generar una matriz de pruebas y casos Gherkin claros y consistentes.
        """
        
        FEW_SHOT_EXAMPLE = """
        | ID | Escenario | Datos de entrada | Resultado esperado |
        |----|-----------|------------------|-------------------|
        | TC001 | Login exitoso | Usuario válido | Acceso concedido |
        | TC002 | Login fallido | Usuario inválido | Mensaje de error "Credenciales inválidas" |

        Feature: Validación de login
          Scenario: Login exitoso
            Given usuario válido
            When ingresa credenciales correctas
            Then muestra "Acceso concedido"
        """
        
        # Llamada a OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.3,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"{FEW_SHOT_EXAMPLE}\n\nRequerimiento:\n{requirement}"}
            ]
        )
        
        output = response.choices[0].message.content
        
        # Procesar matriz de prueba
        rows = []
        for line in output.splitlines():
            if "|" in line and "---" not in line:
                cols = [c.strip() for c in line.split("|") if c.strip()]
                if len(cols) > 1:
                    rows.append(cols)
        
        # Crear DataFrame
        df = None
        if rows:
            df = pd.DataFrame(rows[1:], columns=rows[0])
        
        # Extraer casos Gherkin
        gherkin_lines = []
        capture = False
        for line in output.splitlines():
            if line.strip().startswith(("Feature", "Scenario")):
                capture = True
            if capture:
                gherkin_lines.append(line)
        
        gherkin_content = "\n".join(gherkin_lines) if gherkin_lines else ""
        
        result = {
            "status": "success",
            "output": output,
            "matrix_data": df.to_dict('records') if df is not None else [],
            "gherkin_content": gherkin_content,
            "matrix_columns": df.columns.tolist() if df is not None else []
        }
        
        axiom_logger.log_info(
            f"Casos generados exitosamente: {len(result['matrix_data'])} filas",
            {"matrix_rows": len(result['matrix_data']), "has_gherkin": bool(gherkin_content)}
        )
        
        return result
        
    except OpenAIError as e:
        error_msg = f"Error al conectar con OpenAI: {e}"
        axiom_logger.log_error("Error en OpenAI", e, {"requirement": requirement[:100]})
        return {
            "status": "error",
            "error": error_msg,
            "output": "",
            "matrix_data": [],
            "gherkin_content": "",
            "matrix_columns": []
        }
    except Exception as e:
        error_msg = f"Error inesperado: {e}"
        axiom_logger.log_error("Error inesperado", e, {"requirement": requirement[:100]})
        return {
            "status": "error", 
            "error": error_msg,
            "output": "",
            "matrix_data": [],
            "gherkin_content": "",
            "matrix_columns": []
        }

# =====================
# ENDPOINT WEB PARA FRONTEND DE VERCEL
# =====================
@app.function()
@modal.fastapi_endpoint(method="POST")
async def analizar_requerimiento(request: Request):
    """
    Endpoint HTTP para recibir requerimientos desde el frontend de Vercel.
    Soporta CORS para conexión con frontend.
    """
    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
    }

    # Manejar preflight CORS
    if request.method == "OPTIONS":
        response = JSONResponse(status_code=204, content=None)
        for key, value in cors_headers.items():
            response.headers[key] = value
        return response

    try:
        payload = await request.json()
        requirement = (
            (payload.get("requerimiento") or payload.get("requirement") or "").strip()
        )

        if not requirement:
            axiom_logger.log_warning("Intento de análisis sin requerimiento")
            response = JSONResponse(
                status_code=400,
                content={"status": "error", "error": "El campo 'requerimiento' es obligatorio."},
            )
            for key, value in cors_headers.items():
                response.headers[key] = value
            return response

        axiom_logger.log_info("Solicitud recibida desde frontend", {"requirement_length": len(requirement)})
        
        # Llamar a la función de generación (usar .remote() para llamadas asíncronas en endpoints web)
        result = generate_test_matrix_and_gherkin.remote(requirement)

        response = JSONResponse(content=result)
        for key, value in cors_headers.items():
            response.headers[key] = value
        return response
    
    except Exception as e:
        axiom_logger.log_error("Error en endpoint web", e)
        error_response = JSONResponse(
            status_code=500,
            content={"status": "error", "error": f"Error interno: {str(e)}"}
        )
        for key, value in cors_headers.items():
            error_response.headers[key] = value
        return error_response

# =====================
# EJECUCIÓN LOCAL (PARA PRUEBAS)
# =====================
if __name__ == "__main__":
    print("🌸 Hannah QA Agent V3 - Versión Unificada")
    print("=" * 50)
    print("Integraciones: Doppler + OpenAI + Modal + Axiom + Vercel Frontend")
    print("=" * 50)
    
    # Prueba local
    test_requirement = "El usuario debe poder iniciar sesión con correo y contraseña."
    print(f"\n📋 Requerimiento de prueba: {test_requirement}\n")
    
    try:
        result = generate_test_matrix_and_gherkin.local(test_requirement)
        print("\n=== RESULTADO DE HANNAH 🌸 ===")
        print(f"Status: {result['status']}")
        
        if result['status'] == 'success':
            print("\n📊 MATRIZ DE PRUEBAS:")
            print(result['output'])
            
            if result['matrix_data']:
                print(f"\n📋 DATOS DE MATRIZ ({len(result['matrix_data'])} filas):")
                for i, row in enumerate(result['matrix_data'][:3]):  # Mostrar solo las primeras 3
                    print(f"  Fila {i+1}: {row}")
            
            print(f"\n🧾 CONTENIDO GHERKIN:")
            print(result['gherkin_content'])
            
            axiom_logger.log_info("Prueba local completada exitosamente")
        else:
            print(f"❌ Error: {result['error']}")
            axiom_logger.log_error("Prueba local falló", None, {"error": result.get('error')})
    except Exception as e:
        print(f"❌ Error en prueba local: {e}")
        axiom_logger.log_error("Error en prueba local", e)
