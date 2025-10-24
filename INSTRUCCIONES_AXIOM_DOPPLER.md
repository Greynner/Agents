# 🔍 Instrucciones para Test de Axiom con Doppler

## 📋 Prerrequisitos

1. **Doppler CLI instalado y configurado**
2. **Variables de entorno configuradas en Doppler:**
   - `AXIOM_API_TOKEN`: Token de API de Axiom
   - `AXIOM_ORG_ID`: ID de la organización en Axiom
   - `AXIOM_DATASET`: Nombre del dataset (opcional, por defecto: 'test-dataset')
   - `ENVIRONMENT`: Entorno (opcional, por defecto: 'development')

## 🚀 Formas de Ejecutar

### Opción 1: Ejecución Directa con Doppler
```bash
# Desde el directorio raíz del proyecto
doppler run -- python test_axiom_connection.py
```

### Opción 2: Usando el ejecutor universal (recomendado)
```bash
# Usando el script run_src_with_doppler.py
python src/run_src_with_doppler.py test_axiom_connection.py
```

### Opción 3: Ejecución con Doppler en carpeta src/
```bash
# Si prefieres mover el archivo a src/
mv test_axiom_connection.py src/
doppler run -- python src/test_axiom_connection.py
```

## 🔧 Configuración de Variables en Doppler

### Variables Requeridas:
```bash
# Configurar en Doppler
doppler secrets set AXIOM_API_TOKEN="tu_token_aqui"
doppler secrets set AXIOM_ORG_ID="tu_org_id_aqui"
doppler secrets set AXIOM_DATASET="tu_dataset_aqui"  # opcional
doppler secrets set ENVIRONMENT="production"  # opcional
```

### Verificar Variables:
```bash
# Ver todas las variables
doppler secrets

# Ver variables específicas
doppler secrets get AXIOM_API_TOKEN
doppler secrets get AXIOM_ORG_ID
```

## 📊 Qué Hace el Test

El archivo `test_axiom_connection.py` realiza las siguientes verificaciones:

1. **✅ Verificación de Variables de Entorno**
   - Confirma que todas las variables de Doppler estén disponibles
   - Muestra valores enmascarados por seguridad

2. **🔗 Test de Conexión Básica**
   - Verifica que la API de Axiom sea accesible
   - Valida las credenciales

3. **📤 Test de Ingesta de Datos**
   - Envía datos de prueba a Axiom
   - Confirma que los datos se procesan correctamente

4. **🔍 Test de Consulta**
   - Ejecuta una consulta simple en Axiom
   - Verifica que los datos se pueden recuperar

## 🎯 Resultados Esperados

### ✅ Éxito:
```
🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!
✅ Integración Axiom + Doppler funcionando correctamente
```

### ❌ Fallo Común:
```
❌ AXIOM_API_TOKEN: NO DISPONIBLE
❌ FALLO: Variables de entorno no disponibles
```

## 🛠️ Solución de Problemas

### Error: "Doppler no está instalado"
```bash
# Instalar Doppler CLI
curl -Ls --tlsv1.2 --proto "=https" --retry 3 https://cli.doppler.com/install.sh | sh
```

### Error: "Variables no disponibles"
```bash
# Verificar configuración de Doppler
doppler configure
doppler secrets
```

### Error: "Conexión fallida con Axiom"
- Verificar que `AXIOM_API_TOKEN` sea válido
- Verificar que `AXIOM_ORG_ID` sea correcto
- Verificar conectividad de red

## 📝 Notas Importantes

- El test envía datos reales a Axiom (datos de prueba)
- Los datos incluyen timestamp y metadatos de la prueba
- El dataset debe existir en Axiom antes de ejecutar
- Las credenciales se muestran enmascaradas por seguridad

## 🔄 Ejecución Continua

Para monitoreo continuo, puedes ejecutar el test periódicamente:

```bash
# Ejecutar cada 5 minutos
watch -n 300 "doppler run -- python test_axiom_connection.py"
```
