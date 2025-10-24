#!/usr/bin/env python3
"""
📤 Enviar Log a Axiom
Script simple para enviar un log de prueba a Axiom usando Doppler
"""

import os
import sys
import requests
import json
from datetime import datetime, timezone

def send_log_to_axiom():
    """Envía un log de prueba a Axiom"""
    
    # Obtener variables de entorno de Doppler
    axiom_api_token = os.getenv('AXIOM_API_TOKEN')
    axiom_org_id = os.getenv('AXIOM_ORG_ID')
    axiom_dataset = os.getenv('AXIOM_DATASET', 'test-dataset')
    
    if not axiom_api_token or not axiom_org_id:
        print("❌ Error: Variables AXIOM_API_TOKEN y AXIOM_ORG_ID son requeridas")
        return False
    
    # URL de ingesta de Axiom
    ingest_url = f"https://api.axiom.co/v1/datasets/{axiom_dataset}/ingest"
    
    # Headers para la petición
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {axiom_api_token}',
        'X-Axiom-Org-Id': axiom_org_id
    }
    
    # Crear log de prueba
    now = datetime.now(timezone.utc)
    log_data = {
        "timestamp": now.isoformat(),
        "level": "INFO",
        "message": "🧪 Log de prueba desde Python con Doppler",
        "source": "python_script",
        "environment": os.getenv('ENVIRONMENT', 'development'),
        "test_id": f"log_test_{now.strftime('%Y%m%d_%H%M%S')}",
        "metadata": {
            "script_name": "send_log_to_axiom.py",
            "python_version": sys.version.split()[0],
            "platform": sys.platform,
            "user": os.getenv('USER', 'unknown'),
            "hostname": os.getenv('HOSTNAME', 'localhost')
        },
        "custom_fields": {
            "test_type": "connection_verification",
            "success": True,
            "timestamp_utc": now.isoformat(),
            "timezone": "UTC"
        }
    }
    
    print("📤 Enviando log a Axiom...")
    print(f"📊 Dataset: {axiom_dataset}")
    print(f"🕐 Timestamp: {now.isoformat()}")
    print(f"📝 Mensaje: {log_data['message']}")
    print("-" * 50)
    
    try:
        # Enviar el log a Axiom
        response = requests.post(
            ingest_url,
            headers=headers,
            json=[log_data],  # Axiom espera un array de eventos
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ ¡Log enviado exitosamente a Axiom!")
            print(f"📊 Respuesta de Axiom:")
            print(f"   • Eventos ingeridos: {result.get('ingested', 0)}")
            print(f"   • Eventos fallidos: {result.get('failed', 0)}")
            print(f"   • Bytes procesados: {result.get('processedBytes', 0)}")
            print(f"   • Longitud WAL: {result.get('walLength', 0)}")
            
            if result.get('failures'):
                print(f"⚠️  Fallos: {result.get('failures')}")
            
            return True
        else:
            print(f"❌ Error al enviar log: {response.status_code}")
            print(f"📄 Respuesta: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {str(e)}")
        return False

def main():
    """Función principal"""
    print("🚀 Enviando Log de Prueba a Axiom")
    print("=" * 50)
    print(f"📁 Directorio: {os.getcwd()}")
    print(f"🐍 Python: {sys.executable}")
    print("=" * 50)
    
    success = send_log_to_axiom()
    
    if success:
        print("\n🎉 ¡Log enviado correctamente!")
        print("✅ Conexión Axiom + Doppler funcionando")
        sys.exit(0)
    else:
        print("\n❌ Error al enviar log")
        sys.exit(1)

if __name__ == "__main__":
    main()
