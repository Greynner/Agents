# Hannah QA Agent

Agente de QA con IA que genera:

- Matriz de casos de prueba
- Escenarios Gherkin
- Variante especializada para pruebas de microservicios/API REST

## Estructura principal

```txt
frontend/                  # UI Next.js
api/modal_proxy.py          # Proxy Vercel hacia Modal
src/IA_agentQA_V3.py        # Backend Modal QA general
src/IA_agentQA_ms_modal.py  # Backend Modal microservicios
```

## Desarrollo local

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Checks:

```bash
npm run check
```

Smoke tests backend:

```bash
doppler run -- python src/IA_agentQA_V3.py
doppler run -- python src/IA_agentQA_ms_modal.py
```

## Deploy backend

```bash
modal deploy src/IA_agentQA_V3.py
modal deploy src/IA_agentQA_ms_modal.py
```

## Variables requeridas

- `OPENAI_API_KEY`
- `MODAL_BASE_URL` para el proxy Vercel
- `MODAL_API_KEY` opcional
- Variables Axiom opcionales para logging
