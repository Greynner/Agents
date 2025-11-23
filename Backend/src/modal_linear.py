import modal
import os
import requests
from openai import OpenAI

app = modal.App("qa-linear-integration")
image = (
    modal.Image.debian_slim()
    .pip_install("requests", "openai")
)

LINEAR_URL = "https://api.linear.app/graphql"


# --- Leer Issue de Linear ---
def get_issue(issue_id: str, linear_api_key: str):
    # Linear API NO acepta el prefijo "Bearer", solo la API key directamente
    # Removemos "Bearer " si está presente
    api_key = linear_api_key.replace("Bearer ", "").strip()
    
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }

    # Determinar si es un identificador corto (ej: "QA-4") o un UUID completo
    # Los identificadores cortos tienen formato "TEAM-NUMBER" (contienen un guion)
    # Los UUIDs son strings largos sin guiones en esa posición
    is_identifier = "-" in issue_id and not issue_id.startswith(("http", "https"))
    
    if is_identifier:
        # Para identificadores cortos, usar la query issues con filtro
        # El formato es "TEAM-NUMBER", separamos en team y number
        parts = issue_id.split("-", 1)
        if len(parts) == 2:
            team_key = parts[0]
            try:
                number = int(parts[1])
            except ValueError:
                raise ValueError(f"Formato de identificador inválido: {issue_id}. El número debe ser un entero (ej: 'QA-4')")
            query = f"""
            query {{
              issues(
                filter: {{
                  team: {{ key: {{ eq: "{team_key}" }} }}
                  number: {{ eq: {number} }}
                }}
                first: 1
              ) {{
                nodes {{
                  id
                  title
                  description
                  identifier
                  team {{
                    id
                  }}
                }}
              }}
            }}
            """
        else:
            raise ValueError(f"Formato de identificador inválido: {issue_id}. Debe ser 'TEAM-NUMBER' (ej: 'QA-4')")
    else:
        # Usar id para buscar por UUID completo
        query = f"""
        query {{
          issue(id: "{issue_id}") {{
            id
            title
            description
            identifier
            team {{
              id
            }}
          }}
        }}
        """

    resp = requests.post(LINEAR_URL, json={"query": query}, headers=headers)
    resp_data = resp.json()
    
    # Manejo de errores de la API de Linear
    if "errors" in resp_data:
        error_msg = resp_data["errors"][0].get("message", "Error desconocido de Linear")
        raise ValueError(f"Error de Linear API: {error_msg}")
    
    # Manejar respuesta según el tipo de query
    if is_identifier:
        # Para queries con issues (filtro)
        if "data" not in resp_data or not resp_data["data"].get("issues", {}).get("nodes"):
            raise ValueError(f"Issue '{issue_id}' no encontrado en Linear. Verifica que el identificador sea correcto (ej: 'QA-4')")
        issue = resp_data["data"]["issues"]["nodes"][0]
    else:
        # Para queries con issue (UUID)
        if "data" not in resp_data or resp_data["data"]["issue"] is None:
            raise ValueError(f"Issue '{issue_id}' no encontrado en Linear. Verifica que el UUID sea correcto")
        issue = resp_data["data"]["issue"]
    
    return issue


# --- Generar contenido QA ---
def generate_test_assets(title: str, description: str, openai_api_key: str):
    client = OpenAI(api_key=openai_api_key)
    
    prompt = f"""
    Eres un QA Senior. A partir de este requerimiento genera:

    1. Test Plan completo
    2. Matriz de pruebas
    3. 10 casos de prueba detallados
    4. Escenarios Gherkin

    --- Requerimiento ---
    Título: {title}
    Descripción: {description}
    """

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content


# --- Crear sub-issue en Linear ---
def create_sub_issue(parent_uuid: str, content: str, linear_api_key: str, team_id: str, parent_identifier: str = None):
    """
    Crea una sub-issue en Linear.
    
    Args:
        parent_uuid: UUID completo del issue padre (requerido para parentId)
        content: Contenido de la descripción de la sub-issue
        linear_api_key: API key de Linear
        team_id: UUID del equipo (requerido para teamId)
        parent_identifier: Identificador corto del issue padre (opcional, para el título)
    """
    # Linear API NO acepta el prefijo "Bearer", solo la API key directamente
    # Removemos "Bearer " si está presente
    api_key = linear_api_key.replace("Bearer ", "").strip()
    
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }

    mutation = """
    mutation CreateIssue($input: IssueCreateInput!) {
      issueCreate(input: $input) {
        success
        issue {
          id
          title
          identifier
        }
      }
    }
    """

    # Usar el identificador corto en el título si está disponible, sino el UUID
    title_ref = parent_identifier if parent_identifier else parent_uuid
    
    variables = {
        "input": {
            "title": f"QA – Test Plan, Matriz y Casos para {title_ref}",
            "description": content,
            "parentId": parent_uuid,  # Debe ser el UUID completo
            "teamId": team_id  # UUID del equipo (requerido)
        }
    }

    resp = requests.post(
        LINEAR_URL,
        json={"query": mutation, "variables": variables},
        headers=headers
    )

    resp_data = resp.json()
    
    # Manejo de errores de la API de Linear
    if "errors" in resp_data:
        error_msg = resp_data["errors"][0].get("message", "Error desconocido de Linear")
        raise ValueError(f"Error de Linear API al crear sub-issue: {error_msg}")
    
    return resp_data


@app.function(
    image=image,
    secrets=[modal.Secret.from_name("qa-agent-secrets")]
)
def generate_tests(issue_id: str):
    """
    Genera assets de QA (Test Plan, Matriz, Casos de Prueba, Gherkin) 
    para un issue de Linear y crea una sub-issue con el contenido generado.
    
    Args:
        issue_id: Identificador del issue de Linear (formato "TEAM-NUMBER" o UUID)
    
    Returns:
        dict: Contiene el issue padre, el contenido generado y la respuesta de la sub-issue creada
    """
    print(f"🚀 Iniciando generación de tests para issue: {issue_id}")
    
    # Obtener las API keys desde las variables de entorno (inyectadas por Modal secrets o Doppler)
    linear_api_key = os.getenv("LINEAR_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not linear_api_key:
        raise ValueError("LINEAR_API_KEY no está configurada")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY no está configurada")
    
    # 1. Leer issue desde Linear
    print(f"📋 Obteniendo información del issue {issue_id} desde Linear...")
    issue = get_issue(issue_id, linear_api_key)
    print(f"✅ Issue encontrado: {issue.get('identifier', 'N/A')} - {issue.get('title', 'Sin título')}")
    
    # Obtener el ID completo (UUID) del issue para usar como parentId
    # Si se pasó un identificador corto (ej: "QA-4"), ahora tenemos el UUID en issue["id"]
    parent_uuid = issue["id"]
    issue_identifier = issue.get("identifier", issue_id)  # Usar el identifier para el título
    
    # Obtener el teamId del issue padre (requerido para crear la sub-issue)
    team_id = issue.get("team", {}).get("id")
    if not team_id:
        raise ValueError("No se pudo obtener el teamId del issue padre. El issue debe tener un equipo asignado.")

    # 2. Generar contenido QA con IA
    print(f"🤖 Generando assets de QA con OpenAI...")
    content = generate_test_assets(issue["title"], issue.get("description", ""), openai_api_key)
    print(f"✅ Contenido generado ({len(content)} caracteres)")

    # 3. Crear sub-issue en Linear (usar UUID para parentId y teamId)
    print(f"📝 Creando sub-issue en Linear...")
    result = create_sub_issue(parent_uuid, content, linear_api_key, team_id, issue_identifier)
    
    # Validar respuesta de creación
    if result.get("data", {}).get("issueCreate", {}).get("success"):
        created_issue = result["data"]["issueCreate"]["issue"]
        print(f"✅ Sub-issue creada exitosamente: {created_issue.get('identifier', 'N/A')} - {created_issue.get('title', 'Sin título')}")
    else:
        errors = result.get("errors", [])
        if errors:
            error_msg = errors[0].get("message", "Error desconocido")
            print(f"⚠️ Advertencia al crear sub-issue: {error_msg}")
        else:
            print(f"⚠️ Advertencia: La creación de la sub-issue puede no haber sido exitosa")

    return {
        "status": "success",
        "parent_issue": {
            "id": issue.get("id"),
            "identifier": issue.get("identifier"),
            "title": issue.get("title"),
            "description": issue.get("description")
        },
        "generated_content": content,
        "sub_issue": result.get("data", {}).get("issueCreate", {}).get("issue") if result.get("data", {}).get("issueCreate", {}).get("success") else None,
        "sub_issue_response": result
    }