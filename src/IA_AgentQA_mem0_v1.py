import os
from typing import Any, List
from urllib.parse import urlparse

import psycopg2
from fastapi import FastAPI
from mem0 import MemoryClient
from openai import OpenAI

try:
    import chromadb
    from chromadb import HttpClient, PersistentClient
    from chromadb.config import Settings
except ImportError as exc:
    raise ImportError("chromadb debe estar instalado en el entorno") from exc

try:
    import modal
except ImportError:
    modal = None  # Modal solo es necesario en despliegues serverless

from pydantic import BaseModel

# =========================
# VARIABLES DESDE DOPPLER
# =========================
# Doppler inyecta todo automáticamente
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MEM0_API_KEY = os.getenv("MEM0_API_KEY")
DATABASE_URL = os.getenv("NEON_DATABASE_URL")
CHROMA_DIR = os.getenv("CHROMA_DIR", "./chroma_db")
CHROMA_REMOTE_URL = os.getenv("CHROMA_REMOTE_URL")
CHROMA_REMOTE_API_KEY = os.getenv("CHROMA_REMOTE_API_KEY")
MODAL_STUB_NAME = os.getenv("MODAL_STUB_NAME", "IA_AgentQA")

if not OPENAI_API_KEY or not MEM0_API_KEY or not DATABASE_URL:
    raise Exception("Faltan variables. Ejecuta con: doppler run -- python app.py")


# =========================
# CONFIGURACIÓN MODAL
# =========================
MODAL_PIP_PACKAGES = [
    "fastapi",
    "uvicorn[standard]",
    "chromadb",
    "mem0ai",
    "openai",
    "psycopg2-binary",
    "python-dotenv",
]

if modal:
    modal_image = (
        modal.Image.debian_slim()
        .apt_install("libpq-dev")
        .pip_install(*MODAL_PIP_PACKAGES)
    )
    stub = modal.App(MODAL_STUB_NAME, image=modal_image)
else:
    stub = None


# =========================
# SEED DATA PARA RAG
# =========================

RAG_SEED_DOCUMENTS: List[dict[str, Any]] = [
    {
        "id": "gherkin-login-positive",
        "type": "gherkin",
        "title": "Login exitoso",
        "document": """
Feature: Autenticación segura
  Como analista QA
  Quiero validar que el acceso al portal es seguro
  Para garantizar la experiencia del usuario

  Background:
    Given el usuario navega al portal corporativo

  Scenario: Credenciales válidas
    When el usuario ingresa usuario "qa_user" y contraseña "Passw0rd!"
    And presiona el botón "Ingresar"
    Then el sistema redirige al dashboard principal
    And se muestra el banner "Bienvenido qa_user"
""",
    },
    {
        "id": "gherkin-login-negative",
        "type": "gherkin",
        "title": "Login bloqueado",
        "document": """
Feature: Autenticación segura
  Scenario: Bloqueo por intentos fallidos consecutivos
    Given el usuario está en la pantalla de login
    When ingresa credenciales inválidas 3 veces
    Then el sistema bloquea el acceso por 30 minutos
    And se registra el evento en la bitácora de auditoría
""",
    },
    {
        "id": "matrix-onboarding",
        "type": "matrix",
        "title": "Matriz onboarding",
        "document": """
| ID | Módulo | Historia | Tipo de prueba | Resultado esperado |
| A1 | Registro | Como nuevo usuario quiero crear cuenta | Funcional | Cuenta creada y correo de verificación enviado |
| A2 | Registro | Validación de campos obligatorios | Validación | Mensajes descriptivos por cada campo vacío |
| A3 | Seguridad | Contraseñas con políticas corporativas | Seguridad | Rechaza claves débiles y acepta fuertes |
""",
    },
    {
        "id": "matrix-payments",
        "type": "matrix",
        "title": "Matriz pagos",
        "document": """
| ID | Flujo | Riesgo | Caso | Resultado esperado |
| P1 | Pago tarjeta | Alto | Autorización correcta | Recibo generado y conciliado |
| P2 | Pago tarjeta | Medio | Timeout gateway | Reversa automática y reporte |
| P3 | Pago transfer | Alto | Datos incompletos | Transacción rechazada con detalle |
""",
    },
]


# =========================
# Inicializar clientes
# =========================

# OpenAI SDK
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Mem0
mem = MemoryClient(api_key=MEM0_API_KEY)

def build_chroma_client():
    """
    Inicializa Chroma usando modo remoto (Chroma Cloud) si se define CHROMA_REMOTE_URL.
    Caso contrario utiliza almacenamiento local persistente.
    """
    settings = Settings(anonymized_telemetry=False)

    if CHROMA_REMOTE_URL:
        parsed = urlparse(CHROMA_REMOTE_URL)
        host = parsed.hostname or "localhost"
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
        ssl = parsed.scheme == "https"
        headers = {}
        if CHROMA_REMOTE_API_KEY:
            headers["Chroma-Api-Key"] = CHROMA_REMOTE_API_KEY

        return HttpClient(
            host=host,
            port=port,
            ssl=ssl,
            headers=headers or None,
            settings=settings,
        )

    return PersistentClient(
        path=CHROMA_DIR,
        settings=settings,
    )


chroma_client = build_chroma_client()
docs_collection = chroma_client.get_or_create_collection(name="qa_docs")


def seed_rag_examples(force: bool = False):
    """
    Pre-carga documentos de prueba para RAG con ejemplos de Gherkin y matrices.
    """
    if docs_collection.count() > 0 and not force:
        return

    ids = [doc["id"] for doc in RAG_SEED_DOCUMENTS]
    documents = [doc["document"] for doc in RAG_SEED_DOCUMENTS]
    metadatas = [{"type": doc["type"], "title": doc["title"]} for doc in RAG_SEED_DOCUMENTS]

    docs_collection.upsert(ids=ids, documents=documents, metadatas=metadatas)


seed_rag_examples()


# Neon PostgreSQL
conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True


if stub:

    @stub.function(schedule=modal.Period(hours=12))
    def sync_rag_seed():
        """
        Job programado en Modal para refrescar los documentos de RAG.
        """
        seed_rag_examples(force=True)


# =========================
# MODELOS Pydantic
# =========================

class RequerimientoQA(BaseModel):
    requerimiento: str
    usuario_id: str | None = None


class MatrizRespuesta(BaseModel):
    matriz: str
    casos_prueba: str
    debug_contexto: dict


# =========================
# FUNCIONES AUXILIARES
# =========================

def buscar_reglas_neon() -> List[str]:
    """
    Consulta reglas de QA almacenadas en Neon (PostgreSQL).
    """
    with conn.cursor() as cur:
        cur.execute("SELECT nombre_regla, descripcion FROM reglas_qa;")
        filas = cur.fetchall()

    return [f"{fila[0]}: {fila[1]}" for fila in filas]


def buscar_docs_rag(consulta: str, n_results: int = 3) -> List[str]:
    """
    Recupera documentos relevantes usando ChromaDB (RAG).
    """
    if docs_collection.count() == 0:
        return []

    result = docs_collection.query(
        query_texts=[consulta],
        n_results=n_results
    )

    return result.get("documents", [[]])[0]


def obtener_memoria(consulta: str, user_id: str | None = None) -> List[str]:
    """
    Recupera memorias previas relevantes desde Mem0.
    """
    query_args = {"query": consulta}
    if user_id:
        query_args["user_id"] = user_id

    items = mem.search(**query_args)
    return [i.get("text") or str(i) for i in items]


def guardar_evento_memoria(texto: str, user_id: str | None = None):
    """
    Guarda un nuevo recuerdo en Mem0.
    """
    payload = {"text": texto}
    if user_id:
        payload["user_id"] = user_id

    mem.add(**payload)


def generar_con_llm(requerimiento: str, contexto: str) -> str:
    """
    Llama al modelo GPT para generar matriz + casos.
    """
    completion = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres un agente QA experto. Generas matrices de prueba claras y casos de prueba "
                    "detallados siguiendo las mejores prácticas en QA."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Requerimiento:\n{requerimiento}\n\n"
                    f"Contexto adicional:\n{contexto}\n\n"
                    "Genera:\n"
                    "1) Matriz de pruebas\n"
                    "2) Lista de casos de prueba\n"
                )
            },
        ],
        temperature=0.2,
    )

    return completion.choices[0].message.content


# =========================
# FASTAPI APP
# =========================

app = FastAPI(
    title="QA Agent - Doppler + Mem0 + RAG + Neon",
    version="1.1.0",
    description="Servicio inteligente de QA usando Mem0, RAG, Neon, OpenAI y Modal.",
)


@app.get("/")
def index():
    return {"status": "running", "message": "QA Agent activo 🚀"}


@app.post("/qa/matriz", response_model=MatrizRespuesta)
def generar_matriz(payload: RequerimientoQA):

    req = payload.requerimiento
    user_id = payload.usuario_id

    # 1) Memoria desde Mem0
    memoria = obtener_memoria(req, user_id)

    # 2) Documentos desde RAG
    docs = buscar_docs_rag(req)

    # 3) Reglas desde Neon
    reglas = buscar_reglas_neon()

    contexto = f"""
    ==== MEMORIA (Mem0) ====
    {memoria}

    ==== DOCUMENTOS (RAG) ====
    {docs}

    ==== REGLAS NEON (SQL) ====
    {reglas}
    """

    # 4) LLM
    respuesta = generar_con_llm(req, contexto)

    # 5) Guardar memoria
    guardar_evento_memoria(f"Matriz generada para: {req}", user_id)

    return MatrizRespuesta(
        matriz=respuesta,
        casos_prueba=respuesta,
        debug_contexto={
            "memoria": memoria,
            "docs": docs,
            "reglas": reglas
        }
    )


# =========================
# INTEGRACIONES SERVERLESS
# =========================

# Modal: expone la app ASGI lista para modal serve/deploy
if stub:

    @stub.function()
    @modal.asgi_app()
    def modal_fastapi_app():
        return app


# Vercel: basta con apuntar al handler
vercel_handler = app
