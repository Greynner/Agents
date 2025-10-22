#!/usr/bin/env python3
"""
🔍 Test de Doppler para archivos en src/
Verifica que las variables de entorno estén disponibles desde la carpeta src/
"""

import os
import sys

def test_doppler_variables():
    """Verifica que las variables de Doppler estén disponibles en src/"""
    
    print("🔍 Verificando variables de entorno desde src/ con Doppler...\n")
    
    # Variables esperadas
    vars_to_check = [
        "OPENAI_API_KEY",
        "DATABASE_URL", 
        "MODAL_TOKEN",
        "AXIOM_API_TOKEN",
        "ENVIRONMENT"
    ]
    
    all_loaded = True
    
    for var in vars_to_check:
        value = os.getenv(var)
        if value:
            # Mostrar solo los primeros y últimos caracteres por seguridad
            masked_value = f"{value[:4]}...{value[-4:]}" if len(value) > 8 else "***"
            print(f"✅ {var} cargada correctamente ({masked_value})")
        else:
            print(f"❌ {var} NO está disponible")
            all_loaded = False
    
    print(f"\n📁 Directorio actual: {os.getcwd()}")
    print(f"🐍 Python path: {sys.executable}")
    
    if all_loaded:
        print("\n🎉 ¡Todas las variables de Doppler están disponibles en src/!")
        return True
    else:
        print("\n⚠️  Algunas variables no están disponibles. Verifica la configuración de Doppler.")
        return False

if __name__ == "__main__":
    test_doppler_variables()
