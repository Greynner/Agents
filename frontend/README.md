# 🧠 Hannah QA Agent - Frontend

Frontend de Next.js para **Hannah QA Agent**, generador de matrices de prueba y casos Gherkin con IA.

## 🚀 Inicio Rápido

### Instalación

```bash
npm install
```

### Desarrollo

```bash
npm run dev
```

Abre [http://localhost:3000](http://localhost:3000) en tu navegador.

### Build

```bash
npm run build
npm start
```

## ⚙️ Configuración

Configura la variable de entorno `NEXT_PUBLIC_MODAL_ENDPOINT` con la URL del backend de Modal:

```env
NEXT_PUBLIC_MODAL_ENDPOINT=https://tu-usuario--qa-agent-backend-modal.functions.modal.run
```

## 🏗️ Stack Tecnológico

- **Next.js 16** - Framework React
- **TypeScript** - Tipado estático
- **Tailwind CSS 4** - Estilos
- **React 19** - Biblioteca UI

## 📁 Estructura

```
src/
  app/
    layout.tsx    # Layout principal
    page.tsx      # Página principal con formulario
    globals.css   # Estilos globales
```

## 🎯 Características

- ✅ Interfaz limpia y moderna
- ✅ Generación de matrices de prueba
- ✅ Visualización de casos Gherkin
- ✅ Responsive design
- ✅ Manejo de errores
- ✅ Loading states

## 📝 Uso

1. Ingresa un requerimiento QA en el formulario
2. Haz clic en "Enviar a Hannah"
3. Visualiza la matriz de pruebas y casos Gherkin generados
4. Revisa la respuesta completa del backend si es necesario

---

Desarrollado con ❤️ para automatizar QA
