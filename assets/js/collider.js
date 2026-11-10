/* HEP@IITK — Home page animation: a collider event display.
   A detector seen end-on (beam pipe, silicon tracker, calorimeters, magnet,
   muon chambers). Collision after collision, charged tracks curl out in the
   magnetic field, calorimeter towers light up and muons reach the outer
   chambers. Underneath, a histogram of the two-photon mass fills up with
   recorded collisions, and a bump appears on top of the falling background —
   the way a new particle shows itself. Some of the events shown are the
   "interesting" ones (two photons, or four muons) whose entry lands in the bump.
   Drawn on the <canvas> inside <div class="merger"> (HERO_ART in build_all.py).
   Plain JavaScript, no libraries. Light enough for phones: a few dozen lines
   and shapes per frame, and the detector itself is drawn only once. Pauses when
   off screen; visitors who prefer reduced motion see one still frame.

   Things you can tune: */
var COLLIDER = {
  event: 2.6,        // seconds per collision shown in the detector
  rate: 22,          // other recorded collisions dropping into the histogram, per second
  fill: 26,          // seconds for the histogram to fill before it starts again
  signal: 0.12,      // fraction of recorded collisions that come from the "new particle"
  special: 0.4       // fraction of the events shown that are signal candidates
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
  var INK = "16,18,22", NAVY = "29,53,87", MAROON = "125,31,44", GOLD = "214,150,58", WARM = "246,197,107";
  // one colour per kind of particle, as in a real event display
  var COL = {
    plus: "184,72,88",     // positive soft tracks: rose
    minus: "52,86,140",    // negative soft tracks: blue
    jet: "205,128,30",     // tracks inside a jet: amber
    e: "28,124,118",       // electrons: teal
    mu: "125,31,44",       // muons: maroon
    photon: "226,150,24",  // photons: orange-gold, dashed
    ecal: "214,150,58",    // electromagnetic calorimeter: gold
    hcal: "58,98,160"      // hadronic calorimeter: blue
  };

  // geometry, in units of the drawing's half-width (centre of canvas = 0,0)
  // the detector and the histogram together are centred in the soft sky disc
  var CY = -0.2;                                    // centre of the detector
  var K = 1.08;                                     // overall size of the detector
  var R = { pipe: 0.022 * K, trk: [0.05, 0.08, 0.11, 0.145, 0.18, 0.215].map(function (r) { return r * K; }),
            trkEnd: 0.235 * K, ecal: [0.25 * K, 0.29 * K], hcal: [0.305 * K, 0.385 * K],
            coil: [0.4 * K, 0.415 * K], mu: [[0.43 * K, 0.46 * K], [0.48 * K, 0.51 * K], [0.53 * K, 0.56 * K]] };
  var NE = 60, NH = 36, NMU = 12;                   // calorimeter cells and muon sectors
  var H = { x0: -0.52, x1: 0.52, y: 0.74, h: 0.25, bins: 24, peak: 10, full: 74, slope: 7 };

  var ZOOM = 1.1;                                   // >1 makes the drawing fill more of its square
  var size = 0, scale = 0, mid = 0, dpr = 1;
  var ev = null, evT = 0, bins = [], total = 0, rain = [], owed = 0, hT = 0, hFade = 1;
  var running = false, onScreen = true, last = 0;

  function rand(a, b) { return a + Math.random() * (b - a); }
  function X(x) { return mid + x * scale; }
  function Y(y) { return mid + y * scale; }
  function ease(x) { x = Math.min(Math.max(x, 0), 1); return 1 - Math.pow(1 - x, 3); }
  function rgba(c, a) { return "rgba(" + c + "," + Math.max(0, Math.min(1, a)).toFixed(3) + ")"; }
  function gauss() { return Math.sqrt(-2 * Math.log(Math.random() + 1e-9)) * Math.cos(TAU * Math.random()); }

  // ---------------------------------------------------------------- the histogram
  // falling background (exponential) plus a narrow bump at bin H.peak
  function bgBin() {
    var k;
    do { k = Math.floor(-H.slope * Math.log(Math.random() + 1e-9)); } while (k >= H.bins);
    return k;
  }
  function sigBin() {
    var k = Math.round(H.peak + 0.8 * gauss());
    return Math.min(H.bins - 1, Math.max(0, k));
  }
  function expected(k) {               // background expected in bin k, for the entries so far
    var norm = total * (1 - COLLIDER.signal) * (1 - Math.exp(-1 / H.slope)) / (1 - Math.exp(-H.bins / H.slope));
    return norm * Math.exp(-k / H.slope);
  }
  // text size: full size on a desktop-sized drawing, a little smaller on phones
  function font(px) {
    var f = Math.max(0.78, Math.min(1, scale / dpr / 230));
    return "italic " + Math.round(px * f * dpr) + "px Georgia, 'Times New Roman', serif";
  }
  function binX(k) { return H.x0 + (H.x1 - H.x0) * (k + 0.5) / H.bins; }
  function resetHist() { bins = []; for (var i = 0; i < H.bins; i++) bins.push({ n: 0, shown: 0 }); total = 0; hT = 0; rain = []; }

  // ---------------------------------------------------------------- one collision
  // a charged track is a circle through the collision point (the magnetic field
  // bends it); q = charge, rc = radius of curvature (∝ momentum), phi = direction
  function track(phi, rc, q, kind) {
    var cx = rc * Math.cos(phi + q * Math.PI / 2), cy = rc * Math.sin(phi + q * Math.PI / 2);
    var a0 = phi - q * Math.PI / 2;
    var reach = kind === "mu" ? R.coil[0] : R.trkEnd;
    var s = reach <= 2 * rc ? 2 * rc * Math.asin(reach / (2 * rc)) : TAU * rc * 0.97;  // low momentum: it loops
    var exitA = a0 + q * s / rc;
    var ex = cx + rc * Math.cos(exitA), ey = cy + rc * Math.sin(exitA);
    return { cx: cx, cy: cy, rc: rc, q: q, a0: a0, s: s, kind: kind, phi: phi,
             ex: ex, ey: ey, dir: exitA + q * Math.PI / 2, loops: reach > 2 * rc,
             at: Math.atan2(ey, ex), delay: rand(0, 0.08) };
  }

  function newEvent() {
    var e = { tracks: [], photons: [], jets: [], ecal: {}, hcal: {}, mu: {}, kind: "bg", entry: null };
    var r = Math.random();
    if (r < COLLIDER.special / 2) e.kind = "gg"; else if (r < COLLIDER.special) e.kind = "4mu";

    // the soft spray every collision has
    var nSoft = Math.round(rand(7, 13));
    for (var i = 0; i < nSoft; i++) {
      var tr = track(rand(0, TAU), rand(0.08, 0.7) * K, Math.random() < 0.5 ? 1 : -1, "h");
      e.tracks.push(tr);
      if (!tr.loops) deposit(e, tr.at, rand(0.15, 0.45), rand(0.2, 0.6));
    }
    // a jet: a narrow spray of stiff tracks and a big hadronic deposit
    if (e.kind === "bg" || Math.random() < 0.4) {
      var jphi = rand(0, TAU), n = Math.round(rand(3, 6));
      for (var j = 0; j < n; j++) {
        var tj = track(jphi + rand(-0.16, 0.16), rand(0.8, 3) * K, Math.random() < 0.5 ? 1 : -1, "jet");
        e.tracks.push(tj);
        deposit(e, tj.at, rand(0.3, 0.6), rand(0.6, 1));
      }
      e.jets.push({ phi: jphi });
    }
    // now and then an electron: a stiff track that stops in a big electromagnetic tower
    if (Math.random() < 0.5) {
      var te = track(rand(0, TAU), rand(0.7, 2) * K, Math.random() < 0.5 ? 1 : -1, "e");
      e.tracks.push(te);
      deposit(e, te.at, 0.85, 0.05, true);
    }
    if (e.kind === "gg") {                         // two photons: no track, a big electromagnetic tower
      var p0 = rand(0, TAU), p1 = p0 + Math.PI + rand(-0.5, 0.5);
      [p0, p1].forEach(function (p) { e.photons.push({ phi: p }); deposit(e, p, 1, 0.08, true); });
    }
    if (e.kind === "4mu") {                         // four muons: stiff tracks right out to the muon chambers
      for (var m = 0; m < 4; m++) {
        var tm = track(rand(0, TAU), rand(0.7, 2.2) * K, m % 2 ? 1 : -1, "mu");
        e.tracks.push(tm);
        deposit(e, tm.at, 0.12, 0.12);
      }
    }
    // where this collision lands in the histogram
    e.entry = { bin: e.kind === "bg" ? bgBin() : sigBin(), sent: false };
    return e;
  }

  function deposit(e, phi, emE, hadE, onlyEcal) {
    var a = (phi % TAU + TAU) % TAU;
    var ke = Math.floor(a / TAU * NE), kh = Math.floor(a / TAU * NH);
    e.ecal[ke] = Math.min(1, (e.ecal[ke] || 0) + emE);
    if (!onlyEcal) e.hcal[kh] = Math.min(1, (e.hcal[kh] || 0) + hadE);
  }

  // ---------------------------------------------------------------- static picture
  // the soft sky disc, the detector and the histogram axes never move: they are
  // painted once and shown as the canvas's background picture
  function ring(g, r0, r1, a0, a1) {
    g.beginPath();
    g.arc(X(0), Y(CY), r1 * scale, a0, a1);
    g.arc(X(0), Y(CY), r0 * scale, a1, a0, true);
    g.closePath();
  }
  function makeBackground() {
    var bg = document.createElement("canvas");
    bg.width = bg.height = size;
    var g = bg.getContext("2d");
    // a soft round halo centred on the detector (not on the canvas), so the
    // detector's rings and the halo share one centre; it fades out well inside
    // the canvas, and the histogram sits on the plain page below it
    var hr = Math.min(R.mu[2][1] + 0.18, 0.98 / ZOOM + CY) * scale;
    var gr = g.createRadialGradient(X(0), Y(CY), 0, X(0), Y(CY), hr);
    [[0, 255, 255, 255, 0.9], [0.55, 248, 246, 239, 0.8], [0.72, 239, 235, 225, 0.7],
     [0.82, 232, 227, 214, 0.55], [0.9, 229, 223, 208, 0.3], [0.96, 229, 223, 208, 0.1],
     [1, 229, 223, 208, 0]].forEach(function (c) {
      gr.addColorStop(c[0], "rgba(" + c[1] + "," + c[2] + "," + c[3] + "," + c[4] + ")");
    });
    g.fillStyle = gr; g.fillRect(0, 0, size, size);

    var line = "rgba(150,140,118,";
    g.lineWidth = 1 * dpr;
    // muon chambers: twelve sectors, three stations each
    for (var k = 0; k < NMU; k++) {
      var a0 = TAU * k / NMU + 0.05, a1 = TAU * (k + 1) / NMU - 0.05;
      for (var st = 0; st < 3; st++) {
        ring(g, R.mu[st][0], R.mu[st][1], a0, a1);
        g.fillStyle = "rgba(29,53,87,0.05)"; g.fill();
        g.strokeStyle = line + "0.45)"; g.stroke();
      }
    }
    // the magnet
    ring(g, R.coil[0], R.coil[1], 0, TAU);
    g.fillStyle = "rgba(150,140,118,0.22)"; g.fill();
    // hadronic and electromagnetic calorimeters, divided into cells
    ring(g, R.hcal[0], R.hcal[1], 0, TAU); g.fillStyle = "rgba(125,31,44,0.04)"; g.fill();
    ring(g, R.ecal[0], R.ecal[1], 0, TAU); g.fillStyle = "rgba(214,150,58,0.06)"; g.fill();
    g.strokeStyle = line + "0.32)";
    [R.hcal, R.ecal].forEach(function (rr, idx) {
      var n = idx ? NE : NH;
      g.beginPath(); g.arc(X(0), Y(CY), rr[0] * scale, 0, TAU); g.stroke();
      g.beginPath(); g.arc(X(0), Y(CY), rr[1] * scale, 0, TAU); g.stroke();
      g.beginPath();
      for (var c = 0; c < n; c++) {
        var a = TAU * c / n;
        g.moveTo(X(rr[0] * Math.cos(a)), Y(CY + rr[0] * Math.sin(a)));
        g.lineTo(X(rr[1] * Math.cos(a)), Y(CY + rr[1] * Math.sin(a)));
      }
      g.strokeStyle = line + "0.18)"; g.stroke();
      g.strokeStyle = line + "0.32)";
    });
    // silicon tracker layers and the beam pipe
    g.setLineDash([2 * dpr, 3 * dpr]);
    g.strokeStyle = line + "0.3)";
    R.trk.forEach(function (r) { g.beginPath(); g.arc(X(0), Y(CY), r * scale, 0, TAU); g.stroke(); });
    g.setLineDash([]);
    g.strokeStyle = line + "0.6)";
    g.beginPath(); g.arc(X(0), Y(CY), R.pipe * scale, 0, TAU); g.stroke();

    // histogram axes, a tick under every fifth bin, and its labels
    g.strokeStyle = "rgba(16,18,22,0.45)";
    g.lineWidth = 1.2 * dpr;
    g.beginPath();
    g.moveTo(X(H.x0), Y(H.y - H.h)); g.lineTo(X(H.x0), Y(H.y)); g.lineTo(X(H.x1), Y(H.y));
    for (var b = 0; b <= H.bins; b += 5) {
      var x = X(H.x0 + (H.x1 - H.x0) * b / H.bins);
      g.moveTo(x, Y(H.y)); g.lineTo(x, Y(H.y) + 4 * dpr);
    }
    g.stroke();
    g.fillStyle = "rgba(16,18,22,0.55)";
    g.font = font(11);
    g.textAlign = "right";
    g.fillText("mass of the photon pair →", X(H.x1), Y(H.y) + 17 * dpr);
    g.textAlign = "left";
    g.save();
    g.translate(X(H.x0) - 7 * dpr, Y(H.y));
    g.rotate(-Math.PI / 2);
    g.fillText("events", 0, 0);
    g.restore();

    canvas.style.background = "url(" + bg.toDataURL() + ") center / 100% 100% no-repeat";
  }

  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    var w = box.getBoundingClientRect().width || 420;
    var newSize = Math.round(w * dpr);
    if (newSize === size) return false;    // phones fire "resize" while scrolling; nothing changed
    size = newSize;
    canvas.width = canvas.height = size;
    mid = size / 2;
    scale = mid * ZOOM;
    makeBackground();
    return true;
  }

  // ---------------------------------------------------------------- update
  function step(dt) {
    // the event in the detector
    evT += dt;
    if (!ev || evT >= COLLIDER.event) { ev = newEvent(); evT = 0; }
    if (!ev.entry.sent && evT > 0.85) {
      ev.entry.sent = true;
      rain.push({ bin: ev.entry.bin, t: 0, big: true, sig: ev.kind !== "bg" });
    }

    // the histogram: other recorded collisions keep dropping in
    hT += dt;
    if (hT > COLLIDER.fill) {
      hFade = Math.max(0, hFade - dt / 0.8);
      if (hFade === 0) { resetHist(); hFade = 1; }
    } else {
      owed += COLLIDER.rate * dt;
      while (owed >= 1) {
        owed -= 1;
        rain.push({ bin: Math.random() < COLLIDER.signal ? sigBin() : bgBin(), t: 0, big: false });
      }
    }
    for (var i = rain.length - 1; i >= 0; i--) {
      var d = rain[i];
      d.t += dt / (d.big ? 0.9 : 0.55);
      if (d.t >= 1) { bins[d.bin].n += 1; total += 1; if (d.big) bins[d.bin].flash = 1; rain.splice(i, 1); }
    }
    for (var k = 0; k < bins.length; k++) {
      var b = bins[k];
      b.shown += (b.n - b.shown) * Math.min(1, dt * 8);
      if (b.flash) b.flash = Math.max(0, b.flash - dt / 0.8);
    }
  }

  // ---------------------------------------------------------------- drawing
  function drawEvent() {
    var e = ev, t = evT;
    var fade = 1 - Math.max(0, (t - (COLLIDER.event - 0.7)) / 0.7);
    if (fade <= 0) return;
    var ox = X(0), oy = Y(CY);

    // the collision: a quick flash at the centre
    if (t < 0.35) {
      var f = 1 - t / 0.35;
      var g = ctx.createRadialGradient(ox, oy, 0, ox, oy, 0.08 * scale);
      g.addColorStop(0, rgba("255,236,190", 0.95 * f));
      g.addColorStop(1, rgba(WARM, 0));
      ctx.fillStyle = g;
      ctx.beginPath(); ctx.arc(ox, oy, 0.08 * scale, 0, TAU); ctx.fill();
    }

    // calorimeter towers grow outwards once the particles arrive
    var grow = ease((t - 0.35) / 0.4) * fade;
    if (grow > 0) {
      var kk, a0, a1, h;
      for (kk in e.ecal) {
        a0 = TAU * kk / NE; a1 = TAU * (+kk + 1) / NE;
        h = (0.012 + 0.11 * e.ecal[kk] * grow) * K;
        ctx.beginPath();
        ctx.arc(ox, oy, (R.ecal[0] + h) * scale, a0, a1);
        ctx.arc(ox, oy, R.ecal[0] * scale, a1, a0, true);
        ctx.closePath();
        ctx.fillStyle = rgba(COL.ecal, (0.25 + 0.6 * e.ecal[kk]) * grow);
        ctx.fill();
      }
      for (kk in e.hcal) {
        a0 = TAU * kk / NH; a1 = TAU * (+kk + 1) / NH;
        h = (0.01 + 0.08 * e.hcal[kk] * grow) * K;
        ctx.beginPath();
        ctx.arc(ox, oy, (R.hcal[0] + h) * scale, a0, a1);
        ctx.arc(ox, oy, R.hcal[0] * scale, a1, a0, true);
        ctx.closePath();
        ctx.fillStyle = rgba(COL.hcal, (0.14 + 0.4 * e.hcal[kk]) * grow);
        ctx.fill();
      }
    }

    // jets: a faint amber cone round each spray of tracks
    for (var jj = 0; jj < e.jets.length; jj++) {
      var jg = ease((t - 0.1) / 0.4) * fade;
      if (jg <= 0) continue;
      var jp = e.jets[jj].phi, jr = R.ecal[0] * scale;
      var cg = ctx.createRadialGradient(ox, oy, 0, ox, oy, jr);
      cg.addColorStop(0, rgba(COL.jet, 0));
      cg.addColorStop(1, rgba(COL.jet, 0.22 * jg));
      ctx.fillStyle = cg;
      ctx.beginPath(); ctx.moveTo(ox, oy); ctx.arc(ox, oy, jr, jp - 0.24, jp + 0.24); ctx.closePath(); ctx.fill();
    }

    // charged tracks curl outwards in the magnetic field
    ctx.lineCap = "round";
    for (var i = 0; i < e.tracks.length; i++) {
      var tr = e.tracks[i];
      var p = ease((t - 0.05 - tr.delay) / 0.45);
      if (p <= 0) continue;
      var isMu = tr.kind === "mu";
      var tc = isMu ? COL.mu : tr.kind === "jet" ? COL.jet : tr.kind === "e" ? COL.e : tr.q > 0 ? COL.plus : COL.minus;
      ctx.strokeStyle = rgba(tc, (tr.kind === "h" ? 0.8 : 0.95) * fade);
      ctx.lineWidth = (isMu ? 2.4 : tr.kind === "h" ? 1.4 : 1.9) * dpr;
      ctx.beginPath();
      ctx.arc(X(tr.cx), Y(CY + tr.cy), tr.rc * scale, tr.a0, tr.a0 + tr.q * tr.s * p / tr.rc, tr.q < 0);
      ctx.stroke();
      // muons carry on through the magnet into the chambers, bending the other way
      if (isMu) {
        var pm = ease((t - 0.45 - tr.delay) / 0.35);
        if (pm > 0) {
          // straight on from where it leaves the magnet to the outer edge of the chambers
          var dx = Math.cos(tr.dir), dy = Math.sin(tr.dir), rt = R.mu[2][1] + 0.006;
          var ed = tr.ex * dx + tr.ey * dy;
          var len = (-ed + Math.sqrt(Math.max(0, ed * ed - (tr.ex * tr.ex + tr.ey * tr.ey) + rt * rt))) * pm;
          var bx = tr.ex + len * Math.cos(tr.dir), by = tr.ey + len * Math.sin(tr.dir);
          var ux = Math.cos(tr.at), uy = Math.sin(tr.at);
          var mx = (tr.ex + bx) / 2 - tr.q * 0.03 * uy * pm, my = (tr.ey + by) / 2 + tr.q * 0.03 * ux * pm;
          ctx.beginPath();
          ctx.moveTo(X(tr.ex), Y(CY + tr.ey));
          ctx.quadraticCurveTo(X(mx), Y(CY + my), X(bx), Y(CY + by));
          ctx.stroke();
          // light up the muon chamber sector it crosses
          var sec = Math.floor(((Math.atan2(by, bx) % TAU + TAU) % TAU) / TAU * NMU);
          var sa0 = TAU * sec / NMU + 0.05, sa1 = TAU * (sec + 1) / NMU - 0.05;
          for (var st = 0; st < 3; st++) {
            if (Math.hypot(bx, by) < R.mu[st][0]) break;
            ctx.beginPath();
            ctx.arc(ox, oy, R.mu[st][1] * scale, sa0, sa1);
            ctx.arc(ox, oy, R.mu[st][0] * scale, sa1, sa0, true);
            ctx.closePath();
            ctx.fillStyle = rgba(MAROON, 0.3 * fade);
            ctx.fill();
          }
        }
      }
    }

    // photons leave no track: dashed lines straight to their towers
    if (e.photons.length) {
      var pp = ease((t - 0.05) / 0.35);
      ctx.strokeStyle = rgba(COL.photon, 0.95 * fade);
      ctx.lineWidth = 1.8 * dpr;
      ctx.setLineDash([5 * dpr, 4 * dpr]);
      ctx.beginPath();
      e.photons.forEach(function (ph) {
        ctx.moveTo(ox, oy);
        ctx.lineTo(ox + R.ecal[0] * pp * scale * Math.cos(ph.phi), oy + R.ecal[0] * pp * scale * Math.sin(ph.phi));
      });
      ctx.stroke();
      ctx.setLineDash([]);
    }

    // a small label for the interesting events
    if (e.kind !== "bg") {
      var la = Math.min(1, Math.max(0, (t - 0.5) / 0.25)) * fade;
      if (la > 0) {
        ctx.fillStyle = rgba(MAROON, la);
        ctx.font = font(13);
        ctx.textAlign = "center";
        ctx.fillText(e.kind === "gg" ? "γγ candidate" : "4μ candidate", ox, Y(CY - R.mu[2][1] - 0.035));
      }
    }
  }

  function drawHistogram() {
    var w = (H.x1 - H.x0) / H.bins;
    ctx.globalAlpha = hFade;
    // the bars
    for (var k = 0; k < bins.length; k++) {
      var b = bins[k];
      if (b.shown < 0.05) continue;
      var hgt = Math.min(1, b.shown / H.full) * H.h;
      var x = X(H.x0 + w * k) + 0.6 * dpr, bw = w * scale - 1.2 * dpr;
      var near = Math.abs(k - H.peak) <= 1;
      ctx.fillStyle = near ? "rgba(125,31,44,0.26)" : "rgba(29,53,87,0.16)";
      ctx.fillRect(x, Y(H.y - hgt), bw, hgt * scale);
      ctx.fillStyle = near ? "rgba(125,31,44,0.85)" : "rgba(29,53,87,0.7)";
      ctx.fillRect(x, Y(H.y - hgt), bw, 1.6 * dpr);
      if (b.flash) {
        ctx.fillStyle = rgba(WARM, 0.8 * b.flash);
        ctx.fillRect(x, Y(H.y - hgt), bw, hgt * scale);
      }
    }
    // the expected background without the new particle, as a dashed curve
    if (total > 40) {
      ctx.strokeStyle = "rgba(16,18,22,0.5)";
      ctx.lineWidth = 1.2 * dpr;
      ctx.setLineDash([4 * dpr, 4 * dpr]);
      ctx.beginPath();
      for (var j = 0; j <= 60; j++) {
        var kb = (H.bins - 0.5) * j / 60;
        var yv = Math.min(1, expected(kb) / H.full) * H.h;
        var px = X(H.x0 + w * (kb + 0.5)), py = Y(H.y - yv);
        if (j === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
      }
      ctx.stroke();
      ctx.setLineDash([]);
    }
    // the bump gets a label once it stands out
    var pk = bins[H.peak] ? bins[H.peak].shown : 0;
    var excess = pk - expected(H.peak);
    if (total > 120 && excess > 10) {
      var la = Math.min(1, (excess - 10) / 8);
      // sit above the tallest bar the label spans, and stay inside the histogram
      ctx.font = font(12);
      var tw = ctx.measureText("a new particle?").width / scale;
      var cx = Math.min(Math.max(binX(H.peak), H.x0 + tw / 2 + 0.02), H.x1 - tw / 2);
      var top = 0;
      for (var kb2 = 0; kb2 < bins.length; kb2++) {
        var bl = H.x0 + w * kb2, br = bl + w;
        if (br > cx - tw / 2 && bl < cx + tw / 2) top = Math.max(top, Math.min(1, bins[kb2].shown / H.full) * H.h);
      }
      ctx.fillStyle = rgba(MAROON, la);
      ctx.textAlign = "center";
      ctx.fillText("a new particle?", X(cx), Y(H.y - top) - 7 * dpr);
    }
    ctx.globalAlpha = 1;
  }

  function drawRain() {
    for (var i = 0; i < rain.length; i++) {
      var d = rain[i], f = ease(d.t);
      var bx = binX(d.bin);
      var topY = H.y - Math.min(1, (bins[d.bin].shown) / H.full) * H.h;
      var x, y;
      if (d.big) {                         // the event just shown: flies from the detector into its bin
        var sx = 0, sy = CY;
        x = sx + (bx - sx) * f;
        y = sy + (topY - sy) * f - 0.12 * Math.sin(Math.PI * f);
        ctx.fillStyle = d.sig ? "rgba(125,31,44,0.95)" : "rgba(29,53,87,0.9)";
        ctx.beginPath(); ctx.arc(X(x), Y(y), 3.4 * dpr, 0, TAU); ctx.fill();
      } else {                             // other recorded collisions: tiny drops into the bins
        x = bx;
        y = (H.y - H.h - 0.06) + (topY - (H.y - H.h - 0.06)) * f * f;
        ctx.fillStyle = rgba(NAVY, 0.5 * (1 - f * 0.4) * hFade);
        ctx.beginPath(); ctx.arc(X(x), Y(y), 1.3 * dpr, 0, TAU); ctx.fill();
      }
    }
  }

  function draw() {
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.globalAlpha = 1;
    ctx.clearRect(0, 0, size, size);
    if (ev) drawEvent();
    drawHistogram();
    drawRain();
  }

  // ---------------------------------------------------------------- loop
  function frame(ms) {
    if (!running) return;
    var dt = Math.min((ms - last) / 1000, 1 / 30);
    last = ms;
    step(dt);
    draw();
    requestAnimationFrame(frame);
  }
  function start() {
    if (running || reduce || !onScreen || document.hidden) return;
    running = true;
    last = performance.now();
    requestAnimationFrame(frame);
  }
  function stop() { running = false; }
  function still() {                       // a full histogram and a two-photon event, frozen
    resetHist();
    for (var i = 0; i < COLLIDER.rate * COLLIDER.fill * 0.9; i++) {
      bins[Math.random() < COLLIDER.signal ? sigBin() : bgBin()].n += 1; total += 1;
    }
    bins.forEach(function (b) { b.shown = b.n; });
    do { ev = newEvent(); } while (ev.kind !== "gg");
    evT = 1.2;
    rain = [];
    draw();
  }

  resetHist();
  resize();
  if (reduce) still(); else { draw(); start(); }

  var resizeTimer = null;
  window.addEventListener("resize", function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function () {
      if (!resize()) return;               // only when the width really changed
      draw();
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