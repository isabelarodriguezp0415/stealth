# BILDO - Landing Page

Landing page profesional para BILDO, plataforma de análisis normativo con IA para el sector inmobiliario.

## 🎨 Colores Corporativos

- **Primary (Azul Oscuro)**: `#16232A`
- **Accent (Naranja)**: `#FF5804`
- **Secondary (Verde Azulado)**: `#075056`

## 🚀 Características

- ✅ Diseño moderno y profesional orientado a B2B
- ✅ Responsive (móvil, tablet, desktop)
- ✅ Componentes React modulares
- ✅ Tailwind CSS para estilos
- ✅ Iconos con Lucide React
- ✅ Animaciones y transiciones suaves
- ✅ Formulario de contacto funcional
- ✅ Secciones optimizadas para conversión

## 📦 Estructura del Proyecto

```
bildo-landing/
├── src/
│   ├── components/
│   │   ├── Navbar.jsx          # Navegación sticky
│   │   ├── Hero.jsx             # Sección hero con CTA
│   │   ├── Problem.jsx          # Problema del mercado
│   │   ├── Solution.jsx         # Solución BILDO
│   │   ├── Features.jsx         # Características (8 features)
│   │   ├── HowItWorks.jsx       # Proceso en 4 pasos
│   │   ├── Benefits.jsx         # Beneficios cuantificables
│   │   ├── CTA.jsx              # Formulario de contacto
│   │   └── Footer.jsx           # Footer con links
│   ├── App.jsx                  # Componente principal
│   ├── main.jsx                 # Punto de entrada
│   └── index.css                # Estilos globales
├── index.html
├── package.json
├── tailwind.config.js
├── postcss.config.js
└── vite.config.js
```

## 🛠️ Instalación y Uso Local

### Prerrequisitos
- Node.js 16+ y npm/yarn instalado

### Pasos

1. **Instalar dependencias**
```bash
cd bildo-landing
npm install
```

2. **Ejecutar en modo desarrollo**
```bash
npm run dev
```

3. **Construir para producción**
```bash
npm run build
```

4. **Previsualizar build de producción**
```bash
npm run preview
```

## 📱 Secciones de la Landing

1. **Hero** - Propuesta de valor principal con CTA destacado
2. **Problem** - 4 problemas del mercado inmobiliario actual
3. **Solution** - Cómo BILDO resuelve estos problemas con IA
4. **Features** - 8 características principales de la plataforma
5. **How It Works** - Proceso en 4 pasos simples
6. **Benefits** - Beneficios cuantificables con métricas
7. **CTA** - Formulario de contacto para solicitar demo
8. **Footer** - Links y redes sociales

## 🎯 Uso en Lovable

### Opción 1: Importar proyecto completo

1. Comprime toda la carpeta `bildo-landing` en un ZIP
2. En Lovable, selecciona "Import Project"
3. Sube el archivo ZIP
4. Lovable detectará automáticamente la configuración

### Opción 2: Prompt para Lovable

Usa este prompt en Lovable:

```
Crea una landing page para BILDO, una plataforma de análisis normativo
inmobiliario con IA.

COLORES:
- Primary: #16232A (azul oscuro)
- Accent: #FF5804 (naranja)
- Secondary: #075056 (verde azulado)

SECCIONES:
1. Hero con CTA destacado
2. Problema del mercado (4 puntos)
3. Solución con IA
4. 8 características principales
5. Cómo funciona (4 pasos)
6. Beneficios cuantificables
7. Formulario de contacto
8. Footer

TECNOLOGÍAS:
- React + Vite
- Tailwind CSS
- Lucide React icons
- Diseño responsive y moderno
- Orientado a constructoras y corporativos B2B
```

### Opción 3: Copiar componentes individualmente

Puedes copiar el contenido de cada archivo `.jsx` y `.css` directamente en Lovable
usando su editor de código.

## 🎨 Personalización

### Cambiar colores

Edita `tailwind.config.js`:

```javascript
colors: {
  primary: {
    DEFAULT: '#16232A',  // Cambia aquí
    // ...
  },
  accent: {
    DEFAULT: '#FF5804',  // Cambia aquí
    // ...
  },
  // ...
}
```

### Modificar contenido

Cada componente en `src/components/` contiene su propio contenido.
Edita directamente los textos, métricas y descripciones según necesites.

### Agregar nuevas secciones

1. Crea un nuevo componente en `src/components/`
2. Impórtalo en `src/App.jsx`
3. Agrégalo en el orden deseado

## 📝 Checklist para Producción

- [ ] Actualizar meta tags en `index.html`
- [ ] Agregar Google Analytics
- [ ] Configurar dominio personalizado
- [ ] Integrar formulario con backend/CRM
- [ ] Optimizar imágenes (si agregas)
- [ ] Configurar redirecciones
- [ ] Implementar SEO completo
- [ ] Agregar favicon personalizado

## 🚀 Deploy

### Vercel (Recomendado)

```bash
npm install -g vercel
vercel
```

### Netlify

```bash
npm run build
# Arrastra la carpeta dist/ a Netlify
```

## 📧 Integración del Formulario

El formulario en `CTA.jsx` actualmente solo muestra los datos en consola.
Para integrarlo con un backend:

1. **Con EmailJS**: Agrega EmailJS y configura el servicio
2. **Con API propia**: Modifica la función `handleSubmit` para hacer POST a tu API
3. **Con Zapier/Make**: Usa webhook para conectar con CRM

## 🤝 Público Objetivo

- Constructoras
- Desarrolladores inmobiliarios
- Inversionistas institucionales
- Arquitectos
- Corporativos del sector inmobiliario

## 📄 Licencia

Propietario - BILDO 2025

---

Desarrollado para BILDO - Transformando normativa en oportunidades con IA 🚀
