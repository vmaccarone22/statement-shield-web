(function () {
  /** Replace with your live address before launch. */
  var CONTACT_EMAIL = "hello@fundpilot.xyz";
  var ASSET_V = "?v=202605258";

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
      var intent = (fd.get("intent") || "").toString().trim();
      var message = (fd.get("message") || "").toString().trim();

      if (!name || !company || !email) {
        return;
      }

      var intentLabel =
        intent === "launch"
          ? "Launching a new MCA company"
          : intent === "switch"
            ? "Switching our current shop"
            : intent === "both"
              ? "Not sure yet — want guidance"
              : "Not sure yet";

      var subject = encodeURIComponent("Fund Pilot — " + company);
      var body = encodeURIComponent(
        "Name: " +
          name +
          "\nCompany: " +
          company +
          "\nEmail: " +
          email +
          "\nIntent: " +
          intentLabel +
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

  function asset(path) {
    return path + ASSET_V;
  }

  /** Only one demo video plays at a time; others lazy-load on demand. */
  function initVideoManager() {
    var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var activeVideo = null;
    var loading = 0;

    function setLoading(on) {
      loading += on ? 1 : -1;
      document.body.classList.toggle("video-loading", loading > 0);
    }

    function pauseOthers(except) {
      document.querySelectorAll(".demo-video, .cinema-screen, .device-screen-fill").forEach(function (v) {
        if (v !== except) v.pause();
      });
    }

    function resolveSrc(video) {
      var lazy = video.getAttribute("data-lazy-src");
      if (lazy) return lazy;
      var source = video.querySelector("source");
      return source ? source.getAttribute("src") || "" : video.getAttribute("src") || "";
    }

    function markLoaded(video) {
      var wrap = video.closest(".cinema-monitor, .cinema-bezel, .device-laptop-bezel");
      if (wrap) wrap.classList.remove("is-loading");
      video.classList.remove("is-loading");
    }

    function loadVideo(video, autoplay) {
      var src = resolveSrc(video);
      if (!src) return Promise.resolve();

      var source = video.querySelector("source");
      var current = source ? source.getAttribute("src") : video.getAttribute("src");
      if (current === src && video.readyState >= 2) {
        markLoaded(video);
        if (autoplay && !reduced) {
          pauseOthers(video);
          video.play().catch(function () {});
          activeVideo = video;
        }
        return Promise.resolve();
      }

      var wrap = video.closest(".cinema-monitor, .cinema-bezel, .device-laptop-bezel");
      if (wrap) wrap.classList.add("is-loading");
      video.classList.add("is-loading");
      setLoading(true);

      return new Promise(function (resolve) {
        function done() {
          video.removeEventListener("canplay", onReady);
          video.removeEventListener("error", onErr);
          setLoading(false);
          markLoaded(video);
          if (autoplay && !reduced) {
            pauseOthers(video);
            video.play().catch(function () {});
            activeVideo = video;
          }
          resolve();
        }

        function onReady() {
          done();
        }

        function onErr() {
          setLoading(false);
          if (wrap) wrap.classList.add("is-error");
          resolve();
        }

        video.addEventListener("canplay", onReady);
        video.addEventListener("error", onErr);

        if (source) {
          source.src = src;
        } else {
          video.src = src;
        }
        video.load();
      });
    }

    function swapVideo(video, src, poster) {
      if (!video || !src) return Promise.resolve();
      video.pause();
      if (poster) video.setAttribute("poster", poster);
      video.setAttribute("data-lazy-src", src);
      var source = video.querySelector("source");
      if (source) source.removeAttribute("src");
      video.removeAttribute("src");
      return loadVideo(video, true);
    }

    document.querySelectorAll(".demo-video, .cinema-screen, .device-screen-fill").forEach(function (video) {
      video.preload = "none";
      if (reduced) {
        video.removeAttribute("autoplay");
        video.loop = false;
      }
      var lazy = video.getAttribute("data-lazy-src");
      if (lazy) {
        var source = video.querySelector("source");
        if (source) source.removeAttribute("src");
      }
    });

    var videoObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          var video = entry.target;
          if (!entry.isIntersecting) {
            if (video !== activeVideo) video.pause();
            return;
          }
          var shouldPlay = entry.intersectionRatio > 0.2 && !reduced;
          loadVideo(video, shouldPlay);
        });
      },
      { rootMargin: "120px 0px", threshold: 0.15 }
    );

    document.querySelectorAll(".demo-video, .cinema-screen, .device-screen-fill").forEach(function (video) {
      videoObserver.observe(video);
    });

    return { swapVideo: swapVideo, loadVideo: loadVideo, prefetch: function (src) {
      if (!src) return;
      var link = document.querySelector('link[data-prefetch="' + src + '"]');
      if (link) return;
      link = document.createElement("link");
      link.rel = "prefetch";
      link.as = "video";
      link.href = src;
      link.setAttribute("data-prefetch", src);
      document.head.appendChild(link);
    }};
  }

  function initBillingToggle() {
    var billingToggle = document.querySelector(".billing-toggle");
    if (!billingToggle) return;

    var opts = billingToggle.querySelectorAll(".billing-opt");

    function applyBilling(mode) {
      opts.forEach(function (btn) {
        var active = btn.getAttribute("data-billing") === mode;
        btn.classList.toggle("is-active", active);
        btn.setAttribute("aria-pressed", active ? "true" : "false");
      });

      document.querySelectorAll(".price-value").forEach(function (el) {
        el.textContent = el.getAttribute("data-" + mode) || el.textContent;
      });

      document.querySelectorAll(".price-billed").forEach(function (el) {
        el.innerHTML = el.getAttribute("data-" + mode) || el.innerHTML;
      });

      document.querySelectorAll(".price-extra").forEach(function (el) {
        el.textContent = el.getAttribute("data-" + mode) || el.textContent;
      });
    }

    opts.forEach(function (btn) {
      btn.addEventListener("click", function () {
        applyBilling(btn.getAttribute("data-billing") || "monthly");
      });
    });
  }

  function initDemoGallery(videoMgr) {
    var main = document.getElementById("galleryMainVideo");
    var desc = document.getElementById("galleryDesc");
    if (!main) return;

    var demos = {
      showreel: {
        main: asset("assets/demo-showreel-lite.mp4"),
        mainPoster: "assets/desktop-analyze-summary.png",
        desc: "Full showreel — analyze, Pilot, dialer, leads, and a live broker floor in one cut.",
      },
      analyze: {
        main: asset("assets/demo-desktop-analyze-lite.mp4"),
        mainPoster: "assets/desktop-analyze-summary.png",
        desc: "Drop four statement PDFs → positions, cash flow, DataMerch clear/hit, funding range.",
      },
      pilot: {
        main: asset("assets/demo-assistant-pilot-lite.mp4"),
        mainPoster: "assets/poster-assistant-pilot.png",
        desc: "“Hey Pilot — find the merchant cell” → traced number → one click to dialer.",
      },
      dialer: {
        main: asset("assets/demo-dialer-campaign-lite.mp4"),
        mainPoster: "assets/poster-dialer.png",
        desc: "Campaign queue, local caller ID, connected call timer, disposition saved to CRM.",
      },
      leads: {
        main: asset("assets/demo-leads-purchase-lite.mp4"),
        mainPoster: "assets/poster-leads.png",
        desc: "AI-scored leads — buy in-app, queued straight to your broker campaign.",
      },
      fleet: {
        main: asset("assets/demo-fleet-live-lite.mp4"),
        mainPoster: "assets/poster-fleet.png",
        desc: "52 brokers on headsets — Pilot on every desk, same platform, one rollout.",
      },
    };

    document.querySelectorAll(".demo-tab").forEach(function (tab) {
      var key = tab.getAttribute("data-gallery") || "showreel";
      var cfg = demos[key] || demos.showreel;
      tab.addEventListener("mouseenter", function () {
        videoMgr.prefetch(cfg.main);
      });
      tab.addEventListener("click", function () {
        document.querySelectorAll(".demo-tab").forEach(function (t) {
          t.classList.toggle("is-active", t === tab);
        });
        videoMgr.swapVideo(main, cfg.main, cfg.mainPoster);
        if (desc) desc.textContent = cfg.desc;
      });
    });
  }

  function initPilotDemoChips(videoMgr) {
    var video = document.getElementById("pilotFeaturedVideo");
    var caption = document.querySelector(".pilot-video-caption");
    if (!video) return;

    document.querySelectorAll(".demo-chip").forEach(function (chip) {
      chip.addEventListener("mouseenter", function () {
        videoMgr.prefetch(chip.getAttribute("data-demo-src"));
      });
      chip.addEventListener("click", function () {
        document.querySelectorAll(".demo-chip").forEach(function (c) {
          c.classList.toggle("is-active", c === chip);
        });
        videoMgr.swapVideo(
          video,
          chip.getAttribute("data-demo-src"),
          chip.getAttribute("data-demo-poster")
        );
        if (caption) caption.textContent = chip.getAttribute("data-demo-caption") || "";
      });
    });
  }

  var videoMgr = initVideoManager();
  initBillingToggle();
  initDemoGallery(videoMgr);
  initPilotDemoChips(videoMgr);
})();
