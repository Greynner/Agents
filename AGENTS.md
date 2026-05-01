# AGENTS.md

## Scope and source of truth
- This repo has two active deploy surfaces: `frontend/` (Next.js UI) and `api/modal_proxy.py` (Vercel Python proxy). The actual QA generation logic is in Modal entrypoints under `src/`.
- Prefer executable config over docs: `README.md` and `COMANDOS_RAPIDOS.md` contain stale commands that reference files that do not exist anymore.

## Real entrypoints
- QA general backend (Modal): `src/IA_agentQA_V3.py` (`modal.App("hannah-qa-agent-v3")`, endpoint function `analizar_requerimiento`).
- Microservices backend (Modal): `src/IA_agentQA_ms_modal.py` (`modal.App("hannah-ms-agent")`, endpoint function `analizar_requerimiento_ms`).
- Vercel proxy backend: `api/modal_proxy.py` (all routes forwarded via `vercel.json`).
- Frontend pages: `frontend/src/app/page.tsx` (general) and `frontend/src/app/ms/page.tsx` (microservices).

## Commands that are reliable
- Frontend dev (from `frontend/`): `npm install && npm run dev`
- Frontend quality check (from `frontend/`): `npm run lint && npm run build`
- Local smoke test for general Modal app: `doppler run -- python src/IA_agentQA_V3.py`
- Local smoke test for microservices Modal app: `doppler run -- python src/IA_agentQA_ms_modal.py`
- Deploy Modal apps: `modal deploy src/IA_agentQA_V3.py` and `modal deploy src/IA_agentQA_ms_modal.py`

## Known command traps
- Root `package.json` scripts are largely outdated (they point to files like `main.py`, `src/app.py`, `src/modal_app.py`, `src/test_doppler_src.py` that are not present). Do not assume root npm scripts are valid.
- Several helper shell scripts under `scripts/` also reference missing Streamlit files; verify target files before using them.

## Environment and integration quirks
- Doppler is the expected local env loader (`.doppler.yaml` uses project `qa-agent`, config `dev`). Most Python checks assume `doppler run -- ...`.
- `api/modal_proxy.py` requires `MODAL_BASE_URL` in Vercel env; without it, proxy returns 500. `MODAL_API_KEY` is optional and injected as `Authorization: Bearer ...` when set.
- Frontend general page uses `NEXT_PUBLIC_API_ENDPOINT` if set, otherwise falls back to same-origin `/api/analizar-requerimiento`.
- Frontend microservices page requires `NEXT_PUBLIC_MODAL_ENDPOINT_MS`; it errors immediately if missing.
- Backend request size guard is enforced in both Modal apps: max requirement length is 5000 chars.

## Dependencies and packaging gotcha
- Root `requirements.txt` is intentionally minimal for Vercel proxy only (`fastapi`, `httpx`).
- Full local Python stack lives in `requirements.local.txt`; use that for local dev/test of `src/` scripts.
