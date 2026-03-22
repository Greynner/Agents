import os
import json
import traceback
from pathlib import Path

import modal
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from fastapi import Request
from fastapi.responses import JSONResponse

from utils_axiom import AxiomLogger

# =====================
# CONFIGURACIÓN
# =====================
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALLOWED_ORIGIN = os.getenv("ALLOWED_ORIGIN", "*")
MAX_REQUIREMENT_LENGTH = 5000

if not OPENAI_API_KEY:
    print("⚠️ OPENAI_API_KEY no está configurada. Usa Doppler o un archivo .env")

axiom_logger = AxiomLogger(source="hannah_qa_agent_v3")

# =====================
# CONFIGURACIÓN MODAL
# =====================
_utils_path = str(Path(__file__).parent / "utils_axiom.py")

image = (
    modal.Image.debian_slim()
    .pip_install(
        "openai>=1.0.0",
        "pandas>=2.0.0",
        "openpyxl",
        "fastapi",
        "requests",
        "python-dotenv",
    )
    .copy_local_file(_utils_path, "/root/utils_axiom.py")
)

app = modal.App("hannah-qa-agent-v3", image=image)

# =====================
# PROMPTS
# =====================
SYSTEM_PROMPT = """
Eres Hannah, una QA Engineer Senior especializada en automatización de pruebas.
Analiza el requerimiento y responde ÚNICAMENTE con un JSON válido con esta estructura exacta:
{
  "matrix": [
    {
      "ID": "TC001",
      "Escenario": "descripción del escenario",
      "Datos de entrada": "datos usados",
      "Resultado esperado": "resultado esperado"
    }
  ],
  "gherkin": "Feature: ...\n  Scenario: ...\n    Given ...\n    When ...\n    Then ..."
}
Genera al menos 5 casos de prueba. No incluyas texto adicional fuera del JSON.
"""

# =====================
# FUNCIÓN PRINCIPAL
# =====================
@app.function(secrets=[modal.Secret.from_name("qa-agent-secrets")])
def generate_test_matrix_and_gherkin(requirement: str):
    """Hannah - Genera matriz de pruebas y casos Gherkin"""
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        axiom_logger.log_info(
            "Generando casos de prueba",
            {"requirement_length": len(requirement)},
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.3,
            max_tokens=2048,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Requerimiento:\n{requirement}"},
            ],
        )

        raw = response.choices[0].message.content
        data = json.loads(raw)

        matrix_data = data.get("matrix", [])
        gherkin_content = data.get("gherkin", "")
        matrix_columns = list(matrix_data[0].keys()) if matrix_data else []

        axiom_logger.log_info(
            "Casos generados exitosamente",
            {"matrix_rows": len(matrix_data), "has_gherkin": bool(gherkin_content)},
        )

        return {
            "status": "success",
            "output": raw,
            "matrix_data": matrix_data,
            "gherkin_content": gherkin_content,
            "matrix_columns": matrix_columns,
        }

    except OpenAIError as e:
        axiom_logger.log_error("Error en OpenAI", e, {"requirement": requirement[:100]})
        return {
            "status": "error",
            "error": f"Error al conectar con OpenAI: {e}",
            "output": "",
            "matrix_data": [],
            "gherkin_content": "",
            "matrix_columns": [],
        }
    except Exception as e:
        axiom_logger.log_error("Error inesperado", e, {"requirement": requirement[:100]})
        return {
            "status": "error",
            "error": f"Error inesperado: {e}",
            "output": "",
            "matrix_data": [],
            "gherkin_content": "",
            "matrix_columns": [],
        }


# =====================
# ENDPOINT WEB
# =====================
@app.function()
@modal.fastapi_endpoint(method="POST")
async def analizar_requerimiento(request: Request):
    cors_headers = {
        "Access-Control-Allow-Origin": ALLOWED_ORIGIN,
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
    }

    if request.method == "OPTIONS":
        response = JSONResponse(status_code=204, content=None)
        for k, v in cors_headers.items():
            response.headers[k] = v
        return response

    try:
        payload = await request.json()
        requirement = (
            (payload.get("requerimiento") or payload.get("requirement") or "").strip()
        )

        if not requirement:
            axiom_logger.log_warning("Solicitud sin requerimiento")
            response = JSONResponse(
                status_code=400,
                content={"status": "error", "error": "El campo 'requerimiento' es obligatorio."},
            )
            for k, v in cors_headers.items():
                response.headers[k] = v
            return response

        if len(requirement) > MAX_REQUIREMENT_LENGTH:
            axiom_logger.log_warning(
                "Requerimiento demasiado largo",
                {"length": len(requirement)},
            )
            response = JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "error": f"El requerimiento no puede superar {MAX_REQUIREMENT_LENGTH} caracteres.",
                },
            )
            for k, v in cors_headers.items():
                response.headers[k] = v
            return response

        axiom_logger.log_info(
            "Solicitud recibida desde frontend",
            {"requirement_length": len(requirement)},
        )

        result = generate_test_matrix_and_gherkin.remote(requirement)

        response = JSONResponse(content=result)
        for k, v in cors_headers.items():
            response.headers[k] = v
        return response

    except Exception as e:
        axiom_logger.log_error("Error en endpoint web", e)
        error_response = JSONResponse(
            status_code=500,
            content={"status": "error", "error": f"Error interno: {str(e)}"},
        )
        for k, v in cors_headers.items():
            error_response.headers[k] = v
        return error_response


# =====================
# EJECUCIÓN LOCAL
# =====================
if __name__ == "__main__":
    print("Hannah QA Agent V3")
    test_requirement = "El usuario debe poder iniciar sesión con correo y contraseña."
    print(f"\nRequerimiento de prueba: {test_requirement}\n")

    try:
        result = generate_test_matrix_and_gherkin.local(test_requirement)
        print(f"Status: {result['status']}")
        if result["status"] == "success":
            print(f"Casos generados: {len(result['matrix_data'])}")
            print(f"Gherkin:\n{result['gherkin_content'][:500]}")
        else:
            print(f"Error: {result['error']}")
    except Exception as e:
        print(f"Error en prueba local: {e}")
