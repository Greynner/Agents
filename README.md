# Hannah QA Agent

AI-powered QA agent that turns requirements or user stories into:

- Test case matrices
- Gherkin scenarios ready for automation
- A specialized variant for microservices / REST API testing

## Live demo

- **General QA:** [https://qa-agent-two.vercel.app](https://qa-agent-two.vercel.app)
- **Microservices:** [https://qa-agent-two.vercel.app/ms](https://qa-agent-two.vercel.app/ms)

## Main structure

```txt
frontend/                  # Next.js UI
api/modal_proxy.py          # Vercel proxy to Modal
src/IA_agentQA_V3.py        # General QA Modal backend
src/IA_agentQA_ms_modal.py  # Microservices Modal backend
requirements.txt            # Minimal dependencies for the Vercel proxy
requirements.local.txt      # Full local development stack
```

> Note: the remote repository may still be named `IA-Agent-QA`, while the local folder can be named `Agents`.

## Local development

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Frontend checks:

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

## Usage examples

### General QA

Requirement:

```txt
The user must be able to sign in with email and password.
If the credentials are correct, the user is redirected to the main dashboard.
If they are incorrect, show the message "Incorrect email or password."
```

Output:

- Test matrix with positive, negative, and edge-case scenarios
- Gherkin cases for automation

### Microservices

Requirement:

```txt
Validate that GET /api/v1/customers/{id} returns 200 with valid data
and 404 when the customer does not exist.
```

Output:

- API-focused test matrix
- REST-specific Gherkin cases
- HTTP status coverage such as 200, 400, 404, and 500
