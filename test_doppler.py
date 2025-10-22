import os

print("🔍 Verificando variables de entorno desde Doppler...\n")

# Variables esperadas
vars_to_check = [
    "OPENAI_API_KEY",
    "DATABASE_URL",
    "MODAL_TOKEN",
    "AXIOM_API_TOKEN",
    "ENVIRONMENT"
]

for var in vars_to_check:
    value = os.getenv(var)
    if value:
        print(f"✅ {var} cargada correctamente")
    else:
        print(f"❌ {var} NO está disponible")

print("\n✅ Test de Doppler completado.")
