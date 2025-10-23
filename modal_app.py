import modal
import os
from openai import OpenAI

# Define la imagen base
image = modal.Image.debian_slim().pip_install("openai", "pandas")

# Crea la app de Modal
app = modal.App("qa-agent-backend", image=image)

# Usa los secretos de Doppler (que ya están en Modal)
@app.function(secrets=[modal.Secret.from_name("qa-agent-secrets")])
def generate_test_cases(requirement: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Genera una matriz de pruebas para el siguiente requerimiento QA:\n\n{requirement}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


# Puedes probar localmente
if __name__ == "__main__":
    result = generate_test_cases.local("El usuario debe poder iniciar sesión con correo y contraseña.")
    print(result)