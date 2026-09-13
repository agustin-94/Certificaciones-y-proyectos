# Rescoldo — tu web

![Demo del sitio](ejemplos/rescoldo-demo.gif)

*Nota de portafolio: el README de abajo es la guía de uso real que le
entregué al cliente (ficticio) junto con el proyecto, pensada para que
pueda editar contenido y subir la web sin saber programar — se deja tal
cual porque es también una muestra de cómo documento un entregable para
alguien no técnico.*

---

Guía rápida, sin tecnicismos. Todo lo que necesitás para ver la web, subirla a internet y editarla vos mismo con el Bloc de notas.

## 1. Ver la web en tu computadora

Hacé doble clic en el archivo `index.html`. Se abre en tu navegador (Chrome, Edge, Firefox) y se ve exactamente igual que en internet, con todas las animaciones.

## 2. Subir la web a Hostinger

1. Entrá al panel de Hostinger → **Administrar** → **Administrador de archivos** (File Manager).
2. Andá a la carpeta `public_html` (o la carpeta de tu dominio).
3. Arrastrá **todos** los archivos y carpetas de esta entrega (`index.html`, `styles.css`, `main.js`, `README.md`, la carpeta `lib/`, la carpeta `assets/` si existe, y el archivo `.htaccess`) adentro de esa carpeta.
4. Importante: el archivo `.htaccess` a veces no se ve en tu computadora porque empieza con un punto. Si tu explorador de archivos lo esconde, activá "mostrar archivos ocultos" antes de arrastrar la carpeta entera — así te asegurás de que también se suba.
5. Entrá a tu dominio en el navegador. Listo.

## 3. Editar textos, platos, horarios y teléfono

Todo lo editable está en un solo archivo: **`lib/manifest.js`**. Abrilo con el Bloc de notas (clic derecho → Abrir con → Bloc de notas).

Vas a ver bloques como este:

```
brand: {
  name: "Rescoldo",
  tagline: "Donde el fuego pone la mesa.",
  phone: "0294 452-9091",
  ...
}
```

Reglas para no romper nada:
- Editá **solo lo que está entre comillas** (`"así"`). No toques las comillas, las comas ni las llaves `{ }`.
- Si un texto tiene un `%` o un `\n`, dejalo como está.
- Cuando termines, guardá el archivo (Ctrl+S) y volvé a subirlo a Hostinger reemplazando el que ya estaba.

### Cambiar los platos de la carta

En el mismo archivo, buscá `dishes:`. Cada plato es un bloque con `name`, `subtitle`, `ingredients` y `description`. Podés cambiar el texto de cualquiera de esos campos. Si agregás o sacás un plato, fijate de no dejar una coma de más al final del último elemento.

### Cambiar la programación semanal

Buscá `sessions:` en el mismo archivo. Cuatro bloques, uno por día.

### Cambiar el número de WhatsApp

El WhatsApp aparece en **dos lugares** — tenés que cambiarlo en los dos:
1. En `lib/manifest.js`, el campo `whatsapp` (solo números, con el código de país, sin espacios ni el "+": ej. `5492944529091`).
2. En `index.html`, buscá (Ctrl+F) `wa.me/` — vas a encontrar 3 enlaces que empiezan así. Reemplazá el número en los tres.

## 4. Cambiar o agregar fotos

Todavía no armamos la web con fotos reales — usamos una escena ilustrada (fuego, degradés, texturas) porque en el momento de generar la web no tuvimos acceso a un banco de imágenes. Cuando tengas tus propias fotos:

1. Guardalas en la carpeta `assets/photos/source/` (creala si no existe).
2. Avisame en el chat y las integro al diseño (hero, El Local, Galería) reemplazando las escenas ilustradas por tus fotos reales, ya optimizadas.

Si mientras tanto querés ir armando esa carpeta vos mismo, cualquier `.jpg`, `.png` o `.webp` sirve.

## 5. Si algo no se actualiza después de subir cambios

Los navegadores guardan una copia de la web para que cargue más rápido. A veces, después de subir un cambio, seguís viendo la versión vieja. Solución, en orden:

1. Recargá la página con **Ctrl+F5** (fuerza a bajar todo de nuevo).
2. Si seguís viendo lo viejo, abrí la web en una ventana de incógnito.
3. Si nada de eso funciona, decímelo — es cuestión de "bumpear" un número de versión (`?v=20260711`) que ya está preparado en el `index.html` para estos casos.

## 6. Estructura de archivos (por si te lo preguntan)

```
index.html          → la página
styles.css           → todos los estilos (colores, tipografías, tamaños)
main.js              → toda la interacción (menú, animaciones, formulario)
lib/manifest.js      → EDITABLE — tus datos (nombre, carta, horarios, contacto)
lib/dishes-3d.js     → las piezas 3D de los 4 platos "Casa"
lib/gsap.min.js, lib/ScrollTrigger.min.js, lib/three.min.js → librerías, no tocar
.htaccess            → configuración para que Hostinger no sirva versiones viejas
```

Cualquier duda, escribime por el chat donde armamos la web.
