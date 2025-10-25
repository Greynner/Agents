#!/usr/bin/env python3
"""
📊 Monitor y Logger para Axiom
Script que monitorea el sistema y envía logs a Axiom periódicamente
"""

import os
import sys
import requests
import json
import time
import psutil
import random
from datetime import datetime, timezone

def get_system_metrics():
    """Obtiene métricas del sistema"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "cpu_usage": cpu_percent,
            "memory_usage": memory.percent,
            "memory_available": memory.available,
            "disk_usage": disk.percent,
            "disk_free": disk.free,
            "load_average": os.getloadavg()[0] if hasattr(os, 'getloadavg') else 0
        }
    except Exception as e:
        return {"error": str(e)}

def send_monitoring_log(metrics, log_type="system_metrics"):
    """Envía log de monitoreo a Axiom"""
    
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
    
    # Crear log de monitoreo
    now = datetime.now(timezone.utc)
    
    # Determinar nivel basado en métricas
    level = "INFO"
    if metrics.get("cpu_usage", 0) > 80 or metrics.get("memory_usage", 0) > 80:
        level = "WARN"
    if metrics.get("cpu_usage", 0) > 95 or metrics.get("memory_usage", 0) > 95:
        level = "ERROR"
    
    log_data = {
        "timestamp": now.isoformat(),
        "level": level,
        "message": f"📊 Métricas del sistema - CPU: {metrics.get('cpu_usage', 0):.1f}%, RAM: {metrics.get('memory_usage', 0):.1f}%",
        "log_type": log_type,
        "source": "system_monitor",
        "environment": os.getenv('ENVIRONMENT', 'development'),
        "monitor_id": f"monitor_{now.strftime('%Y%m%d_%H%M%S')}",
        "metrics": metrics,
        "metadata": {
            "script_name": "monitor_and_log.py",
            "python_version": sys.version.split()[0],
            "platform": sys.platform,
            "hostname": os.getenv('HOSTNAME', 'localhost')
        }
    }
    
    try:
        # Enviar el log a Axiom
        response = requests.post(
            ingest_url,
            headers=headers,
            json=[log_data],
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Log de monitoreo enviado - CPU: {metrics.get('cpu_usage', 0):.1f}%, RAM: {metrics.get('memory_usage', 0):.1f}%")
            return True
        else:
            print(f"❌ Error al enviar log: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {str(e)}")
        return False

def simulate_application_logs():
    """Simula logs de aplicación"""
    log_messages = [
        ("🔍 Usuario autenticado correctamente", "INFO"),
        ("📝 Nueva transacción procesada", "INFO"),
        ("⚠️ Tiempo de respuesta lento detectado", "WARN"),
        ("🔄 Reintentando conexión a base de datos", "WARN"),
        ("❌ Error en validación de datos", "ERROR"),
        ("✅ Proceso completado exitosamente", "INFO"),
        ("📊 Reporte generado correctamente", "INFO"),
        ("🔐 Sesión expirada, redirigiendo", "WARN")
    ]
    
    message, level = random.choice(log_messages)
    
    # Obtener variables de entorno de Doppler
    axiom_api_token = os.getenv('AXIOM_API_TOKEN')
    axiom_org_id = os.getenv('AXIOM_ORG_ID')
    axiom_dataset = os.getenv('AXIOM_DATASET', 'test-dataset')
    
    if not axiom_api_token or not axiom_org_id:
        return False
    
    # URL de ingesta de Axiom
    ingest_url = f"https://api.axiom.co/v1/datasets/{axiom_dataset}/ingest"
    
    # Headers para la petición
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {axiom_api_token}',
        'X-Axiom-Org-Id': axiom_org_id
    }
    
    # Crear log de aplicación
    now = datetime.now(timezone.utc)
    
    log_data = {
        "timestamp": now.isoformat(),
        "level": level,
        "message": message,
        "log_type": "application",
        "source": "simulated_app",
        "environment": os.getenv('ENVIRONMENT', 'development'),
        "app_log_id": f"app_{now.strftime('%Y%m%d_%H%M%S')}",
        "user_id": f"user_{random.randint(1000, 9999)}",
        "session_id": f"session_{random.randint(10000, 99999)}",
        "metadata": {
            "script_name": "monitor_and_log.py",
            "simulation": True,
            "random_seed": random.randint(1, 1000)
        }
    }
    
    try:
        # Enviar el log a Axiom
        response = requests.post(
            ingest_url,
            headers=headers,
            json=[log_data],
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"✅ Log de aplicación enviado - {message}")
            return True
        else:
            print(f"❌ Error al enviar log: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {str(e)}")
        return False

def main():
    """Función principal de monitoreo"""
    print("📊 Iniciando Monitor y Logger para Axiom")
    print("=" * 50)
    print(f"📁 Directorio: {os.getcwd()}")
    print(f"🐍 Python: {sys.executable}")
    print("=" * 50)
    
    try:
        for i in range(5):  # Enviar 5 logs de prueba
            print(f"\n🔄 Ciclo {i+1}/5")
            
            # Enviar métricas del sistema
            metrics = get_system_metrics()
            send_monitoring_log(metrics, "system_metrics")
            
            # Simular log de aplicación
            simulate_application_logs()
            
            # Esperar 2 segundos entre logs
            if i < 4:  # No esperar en el último ciclo
                time.sleep(2)
        
        print("\n🎉 ¡Monitoreo completado!")
        print("✅ Todos los logs enviados a Axiom correctamente")
        
    except KeyboardInterrupt:
        print("\n⏹️  Monitoreo interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante el monitoreo: {str(e)}")

if __name__ == "__main__":
    main()
