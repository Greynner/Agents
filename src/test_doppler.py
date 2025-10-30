"""
Test simple de variables de entorno de Doppler
"""
import os

print("🔍 Verificando variables de Doppler...\n")

vars_to_check = ["OPENAI_API_KEY", "AXIOM_API_TOKEN", "AXIOM_ORG_ID", "ENVIRONMENT"]

for var in vars_to_check:
    print(f"{'✅' if os.getenv(var) else '❌'} {var}")

print("\n✅ Test completado.")
