# Hannah QA Agent

AI-powered QA agent that generates:

- Test case matrices
- Gherkin scenarios
- A specialized variant for microservices / REST API testing

## Main structure

```txt
frontend/                  # Next.js UI
api/modal_proxy.py          # Vercel proxy to Modal
src/IA_agentQA_V3.py        # General QA Modal backend
src/IA_agentQA_ms_modal.py  # Microservices Modal backend
```

## Local development

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Checks:

```bash
cd frontend
npm run lint
npm run build
```

Backend smoke tests:

```bash
doppler run -- python src/IA_agentQA_V3.py
doppler run -- python src/IA_agentQA_ms_modal.py
```

## Backend deployment

```bash
modal deploy src/IA_agentQA_V3.py
modal deploy src/IA_agentQA_ms_modal.py
```

## Required variables

- `OPENAI_API_KEY`
- `MODAL_BASE_URL` for the Vercel proxy
- `MODAL_API_KEY` optional
- Optional Axiom variables for logging
