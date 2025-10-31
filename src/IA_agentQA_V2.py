"""
🌸 Hannah QA Agent - Versión con Modal Backend
Aplicación simplificada que usa Modal para procesamiento en la nube
"""

import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Configuración
load_dotenv()

# UI
st.set_page_config(page_title="Hannah QA Agent 🌸", page_icon="🌸")
st.title("🌸 Hannah QA Agent – Generador de Matrices de Prueba y Casos Gherkin")
st.caption("Desarrollado con IA y amor 💜 para automatizar QA desde tus requerimientos.")

st.write("📋 Ingresa un requerimiento funcional o historia de usuario y Hannah generará automáticamente:")
st.markdown("- Una **matriz de pruebas (.xlsx)**")
st.markdown("- Casos **Gherkin (.feature)** listos para tu framework BDD")

requerimiento = st.text_area("✍️ Ingrese el requerimiento aquí:", height=150)

if st.button("🚀 Generar Matriz de Prueba y Casos de Prueba"):
    if not requerimiento.strip():
        st.warning("⚠️ Debes ingresar un requerimiento antes de continuar.")
        st.stop()

    try:
        # Intentar usar Modal, si falla usar OpenAI directo
        try:
            from hannah_modal_client import call_modal_backend
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
            
            # Sistema de prompts similar a app.py
            class Hannah:
                def __init__(self, client):
                    self.client = client
                
                def generar_pruebas(self, requerimiento):
                    few_shot_example = """
Ejemplo de matriz de prueba:
| ID    | Escenario                  | Datos de entrada        | Resultado esperado               |
|-------|----------------------------|-------------------------|----------------------------------|
| TC001 | Login exitoso              | Usuario válido          | Acceso concedido                 |
| TC002 | Login fallido              | Usuario inválido        | Mensaje de error                 |

Ejemplo de casos Gherkin:
Feature: Validar login de usuarios
  Scenario: Usuario válido accede con credenciales correctas
    Given un usuario registrado
    When introduce usuario y contraseña válidos
    Then debe acceder exitosamente al sistema
"""
                    resp = self.client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "Eres Hannah 🌸, un agente de QA que genera matrices de prueba y casos Gherkin."},
                            {"role": "user", "content": "Ejemplo:\n" + few_shot_example + "\n\nRequerimiento:\n" + requerimiento}
                        ],
                        temperature=0.3
                    )
                    return resp.choices[0].message.content
            
            with st.spinner("🤖 Hannah está generando las pruebas..."):
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
        
        st.success("✅ Casos de prueba generados correctamente! 🌸")
        st.text_area("🧠 Resultado de Hannah:", value=output, height=300)
        
        # Exportar archivos
        os.makedirs("Outputs", exist_ok=True)
        
        if matrix_data:
            df = pd.DataFrame(matrix_data)
            matriz_path = "Outputs/matriz_pruebas.xlsx"
            df.to_excel(matriz_path, index=False)
            with open(matriz_path, "rb") as f:
                st.download_button("📊 Descargar matriz_pruebas.xlsx", f, "matriz_pruebas.xlsx",
                                 "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        
        if gherkin_content:
            gherkin_path = "Outputs/casos.feature"
            with open(gherkin_path, "w", encoding="utf-8") as f:
                f.write(gherkin_content)
            with open(gherkin_path, "rb") as f:
                st.download_button("🧾 Descargar casos.feature", f, "casos.feature", "text/plain")

    except Exception as e:
        st.error(f"❌ Error: {e}")

st.divider()
st.caption("🌸 Hannah QA Agent – Powered by Modal & OpenAI · Creado por Greynner M.")
