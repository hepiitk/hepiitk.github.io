/* HEP@IITK — Home page animation.
   Two neutron stars spiral together along engraved orbit paths, trailing
   smooth glowing tails of stripped matter that flare into spiral arms as they
   get close, collide in a burst and leave a black hole, while the gravitational-
   wave "chirp" a detector would record is drawn underneath, in step.
   Drawn on the <canvas> inside <div class="merger"> (HERO_ART in build_all.py).
   Plain JavaScript, no libraries. Pauses when off screen; visitors who prefer
   reduced motion see one still frame. Kept light so phones and tablets run it
   smoothly: a fixed number of particles, no special blending, and the parts
   that never move are drawn only once.

   Things you can tune: */
var MERGER = {
  cycle: 13,        // seconds for one full loop
  inspiral: 8,      // seconds the two stars orbit before they touch
  turns: 4,         // orbits during the inspiral
  tail: 1.6,        // tail length at the start, in radians of orbit (it grows as the stars close in)
  maxParticles: 700,// puffs of stripped matter on screen at once (lower = lighter for old phones)
  // star colours: [highlight, body, rim] as R,G,B
  starA: [[255, 244, 214], [245, 158, 11], [194, 65, 12]],    // amber
  starB: [[232, 242, 255], [59, 130, 246], [30, 58, 138]]     // blue
};

(function () {
  "use strict";
  var box = document.querySelector(".merger");
  if (!box) return;
  var canvas = box.querySelector("canvas");
  var ctx = canvas.getContext && canvas.getContext("2d");
  if (!ctx) return;

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var TAU = Math.PI * 2;
  var A0 = 0.42;                    // starting distance of each star from the centre (unit disc)
  var WAVE = { x0: -0.5, x1: 0.5, y: 0.72, amp: 0.075, merge: 0.8 };  // the chirp graph
  var size = 0, scale = 0, dpr = 1;
  var particles = [], ripples = [], dots = [];
  var t = 0, lastRipple = 0, merged = false, owed = 0, G = 1;
  var running = false, onScreen = true, last = 0;

  function rand(a, b) { return a + Math.random() * (b - a); }
  function rgba(c, a) { return "rgba(" + c[0] + "," + c[1] + "," + c[2] + "," + Math.max(0, a).toFixed(3) + ")"; }
  function lerp(c1, c2, f) {
    return [Math.round(c1[0] + (c2[0] - c1[0]) * f), Math.round(c1[1] + (c2[1] - c1[1]) * f),
            Math.round(c1[2] + (c2[2] - c1[2]) * f)];
  }
  function X(x) { return scale + x * scale; }
  // moving parts fade out towards the edge, so the animation melts into the page
  // (worked out per object: far cheaper on phones than masking the whole canvas)
  function edge(r) { return r <= 0.6 ? 1 : r >= 0.93 ? 0 : 1 - (r - 0.6) / 0.33; }

  // ---------------------------------------------------------------- physics
  // separation and orbital phase follow the gravitational-wave chirp:
  // a ∝ τ^(1/4), phase ∝ 1 − τ^(5/8)
  function orbit(time) {
    var tau = Math.min(Math.max(1 - time / MERGER.inspiral, 0), 1);
    var a = A0 * Math.pow(tau, 0.25);
    var phi = TAU * MERGER.turns * (1 - Math.pow(tau, 0.625));
    var omega = TAU * MERGER.turns * 0.625 * Math.pow(Math.max(tau, 1e-4), -0.375) / MERGER.inspiral;
    return { a: a, phi: phi, omega: Math.min(omega, 40), tau: tau };
  }
  // the same orbit, looked up by phase instead of time (used to draw the tails)
  function sepAtPhase(phi) {
    if (phi <= 0) return A0;
    var tau = Math.pow(Math.max(1 - phi / (TAU * MERGER.turns), 0), 1.6);
    return A0 * Math.pow(tau, 0.25);
  }

  function emit(o, k) {
    // puffs of stripped matter leave each star; each keeps its star's colour at first
    for (var s = 0; s < 2; s++) {
      var ang = o.phi + s * Math.PI;
      for (var n = 0; n < k; n++) {
        if (particles.length >= MERGER.maxParticles) return;
        var r = o.a + rand(0, 0.05);
        var vt = o.a * o.omega * rand(0.95, 1.3);
        particles.push({ r: r, th: ang + rand(-0.15, 0.15), L: r * vt, vr: rand(0.03, 0.14),
                         age: 0, life: rand(1.8, 3.2), size: rand(0.014, 0.026), a: 0.5, ramp: s });
      }
    }
  }

  function explode() {
    merged = true;
    for (var i = 0; i < 200; i++) {
      var sp = rand(0.08, 0.5) * rand(0.6, 1);
      particles.push({ r: rand(0, 0.04), th: rand(0, TAU), L: rand(0.004, 0.03), vr: sp, age: 0,
                       life: rand(2.2, 4), size: rand(0.026, 0.044), a: 0.3, ramp: 2 });
    }
    ripples.push({ r: 0.03, a: 0.6, w: 2.2 });
  }

  function reset() { particles = []; ripples = []; t = 0; lastRipple = 0; merged = false; owed = 0; }

  function step(dt) {
    t += dt;
    if (t >= MERGER.cycle) reset();
    var o = orbit(t);
    if (!merged && t < MERGER.inspiral) {
      // emission is counted per second, not per frame, so 60 Hz and 120 Hz
      // screens make the same amount of matter
      if (o.a < 0.3) {
        owed += (0.3 - o.a) * 900 * dt;
        var k = Math.floor(owed);
        owed -= k;
        if (k) emit(o, k);
      }
      var period = TAU / Math.max(o.omega, 0.1) / 2;           // ripples twice per orbit
      if (t - lastRipple > Math.max(period, 0.18)) {
        ripples.push({ r: 0.05, a: 0.1 + 0.25 * (1 - o.a / A0), w: 1 });
        lastRipple = t;
      }
    }
    if (!merged && t >= MERGER.inspiral) explode();
    for (var i = particles.length - 1; i >= 0; i--) {
      var p = particles[i];
      p.age += dt;
      if (p.age > p.life || p.r > 0.95) { particles.splice(i, 1); continue; }
      p.vr += 0.02 * dt;
      p.r += p.vr * dt;
      p.th += (p.L / Math.max(p.r * p.r, 0.002)) * dt;
    }
    for (var j = ripples.length - 1; j >= 0; j--) {
      var w = ripples[j];
      w.r += 0.42 * dt;
      w.a *= Math.pow(0.55, dt);
      if (w.r > 0.95 || w.a < 0.01) ripples.splice(j, 1);
    }
  }

  // ---------------------------------------------------------------- set-up drawing
  var GOLD = [214, 150, 58], MAROON = [125, 31, 44], VIOLET = [109, 76, 160];
  var RAMPS = [
    [MERGER.starA[1], GOLD, MAROON],            // matter from star A
    [MERGER.starB[1], VIOLET, MAROON],          // matter from star B
    [[236, 170, 80], [214, 110, 70], MAROON],   // debris after the collision
    [MERGER.starA[0], MERGER.starA[1], VIOLET], // tail of star A: hot core → amber → violet
    [MERGER.starB[0], MERGER.starB[1], VIOLET]  // tail of star B: hot core → blue → violet
  ];
  var SPRITES = [];
  function makeSprites() {
    SPRITES = RAMPS.map(function (ramp) {
      var list = [];
      for (var i = 0; i < 16; i++) {
        var c = i / 15, col = c < 0.5 ? lerp(ramp[0], ramp[1], c * 2) : lerp(ramp[1], ramp[2], (c - 0.5) * 2);
        var cv = document.createElement("canvas");
        cv.width = cv.height = 64;
        var g = cv.getContext("2d"), gr = g.createRadialGradient(32, 32, 0, 32, 32, 32);
        gr.addColorStop(0, rgba(col, 0.9));
        gr.addColorStop(0.35, rgba(col, 0.42));
        gr.addColorStop(0.7, rgba(col, 0.1));
        gr.addColorStop(1, rgba(col, 0));
        g.fillStyle = gr; g.fillRect(0, 0, 64, 64);
        list.push(cv);
      }
      return list;
    });
  }

  // the parts that never move — the soft sky disc, two faint guide rings, the
  // engraved orbit paths and the graph's base line — are painted once and shown
  // as the canvas's background picture, so no frame has to repaint them
  function makeBackground() {
    var bg = document.createElement("canvas");
    bg.width = bg.height = size;
    var g = bg.getContext("2d");

    // a soft round window of sky whose edge feathers into the page (no hard line)
    var gr = g.createRadialGradient(scale, scale, 0, scale, scale, scale);
    var stops = [[0, 255, 255, 255, 0.9], [0.5, 248, 246, 239, 0.8], [0.72, 239, 235, 225, 0.72],
                 [0.84, 232, 227, 214, 0.62], [0.92, 229, 223, 208, 0.4], [0.97, 229, 223, 208, 0.14],
                 [1, 229, 223, 208, 0]];
    stops.forEach(function (c) { gr.addColorStop(c[0], "rgba(" + c[1] + "," + c[2] + "," + c[3] + "," + c[4] + ")"); });
    g.fillStyle = gr; g.fillRect(0, 0, size, size);

    // two whisper-thin guide rings that fade in and out around the circle
    g.lineWidth = 1 * dpr;
    for (var ring = 0; ring < 2; ring++) {
      var rr = [0.86, 0.72][ring] * scale;
      var cg = g.createConicGradient ? g.createConicGradient(-Math.PI / 2 + ring, scale, scale) : null;
      if (cg) {
        cg.addColorStop(0, "rgba(160,150,128,0.2)");
        cg.addColorStop(0.25, "rgba(160,150,128,0.05)");
        cg.addColorStop(0.5, "rgba(160,150,128,0.18)");
        cg.addColorStop(0.75, "rgba(160,150,128,0.05)");
        cg.addColorStop(1, "rgba(160,150,128,0.2)");
        g.strokeStyle = cg;
      } else {
        g.strokeStyle = "rgba(160,150,128,0.12)";
      }
      g.setLineDash(ring ? [1 * dpr, 5 * dpr] : []);
      g.beginPath(); g.arc(scale, scale, rr, 0, TAU); g.stroke();
    }

    // engraved inspiral paths, one per star
    var cols = ["rgba(170,120,70,0.5)", "rgba(80,105,160,0.5)"];
    for (var s = 0; s < 2; s++) {
      g.strokeStyle = cols[s];
      g.setLineDash([1.1 * dpr, 3.6 * dpr]);
      g.beginPath();
      for (var k = 0; k <= 600; k++) {
        var o = orbit(MERGER.inspiral * k / 600);
        var ang = o.phi + s * Math.PI;
        var x = X(o.a * Math.cos(ang)), y = X(o.a * Math.sin(ang));
        if (k === 0) g.moveTo(x, y); else g.lineTo(x, y);
      }
      g.stroke();
    }
    g.setLineDash([]);

    // base line of the gravitational-wave graph
    g.strokeStyle = "rgba(197,191,174,0.9)";
    g.beginPath(); g.moveTo(X(WAVE.x0), X(WAVE.y)); g.lineTo(X(WAVE.x1), X(WAVE.y)); g.stroke();

    canvas.style.background = "url(" + bg.toDataURL() + ") center / 100% 100% no-repeat";
  }

  function makeDots() {
    dots = [];
    for (var i = 0; i < 120; i++) {
      var r = Math.sqrt(Math.random()) * 0.88, a = rand(0, TAU);
      var big = Math.random() < 0.08;
      dots.push({ x: r * Math.cos(a), y: r * Math.sin(a), s: big ? rand(1.4, 2) : rand(0.5, 1.1),
                  b: (big ? rand(0.45, 0.7) : rand(0.18, 0.5)) * (1 - Math.pow(r / 0.9, 4)),
                  tw: rand(0.6, 2.2), ph: rand(0, TAU), big: big,
                  c: Math.random() < 0.5 ? "29,53,87" : (Math.random() < 0.5 ? "125,31,44" : "90,96,104") });
    }
  }
  function drawDots(now) {
    for (var i = 0; i < dots.length; i++) {
      var d = dots[i], b = d.b * (0.65 + 0.35 * Math.sin(now * d.tw + d.ph));
      var x = X(d.x), y = X(d.y), r = d.s * dpr;
      ctx.fillStyle = "rgba(" + d.c + "," + b.toFixed(3) + ")";
      ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill();
      if (d.big) {                                   // a faint four-point glint on the brighter ones
        ctx.strokeStyle = "rgba(" + d.c + "," + (b * 0.5).toFixed(3) + ")";
        ctx.lineWidth = 0.6 * dpr;
        ctx.beginPath();
        ctx.moveTo(x - 4 * r, y); ctx.lineTo(x + 4 * r, y);
        ctx.moveTo(x, y - 4 * r); ctx.lineTo(x, y + 4 * r);
        ctx.stroke();
      }
    }
  }

  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    var w = box.getBoundingClientRect().width || 420;
    var newSize = Math.round(w * dpr);
    if (newSize === size) return false;   // phones fire "resize" while scrolling; nothing changed
    size = newSize;
    canvas.width = canvas.height = size;
    scale = size / 2;
    makeBackground();
    return true;
  }

  // ---------------------------------------------------------------- drawing
  function glow(x, y, r, stops, fade) {
    var g = ctx.createRadialGradient(X(x), X(y), 0, X(x), X(y), r * scale);
    for (var i = 0; i < stops.length; i++) g.addColorStop(stops[i][0], stops[i][1]);
    ctx.fillStyle = g;
    ctx.beginPath(); ctx.arc(X(x), X(y), r * scale, 0, TAU); ctx.fill();
  }

  // the gravitational-wave strain: frequency and height rise until the merger,
  // then the signal "rings down"
  function strain(time) {
    if (time <= MERGER.inspiral) {
      var o = orbit(time);
      var amp = Math.min(0.18 * Math.pow(Math.max(o.tau, 0.002), -0.25), 1);
      return amp * Math.sin(2 * o.phi);
    }
    var o2 = orbit(MERGER.inspiral), since = time - MERGER.inspiral;
    return Math.exp(-since / 0.12) * Math.sin(2 * o2.phi + 2 * 40 * since);
  }

  function drawWave() {
    var tEnd = MERGER.inspiral + 0.9;                       // the graph ends shortly after the merger
    var now = Math.min(t, tEnd);
    var w = WAVE.x1 - WAVE.x0;
    function xAt(time) {
      return time <= MERGER.inspiral ? WAVE.x0 + w * WAVE.merge * time / MERGER.inspiral
                                     : WAVE.x0 + w * (WAVE.merge + (1 - WAVE.merge) * (time - MERGER.inspiral) / 0.9);
    }
    ctx.strokeStyle = "rgba(29,53,87,0.9)";
    ctx.lineWidth = 1.3 * dpr;
    ctx.lineJoin = "round";
    ctx.beginPath();
    var n = Math.max(2, Math.round(420 * now / tEnd));
    for (var i = 0; i <= n; i++) {
      var time = now * i / n;
      var x = X(xAt(time)), y = X(WAVE.y - WAVE.amp * strain(time));
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();
    // a small marker at the pen tip while the signal is being written
    if (t < tEnd) {
      ctx.fillStyle = "rgba(125,31,44,0.9)";
      ctx.beginPath(); ctx.arc(X(xAt(now)), X(WAVE.y - WAVE.amp * strain(now)), 2.2 * dpr, 0, TAU); ctx.fill();
    }
  }

  function drawStar(x, y, ang, stretch, col) {
    glow(x, y, 0.16, [[0, rgba(col[1], 0.38 * G)], [0.45, rgba(col[1], 0.13 * G)], [1, rgba(col[1], 0)]]);
    ctx.save();
    ctx.translate(X(x), X(y));
    ctx.rotate(ang);
    ctx.scale(stretch, 1 / Math.sqrt(stretch));
    var R = 0.05 * scale;
    var core = ctx.createRadialGradient(-R * 0.25, -R * 0.25, 0, 0, 0, R);
    core.addColorStop(0, rgba(col[0], G));
    core.addColorStop(0.45, rgba(col[1], G));
    core.addColorStop(0.85, rgba(col[2], 0.95 * G));
    core.addColorStop(1, rgba(col[2], 0));
    ctx.fillStyle = core;
    ctx.beginPath(); ctx.arc(0, 0, R, 0, TAU); ctx.fill();
    ctx.restore();
  }

  // A smooth tail of stripped matter behind each star: many soft, overlapping
  // glows laid along the star's own orbit, shrinking and cooling from the hot
  // core colour through the star's colour to violet. As the stars close in the
  // tail gets longer and swings outwards into a spiral arm.
  function drawTail(s, o) {
    var close = Math.max(0, 0.26 - o.a) / 0.26;           // 0 far apart … 1 touching
    var len = Math.min(MERGER.tail * (1 + 1.4 * close), 0.85 * TAU);
    var W = 0.05 * (0.85 + 0.6 * close);                  // tail width at the star
    var n = 54;
    for (var i = n; i >= 1; i--) {                         // from the tip of the tail up to the star
      var u = i / n;                                       // 0 at the star, 1 at the tip
      var ph = o.phi - len * u;
      var r = sepAtPhase(ph) * (1 + 0.55 * close * u * u) + 0.01 * u;
      if (r < 0.005) continue;
      var ang = ph + s * Math.PI;
      var x = r * Math.cos(ang), y = r * Math.sin(ang);
      var w = W * (0.25 + 0.95 * Math.pow(1 - u, 0.7)) * (1 + 0.6 * close * u);
      var al = 0.26 * Math.pow(1 - u, 1.2) * edge(r) * G;
      if (al < 0.004) continue;
      ctx.globalAlpha = al;
      var px = X(x), py = X(y), sz = w * scale * 2;
      ctx.drawImage(SPRITES[3 + s][Math.round(Math.min(1, 0.15 + u) * 15)], px - sz, py - sz, 2 * sz, 2 * sz);
    }
    ctx.globalAlpha = 1;
  }

  function draw(now) {
    now = now || 0;
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.globalCompositeOperation = "source-over";
    ctx.globalAlpha = 1;
    ctx.clearRect(0, 0, size, size);       // transparent: the sky disc behind shows through

    drawDots(now);                         // distant stars twinkle underneath everything

    // the moving parts fade out together at the end of the loop
    var fadeOut = MERGER.cycle - 0.8;
    G = t > fadeOut ? Math.max(0, 1 - (t - fadeOut) / 0.8) : 1;

    for (var j = 0; j < ripples.length; j++) {
      var w = ripples[j];
      ctx.strokeStyle = "rgba(29,53,87," + (w.a * 0.8 * edge(w.r) * G).toFixed(3) + ")";
      ctx.lineWidth = w.w * dpr;
      ctx.beginPath(); ctx.arc(scale, scale, w.r * scale, 0, TAU); ctx.stroke();
    }

    // stripped matter and debris: soft puffs that cool to maroon as they drift out
    for (var k = 0; k < particles.length; k++) {
      var p = particles[k], f = p.age / p.life;
      var c = Math.min(1, f * 1.5 + (p.ramp === 2 ? 0.2 : 0));
      var al = (1 - f) * (f < 0.08 ? f / 0.08 : 1) * p.a * edge(p.r) * G;
      if (al < 0.01) continue;
      ctx.globalAlpha = al;
      var s = p.size * scale * (1 + 1.1 * f);
      ctx.drawImage(SPRITES[p.ramp][Math.round(c * 15)],
                    X(p.r * Math.cos(p.th)) - s, X(p.r * Math.sin(p.th)) - s, 2 * s, 2 * s);
    }
    ctx.globalAlpha = 1;

    var o = orbit(t);
    if (!merged) {
      var cols = [MERGER.starA, MERGER.starB];
      var stretch = 1 + 1.4 * Math.max(0, 0.2 - o.a) / 0.2;      // tides stretch the stars
      for (var s2 = 0; s2 < 2; s2++) drawTail(s2, o);
      for (var s3 = 0; s3 < 2; s3++) {
        var ang = o.phi + s3 * Math.PI;
        drawStar(o.a * Math.cos(ang), o.a * Math.sin(ang), ang, stretch, cols[s3]);
      }
      if (o.a < 0.12) glow(0, 0, 0.3, [[0, "rgba(245,180,80," + (0.35 * (1 - o.a / 0.12)).toFixed(3) + ")"], [1, "rgba(245,180,80,0)"]]);
    } else {
      var since = t - MERGER.inspiral;
      var fl = Math.max(0, 1 - since / 0.9);
      if (fl > 0) {                                       // the burst: gold glow and a racing maroon rim
        glow(0, 0, 0.12 + since * 0.8, [[0, "rgba(255,214,120," + (0.9 * fl).toFixed(3) + ")"], [0.55, "rgba(232,160,60," + (0.45 * fl).toFixed(3) + ")"], [1, "rgba(232,160,60,0)"]]);
        var rim = 0.05 + since * 0.75;
        ctx.strokeStyle = "rgba(125,31,44," + (0.7 * fl * edge(rim)).toFixed(3) + ")";
        ctx.lineWidth = 2 * dpr;
        ctx.beginPath(); ctx.arc(scale, scale, rim * scale, 0, TAU); ctx.stroke();
      }
      var kn = Math.min(1, since / 0.8) * Math.max(0, 1 - (since - 1.2) / 3.2) * G;
      if (kn > 0) {                                       // the kilonova afterglow
        glow(0, 0, 0.12 + 0.42 * Math.min(1, since / 3), [[0, "rgba(255,226,170," + (0.75 * kn).toFixed(3) + ")"], [0.45, "rgba(240,170,110," + (0.35 * kn).toFixed(3) + ")"], [1, "rgba(200,90,80,0)"]]);
      }
      var jet = Math.min(1, since / 0.35) * Math.max(0, 1 - (since - 0.5) / 2.2) * G;
      if (jet > 0) {                                      // two thin polar jets
        ctx.save();
        ctx.translate(scale, scale);
        ctx.rotate(-0.35);
        for (var d = -1; d <= 1; d += 2) {
          var len = 0.78 * Math.min(1, since / 0.6) * scale * d;
          for (var l = 0; l < 3; l++) {
            var wid = [0.006, 0.016, 0.03][l] * scale, aj = [0.6, 0.22, 0.08][l] * jet;
            var g = ctx.createLinearGradient(0, 0, 0, len);
            g.addColorStop(0, "rgba(29,53,87," + aj.toFixed(3) + ")");
            g.addColorStop(0.65, "rgba(29,53,87," + (aj * 0.3).toFixed(3) + ")");
            g.addColorStop(1, "rgba(29,53,87,0)");
            ctx.fillStyle = g;
            ctx.beginPath();
            ctx.moveTo(-wid * 0.3, 0); ctx.lineTo(wid * 0.3, 0); ctx.lineTo(wid, len); ctx.lineTo(-wid, len);
            ctx.closePath(); ctx.fill();
          }
        }
        ctx.restore();
      }
      var rem = Math.max(0, 1 - since / 4.5) * G;         // the black hole left behind
      glow(0, 0, 0.045, [[0, "rgba(16,18,22," + rem.toFixed(3) + ")"], [0.6, "rgba(16,18,22," + (0.8 * rem).toFixed(3) + ")"], [1, "rgba(16,18,22,0)"]]);
    }

    ctx.globalAlpha = G;
    drawWave();                            // the gravitational-wave graph underneath
    ctx.globalAlpha = 1;
  }

  // ---------------------------------------------------------------- loop
  function frame(ms) {
    if (!running) return;
    var dt = Math.min((ms - last) / 1000, 1 / 30);
    last = ms;
    step(dt);
    draw(ms / 1000);
    requestAnimationFrame(frame);
  }
  function start() {
    if (running || reduce || !onScreen || document.hidden) return;
    running = true;
    last = performance.now();
    requestAnimationFrame(frame);
  }
  function stop() { running = false; }
  function still() {                // one frame shortly before the collision
    reset();
    while (t < MERGER.inspiral - 0.7) step(1 / 30);
    draw();
  }

  makeSprites();
  makeDots();
  resize();
  if (reduce) still(); else { reset(); draw(); start(); }

  var resizeTimer = null;
  window.addEventListener("resize", function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function () {
      if (!resize()) return;              // only when the width really changed
      if (reduce) still(); else draw();
    }, 150);
  });
  document.addEventListener("visibilitychange", function () { if (document.hidden) stop(); else start(); });
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (e) {
      onScreen = e[0].isIntersecting;
      if (onScreen) start(); else stop();
    }).observe(box);
  }
})();