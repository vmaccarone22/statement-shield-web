(function () {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  function parallaxBase(el) {
    var useMobile = window.innerWidth <= 960 && el.getAttribute("data-parallax-mobile");
    return el.getAttribute(useMobile ? "data-parallax-mobile" : "data-parallax-base") || "";
  }

  var stages = document.querySelectorAll("[data-tilt]");
  stages.forEach(function (stage) {
    var max = parseFloat(stage.getAttribute("data-tilt-max") || "14");
    var inner = stage.querySelector(".tilt-inner") || stage;
    var resting = "";
    var raf = 0;
    var target = { x: 0, y: 0 };
    var current = { x: 0, y: 0 };

    function apply() {
      current.x += (target.x - current.x) * 0.12;
      current.y += (target.y - current.y) * 0.12;
      inner.style.transform =
        "rotateX(" + (-current.y * max).toFixed(2) + "deg) rotateY(" + (current.x * max).toFixed(2) + "deg)";
      if (Math.abs(target.x - current.x) > 0.001 || Math.abs(target.y - current.y) > 0.001) {
        raf = requestAnimationFrame(apply);
      }
    }

    stage.addEventListener("pointermove", function (e) {
      var r = stage.getBoundingClientRect();
      target.x = (e.clientX - r.left) / r.width - 0.5;
      target.y = (e.clientY - r.top) / r.height - 0.5;
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(apply);
    });

    stage.addEventListener("pointerleave", function () {
      target.x = 0;
      target.y = 0;
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(apply);
    });
  });

  /* Scroll parallax on floating layers */
  var layers = document.querySelectorAll("[data-parallax]");
  if (!layers.length) return;

  function onScroll() {
    var vh = window.innerHeight;
    layers.forEach(function (el) {
      var speed = parseFloat(el.getAttribute("data-parallax") || "0.08");
      var r = el.getBoundingClientRect();
      var center = r.top + r.height * 0.5 - vh * 0.5;
      var shift = center * speed;
      el.style.transform = parallaxBase(el) + " translate3d(0," + shift.toFixed(1) + "px,0)";
    });
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();
})();
