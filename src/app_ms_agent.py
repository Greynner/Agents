import os
import pandas as pd
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from io import BytesIO

# === Configuración inicial ===
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Hannah MS Agent", layout="wide")

st.title("Hannah MS Agent")
st.caption("Agente de QA especializado en pruebas de microservicios (API REST).")

# === Entrada del requerimiento ===
requerimiento = st.text_area(
    "Ingresa el requerimiento técnico o funcional del microservicio:",
    placeholder="Ejemplo: Validar que el endpoint GET /api/v1/clientes/{id} retorne 200 con datos válidos y 404 si el cliente no existe.",
    height=150
)

# === Botón principal ===
if st.button("Generar Casos de Prueba"):
    if not requerimiento.strip():
        st.warning("Debes ingresar un requerimiento antes de continuar.")
        st.stop()

    # === Prompt del modelo ===
    prompt = f"""
    Eres un QA Engineer experto en pruebas de microservicios (API REST).

    A partir del siguiente requerimiento:
    ---
    {requerimiento}
    ---

    Genera:
    1. Una matriz de pruebas en formato de tabla Markdown con las columnas:
    | ID | Endpoint | Método | Descripción | Datos de entrada | Código esperado | Resultado esperado |
    Incluye al menos 5 escenarios: exitoso, error 400, error 500, payload inválido y respuesta vacía.

    2. Los casos Gherkin (.feature) correspondientes para automatización.
    Usa el formato Cucumber estándar con lenguaje Gherkin.
    """

    with st.spinner("Generando casos de prueba con OpenAI..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Eres un QA Engineer experto en validación de microservicios REST."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            output = response.choices[0].message.content
            st.success("Casos generados correctamente.")
        except Exception as e:
            st.error(f"Error generando los casos: {e}")
            st.stop()

    # === Procesar y mostrar la matriz de prueba ===
    table_lines = []
    capture = False
    for line in output.splitlines():
        if "|" in line:
            capture = True
        if capture:
            if line.strip() == "":
                break
            table_lines.append(line)

    if table_lines:
        table_text = "\n".join(table_lines)

        # Detectar encabezados y filas de forma robusta
        lines = table_text.split("\n")
        if len(lines) > 2:
            headers = [h.strip() for h in lines[1].split("|")[1:-1]]
            data = [[c.strip() for c in r.split("|")[1:-1]] for r in lines[2:] if "|" in r]
        else:
            headers = ["ID", "Endpoint", "Método", "Descripción", "Datos de entrada", "Código esperado", "Resultado esperado"]
            data = []

        df = pd.DataFrame(data, columns=headers)
        st.subheader("Matriz de Pruebas (formato tabular)")
        st.dataframe(df, use_container_width=True)

        # Exportar a Excel
        excel_buffer = BytesIO()
        df.to_excel(excel_buffer, index=False)
        excel_buffer.seek(0)
        st.download_button(
            label="Descargar matriz de pruebas (.xlsx)",
            data=excel_buffer,
            file_name="matriz_ms.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("No se detectó tabla de matriz de prueba en el resultado.")

    # === Exportar los escenarios Gherkin ===
    gherkin_lines = []
    capture = False
    for line in output.splitlines():
        if line.strip().startswith(("Feature", "Scenario")):
            capture = True
        if capture:
            gherkin_lines.append(line)

    if gherkin_lines:
        feature_content = "\n".join(gherkin_lines)
        st.subheader("Casos Gherkin generados")
        st.code(feature_content, language="gherkin")

        st.download_button(
            label="Descargar casos Gherkin (.feature)",
            data=feature_content,
            file_name="casos_ms.feature",
            mime="text/plain"
        )
    else:
        st.warning("No se detectaron casos Gherkin en el resultado.")
