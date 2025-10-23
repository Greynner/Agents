# ==============================================
# 🌸 Hannah QA Agent - app.py (versión estable con manejo de errores)
# ==============================================

import os
import pandas as pd
import streamlit as st
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
import modal

# ==============================================
# 1️⃣ CONFIGURACIÓN INICIAL
# ==============================================

# Cargar variables de entorno
load_dotenv()

# Importar cliente de Modal
from hannah_modal_client import call_modal_backend

# ==============================================
# 2️⃣ INTERFAZ DE USUARIO
# ==============================================

st.set_page_config(page_title="Hannah QA Agent 🌸", page_icon="🌸", layout="centered")
st.title(" Hannah QA Agent – Generador de Matrices de Prueba y Casos Gherkin")
st.caption("Desarrollado con IA y amor 💜 para automatizar QA desde tus requerimientos.")

st.divider()
st.write("📋 Ingresa un requerimiento funcional o historia de usuario y Hannah generará automáticamente:")
st.markdown("- Una **matriz de pruebas (.xlsx)**")
st.markdown("- Casos **Gherkin (.feature)** listos para tu framework BDD")

# Indicador de Modal
st.info("☁️ **Backend:** Ejecutándose en Modal (Serverless Cloud) | 🔐 **Variables:** Doppler Secure")

# Campo de texto del usuario
requerimiento = st.text_area("✍️ Ingrese el requerimiento aquí:", height=180)

# ==============================================
# 3️⃣ BOTÓN PRINCIPAL
# ==============================================

if st.button("🚀 Generar Matriz de prueba y  Casos de Prueba"):
    if not requerimiento.strip():
        st.warning("⚠️ Debes ingresar un requerimiento antes de continuar.")
        st.stop()

    try:
        # ==============================================
        # 4️⃣ LLAMADA A MODAL (BACKEND SERVERLESS)
        # ==============================================
        with st.spinner("🤖 Hannah está analizando tu requerimiento en la nube..."):
            # Llamar a la función de Modal
            result = call_modal_backend(requerimiento)
        
        # Verificar el resultado
        if result["status"] == "success":
            output = result["output"]
            matrix_data = result["matrix_data"]
            gherkin_content = result["gherkin_content"]
            
            st.success("✅ Casos de prueba generados correctamente por Hannah en Modal! 🌸")
            st.text_area("🧠 Resultado de Hannah:", value=output, height=400)
            
            # Mostrar información adicional
            st.info(f"📊 Se generaron {len(matrix_data)} casos de prueba")
            if gherkin_content:
                st.info("🧾 Casos Gherkin generados correctamente")
        else:
            st.error(f"❌ Error en Modal: {result.get('error', 'Error desconocido')}")
            st.stop()

        # ==============================================
        # 5️⃣ PROCESAR RESULTADOS Y EXPORTAR ARCHIVOS
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

        except Exception as e:
            st.error(f"⚠️ Error al generar o exportar archivos: {e}")

    except Exception as e:
        st.error(f"⚠️ Ocurrió un error inesperado: {e}")

# ==============================================
# 6️⃣ PIE DE PÁGINA
# ==============================================
st.divider()
st.caption("🌸 Hannah QA Agent – Powered by Modal & OpenAI · Creado por Greynner M.")
