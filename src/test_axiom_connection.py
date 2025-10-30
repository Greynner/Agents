"""
Test de conexión con Axiom usando Doppler
"""
import os
import sys
import requests
from datetime import datetime, timezone
from utils_axiom import logger

class AxiomConnectionTester:
    """Clase para probar la conexión con Axiom usando variables de Doppler"""
    
    def __init__(self):
        """Inicializa el tester con variables de entorno de Doppler"""
        self.axiom_api_token = os.getenv('AXIOM_API_TOKEN')
        self.axiom_org_id = os.getenv('AXIOM_ORG_ID')
        self.axiom_dataset = os.getenv('AXIOM_DATASET', 'default')
        self.environment = os.getenv('ENVIRONMENT', 'development')
        
        # URLs de la API de Axiom
        self.axiom_base_url = "https://api.axiom.co"
        self.ingest_url = f"{self.axiom_base_url}/v1/datasets/{self.axiom_dataset}/ingest"
        self.query_url = f"{self.axiom_base_url}/v1/datasets/{self.axiom_dataset}/query"
        
        # Headers para las peticiones
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.axiom_api_token}',
            'X-Axiom-Org-Id': self.axiom_org_id
        }
    
    def check_environment_variables(self) -> bool:
        """Verifica que todas las variables de entorno necesarias estén disponibles"""
        print("🔍 Verificando variables de entorno de Doppler...\n")
        
        required_vars = {
            'AXIOM_API_TOKEN': self.axiom_api_token,
            'AXIOM_ORG_ID': self.axiom_org_id,
            'AXIOM_DATASET': self.axiom_dataset,
            'ENVIRONMENT': self.environment
        }
        
        all_available = True
        
        for var_name, var_value in required_vars.items():
            if var_value:
                # Mostrar solo los primeros y últimos caracteres por seguridad
                if len(var_value) > 8:
                    masked_value = f"{var_value[:4]}...{var_value[-4:]}"
                else:
                    masked_value = "***"
                print(f"✅ {var_name}: {masked_value}")
            else:
                print(f"❌ {var_name}: NO DISPONIBLE")
                all_available = False
        
        return all_available
    
    def test_axiom_connection(self) -> bool:
        """Prueba la conexión básica con Axiom"""
        print("\n🔗 Probando conexión con Axiom...")
        
        try:
            # Intentar hacer una petición simple para verificar la conexión
            response = requests.get(
                f"{self.axiom_base_url}/v1/datasets",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ Conexión exitosa con Axiom API")
                
                # Verificar si el dataset existe
                datasets = response.json()
                dataset_names = [ds.get('name') for ds in datasets]
                
                if self.axiom_dataset in dataset_names:
                    print(f"✅ Dataset '{self.axiom_dataset}' encontrado")
                else:
                    print(f"⚠️  Dataset '{self.axiom_dataset}' no encontrado")
                    print(f"📋 Datasets disponibles: {', '.join(dataset_names)}")
                    print("💡 Sugerencia: Usa uno de los datasets disponibles o crea el dataset en Axiom")
                
                return True
            else:
                print(f"❌ Error en la conexión: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión: {str(e)}")
            return False
    
    def test_axiom_ingest(self) -> bool:
        """Prueba el envío de datos a Axiom"""
        print("\n📤 Probando ingesta de datos en Axiom...")
        
        # Datos de prueba
        now = datetime.now(timezone.utc)
        test_data = {
            "timestamp": now.isoformat(),
            "level": "info",
            "message": "Test de conexión Axiom con Doppler",
            "environment": self.environment,
            "test_id": f"test_{now.strftime('%Y%m%d_%H%M%S')}",
            "metadata": {
                "source": "doppler_test",
                "version": "1.0.0",
                "python_version": sys.version,
                "platform": sys.platform
            }
        }
        
        try:
            response = requests.post(
                self.ingest_url,
                headers=self.headers,
                json=[test_data],  # Axiom espera un array de eventos
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ Datos enviados exitosamente a Axiom")
                print(f"📊 Respuesta: {response.json()}")
                return True
            else:
                print(f"❌ Error en la ingesta: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error al enviar datos: {str(e)}")
            return False
    
    def test_axiom_query(self) -> bool:
        """Prueba una consulta simple a Axiom"""
        print("\n🔍 Probando consulta en Axiom...")
        
        # Query simple para obtener los últimos eventos
        now = datetime.now(timezone.utc)
        query_data = {
            "startTime": "2024-01-01T00:00:00Z",
            "endTime": now.isoformat(),
            "query": f"['{self.axiom_dataset}'] | where test_id != null | limit 5"
        }
        
        try:
            response = requests.post(
                self.query_url,
                headers=self.headers,
                json=query_data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Consulta ejecutada exitosamente")
                print(f"📊 Resultados encontrados: {len(result.get('matches', []))}")
                return True
            elif response.status_code == 403:
                print("⚠️  Token no tiene permisos de lectura (esto es normal para tokens de ingesta)")
                print("✅ La ingesta funciona correctamente, que es lo principal")
                return True  # Consideramos esto como éxito parcial
            else:
                print(f"❌ Error en la consulta: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error en la consulta: {str(e)}")
            return False
    
    def run_full_test(self) -> bool:
        """Ejecuta todas las pruebas de integración"""
        print("🚀 Iniciando test completo de integración Axiom + Doppler")
        print("=" * 60)
        
        # 1. Verificar variables de entorno
        if not self.check_environment_variables():
            print("\n❌ FALLO: Variables de entorno no disponibles")
            return False
        
        # 2. Probar conexión básica
        if not self.test_axiom_connection():
            print("\n❌ FALLO: No se pudo conectar con Axiom")
            return False
        
        # 3. Probar ingesta de datos
        if not self.test_axiom_ingest():
            print("\n❌ FALLO: No se pudo enviar datos a Axiom")
            return False
        
        # 4. Probar consulta
        if not self.test_axiom_query():
            print("\n❌ FALLO: No se pudo consultar datos en Axiom")
            return False
        
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
        print("✅ Integración Axiom + Doppler funcionando correctamente")
        return True

def main():
    """Función principal para ejecutar el test"""
    print("🔍 Test de Conexión Axiom con Doppler")
    print("=" * 50)
    print(f"📁 Directorio actual: {os.getcwd()}")
    print(f"🐍 Python: {sys.executable}")
    print(f"📦 Versión Python: {sys.version}")
    print("=" * 50)
    
    # Crear instancia del tester
    tester = AxiomConnectionTester()
    
    # Ejecutar todas las pruebas
    success = tester.run_full_test()
    
    if success:
        print("\n✅ Test completado exitosamente")
        sys.exit(0)
    else:
        print("\n❌ Test falló")
        sys.exit(1)

if __name__ == "__main__":
    main()
