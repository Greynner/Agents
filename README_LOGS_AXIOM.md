# 📤 Scripts para Enviar Logs a Axiom

## 🎯 Resumen

Esta colección de scripts te permite enviar diferentes tipos de logs a Axiom usando Doppler para la gestión de variables de entorno.

## 📁 Scripts Disponibles

### 1. `test_axiom_connection.py` - Test Completo
**Propósito**: Verificar la integración completa entre Axiom y Doppler

```bash
doppler run -- python test_axiom_connection.py
```

**Funcionalidades**:
- ✅ Verifica variables de entorno de Doppler
- ✅ Prueba conexión con Axiom API
- ✅ Envía datos de prueba
- ✅ Intenta consultar datos (puede fallar por permisos)

### 2. `send_log_to_axiom.py` - Log Simple
**Propósito**: Enviar un log básico de prueba a Axiom

```bash
doppler run -- python send_log_to_axiom.py
```

**Funcionalidades**:
- 📤 Envía un log de prueba simple
- 📊 Muestra métricas de respuesta
- ✅ Confirma que la conexión funciona

### 3. `send_custom_log.py` - Log Personalizado
**Propósito**: Enviar logs personalizados con diferentes niveles y datos

```bash
# Log básico
doppler run -- python send_custom_log.py "Mi mensaje personalizado"

# Log con nivel específico
doppler run -- python send_custom_log.py "Error crítico" --level ERROR

# Log con datos personalizados
doppler run -- python send_custom_log.py "Proceso completado" --level INFO --data '{"user_id": 123, "action": "login"}'
```

**Funcionalidades**:
- 📝 Mensajes personalizados
- 🔍 Niveles de log (DEBUG, INFO, WARN, ERROR, FATAL)
- 📋 Datos personalizados en JSON
- 🎯 Control total sobre el contenido del log

### 4. `monitor_and_log.py` - Monitor del Sistema
**Propósito**: Monitorear el sistema y enviar logs automáticamente

```bash
doppler run -- python monitor_and_log.py
```

**Funcionalidades**:
- 📊 Métricas del sistema (CPU, RAM, disco)
- 🔄 Logs de aplicación simulados
- ⏰ Envío periódico de logs
- 🎯 Diferentes tipos de logs (sistema + aplicación)

## 🔧 Configuración Requerida

### Variables de Doppler:
```bash
# Configurar en Doppler
doppler secrets set AXIOM_API_TOKEN="tu_token_aqui"
doppler secrets set AXIOM_ORG_ID="tu_org_id_aqui"
doppler secrets set AXIOM_DATASET="test-dataset"  # opcional
doppler secrets set ENVIRONMENT="development"     # opcional
```

### Dependencias Python:
```bash
pip install requests psutil
```

## 📊 Tipos de Logs Enviados

### 1. **Logs de Sistema**
```json
{
  "timestamp": "2025-10-23T23:34:16.510846+00:00",
  "level": "INFO",
  "message": "📊 Métricas del sistema - CPU: 15.2%, RAM: 74.7%",
  "log_type": "system_metrics",
  "metrics": {
    "cpu_usage": 15.2,
    "memory_usage": 74.7,
    "memory_available": 2147483648,
    "disk_usage": 45.2,
    "disk_free": 50000000000
  }
}
```

### 2. **Logs de Aplicación**
```json
{
  "timestamp": "2025-10-23T23:34:16.510846+00:00",
  "level": "INFO",
  "message": "✅ Proceso completado exitosamente",
  "log_type": "application",
  "user_id": "user_1234",
  "session_id": "session_56789"
}
```

### 3. **Logs Personalizados**
```json
{
  "timestamp": "2025-10-23T23:34:16.510846+00:00",
  "level": "ERROR",
  "message": "❌ Error crítico en base de datos",
  "custom_data": {
    "error_code": "DB_CONNECTION_FAILED",
    "retry_count": 3,
    "last_error": "Connection timeout"
  }
}
```

## 🚀 Ejemplos de Uso

### Verificar Conexión:
```bash
doppler run -- python test_axiom_connection.py
```

### Enviar Log de Prueba:
```bash
doppler run -- python send_log_to_axiom.py
```

### Enviar Log de Error:
```bash
doppler run -- python send_custom_log.py "Error en procesamiento" --level ERROR
```

### Monitorear Sistema:
```bash
doppler run -- python monitor_and_log.py
```

## 📈 Métricas de Éxito

Cuando los logs se envían correctamente, verás:
```
✅ ¡Log enviado exitosamente a Axiom!
📊 Respuesta de Axiom:
   • Eventos ingeridos: 1
   • Eventos fallidos: 0
   • Bytes procesados: 539
   • Longitud WAL: 3
```

## 🔍 Solución de Problemas

### Error: "dataset not found"
- Verificar que `AXIOM_DATASET` esté configurado correctamente
- Crear el dataset en Axiom si no existe

### Error: "token does not have access"
- Normal para tokens con permisos limitados
- La ingesta funciona, solo las consultas pueden fallar

### Error: "variables not available"
- Verificar configuración de Doppler: `doppler secrets`
- Ejecutar con Doppler: `doppler run -- python script.py`

## 🎉 ¡Integración Completa!

Todos los scripts confirman que:
- ✅ **Doppler** funciona correctamente
- ✅ **Axiom** está accesible
- ✅ **Variables de entorno** están disponibles
- ✅ **Ingesta de datos** funciona perfectamente
- ✅ **Conexión** es estable y confiable
