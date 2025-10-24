#!/usr/bin/env python3
"""
🚀 Ejecutor de Hannah QA Agent con Logging a Axiom
Script para ejecutar la aplicación Hannah con integración completa a Axiom
"""

import os
import sys
import subprocess
from pathlib import Path

def run_hannah_with_axiom():
    """Ejecuta Hannah QA Agent con logging a Axiom usando Doppler"""
    
    print("🚀 Iniciando Hannah QA Agent con Logging a Axiom")
    print("=" * 60)
    print(f"📁 Directorio: {os.getcwd()}")
    print(f"🐍 Python: {sys.executable}")
    print("=" * 60)
    
    # Verificar que el archivo existe
    hannah_file = Path("src/app_hannah_error_handling_with_axiom.py")
    if not hannah_file.exists():
        print(f"❌ Archivo no encontrado: {hannah_file}")
        return False
    
    # Verificar que Doppler está disponible
    try:
        result = subprocess.run(["doppler", "--version"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            print("❌ Doppler no está disponible")
            return False
        print(f"✅ Doppler disponible: {result.stdout.strip()}")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Doppler no está instalado o no está en el PATH")
        return False
    
    # Buscar puerto disponible
    import socket
    def find_free_port():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port
    
    port = find_free_port()
    
    # Comando para ejecutar Hannah con Doppler
    cmd = [
        "doppler", "run", "--",
        "streamlit", "run", str(hannah_file),
        "--server.port", str(port),
        "--server.address", "0.0.0.0"
    ]
    
    print(f"🚀 Ejecutando comando: {' '.join(cmd)}")
    print("\n📊 Características habilitadas:")
    print("   ✅ Variables de entorno: Doppler")
    print("   ✅ Backend: Modal (Serverless)")
    print("   ✅ Logging: Axiom")
    print("   ✅ Interfaz: Streamlit")
    print(f"\n🌐 La aplicación estará disponible en: http://localhost:{port}")
    print("📊 Los logs se enviarán automáticamente a Axiom")
    print("\n⏹️  Presiona Ctrl+C para detener la aplicación")
    print("-" * 60)
    
    try:
        # Ejecutar la aplicación
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al ejecutar Hannah: {e}")
        return False
    except KeyboardInterrupt:
        print("\n⏹️  Hannah QA Agent detenido por el usuario")
        return True

def main():
    """Función principal"""
    success = run_hannah_with_axiom()
    
    if success:
        print("\n✅ Hannah QA Agent ejecutado correctamente")
        sys.exit(0)
    else:
        print("\n❌ Error al ejecutar Hannah QA Agent")
        sys.exit(1)

if __name__ == "__main__":
    main()
