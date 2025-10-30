"""
🌸 Hannah Modal Client - Cliente simplificado para conectar con Modal
"""

def call_modal_backend(requirement):
    """
    Llama al backend de Modal localmente
    """
    try:
        # Importar la función de Modal directamente
        from src.hannah_modal_app import generate_test_matrix_and_gherkin
        
        # Ejecutar la función localmente
        result = generate_test_matrix_and_gherkin.local(requirement)
        
        # Retornar el resultado
        if isinstance(result, dict):
            return result
        else:
            return {
                "status": "success",
                "output": str(result) if result else "",
                "matrix_data": [],
                "gherkin_content": ""
            }
            
    except ImportError as e:
        return {
            "status": "error",
            "error": f"Error importando Modal: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": f"Error ejecutando Modal: {str(e)}"
        }
