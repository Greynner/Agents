"""
Test de conexión con Modal y cliente simplificado
"""
import os
import sys

def test_modal_direct():
    """Prueba Modal directamente"""
    print("🔍 Test 1: Modal Directo\n")
    
    try:
        from src.hannah_modal_app import generate_test_matrix_and_gherkin
        print("✅ Función Modal importada")
        
        result = generate_test_matrix_and_gherkin.local("Usuario debe poder iniciar sesión")
        print(f"✅ Status: {result['status']}")
        print(f"📊 Casos: {len(result.get('matrix_data', []))}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_modal_client():
    """Prueba el cliente de Modal"""
    print("\n🔍 Test 2: Cliente Modal\n")
    
    try:
        from src.hannah_modal_client import call_modal_backend
        print("✅ Cliente importado")
        
        result = call_modal_backend("Usuario debe poder iniciar sesión")
        print(f"✅ Status: {result['status']}")
        print(f"📊 Casos: {len(result.get('matrix_data', []))}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success1 = test_modal_direct()
    success2 = test_modal_client()
    
    if success1 and success2:
        print("\n✅ Todos los tests pasaron")
    else:
        print("\n❌ Algunos tests fallaron")
        sys.exit(1)
