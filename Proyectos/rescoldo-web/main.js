(function () {
  // Rescoldo — main.js — IIFE clásico, sin imports/exports.
  // Usa window.__RESCOLDO__ (definido en lib/manifest.js).
  "use strict";

  var data = window.__RESCOLDO__ || {};
  var reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fineHover = matchMedia("(hover: hover) and (pointer: fine)").matches;

  var $ = function (sel, scope) { return (scope || document).querySelector(sel); };
  var $$ = function (sel, scope) { return Array.prototype.slice.call((scope || document).querySelectorAll(sel)); };
  var escHTML = function (s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  };
  function safe(fn, name) { try { fn(); } catch (e) { console.warn("[" + name + "]", e); } }

  /* ------------------------------------------------------------------
     Vessel line-art (SVG poligonal) — un dibujo distinto por vajilla
     ------------------------------------------------------------------ */
  var VESSEL_SVG = {
    asador_cruz: {
      outline: "M100,8 L100,132 M38,45 L162,45 M100,55 L131,80 L100,105 L69,80 Z",
      fill: "M100,59 L127,80 L100,101 L73,80 Z"
    },
    plancha: {
      outline: "M18,112 L58,38 L182,38 L142,112 Z M80,75 L110,60 L142,75 L142,90 L110,106 L80,90 Z",
      fill: "M83,76 L110,64 L137,76 L137,88 L110,101 L83,88 Z"
    },
    parrilla: {
      outline: "M18,50 L182,50 M18,65 L182,65 M18,80 L182,80 M18,95 L182,95 M18,110 L182,110 M58,38 L142,38 L142,74 L58,74 Z",
      fill: "M62,42 L138,42 L138,70 L62,70 Z"
    },
    cazuela: {
      outline: "M38,50 L162,50 L146,112 L54,112 Z M38,55 L18,66 L38,77 Z M162,55 L182,66 L162,77 Z",
      fill: "M50,56 L150,56 L137,104 L63,104 Z"
    },
    fuente_horno: {
      outline: "M28,44 L172,44 L172,106 L28,106 Z",
      fill: "M40,55 L160,55 L160,96 L40,96 Z"
    },
    tabla: {
      outline: "M14,72 L60,38 L186,38 L140,102 L14,102 Z",
      fill: "M58,58 L75,52 L81,66 L64,72 Z M98,64 L118,58 L123,74 L104,80 Z M138,55 L156,52 L160,66 L144,71 Z"
    },
    copa_postre: {
      outline: "M58,38 L142,38 L110,76 L90,76 Z M100,76 L100,108 M74,120 L126,120",
      fill: "M66,44 L134,44 L107,72 L93,72 Z"
    },
    fondue_olla: {
      outline: "M53,46 L147,46 L136,88 L64,88 Z M70,88 L54,118 M130,88 L146,118 M100,88 L100,118 M38,24 L162,56 M162,24 L38,56",
      fill: "M60,50 L140,50 L131,82 L69,82 Z"
    },
    plato_hondo: {
      outline: "M26,54 L174,54 L152,102 L48,102 Z M68,102 L132,102 L122,112 L78,112 Z",
      fill: "M42,58 L158,58 L140,96 L60,96 Z"
    },
    fuente_grande: {
      outline: "M38,70 L60,44 L140,44 L162,70 L140,96 L60,96 Z",
      fill: "M53,68 L67,51 L133,51 L147,68 L133,89 L67,89 Z"
    }
  };

  function vesselSVG(kind, liquidColor, accent) {
    var v = VESSEL_SVG[kind] || VESSEL_SVG.plato_hondo;
    return (
      '<svg class="dish-svg" viewBox="0 0 200 140" aria-hidden="true">' +
      '<path class="outline" d="' + v.outline + '" stroke="' + escHTML(accent) + '"></path>' +
      '<path class="fill" d="' + v.fill + '" fill="' + escHTML(liquidColor) + '"></path>' +
      "</svg>"
    );
  }

  /* Iconos simples para La Semana */
  var WEEK_ICONS = {
    asador_cruz: '<svg viewBox="0 0 24 24"><path d="M12 2v20M5 7h14M9 9l3 3-3 3M15 9l-3 3 3 3" stroke="currentColor" stroke-width="1.6" fill="none"/></svg>',
    guitarra: '<svg viewBox="0 0 24 24"><path d="M9 21c-2 0-3-1.4-3-3.4 0-2.6 2.4-3.6 2.4-6.4C8.4 8.6 7 7.6 7 5.6 7 3.8 8.6 2.4 10.6 2.4c2.4 0 4 1.8 4 4 0 2.4-1.8 3-1.8 5.6 0 2 1.6 3 3.2 4.6" stroke="currentColor" stroke-width="1.5" fill="none"/><circle cx="9.4" cy="17.6" r="2.3" stroke="currentColor" stroke-width="1.4" fill="none"/></svg>',
    humo: '<svg viewBox="0 0 24 24"><path d="M8 21c2-2 0-3 2-5s0-3 2-5-1-4 1-6" stroke="currentColor" stroke-width="1.6" fill="none" stroke-linecap="round"/></svg>',
    fondue_olla: '<svg viewBox="0 0 24 24"><path d="M4 10h16l-2 8H6L4 10ZM2 6l3 4M22 6l-3 4M9 6l3-3 3 3" stroke="currentColor" stroke-width="1.5" fill="none"/></svg>'
  };

  /* ------------------------------------------------------------------
     Mounts idempotentes
     ------------------------------------------------------------------ */
  function mountDishes() {
    var target = $("[data-dishes]");
    if (!target || target.children.length > 0 || !data.dishes) return;
    target.innerHTML = data.dishes.map(function (d, i) {
      var isCasa = d.series === "casa";
      var num = String(i + 1).padStart(2, "0");
      return (
        '<article class="dish-card series-' + d.series + '" data-dish-card data-index="' + i + '">' +
        '<span class="tag">' + (isCasa ? "Casa" : "Temporada") + " · " + num + "/10</span>" +
        '<div class="dish-visual">' +
        (isCasa
          ? '<div class="dish-3d" data-dish-3d="' + d.vessel + '" data-dish-color="' + d.liquidColor + '" data-dish-accent="' + d.accent + '"></div>'
          : "") +
        vesselSVG(d.vessel, d.liquidColor, d.accent) +
        "</div>" +
        '<p class="dish-vessel">' + escHTML(d.vesselLabel) + "</p>" +
        '<h3 class="dish-name">' + escHTML(d.name) + "</h3>" +
        '<p class="dish-subtitle">' + escHTML(d.subtitle) + "</p>" +
        '<div class="dish-ingredients">' +
        d.ingredients.map(function (ing) { return "<span>" + escHTML(ing) + "</span>"; }).join("") +
        "</div>" +
        '<p class="dish-desc">' + escHTML(d.description) + "</p>" +
        "</article>"
      );
    }).join("");
  }

  function mountSessions() {
    var target = $("[data-sessions]");
    if (!target || target.children.length > 0 || !data.sessions) return;
    target.innerHTML = data.sessions.map(function (s) {
      return (
        '<div class="week-row" style="--row-accent:' + s.accent + '">' +
        '<span class="week-icon" style="color:' + s.accent + '; border-color:' + s.accent + '55">' +
        (WEEK_ICONS[s.icon] || "") +
        "</span>" +
        '<div><p class="week-day">' + escHTML(s.day) + '</p><p class="week-title">' + escHTML(s.title) + "</p></div>" +
        '<p class="week-note">' + escHTML(s.note) + "</p>" +
        "</div>"
      );
    }).join("");
  }

  function mountGallery() {
    var lanes = [$("[data-gallery-lane='1']"), $("[data-gallery-lane='2']"), $("[data-gallery-lane='3']")];
    if (!lanes[0] || lanes[0].children.length > 0 || !data.gallery) return;
    var items = data.gallery;
    var thirds = [[], [], []];
    items.forEach(function (item, i) { thirds[i % 3].push(item); });
    thirds.forEach(function (group, li) {
      var lane = lanes[li];
      if (!lane) return;
      lane.innerHTML = group.map(function (g) {
        return '<div class="gallery-tile" data-tone="' + g.tone + '"><span>' + escHTML(g.label) + "</span></div>";
      }).join("");
    });
  }

  /* ------------------------------------------------------------------
     Splash
     ------------------------------------------------------------------ */
  function initSplash() {
    var splash = $("[data-splash]");
    if (!splash) return;
    var hide = function () { splash.classList.add("is-out"); };
    if (document.readyState === "complete") setTimeout(hide, 900);
    else window.addEventListener("load", function () { setTimeout(hide, 700); });
    setTimeout(hide, 4000);
  }

  /* ------------------------------------------------------------------
     Ember particles (hero) — decorativo, pocas partículas
     ------------------------------------------------------------------ */
  function initEmbers() {
    var wrap = $("[data-embers]");
    if (!wrap) return;
    var COUNT = 14;
    for (var i = 0; i < COUNT; i++) {
      var s = document.createElement("span");
      s.className = "ember-spark";
      s.style.left = (Math.random() * 100) + "%";
      s.style.animationDuration = (7 + Math.random() * 6) + "s";
      s.style.animationDelay = (Math.random() * 8) + "s";
      wrap.appendChild(s);
    }
  }

  /* ------------------------------------------------------------------
     Cursor
     ------------------------------------------------------------------ */
  function initCursor() {
    var root = $("[data-cursor-root]");
    if (!root || !fineHover) return;
    document.documentElement.classList.add("has-cursor");
    var dot = $(".cursor-dot", root);
    var ring = $(".cursor-ring", root);
    var label = $(".cursor-label", root);
    var firstMove = false;
    var mx = 0, my = 0, rx = 0, ry = 0;

    window.addEventListener("mousemove", function (e) {
      mx = e.clientX; my = e.clientY;
      dot.style.transform = "translate3d(" + mx + "px," + my + "px,0)";
      if (!firstMove) {
        firstMove = true;
        rx = mx; ry = my;
        ring.style.transform = "translate3d(" + rx + "px," + ry + "px,0)";
        root.classList.add("is-ready");
      }
    });

    function loop() {
      rx += (mx - rx) * 0.18;
      ry += (my - ry) * 0.18;
      ring.style.transform = "translate3d(" + rx + "px," + ry + "px,0)";
      requestAnimationFrame(loop);
    }
    requestAnimationFrame(loop);

    $$("[data-cursor-text]").forEach(function (el) {
      el.addEventListener("mouseover", function (e) {
        if (!el.contains(e.relatedTarget)) {
          root.classList.add("is-interactive");
          label.textContent = el.getAttribute("data-cursor-text") || "";
        }
      });
      el.addEventListener("mouseout", function (e) {
        if (!el.contains(e.relatedTarget)) { root.classList.remove("is-interactive"); }
      });
    });
  }

  /* ------------------------------------------------------------------
     Nav
     ------------------------------------------------------------------ */
  function initNav() {
    var nav = $(".nav");
    if (nav) {
      var onScroll = function () { nav.classList.toggle("is-scrolled", scrollY > 60); };
      onScroll();
      window.addEventListener("scroll", onScroll, { passive: true });
    }
    var burger = $("[data-burger]");
    var mobile = $("[data-nav-mobile]");
    if (!burger || !mobile) return;
    burger.addEventListener("click", function () {
      var open = burger.getAttribute("aria-expanded") === "true";
      burger.setAttribute("aria-expanded", String(!open));
      mobile.setAttribute("aria-hidden", String(open));
      document.body.style.overflow = open ? "" : "hidden";
    });
    $$("a", mobile).forEach(function (a) {
      a.addEventListener("click", function () {
        burger.setAttribute("aria-expanded", "false");
        mobile.setAttribute("aria-hidden", "true");
        document.body.style.overflow = "";
      });
    });
  }

  /* ------------------------------------------------------------------
     Smooth anchor scroll (native)
     ------------------------------------------------------------------ */
  function initSmoothScroll() {
    document.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest('a[href^="#"]');
      if (!a) return;
      var id = a.getAttribute("href");
      if (!id || id === "#") return;
      var el = document.querySelector(id);
      if (!el) return;
      e.preventDefault();
      var navOffset = 76;
      window.scrollTo({
        top: el.getBoundingClientRect().top + scrollY - navOffset,
        behavior: reduced ? "auto" : "smooth"
      });
    });
  }

  /* ------------------------------------------------------------------
     Reveals — ScrollTrigger si está, si no IntersectionObserver plano
     ------------------------------------------------------------------ */
  function initReveals() {
    var els = $$(".reveal");
    if (!els.length) return;

    if (window.gsap && window.ScrollTrigger) {
      els.forEach(function (el) {
        ScrollTrigger.create({
          trigger: el, start: "top 88%", once: true,
          onEnter: function () { el.classList.add("is-visible"); }
        });
      });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { e.target.classList.add("is-visible"); io.unobserve(e.target); }
        });
      }, { threshold: 0.01, rootMargin: "0px 0px -2% 0px" });
      els.forEach(function (el) { io.observe(el); });
    }

    setTimeout(function () {
      els.forEach(function (el) {
        if (!el.classList.contains("is-visible") && el.getBoundingClientRect().top < window.innerHeight) {
          el.classList.add("is-visible");
        }
      });
    }, 6000);
  }

  /* ------------------------------------------------------------------
     Tilt 3D subtle en cards
     ------------------------------------------------------------------ */
  function initTilt() {
    if (!fineHover) return;
    $$(".local-photo, .events-card, .week-row").forEach(function (card) {
      var MAX = 6;
      var tx = 0, ty = 0, cx = 0, cy = 0, raf = null;
      card.classList.add("has-tilt");
      card.addEventListener("mousemove", function (e) {
        var r = card.getBoundingClientRect();
        var px = (e.clientX - r.left) / r.width - 0.5;
        var py = (e.clientY - r.top) / r.height - 0.5;
        tx = -py * MAX; ty = px * MAX;
        if (!raf) raf = requestAnimationFrame(loop);
      });
      card.addEventListener("mouseleave", function () {
        tx = 0; ty = 0; if (!raf) raf = requestAnimationFrame(loop);
      });
      function loop() {
        cx += (tx - cx) * 0.15; cy += (ty - cy) * 0.15;
        card.style.setProperty("--rx", cx.toFixed(2) + "deg");
        card.style.setProperty("--ry", cy.toFixed(2) + "deg");
        raf = (Math.abs(tx - cx) > 0.05 || Math.abs(ty - cy) > 0.05) ? requestAnimationFrame(loop) : null;
      }
    });
  }

  /* ------------------------------------------------------------------
     Marquees — clona contenido y anima con CSS keyframes (robusto sin GSAP)
     ------------------------------------------------------------------ */
  function initMarquees() {
    $$("[data-marquee]").forEach(function (track) {
      if (track.dataset.marqueeBound) return;
      track.dataset.marqueeBound = "1";
      var clone = track.cloneNode(true);
      clone.removeAttribute("data-marquee");
      clone.setAttribute("aria-hidden", "true");
      track.parentNode.appendChild(clone);
      var speed = parseFloat(track.getAttribute("data-speed")) || 60;
      var dir = track.getAttribute("data-dir") === "right" ? "right" : "left";
      var widthPx = track.scrollWidth;
      var duration = Math.max(8, widthPx / speed);
      [track, clone].forEach(function (t) {
        t.style.animationDuration = duration + "s";
        t.classList.add("dir-" + dir);
      });
    });
  }

  /* ------------------------------------------------------------------
     Fuego — showcase pinned horizontal + draw-on SVG + progreso
     ------------------------------------------------------------------ */
  function initDishDraw() {
    $$(".dish-card").forEach(function (card) {
      var outline = $(".outline", card);
      if (outline && outline.getTotalLength) {
        safe(function () {
          var len = outline.getTotalLength();
          outline.style.strokeDasharray = len;
          outline.style.strokeDashoffset = len;
        }, "dishDrawSetup");
      }
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var card = e.target;
        card.classList.add("is-drawn");
        var outline = $(".outline", card);
        if (outline) outline.style.strokeDashoffset = 0;
      });
    }, { threshold: 0.15 });
    $$(".dish-card").forEach(function (card) { io.observe(card); });

    setTimeout(function () {
      $$(".dish-card:not(.is-drawn)").forEach(function (card) {
        if (card.getBoundingClientRect().top < window.innerHeight) {
          card.classList.add("is-drawn");
          var outline = $(".outline", card);
          if (outline) outline.style.strokeDashoffset = 0;
        }
      });
    }, 6000);
  }

  function initShowcaseProgress() {
    var label = $("[data-showcase-progress]");
    var cards = $$(".dish-card");
    if (!label || !cards.length) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting && e.intersectionRatio > 0.5) {
          var idx = parseInt(e.target.getAttribute("data-index"), 10) || 0;
          label.querySelector("strong").textContent = String(idx + 1).padStart(2, "0");
        }
      });
    }, { threshold: [0.5] });
    cards.forEach(function (c) { io.observe(c); });
  }

  function initShowcasePinned() {
    if (!window.gsap || !window.ScrollTrigger) return;
    var sec = $(".showcase");
    var wrap = $("[data-showcase-wrap]");
    var track = $("[data-showcase]");
    if (!sec || !wrap || !track) return;

    var setup = function () {
      ScrollTrigger.getAll().forEach(function (s) { if (s.vars.id === "showcase-pin") s.kill(); });
      gsap.set(track, { x: 0 });
      var isDesktop = window.innerWidth >= 1024;
      sec.classList.toggle("is-pinned", isDesktop);
      if (!isDesktop) return;

      var distance = track.scrollWidth - window.innerWidth + 48;
      if (distance <= 0) return;

      gsap.to(track, {
        x: function () { return -distance; }, ease: "none",
        scrollTrigger: {
          id: "showcase-pin",
          trigger: sec, start: "top top+=76",
          end: function () { return "+=" + (distance + window.innerHeight * 0.5); },
          pin: true, scrub: 0.6, invalidateOnRefresh: true, anticipatePin: 1
        }
      });
    };

    setup();
    var to;
    window.addEventListener("resize", function () {
      clearTimeout(to);
      to = setTimeout(function () { ScrollTrigger.refresh(); setup(); }, 250);
    });
  }

  /* ------------------------------------------------------------------
     Reserva — WhatsApp
     ------------------------------------------------------------------ */
  function buildWhatsAppReserveLink(fields) {
    var wa = (data.brand && data.brand.whatsapp) || "";
    var lines = [
      "Hola Rescoldo! Quiero reservar mesa.",
      "Nombre: " + fields.name,
      "Teléfono: " + fields.phone,
      "Día: " + fields.day + " · Personas: " + fields.people
    ];
    if (fields.note) lines.push("Nota: " + fields.note);
    var text = encodeURIComponent(lines.join("\n"));
    return "https://wa.me/" + wa + "?text=" + text;
  }

  function initReservationForm() {
    var form = $("[data-reserve-form]");
    if (!form) return;
    form.setAttribute("novalidate", "novalidate");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var fields = {
        name: form.elements.nombre.value.trim(),
        phone: form.elements.telefono.value.trim(),
        day: form.elements.dia.value.trim(),
        people: form.elements.personas.value.trim(),
        note: form.elements.nota ? form.elements.nota.value.trim() : ""
      };
      var url = buildWhatsAppReserveLink(fields);
      window.open(url, "_blank", "noopener");
    });
  }

  /* ------------------------------------------------------------------
     Boot
     ------------------------------------------------------------------ */
  function boot() {
    safe(mountDishes, "mountDishes");
    safe(mountSessions, "mountSessions");
    safe(mountGallery, "mountGallery");
    safe(function () {
      if (window.__RESCOLDO_DISHES_3D_BOOT__) window.__RESCOLDO_DISHES_3D_BOOT__();
    }, "dishes3dBoot");

    safe(initSplash, "initSplash");
    safe(initEmbers, "initEmbers");
    safe(initCursor, "initCursor");
    safe(initNav, "initNav");
    safe(initSmoothScroll, "initSmoothScroll");
    safe(initReveals, "initReveals");
    safe(initTilt, "initTilt");
    safe(initMarquees, "initMarquees");
    safe(initDishDraw, "initDishDraw");
    safe(initShowcaseProgress, "initShowcaseProgress");
    safe(initReservationForm, "initReservationForm");

    if (window.gsap && window.ScrollTrigger) {
      try { gsap.registerPlugin(ScrollTrigger); } catch (_e) {}
      safe(initShowcasePinned, "initShowcasePinned");
    }

    document.documentElement.classList.add("is-ready");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
