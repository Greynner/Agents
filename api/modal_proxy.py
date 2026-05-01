import json
import os
from typing import Dict

import httpx
from fastapi import FastAPI, Request, Response


MODAL_BASE_URL = os.getenv("MODAL_BASE_URL", "").rstrip("/")
MODAL_API_KEY = os.getenv("MODAL_API_KEY")
PROXY_TIMEOUT = float(os.getenv("MODAL_PROXY_TIMEOUT", "60"))
ALLOWED_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": ",".join(ALLOWED_METHODS),
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
}
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

app = FastAPI(
    title="QA Agent Proxy",
    description="Proxy ligero que reenvía peticiones a la instancia FastAPI desplegada en Modal.",
)


def _filtered_headers(headers: Dict[str, str]) -> Dict[str, str]:
    return {
        key: value
        for key, value in headers.items()
        if key.lower() not in HOP_HEADERS
    }


@app.api_route("/{full_path:path}", methods=ALLOWED_METHODS)
async def proxy(full_path: str, request: Request):
    try:
        if request.method == "OPTIONS":
            return Response(status_code=204, headers=CORS_HEADERS)

        if not MODAL_BASE_URL:
            error_msg = "MODAL_BASE_URL no está configurada en las variables de entorno de Vercel"
            print(f"❌ Error: {error_msg}")
            return Response(
                status_code=500,
                content=json.dumps({"error": error_msg, "detail": "Configura MODAL_BASE_URL en Vercel"}),
                media_type="application/json",
                headers=CORS_HEADERS,
            )

        target_url = f"{MODAL_BASE_URL}/{full_path.lstrip('/')}" if full_path else MODAL_BASE_URL
        body = await request.body()

        upstream_headers = dict(request.headers)
        upstream_headers.pop("host", None)
        upstream_headers.pop("content-length", None)

        if MODAL_API_KEY:
            upstream_headers["authorization"] = f"Bearer {MODAL_API_KEY}"

        print(f"🔄 Proxying {request.method} {full_path} -> {target_url}")

        async with httpx.AsyncClient(timeout=PROXY_TIMEOUT) as client:
            resp = await client.request(
                request.method,
                target_url,
                params=request.query_params,
                content=body if body else None,
                headers=upstream_headers,
            )

        response_headers = _filtered_headers(resp.headers)
        response_headers.update(CORS_HEADERS)

        return Response(
            content=resp.content,
            status_code=resp.status_code,
            headers=response_headers,
            media_type=resp.headers.get("content-type"),
        )

    except httpx.TimeoutException:
        error_msg = f"Timeout al conectar con Modal (>{PROXY_TIMEOUT}s)"
        print(f"❌ {error_msg}")
        return Response(
            status_code=504,
            content=json.dumps({"error": error_msg}),
            media_type="application/json",
            headers=CORS_HEADERS,
        )
    except Exception as e:
        error_msg = f"Error inesperado en proxy: {str(e)}"
        print(f"❌ {error_msg}")
        return Response(
            status_code=500,
            content=json.dumps({"error": error_msg, "detail": "Revisa los logs del servidor"}),
            media_type="application/json",
            headers=CORS_HEADERS,
        )


handler = app
