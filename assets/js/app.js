/* HEP@IITK — small progressive-enhancement layer.
   Nothing here is required for the content to be readable. */
(function () {
  "use strict";
  document.documentElement.classList.add("js");

  /* --- mobile navigation ------------------------------------------------ */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.getAttribute("data-open") === "true";
      nav.setAttribute("data-open", String(!open));
      toggle.setAttribute("aria-expanded", String(!open));
    });
    nav.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        nav.setAttribute("data-open", "false");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.getAttribute("data-open") === "true") {
        nav.setAttribute("data-open", "false");
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
      }
    });
  }

  /* --- scroll reveal ---------------------------------------------------- */
  var reveal = document.querySelectorAll("[data-reveal]");
  if (reveal.length) {
    if (!("IntersectionObserver" in window)) {
      reveal.forEach(function (el) { el.classList.add("is-in"); });
    } else {
      var io = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              entry.target.classList.add("is-in");
              io.unobserve(entry.target);
            }
          });
        },
        { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
      );
      reveal.forEach(function (el) { io.observe(el); });
    }
  }

  /* --- count-up for stat tiles ----------------------------------------- */
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var nums = document.querySelectorAll("[data-count]");
  if (nums.length && !reduce && "IntersectionObserver" in window) {
    var cio = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          var el = entry.target;
          cio.unobserve(el);
          var target = parseInt(el.getAttribute("data-count"), 10);
          if (isNaN(target)) return;
          var start = performance.now();
          var dur = 900;
          (function step(now) {
            var t = Math.min((now - start) / dur, 1);
            var eased = 1 - Math.pow(1 - t, 3);
            el.textContent = String(Math.round(target * eased));
            if (t < 1) requestAnimationFrame(step);
          })(start);
        });
      },
      { threshold: 0.4 }
    );
    nums.forEach(function (el) { cio.observe(el); });
  }

  /* --- members filter --------------------------------------------------- */
  var search = document.getElementById("member-search");
  if (search) {
    var items = Array.prototype.slice.call(
      document.querySelectorAll("[data-person]")
    );
    var groups = Array.prototype.slice.call(
      document.querySelectorAll("[data-person-group]")
    );
    var status = document.getElementById("filter-status");

    var run = function () {
      var q = search.value.trim().toLowerCase();
      var shown = 0;
      items.forEach(function (el) {
        var hit = !q || (el.getAttribute("data-person") || "").indexOf(q) !== -1;
        el.classList.toggle("is-hidden", !hit);
        if (hit) shown++;
      });
      // hide a whole section when nothing in it matches
      groups.forEach(function (g) {
        var any = g.querySelectorAll("[data-person]:not(.is-hidden)").length;
        g.classList.toggle("is-hidden", q !== "" && any === 0);
      });
      if (status) {
        status.textContent = q
          ? shown + (shown === 1 ? " person matches “" : " people match “") + search.value + "”"
          : "";
      }
    };
    search.addEventListener("input", run);
    search.addEventListener("search", run);
    run();
  }

  /* --- active in-page subnav link -------------------------------------- */
  var subnavLinks = Array.prototype.slice.call(
    document.querySelectorAll(".subnav a[href^='#']")
  );
  if (subnavLinks.length && "IntersectionObserver" in window) {
    var targets = subnavLinks
      .map(function (a) { return document.querySelector(a.getAttribute("href")); })
      .filter(Boolean);
    var visible = Object.create(null);
    var paint = function () {
      // highlight the first section currently inside the band; none if empty
      var active = null;
      targets.some(function (t) {
        if (visible[t.id]) { active = t.id; return true; }
        return false;
      });
      subnavLinks.forEach(function (a) {
        a.classList.toggle("is-active", active !== null && a.getAttribute("href") === "#" + active);
      });
    };
    var sio = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          visible[entry.target.id] = entry.isIntersecting;
        });
        paint();
      },
      { rootMargin: "-20% 0px -60% 0px" }
    );
    targets.forEach(function (t) { sio.observe(t); });
  }

  /* --- current year in footer ------------------------------------------ */
  var y = document.querySelectorAll("[data-year]");
  y.forEach(function (el) { el.textContent = String(new Date().getFullYear()); });
})();
