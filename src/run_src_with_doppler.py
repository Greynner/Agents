"""
Ejecutor simple para archivos en src/ con Doppler
"""
import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_with_doppler(file_path, args=None):
    """Ejecuta un archivo Python con Doppler"""
    file_path = Path(file_path)
    if not file_path.exists():
        print(f"❌ Archivo no existe: {file_path}")
        return False
    
    cmd = ["doppler", "run", "--", "python", str(file_path)]
    if args:
        cmd.extend(args)
    
    print(f"🚀 Ejecutando: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"❌ Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Ejecutar archivos con Doppler")
    parser.add_argument("file", help="Archivo a ejecutar")
    parser.add_argument("args", nargs="*", help="Argumentos")
    args = parser.parse_args()
    
    if run_with_doppler(args.file, args.args):
        print("\n✅ Completado")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
