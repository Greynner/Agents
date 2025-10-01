import streamlit as st
from openai import OpenAI
import pandas as pd
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
client = OpenAI()

# =====================
# Clase Hannah 🌸
# =====================
class Hannah:
    def __init__(self, client):
        self.client = client

    def generar_pruebas(self, requerimiento, few_shot_example):
        resp = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres Hannah 🌸, un agente de QA que genera matrices de prueba y casos Gherkin."},
                {"role": "user", "content": "Ejemplo:\n" + few_shot_example + "\n\nRequerimiento:\n" + requerimiento}
            ],
            temperature=0.3
        )
        return resp.choices[0].message.content


# =====================
# Ejemplo few-shot (formato esperado)
# =====================
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

# =====================
# Interfaz con Streamlit
# =====================
st.set_page_config(page_title="Hannah 🌸 - QA Agent", page_icon="🌸")

st.title("🌸 Hannah – QA Agent with AI")
st.write("Transforma un requerimiento en **matriz de pruebas** y **casos Gherkin** listos para automatización.")

# Input de usuario
requerimiento = st.text_area("✍️ Ingresa tu requerimiento (HDU / historia de usuario):")

if st.button("Generar pruebas"):
    hannah = Hannah(client)
    output = hannah.generar_pruebas(requerimiento, few_shot_example)

    st.subheader("📊 Resultado generado por Hannah 🌸")
    st.text(output)

    # Procesar tabla en pandas
    rows = []
    for line in output.splitlines():
        if "|" in line and "---" not in line:
            cols = [c.strip() for c in line.split("|") if c.strip()]
            if len(cols) > 1:
                rows.append(cols)

    if rows:
        df = pd.DataFrame(rows[1:], columns=rows[0])
        st.write("### 📑 Matriz de pruebas")
        st.dataframe(df)

        # Descargar Excel
        excel_file = "matriz_pruebas.xlsx"
        df.to_excel(excel_file, index=False)
        with open(excel_file, "rb") as f:
            st.download_button("📥 Descargar matriz Excel", f, file_name=excel_file)

    # Procesar casos Gherkin
    gherkin = []
    capture = False
    for line in output.splitlines():
        if line.strip().startswith(("Feature", "Scenario")):
            capture = True
        if capture:
            gherkin.append(line)

    if gherkin:
        gherkin_file = "casos.feature"
        with open(gherkin_file, "w", encoding="utf-8") as f:
            f.write("\n".join(gherkin))

        with open(gherkin_file, "rb") as f:
            st.download_button("📥 Descargar casos Gherkin", f, file_name=gherkin_file)
