/* ==========================================================================
   Rescoldo — datos editables de la marca
   Cocina de fuego patagónica · Bariloche

   EDITAR AQUÍ (con el Bloc de notas):
   - Nombre, dirección, teléfono, WhatsApp, Instagram, horario → objeto "brand"
   - Los 10 platos de la carta → array "dishes"
   - La programación semanal → array "sessions"
   - Los textos de la galería → array "gallery"

   No tocar nada fuera de comillas. No borrar comas. Si algo se rompe,
   volvé a bajar una copia de este archivo antes de editar.
   ========================================================================== */
(function () {
  "use strict";

  window.__RESCOLDO__ = {

    brand: {
      name: "Rescoldo",
      tagline: "Donde el fuego pone la mesa.",
      kicker: "Cocina de fuego patagónica",
      typeLine: "Restaurante de fuego · Circuito Chico / Bariloche",
      location: "Circuito Chico · Bariloche",
      address: "Av. Bustillo, Km 11,500 · Circuito Chico · San Carlos de Bariloche, Río Negro",
      phone: "0294 452-9091",
      phoneHref: "tel:+542944529091",
      whatsapp: "5492944529091",
      instagramHandle: "@rescoldo.bariloche",
      instagramUrl: "https://instagram.com/rescoldo.bariloche",
      hours: "Martes a domingo, 19:30 → 01:00",
      hoursShort: "MAR → DOM · 19:30 → 01:00",
      closedNote: "Cerrado los lunes",
      capacity: 60,
      established: "2019",
      establishedTag: "EST · 2019 · BRC",
      mapEmbed: "https://www.google.com/maps?q=Av.+Bustillo+Km+11.5,+Circuito+Chico,+San+Carlos+de+Bariloche&output=embed",
      year: 2026
    },

    /* Los 10 platos — 4 "Casa" (insignia, con pieza 3D) + 6 "Temporada" (line-art) */
    dishes: [
      {
        id: "rescoldo",
        name: "Rescoldo",
        series: "casa",
        vessel: "asador_cruz",
        vesselLabel: "Asador de cruz",
        subtitle: "El plato de la casa",
        ingredients: ["Cordero patagónico", "Hierbas de la estepa", "Brasa de lenga"],
        description: "Seis horas de fuego lento sobre brasa de lenga. El plato que le da nombre a la casa.",
        liquidColor: "#7a2a1c",
        accent: "#E8592A"
      },
      {
        id: "glaciar",
        name: "Glaciar",
        series: "casa",
        vessel: "plancha",
        vesselLabel: "Plancha",
        subtitle: "Trucha de lago a la plancha",
        ingredients: ["Trucha del Nahuel Huapi", "Manteca de hierbas", "Limón"],
        description: "Piel crujiente, manteca dorada. El frío del lago servido caliente.",
        liquidColor: "#d9a441",
        accent: "#3DE2C9"
      },
      {
        id: "humo",
        name: "Humo",
        series: "casa",
        vessel: "parrilla",
        vesselLabel: "Parrilla",
        subtitle: "Bondiola ahumada de la casa",
        ingredients: ["Bondiola ahumada 12 h", "Puré de manzana verde", "Reducción de calafate"],
        description: "Ahumado dulce, ácido de calafate. La brasa que se siente en la cara.",
        liquidColor: "#4a1f3a",
        accent: "#E8592A"
      },
      {
        id: "musgo",
        name: "Musgo",
        series: "casa",
        vessel: "cazuela",
        vesselLabel: "Cazuela",
        subtitle: "Risotto de hongos de bosque",
        ingredients: ["Hongos de bosque", "Manteca de trufa negra patagónica"],
        description: "Bosque húmedo en un plato. Cremoso, terroso, para los que llegan tarde a cenar.",
        liquidColor: "#3a4a2a",
        accent: "#C9A35B"
      },
      {
        id: "ceniza",
        name: "Ceniza",
        series: "temporada",
        vessel: "fuente_horno",
        vesselLabel: "Fuente de horno",
        subtitle: "Jabalí estofado de la casa",
        ingredients: ["Jabalí de bosque", "Vino tinto de altura", "Papines andinos"],
        description: "Barro caliente, vino oscuro, humo dulce. Estofado de seis horas.",
        liquidColor: "#5a1f2e",
        accent: "#C9A35B"
      },
      {
        id: "sereno",
        name: "Sereno",
        series: "temporada",
        vessel: "tabla",
        vesselLabel: "Tabla",
        subtitle: "Tabla de ahumados",
        ingredients: ["Trucha ahumada", "Ciervo ahumado", "Quesos de la zona"],
        description: "Para picar despacio, con vino, mientras el lago se pone oscuro.",
        liquidColor: "#8a5a3a",
        accent: "#E8592A"
      },
      {
        id: "aurora",
        name: "Aurora",
        series: "temporada",
        vessel: "copa_postre",
        vesselLabel: "Copa de postre",
        subtitle: "Copa de chocolate patagónico",
        ingredients: ["Chocolate amargo", "Frutos rojos", "Nieve de menta"],
        description: "Chocolate de la casa, frío por fuera, tibio por dentro. Sube rápido, baja despacio.",
        liquidColor: "#2a160a",
        accent: "#C9A35B"
      },
      {
        id: "ultima-brasa",
        name: "Última Brasa",
        series: "temporada",
        vessel: "fondue_olla",
        vesselLabel: "Olla de fondue",
        subtitle: "Fondue de quesos de altura",
        ingredients: ["Quesos de altura", "Pan de campo", "Papines"],
        description: "Para los que se quedan hasta el cierre. Queso fundido, mesa compartida.",
        liquidColor: "#e0b955",
        accent: "#C9A35B"
      },
      {
        id: "veneno-verde",
        name: "Veneno Verde",
        series: "temporada",
        vessel: "plato_hondo",
        vesselLabel: "Plato hondo",
        subtitle: "Ceviche patagónico de trucha",
        ingredients: ["Trucha", "Leche de tigre con ají de la estepa", "Cardamomo"],
        description: "Trucha cruda, cítrico y un golpe de ají verde. Suave en boca, largo en cabeza.",
        liquidColor: "#d8c272",
        accent: "#3DE2C9"
      },
      {
        id: "vertigo",
        name: "Vértigo",
        series: "temporada",
        vessel: "fuente_grande",
        vesselLabel: "Fuente grande",
        subtitle: "Costillar al asador",
        ingredients: ["Costillar de cerdo 14 h", "Salsa de ruibarbo y whisky"],
        description: "El plato que se pide cuando ya hay confianza. Dulce, ahumado, para compartir.",
        liquidColor: "#a8341a",
        accent: "#E8592A"
      }
    ],

    /* Programación semanal — La Semana (03) */
    sessions: [
      {
        day: "Jueves",
        title: "Asado al Asador de Cruz",
        note: "Cordero entero. Reserva con 24 horas.",
        icon: "asador_cruz",
        accent: "#E8592A"
      },
      {
        day: "Viernes",
        title: "Música en Vivo: Folk & Blues",
        note: "Guitarra y fuego bajo, mesa larga.",
        icon: "guitarra",
        accent: "#3DE2C9"
      },
      {
        day: "Sábado",
        title: "Noche de Ahumados",
        note: "Tabla de la casa, vino de altura.",
        icon: "humo",
        accent: "#E8592A"
      },
      {
        day: "Domingo",
        title: "Noche de Fondue",
        note: "Queso fundido, cierre de semana.",
        icon: "fondue_olla",
        accent: "#C9A35B"
      }
    ],

    /* Galería / atmósfera — 04. Sin fotos propias todavía: se muestran
       como texturas ilustradas. Cuando el cliente suba fotos reales a
       assets/photos/source/, se reemplazan por <img> (ver README). */
    gallery: [
      { label: "Fuego", tone: "ember" },
      { label: "Humo de lenga", tone: "smoke" },
      { label: "Cordero al asador", tone: "ember" },
      { label: "Trucha de lago", tone: "teal" },
      { label: "Hongos de bosque", tone: "moss" },
      { label: "Lago al atardecer", tone: "teal" },
      { label: "Montaña", tone: "night" },
      { label: "Madera de lenga", tone: "wood" },
      { label: "Velas", tone: "gold" },
      { label: "Vino de altura", tone: "wine" },
      { label: "Nieve", tone: "teal" },
      { label: "Chocolate patagónico", tone: "cocoa" },
      { label: "Brasas", tone: "ember" },
      { label: "Copas junto al fuego", tone: "gold" },
      { label: "Mesa de madera", tone: "wood" },
      { label: "Cielo estrellado", tone: "night" }
    ]
  };

  /* Alias genérico por compatibilidad con herramientas que esperan __BRAND__ */
  window.__BRAND__ = window.__RESCOLDO__;
})();
