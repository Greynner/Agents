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
    import tempfile
    
    try:
        # Crear un archivo temporal con el código Python
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(f"""
import sys
import json
sys.path.append('.')

try:
    from src.hannah_modal_app import generate_test_matrix_and_gherkin
    
    # Ejecutar la función de Modal
    result = generate_test_matrix_and_gherkin.local('''{requirement}''')
    
    # Convertir a string para evitar problemas de serialización
    if hasattr(result, '__dict__'):
        result_dict = {{
            'status': 'success',
            'output': str(result.get('output', '')),
            'matrix_data': result.get('matrix_data', []),
            'gherkin_content': result.get('gherkin_content', '')
        }}
    else:
        result_dict = {{
            'status': 'success',
            'output': str(result),
            'matrix_data': [],
            'gherkin_content': ''
        }}
    
    print(json.dumps(result_dict))
    
except Exception as e:
    error_result = {{
        'status': 'error',
        'error': str(e)
    }}
    print(json.dumps(error_result))
""")
            temp_file = f.name
        
        # Ejecutar el archivo temporal
        cmd = ["python", temp_file]
        
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            cwd=os.getcwd()
        )
        
        # Limpiar archivo temporal
        os.unlink(temp_file)
        
        if result.returncode == 0:
            # Parsear el resultado JSON
            try:
                return json.loads(result.stdout.strip())
            except json.JSONDecodeError:
                return {
                    "status": "error", 
                    "error": f"Error parseando resultado: {result.stdout}"
                }
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
