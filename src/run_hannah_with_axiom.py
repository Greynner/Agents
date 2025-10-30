"""
Ejecutor simple de Hannah con Axiom
"""
import os
import sys
import subprocess
import socket
from pathlib import Path

def find_free_port():
    """Encuentra un puerto libre"""
    with socket.socket() as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def main():
    hannah_file = Path("src/app_hannah_error_handling_with_axiom.py")
    if not hannah_file.exists():
        print(f"❌ Archivo no encontrado: {hannah_file}")
        sys.exit(1)
    
    port = find_free_port()
    cmd = ["doppler", "run", "--", "streamlit", "run", str(hannah_file),
           "--server.port", str(port), "--server.address", "0.0.0.0"]
    
    print("🚀 Iniciando Hannah con Axiom")
    print(f"🌐 Disponible en: http://localhost:{port}")
    print("⏹️  Ctrl+C para detener\n")
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n⏹️  Detenido por el usuario")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
