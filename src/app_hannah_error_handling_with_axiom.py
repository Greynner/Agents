# ==============================================
# 🌸 Hannah QA Agent - Con Logging a Axiom
# ==============================================

import os
import pandas as pd
import streamlit as st
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
import modal
import requests
import json
from datetime import datetime, timezone
import traceback

# ==============================================
# 1️⃣ CONFIGURACIÓN INICIAL
# ==============================================

# Cargar variables de entorno
load_dotenv()

# Importar cliente de Modal
from hannah_modal_client import call_modal_backend

# ==============================================
# 2️⃣ CLASE PARA LOGGING A AXIOM
# ==============================================

class AxiomLogger:
    """Clase para enviar logs a Axiom usando variables de Doppler"""
    
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
    
    def log_event(self, level, message, user_action=None, error_details=None, metadata=None):
        """Envía un log a Axiom"""
        
        if not self.axiom_api_token or not self.axiom_org_id:
            # Si no hay configuración de Axiom, solo imprimir
            print(f"[{level}] {message}")
            return False
        
        try:
            now = datetime.now(timezone.utc)
            
            log_data = {
                "timestamp": now.isoformat(),
                "level": level.upper(),
                "message": message,
                "source": "hannah_qa_agent",
                "environment": self.environment,
                "session_id": f"session_{now.strftime('%Y%m%d_%H%M%S')}",
                "metadata": {
                    "app_name": "Hannah QA Agent",
                    "version": "2.0.0",
                    "platform": "streamlit",
                    "user_action": user_action,
                    "error_details": error_details,
                    **(metadata or {})
                }
            }
            
            # Enviar a Axiom
            response = requests.post(
                self.ingest_url,
                headers=self.headers,
                json=[log_data],
                timeout=5
            )
            
            if response.status_code == 200:
                print(f"✅ Log enviado a Axiom: {message}")
                return True
            else:
                print(f"⚠️ Error enviando log a Axiom: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error en logging: {str(e)}")
            return False
    
    def log_user_interaction(self, action, details=None):
        """Log específico para interacciones del usuario"""
        self.log_event(
            "INFO", 
            f"Usuario {action}", 
            user_action=action,
            metadata=details
        )
    
    def log_error(self, error, context=None):
        """Log específico para errores"""
        self.log_event(
            "ERROR",
            f"Error en Hannah QA Agent: {str(error)}",
            error_details={
                "error_type": type(error).__name__,
                "error_message": str(error),
                "context": context,
                "traceback": traceback.format_exc()
            }
        )
    
    def log_success(self, action, details=None):
        """Log específico para acciones exitosas"""
        self.log_event(
            "INFO",
            f"✅ {action} completado exitosamente",
            user_action=action,
            metadata=details
        )

# Inicializar logger
axiom_logger = AxiomLogger()

# ==============================================
# 3️⃣ INTERFAZ DE USUARIO
# ==============================================

st.set_page_config(page_title="Hannah QA Agent 🌸", page_icon="🌸", layout="centered")
st.title(" Hannah QA Agent – Generador de Matrices de Prueba y Casos Gherkin")
st.caption("Desarrollado con IA y amor 💜 para automatizar QA desde tus requerimientos.")

st.divider()
st.write("📋 Ingresa un requerimiento funcional o historia de usuario y Hannah generará automáticamente:")
st.markdown("- Una **matriz de pruebas (.xlsx)**")
st.markdown("- Casos **Gherkin (.feature)** listos para tu framework BDD")

# Indicador de Modal y Axiom
st.info("☁️ **Backend:** Modal (Serverless) | 🔐 **Variables:** Doppler | 📊 **Logs:** Axiom")

# Log de inicio de sesión
axiom_logger.log_user_interaction("inició sesión en Hannah QA Agent")

# Campo de texto del usuario
requerimiento = st.text_area("✍️ Ingrese el requerimiento aquí:", height=180)

# ==============================================
# 4️⃣ BOTÓN PRINCIPAL
# ==============================================

if st.button("🚀 Generar Matriz de prueba y  Casos de Prueba"):
    if not requerimiento.strip():
        st.warning("⚠️ Debes ingresar un requerimiento antes de continuar.")
        axiom_logger.log_user_interaction("intentó generar sin requerimiento")
        st.stop()

    # Log del requerimiento del usuario
    axiom_logger.log_user_interaction(
        "solicitó generación de casos de prueba",
        {
            "requerimiento_length": len(requerimiento),
            "requerimiento_preview": requerimiento[:100] + "..." if len(requerimiento) > 100 else requerimiento
        }
    )

    try:
        # ==============================================
        # 5️⃣ LLAMADA A MODAL (BACKEND SERVERLESS)
        # ==============================================
        with st.spinner("🤖 Hannah está analizando tu requerimiento en la nube..."):
            # Log de inicio de procesamiento
            axiom_logger.log_event("INFO", "Iniciando procesamiento en Modal", user_action="modal_processing_start")
            
            # Llamar a la función de Modal
            result = call_modal_backend(requerimiento)
        
        # Verificar el resultado
        if result["status"] == "success":
            output = result["output"]
            matrix_data = result["matrix_data"]
            gherkin_content = result["gherkin_content"]
            
            st.success("✅ Casos de prueba generados correctamente por Hannah en Modal! 🌸")
            st.text_area("🧠 Resultado de Hannah:", value=output, height=400)
            
            # Log de éxito
            axiom_logger.log_success(
                "generación de casos de prueba en Modal",
                {
                    "casos_generados": len(matrix_data) if matrix_data else 0,
                    "gherkin_generado": bool(gherkin_content),
                    "output_length": len(output)
                }
            )
            
            # Mostrar información adicional
            st.info(f"📊 Se generaron {len(matrix_data)} casos de prueba")
            if gherkin_content:
                st.info("🧾 Casos Gherkin generados correctamente")
        else:
            error_msg = result.get('error', 'Error desconocido')
            st.error(f"❌ Error en Modal: {error_msg}")
            
            # Log de error de Modal
            axiom_logger.log_error(
                Exception(f"Error en Modal: {error_msg}"),
                context="modal_backend_call"
            )
            st.stop()

        # ==============================================
        # 6️⃣ PROCESAR RESULTADOS Y EXPORTAR ARCHIVOS
        # ==============================================
        try:
            os.makedirs("Outputs", exist_ok=True)

            # Usar datos de Modal para crear Excel
            if matrix_data and len(matrix_data) > 0:
                df = pd.DataFrame(matrix_data)
                matriz_path = "Outputs/matriz_pruebas.xlsx"
                df.to_excel(matriz_path, index=False)

                with open(matriz_path, "rb") as file:
                    st.download_button(
                        label="📊 Descargar matriz_pruebas.xlsx",
                        data=file,
                        file_name="matriz_pruebas.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                
                # Log de exportación exitosa
                axiom_logger.log_success(
                    "exportación de matriz de pruebas",
                    {"archivo": "matriz_pruebas.xlsx", "filas": len(df)}
                )

            # Usar contenido Gherkin de Modal
            if gherkin_content:
                gherkin_path = "Outputs/casos.feature"
                with open(gherkin_path, "w", encoding="utf-8") as f:
                    f.write(gherkin_content)

                with open(gherkin_path, "rb") as file:
                    st.download_button(
                        label="🧾 Descargar casos.feature",
                        data=file,
                        file_name="casos.feature",
                        mime="text/plain"
                    )
                
                # Log de exportación exitosa
                axiom_logger.log_success(
                    "exportación de casos Gherkin",
                    {"archivo": "casos.feature", "contenido_length": len(gherkin_content)}
                )

        except Exception as e:
            st.error(f"⚠️ Error al generar o exportar archivos: {e}")
            axiom_logger.log_error(e, context="file_export")

    except Exception as e:
        st.error(f"⚠️ Ocurrió un error inesperado: {e}")
        axiom_logger.log_error(e, context="main_processing")

# ==============================================
# 7️⃣ PIE DE PÁGINA
# ==============================================
st.divider()
st.caption("🌸 Hannah QA Agent – Powered by Modal, OpenAI & Axiom · Creado por Greynner M.")

# Log de fin de sesión
axiom_logger.log_user_interaction("finalizó sesión en Hannah QA Agent")
