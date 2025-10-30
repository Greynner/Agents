"""
Test simple de conexión con OpenAI usando Doppler
"""
import os
from openai import OpenAI

print("🚀 Test de OpenAI con Doppler\n")

if not os.getenv("OPENAI_API_KEY"):
    print("❌ OPENAI_API_KEY no disponible")
    exit(1)

try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Saluda brevemente"}],
    )
    print("✅ Respuesta:", response.choices[0].message.content)
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)