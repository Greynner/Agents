# Configuración de Vercel para Hannah QA Agent

## Problema Resuelto

El error `500: INTERNAL_SERVER_ERROR` en Vercel se debía a:
1. El frontend llamaba directamente a Modal sin usar el proxy
2. El proxy no tenía manejo adecuado de errores
3. Faltaban variables de entorno en Vercel

## Solución Implementada

### 1. Frontend Actualizado
- Ahora usa el proxy de Next.js API Route en lugar de llamar directamente a Modal
- Mejor manejo de errores con mensajes más descriptivos
- Soporte para CORS mejorado

### 2. Proxy de Next.js (`frontend/src/app/api/analizar-requerimiento/route.ts`)
- Ruta API nativa de Next.js que actúa como proxy
- Manejo robusto de errores
- Logging para debugging
- Soporte completo para CORS
- Validación de variables de entorno
- Timeout configurable

### 3. Proxy Alternativo (`api/modal_proxy.py`)
- Proxy FastAPI alternativo (si prefieres usar Python)
- Manejo robusto de errores
- Logging para debugging
- Soporte completo para CORS
- Validación de variables de entorno

## Variables de Entorno Requeridas en Vercel

Configura estas variables en el dashboard de Vercel (Settings → Environment Variables):

### Obligatorias:
```bash
MODAL_BASE_URL=https://greynner--hannah-qa-agent-v3-analizar-requerimiento.modal.run
```

**⚠️ IMPORTANTE:** Reemplaza esta URL con la URL real de tu endpoint de Modal después de desplegar.

### Opcionales:
```bash
MODAL_API_KEY=tu_api_key_de_modal  # Solo si Modal requiere autenticación
MODAL_PROXY_TIMEOUT=60  # Timeout en segundos (default: 60)
```

## Cómo Obtener la URL de Modal

1. **Despliega la app de Modal:**
   ```bash
   cd IA-Agent-QA/Backend/src
   modal deploy IA_agentQA_V3.py
   ```

2. **Obtén la URL del endpoint:**
   Después del despliegue, Modal mostrará la URL del endpoint. Debería verse así:
   ```
   https://[usuario]--hannah-qa-agent-v3-analizar-requerimiento.modal.run
   ```

3. **También puedes obtenerla con:**
   ```bash
   modal app list
   modal endpoint list hannah-qa-agent-v3
   ```

## Estructura de Rutas

El proxy está configurado como una Next.js API Route:
- `/api/analizar-requerimiento` → Reenvía a Modal

El frontend ahora llama a esta ruta relativa, que funciona tanto en desarrollo como en producción usando la API Route de Next.js.

## Verificación

1. **Verifica que Modal esté desplegado:**
   ```bash
   modal app list
   ```

2. **Prueba el endpoint de Modal directamente:**
   ```bash
   curl -X POST https://[tu-url-modal]/analizar-requerimiento \
     -H "Content-Type: application/json" \
     -d '{"requerimiento": "Test"}'
   ```

3. **Verifica las variables de entorno en Vercel:**
   - Ve a tu proyecto en Vercel
   - Settings → Environment Variables
   - Asegúrate de que `MODAL_BASE_URL` esté configurada

4. **Revisa los logs de Vercel:**
   - En el dashboard de Vercel, ve a la pestaña "Functions"
   - Revisa los logs del proxy para ver errores específicos

## Troubleshooting

### Error: "MODAL_BASE_URL no está configurada"
- **Solución:** Configura la variable `MODAL_BASE_URL` en Vercel

### Error: "Timeout al conectar con Modal"
- **Solución:** Aumenta `MODAL_PROXY_TIMEOUT` o verifica que Modal esté funcionando

### Error: "404 Not Found"
- **Solución:** Verifica que la URL de `MODAL_BASE_URL` sea correcta y que el endpoint esté desplegado

### Error: CORS
- **Solución:** Ya está resuelto con los headers CORS en el proxy

## Próximos Pasos

1. Despliega la app de Modal si no lo has hecho
2. Obtén la URL del endpoint
3. Configura `MODAL_BASE_URL` en Vercel
4. Redespliega la aplicación en Vercel
5. Prueba la aplicación en `https://qa-agent-two.vercel.app/`

