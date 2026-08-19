# Coach Nutricional 🥗

App que arma tu despensa a partir de una foto de tu ticket de compra (o carga manual) y genera recetas personalizadas según tu perfil, objetivos e ingredientes disponibles — usando IA generativa (Google Gemini) para leer el ticket y crear las recetas.

Existe en dos formas a partir del mismo código: una **PWA web** y una **app Android nativa** con todo el código empaquetado dentro del APK.

**Demo web:** https://agustin-94.github.io/coach-nutricional/ *(reemplazar si el link real es distinto)*
**APK para Android:** archivo `coach-nutricional.apk` en esta misma carpeta

> 🤖 **Integración con IA:** usa la API de **Google Gemini** (capa gratuita) para (1) leer una foto de ticket de supermercado y extraer productos, cantidades y categorías, y (2) generar recetas a medida combinando el perfil nutricional del usuario con los ingredientes reales de su despensa. La respuesta se fuerza a JSON estricto (`responseMimeType: application/json`) para que sea siempre parseable.

## Capturas

*(agregar screenshots del onboarding, despensa y recetas aquí)*

## Funcionalidades

- **Onboarding** de perfil: edad, peso, altura, actividad, objetivos, alergias.
- **Carga de despensa** de dos formas: foto de ticket (IA) o carga manual (nombre, cantidad, unidad, categoría).
- **Generación de recetas** con IA según perfil + despensa, con macros, tiempo, dificultad e ingredientes faltantes.
- **Historial** de tickets y recetas cocinadas.
- **Ajustes**: la API key de Gemini se guarda solo en el dispositivo, nunca se comparte.

## Arquitectura

### Versión web (`index.html`)
- **React 18 sin build step**: el JSX se transforma en el propio navegador con **Babel Standalone**; React, ReactDOM e íconos (`lucide-react`) se cargan como scripts UMD desde `unpkg`. Un solo archivo, sin Node ni bundler.
- Persistencia en `localStorage` del navegador.
- Publicada en **GitHub Pages**.

### Versión Android nativa (`/android`)
Evolucionó de "WebView apuntando a la URL de GitHub Pages" a **una app totalmente autocontenida**:

- `MainActivity.kt`: un `WebView` que sirve los archivos empaquetados dentro del propio APK usando **`WebViewAssetLoader`** (`androidx.webkit`), que expone `app/src/main/assets/` bajo el origen virtual `https://appassets.androidplatform.net/`. Esto evita los problemas de `file://` (cámara, `localStorage`) sin depender de ningún servidor externo.
- `android/assets/index.html`: la misma app, pero con las librerías (React, ReactDOM, lucide-react, Babel Standalone, Tailwind) **descargadas y empaquetadas localmente** en `assets/vendor/` en vez de cargarse desde `unpkg.com` — la app funciona igual aunque el repositorio, GitHub Pages o el CDN estén caídos. Lo único que sigue requiriendo internet es la llamada a la API de Gemini (inherente a cualquier feature de IA).
- Selector de archivos nativo (`onShowFileChooser` + `FileProvider`) para elegir entre cámara o galería al cargar un ticket.
- Manejo del botón "Atrás" con `OnBackPressedCallback` (API moderna, no deprecada).

```
android/
  MainActivity.kt
  AndroidManifest.xml
  assets/
    index.html         ← versión offline (referencia vendor/ local)
    manifest.json
    sw.js
    icon-192.png
    icon-512.png
    vendor/            ← no incluido en el repo por tamaño, ver abajo
```

> `assets/vendor/` no se subió al repositorio para no inflarlo con librerías de terceros. Son builds UMD estándar, descargables desde:
> [react.production.min.js](https://unpkg.com/react@18/umd/react.production.min.js) · [react-dom.production.min.js](https://unpkg.com/react-dom@18/umd/react-dom.production.min.js) · [lucide-react.min.js](https://unpkg.com/lucide-react@0.436.0/dist/umd/lucide-react.min.js) · [babel.min.js](https://unpkg.com/@babel/standalone@7.24.7/babel.min.js) · [tailwind.js](https://cdn.tailwindcss.com)

## Stack

`React 18` · `Tailwind CSS` · `Babel Standalone` · `lucide-react` · `Google Gemini API` · `Kotlin` · `Android WebView + WebViewAssetLoader` · `GitHub Pages`

## Cómo correrla vos mismo

**Web:** abrí el link de demo, andá a **Ajustes** y pegá tu propia API key de Gemini (gratis, sin tarjeta) desde [aistudio.google.com/apikey](https://aistudio.google.com/apikey). Completá el onboarding y ya podés usarla.

**Android:** instalá el `.apk` (activando "orígenes desconocidos" la primera vez), o compilá el proyecto vos mismo desde `/android` en Android Studio.
