# ==============================================
# 🌸 Hannah QA Agent - app.py (versión estable con manejo de errores)
# ==============================================

import os
import pandas as pd
import streamlit as st
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv

# ==============================================
# 1️⃣ CONFIGURACIÓN INICIAL
# ==============================================

# Cargar variables de entorno
load_dotenv()

# Inicializar cliente OpenAI con control de errores
try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    st.error("⚠️ Error al inicializar el cliente OpenAI. Revisa tu archivo .env o la variable OPENAI_API_KEY.")
    st.stop()

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
        # Prompt base
        SYSTEM_PROMPT = """
        Eres Hannah 🌸, una QA Engineer Senior especializada en automatización de pruebas.
        Tu tarea es analizar un requerimiento y generar una matriz de pruebas y casos Gherkin claros y consistentes.
        """

        FEW_SHOT_EXAMPLE = """
        | ID | Escenario | Datos de entrada | Resultado esperado |
        |----|------------|------------------|--------------------|
        | TC001 | Login exitoso | Usuario válido | Acceso concedido |
        | TC002 | Login fallido | Usuario inválido | Mensaje de error "Credenciales inválidas" |

        Feature: Validación de login
          Scenario: Login exitoso
            Given usuario válido
            When ingresa credenciales correctas
            Then muestra "Acceso concedido"
        """

        # ==============================================
        # 4️⃣ LLAMADA A LA API DE OPENAI
        # ==============================================
        with st.spinner("🤖 Hannah está analizando tu requerimiento..."):
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0.3,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"{FEW_SHOT_EXAMPLE}\n\nRequerimiento:\n{requerimiento}"}
                ]
            )

        output = resp.choices[0].message.content
        st.success("✅ Casos de prueba generados correctamente por Hannah.")
        st.text_area("🧠 Resultado de Hannah:", value=output, height=400)

        # ==============================================
        # 5️⃣ PROCESAR RESULTADOS Y EXPORTAR ARCHIVOS
        # ==============================================
        try:
            os.makedirs("Outputs", exist_ok=True)

            # Extraer matriz de prueba
            rows = []
            for line in output.splitlines():
                if "|" in line and "---" not in line:
                    cols = [c.strip() for c in line.split("|") if c.strip()]
                    if len(cols) > 1:
                        rows.append(cols)

            # Guardar matriz en Excel
            if rows:
                df = pd.DataFrame(rows[1:], columns=rows[0])
                matriz_path = "Outputs/matriz_pruebas.xlsx"
                df.to_excel(matriz_path, index=False)

                with open(matriz_path, "rb") as file:
                    st.download_button(
                        label="📊 Descargar matriz_pruebas.xlsx",
                        data=file,
                        file_name="matriz_pruebas.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

            # Extraer y guardar casos Gherkin
            gherkin = []
            capture = False
            for line in output.splitlines():
                if line.strip().startswith(("Feature", "Scenario")):
                    capture = True
                if capture:
                    gherkin.append(line)

            if gherkin:
                gherkin_path = "Outputs/casos.feature"
                with open(gherkin_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(gherkin))

                with open(gherkin_path, "rb") as file:
                    st.download_button(
                        label="🧾 Descargar casos.feature",
                        data=file,
                        file_name="casos.feature",
                        mime="text/plain"
                    )

        except Exception as e:
            st.error(f"⚠️ Error al generar o exportar archivos: {e}")

    except OpenAIError as e:
        st.error(f"❌ Error al conectar con OpenAI: {e}")
    except Exception as e:
        st.error(f"⚠️ Ocurrió un error inesperado: {e}")

# ==============================================
# 6️⃣ PIE DE PÁGINA
# ==============================================
st.divider()
st.caption("🌸 Hannah QA Agent – Powered by OpenAI · Creado por Greynner M.")
