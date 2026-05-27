import * as THREE from "three";
import {
  MODELS,
  createRenderer,
  createCamera,
  addBrandLights,
  applyStudioEnvironment,
  loadModel,
  addGoldParticles,
  resizeRenderer,
} from "./fp-gltf-core.js";

if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  var canvas = document.getElementById("hero-canvas");
  if (canvas) {
    var scene = new THREE.Scene();
    var camera = createCamera(40);
    camera.position.set(0.2, 0.1, 5.8);
    var renderer = createRenderer(canvas);
    addBrandLights(scene);
    applyStudioEnvironment(renderer, scene);
    var particles = addGoldParticles(scene, 420);

    var group = new THREE.Group();
    scene.add(group);
    var mouse = { x: 0, y: 0 };
    var wrap = canvas.parentElement;

    loadModel(MODELS.hero).then(function (loaded) {
      group.add(loaded.root);
    });

    (wrap || window).addEventListener(
      "pointermove",
      function (e) {
        var r = wrap
          ? wrap.getBoundingClientRect()
          : { width: window.innerWidth, height: window.innerHeight, left: 0, top: 0 };
        mouse.x = ((e.clientX - r.left) / r.width - 0.5) * 2;
        mouse.y = ((e.clientY - r.top) / r.height - 0.5) * 2;
      },
      { passive: true }
    );

    function resize() {
      resizeRenderer(renderer, camera, canvas);
    }
    resize();
    window.addEventListener("resize", resize);

    var visible = true;
    new IntersectionObserver(
      function (entries) {
        visible = entries[0] && entries[0].isIntersecting;
      },
      { threshold: 0.05 }
    ).observe(wrap || canvas);

    var t0 = performance.now();
    function tick(now) {
      if (visible) {
        var t = (now - t0) * 0.001;
        group.rotation.y = t * 0.28 + mouse.x * 0.18;
        group.rotation.x = mouse.y * 0.1 + Math.sin(t * 0.5) * 0.04;
        group.position.y = Math.sin(t * 0.7) * 0.06;
        particles.rotation.y = t * 0.04;
        renderer.render(scene, camera);
      }
      requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }
}
