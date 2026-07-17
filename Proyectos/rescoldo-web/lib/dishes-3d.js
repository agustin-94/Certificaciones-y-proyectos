/* ==========================================================================
   Rescoldo — piezas 3D poligonales para los 4 platos "Casa"
   Requiere: lib/three.min.js (cargado ANTES de este archivo)
   No usa texturas ni imágenes externas: geometría + material únicamente.
   ========================================================================== */
(function () {
  "use strict";

  function safe(fn, name) {
    try { fn(); } catch (e) { console.warn("[" + name + "]", e); }
  }

  /* Un único rAF compartido para todas las escenas (evita B.11: múltiples loops) */
  var ticker = {
    fns: [],
    running: false,
    add: function (fn) { this.fns.push(fn); this.start(); },
    start: function () {
      if (this.running) return;
      this.running = true;
      var self = this;
      function loop(t) {
        for (var i = 0; i < self.fns.length; i++) {
          safe(function () { self.fns[i](t); }, "dish3d-tick");
        }
        requestAnimationFrame(loop);
      }
      requestAnimationFrame(loop);
    }
  };

  function hasWebGL() {
    try {
      var c = document.createElement("canvas");
      return !!(window.WebGLRenderingContext &&
        (c.getContext("webgl") || c.getContext("experimental-webgl")));
    } catch (e) { return false; }
  }

  function isMobile() {
    return window.innerWidth < 900 || /Mobi|Android/i.test(navigator.userAgent);
  }

  /* Geometría poligonal distinta por vajilla — bajo poligonaje a propósito */
  function makeGeometry(kind) {
    var THREE_ = window.THREE;
    switch (kind) {
      case "asador_cruz":
        return new THREE_.OctahedronGeometry(1.05, 0);
      case "plancha":
        return new THREE_.IcosahedronGeometry(1, 0);
      case "parrilla":
        return new THREE_.TorusKnotGeometry(0.62, 0.22, 90, 8, 2, 3);
      case "cazuela":
        return new THREE_.DodecahedronGeometry(1, 0);
      default:
        return new THREE_.IcosahedronGeometry(1, 0);
    }
  }

  function hexToInt(hex) {
    return parseInt(String(hex || "#E8592A").replace("#", ""), 16);
  }

  function initDishScene(container, opts) {
    if (!hasWebGL() || !window.THREE) {
      container.classList.add("is-flat");
      return;
    }
    var THREE_ = window.THREE;
    var w = container.clientWidth || 240;
    var h = container.clientHeight || 240;

    var scene = new THREE_.Scene();
    var camera = new THREE_.PerspectiveCamera(38, w / h, 0.1, 100);
    camera.position.set(0, 0.15, 4.4);

    var renderer = new THREE_.WebGLRenderer({ antialias: true, alpha: true });
    var dpr = Math.min(window.devicePixelRatio || 1, isMobile() ? 1.5 : 2);
    renderer.setPixelRatio(dpr);
    renderer.setSize(w, h);
    if (isMobile()) { renderer.shadowMap.enabled = false; }
    renderer.domElement.setAttribute("aria-hidden", "true");
    container.appendChild(renderer.domElement);

    var geo = makeGeometry(opts.kind);
    var colorInt = hexToInt(opts.color);
    var accentInt = hexToInt(opts.accent);

    var mat = new THREE_.MeshStandardMaterial({
      color: colorInt, flatShading: true, metalness: 0.32, roughness: 0.42
    });
    var mesh = new THREE_.Mesh(geo, mat);
    scene.add(mesh);

    var edges = new THREE_.EdgesGeometry(geo);
    var wire = new THREE_.LineSegments(edges, new THREE_.LineBasicMaterial({
      color: accentInt, transparent: true, opacity: 0.55
    }));
    mesh.add(wire);

    var key = new THREE_.DirectionalLight(0xfff2df, 1.15);
    key.position.set(3, 4, 5);
    scene.add(key);
    var rim = new THREE_.PointLight(accentInt, 1.6, 12);
    rim.position.set(-3, -1.5, 2.2);
    scene.add(rim);
    var amb = new THREE_.AmbientLight(0xffffff, 0.32);
    scene.add(amb);

    var visible = false;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { visible = e.isIntersecting; });
    }, { threshold: 0.05 });
    io.observe(container);

    var t0 = null;
    function update(t) {
      if (!visible) return;
      if (t0 === null) t0 = t;
      var dt = t - t0;
      mesh.rotation.y = dt * 0.00028;
      mesh.rotation.x = Math.sin(dt * 0.00018) * 0.18;
      renderer.render(scene, camera);
    }
    ticker.add(update);

    var resizeTo;
    window.addEventListener("resize", function () {
      clearTimeout(resizeTo);
      resizeTo = setTimeout(function () {
        var w2 = container.clientWidth, h2 = container.clientHeight;
        if (!w2 || !h2) return;
        camera.aspect = w2 / h2;
        camera.updateProjectionMatrix();
        renderer.setSize(w2, h2);
      }, 150);
    });
  }

  function boot() {
    var mounts = document.querySelectorAll("[data-dish-3d]");
    mounts.forEach(function (el) {
      if (el.dataset.dish3dBound) return;
      el.dataset.dish3dBound = "1";
      var kind = el.getAttribute("data-dish-3d");
      var color = el.getAttribute("data-dish-color") || "#E8592A";
      var accent = el.getAttribute("data-dish-accent") || "#E8592A";
      safe(function () { initDishScene(el, { kind: kind, color: color, accent: accent }); }, "initDishScene:" + kind);
    });
  }

  /* No se auto-arranca en DOMContentLoaded: los [data-dish-3d] recién existen
     después de que main.js monte las tarjetas de plato (mountDishes). main.js
     llama a window.__RESCOLDO_DISHES_3D_BOOT__() explícitamente en su boot(). */
  window.__RESCOLDO_DISHES_3D_BOOT__ = boot;
})();
