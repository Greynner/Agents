# ⚡ Comandos Rápidos - Hannah QA Agent

## 🎯 Resumen de Comandos

### 📱 Apps Principales (Streamlit)

```bash
# 🌸 App Básica
doppler run -- streamlit run src/app.py

# ☁️ App con Modal  
doppler run -- streamlit run src/app_hannah_error_handling.py

# 📊 App con Modal + Axiom
doppler run -- streamlit run src/app_hannah_error_handling_with_axiom.py

# 🤖 App Microservicios
doppler run -- streamlit run src/app_ms_agent.py
```

### 🌸 IA_agentQA_V3.py - Versión Unificada (Doppler + OpenAI + Modal + Axiom + Vercel)

```bash
# 🧪 Ejecución local (prueba)
doppler run -- python src/IA_agentQA_V3.py

# 🚀 Desplegar a Modal (producción)
modal deploy src/IA_agentQA_V3.py

# 📝 Ejecutar función Modal localmente
doppler run -- modal run src/IA_agentQA_V3.py::generate_test_matrix_and_gherkin --requirement "Tu requerimiento aquí"

# ⚡ Sin Doppler (usando .env)
python src/IA_agentQA_V3.py
```

### 🤖 IA_agentQA_ms_modal.py - Microservicios (Doppler + OpenAI + Modal + Axiom + Vercel)

```bash
# 🧪 Ejecución local (prueba)
doppler run -- python src/IA_agentQA_ms_modal.py

# 🚀 Desplegar a Modal (producción)
modal deploy src/IA_agentQA_ms_modal.py

# 📝 Ejecutar función Modal localmente
doppler run -- modal run src/IA_agentQA_ms_modal.py::generate_ms_test_cases --requirement "Validar endpoint GET /api/v1/clientes/{id}"

# ⚡ Sin Doppler (usando .env)
python src/IA_agentQA_ms_modal.py
```

### 🧪 Tests

```bash
# OpenAI
doppler run -- python src/main.py

# Doppler
doppler run -- python src/test_doppler.py

# Modal
doppler run -- python src/test_modal_connection.py

# Axiom
doppler run -- python src/test_axiom_connection.py

# Integración
doppler run -- python src/test_hannah_axiom_integration.py
```

---

## 📖 Comandos Completos

Ver [SCRIPTS_BASH.md](SCRIPTS_BASH.md) para todos los comandos detallados.

---

## 🚀 Uso Rápido sin Doppler

```bash
# Instalar dependencias
pip install -r requirements.local.txt

# Crear .env
echo "OPENAI_API_KEY=tu_key" > .env

# Ejecutar app
streamlit run src/app.py
```

---

**Documentación completa:** [SCRIPTS_BASH.md](SCRIPTS_BASH.md)

