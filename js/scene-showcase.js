(function () {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  if (typeof THREE === "undefined") return;

  document.querySelectorAll("[data-scene-3d]").forEach(function (wrap) {
    var canvas = wrap.querySelector("canvas");
    if (!canvas) return;

    var intensity = parseFloat(wrap.getAttribute("data-scene-intensity") || "1");
    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(38, 1, 0.1, 80);
    camera.position.z = 8;

    var renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.setClearColor(0x000000, 0);

    scene.add(new THREE.AmbientLight(0xffffff, 0.28));
    var key = new THREE.DirectionalLight(0xffe4b5, 0.9 * intensity);
    key.position.set(3, 5, 6);
    scene.add(key);

    var group = new THREE.Group();
    scene.add(group);

    var goldMat = new THREE.MeshPhysicalMaterial({
      color: 0xd4af73,
      metalness: 0.65,
      roughness: 0.28,
      clearcoat: 0.7,
      transparent: true,
      opacity: 0.85,
    });

    for (var i = 0; i < 5; i++) {
      var geo =
        i % 3 === 0
          ? new THREE.BoxGeometry(1.2, 0.7, 0.04)
          : i % 3 === 1
            ? new THREE.TorusGeometry(0.9 + i * 0.15, 0.035, 12, 64)
            : new THREE.OctahedronGeometry(0.35 + i * 0.08, 0);
      var mesh = new THREE.Mesh(geo, goldMat.clone());
      mesh.material.opacity = 0.35 + i * 0.08;
      mesh.position.set((i - 2) * 1.8, Math.sin(i) * 0.6, -i * 0.4);
      mesh.rotation.set(i * 0.4, i * 0.55, 0);
      group.add(mesh);
    }

    var pCount = 180;
    var positions = new Float32Array(pCount * 3);
    for (var p = 0; p < pCount * 3; p++) positions[p] = (Math.random() - 0.5) * 16;
    var particles = new THREE.BufferGeometry();
    particles.setAttribute("position", new THREE.BufferAttribute(positions, 3));
    scene.add(
      new THREE.Points(
        particles,
        new THREE.PointsMaterial({ color: 0xd4af73, size: 0.022, transparent: true, opacity: 0.4 })
      )
    );

    var mouse = { x: 0, y: 0 };
    wrap.addEventListener("pointermove", function (e) {
      var r = wrap.getBoundingClientRect();
      mouse.x = (e.clientX - r.left) / r.width - 0.5;
      mouse.y = (e.clientY - r.top) / r.height - 0.5;
    });

    function resize() {
      var w = wrap.clientWidth;
      var h = wrap.clientHeight;
      if (!w || !h) return;
      renderer.setSize(w, h, false);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
    }
    resize();
    window.addEventListener("resize", resize);

    var t0 = performance.now();
    var visible = false;
    var obs = new IntersectionObserver(
      function (entries) {
        visible = entries[0] && entries[0].isIntersecting;
      },
      { threshold: 0.05 }
    );
    obs.observe(wrap);

    function tick(now) {
      if (visible) {
        var t = (now - t0) * 0.001;
        group.rotation.y = t * 0.22 + mouse.x * 0.25;
        group.rotation.x = mouse.y * 0.18;
        group.children.forEach(function (c, idx) {
          c.rotation.z = t * (0.15 + idx * 0.05);
        });
        renderer.render(scene, camera);
      }
      requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  });
})();
