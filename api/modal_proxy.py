import os
import json
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
    try:
        # Manejar CORS preflight
        if request.method == "OPTIONS":
            return Response(
                status_code=204,
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": ",".join(ALLOWED_METHODS),
                    "Access-Control-Allow-Headers": "Content-Type, Authorization",
                },
            )

        if not MODAL_BASE_URL:
            error_msg = "MODAL_BASE_URL no está configurada en las variables de entorno de Vercel"
            print(f"❌ Error: {error_msg}")
            return Response(
                status_code=500,
                content=json.dumps({"error": error_msg, "detail": "Configura MODAL_BASE_URL en Vercel"}),
                media_type="application/json",
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type",
                },
            )

        target_url = _build_target_path(full_path)
        body = await request.body()

        upstream_headers = dict(request.headers)
        upstream_headers.pop("host", None)
        upstream_headers.pop("content-length", None)  # Modal calculará esto

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
        response_headers["Access-Control-Allow-Origin"] = "*"
        response_headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"

        return Response(
            content=resp.content,
            status_code=resp.status_code,
            headers=response_headers,
            media_type=resp.headers.get("content-type"),
        )

    except HTTPException as e:
        print(f"❌ HTTPException: {e.detail}")
        return Response(
            status_code=e.status_code,
            content=json.dumps({"error": str(e.detail)}),
            media_type="application/json",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
            },
        )
    except httpx.TimeoutException:
        error_msg = f"Timeout al conectar con Modal (>{PROXY_TIMEOUT}s)"
        print(f"❌ {error_msg}")
        return Response(
            status_code=504,
            content=json.dumps({"error": error_msg}),
            media_type="application/json",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
            },
        )
    except Exception as e:
        error_msg = f"Error inesperado en proxy: {str(e)}"
        print(f"❌ {error_msg}")
        import traceback
        traceback.print_exc()
        return Response(
            status_code=500,
            content=json.dumps({"error": error_msg, "detail": "Revisa los logs del servidor"}),
            media_type="application/json",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
            },
        )


handler = app

