import os
from typing import Dict

import httpx
from fastapi import FastAPI, HTTPException, Request, Response


MODAL_BASE_URL = os.getenv("MODAL_BASE_URL", "").rstrip("/")
MODAL_API_KEY = os.getenv("MODAL_API_KEY")
PROXY_TIMEOUT = float(os.getenv("MODAL_PROXY_TIMEOUT", "60"))

app = FastAPI(
    title="QA Agent Proxy",
    description="Proxy ligero que reenvía peticiones a la instancia FastAPI desplegada en Modal.",
)

ALLOWED_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
HOP_HEADERS = {
    "content-encoding",
    "transfer-encoding",
    "content-length",
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "upgrade",
}


def _build_target_path(path: str) -> str:
    trimmed_base = MODAL_BASE_URL.rstrip("/")
    trimmed_path = path.lstrip("/")
    if not trimmed_base:
        raise HTTPException(status_code=500, detail="MODAL_BASE_URL no está configurada.")
    if not trimmed_path:
        return trimmed_base
    return f"{trimmed_base}/{trimmed_path}"


def _filtered_headers(headers: Dict[str, str]) -> Dict[str, str]:
    return {
        key: value
        for key, value in headers.items()
        if key.lower() not in HOP_HEADERS
    }


@app.api_route("/{full_path:path}", methods=ALLOWED_METHODS)
async def proxy(full_path: str, request: Request):
    target_url = _build_target_path(full_path)
    body = await request.body()

    upstream_headers = dict(request.headers)
    upstream_headers.pop("host", None)

    if MODAL_API_KEY:
        upstream_headers["authorization"] = f"Bearer {MODAL_API_KEY}"

    async with httpx.AsyncClient(timeout=PROXY_TIMEOUT) as client:
        resp = await client.request(
            request.method,
            target_url,
            params=request.query_params,
            content=body if body else None,
            headers=upstream_headers,
        )

    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers=_filtered_headers(resp.headers),
        media_type=resp.headers.get("content-type"),
    )


handler = app

