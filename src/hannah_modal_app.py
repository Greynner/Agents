import modal
import os
import pandas as pd
from openai import OpenAI, OpenAIError

# Define la imagen base con todas las dependencias
image = modal.Image.debian_slim().pip_install(
    "openai", 
    "pandas", 
    "streamlit",
    "openpyxl"
)

# Crea la app de Modal
app = modal.App("hannah-qa-agent", image=image)

# Usa los secretos de Doppler (que ya están en Modal)
@app.function(secrets=[modal.Secret.from_name("qa-agent-secrets")])
def generate_test_matrix_and_gherkin(requirement: str):
    """
    Hannah 🌸 - Genera matriz de pruebas y casos Gherkin desde Modal
    """
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Prompt mejorado de Hannah
        SYSTEM_PROMPT = """
        Eres Hannah 🌸, una QA Engineer Senior especializada en automatización de pruebas.
        Tu tarea es analizar un requerimiento y generar una matriz de pruebas y casos Gherkin claros y consistentes.
        """
        
        FEW_SHOT_EXAMPLE = """
        | ID | Escenario | Datos de entrada | Resultado esperado |
        |----|------------|------------------|--------------------|
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
        
        return {
            "status": "success",
            "output": output,
            "matrix_data": df.to_dict('records') if df is not None else [],
            "gherkin_content": gherkin_content,
            "matrix_columns": df.columns.tolist() if df is not None else []
        }
        
    except OpenAIError as e:
        return {
            "status": "error",
            "error": f"Error al conectar con OpenAI: {e}",
            "output": "",
            "matrix_data": [],
            "gherkin_content": "",
            "matrix_columns": []
        }
    except Exception as e:
        return {
            "status": "error", 
            "error": f"Error inesperado: {e}",
            "output": "",
            "matrix_data": [],
            "gherkin_content": "",
            "matrix_columns": []
        }

# Función para probar localmente
if __name__ == "__main__":
    # Prueba local
    result = generate_test_matrix_and_gherkin.local("El usuario debe poder iniciar sesión con correo y contraseña.")
    print("=== RESULTADO DE HANNAH 🌸 ===")
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
    else:
        print(f"❌ Error: {result['error']}")
