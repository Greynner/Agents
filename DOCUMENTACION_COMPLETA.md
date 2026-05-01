# 📚 Documentación Completa del Proyecto Agents

## Tabla de Contenidos

1. [Estructura de Carpetas](#estructura-de-carpetas)
2. [Archivos Principales - Backend](#archivos-principales---backend)
3. [Archivos Principales - Frontend](#archivos-principales---frontend)
4. [Archivos de Configuración](#archivos-de-configuración)
5. [Explicación Línea por Línea](#explicación-línea-por-línea)

---

## 📂 Estructura de Carpetas

### `/` (Raíz del Proyecto)

**Propósito:** Contiene la configuración principal y archivos de documentación del proyecto.

**Archivos importantes:**
- `README.md` - Documentación principal del proyecto
- `requirements.txt` - Dependencias mínimas (proxy Vercel)
- `requirements.local.txt` - Dependencias completas para desarrollo Python
- `package.json` - Configuración Node.js (si aplica)
- `COMANDOS_RAPIDOS.md` - Guía rápida de comandos
- `.gitignore` - Archivos ignorados por Git

---

### `/src/` - Código Fuente Backend

**Propósito:** Contiene todo el código Python del backend, incluyendo los agentes principales y utilidades.

#### Archivos Principales:

**`IA_agentQA_V3.py`** ⭐
- **Propósito:** Agente principal unificado para QA general
- **Funcionalidad:** Genera matrices de prueba y casos Gherkin para requerimientos funcionales
- **Integraciones:** Doppler, OpenAI, Modal, Axiom, Vercel
- **Líneas:** 322

**`IA_agentQA_ms_modal.py`** ⭐
- **Propósito:** Agente especializado en microservicios (APIs REST)
- **Funcionalidad:** Genera casos de prueba específicos para endpoints REST
- **Integraciones:** Mismas que V3, pero con prompts especializados para APIs
- **Líneas:** 328

**`IA_agentQA_V1.py`**
- **Propósito:** Versión 1 (Streamlit básico)
- **Estado:** Versión anterior, mantenida para referencia

**`IA_agentQA_V2.py`**
- **Propósito:** Versión 2 (con Modal)
- **Estado:** Versión anterior, mantenida para referencia

**`IA_agentQA_ms.py`**
- **Propósito:** Versión MS con Streamlit
- **Estado:** Versión anterior, mantenida para referencia

**`utils_axiom.py`**
- **Propósito:** Utilidades para logging a Axiom
- **Funcionalidad:** Clase `AxiomLogger` reutilizable

**`hannah_modal_app.py`**
- **Propósito:** App Modal original (versión anterior)
- **Estado:** Mantenida para referencia

**`hannah_modal_client.py`**
- **Propósito:** Cliente para conectar con Modal localmente
- **Funcionalidad:** Wrapper para llamadas a funciones de Modal

**`test_*.py`**
- **Propósito:** Scripts de prueba para validar integraciones
- **Archivos:**
  - `test_doppler.py` - Prueba conexión con Doppler
  - `test_modal_connection.py` - Prueba conexión con Modal
  - `test_axiom_connection.py` - Prueba conexión con Axiom
  - `test_hannah_axiom_integration.py` - Prueba integración completa

**`main.py`**
- **Propósito:** Punto de entrada principal (versión anterior)

**`__init__.py`**
- **Propósito:** Hace que `src/` sea un paquete Python

---

### `/frontend/` - Aplicación Frontend

**Propósito:** Aplicación Next.js que sirve como interfaz de usuario.

#### Estructura:

**`/frontend/src/app/`**
- **Propósito:** Directorio principal de la aplicación Next.js (App Router)

**`/frontend/src/app/page.tsx`**
- **Propósito:** Página principal (QA General)
- **Ruta:** `/`
- **Funcionalidad:** Interfaz para generar casos de prueba generales

**`/frontend/src/app/ms/page.tsx`**
- **Propósito:** Página de microservicios
- **Ruta:** `/ms`
- **Funcionalidad:** Interfaz para generar casos de prueba de APIs REST

**`/frontend/src/app/layout.tsx`**
- **Propósito:** Layout raíz de la aplicación
- **Funcionalidad:** Define el HTML base y metadatos

**`/frontend/src/app/globals.css`**
- **Propósito:** Estilos CSS globales
- **Framework:** Tailwind CSS

**`/frontend/src/app/favicon.ico`**
- **Propósito:** Icono de la aplicación

**`/frontend/package.json`**
- **Propósito:** Dependencias y scripts de Node.js
- **Contiene:** React, Next.js, TypeScript, Tailwind CSS

**`/frontend/next.config.ts`**
- **Propósito:** Configuración de Next.js
- **Funcionalidad:** Configuración del framework

**`/frontend/vercel.json`**
- **Propósito:** Configuración de deployment en Vercel
- **Funcionalidad:** Define build commands y framework

**`/frontend/tsconfig.json`**
- **Propósito:** Configuración de TypeScript
- **Funcionalidad:** Opciones del compilador TypeScript

**`/frontend/.vercel/`**
- **Propósito:** Configuración local de Vercel
- **Contiene:** Información del proyecto vinculado

---

### `/Notebooks/` - Jupyter Notebooks

**Propósito:** Notebooks de desarrollo y experimentación.

**Archivos:**
- `hannah_agent.ipynb` - Notebook principal de desarrollo
- `QA v2.ipynb` - Versión 2 del notebook
- `qa_agent.ipynb` - Notebook de pruebas

**Uso:** Para experimentar con prompts y probar funcionalidades antes de integrarlas al código principal.

---

### `/scripts/` - Scripts de Ejecución

**Propósito:** Scripts bash para facilitar la ejecución de diferentes versiones.

**Archivos:**
- `run_app_*.sh` - Scripts para ejecutar diferentes apps
- `test_*.sh` - Scripts para ejecutar tests

---

### `/Outputs/` - Archivos Generados

**Propósito:** Directorio donde se guardan los archivos generados por la aplicación.

**Archivos típicos:**
- `matriz_pruebas.xlsx` - Matriz de pruebas en Excel
- `casos.feature` - Casos Gherkin generados

---

### `/tests/` - Tests

**Propósito:** Directorio para tests automatizados (actualmente vacío o en desarrollo).

---

## 📄 Archivos Principales - Backend

### `src/IA_agentQA_V3.py` - Explicación Detallada

Este es el archivo principal del agente de QA general. A continuación, la explicación línea por línea:

#### **Líneas 1-12: Imports**

```python
import os                    # Acceso a variables de entorno del sistema
import pandas as pd         # Manipulación de datos y creación de DataFrames
import modal                # Framework para deployment serverless en Modal
from dotenv import load_dotenv  # Carga variables de entorno desde .env
from openai import OpenAI, OpenAIError  # Cliente de OpenAI y manejo de errores
from fastapi import Request  # Request de FastAPI para endpoints HTTP
from fastapi.responses import JSONResponse  # Respuesta JSON para FastAPI
import requests             # Para hacer peticiones HTTP (Axiom)
import json                 # Manipulación de JSON
import traceback            # Para obtener stack traces de errores
from datetime import datetime, timezone  # Para timestamps en logs
from typing import Dict, Any, Optional  # Type hints para mejor documentación
```

**Propósito:** Importar todas las librerías necesarias para el funcionamiento del agente.

---

#### **Líneas 14-28: Configuración de Variables de Entorno**

```python
# =====================
# CONFIGURACIÓN DOPPLER + VARIABLES DE ENTORNO
# =====================
# Doppler inyecta variables de entorno, dotenv como fallback
load_dotenv()  # Carga variables desde archivo .env (si existe)

# Variables de entorno (desde Doppler o .env)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # API key de OpenAI
AXIOM_API_TOKEN = os.getenv("AXIOM_API_TOKEN")  # Token de Axiom para logging
AXIOM_ORG_ID = os.getenv("AXIOM_ORG_ID")  # ID de organización en Axiom
AXIOM_DATASET = os.getenv("AXIOM_DATASET", "hannah-qa-agent")  # Dataset de Axiom (default)
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")  # Entorno actual (default: production)

if not OPENAI_API_KEY:
    print("⚠️ Advertencia: OPENAI_API_KEY no está configurada. Usa Doppler o un archivo .env")
```

**Propósito:** 
- Cargar variables de entorno desde Doppler (cuando se ejecuta con `doppler run`) o desde archivo `.env`
- Definir variables globales con valores por defecto
- Validar que la API key de OpenAI esté configurada

**Flujo:**
1. `load_dotenv()` busca archivo `.env` en el directorio actual
2. `os.getenv()` obtiene variables del entorno (inyectadas por Doppler o desde `.env`)
3. Si no encuentra la variable, usa el valor por defecto (si se especifica)

---

#### **Líneas 30-100: Clase AxiomLogger**

```python
# =====================
# LOGGER AXIOM
# =====================
class AxiomLogger:
    """Clase para enviar logs a Axiom"""
    
    def __init__(self):
        # Inicializa las credenciales de Axiom desde variables de entorno
        self.api_token = AXIOM_API_TOKEN
        self.org_id = AXIOM_ORG_ID
        self.dataset = AXIOM_DATASET
        self.environment = ENVIRONMENT
        # Construye la URL del endpoint de Axiom para ingesta de logs
        self.ingest_url = f"https://api.axiom.co/v1/datasets/{self.dataset}/ingest"
        # Headers para autenticación en Axiom (solo si hay credenciales)
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_token}',
            'X-Axiom-Org-Id': self.org_id
        } if self.api_token and self.org_id else None
```

**Propósito:** Inicializar el logger con las credenciales de Axiom.

**Líneas 48-78: Método `log()`**

```python
def log(self, level: str, message: str, metadata: Optional[Dict] = None) -> bool:
    """Envía un log a Axiom"""
    # Si no hay credenciales, solo imprime en consola (fallback)
    if not self.api_token or not self.org_id or not self.headers:
        print(f"[{level}] {message}")
        return False
    
    try:
        # Construye el objeto de log con toda la información
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),  # Timestamp UTC
            "level": level.upper(),  # Nivel del log (INFO, ERROR, WARN)
            "message": message,  # Mensaje principal
            "source": "hannah_qa_agent_v3",  # Identificador del origen
            "environment": self.environment,  # Entorno (production/development)
            "metadata": metadata or {}  # Metadatos adicionales (opcional)
        }
        
        # Envía el log a Axiom mediante POST request
        response = requests.post(
            self.ingest_url,  # URL del endpoint de Axiom
            headers=self.headers,  # Headers de autenticación
            json=[log_data],  # Axiom espera un array de logs
            timeout=5  # Timeout de 5 segundos
        )
        
        # Verifica si el envío fue exitoso
        if response.status_code == 200:
            return True
        else:
            print(f"⚠️ Error enviando log a Axiom: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en logging: {str(e)}")
        return False
```

**Propósito:** 
- Enviar logs estructurados a Axiom
- Si no hay credenciales, hacer fallback a `print()` (no falla)
- Manejar errores de red o de Axiom

**Líneas 80-97: Métodos Helper**

```python
def log_info(self, message: str, metadata: Optional[Dict] = None) -> bool:
    """Log de información"""
    return self.log("INFO", message, metadata)

def log_error(self, message: str, error: Exception = None, context: Optional[Dict] = None) -> bool:
    """Log de error con detalles"""
    metadata = context or {}
    if error:
        # Agrega información detallada del error
        metadata.update({
            "error_type": type(error).__name__,  # Tipo de excepción
            "error_message": str(error),  # Mensaje del error
            "traceback": traceback.format_exc()  # Stack trace completo
        })
    return self.log("ERROR", message, metadata)

def log_warning(self, message: str, metadata: Optional[Dict] = None) -> bool:
    """Log de advertencia"""
    return self.log("WARN", message, metadata)
```

**Propósito:** Métodos convenientes para diferentes niveles de log.

**Línea 100: Instancia Global**

```python
axiom_logger = AxiomLogger()
```

**Propósito:** Crear una instancia global del logger para usar en todo el módulo.

---

#### **Líneas 102-116: Configuración de Modal**

```python
# =====================
# CONFIGURACIÓN MODAL
# =====================
# Imagen base con todas las dependencias
image = modal.Image.debian_slim().pip_install(
    "openai>=1.0.0",    # Cliente de OpenAI
    "pandas>=2.0.0",    # Manipulación de datos
    "openpyxl",         # Para generar archivos Excel
    "fastapi",          # Framework web para endpoints
    "requests",        # Para peticiones HTTP (Axiom)
    "python-dotenv",   # Para cargar .env
)

# Crea la app de Modal
app = modal.App("hannah-qa-agent-v3", image=image)
```

**Propósito:**
- Definir la imagen Docker que Modal usará para ejecutar el código
- `debian_slim()`: Imagen base ligera de Debian
- `pip_install()`: Instala las dependencias en la imagen
- `modal.App()`: Crea la aplicación Modal con un nombre único

**Cómo funciona:**
- Modal construye una imagen Docker con estas dependencias
- Cada función que uses `@app.function()` se ejecuta en un contenedor con esta imagen

---

#### **Líneas 118-224: Función Principal de Generación**

```python
@app.function(secrets=[modal.Secret.from_name("qa-agent-secrets")])
def generate_test_matrix_and_gherkin(requirement: str):
```

**Decorador `@app.function()`:**
- Convierte la función en una función ejecutable en Modal
- `secrets=[]`: Especifica qué secretos de Modal usar (variables de entorno inyectadas)

**Parámetros:**
- `requirement: str`: El requerimiento de QA que se quiere procesar

**Líneas 127-131: Inicialización**

```python
try:
    # Inicializar cliente OpenAI (usa secretos de Modal/Doppler)
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    axiom_logger.log_info(f"Generando casos para requerimiento: {requirement[:100]}...")
```

**Propósito:**
- Crear cliente de OpenAI con la API key desde variables de entorno
- Loggear el inicio del proceso (solo primeros 100 caracteres del requerimiento)

**Líneas 133-150: Prompts para OpenAI**

```python
# Prompt mejorado de Hannah
SYSTEM_PROMPT = """
Eres Hannah 🌸, una QA Engineer Senior especializada en automatización de pruebas.
Tu tarea es analizar un requerimiento y generar una matriz de pruebas y casos Gherkin claros y consistentes.
"""

FEW_SHOT_EXAMPLE = """
| ID | Escenario | Datos de entrada | Resultado esperado |
|----|-----------|------------------|-------------------|
| TC001 | Login exitoso | Usuario válido | Acceso concedido |
| TC002 | Login fallido | Usuario inválido | Mensaje de error "Credenciales inválidas" |

Feature: Validación de login
  Scenario: Login exitoso
    Given usuario válido
    When ingresa credenciales correctas
    Then muestra "Acceso concedido"
"""
```

**Propósito:**
- `SYSTEM_PROMPT`: Define el rol y comportamiento de la IA
- `FEW_SHOT_EXAMPLE`: Ejemplo que guía el formato de salida esperado
- Técnica "few-shot learning": Mostrar ejemplos para que la IA aprenda el formato

**Líneas 152-160: Llamada a OpenAI**

```python
# Llamada a OpenAI
response = client.chat.completions.create(
    model="gpt-4o-mini",  # Modelo de OpenAI (ligero y económico)
    temperature=0.3,      # Baja temperatura = respuestas más deterministas
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"{FEW_SHOT_EXAMPLE}\n\nRequerimiento:\n{requirement}"}
    ]
)

output = response.choices[0].message.content
```

**Propósito:**
- Enviar el prompt a OpenAI
- `temperature=0.3`: Baja creatividad, alta consistencia (ideal para QA)
- Obtener la respuesta generada

**Líneas 164-175: Procesamiento de Matriz**

```python
# Procesar matriz de prueba
rows = []
for line in output.splitlines():  # Itera cada línea de la respuesta
    if "|" in line and "---" not in line:  # Busca líneas de tabla Markdown
        cols = [c.strip() for c in line.split("|") if c.strip()]  # Separa columnas
        if len(cols) > 1:  # Solo si tiene más de una columna
            rows.append(cols)

# Crear DataFrame
df = None
if rows:
    df = pd.DataFrame(rows[1:], columns=rows[0])  # Primera fila = headers, resto = datos
```

**Propósito:**
- Parsear la tabla Markdown generada por OpenAI
- Convertirla en un DataFrame de Pandas para fácil manipulación
- `rows[1:]`: Todas las filas excepto la primera (que son los headers)
- `rows[0]`: La primera fila como nombres de columnas

**Líneas 177-186: Extracción de Gherkin**

```python
# Extraer casos Gherkin
gherkin_lines = []
capture = False
for line in output.splitlines():
    if line.strip().startswith(("Feature", "Scenario")):  # Inicio de casos Gherkin
        capture = True
    if capture:
        gherkin_lines.append(line)

gherkin_content = "\n".join(gherkin_lines) if gherkin_lines else ""
```

**Propósito:**
- Extraer solo la parte de Gherkin de la respuesta
- Buscar líneas que empiecen con "Feature" o "Scenario"
- Una vez encontrado, capturar todo lo que sigue

**Líneas 188-201: Construcción de Resultado**

```python
result = {
    "status": "success",
    "output": output,  # Respuesta completa de OpenAI
    "matrix_data": df.to_dict('records') if df is not None else [],  # Matriz como array de objetos
    "gherkin_content": gherkin_content,  # Casos Gherkin extraídos
    "matrix_columns": df.columns.tolist() if df is not None else []  # Nombres de columnas
}

axiom_logger.log_info(
    f"Casos generados exitosamente: {len(result['matrix_data'])} filas",
    {"matrix_rows": len(result['matrix_data']), "has_gherkin": bool(gherkin_content)}
)

return result
```

**Propósito:**
- Construir el objeto de respuesta estructurado
- `df.to_dict('records')`: Convierte DataFrame a array de diccionarios (formato JSON)
- Loggear el éxito con métricas
- Retornar el resultado

**Líneas 203-224: Manejo de Errores**

```python
except OpenAIError as e:
    # Error específico de OpenAI (API key inválida, rate limit, etc.)
    error_msg = f"Error al conectar con OpenAI: {e}"
    axiom_logger.log_error("Error en OpenAI", e, {"requirement": requirement[:100]})
    return {
        "status": "error",
        "error": error_msg,
        # ... campos vacíos
    }
except Exception as e:
    # Cualquier otro error inesperado
    error_msg = f"Error inesperado: {e}"
    axiom_logger.log_error("Error inesperado", e, {"requirement": requirement[:100]})
    return {
        "status": "error",
        # ... campos vacíos
    }
```

**Propósito:**
- Capturar errores específicos de OpenAI
- Capturar cualquier otro error
- Loggear errores a Axiom con contexto
- Retornar respuesta de error estructurada

---

#### **Líneas 226-283: Endpoint HTTP para Frontend**

```python
@app.function()
@modal.fastapi_endpoint(method="POST")
async def analizar_requerimiento(request: Request):
```

**Decoradores:**
- `@app.function()`: Hace la función ejecutable en Modal
- `@modal.fastapi_endpoint(method="POST")`: Expone la función como endpoint HTTP POST
- `async`: Función asíncrona (requerido para FastAPI)

**Líneas 236-247: Headers CORS**

```python
cors_headers = {
    "Access-Control-Allow-Origin": "*",  # Permite requests desde cualquier origen
    "Access-Control-Allow-Headers": "Content-Type",  # Headers permitidos
    "Access-Control-Allow-Methods": "POST, OPTIONS",  # Métodos HTTP permitidos
}

# Manejar preflight CORS
if request.method == "OPTIONS":
    response = JSONResponse(status_code=204, content=None)
    for key, value in cors_headers.items():
        response.headers[key] = value
    return response
```

**Propósito:**
- Configurar CORS para permitir requests desde el frontend de Vercel
- Manejar preflight requests (OPTIONS) que los navegadores envían antes de POST

**Líneas 249-263: Procesamiento de Request**

```python
try:
    payload = await request.json()  # Obtener JSON del body
    requirement = (
        (payload.get("requerimiento") or payload.get("requirement") or "").strip()
    )  # Buscar el requerimiento con diferentes nombres posibles

    if not requirement:
        axiom_logger.log_warning("Intento de análisis sin requerimiento")
        response = JSONResponse(
            status_code=400,  # Bad Request
            content={"status": "error", "error": "El campo 'requerimiento' es obligatorio."},
        )
        # Agregar headers CORS
        for key, value in cors_headers.items():
            response.headers[key] = value
        return response
```

**Propósito:**
- Extraer el requerimiento del JSON recibido
- Validar que no esté vacío
- Retornar error 400 si falta el requerimiento

**Líneas 265-273: Llamada a Función y Respuesta**

```python
axiom_logger.log_info("Solicitud recibida desde frontend", {"requirement_length": len(requirement)})

# Llamar a la función de generación (usar .remote() para llamadas asíncronas en endpoints web)
result = generate_test_matrix_and_gherkin.remote(requirement)

response = JSONResponse(content=result)
for key, value in cors_headers.items():
    response.headers[key] = value
return response
```

**Propósito:**
- Loggear la solicitud recibida
- `generate_test_matrix_and_gherkin.remote()`: Ejecuta la función en Modal (remotamente)
- Retornar el resultado como JSON con headers CORS

**Líneas 275-283: Manejo de Errores del Endpoint**

```python
except Exception as e:
    axiom_logger.log_error("Error en endpoint web", e)
    error_response = JSONResponse(
        status_code=500,  # Internal Server Error
        content={"status": "error", "error": f"Error interno: {str(e)}"}
    )
    for key, value in cors_headers.items():
        error_response.headers[key] = value
    return error_response
```

**Propósito:** Capturar cualquier error y retornar respuesta de error con CORS.

---

#### **Líneas 285-321: Ejecución Local**

```python
if __name__ == "__main__":
    # Este bloque solo se ejecuta cuando se corre el script directamente
    print("🌸 Hannah QA Agent V3 - Versión Unificada")
    print("=" * 50)
    print("Integraciones: Doppler + OpenAI + Modal + Axiom + Vercel Frontend")
    print("=" * 50)
    
    # Prueba local
    test_requirement = "El usuario debe poder iniciar sesión con correo y contraseña."
    print(f"\n📋 Requerimiento de prueba: {test_requirement}\n")
    
    try:
        # .local() ejecuta la función localmente (no en Modal)
        result = generate_test_matrix_and_gherkin.local(test_requirement)
        # ... mostrar resultados
    except Exception as e:
        # ... manejar errores
```

**Propósito:**
- Permitir ejecutar el script localmente para pruebas
- `.local()`: Ejecuta la función en tu máquina local (no en Modal)
- Útil para desarrollo y debugging

---

### `src/IA_agentQA_ms_modal.py` - Explicación

Este archivo es muy similar a `IA_agentQA_V3.py`, pero con diferencias clave:

#### **Diferencias Principales:**

1. **Línea 29: Dataset diferente**
   ```python
   AXIOM_DATASET = os.getenv("AXIOM_DATASET", "hannah-qa-agent-ms")
   ```
   - Usa un dataset separado para logs de microservicios

2. **Línea 64: Source diferente**
   ```python
   "source": "hannah_ms_agent_modal",
   ```
   - Identificador diferente para distinguir logs

3. **Líneas 137-155: Prompts especializados**
   ```python
   SYSTEM_PROMPT = """
   Eres un QA Engineer experto en pruebas de microservicios (API REST).
   ...
   """
   
   USER_PROMPT = f"""...
   | ID | Endpoint | Método | Descripción | Datos de entrada | Código esperado | Resultado esperado |
   ...
   """
   ```
   - Prompts enfocados en APIs REST
   - Incluye columnas específicas para microservicios (Endpoint, Método, Código esperado)

4. **Línea 121: Nombre de app diferente**
   ```python
   app = modal.App("hannah-ms-agent", image=image)
   ```
   - App separada en Modal para microservicios

5. **Línea 236: Endpoint diferente**
   ```python
   async def analizar_requerimiento_ms(request: Request):
   ```
   - Función con nombre diferente para evitar conflictos

---

## 📄 Archivos Principales - Frontend

### `frontend/src/app/page.tsx` - Explicación Línea por Línea

#### **Líneas 1-3: Imports**

```typescript
"use client";  // Indica que este componente se ejecuta en el cliente (React)

import { FormEvent, useState } from "react";  // Hooks de React
```

**Propósito:**
- `"use client"`: Next.js App Router requiere esto para componentes con interactividad
- `FormEvent`: Tipo para eventos de formulario
- `useState`: Hook para manejar estado del componente

#### **Líneas 5-12: Tipo de Respuesta**

```typescript
type HannahResponse = {
  status: string;                    // "success" o "error"
  output: string;                    // Respuesta completa de OpenAI
  matrix_data: Record<string, string>[];  // Array de objetos (filas de la matriz)
  matrix_columns: string[];          // Nombres de las columnas
  gherkin_content: string;          // Casos Gherkin generados
  error?: string;                   // Mensaje de error (opcional)
};
```

**Propósito:** Definir la estructura TypeScript de la respuesta del backend.

#### **Líneas 14-16: Configuración del Endpoint**

```typescript
// Usar la variable de entorno o el endpoint de Modal como fallback
const ENDPOINT = process.env.NEXT_PUBLIC_MODAL_ENDPOINT || 
                 "https://greynner--hannah-qa-agent-v3-analizar-requerimiento.modal.run";
```

**Propósito:**
- `NEXT_PUBLIC_*`: Variables de entorno accesibles en el cliente (Next.js)
- Fallback a URL directa si no hay variable de entorno
- Esto permite que funcione incluso sin configurar la variable

#### **Líneas 18-22: Estado del Componente**

```typescript
export default function Home() {
  const [requirement, setRequirement] = useState("");  // Texto del requerimiento
  const [loading, setLoading] = useState(false);      // Estado de carga
  const [error, setError] = useState<string | null>(null);  // Mensaje de error
  const [result, setResult] = useState<HannahResponse | null>(null);  // Resultado del backend
```

**Propósito:**
- `useState`: Hooks para manejar el estado del componente
- Cada estado tiene su setter (ej: `setRequirement` para actualizar `requirement`)

#### **Líneas 24-59: Manejo del Submit**

```typescript
const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
  e.preventDefault();  // Previene el comportamiento por defecto del formulario

  if (!ENDPOINT) {
    setError("Configura NEXT_PUBLIC_MODAL_ENDPOINT.");
    return;  // Sale si no hay endpoint
  }

  if (!requirement.trim()) {
    setError("Ingresa un requerimiento.");
    return;  // Sale si el requerimiento está vacío
  }

  setLoading(true);   // Activa el estado de carga
  setError(null);    // Limpia errores anteriores

  try {
    // Hace la petición POST al backend
    const res = await fetch(ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ requerimiento: requirement }),  // Envía el requerimiento
    });

    const data: HannahResponse = await res.json();  // Parsea la respuesta JSON

    if (!res.ok || data.status !== "success") {
      throw new Error(data.error || "Error al generar.");  // Lanza error si falla
    }

    setResult(data);  // Guarda el resultado exitoso
  } catch (err) {
    setError(err instanceof Error ? err.message : "Error inesperado.");  // Captura errores
    setResult(null);  // Limpia el resultado
  } finally {
    setLoading(false);  // Siempre desactiva el loading
  }
};
```

**Propósito:**
- Manejar el envío del formulario
- Validar inputs
- Hacer petición al backend
- Manejar respuestas y errores

#### **Línea 62: Helper para Verificar Matriz**

```typescript
const hasMatrix = result && result.matrix_columns?.length && result.matrix_data?.length;
```

**Propósito:** Verificar si hay datos de matriz para mostrar (evita errores si está vacío).

#### **Líneas 64-167: JSX del Componente**

```typescript
return (
  <div className="flex min-h-screen justify-center bg-gray-100 py-12 px-4">
    {/* Contenedor principal con Tailwind CSS */}
    
    <main className="w-full max-w-4xl space-y-8 rounded-2xl border border-gray-200 bg-white p-8 shadow-lg">
      {/* Card principal */}
      
      <header>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          🧠 Hannah QA Agent
        </h1>
        <p className="text-gray-600">
          Genera matrices de prueba y casos Gherkin con IA
        </p>
      </header>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Formulario con validación de endpoint */}
        {!ENDPOINT && (
          <div className="rounded-xl border border-orange-300 bg-orange-50 p-4 text-sm text-orange-800">
            ⚠️ Configura NEXT_PUBLIC_MODAL_ENDPOINT
          </div>
        )}
        
        <label className="block">
          <span className="text-sm font-semibold text-green-700 uppercase mb-2 block">
            Requerimiento QA
          </span>
          <textarea
            value={requirement}  // Valor controlado por React
            onChange={(e) => setRequirement(e.target.value)}  // Actualiza estado al escribir
            rows={6}
            className="w-full rounded-xl border border-gray-200 bg-gray-50 p-4 text-gray-700 focus:border-green-400 focus:ring-2 focus:ring-green-200 outline-none transition"
            placeholder="Ejemplo: Como usuario quiero iniciar sesión..."
          />
        </label>
        
        <button
          type="submit"
          disabled={loading}  // Deshabilita durante la carga
          className="w-full rounded-xl bg-gradient-to-r from-yellow-400 via-orange-400 to-green-400 px-6 py-3 font-semibold text-gray-900 transition hover:shadow-md disabled:opacity-60 disabled:cursor-not-allowed"
        >
          {loading ? "⏳ Generando..." : "🚀 Enviar a Hannah"}
        </button>
        
        {error && (
          <div className="rounded-xl border border-red-300 bg-red-50 p-4 text-sm text-red-800">
            ❌ {error}
          </div>
        )}
      </form>

      {result && (
        <section className="space-y-6 rounded-2xl border border-gray-200 bg-gray-50 p-6">
          {/* Sección de resultados */}
          
          {hasMatrix && (
            <div className="overflow-x-auto rounded-xl border border-gray-200 bg-white">
              <table className="min-w-full divide-y divide-gray-200 text-sm">
                <thead className="bg-green-50 text-xs uppercase text-green-700">
                  <tr>
                    {result.matrix_columns.map((col) => (
                      <th key={col} className="px-4 py-3 font-medium">{col}</th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {result.matrix_data.map((row, i) => (
                    <tr key={i} className="bg-white">
                      {result.matrix_columns.map((col) => (
                        <td key={col} className="px-4 py-3 text-gray-700">{row[col]}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {result.gherkin_content && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">🧾 Casos Gherkin</h3>
              <pre className="whitespace-pre-wrap rounded-xl border border-yellow-200 bg-yellow-50 p-4 text-sm">
                {result.gherkin_content}
              </pre>
            </div>
          )}
        </section>
      )}
    </main>
  </div>
);
```

**Propósito:**
- Renderizar la interfaz de usuario
- Mostrar formulario
- Mostrar resultados en tabla
- Mostrar casos Gherkin
- Manejar estados de loading y error

**Conceptos clave:**
- `className`: Clases de Tailwind CSS para estilos
- `{result && ...}`: Renderizado condicional (solo si hay resultado)
- `.map()`: Iterar sobre arrays para renderizar listas
- `key={i}`: Propiedad requerida por React para listas

---

### `frontend/src/app/ms/page.tsx` - Diferencias

Este archivo es casi idéntico a `page.tsx`, pero con estas diferencias:

1. **Línea 15: Endpoint diferente**
   ```typescript
   const ENDPOINT = process.env.NEXT_PUBLIC_MODAL_ENDPOINT_MS || ...
   ```

2. **Línea 18: Nombre de función diferente**
   ```typescript
   export default function MicroservicesPage() {
   ```

3. **Líneas 68-73: Título y descripción diferentes**
   ```typescript
   <h1>🤖 Hannah MS Agent</h1>
   <p>Genera casos de prueba especializados para microservicios (API REST)</p>
   ```

4. **Líneas 84-85: Label diferente**
   ```typescript
   <span>Requerimiento de Microservicio</span>
   ```

5. **Líneas 99-100: Colores diferentes (azul/púrpura en lugar de verde/naranja)**
   ```typescript
   className="...from-blue-400 via-purple-400 to-indigo-400..."
   ```

---

### `frontend/src/app/layout.tsx` - Explicación

```typescript
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });  // Carga fuente Inter de Google Fonts

export const metadata: Metadata = {
  title: "Hannah QA Agent - Generador de Matrices de Prueba",
  description: "Genera matrices de prueba y casos Gherkin con IA",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
```

**Propósito:**
- Define el layout raíz de la aplicación Next.js
- Configura metadatos (título, descripción) para SEO
- Carga la fuente Inter
- Aplica estilos globales
- `{children}`: Renderiza el contenido de cada página

---

## 📄 Archivos de Configuración

### `requirements.txt`

```txt
fastapi==0.111.0
httpx==0.28.1
```

**Propósito:** Dependencias mínimas para el proxy Python que corre en Vercel.

> Para el stack completo del backend utiliza `requirements.local.txt`, que mantiene todas las librerías necesarias para desarrollo (OpenAI, LangChain, Modal, Playwright, etc.).

---

### `frontend/package.json`

```json
{
  "name": "frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",        // Servidor de desarrollo
    "build": "next build",    // Build para producción
    "start": "next start",    // Servidor de producción
    "lint": "eslint"          // Linter de código
  },
  "dependencies": {
    "react": "19.2.0",        // Biblioteca React
    "react-dom": "19.2.0",    // React para DOM
    "next": "16.0.0"          // Framework Next.js
  },
  "devDependencies": {
    "typescript": "^5",       // Compilador TypeScript
    "@types/node": "^20",     // Tipos para Node.js
    "@types/react": "^19",    // Tipos para React
    "tailwindcss": "^4",      // Framework CSS
    "eslint": "^9"            // Linter
  }
}
```

**Propósito:** Define dependencias y scripts de Node.js para el frontend.

---

### `frontend/next.config.ts`

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
};

export default nextConfig;
```

**Propósito:** Configuración de Next.js (actualmente vacía, usa defaults).

---

### `frontend/vercel.json`

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "installCommand": "npm install"
}
```

**Propósito:**
- Configuración para deployment en Vercel
- Define comandos de build e instalación
- Especifica el framework (Next.js)

---

### `frontend/tsconfig.json`

**Propósito:** Configuración del compilador TypeScript (opciones de compilación, paths, etc.)

---

## 🔄 Flujo de Datos Completo

### 1. Usuario ingresa requerimiento en Frontend

```
Usuario → Textarea → useState("requirement") → handleSubmit()
```

### 2. Frontend envía request al Backend

```
fetch(ENDPOINT, {
  method: "POST",
  body: JSON.stringify({ requerimiento: requirement })
})
```

### 3. Backend recibe request

```
analizar_requerimiento(request) → 
  payload.get("requerimiento") → 
  generate_test_matrix_and_gherkin.remote(requirement)
```

### 4. Backend procesa con OpenAI

```
OpenAI API → 
  SYSTEM_PROMPT + FEW_SHOT_EXAMPLE + requirement → 
  response.choices[0].message.content
```

### 5. Backend procesa respuesta

```
output → 
  Parsear tabla Markdown → DataFrame → 
  Extraer Gherkin → 
  Construir resultado JSON
```

### 6. Backend retorna respuesta

```
JSONResponse(result) → 
  Frontend recibe → 
  setResult(data) → 
  Renderizar tabla y Gherkin
```

---

## 🔐 Seguridad y Variables de Entorno

### Variables en Doppler

- `OPENAI_API_KEY` - Clave de API de OpenAI
- `AXIOM_API_TOKEN` - Token de Axiom
- `AXIOM_ORG_ID` - ID de organización
- `AXIOM_DATASET` - Nombre del dataset
- `ENVIRONMENT` - Entorno (production/development)

### Variables en Vercel

- `NEXT_PUBLIC_MODAL_ENDPOINT` - URL del endpoint general
- `NEXT_PUBLIC_MODAL_ENDPOINT_MS` - URL del endpoint MS

**Nota:** `NEXT_PUBLIC_*` hace que la variable sea accesible en el cliente (navegador).

---

## 📊 Estructura de Respuesta JSON

```json
{
  "status": "success",
  "output": "Respuesta completa de OpenAI...",
  "matrix_data": [
    {
      "ID": "TC001",
      "Escenario": "Login exitoso",
      "Datos de entrada": "Usuario válido",
      "Resultado esperado": "Acceso concedido"
    }
  ],
  "matrix_columns": ["ID", "Escenario", "Datos de entrada", "Resultado esperado"],
  "gherkin_content": "Feature: ...\n  Scenario: ..."
}
```

---

## 🎯 Conceptos Clave

### Modal

- **Función:** `@app.function()` - Ejecuta código en la nube
- **Endpoint:** `@modal.fastapi_endpoint()` - Expone función como HTTP
- **Secretos:** `modal.Secret.from_name()` - Variables de entorno seguras
- **Imagen:** `modal.Image.debian_slim().pip_install()` - Define dependencias

### Next.js

- **App Router:** Sistema de routing basado en carpetas
- **Server Components:** Por defecto, componentes se renderizan en servidor
- **Client Components:** `"use client"` para interactividad
- **Environment Variables:** `NEXT_PUBLIC_*` para variables del cliente

### React

- **Hooks:** `useState` para estado, `useEffect` para efectos
- **Event Handlers:** Funciones que manejan eventos (onSubmit, onChange)
- **Conditional Rendering:** `{condition && <Component />}`
- **Lists:** `.map()` para renderizar arrays

---

## 📝 Notas Finales

- **Modularidad:** Cada archivo tiene una responsabilidad clara
- **Reutilización:** `AxiomLogger` se puede usar en múltiples archivos
- **Error Handling:** Todos los errores se capturan y loggean
- **Type Safety:** TypeScript en frontend, type hints en Python
- **CORS:** Configurado para permitir requests desde Vercel
- **Fallbacks:** El código funciona incluso si faltan algunas configuraciones

---

**Última actualización:** Octubre 2025
