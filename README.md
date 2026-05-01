# 🌸 Hannah – AI-powered QA Agent

Hannah es un agente de QA impulsado por IA que transforma un requerimiento (HDU / historia de usuario) en:
- 📑 Matriz de pruebas en Excel
- 🧪 Casos Gherkin (Cucumber) listos para automatización

✅ Diseñada para ahorrar tiempo a equipos QA y aumentar la cobertura de pruebas.

---

## 🚀 Demo Online

### 🌐 Frontend en Producción

- **QA General:** [https://qa-agent-two.vercel.app](https://qa-agent-two.vercel.app)
- **Microservicios:** [https://qa-agent-two.vercel.app/ms](https://qa-agent-two.vercel.app/ms)

### 🔗 Backend APIs

- **QA General:** `https://greynner--hannah-qa-agent-v3-analizar-requerimiento.modal.run`
- **Microservicios:** `https://greynner--hannah-ms-agent-analizar-requerimiento-ms.modal.run`

---

## 🛠️ Stack Tecnológico

### Frontend
- **Vercel** - Hosting y deployment del frontend
- **Next.js 16** - Framework React con App Router
- **TypeScript** - Tipado estático
- **Tailwind CSS** - Estilos y diseño responsive

### Backend
- **Modal** - Deployment serverless en la nube
- **FastAPI** - Framework para endpoints REST
- **Python 3.11** - Lenguaje principal

### IA y Procesamiento
- **OpenAI GPT-4o-mini** - Generación de casos de prueba con IA
- **Pandas** - Procesamiento de datos y matrices
- **OpenPyXL** - Generación de archivos Excel

### DevOps y Observabilidad
- **Doppler** - Gestión de secretos y variables de entorno
- **Axiom** - Logging centralizado y monitoreo
- **GitHub** - Control de versiones

### Integraciones
- **CORS** - Configurado para comunicación frontend-backend
- **Environment Variables** - Gestión centralizada con Doppler

---

## 📂 Estructura del Proyecto

```
Agents/
├── src/
│   ├── IA_agentQA_V3.py          # 🌸 Agente principal (QA general) - Modal + Vercel
│   ├── IA_agentQA_ms_modal.py    # 🤖 Agente microservicios - Modal + Vercel
│   ├── IA_agentQA_V1.py          # Versión 1 (Streamlit básico)
│   ├── IA_agentQA_V2.py          # Versión 2 (con Modal)
│   ├── IA_agentQA_ms.py          # Versión MS (Streamlit)
│   ├── hannah_modal_app.py       # App Modal original
│   ├── hannah_modal_client.py    # Cliente Modal
│   ├── utils_axiom.py            # Utilidades para logging Axiom
│   └── test_*.py                  # Scripts de prueba
│
├── frontend/
│   ├── src/
│   │   └── app/
│   │       ├── page.tsx          # Página principal (QA general)
│   │       ├── ms/
│   │       │   └── page.tsx      # Página microservicios
│   │       ├── layout.tsx        # Layout principal
│   │       └── globals.css       # Estilos globales
│   ├── package.json              # Dependencias Node.js
│   ├── next.config.ts            # Configuración Next.js
│   └── vercel.json               # Configuración Vercel
│
├── Notebooks/
│   ├── hannah_agent.ipynb        # Notebooks de desarrollo
│   ├── QA v2.ipynb
│   └── qa_agent.ipynb
│
├── scripts/                      # Scripts de ejecución
│   ├── run_app_*.sh
│   └── test_*.sh
│
├── Outputs/                      # Archivos generados
│   ├── matriz_pruebas.xlsx
│   └── casos.feature
│
├── requirements.txt              # Dependencias mínimas (proxy Vercel)
├── requirements.local.txt        # Stack completo para desarrollo
├── COMANDOS_RAPIDOS.md          # Guía de comandos
└── README.md                     # Este archivo
```

---

## ⚙️ Configuración y Uso

### Prerrequisitos

1. **Cuentas necesarias:**
   - [Doppler](https://doppler.com) - Para gestión de secretos
   - [Modal](https://modal.com) - Para deployment backend
   - [Vercel](https://vercel.com) - Para deployment frontend
   - [OpenAI](https://openai.com) - API key para IA
   - [Axiom](https://axiom.co) - (Opcional) Para logging avanzado

2. **CLIs instalados:**
   ```bash
   # Doppler CLI
   brew install dopplerhq/cli/doppler
   
   # Modal CLI
   pip install modal
   
   # Vercel CLI
   npm i -g vercel
   ```

### Configuración Inicial

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Greynner/IA-Agent-QA.git
   cd IA-Agent-QA  # o cd Agents si lo renombraste localmente
   ```

2. **Configurar Doppler:**
   ```bash
   doppler login
   doppler setup
   ```

3. **Configurar Modal:**
   ```bash
   modal token new
   ```

4. **Configurar secretos en Modal:**
   ```bash
   modal secret create qa-agent-secrets \
     OPENAI_API_KEY=tu_key \
     AXIOM_API_TOKEN=tu_token \
     AXIOM_ORG_ID=tu_org_id \
     AXIOM_DATASET=hannah-qa-agent \
     ENVIRONMENT=production
   ```

---

## 🚀 Deployment

### Backend (Modal)

```bash
# Desplegar agente general
modal deploy src/IA_agentQA_V3.py

# Desplegar agente microservicios
modal deploy src/IA_agentQA_ms_modal.py
```

### Frontend (Vercel)

```bash
cd frontend

# Configurar variables de entorno
vercel env add NEXT_PUBLIC_MODAL_ENDPOINT production
vercel env add NEXT_PUBLIC_MODAL_ENDPOINT_MS production

# Desplegar
vercel --prod
```

---

## 💻 Uso Local

### Ejecutar Backend Localmente

```bash
# Agente general
doppler run -- python src/IA_agentQA_V3.py

# Agente microservicios
doppler run -- python src/IA_agentQA_ms_modal.py
```

### Desarrollo Frontend Local

```bash
cd frontend
npm install
npm run dev
# Abre http://localhost:3000
```

---

## 📋 Ejemplos de Uso

### QA General

**Requerimiento:**
```
El usuario debe poder iniciar sesión con correo y contraseña. 
Si las credenciales son correctas, redirige al panel principal. 
Si son incorrectas, muestra el mensaje "Correo o contraseña incorrectos."
```

**Salida:**
- Matriz de pruebas con escenarios (exitoso, fallido, campos vacíos, etc.)
- Casos Gherkin para automatización

### Microservicios

**Requerimiento:**
```
Validar que el endpoint GET /api/v1/clientes/{id} retorne 200 con datos válidos 
y 404 si el cliente no existe.
```

**Salida:**
- Matriz con columnas: ID, Endpoint, Método, Descripción, Datos de entrada, Código esperado, Resultado esperado
- Casos Gherkin específicos para APIs REST
- Cobertura de códigos HTTP (200, 400, 404, 500)

---

## 🔧 Comandos Rápidos

Ver [COMANDOS_RAPIDOS.md](COMANDOS_RAPIDOS.md) para la lista completa de comandos.

> Nota: el repositorio remoto se mantiene como `IA-Agent-QA`, pero localmente esta carpeta puede estar renombrada como `Agents`.

### Principales

```bash
# Desplegar backend
modal deploy src/IA_agentQA_V3.py

# Desplegar frontend
cd frontend && vercel --prod

# Ejecutar localmente
doppler run -- python src/IA_agentQA_V3.py
```

---

## 📊 Arquitectura

```
┌─────────────────┐
│   Vercel        │  Frontend (Next.js)
│   Frontend       │  └─> Página General (/)
└────────┬────────┘  └─> Página MS (/ms)
         │
         │ HTTP POST
         │
┌────────▼────────┐
│   Modal         │  Backend Serverless
│   Backend       │  ├─> IA_agentQA_V3.py (QA General)
│                 │  └─> IA_agentQA_ms_modal.py (MS)
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼────┐
│OpenAI │ │ Axiom │
│  API  │ │ Logs  │
└───────┘ └───────┘
```

---

## 🔐 Variables de Entorno

### Backend (Modal Secrets)

- `OPENAI_API_KEY` - API key de OpenAI
- `AXIOM_API_TOKEN` - Token de Axiom (opcional)
- `AXIOM_ORG_ID` - ID de organización Axiom
- `AXIOM_DATASET` - Dataset de Axiom
- `ENVIRONMENT` - Entorno (production/development)

### Frontend (Vercel Environment Variables)

- `NEXT_PUBLIC_MODAL_ENDPOINT` - URL endpoint QA general
- `NEXT_PUBLIC_MODAL_ENDPOINT_MS` - URL endpoint microservicios

---

## 📈 Roadmap

- ✅ Integración con Modal para deployment serverless
- ✅ Frontend en Vercel con Next.js
- ✅ Agente especializado en microservicios
- ✅ Logging centralizado con Axiom
- ✅ Gestión de secretos con Doppler
- 🔜 Integración con Jira / Confluence
- 🔜 Dashboard con métricas de cobertura QA
- 🔜 Extensión a pruebas automáticas E2E
- 🔜 Exportación a múltiples formatos (JSON, CSV, etc.)

---

## 🧪 Testing

```bash
# Probar conexión OpenAI
doppler run -- python src/test_openai.sh

# Probar conexión Modal
doppler run -- python src/test_modal_connection.py

# Probar conexión Axiom
doppler run -- python src/test_axiom_connection.py

# Probar integración completa
doppler run -- python src/test_hannah_axiom_integration.py
```

---

## 📝 Versiones

- **V1** (`IA_agentQA_V1.py`) - Versión básica con Streamlit
- **V2** (`IA_agentQA_V2.py`) - Versión con Modal
- **V3** (`IA_agentQA_V3.py`) - ⭐ Versión unificada (Modal + Vercel + Axiom)
- **MS** (`IA_agentQA_ms_modal.py`) - ⭐ Versión especializada en microservicios

---

## 👨‍💻 Autor

**Greynner Moreno**  
QA Engineer & AI Entrepreneur 🇨🇱 | Construyendo el futuro del QA con IA

---

## 📄 Licencia

Este proyecto es de código abierto. Ver archivo LICENSE para más detalles.

---

## 🙏 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

**Última actualización:** Octubre 2025
