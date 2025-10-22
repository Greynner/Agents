import os
from openai import OpenAI

print("🚀 Iniciando aplicación con Doppler...\n")

# Verificar solo las variables esenciales
required_vars = ["OPENAI_API_KEY", "DATABASE_URL"]
missing = [v for v in required_vars if not os.getenv(v)]

if missing:
    print(f"❌ Faltan variables en Doppler: {', '.join(missing)}")
    print("👉 Revisa tu configuración en Doppler o tu entorno activo (qa-agent/dev).")
    exit(1)
else:
    print("✅ Variables esenciales cargadas correctamente.\n")

# Inicializar cliente de OpenAI
try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Llamada de prueba al modelo GPT-4o-mini
    prompt = "Di un mensaje corto de bienvenida para un agente QA impulsado por IA."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    print("🤖 Respuesta del modelo:")
    print(response.choices[0].message.content)

except Exception as e:
    print("❌ Error al conectar con la API de OpenAI:")
    print(str(e))