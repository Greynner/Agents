🌸 Hannah – AI-powered QA Agent

Hannah es un agente de QA impulsado por IA que transforma un requerimiento (HDU / historia de usuario) en:
	•	📑 Matriz de pruebas en Excel
	•	🧪 Casos Gherkin (Cucumber) listos para automatización

✅ Diseñada para ahorrar tiempo a equipos QA y aumentar la cobertura de pruebas.


🚀 Demo online

🔗 Demo en Streamlit (ejemplo, ajusta con tu link real cuando despliegues)

Interfaz sencilla de Hannah en Streamlit: ingresas un requerimiento y obtienes la matriz + casos descargables

⚙️ Cómo usar localmente
1. Clonar el repo
git clone https://github.com/tu-usuario/IA-Agent_QA.git
cd IA-Agent_QA

2. Crear entorno virtual (ejemplo con conda)
conda create -n qa-agent python=3.11
conda activate qa-agent

3. Instalar dependencias
pip install -r requirements.txt

4. Configurar tu API Key
Crea un archivo .env en la raíz con:
OPENAI_API_KEY=sk-xxxxxx_tu_api_key

5. Ejecutar el frontend
streamlit run app.py
La app se abrirá en http://localhost:8501 🚀


📌 Ejemplo de requerimiento
HDU: [Web] Validar flujo de inicio de sesión en la banca digital

Objetivo:
- Permitir acceso con credenciales válidas
- Bloquear al usuario tras 3 intentos fallidos
- Mostrar error con credenciales incorrectas

Criterios de aceptación:
1. Usuario válido → acceso correcto
2. Usuario inválido → mensaje “Credenciales incorrectas”
3. 3 intentos fallidos → cuenta bloqueada

🔎 Salida esperada:
	•	Una tabla con TC001, TC002, TC003…
	•	Escenarios en formato Gherkin:

  Feature: Validar login
  Scenario: Login exitoso
    Given un usuario válido
    When introduce credenciales correctas
    Then accede exitosamente


 ## 📂 Project Structure
 
IA-Agent_QA/
├── hannah_agent.ipynb   # Notebook (backend, pruebas de prompts)
├── app.py               # Frontend en Streamlit
├── requirements.txt     # Dependencias del proyecto
├── .env                 # (ignorado en git) contiene tu API key
├── README.md            # Documentación principal
└── docs/
└── demo_ui.png      # Screenshot de la demo en Streamlit


📈 Roadmap
	•	🔜 Integración con Jira / Confluence
	•	🔜 Dashboard con métricas de cobertura QA
	•	🔜 Extensión a pruebas automáticas E2E


👨‍💻 Autor

Greynner Moreno
QA Engineer & AI Entrepreneur 🇨🇱 | Construyendo el futuro del QA con IA

⸻


