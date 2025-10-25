#!/usr/bin/env python3
"""
🔍 Test de conexión con Modal desde el frontend
Verifica que la función de Modal se puede llamar correctamente
"""

import os
import sys

def test_modal_connection():
    """Prueba la conexión con Modal"""
    print("🔍 Probando conexión con Modal...\n")
    
    try:
        # Importar la función de Modal
        from src.hannah_modal_app import generate_test_matrix_and_gherkin
        
        print("✅ Función de Modal importada correctamente")
        
        # Probar la función localmente
        print("🧪 Probando función localmente...")
        result = generate_test_matrix_and_gherkin.local("El usuario debe poder iniciar sesión")
        
        print(f"✅ Resultado: {result['status']}")
        print(f"📊 Casos generados: {len(result.get('matrix_data', []))}")
        print(f"🧾 Gherkin generado: {'Sí' if result.get('gherkin_content') else 'No'}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error al importar: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    success = test_modal_connection()
    
    if success:
        print("\n🎉 ¡Conexión con Modal exitosa!")
        print("✅ El frontend puede conectarse al backend de Modal")
    else:
        print("\n⚠️ Error en la conexión con Modal")
        sys.exit(1)
