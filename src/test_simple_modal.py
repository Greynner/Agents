#!/usr/bin/env python3
"""
🔍 Test simple de conexión con Modal
"""

import os
import sys

# Agregar el directorio actual al path
sys.path.append('.')

def test_simple_modal():
    """Prueba simple de Modal"""
    print("🔍 Probando conexión simple con Modal...\n")
    
    try:
        # Importar directamente
        from src.hannah_modal_app import generate_test_matrix_and_gherkin
        
        print("✅ Función importada correctamente")
        
        # Probar localmente
        result = generate_test_matrix_and_gherkin.local("Usuario debe poder hacer login")
        
        print(f"✅ Resultado: {result['status']}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_simple_modal()
