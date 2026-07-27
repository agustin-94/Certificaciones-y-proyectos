# Auditoría SEO — Hertz Argentina (proyecto propio / demo)

Auditoría de SEO independiente sobre `hertz.com.ar`, hecha como ejercicio
propio de análisis (**no fue un trabajo encargado por Hertz ni por ningún
cliente** — es una pieza de portafolio para mostrar capacidad de análisis
SEO on-page, técnico y competitivo sobre un caso real y público).

Presentada como un informe HTML autocontenido, navegable, con modo oscuro.

## Qué incluye

- **Puntuación por área** (on-page, técnico, contenido, arquitectura)
- **Auditoría de home + 4 landings de producto**: title, meta description,
  canonical, encabezados, hallazgos por severidad (rojo/amarillo/verde)
- **Rastreo e indexación**: revisión de `robots.txt`, sitemap
- **Diagnóstico arquitectónico de front-end**
- **Profundidad editorial y silo temático del blog**
- **Comparativa competitiva**: Hertz vs. Avis, Europcar y Sixt Argentina
- **10 keywords long-tail validadas con SERP real**
- **25 acciones priorizadas** por impacto y esfuerzo
- **Metodología**: sección final que documenta cómo se relevaron los datos
  (vía fetch web, con verificación cruzada entre pasadas y marcado explícito
  de datos no verificables cuando hubo inconsistencia)

## Cómo verlo

Es un único archivo HTML autocontenido — se abre directo en el navegador,
sin dependencias ni servidor. Incluye:
- Navegación lateral con scroll-spy
- Toggle de modo oscuro/claro
- Barra de progreso de lectura
- Exportación a PDF desde el propio informe

## Nota de transparencia

Este análisis se hizo con datos públicos accesibles en el sitio de Hertz
Argentina y de sus competidores directos, con fines de demostración de
habilidades de auditoría SEO. Los hallazgos y recomendaciones no fueron
solicitados ni validados por Hertz.

## Stack

`HTML` · `CSS` (variables CSS para temas claro/oscuro) · `JavaScript` (scroll-spy, filtros, exportación PDF)
