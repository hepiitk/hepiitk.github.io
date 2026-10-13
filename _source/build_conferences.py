#!/usr/bin/env python3
"""
build_conferences.py — builds conferences.html, then refreshes index.html

    python3 _source/build_conferences.py

New symposium: copy the first { ... } block of SYMPOSIA, paste it ABOVE it,
change the fields (explained just above SYMPOSIA), and set "highlight" of the
previous year to False. New conference / workshop: add a line to CONFERENCES.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_all import *  # noqa: F401,F403  (shared helpers: head, footer, img, ICON, build_index, ...)


# ==========================================================================
# Conference data  —  edit these lists
# ==========================================================================
# One entry per in-house symposium, newest first.
#   year      : shown in the badge; also the page anchor  conferences.html#symposium-<year>
#   poster    : poster file inside assets/ConferenceWorkshop/  (click opens it full size)
#   title     : heading of the card
#   dates     : "&amp;" is how you write "&" in HTML
#   body      : one or two sentences under the heading
#   sheet     : the long ID in the Google-Sheet link  docs.google.com/spreadsheets/d/<ID>/...
#   gid       : the tab number after "#gid=" in the sheet link, or None for the first tab
#   highlight : True -> maroon badge (use it for the latest / upcoming edition)
#   open      : True -> the programme starts unfolded
SYMPOSIA = [
    {
        "year": "2026",
        "poster": "symposium-2026.webp",
        "title": "In-House Symposium 2026",
        "dates": "31 January &amp; 1 February 2026",
        "body": "The HEP group at IIT Kanpur is organising an in-house symposium. Join us!",
        "sheet": "1ZX2D_ekNjg2hT5NVX8TgTxvaQ5XAxYSDIR8cY_kvVFw",
        "gid": None,
        "highlight": True,
        "open": False,
    },
    {
        "year": "2025",
        "poster": "symposium-2025.webp",
        "title": "In-House Symposium 2025",
        "dates": "22 &amp; 23 March 2025",
        "body": "The HEP group at IIT Kanpur organised an in-house symposium across both days.",
        "sheet": "13BAoV9avu8Uj0lWPkF5D7oqi47VkHMRknYoY67ZOV6g",
        "gid": "1929783250",
        "highlight": False,
        "open": False,
    },
    {
        "year": "2024",
        "poster": "symposium-2024.webp",
        "title": "In-House Symposium 2024",
        "dates": "2 &amp; 3 February 2024",
        "body": "Two days of talks across the theory, experiment and string subgroups.",
        "sheet": "15Nq03RAkqwOqRto4QZPhdWVYTuY2QAqFZZJ2mBIgmlo",
        "gid": None,
        "highlight": False,
        "open": False,
    },
    {
        "year": "2023",
        "poster": "symposium-2023.webp",
        "title": "In-House Symposium 2023",
        "dates": "20 December 2022",
        "body": "The first of the recent series of in-house symposia.",
        "sheet": "1NLZrcR9scQTlMbO4JUFqWcmVNvZK5allDG643ur7AXM",
        "gid": None,
        "highlight": False,
        "open": False,
    },
]

# Other conferences / workshops: (name, year, one-line description, website)
CONFERENCES = [
    ("Aspects of CFTs", "2024",
     "A focused meeting on conformal field theory, hosted at IIT Kanpur.",
     "https://sites.google.com/view/iitkcft/home"),
    ("Strings Attached 2.0", "2023",
     "The second edition of the group's string theory meeting.",
     "https://sites.google.com/view/arjunbagchi/events/strings-attached-2-0?authuser=0"),
]

# ==========================================================================
# Page layout  —  you rarely need to change anything below
# ==========================================================================


def build():
    # Each year is a programme card: poster | title, dates, blurb, buttons —
    # then the Google-Sheet programme in a fold-out panel underneath.
    blocks = []
    for s in SYMPOSIA:
        badge = (f'<span class="pill pill--accent">{s["year"]}</span>' if s["highlight"]
                 else f'<span class="pill">{s["year"]}</span>')
        poster_url = f"{IMG_DIR}/ConferenceWorkshop/{s['poster']}"
        drive_url = f"https://drive.google.com/open?id={s['sheet']}"
        src = f"https://docs.google.com/spreadsheets/d/{s['sheet']}/htmlembed"
        if s["gid"]:
            src += f"?gid={s['gid']}"
        is_open = " open" if s["open"] else ""
        blocks.append(f"""      <article class="symposium" id="symposium-{s['year']}" data-reveal>
        <a class="symposium__poster" href="{poster_url}" target="_blank" rel="noopener"
           title="Open the full-size poster">{img('ConferenceWorkshop/' + s['poster'], s['title'] + ' poster')}</a>
        <div class="symposium__body">
          <div class="symposium__meta">{badge}<span class="symposium__dates">{s['dates']}</span></div>
          <h2 class="symposium__title">{s['title']}</h2>
          <p class="muted">{s['body']}</p>
          <div class="cluster symposium__actions">
            <a class="btn btn--ghost" href="{poster_url}" target="_blank" rel="noopener">View poster</a>
            {ext(drive_url, "Schedule in Drive", "external", "btn btn--ghost")}
          </div>
        </div>
        <details class="symposium__schedule"{is_open}>
          <summary><span class="symposium__summary-open">Show the programme</span><span class="symposium__summary-close">Hide the programme</span></summary>
          <div class="embed embed--sheet">
            <iframe src="{src}" title="{s['title']} programme" loading="lazy"></iframe>
          </div>
        </details>
      </article>""")

    conf_cards = []
    for name, year, blurb, url in CONFERENCES:
        conf_cards.append(f"""        <a class="card card--link accent-navy" href="{url}" target="_blank" rel="noopener" data-reveal>
          <span class="meta">{year}</span>
          <h3>{name}</h3>
          <p>{blurb}</p>
          <p class="mt-4" style="color:var(--accent);font-weight:600">Meeting website →</p>
        </a>""")

    body = head(
        "Conference / Workshop",
        "In-house symposia, conferences and workshops organised by the HEP group at IIT Kanpur.",
        "conferences.html",
    )
    body += page_head_band(
        "Conference / Workshop",
        "The group organises an annual two-day in-house symposium, alongside focused "
        "conferences and workshops hosted at IIT Kanpur.",
        art="symposium",
    )
    body += f"""
  <div class="subnav">
    <div class="wrap">
      <ul>
        <li><a href="#symposia">In-house symposia</a></li>
        <li><a href="#meetings">Conferences &amp; workshops</a></li>
      </ul>
    </div>
  </div>

  <section class="section section--tight" id="symposia">
    <div class="wrap">
      <div class="section-head">
        <h2>In-house symposia</h2>
        <span class="section-head__aside">{len(SYMPOSIA)} editions</span>
      </div>
      <div class="accent-maroon">
{chr(10).join(blocks)}
      </div>
    </div>
  </section>

  <section class="section" id="meetings">
    <div class="wrap">
      <div class="section-head"><h2>Conferences &amp; workshops</h2></div>
      <div class="grid grid--2">
{''.join(conf_cards)}
      </div>
    </div>
  </section>
"""
    body += footer()
    write("conferences.html", body)


if __name__ == "__main__":
    build()
    build_index()  # refresh the Home page (index.html) too
