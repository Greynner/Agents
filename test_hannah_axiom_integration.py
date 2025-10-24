#!/usr/bin/env python3
"""
🧪 Test de Integración Hannah QA Agent + Axiom
Verifica que el logging a Axiom funcione correctamente en la aplicación Hannah
"""

import os
import sys
import requests
import json
from datetime import datetime, timezone

class HannahAxiomTester:
    """Tester para verificar la integración Hannah + Axiom"""
    
    def __init__(self):
        self.axiom_api_token = os.getenv('AXIOM_API_TOKEN')
        self.axiom_org_id = os.getenv('AXIOM_ORG_ID')
        self.axiom_dataset = os.getenv('AXIOM_DATASET', 'hannah-qa-agent')
        self.environment = os.getenv('ENVIRONMENT', 'development')
        
        # URLs de Axiom
        self.axiom_base_url = "https://api.axiom.co"
        self.ingest_url = f"{self.axiom_base_url}/v1/datasets/{self.axiom_dataset}/ingest"
        
        # Headers
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.axiom_api_token}',
            'X-Axiom-Org-Id': self.axiom_org_id
        }
    
    def test_axiom_connection(self):
        """Prueba la conexión con Axiom"""
        print("🔗 Probando conexión con Axiom...")
        
        try:
            response = requests.get(
                f"{self.axiom_base_url}/v1/datasets",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ Conexión exitosa con Axiom API")
                return True
            else:
                print(f"❌ Error en la conexión: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión: {str(e)}")
            return False
    
    def test_hannah_logging(self):
        """Prueba el logging específico de Hannah"""
        print("\n📤 Probando logging de Hannah QA Agent...")
        
        # Simular logs típicos de Hannah
        test_logs = [
            {
                "level": "INFO",
                "message": "Usuario inició sesión en Hannah QA Agent",
                "user_action": "inició sesión",
                "metadata": {"session_type": "new"}
            },
            {
                "level": "INFO", 
                "message": "Usuario solicitó generación de casos de prueba",
                "user_action": "solicitó generación",
                "metadata": {
                    "requerimiento_length": 150,
                    "requerimiento_preview": "Como usuario quiero..."
                }
            },
            {
                "level": "INFO",
                "message": "Iniciando procesamiento en Modal",
                "user_action": "modal_processing_start",
                "metadata": {"backend": "modal", "status": "processing"}
            },
            {
                "level": "INFO",
                "message": "✅ generación de casos de prueba en Modal completado exitosamente",
                "user_action": "generación exitosa",
                "metadata": {
                    "casos_generados": 5,
                    "gherkin_generado": True,
                    "output_length": 1200
                }
            },
            {
                "level": "INFO",
                "message": "✅ exportación de matriz de pruebas completado exitosamente",
                "user_action": "exportación exitosa",
                "metadata": {
                    "archivo": "matriz_pruebas.xlsx",
                    "filas": 5
                }
            },
            {
                "level": "ERROR",
                "message": "Error en Hannah QA Agent: Error en Modal: Timeout",
                "error_details": {
                    "error_type": "TimeoutError",
                    "error_message": "Error en Modal: Timeout",
                    "context": "modal_backend_call"
                }
            }
        ]
        
        success_count = 0
        
        for i, log_data in enumerate(test_logs, 1):
            print(f"\n📝 Enviando log {i}/{len(test_logs)}: {log_data['message'][:50]}...")
            
            # Crear log completo
            now = datetime.now(timezone.utc)
            full_log = {
                "timestamp": now.isoformat(),
                "level": log_data["level"],
                "message": log_data["message"],
                "source": "hannah_qa_agent",
                "environment": self.environment,
                "session_id": f"test_session_{now.strftime('%Y%m%d_%H%M%S')}",
                "metadata": {
                    "app_name": "Hannah QA Agent",
                    "version": "2.0.0",
                    "platform": "test_script",
                    "user_action": log_data.get("user_action"),
                    "error_details": log_data.get("error_details"),
                    **(log_data.get("metadata", {}))
                }
            }
            
            try:
                response = requests.post(
                    self.ingest_url,
                    headers=self.headers,
                    json=[full_log],
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Log {i} enviado exitosamente")
                    print(f"   📊 Eventos ingeridos: {result.get('ingested', 0)}")
                    success_count += 1
                else:
                    print(f"❌ Error en log {i}: {response.status_code} - {response.text}")
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ Error de conexión en log {i}: {str(e)}")
        
        print(f"\n📊 Resumen: {success_count}/{len(test_logs)} logs enviados exitosamente")
        return success_count == len(test_logs)
    
    def test_workflow_simulation(self):
        """Simula un flujo completo de trabajo de Hannah"""
        print("\n🎭 Simulando flujo completo de Hannah QA Agent...")
        
        workflow_logs = [
            {
                "message": "Usuario inició sesión en Hannah QA Agent",
                "level": "INFO",
                "action": "session_start"
            },
            {
                "message": "Usuario ingresó requerimiento: 'Como usuario quiero gestionar productos'",
                "level": "INFO", 
                "action": "requirement_input",
                "metadata": {"requirement_length": 45}
            },
            {
                "message": "Iniciando procesamiento en Modal",
                "level": "INFO",
                "action": "modal_processing_start"
            },
            {
                "message": "✅ Casos de prueba generados: 8 casos",
                "level": "INFO",
                "action": "generation_success",
                "metadata": {"cases_count": 8, "gherkin_generated": True}
            },
            {
                "message": "✅ Archivos exportados: matriz_pruebas.xlsx, casos.feature",
                "level": "INFO",
                "action": "export_success",
                "metadata": {"files_exported": 2}
            },
            {
                "message": "Usuario finalizó sesión en Hannah QA Agent",
                "level": "INFO",
                "action": "session_end"
            }
        ]
        
        print("📋 Flujo simulado:")
        for i, log in enumerate(workflow_logs, 1):
            print(f"   {i}. {log['message']}")
        
        # Enviar todos los logs del flujo
        success_count = 0
        for log in workflow_logs:
            now = datetime.now(timezone.utc)
            full_log = {
                "timestamp": now.isoformat(),
                "level": log["level"],
                "message": log["message"],
                "source": "hannah_qa_agent",
                "environment": self.environment,
                "session_id": f"workflow_{now.strftime('%Y%m%d_%H%M%S')}",
                "metadata": {
                    "app_name": "Hannah QA Agent",
                    "version": "2.0.0",
                    "platform": "workflow_simulation",
                    "user_action": log["action"],
                    **(log.get("metadata", {}))
                }
            }
            
            try:
                response = requests.post(
                    self.ingest_url,
                    headers=self.headers,
                    json=[full_log],
                    timeout=5
                )
                
                if response.status_code == 200:
                    success_count += 1
                else:
                    print(f"⚠️ Error en flujo: {response.status_code}")
                    
            except Exception as e:
                print(f"⚠️ Error en flujo: {str(e)}")
        
        print(f"✅ Flujo simulado: {success_count}/{len(workflow_logs)} logs enviados")
        return success_count == len(workflow_logs)
    
    def run_full_test(self):
        """Ejecuta todas las pruebas"""
        print("🧪 Test de Integración Hannah QA Agent + Axiom")
        print("=" * 60)
        print(f"📁 Directorio: {os.getcwd()}")
        print(f"🐍 Python: {sys.executable}")
        print(f"📊 Dataset: {self.axiom_dataset}")
        print("=" * 60)
        
        # 1. Verificar variables de entorno
        print("\n🔍 Verificando variables de entorno...")
        if not self.axiom_api_token and self.axiom_org_id:
            print("❌ Variables de Axiom no disponibles")
            return False
        print("✅ Variables de entorno disponibles")
        
        # 2. Probar conexión
        if not self.test_axiom_connection():
            print("\n❌ FALLO: No se pudo conectar con Axiom")
            return False
        
        # 3. Probar logging específico de Hannah
        if not self.test_hannah_logging():
            print("\n❌ FALLO: Logging de Hannah no funcionó correctamente")
            return False
        
        # 4. Simular flujo completo
        if not self.test_workflow_simulation():
            print("\n❌ FALLO: Simulación de flujo no funcionó")
            return False
        
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
        print("✅ Integración Hannah QA Agent + Axiom funcionando correctamente")
        return True

def main():
    """Función principal"""
    tester = HannahAxiomTester()
    success = tester.run_full_test()
    
    if success:
        print("\n✅ Test completado exitosamente")
        sys.exit(0)
    else:
        print("\n❌ Test falló")
        sys.exit(1)

if __name__ == "__main__":
    main()
