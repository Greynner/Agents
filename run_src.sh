#!/bin/bash
# 🚀 Script de conveniencia para ejecutar archivos en src/ con Doppler

# Verificar que Doppler esté instalado
if ! command -v doppler &> /dev/null; then
    echo "❌ Doppler no está instalado. Instálalo con: curl -Ls --tlsv1.2 --proto "=https" --retry 3 https://cli.doppler.com/install.sh | sh"
    exit 1
fi

# Verificar que estamos en el directorio correcto
if [ ! -d "src" ]; then
    echo "❌ La carpeta src/ no existe. Ejecuta este script desde la raíz del proyecto."
    exit 1
fi

# Función para mostrar ayuda
show_help() {
    echo "🚀 Ejecutor de archivos src/ con Doppler"
    echo ""
    echo "Uso:"
    echo "  ./run_src.sh <archivo> [argumentos]"
    echo ""
    echo "Ejemplos:"
    echo "  ./run_src.sh app.py"
    echo "  ./run_src.sh app_hannah_error_handling.py"
    echo "  ./run_src.sh app_ms_agent.py"
    echo "  ./run_src.sh test_doppler_src.py"
    echo ""
    echo "O usando npm:"
    echo "  npm run src:app"
    echo "  npm run src:app-hannah"
    echo "  npm run src:app-ms"
    echo "  npm run src:main"
}

# Verificar argumentos
if [ $# -eq 0 ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    show_help
    exit 0
fi

# Construir la ruta del archivo
FILE_PATH="src/$1"

# Verificar que el archivo existe
if [ ! -f "$FILE_PATH" ]; then
    echo "❌ El archivo $FILE_PATH no existe"
    exit 1
fi

# Determinar el comando según el archivo
if [[ "$1" == *"streamlit"* ]] || [[ "$1" == "app.py" ]] || [[ "$1" == "app_hannah_error_handling.py" ]] || [[ "$1" == "app_ms_agent.py" ]]; then
    echo "🚀 Ejecutando $FILE_PATH con Streamlit y Doppler..."
    doppler run -- streamlit run "$FILE_PATH" "${@:2}"
else
    echo "🚀 Ejecutando $FILE_PATH con Python y Doppler..."
    doppler run -- python "$FILE_PATH" "${@:2}"
fi
