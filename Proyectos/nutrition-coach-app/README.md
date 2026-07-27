# Coach Nutricional — App con IA (Claude Artifact)

App de coaching nutricional construida como **artifact interactivo de Claude**
(no es un proyecto React independiente con build propio — corre dentro del
entorno de Claude, que expone la API de Claude y almacenamiento persistente
sin necesidad de backend ni API key propia).

## Qué hace

- **Onboarding de perfil**: edad, peso, altura, nivel de actividad, horas de
  sueño, tipo y frecuencia de entrenamiento, objetivos (perder grasa, ganar
  músculo, recomposición, rendimiento, salud general) y restricciones
  alimentarias (alergias, intolerancias, preferencias).
- **Despensa por foto de ticket**: el usuario saca una foto del ticket de
  compra, la app la envía a la API de Claude (modelo con visión) para
  extraer los productos comprados y los suma automáticamente a la despensa.
- **Generación de recetas con IA**: a partir del perfil nutricional del
  usuario y lo que hay en la despensa, Claude genera recetas personalizadas
  respetando restricciones y objetivos.
- **Historial y persistencia**: perfil, despensa e historial de recetas
  cocinadas se guardan de forma persistente entre sesiones.

## Cómo está construido

- **React** (hooks: `useState`, `useReducer`, `useEffect`, `useRef`)
- **lucide-react** para iconografía
- **Tailwind** para estilos
- Ilustraciones propias en SVG para los estados vacíos
- Integración con **Claude (Anthropic API)** para:
  - Lectura de tickets de compra (visión + JSON estructurado)
  - Generación de recetas personalizadas (texto + JSON estructurado)
- Persistencia vía `window.storage` (API de almacenamiento de Claude
  Artifacts — clave/valor, por usuario)

## Cómo verlo / probarlo

Este archivo (`CoachNutricional.jsx`) está pensado para pegarse y ejecutarse
como artifact dentro de Claude (claude.ai), donde `window.storage` y el
acceso a la API de Claude ya están disponibles sin configuración. No corre
"tal cual" con `npm start` en un proyecto React genérico, porque:

1. Depende de `window.storage`, que solo existe en el entorno de artifacts.
2. Llama a `api.anthropic.com` sin key — eso lo maneja Claude por detrás
   dentro del artifact; en un proyecto propio necesitarías tu propia API key
   y probablemente un proxy backend para no exponerla en el cliente.

Para adaptarlo a un proyecto React standalone habría que:
- Reemplazar `window.storage` por `localStorage` o una base de datos propia.
- Mover las llamadas a Claude a un backend propio que guarde la API key de
  forma segura.

## Stack

`React` · `Claude (Anthropic API) — visión + generación de texto` · `lucide-react` · `Tailwind CSS`
