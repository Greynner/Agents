"""
🌸 Hannah Modal Client - Cliente simplificado para conectar con Modal
"""

import subprocess
import json
import os

def call_modal_backend(requirement):
    """
    Llama al backend de Modal de manera simple y directa
    """
    try:
        # Comando para ejecutar la función de Modal
        cmd = [
            "python", "-c",
            f"""
import sys
sys.path.append('.')
from src.hannah_modal_app import generate_test_matrix_and_gherkin
result = generate_test_matrix_and_gherkin.local('{requirement.replace("'", "\\'")}')
print(str(result))
"""
        ]
        
        # Ejecutar el comando
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            cwd=os.getcwd()
        )
        
        if result.returncode == 0:
            # Parsear el resultado
            import ast
            return ast.literal_eval(result.stdout.strip())
        else:
            return {
                "status": "error", 
                "error": f"Error ejecutando Modal: {result.stderr}"
            }
            
    except Exception as e:
        return {
            "status": "error", 
            "error": f"Error al conectar con Modal: {str(e)}"
        }
