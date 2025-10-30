"""
Hannah MS Agent - Agente especializado en pruebas de microservicios
Versión simplificada para APIs REST
"""

import os
import pandas as pd
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from io import BytesIO

# Configuración
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# UI
st.set_page_config(page_title="Hannah MS Agent", page_icon="🤖")

st.title("🤖 Hannah MS Agent")
st.caption("Agente de QA especializado en pruebas de microservicios (API REST).")

requerimiento = st.text_area(
    "Ingresa el requerimiento técnico o funcional del microservicio:",
    placeholder="Ejemplo: Validar que el endpoint GET /api/v1/clientes/{id} retorne 200 con datos válidos y 404 si el cliente no existe.",
    height=120
)

if st.button("🚀 Generar Casos de Prueba"):
    if not requerimiento.strip():
        st.warning("⚠️ Debes ingresar un requerimiento antes de continuar.")
        st.stop()

    prompt = f"""Eres un QA Engineer experto en pruebas de microservicios (API REST).

A partir del siguiente requerimiento:
{requerimiento}

Genera:
1. Una matriz de pruebas en formato de tabla Markdown con las columnas:
| ID | Endpoint | Método | Descripción | Datos de entrada | Código esperado | Resultado esperado |
Incluye al menos 5 escenarios: exitoso, error 400, error 500, payload inválido y respuesta vacía.

2. Los casos Gherkin (.feature) correspondientes para automatización."""

    try:
        with st.spinner("🤖 Generando casos de prueba..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Eres un QA Engineer experto en validación de microservicios REST."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            output = response.choices[0].message.content
        
        st.success("✅ Casos generados correctamente.")
    except Exception as e:
        st.error(f"❌ Error generando los casos: {e}")
        st.stop()

    # Procesar matriz de pruebas
    st.subheader("📊 Resultado generado")
    st.text_area("🧠 Output:", value=output, height=300)
    
    rows = []
    for line in output.splitlines():
        if "|" in line and "---" not in line:
            cols = [c.strip() for c in line.split("|") if c.strip()]
            if len(cols) > 1:
                rows.append(cols)

    if rows:
        df = pd.DataFrame(rows[1:], columns=rows[0])
        st.subheader("📑 Matriz de Pruebas")
        st.dataframe(df)
        
        os.makedirs("Outputs", exist_ok=True)
        excel_path = "Outputs/matriz_ms.xlsx"
        df.to_excel(excel_path, index=False)
        with open(excel_path, "rb") as f:
            st.download_button("📥 Descargar matriz_ms.xlsx", f, "matriz_ms.xlsx",
                             "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Procesar casos Gherkin
    gherkin_lines = []
    capture = False
    for line in output.splitlines():
        if line.strip().startswith(("Feature", "Scenario")):
            capture = True
        if capture:
            gherkin_lines.append(line)

    if gherkin_lines:
        gherkin_content = "\n".join(gherkin_lines)
        st.subheader("🧾 Casos Gherkin")
        st.code(gherkin_content, language="gherkin")
        
        gherkin_path = "Outputs/casos_ms.feature"
        with open(gherkin_path, "w", encoding="utf-8") as f:
            f.write(gherkin_content)
        with open(gherkin_path, "rb") as f:
            st.download_button("📥 Descargar casos_ms.feature", f, "casos_ms.feature", "text/plain")
