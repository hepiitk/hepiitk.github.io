#!/usr/bin/env python3
"""
build_news.py — builds news.html, then refreshes index.html

    python3 _source/build_news.py

Add a news item at the TOP of NEWS (newest first) by copying a { ... } block.
The Home page shows the four newest items automatically.

  "tag"    small label above the title: Symposium, New faculty, Award, Placement...
  "title"  heading of the item
  "body"   the text (a long text can be split over lines, each piece in quotes)
  "link"   None, or a button: ("address", "button text")

PMRF is the list of PMRF fellows. The "Postdoctoral positions" text is inside
build() further down. Write "&" as "&amp;" inside text.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_all import *  # noqa: F401,F403  (shared helpers: head, footer, img, ICON, build_index, ...)


# ==========================================================================
# News data  —  edit these lists
# ==========================================================================
NEWS = [
    {
        "tag": "Symposium",
        "title": "In-House Symposium 2026",
        "body": "The group's in-house symposium was held on 31 January &amp; 1 February 2026.",
        "link": ("conferences.html#symposium-2026", "Schedule and details"),
    },
    {
        "tag": "Symposium",
        "title": "In-House Symposium 2025",
        "body": "The group's in-house symposium was held on 22 &amp; 23 March 2025.",
        "link": ("conferences.html#symposium-2025", "Schedule and details"),
    },
    {
        "tag": "Symposium",
        "title": "In-House Symposium 2024",
        "body": "The group's in-house symposium was held on 2 &amp; 3 February 2024.",
        "link": ("conferences.html#symposium-2024", "Schedule and details"),
    },
    {
        "tag": "New faculty",
        "title": "Welcome, Dr. Apratim Kaviraj",
        "body": "Dr. Kaviraj joins the group as an assistant professor. His research is "
                "primarily dedicated to the conformal bootstrap and critical phenomena.",
        "link": None,
    },
    {
        "tag": "New faculty",
        "title": "Welcome, Dr. Sanmay Ganguly",
        "body": "Dr. Ganguly joins the group as an assistant professor. He is an experimental "
                "high energy physicist and a leading expert in machine learning techniques.",
        "link": None,
    },
    {
        "tag": "New faculty",
        "title": "Welcome, Dr. Swagata Mukherjee",
        "body": "Dr. Mukherjee joins the group as an assistant professor. Her research covers "
                "the high-level trigger in collider experiments, particle-flow reconstruction "
                "in CMS, data scouting, dark photon searches, R-parity violating SUSY searches, "
                "long-lived particles and machine learning.",
        "link": None,
    },
    {
        "tag": "Award",
        "title": "Humboldt Research Fellowship for Upalaparna Banerjee",
        "body": "Upalaparna Banerjee has been awarded a Humboldt Research Fellowship for "
                "postdocs. Congratulations, Upala!",
        "link": None,
    },
    {
        "tag": "Placement",
        "title": "Suraj Prakash — postdoctoral offer from IFIC, Valencia",
        "body": "Suraj Prakash (graduate student) received a postdoctoral offer from IFIC, Valencia.",
        "link": None,
    },
    {
        "tag": "Placement",
        "title": "Shakeel Ur Rahaman — postdoctoral offer from IPPP, Durham",
        "body": "Shakeel Ur Rahaman (graduate student) received a postdoctoral offer from "
                "IPPP, Durham.",
        "link": None,
    },
    {
        "tag": "Placement",
        "title": "Bidyut Dey — postdoctoral offer from INFN, Cosenza",
        "body": "Bidyut Dey (graduate student) received a postdoctoral offer from INFN, Cosenza.",
        "link": None,
    },
]

PMRF = ["Amartya Saha", "Subrata Samanta", "Aryabrat Mahapatra"]

NEWS_FUNDERS_IMG = "News/a39433749708ab3151f2293a95201dd1.jpg"

# ==========================================================================
# Page layout  —  you rarely need to change anything below
# ==========================================================================


def build():
    items = []
    for n in NEWS:
        link = f'<p class="mt-0"><a href="{n["link"][0]}">{n["link"][1]} →</a></p>' if n["link"] else ""
        items.append(f"""        <li data-reveal>
          <span class="meta">{n['tag']}</span>
          <h3>{n['title']}</h3>
          <p>{n['body']}</p>
          {link}
        </li>""")

    pmrf = "".join(f'<li><span class="pill pill--accent">{p}</span></li>' for p in PMRF)

    body = head(
        "News",
        "Group news, postdoctoral openings, fellowships and placements at the HEP group, "
        "IIT Kanpur.",
        "news.html",
    )
    body += page_head_band(
        "News",
        "Arrivals, awards, placements and openings from the high energy physics group.",
        art="news",
    )
    body += f"""
  <div class="subnav">
    <div class="wrap">
      <ul>
        <li><a href="#updates">Updates</a></li>
        <li><a href="#positions">Positions</a></li>
        <li><a href="#pmrf">PMRF</a></li>
        <li><a href="#support">Funding</a></li>
      </ul>
    </div>
  </div>

  <section class="section section--tight" id="updates">
    <div class="wrap">
      <div class="section-head"><h2>Updates</h2></div>
      <ul class="timeline">
{''.join(items)}
      </ul>
    </div>
  </section>

  <section class="section" id="positions">
    <div class="wrap">
      <div class="section-head"><h2>Postdoctoral positions</h2></div>
      <div class="callout accent-maroon" data-reveal>
        <h3>Applications in theory and experiment</h3>
        <p class="muted">
          The high energy physics group at the Indian Institute of Technology Kanpur invites
          applications for postdoctoral positions in theoretical physics (formal / string
          theory, particle phenomenology) and experimental physics (neutrino). Applications
          go through the institute's online portal.
        </p>
        <p class="muted">
          Interested applicants are also encouraged to send a cover letter, curriculum vitae
          and list of publications — all in a <strong style="color:var(--text-hi)">single PDF
          file</strong> — to <a href="mailto:pdf.hepiitk@gmail.com">pdf.hepiitk@gmail.com</a>.
          The most recent advertised round closed on 31 December 2022; please check the portal
          for the current call.
        </p>
        <p class="muted mb-0">We also support applications through the INSPIRE and N-PDF schemes.</p>
        <div class="cluster mt-6">
          {ext("https://www.iitk.ac.in/phy/data/Post-doctoral-vacancies-2022-2023-round-II-02-12-22.pdf", "Advertisement (PDF)", "doc", "btn btn--ghost")}
          {ext("https://online-inspire.gov.in", "INSPIRE", "external", "btn btn--ghost")}
          {ext("https://serbonline.in/SERB/npdf", "SERB N-PDF", "external", "btn btn--ghost")}
        </div>
      </div>
    </div>
  </section>

  <section class="section" id="pmrf">
    <div class="wrap">
      <div class="section-head">
        <h2>Prime Minister's Research Fellows</h2>
        <span class="section-head__aside">{len(PMRF)} fellows</span>
      </div>
      <div class="accent-gold">
        <ul class="pill-list">{pmrf}</ul>
      </div>
    </div>
  </section>

  <section class="section" id="support">
    <div class="wrap funders-block">
      <div class="section-head"><h2>Financial support</h2></div>
      <p class="muted">We gratefully acknowledge the financial support received from our
         funding agencies.</p>
      <div class="mt-6" data-reveal>
        {figure(NEWS_FUNDERS_IMG, "", "")}
      </div>
      <div class="funders mt-4">
        <span class="funder">SERB / DST</span>
        <span class="funder">CSIR</span>
        <span class="funder">DAE</span>
        <span class="funder">MoE · PMRF</span>
        <span class="funder">IIT Kanpur</span>
      </div>
    </div>
  </section>
"""
    body += footer()
    write("news.html", body)


if __name__ == "__main__":
    build()
    build_index()  # refresh the Home page (index.html) too
