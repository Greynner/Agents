# 🌸 Hannah QA Agent + Axiom Integration

## 🎯 Resumen

Integración completa de Hannah QA Agent con logging automático a Axiom usando Doppler para la gestión de variables de entorno.

## 📁 Archivos de la Integración

### 1. **`app_hannah_error_handling_with_axiom.py`** - Aplicación Principal
**Ubicación**: `src/app_hannah_error_handling_with_axiom.py`

**Características**:
- ✅ Interfaz Streamlit completa
- ✅ Backend Modal (Serverless)
- ✅ Variables de entorno con Doppler
- ✅ **Logging automático a Axiom**
- ✅ Manejo de errores robusto

### 2. **`test_hannah_axiom_integration.py`** - Test de Integración
**Propósito**: Verificar que el logging a Axiom funcione correctamente

```bash
doppler run -- python test_hannah_axiom_integration.py
```

### 3. **`run_hannah_with_axiom.py`** - Ejecutor
**Propósito**: Ejecutar Hannah con todas las integraciones

```bash
python run_hannah_with_axiom.py
```

## 🔧 Configuración Requerida

### Variables de Doppler:
```bash
# Variables principales
doppler secrets set AXIOM_API_TOKEN="tu_token_aqui"
doppler secrets set AXIOM_ORG_ID="tu_org_id_aqui"
doppler secrets set AXIOM_DATASET="hannah-qa-agent"  # opcional
doppler secrets set ENVIRONMENT="production"         # opcional

# Variables de Modal (ya configuradas)
doppler secrets set MODAL_TOKEN="tu_modal_token"
doppler secrets set OPENAI_API_KEY="tu_openai_key"
```

### Dependencias:
```bash
pip install streamlit requests pandas openai modal python-dotenv
```

## 📊 Tipos de Logs Enviados a Axiom

### 1. **Logs de Sesión de Usuario**
```json
{
  "timestamp": "2025-10-23T23:34:16.510846+00:00",
  "level": "INFO",
  "message": "Usuario inició sesión en Hannah QA Agent",
  "source": "hannah_qa_agent",
  "user_action": "inició sesión",
  "metadata": {
    "app_name": "Hannah QA Agent",
    "version": "2.0.0",
    "platform": "streamlit"
  }
}
```

### 2. **Logs de Procesamiento**
```json
{
  "timestamp": "2025-10-23T23:34:16.510846+00:00",
  "level": "INFO",
  "message": "Usuario solicitó generación de casos de prueba",
  "user_action": "solicitó generación",
  "metadata": {
    "requerimiento_length": 150,
    "requerimiento_preview": "Como usuario quiero..."
  }
}
```

### 3. **Logs de Modal Backend**
```json
{
  "timestamp": "2025-10-23T23:34:16.510846+00:00",
  "level": "INFO",
  "message": "Iniciando procesamiento en Modal",
  "user_action": "modal_processing_start",
  "metadata": {
    "backend": "modal",
    "status": "processing"
  }
}
```

### 4. **Logs de Éxito**
```json
{
  "timestamp": "2025-10-23T23:34:16.510846+00:00",
  "level": "INFO",
  "message": "✅ generación de casos de prueba en Modal completado exitosamente",
  "user_action": "generación exitosa",
  "metadata": {
    "casos_generados": 5,
    "gherkin_generado": true,
    "output_length": 1200
  }
}
```

### 5. **Logs de Exportación**
```json
{
  "timestamp": "2025-10-23T23:34:16.510846+00:00",
  "level": "INFO",
  "message": "✅ exportación de matriz de pruebas completado exitosamente",
  "user_action": "exportación exitosa",
  "metadata": {
    "archivo": "matriz_pruebas.xlsx",
    "filas": 5
  }
}
```

### 6. **Logs de Error**
```json
{
  "timestamp": "2025-10-23T23:34:16.510846+00:00",
  "level": "ERROR",
  "message": "Error en Hannah QA Agent: Error en Modal: Timeout",
  "error_details": {
    "error_type": "TimeoutError",
    "error_message": "Error en Modal: Timeout",
    "context": "modal_backend_call",
    "traceback": "..."
  }
}
```

## 🚀 Formas de Ejecutar

### Opción 1: Ejecutor Automático (Recomendado)
```bash
python run_hannah_with_axiom.py
```

### Opción 2: Ejecución Manual
```bash
doppler run -- streamlit run src/app_hannah_error_handling_with_axiom.py
```

### Opción 3: Con Puerto Específico
```bash
doppler run -- streamlit run src/app_hannah_error_handling_with_axiom.py --server.port 8502
```

## 📈 Flujo Completo de Logging

1. **Inicio de Sesión** → Log de usuario inició sesión
2. **Ingreso de Requerimiento** → Log con detalles del requerimiento
3. **Procesamiento en Modal** → Log de inicio de procesamiento
4. **Generación Exitosa** → Log con métricas de casos generados
5. **Exportación de Archivos** → Log de archivos exportados
6. **Fin de Sesión** → Log de usuario finalizó sesión

## 🔍 Verificación de Logs

### Test de Integración:
```bash
doppler run -- python test_hannah_axiom_integration.py
```

### Verificar Logs en Axiom:
1. Ve a tu dashboard de Axiom
2. Busca el dataset `hannah-qa-agent` (o el configurado)
3. Filtra por `source:hannah_qa_agent`
4. Verifica que los logs aparezcan en tiempo real

## 🎯 Beneficios de la Integración

### Para Desarrollo:
- ✅ **Trazabilidad completa** de interacciones del usuario
- ✅ **Monitoreo de errores** en tiempo real
- ✅ **Métricas de uso** de la aplicación
- ✅ **Debugging facilitado** con logs estructurados

### Para Producción:
- ✅ **Monitoreo de rendimiento** de Modal
- ✅ **Análisis de uso** de la aplicación
- ✅ **Detección temprana** de problemas
- ✅ **Auditoría completa** de actividades

## 🛠️ Solución de Problemas

### Error: "Variables de Axiom no disponibles"
```bash
# Verificar variables
doppler secrets

# Configurar si faltan
doppler secrets set AXIOM_API_TOKEN="tu_token"
doppler secrets set AXIOM_ORG_ID="tu_org_id"
```

### Error: "Dataset no encontrado"
```bash
# Crear dataset en Axiom o usar uno existente
doppler secrets set AXIOM_DATASET="nombre_del_dataset_existente"
```

### Error: "Streamlit no encontrado"
```bash
# Instalar dependencias
pip install streamlit
```

## 🎉 ¡Integración Completa!

La aplicación Hannah QA Agent ahora incluye:
- ✅ **Interfaz Streamlit** moderna y funcional
- ✅ **Backend Modal** serverless y escalable
- ✅ **Variables Doppler** seguras y centralizadas
- ✅ **Logging Axiom** automático y estructurado
- ✅ **Manejo de errores** robusto y detallado

**¡Hannah está lista para producción con monitoreo completo!** 🌸
