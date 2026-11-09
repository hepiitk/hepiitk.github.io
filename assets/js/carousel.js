/* HEP@IITK — "Selected figures" slideshow on the Research page.
   Without JavaScript the figures are still a swipeable, scroll-snapping strip;
   this script adds autoplay, the dots, the 01 / 14 counter and the buttons.

   Change how long each figure stays on screen here (milliseconds): */
var CAROUSEL_DELAY = 6000;

(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  document.querySelectorAll("[data-carousel]").forEach(function (root) {
    var track = root.querySelector(".carousel__track");
    var slides = Array.prototype.slice.call(track.children);
    var dots = Array.prototype.slice.call(root.querySelectorAll(".carousel__dot"));
    var current = root.querySelector("[data-carousel-current]");
    var playBtn = root.querySelector("[data-carousel-play]");
    var n = slides.length;
    if (!n) return;

    var index = 0;
    var timer = null;
    var userPaused = reduce;   // reduced-motion visitors start paused
    var hovering = false;
    var focused = false;
    var onScreen = false;

    root.classList.add("is-ready");
    root.style.setProperty("--carousel-delay", CAROUSEL_DELAY + "ms");

    function pad(k) { return (k < 10 ? "0" : "") + k; }

    function paint() {
      dots.forEach(function (d, k) { d.setAttribute("aria-current", k === index ? "true" : "false"); });
      slides.forEach(function (s, k) {
        if (k === index) s.removeAttribute("inert"); else s.setAttribute("inert", "");
      });
      if (current) current.textContent = pad(index + 1);
    }

    function shouldPlay() {
      return !userPaused && !hovering && !focused && onScreen && !document.hidden;
    }

    function restart() {
      clearTimeout(timer);
      root.classList.remove("is-running");
      void root.offsetWidth; // restart the progress animation on the active dot
      if (shouldPlay()) {
        root.classList.add("is-running");
        timer = setTimeout(function () { go(index + 1, true); }, CAROUSEL_DELAY);
      }
    }

    function go(k, smooth) {
      index = (k + n) % n;
      track.scrollTo({ left: index * track.clientWidth, behavior: smooth && !reduce ? "smooth" : "auto" });
      paint();
      restart();
    }

    // dots and buttons
    dots.forEach(function (d, k) { d.addEventListener("click", function () { go(k, true); }); });
    root.querySelector("[data-carousel-prev]").addEventListener("click", function () { go(index - 1, true); });
    root.querySelector("[data-carousel-next]").addEventListener("click", function () { go(index + 1, true); });
    playBtn.addEventListener("click", function () {
      userPaused = !userPaused;
      root.classList.toggle("is-paused", userPaused);
      playBtn.setAttribute("aria-label", userPaused ? "Play the slideshow" : "Pause the slideshow");
      restart();
    });
    root.classList.toggle("is-paused", userPaused);
    if (userPaused) playBtn.setAttribute("aria-label", "Play the slideshow");

    // keyboard: arrow keys while the figures have focus
    track.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); go(index + 1, true); }
      if (e.key === "ArrowLeft") { e.preventDefault(); go(index - 1, true); }
    });

    // swiping / scrolling by hand: work out which figure is showing once it settles
    var settle = null;
    track.addEventListener("scroll", function () {
      clearTimeout(settle);
      settle = setTimeout(function () {
        var k = Math.round(track.scrollLeft / track.clientWidth);
        if (k !== index && k >= 0 && k < n) { index = k; paint(); restart(); }
      }, 140);
    }, { passive: true });

    // pause while the visitor is reading (mouse over it, or keyboard focus inside)
    root.addEventListener("mouseenter", function () { hovering = true; restart(); });
    root.addEventListener("mouseleave", function () { hovering = false; restart(); });
    root.addEventListener("focusin", function () { focused = true; restart(); });
    root.addEventListener("focusout", function (e) {
      if (!root.contains(e.relatedTarget)) { focused = false; restart(); }
    });
    document.addEventListener("visibilitychange", restart);

    // only run while the slideshow is on screen
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        onScreen = entries[0].isIntersecting;
        restart();
      }, { threshold: 0.35 }).observe(root);
    } else {
      onScreen = true;
    }

    // keep the current figure lined up when the window is resized
    window.addEventListener("resize", function () {
      track.scrollTo({ left: index * track.clientWidth, behavior: "auto" });
    });

    paint();
    restart();
  });
})();
