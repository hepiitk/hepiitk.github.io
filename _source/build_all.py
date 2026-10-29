#!/usr/bin/env python3
"""
build_all.py — rebuilds the WHOLE site, and holds everything shared.

    python3 _source/build_all.py

The site is made by five files in _source/:

  build_members.py      members.html      (+ index.html)   people and photos
  build_news.py         news.html         (+ index.html)   news, PMRF, positions
  build_conferences.py  conferences.html  (+ index.html)   symposia and meetings
  build_research.py           research.html     (+ index.html)   research areas and figures
  build_all.py          this file: the parts every page shares, plus the pages
                        that rarely change — Home, Seminars, Contact.
                        Running it rebuilds all seven pages.

Sections of this file:
  1. Site-wide settings  — site name, EMAIL, PHONE, the menu (NAV)
  2. Icons and drawings
  3. Helpers used by every page  (head, header, footer, img, ...)
  4. Home page          — build_index()
  5. Research page      — now in build_research.py
  6. Seminars page      — build_seminars()
  7. Contact page       — EDITORS, build_contact()
  8. Build everything

After changing ANYTHING in this file, run it:  python3 _source/build_all.py

To download any missing research figures (see build_research.py) and then
rebuild everything:                            python3 _source/build_all.py --figures
"""

import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)  # so the page files can be imported from anywhere


# ==========================================================================
# 1. SITE-WIDE SETTINGS  (header / footer of every page)
# ==========================================================================

SITE_NAME = "High Energy Physics @ IIT Kanpur"
SITE_SHORT = "HEP@IITK"
EMAIL = "hepiitk@gmail.com"
PHONE = "+91 512 259 7641"

NAV = [
    ("index.html", "Home"),
    ("members.html", "Members"),
    ("research.html", "Research"),
    ("seminars.html", "Seminars"),
    ("conferences.html", "Conference / Workshop"),
    ("news.html", "News"),
    ("contact.html", "Contact"),
]


# ==========================================================================
# 2. ICONS AND DRAWINGS  (inline SVG, currentColor)
# ==========================================================================

ICON = {
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "external": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 4h6v6M20 4l-8 8M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>',
    "doc": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 3H7a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1V7z"/><path d="M14 3v4h4M9 13h6M9 17h4"/></svg>',
    "globe": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 2.5 15.4 0 18M12 3c-2.5 2.6-2.5 15.4 0 18"/></svg>',
    "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    "atom": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="2.2"/><ellipse cx="12" cy="12" rx="10" ry="4.4"/><ellipse cx="12" cy="12" rx="10" ry="4.4" transform="rotate(60 12 12)"/><ellipse cx="12" cy="12" rx="10" ry="4.4" transform="rotate(120 12 12)"/></svg>',
    "detector": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3.6"/><path d="M12 3v3.4M12 17.6V21M3 12h3.4M17.6 12H21M5.6 5.6l2.4 2.4M16 16l2.4 2.4M18.4 5.6 16 8M8 16l-2.4 2.4"/></svg>',
    "string": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M3 17c3.5 0 3.5-10 7-10s3.5 10 7 10 4-3 4-3"/><path d="M3 7c1.8 0 2.6 2.6 3.6 5"/><circle cx="12" cy="12" r="0.9" fill="currentColor" stroke="none"/></svg>',
    "calendar": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/></svg>',
    "users": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="8" r="3.4"/><path d="M2.5 20c0-3.6 2.9-5.6 6.5-5.6s6.5 2 6.5 5.6"/><path d="M16.5 5.2a3.4 3.4 0 0 1 0 6.6M18 14.8c2.2.6 3.6 2.3 3.6 5.2"/></svg>',
    "arrow-left": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 18l-6-6 6-6"/></svg>',
    "arrow-right": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "pause": '<svg class="icon-pause" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><rect x="6.5" y="5" width="4" height="14" rx="1"/><rect x="13.5" y="5" width="4" height="14" rx="1"/></svg>',
    "play": '<svg class="icon-play" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13a1 1 0 0 0 1.5.86l10.5-6.5a1 1 0 0 0 0-1.72L9.5 4.64A1 1 0 0 0 8 5.5z"/></svg>',
    "news": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 5h12a1 1 0 0 1 1 1v13H5a1 1 0 0 1-1-1z"/><path d="M17 9h2a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1h-2M7 9h6M7 13h6M7 17h4"/></svg>',
}

# Home page animation: two neutron stars spiral together, collide and blow out
# a glowing kilonova cloud. Drawn by assets/merger.js on the <canvas> below;
# its styles are in assets/style.css (search for ".merger").
HERO_ART = """
<div class="merger" role="img" aria-label="Animation of two neutron stars spiralling together, colliding and blowing out a glowing cloud of debris">
  <canvas width="840" height="840" aria-hidden="true"></canvas>
</div>
"""

BRAND_MARK = """
<svg class="brand__mark" viewBox="0 0 40 40" aria-hidden="true">
  <circle cx="20" cy="20" r="18.4" fill="none" stroke="currentColor" stroke-width="0.9"/>
  <circle cx="20" cy="20" r="15.6" fill="none" stroke="currentColor" stroke-width="0.6" opacity=".5"/>
  <g fill="none" stroke="currentColor" stroke-width="1.1">
    <ellipse cx="20" cy="20" rx="16" ry="6.4"/>
    <ellipse cx="20" cy="20" rx="16" ry="6.4" transform="rotate(60 20 20)"/>
    <ellipse cx="20" cy="20" rx="16" ry="6.4" transform="rotate(120 20 20)"/>
  </g>
  <circle cx="20" cy="20" r="3" fill="currentColor"/>
</svg>
"""


# ==========================================================================
# 2b. IMAGES
# ==========================================================================

# Every image path is relative to the assets/ folder, e.g. "Members/<file>.webp"
# means assets/Members/<file>.webp. A file that is missing simply hides
# itself on the page (no broken-image icon), so it is safe to add later.
# Remember: GitHub Pages is case-sensitive — "Photo.WEBP" is not "photo.webp".
IMG_DIR = "assets"

# Institute emblem in the masthead: copy either top-level .jpg from the old
# export to assets/iitk-logo.svg. Falls back to the drawn mark above.
LOGO = "iitk-logo.svg"

# Drawn artwork that ships with the site (assets/img/*.svg) — nothing to copy.
# These are line engravings made for this site, in the same ink/maroon palette.
ART = {
    "theory": ("img/theory.svg", "One-loop Feynman diagram with an exchanged boson"),
    "experiment": ("img/experiment.svg",
                   "Cylindrical collider detector with a beam line and two jet cones"),
    "string": ("img/string.svg",
               "Anti-de Sitter cylinder with a boundary theory and a geodesic through the bulk"),
    "seminar": ("img/seminar.svg", "Blackboard with an equation and a lectern"),
    "symposium": ("img/symposium.svg", "Auditorium with a projection screen and rows of seats"),
    "news": ("img/news.svg", "Noticeboard with pinned announcements"),
    "contact": ("img/contact.svg", "A letter travelling towards the department building"),
    "members": ("img/members.svg",
                "Group members talking round a table, with portraits on the wall behind them"),
    "research": ("img/research.svg",
                 "An open notebook under a desk lamp, with a Feynman diagram and a plot with a peak"),
}


# ==========================================================================
# 3. HELPERS USED BY EVERY PAGE
# ==========================================================================


def initials(name):
    parts = [p for p in re.split(r"\s+", name) if p]
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()


def ext(url, label, icon="external", cls="chip"):
    return (
        f'<a class="{cls}" href="{url}" target="_blank" rel="noopener">'
        f"{ICON[icon]}<span>{label}</span></a>"
    )


# Every <img> carries this handler: a file that 404s marks itself, and the CSS
# then hides the image — and for figures, banners and posters the whole block —
# instead of leaving a broken-image icon on the page.
ONERR = "onerror=\"this.setAttribute('data-failed','')\""


def img(path, alt="", cls="", eager=False):
    c = f' class="{cls}"' if cls else ""
    load = "eager" if eager else "lazy"
    return (
        f'<img{c} src="{IMG_DIR}/{path}" alt="{html.escape(alt, quote=True)}" '
        f'loading="{load}" decoding="async" {ONERR}>'
    )


def figure(path, title="", caption="", cls="figure"):
    cap = ""
    if title or caption:
        inner = (f"<b>{title}</b>" if title else "") + (caption or "")
        cap = f"<figcaption>{inner}</figcaption>"
    return f'<figure class="{cls}">{img(path, title or caption)}{cap}</figure>'


def sheet_embed(sheet_id, label, gid=None):
    src = f"https://docs.google.com/spreadsheets/d/{sheet_id}/htmlembed"
    if gid:
        src += f"?gid={gid}"
    open_url = f"https://drive.google.com/open?id={sheet_id}"
    return f"""      <div class="embed embed--sheet">
        <div class="embed__bar">
          <span>{label}</span>
          {ext(open_url, "Open in Drive", "external")}
        </div>
        <iframe src="{src}" title="{label}" loading="lazy"></iframe>
      </div>"""

def fold(show, hide, inner, open=False):
    """An open/close bar ("Show the calendar" / "Hide the calendar") with
    `inner` underneath. open=True starts it unfolded."""
    return f"""      <details class="fold" data-reveal{' open' if open else ''}>
        <summary><span class="fold__open">{show}</span><span class="fold__close">{hide}</span></summary>
{inner}
      </details>"""

def head(title, desc, page):
    full = f"{title} · {SITE_SHORT}" if page != "index.html" else f"{SITE_NAME}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#fbfaf6">
<meta property="og:title" content="{full}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
{header(page)}
<main id="main">"""


def header(page):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == page else ""
        items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    return f"""<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="index.html">
      <img class="brand__logo" src="{IMG_DIR}/{LOGO}" alt="" {ONERR}>
      {BRAND_MARK.strip()}
      <span class="brand__text">
        <span class="brand__title">High Energy Physics</span>
        <span class="brand__sub">Indian Institute of Technology Kanpur</span>
      </span>
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">
      <span class="visually-hidden">Menu</span>{ICON['menu']}
    </button>
    <nav class="nav" id="site-nav" aria-label="Primary" data-open="false">
      <ul>{''.join(items)}</ul>
    </nav>
  </div>
</header>"""


def footer():
    nav_links = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l in NAV[1:4])
    nav_links2 = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l in NAV[4:])
    return f"""</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <h2>{SITE_SHORT}</h2>
        <p class="dim" style="font-size:var(--step--1);max-width:34ch">
          Astroparticle physics, cosmology, particle theory and experiment, and string
          theory at the Department of Physics, Indian Institute of Technology Kanpur.
        </p>
      </div>
      <div>
        <h2>Group</h2>
        <ul>{nav_links}</ul>
      </div>
      <div>
        <h2>Activities</h2>
        <ul>{nav_links2}</ul>
      </div>
      <div>
        <h2>Reach us</h2>
        <ul>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><span class="dim">{PHONE}</span></li>
          <li><a href="https://www.iitk.ac.in/phy/" target="_blank" rel="noopener">Department of Physics</a></li>
          <li><a href="https://www.iitk.ac.in/" target="_blank" rel="noopener">IIT Kanpur</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> High Energy Physics Group, IIT Kanpur.</span>
      <span class="dim">Maintained by the group's editor team.</span>
    </div>
  </div>
</footer>
<script src="assets/app.js" defer></script>
</body>
</html>
"""


def page_head_band(title, desc, extra="", art=None):
    """The masthead at the top of every inner page.

    title / desc : heading and the sentence under it
    extra        : optional HTML placed under the sentence (the members search box)
    art          : optional key of ART above — draws that picture beside the heading
    """
    illus = ""
    if art:
        path, alt = ART[art]
        illus = f'      <figure class="page-head__illus">{img(path, alt, eager=True)}</figure>\n'
    inner = f"""      <div>
        <p class="eyebrow">{SITE_SHORT}</p>
        <h1>{title}</h1>
        <p>{desc}</p>
        {extra}
      </div>
{illus}"""
    grid_open, grid_close = ('    <div class="page-head__grid">\n', "    </div>\n") if illus else ("", "")
    if not illus:
        inner = inner.replace("      <div>\n", "").replace("\n      </div>\n", "\n")
    return f"""  <section class="page-head">
    <div class="wrap">
{grid_open}{inner}{grid_close}    </div>
  </section>
"""


def write(name, body):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    print("wrote", name, f"({len(body)//1024} KB)")


# ==========================================================================
# 4. HOME PAGE  (index.html)
# ==========================================================================
# Big photo in the Home page hero: (file inside assets/, credit line under it)
HERO_PHOTO = ("Home/e8e5c3c4d0f40b553317792526dc596a.jpg", "pic courtesy: CERN")


def build_index():
    """Home page. Counts, news and research areas come from the other files."""
    from build_members import FACULTY, POSTDOCS, STUDENTS, ALUMNI
    from build_news import NEWS
    from build_research import THRUSTS

    cards = []
    for t in THRUSTS:
        top = " · ".join(t["topics"][:4])
        art_path, art_alt = ART[t["art"]]
        cards.append(f"""      <a class="card card--link {t['accent']}" href="research.html#{t['id']}" data-reveal>
        <span class="card__art">{img(art_path, art_alt)}</span>
        <h3>{t['title']}</h3>
        <p>{t['blurb']}</p>
        <p class="card__topics">{top}</p>
        <p class="mt-4" style="color:var(--accent);font-weight:600">Explore the group's work →</p>
      </a>""")

    news_items = []
    for n in NEWS[:4]:
        link = ""
        if n["link"]:
            link = f'<p class="mt-0"><a href="{n["link"][0]}">{n["link"][1]} →</a></p>'
        news_items.append(f"""        <li data-reveal>
          <span class="meta">{n['tag']}</span>
          <h3>{n['title']}</h3>
          <p>{n['body']}</p>
          {link}
        </li>""")

    body = head(
        "Home",
        "The high energy physics group at IIT Kanpur works on astroparticle physics, "
        "cosmology, particle theory and experiment, and string theory.",
        "index.html",
    )
    body += f"""
  <section class="hero">
    <div class="wrap hero__grid">
      <div>
        <p class="eyebrow">Department of Physics · IIT Kanpur</p>
        <h1>From quarks to <em>colliding stars</em></h1>
        <div class="hero__rule"></div>
        <!-- <p class="lede dropcap">
          We are faculty, postdoctoral fellows and graduate students in the Department of
          Physics at IIT Kanpur. Our work spans particle theory, collider and neutrino
          experiments, and string theory — from the particles made at the LHC to dark
          matter, the early universe, black holes and the gravitational waves of merging
          stars — and many of our projects cross between them.
        </p>
        -->
        <p class="lede dropcap">
          We are faculty, postdoctoral fellows and graduate students in the Department of
          Physics at IIT Kanpur. Our work spans string theory, particle theory and particle
          experiments. We study holography, conformal field theories and the bootstrap, black
          holes and entanglement, physics beyond the Standard Model, dark matter, neutrinos
          and inflation, and take part in collider and neutrino experiments at the LHC and
          DUNE. Many of our projects cross between these areas.
        </p>
        <div class="cluster hero__actions">
          <a class="btn btn--primary" href="research.html">Research areas {ICON['arrow']}</a>
          <a class="btn btn--ghost" href="members.html">Meet the group</a>
        </div>
      </div>
      <figure class="hero__art">
        {img(HERO_PHOTO[0], "The group's research spans collider, neutrino and gravitational physics", eager=True)}
        {HERO_ART.strip()}
        <figcaption class="credit mt-4">{HERO_PHOTO[1]}</figcaption>
      </figure>
    </div>
  </section>

  <section class="section section--tight">
    <div class="wrap">
      <div class="stats" data-reveal>
        <div class="stat"><span class="stat__num" data-count="{len(FACULTY)}">{len(FACULTY)}</span><span class="stat__label">Faculty</span></div>
        <div class="stat"><span class="stat__num" data-count="{len(POSTDOCS)}">{len(POSTDOCS)}</span><span class="stat__label">Postdocs</span></div>
        <div class="stat"><span class="stat__num" data-count="{len(STUDENTS)}">{len(STUDENTS)}</span><span class="stat__label">Graduate students</span></div>
        <div class="stat"><span class="stat__num" data-count="{len(ALUMNI)}">{len(ALUMNI)}</span><span class="stat__label">Alumni</span></div>
        <div class="stat"><span class="stat__num">3</span><span class="stat__label">Subgroups</span></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section-head">
        <h2>What we work on</h2>
        <span class="section-head__aside">three overlapping subgroups</span>
      </div>
      <div class="grid grid--3">
{''.join(cards)}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="split">
        <div>
          <div class="section-head"><h2>Latest news</h2></div>
          <ul class="timeline">
{''.join(news_items)}
          </ul>
          <a class="btn btn--ghost mt-4" href="news.html">All news &amp; openings {ICON['arrow']}</a>
        </div>
        <div class="stack">
          <div class="card accent-maroon" data-reveal>
            <span class="card__icon">{ICON['calendar']}</span>
            <h3>Seminars &amp; journal clubs</h3>
            <p>A weekly HEP seminar, a particle journal club and a string journal club run
               through the semester. The group calendar has the current schedule.</p>
            <p class="mt-4"><a href="seminars.html">See the calendar →</a></p>
          </div>
          <div class="card accent-navy" data-reveal>
            <span class="card__icon">{ICON['users']}</span>
            <h3>Join us</h3>
            <p>We welcome postdoctoral applications in formal and string theory, particle
               phenomenology and experimental neutrino physics, and support INSPIRE and
               N-PDF applications.</p>
            <p class="mt-4"><a href="news.html#positions">Open positions →</a></p>
          </div>
          <div class="card accent-gold" data-reveal>
            <span class="card__icon">{ICON['news']}</span>
            <h3>In-house symposium</h3>
            <p>The group meets every year for a two-day in-house symposium where every
               subgroup presents its current work.</p>
            <p class="mt-4"><a href="conferences.html">Past &amp; upcoming meetings →</a></p>
          </div>
        </div>
      </div>
    </div>
  </section>
"""
    body += footer().replace(
        '<script src="assets/app.js" defer></script>',
        '<script src="assets/app.js" defer></script>\n<script src="assets/merger.js" defer></script>')
    write("index.html", body)


# ==========================================================================
# 5. RESEARCH PAGE  —  lives in build_research.py (THRUSTS, FIGURES, build())
# ==========================================================================


# ==========================================================================
# 6. SEMINARS PAGE  (seminars.html)  —  text and links are inside the function
# ==========================================================================


def build_seminars():
    """Seminars page. Seminars themselves come from the Google Calendar."""
    cal_src = (
        "https://calendar.google.com/calendar/embed?src=hepiitk%40gmail.com"
        "&ctz=Asia%2FKolkata&color=%239fe1e7&mode=AGENDA&showTitle=0&showPrint=0"
    )
    calendar = f"""      <div class="embed embed--calendar">
        <div class="embed__bar">
          <span>hepiitk@gmail.com</span>
          {ext("https://calendar.google.com/calendar/embed?src=hepiitk%40gmail.com&ctz=Asia%2FKolkata", "Open calendar", "external")}
        </div>
        <iframe src="{cal_src}" title="HEP@IITK seminar calendar" loading="lazy"></iframe>
      </div>"""
    roster = sheet_embed("1anX0qlXKS1CVkrHNJprBONlXY60kgFt8gxzGX6w_rms", "Journal_Club@IITK", "0")

    body = head(
        "Seminars",
        "HEP seminars, the particle journal club and the string journal club at IIT Kanpur.",
        "seminars.html",
    )
    body += page_head_band(
        "Seminars",
        "A weekly HEP seminar plus two journal clubs, one for particle physics and one for "
        "string theory. Everything runs on the group calendar below.",
        art="seminar",
    )
    body += f"""
  <div class="subnav">
    <div class="wrap">
      <ul>
        <li><a href="#hep-seminars">HEP seminars</a></li>
        <li><a href="#particle-jc">Particle journal club</a></li>
        <li><a href="#string-jc">String journal club</a></li>
      </ul>
    </div>
  </div>

  <section class="section section--tight" id="hep-seminars">
    <div class="wrap">
      <div class="section-head">
        <h2>HEP seminars</h2>
        <span class="section-head__aside">group calendar · Asia/Kolkata</span>
      </div>
{fold("Show the seminar calendar", "Hide the seminar calendar", calendar)}
      <p class="credit mt-4">
        Speakers and visitors are welcome — write to
        <a href="mailto:{EMAIL}">{EMAIL}</a> to be added to the seminar announcements.
      </p>
    </div>
  </section>

  <section class="section" id="particle-jc">
    <div class="wrap">
      <div class="section-head">
        <h2>Particle journal club</h2>
        <span class="section-head__aside">Journal_Club@IITK</span>
      </div>
      <p class="muted">A rotating journal club run by the particle theory and experiment
         subgroups. The sheet below carries the speaker roster and papers.</p>
{fold("Show the journal club roster", "Hide the journal club roster", roster, open=True)}
    </div>
  </section>

  <section class="section" id="string-jc">
    <div class="wrap">
      <div class="section-head"><h2>String journal club</h2></div>
      <div class="card accent-navy" style="max-width:34rem" data-reveal>
        <span class="card__icon">{ICON['string']}</span>
        <h3>Seminars &amp; events, string theory group</h3>
        <p>The string subgroup keeps its own schedule of journal club meetings, seminars
           and visitors.</p>
        <p class="mt-4">{ext("https://sites.google.com/view/st-iitk/seminars-events", "String group schedule", "external")}</p>
      </div>
    </div>
  </section>
"""
    body += footer()
    write("seminars.html", body)

# ==========================================================================
# 7. CONTACT PAGE  (contact.html)  —  edit EDITORS
# ==========================================================================
EDITORS = [
    ("Subrata Samanta", "samantaphy20@iitk.ac.in"),
    ("Atanu Samanta", "asamanta23@iitk.ac.in"),
    ("Debmalya Dey", "debmalyad23@iitk.ac.in"),
    ("Pushkar Soni", "pushkars21@iitk.ac.in"),
    ("Shibam Das", "shibamdas23@iitk.ac.in"),
]


def build_contact():
    """Contact page. E-mail and phone are EMAIL / PHONE in section 1."""
    eds = "".join(
        f"""        <div class="roster__item accent-maroon">
          <span class="roster__name">{n}</span>
          <a class="chip" href="mailto:{e}">{ICON['mail']}<span>{e}</span></a>
        </div>"""
        for n, e in EDITORS
    )
    body = head(
        "Contact",
        "How to reach the high energy physics group at IIT Kanpur.",
        "contact.html",
    )
    body += page_head_band(
        "Contact",
        "For seminars, visits, applications or corrections to this site, the group email "
        "reaches all of us.",
        art="contact",
    )
    body += f"""
  <section class="section section--tight">
    <div class="wrap">
      <div class="split split--even">
        <div data-reveal>
          <div class="section-head"><h2>The group</h2></div>
          <dl class="dl">
            <div>
              <dt>Email</dt>
              <dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
            </div>
            <div>
              <dt>Phone</dt>
              <dd>{PHONE} <span class="dim">(Physics Office)</span></dd>
            </div>
            <div>
              <dt>Postdoc applications</dt>
              <dd><a href="mailto:pdf.hepiitk@gmail.com">pdf.hepiitk@gmail.com</a></dd>
            </div>
            <div>
              <dt>Address</dt>
              <dd>Department of Physics,<br>Indian Institute of Technology Kanpur,<br>Kanpur 208016, Uttar Pradesh, India</dd>
            </div>
            <div>
              <dt>Department</dt>
              <dd><a href="https://www.iitk.ac.in/phy/" target="_blank" rel="noopener">iitk.ac.in/phy</a></dd>
            </div>
          </dl>
        </div>
        <div data-reveal>
          <div class="section-head"><h2>Editor team</h2></div>
          <p class="muted">This site is maintained by graduate students in the group.
             Send corrections, new publications or news items to any of us.</p>
          <div class="stack mt-6" style="--sp-4:0.6rem">
{eds}
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="callout accent-navy" data-reveal>
        <h3>Prospective students and postdocs</h3>
        <p class="muted mb-0">
          If you are interested in joining, look through the
          <a href="research.html">research areas</a> first and write directly to the faculty
          whose work overlaps with yours — several projects span more than one subgroup.
          Current openings are listed under <a href="news.html#positions">news</a>.
        </p>
      </div>
    </div>
  </section>
"""
    body += footer()
    write("contact.html", body)


# ==========================================================================
# 8. BUILD EVERYTHING
# ==========================================================================


if __name__ == "__main__":
    import build_members
    import build_news
    import build_conferences
    import build_research

    if "--figures" in sys.argv:
        build_research.fetch_figures(force="--force" in sys.argv)
        print()

    build_index()
    build_members.build()
    build_research.build()
    build_seminars()
    build_conferences.build()
    build_news.build()
    build_contact()
