(function () {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var isMobile = window.matchMedia("(max-width: 900px)").matches;
  if (isMobile) {
    document.documentElement.classList.add("mobile-static");
    return;
  }

  var hasThree = typeof THREE !== "undefined";

  var GOLD = 0xd4af73;
  var SAGE = 0x8eb69b;

  function goldMat(opacity) {
    return new THREE.MeshPhysicalMaterial({
      color: GOLD,
      metalness: 0.68,
      roughness: 0.24,
      clearcoat: 0.75,
      transparent: opacity < 1,
      opacity: opacity || 1,
    });
  }

  function buildScene(type) {
    if (!hasThree) return null;
    var scene = new THREE.Scene();
    var group = new THREE.Group();
    scene.add(group);

    scene.add(new THREE.AmbientLight(0xffffff, 0.32));
    var key = new THREE.DirectionalLight(0xffe4b5, 1.05);
    key.position.set(4, 6, 8);
    scene.add(key);
    var rim = new THREE.PointLight(SAGE, 0.65, 24);
    rim.position.set(-5, -1, 4);
    scene.add(rim);

    var extras = [];

    if (type === "analyze") {
      for (var i = 0; i < 5; i++) {
        var sheet = new THREE.Mesh(
          new THREE.BoxGeometry(1.4, 1.9, 0.03),
          goldMat(0.55 + i * 0.08)
        );
        sheet.position.set((i - 2) * 0.08, i * 0.06, -i * 0.12);
        sheet.rotation.y = (i - 2) * 0.12;
        group.add(sheet);
      }
      var ring = new THREE.Mesh(
        new THREE.TorusGeometry(1.65, 0.055, 14, 100),
        new THREE.MeshStandardMaterial({ color: 0xe8c992, metalness: 0.88, roughness: 0.28 })
      );
      ring.rotation.x = Math.PI / 2.2;
      group.add(ring);
    } else if (type === "crm") {
      var board = new THREE.Mesh(new THREE.BoxGeometry(2.2, 1.4, 0.06), goldMat(0.7));
      group.add(board);
      for (var c = 0; c < 9; c++) {
        var card = new THREE.Mesh(
          new THREE.BoxGeometry(0.42, 0.28, 0.04),
          new THREE.MeshStandardMaterial({
            color: SAGE,
            metalness: 0.3,
            roughness: 0.4,
            emissive: 0x1a3028,
            emissiveIntensity: 0.5,
          })
        );
        card.position.set(((c % 3) - 1) * 0.55, Math.floor(c / 3) * 0.35 - 0.35, 0.08);
        group.add(card);
      }
    } else if (type === "pilot") {
      var core = new THREE.Mesh(
        new THREE.IcosahedronGeometry(0.95, 1),
        new THREE.MeshPhysicalMaterial({
          color: GOLD,
          metalness: 0.72,
          roughness: 0.2,
          clearcoat: 0.85,
          emissive: 0x3a2e18,
          emissiveIntensity: 0.45,
        })
      );
      group.add(core);
      for (var d = 0; d < 6; d++) {
        var a = (d / 6) * Math.PI * 2;
        var dot = new THREE.Mesh(
          new THREE.SphereGeometry(0.08, 12, 12),
          new THREE.MeshStandardMaterial({
            color: SAGE,
            emissive: 0x2a5040,
            emissiveIntensity: 0.8,
          })
        );
        dot.position.set(Math.cos(a) * 1.55, Math.sin(a * 0.5) * 0.3, Math.sin(a) * 1.55);
        group.add(dot);
      }
    } else if (type === "dialer") {
      var handset = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 1.6, 24), goldMat(0.85));
      handset.rotation.z = Math.PI / 2.4;
      group.add(handset);
      for (var w = 0; w < 3; w++) {
        var wave = new THREE.Mesh(
          new THREE.TorusGeometry(0.9 + w * 0.35, 0.025, 10, 64),
          new THREE.MeshStandardMaterial({
            color: SAGE,
            transparent: true,
            opacity: 0.35 - w * 0.08,
            metalness: 0.5,
          })
        );
        wave.rotation.x = Math.PI / 2;
        extras.push(wave);
        group.add(wave);
      }
    } else if (type === "leads") {
      var cone = new THREE.Mesh(new THREE.ConeGeometry(0.9, 1.8, 32), goldMat(0.5));
      cone.rotation.x = Math.PI;
      group.add(cone);
      for (var l = 0; l < 12; l++) {
        var lead = new THREE.Mesh(
          new THREE.SphereGeometry(0.07, 10, 10),
          new THREE.MeshStandardMaterial({
            color: SAGE,
            emissive: 0x2a5040,
            emissiveIntensity: 0.7,
          })
        );
        lead.position.set((Math.random() - 0.5) * 1.2, 0.5 + Math.random() * 1.2, (Math.random() - 0.5) * 1.2);
        extras.push(lead);
        group.add(lead);
      }
    }

    var pCount = 220;
    var positions = new Float32Array(pCount * 3);
    for (var p = 0; p < pCount * 3; p++) positions[p] = (Math.random() - 0.5) * 12;
    var particles = new THREE.BufferGeometry();
    particles.setAttribute("position", new THREE.BufferAttribute(positions, 3));
    var pts = new THREE.Points(
      particles,
      new THREE.PointsMaterial({ color: GOLD, size: 0.028, transparent: true, opacity: 0.45 })
    );
    scene.add(pts);

    return { scene: scene, group: group, extras: extras, particles: pts };
  }

  var stories = document.querySelectorAll("[data-scroll-story]");
  if (!stories.length) return;

  var instances = [];

  stories.forEach(function (section) {
    var canvas = section.querySelector(".story-canvas");
    var track = section.querySelector(".scroll-story-track");
    var steps = section.querySelectorAll(".story-step");
    var visual = section.querySelector(".story-visual");
    var mediaItems = section.querySelectorAll(".story-media");
    if (!track || !steps.length) return;

    var type = section.getAttribute("data-scroll-story") || "default";
    var built = hasThree && canvas ? buildScene(type) : null;
    var renderer = null;
    var camera = null;

    if (built && canvas) {
      camera = new THREE.PerspectiveCamera(40, 1, 0.1, 80);
      camera.position.set(0, 0, 5.5);
      renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
      renderer.setClearColor(0x000000, 0);

      function resize() {
        var w = canvas.clientWidth;
        var h = canvas.clientHeight;
        if (!w || !h) return;
        renderer.setSize(w, h, false);
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
      }
      resize();
    }

    instances.push({
      section: section,
      track: track,
      steps: steps,
      visual: visual,
      mediaItems: mediaItems,
      built: built,
      camera: camera,
      renderer: renderer,
      canvas: canvas,
      progress: 0,
      visible: false,
    });
  });

  if (!instances.length) return;

  function scrollProgress(track) {
    var rect = track.getBoundingClientRect();
    var total = track.offsetHeight - window.innerHeight;
    if (total <= 0) return 0;
    return Math.max(0, Math.min(1, -rect.top / total));
  }

  function applyProgress(inst, progress) {
    var steps = inst.steps;
    var stepCount = steps.length;
    var idx = Math.min(stepCount - 1, Math.floor(progress * stepCount));
    var local = progress * stepCount - idx;

    steps.forEach(function (step, i) {
      var active = i === idx;
      step.classList.toggle("is-active", active);
      step.style.opacity = active ? "1" : "0";
      step.style.visibility = active ? "visible" : "hidden";
      step.style.pointerEvents = active ? "auto" : "none";
    });

    if (inst.mediaItems.length) {
      inst.mediaItems.forEach(function (media, i) {
        var active = i === idx;
        media.classList.toggle("is-active", active);
        media.style.opacity = active ? String(1 - Math.abs(local - 0.5) * 0.3) : "0";
      });
    }

    if (inst.built) {
      var g = inst.built.group;
      var p = progress;
      g.rotation.y = p * Math.PI * 1.6 - 0.4;
      g.rotation.x = Math.sin(p * Math.PI) * 0.22;
      g.position.y = Math.sin(p * Math.PI * 2) * 0.15;
      g.scale.setScalar(0.85 + p * 0.35);

      inst.camera.position.z = 5.8 - p * 1.4;
      inst.camera.position.x = Math.sin(p * Math.PI * 2) * 0.35;
      inst.camera.lookAt(0, 0, 0);

      inst.built.extras.forEach(function (mesh, i) {
        if (mesh.geometry && mesh.geometry.type === "TorusGeometry") {
          mesh.scale.setScalar(1 + p * (0.4 + i * 0.15));
          mesh.material.opacity = Math.max(0.08, 0.4 - i * 0.1 + p * 0.2);
        }
      });
    }

    if (inst.visual) {
      var hasMedia = inst.mediaItems && inst.mediaItems.length;
      if (hasMedia) {
        var subtle = 0.98 + progress * 0.04;
        inst.visual.style.transform = "scale(" + subtle.toFixed(3) + ")";
      } else {
        var scale = 0.92 + progress * 0.12;
        var rotY = -14 + progress * 28;
        var rotX = 6 - progress * 10;
        var ty = (progress - 0.5) * -40;
        inst.visual.style.transform =
          "perspective(1200px) translateY(" +
          ty.toFixed(1) +
          "px) scale(" +
          scale.toFixed(3) +
          ") rotateX(" +
          rotX.toFixed(1) +
          "deg) rotateY(" +
          rotY.toFixed(1) +
          "deg)";
      }
    }

    inst.progress = progress;
  }

  var io = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        var inst = instances.find(function (x) {
          return x.section === entry.target;
        });
        if (inst) inst.visible = entry.isIntersecting;
      });
    },
    { rootMargin: "20% 0px", threshold: 0 }
  );
  instances.forEach(function (inst) {
    io.observe(inst.section);
  });

  function onScroll() {
    instances.forEach(function (inst) {
      applyProgress(inst, scrollProgress(inst.track));
    });
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", function () {
    instances.forEach(function (inst) {
      if (!inst.renderer || !inst.canvas) return;
      var w = inst.canvas.clientWidth;
      var h = inst.canvas.clientHeight;
      if (!w || !h) return;
      inst.renderer.setSize(w, h, false);
      inst.camera.aspect = w / h;
      inst.camera.updateProjectionMatrix();
    });
    onScroll();
  });

  onScroll();

  if (hasThree) {
    var t0 = performance.now();
    function tick(now) {
      var t = (now - t0) * 0.001;
      instances.forEach(function (inst) {
        if (!inst.visible || !inst.renderer || !inst.built) return;
        inst.built.particles.rotation.y = t * 0.06 + inst.progress * 0.5;
        inst.renderer.render(inst.built.scene, inst.camera);
      });
      requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }
})();
