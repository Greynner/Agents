"""
🌸 Hannah QA Agent - Versión con Logging a Axiom
Usa Modal para procesamiento y Axiom para logging centralizado
"""

import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from utils_axiom import logger as axiom_logger

# Configuración
load_dotenv()

# UI
st.set_page_config(page_title="Hannah QA Agent 🌸", page_icon="🌸")
st.title("🌸 Hannah QA Agent – Generador de Matrices y Casos Gherkin")
st.caption("Desarrollado con IA para automatizar QA desde tus requerimientos.")

st.write("📋 Ingresa un requerimiento y Hannah generará:")
st.markdown("- Una **matriz de pruebas (.xlsx)**")
st.markdown("- Casos **Gherkin (.feature)** listos para BDD")

requerimiento = st.text_area("✍️ Ingrese el requerimiento aquí:", height=120)

if st.button("🚀 Generar Matriz y Casos de Prueba"):
    if not requerimiento.strip():
        st.warning("⚠️ Debes ingresar un requerimiento.")
        axiom_logger.log_info("Intento sin requerimiento")
        st.stop()

    axiom_logger.log_info("Solicitando generación de casos")
    
    try:
        # Intentar usar Modal
        try:
            from hannah_modal_client import call_modal_backend
            st.info("☁️ Usando backend Modal")
            with st.spinner("🤖 Hannah está analizando en la nube..."):
                result = call_modal_backend(requerimiento)
            
            if result["status"] == "success":
                output = result["output"]
                matrix_data = result.get("matrix_data", [])
                gherkin_content = result.get("gherkin_content", "")
            else:
                raise Exception(result.get('error', 'Error desconocido'))
        except (ImportError, Exception) as e:
            # Fallback a OpenAI directo
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            st.info("⚡ Usando OpenAI directo (Modal no disponible)")
            
            # Clase Hannah inline
            class Hannah:
                def __init__(self, client):
                    self.client = client
                
                def generar_pruebas(self, requerimiento):
                    few_shot = """| ID    | Escenario     | Datos de entrada | Resultado esperado |
|-------|---------------|------------------|--------------------|
| TC001 | Login exitoso | Usuario válido   | Acceso concedido   |
| TC002 | Login fallido | Usuario inválido | Mensaje de error   |

Feature: Validar login
  Scenario: Login exitoso
    Given un usuario registrado
    When introduce credenciales correctas
    Then debe acceder exitosamente"""
                    
                    resp = self.client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "Eres Hannah 🌸, un agente de QA que genera matrices de prueba y casos Gherkin."},
                            {"role": "user", "content": f"Ejemplo:\n{few_shot}\n\nRequerimiento:\n{requerimiento}"}
                        ],
                        temperature=0.3
                    )
                    return resp.choices[0].message.content
            
            with st.spinner("🤖 Hannah está generando..."):
                hannah = Hannah(client)
                output = hannah.generar_pruebas(requerimiento)
                
                # Procesar matriz
                rows = []
                for line in output.splitlines():
                    if "|" in line and "---" not in line:
                        cols = [c.strip() for c in line.split("|") if c.strip()]
                        if len(cols) > 1:
                            rows.append(cols)
                
                matrix_data = [dict(zip(rows[0], row)) for row in rows[1:]] if rows and len(rows) > 1 else []
                
                # Procesar Gherkin
                gherkin_lines = []
                capture = False
                for line in output.splitlines():
                    if line.strip().startswith(("Feature", "Scenario")):
                        capture = True
                    if capture:
                        gherkin_lines.append(line)
                gherkin_content = "\n".join(gherkin_lines) if gherkin_lines else ""
        
        st.success("✅ Casos generados correctamente! 🌸")
        st.text_area("🧠 Resultado:", value=output, height=300)
        
        axiom_logger.log_info(f"Casos generados: {len(matrix_data) if 'matrix_data' in locals() and matrix_data else 0}")
        
        # Exportar archivos
        os.makedirs("Outputs", exist_ok=True)
        
        if matrix_data:
            df = pd.DataFrame(matrix_data)
            excel_path = "Outputs/matriz_pruebas.xlsx"
            df.to_excel(excel_path, index=False)
            with open(excel_path, "rb") as f:
                st.download_button("📊 Descargar matriz_pruebas.xlsx", f, "matriz_pruebas.xlsx",
                                 "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            axiom_logger.log_info(f"Excel exportado: {len(df)} filas")
        
        if gherkin_content:
            gherkin_path = "Outputs/casos.feature"
            with open(gherkin_path, "w", encoding="utf-8") as f:
                f.write(gherkin_content)
            with open(gherkin_path, "rb") as f:
                st.download_button("🧾 Descargar casos.feature", f, "casos.feature", "text/plain")
            axiom_logger.log_info("Gherkin exportado")
    
    except Exception as e:
        st.error(f"❌ Error: {e}")
        axiom_logger.log_error(e)

st.divider()
st.caption("🌸 Hannah QA Agent – Powered by Modal, OpenAI & Axiom · Creado por Greynner M.")
