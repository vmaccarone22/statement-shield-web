(function () {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var canvas = document.getElementById("hero-canvas");
  if (!canvas || typeof THREE === "undefined") return;

  var scene = new THREE.Scene();
  var camera = new THREE.PerspectiveCamera(42, 1, 0.1, 100);
  camera.position.set(0.4, 0.1, 6.4);

  var renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setClearColor(0x000000, 0);

  scene.add(new THREE.AmbientLight(0xffffff, 0.35));
  var key = new THREE.DirectionalLight(0xffe4b5, 1.15);
  key.position.set(4, 6, 8);
  scene.add(key);
  var rim = new THREE.PointLight(0x8eb69b, 0.7, 22);
  rim.position.set(-5, -1, 4);
  scene.add(rim);

  var gold = new THREE.Color(0xd4af73);
  var group = new THREE.Group();
  scene.add(group);

  var core = new THREE.Mesh(
    new THREE.IcosahedronGeometry(1.12, 1),
    new THREE.MeshPhysicalMaterial({
      color: gold,
      metalness: 0.72,
      roughness: 0.22,
      clearcoat: 0.85,
      clearcoatRoughness: 0.15,
      emissive: 0x3a2e18,
      emissiveIntensity: 0.4,
    })
  );
  group.add(core);

  var ring = new THREE.Mesh(
    new THREE.TorusGeometry(1.72, 0.065, 16, 120),
    new THREE.MeshStandardMaterial({ color: 0xe8c992, metalness: 0.9, roughness: 0.25 })
  );
  ring.rotation.x = Math.PI / 2.35;
  group.add(ring);

  var orbitDots = new THREE.Group();
  for (var i = 0; i < 8; i++) {
    var a = (i / 8) * Math.PI * 2;
    var dot = new THREE.Mesh(
      new THREE.SphereGeometry(0.09, 16, 16),
      new THREE.MeshStandardMaterial({
        color: 0x8eb69b,
        emissive: 0x3a6a58,
        emissiveIntensity: 0.85,
        metalness: 0.2,
        roughness: 0.35,
      })
    );
    dot.position.set(Math.cos(a) * 2.15, Math.sin(a * 0.6) * 0.38, Math.sin(a) * 2.15);
    orbitDots.add(dot);
  }
  group.add(orbitDots);

  var particles = new THREE.BufferGeometry();
  var count = 620;
  var positions = new Float32Array(count * 3);
  for (var p = 0; p < count * 3; p++) positions[p] = (Math.random() - 0.5) * 14;
  particles.setAttribute("position", new THREE.BufferAttribute(positions, 3));
  scene.add(
    new THREE.Points(
      particles,
      new THREE.PointsMaterial({ color: 0xd4af73, size: 0.032, transparent: true, opacity: 0.55 })
    )
  );

  var innerRing = new THREE.Mesh(
    new THREE.TorusGeometry(2.25, 0.032, 12, 100),
    new THREE.MeshStandardMaterial({
      color: 0x8eb69b,
      metalness: 0.7,
      roughness: 0.3,
      transparent: true,
      opacity: 0.42,
    })
  );
  innerRing.rotation.x = Math.PI / 3;
  group.add(innerRing);

  var grid = new THREE.GridHelper(12, 24, 0x2a2520, 0x141210);
  grid.position.y = -1.85;
  grid.material.opacity = 0.2;
  grid.material.transparent = true;
  scene.add(grid);

  var mouse = { x: 0, y: 0 };
  var wrap = canvas.parentElement;
  (wrap || window).addEventListener(
    "pointermove",
    function (e) {
      var r = wrap ? wrap.getBoundingClientRect() : { width: window.innerWidth, height: window.innerHeight, left: 0, top: 0 };
      mouse.x = ((e.clientX - r.left) / r.width - 0.5) * 2;
      mouse.y = ((e.clientY - r.top) / r.height - 0.5) * 2;
    },
    { passive: true }
  );

  function resize() {
    var parent = canvas.parentElement;
    if (!parent) return;
    var w = parent.clientWidth;
    var h = parent.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    group.position.x = 0.15;
  }

  resize();
  window.addEventListener("resize", resize);

  var visible = true;
  var io = new IntersectionObserver(
    function (entries) {
      visible = entries[0] && entries[0].isIntersecting;
    },
    { threshold: 0.05 }
  );
  io.observe(wrap || canvas);

  var t0 = performance.now();
  function tick(now) {
    if (visible) {
      var t = (now - t0) * 0.001;
      group.rotation.y = t * 0.38 + mouse.x * 0.16;
      group.rotation.x = Math.sin(t * 0.42) * 0.07 + mouse.y * 0.1;
      ring.rotation.z = t * 0.55;
      orbitDots.rotation.y = -t * 0.48;
      innerRing.rotation.z = t * 0.32;
      renderer.render(scene, camera);
    }
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
})();
