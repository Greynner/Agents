#!/bin/bash
# 🚀 Scripts para ejecutar todos los .py de src/

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Verificar Doppler
if ! command -v doppler &> /dev/null; then
    echo -e "${RED}❌ Doppler no está instalado${NC}"
    echo -e "${YELLOW}Instálalo con:${NC} curl -Ls https://cli.doppler.com/install.sh | sh"
    exit 1
fi

# Función para mostrar menú
show_menu() {
    clear
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}🧠 Hannah QA Agent - Ejecutor de Apps${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${YELLOW}📱 APPS STREAMLIT:${NC}"
    echo "  1) app.py                           - App básica Hannah"
    echo "  2) app_hannah_error_handling.py     - Hannah con Modal"
    echo "  3) app_hannah_error_handling_with_axiom.py - Hannah con Modal + Axiom"
    echo "  4) app_ms_agent.py                  - App para Microservicios"
    echo ""
    echo -e "${YELLOW}🧪 TESTS:${NC}"
    echo "  5) main.py                          - Test OpenAI"
    echo "  6) test_doppler.py                  - Test Doppler"
    echo "  7) test_modal_connection.py         - Test Modal"
    echo "  8) test_axiom_connection.py         - Test Axiom"
    echo "  9) test_hannah_axiom_integration.py - Test Hannah + Axiom"
    echo ""
    echo -e "${YELLOW}🔧 UTILIDADES:${NC}"
    echo "  10) hannah_modal_client.py          - Cliente Modal"
    echo "  11) run_hannah_with_axiom.py        - Runner Hannah + Axiom"
    echo "  12) run_src_with_doppler.py         - Runner con Doppler"
    echo "  13) hannah_modal_app.py             - App Modal"
    echo ""
    echo -e "${RED}  0) Salir${NC}"
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# Función para ejecutar Streamlit apps
run_streamlit() {
    local file=$1
    echo -e "${GREEN}🚀 Ejecutando $file con Streamlit...${NC}"
    doppler run -- streamlit run "src/$file"
}

# Función para ejecutar Python scripts
run_python() {
    local file=$1
    echo -e "${GREEN}🚀 Ejecutando $file con Python...${NC}"
    doppler run -- python "src/$file"
}

# Loop principal
while true; do
    show_menu
    read -p "Selecciona una opción [0-13]: " choice
    
    case $choice in
        1) run_streamlit "app.py" ;;
        2) run_streamlit "app_hannah_error_handling.py" ;;
        3) run_streamlit "app_hannah_error_handling_with_axiom.py" ;;
        4) run_streamlit "app_ms_agent.py" ;;
        5) run_python "main.py" ;;
        6) run_python "test_doppler.py" ;;
        7) run_python "test_modal_connection.py" ;;
        8) run_python "test_axiom_connection.py" ;;
        9) run_python "test_hannah_axiom_integration.py" ;;
        10) run_python "hannah_modal_client.py" ;;
        11) run_python "run_hannah_with_axiom.py" ;;
        12) run_python "run_src_with_doppler.py" ;;
        13) run_python "hannah_modal_app.py" ;;
        0) 
            echo -e "${GREEN}👋 ¡Hasta luego!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Opción inválida. Presiona Enter para continuar...${NC}"
            read
            ;;
    esac
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Ejecución completada${NC}"
    else
        echo -e "${RED}❌ Error en la ejecución${NC}"
    fi
    
    echo ""
    echo -e "${YELLOW}Presiona Enter para continuar...${NC}"
    read
done


