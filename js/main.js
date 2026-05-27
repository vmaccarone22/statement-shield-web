(function () {
  var CONTACT_EMAIL = "hello@fundpilot.xyz";
  var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var nav = document.getElementById("nav");
  var toggle = document.getElementById("navToggle");
  var productNav = document.getElementById("productNav");
  var hero = document.getElementById("top");
  var yEl = document.getElementById("y");
  var emailEl = document.getElementById("contactEmail");
  var form = document.getElementById("contactForm");

  if (yEl) yEl.textContent = new Date().getFullYear();
  if (emailEl) emailEl.textContent = CONTACT_EMAIL;

  function setNavOpen(open) {
    if (!nav || !toggle) return;
    nav.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", open);
    toggle.textContent = open ? "×" : "☰";
    document.body.classList.toggle("nav-open", open);
  }

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      setNavOpen(!nav.classList.contains("is-open"));
    });
    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () { setNavOpen(false); });
    });
  }

  if (productNav && hero) {
    var navObs = new IntersectionObserver(
      function (entries) {
        productNav.classList.toggle("is-visible", !entries[0].isIntersecting);
      },
      { threshold: 0, rootMargin: "-" + getComputedStyle(document.documentElement).getPropertyValue("--nav-h").trim() + " 0px 0px 0px" }
    );
    navObs.observe(hero);
  }

  var navLinks = document.querySelectorAll(".product-nav-links a[data-section]");
  var sections = document.querySelectorAll("[data-nav-section]");
  if (navLinks.length && sections.length) {
    var secObs = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          var id = entry.target.getAttribute("data-nav-section");
          navLinks.forEach(function (link) {
            link.classList.toggle("is-active", link.getAttribute("data-section") === id);
          });
        });
      },
      { threshold: 0.25, rootMargin: "-15% 0px -45% 0px" }
    );
    sections.forEach(function (s) { secObs.observe(s); });
  }

  var reveals = document.querySelectorAll(".reveal");
  var isMobile = window.matchMedia("(max-width: 900px)").matches;
  if (reveals.length && (isMobile || reducedMotion)) {
    reveals.forEach(function (el) { el.classList.add("is-visible"); });
  } else if (reveals.length) {
    var revObs = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            revObs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1 }
    );
    reveals.forEach(function (el) { revObs.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-visible"); });
  }

  function loadVideo(video) {
    var src = video.getAttribute("data-src");
    if (!src || video.getAttribute("src")) return;
    video.setAttribute("src", src);
    video.load();
    video.play().catch(function () {});
  }

  document.querySelectorAll("video[data-lazy]").forEach(function (v) {
    if (reducedMotion) {
      loadVideo(v);
      return;
    }
    var vo = new IntersectionObserver(
      function (entries) {
        if (entries[0].isIntersecting) {
          loadVideo(v);
          vo.disconnect();
        }
      },
      { threshold: 0.15 }
    );
    vo.observe(v);
  });

  var pilotSection = document.getElementById("pilot");
  document.querySelectorAll(".demo-chip[data-pilot-step]").forEach(function (chip) {
    chip.addEventListener("click", function () {
      if (!pilotSection) return;
      var idx = parseInt(chip.getAttribute("data-pilot-step"), 10);
      if (isNaN(idx)) return;
      pilotSection.querySelectorAll(".demo-chip").forEach(function (c) {
        c.classList.toggle("is-active", c === chip);
      });
      pilotSection.querySelectorAll(".story-step").forEach(function (step, i) {
        var active = i === idx;
        step.classList.toggle("is-active", active);
        step.style.opacity = active ? "1" : "0";
        step.style.pointerEvents = active ? "auto" : "none";
      });
      pilotSection.querySelectorAll(".story-media").forEach(function (media, i) {
        var active = i === idx;
        media.classList.toggle("is-active", active);
        media.style.opacity = active ? "1" : "0";
      });
    });
  });

  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var fd = new FormData(form);
      var name = (fd.get("name") || "").toString().trim();
      var company = (fd.get("company") || "").toString().trim();
      var email = (fd.get("email") || "").toString().trim();
      var intent = (fd.get("intent") || "").toString().trim();
      var message = (fd.get("message") || "").toString().trim();
      if (!name || !company || !email) return;

      var intentLabel =
        intent === "launch" ? "Launching a new MCA company"
          : intent === "switch" ? "Switching our current shop"
            : "Not sure yet";

      var subject = encodeURIComponent("Fund Pilot — " + company);
      var body = encodeURIComponent(
        "Name: " + name + "\nCompany: " + company + "\nEmail: " + email +
          "\nIntent: " + intentLabel + "\n\n" + (message || "(no additional message)")
      );
      window.location.href =
        "mailto:" + encodeURIComponent(CONTACT_EMAIL) + "?subject=" + subject + "&body=" + body;
    });
  }

  /* Story progress dots */
  if (!reducedMotion) {
    document.querySelectorAll(".scroll-story").forEach(function (story) {
      var track = story.querySelector(".scroll-story-track");
      var dots = story.querySelectorAll(".story-dots span");
      var steps = story.querySelectorAll(".story-step");
      if (!track || !dots.length) return;

      function updateDots() {
        var rect = track.getBoundingClientRect();
        var total = track.offsetHeight - window.innerHeight;
        if (total <= 0) return;
        var progress = Math.max(0, Math.min(1, -rect.top / total));
        var idx = Math.min(steps.length - 1, Math.floor(progress * steps.length));
        dots.forEach(function (dot, i) {
          dot.style.background = i === idx ? "var(--accent)" : "rgba(255,255,255,0.15)";
          dot.style.transform = i === idx ? "scale(1.25)" : "scale(1)";
        });
      }
      window.addEventListener("scroll", updateDots, { passive: true });
      updateDots();
    });
  }
})();
