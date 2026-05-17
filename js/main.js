(function () {
  /** Replace with your live address before launch. */
  var CONTACT_EMAIL = "hello@statementshield.example";

  var nav = document.getElementById("nav");
  var toggle = document.getElementById("navToggle");
  var y = document.getElementById("y");
  var emailDisplay = document.getElementById("contactEmailDisplay");
  var form = document.getElementById("contactForm");

  if (y) y.textContent = new Date().getFullYear();
  if (emailDisplay) emailDisplay.textContent = CONTACT_EMAIL;

  function setNavOpen(open) {
    if (!nav || !toggle) return;
    nav.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", open);
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    toggle.textContent = open ? "×" : "☰";
    document.body.classList.toggle("nav-open", open);
  }

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      setNavOpen(!nav.classList.contains("is-open"));
    });

    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        setNavOpen(false);
      });
    });
  }

  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var fd = new FormData(form);
      var name = (fd.get("name") || "").toString().trim();
      var company = (fd.get("company") || "").toString().trim();
      var email = (fd.get("email") || "").toString().trim();
      var message = (fd.get("message") || "").toString().trim();

      if (!name || !company || !email) {
        return;
      }

      var subject =
        encodeURIComponent("Statement Shield demo — " + company);
      var body = encodeURIComponent(
        "Name: " +
          name +
          "\nCompany: " +
          company +
          "\nEmail: " +
          email +
          "\n\n" +
          (message || "(no additional message)")
      );
      window.location.href =
        "mailto:" +
        encodeURIComponent(CONTACT_EMAIL) +
        "?subject=" +
        subject +
        "&body=" +
        body;
    });
  }

  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var reveals = document.querySelectorAll(".reveal");
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) e.target.classList.add("is-visible");
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
    );
    reveals.forEach(function (el) {
      observer.observe(el);
    });
  } else {
    document.querySelectorAll(".reveal").forEach(function (el) {
      el.classList.add("is-visible");
    });
  }
})();
