#!/usr/bin/env python3
"""
🚀 Ejecutor universal para archivos en src/ con Doppler
Permite ejecutar cualquier archivo de la carpeta src/ con las variables de Doppler
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_with_doppler(file_path, args=None):
    """
    Ejecuta un archivo en src/ con las variables de Doppler
    
    Args:
        file_path (str): Ruta del archivo a ejecutar
        args (list): Argumentos adicionales para pasar al archivo
    """
    
    # Verificar que el archivo existe
    src_dir = Path("src")
    if not src_dir.exists():
        print("❌ La carpeta src/ no existe")
        return False
    
    file_path = Path(file_path)
    if not file_path.exists():
        print(f"❌ El archivo {file_path} no existe")
        return False
    
    # Verificar que está en src/
    if not str(file_path).startswith("src/"):
        print("❌ El archivo debe estar en la carpeta src/")
        return False
    
    # Construir el comando
    cmd = ["doppler", "run", "--"]
    
    # Determinar el comando según la extensión del archivo
    if file_path.suffix == ".py":
        cmd.append("python")
    elif file_path.name.endswith(".py") and "streamlit" in file_path.name:
        cmd.append("streamlit")
        cmd.append("run")
    else:
        cmd.append("python")
    
    cmd.append(str(file_path))
    
    # Agregar argumentos adicionales si los hay
    if args:
        cmd.extend(args)
    
    print(f"🚀 Ejecutando: {' '.join(cmd)}")
    print(f"📁 Desde directorio: {os.getcwd()}")
    print("-" * 50)
    
    try:
        # Ejecutar el comando
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al ejecutar: {e}")
        return False
    except FileNotFoundError:
        print("❌ Doppler no está instalado o no está en el PATH")
        return False

def main():
    parser = argparse.ArgumentParser(description="Ejecutar archivos en src/ con Doppler")
    parser.add_argument("file", help="Archivo a ejecutar (relativo a src/)")
    parser.add_argument("args", nargs="*", help="Argumentos adicionales")
    
    args = parser.parse_args()
    
    # Si el archivo no tiene ruta completa, asumir que está en src/
    file_path = args.file
    if not file_path.startswith("src/"):
        file_path = f"src/{file_path}"
    
    success = run_with_doppler(file_path, args.args)
    
    if success:
        print("\n✅ Ejecución completada exitosamente")
    else:
        print("\n❌ La ejecución falló")
        sys.exit(1)

if __name__ == "__main__":
    main()
