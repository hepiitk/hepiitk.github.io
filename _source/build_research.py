#!/usr/bin/env python3
"""
build_research.py — builds research.html, then refreshes index.html

    python3 _source/build_research.py              rebuild the Research page (+ Home)
    python3 _source/build_research.py --figures    first download any missing figures

What to edit in this file:
  THRUSTS   the three research areas: Home-page line, paragraph, topics, faculty
  FIGURES   the slideshow of paper figures inside each area:
            FIGURES["theory"], FIGURES["experiment"], FIGURES["string"]

Downloading figures needs (once):  sudo apt install imagemagick poppler-utils ghostscript
Write "&" as "&amp;" inside text.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_all import *  # noqa: F401,F403  (shared helpers: head, footer, img, ICON, build_index, ...)


# ==========================================================================
# THRUSTS  —  the three research areas
# ==========================================================================
# "id" must stay "theory", "experiment" or "string": it links each area to its
# FIGURES list below and to research.html#theory etc.
#
#   "blurb"   one short line, shown on the HOME page card (index.html)
#   "about"   the full paragraph, shown on the RESEARCH page
#   "topics"  the topic list (the Home page card shows only the first few,
#             so put the most important first)
THRUSTS = [
    {
        "id": "theory",
        "art": "theory",
        "num": "01",
        "title": "Particle Theory",
        "accent": "accent-maroon",
        "icon": "atom",
        "blurb": "Physics beyond the Standard Model, the early universe and the "
                 "structure of the proton.",
        "about": "We build and test extensions of the Standard Model with effective field "
                 "theory, and follow them into the early universe: phase transitions and the "
                 "gravitational waves they leave, dark matter, axions and inflation. We also "
                 "map the inner structure of the proton with light-front QCD. Much of this "
                 "work sits where theory meets data: which models survive precision "
                 "measurements at the LHC and in flavour physics, and what signals they would "
                 "leave in gravitational-wave detectors, supernovae and the sky.",
        "topics": [
            "Beyond the Standard Model",
            "Effective field theory",
            "Phase transitions &amp; gravitational waves",
            "Dark matter &amp; cosmology",
            "Axions",
            "Proton structure (light-front QCD)",
            "Inflation &amp; compact objects",
            "Flavour &amp; neutrino physics",
            "Collider phenomenology",
        ],
        "members": ["Dipankar", "Debtosh", "Joydeep", "Kaushik", "Sabyasachi"],
        "link": None,
    },
    {
        "id": "experiment",
        "art": "experiment",
        "num": "02",
        "title": "Particle Experiments",
        "accent": "accent-gold",
        "icon": "detector",
        "blurb": "New-particle searches with CMS, neutrino experiments and machine "
                 "learning for particle physics.",
        "about": "We search for new particles and dark matter with the CMS experiment at "
                 "the LHC, study neutrinos with ANNIE and DUNE, and build detectors in our own "
                 "lab. Machine learning runs through all of it, from reconstructing and "
                 "tagging events to explaining what the networks have learned. We also work on "
                 "the trigger, particle-flow reconstruction and data scouting in CMS, look "
                 "ahead to the HL-LHC and a future 100 TeV collider, and use a scintillator "
                 "telescope in the lab to measure cosmic-ray muons.",
        "topics": [
            "Dark matter &amp; new-particle searches",
            "Machine learning &amp; explainable AI",
            "Jet substructure &amp; tagging",
            "Neutrino oscillations (DUNE)",
            "Neutrino interactions (ANNIE)",
            "Long-lived particles",
            "Higgs measurements at the LHC",
            "Trigger, reconstruction &amp; data scouting (CMS)",
            "Future colliders: HL-LHC &amp; FCC-hh",
            "Detectors &amp; cosmic-ray measurements",
        ],
        "members": ["Navaneeth", "Swagata", "Sanmay"],
        "link": None,
    },
    {
        "id": "string",
        "art": "string",
        "num": "03",
        "title": "String Theory",
        "accent": "accent-navy",
        "icon": "string",
        "blurb": "Holography, black holes, Carrollian physics and quantum systems out "
                 "of equilibrium.",
        "about": "We study quantum gravity and strongly coupled quantum systems: "
                 "holography, black holes and their horizons, entanglement and islands, and "
                 "Carrollian physics with tensionless strings. The conformal bootstrap and "
                 "periodically driven systems link this work to statistical and "
                 "condensed-matter physics. Recent work ranges from the scattering of null "
                 "strings and holography in flat space to islands in braneworlds, Floquet "
                 "conformal field theories, and stars torn apart by black holes and wormholes.",
        "topics": [
            "Tensionless (null) strings",
            "Holography &amp; AdS/CFT",
            "Black holes &amp; horizons",
            "Entanglement &amp; islands",
            "Carrollian holography",
            "Conformal bootstrap",
            "Floquet &amp; non-equilibrium dynamics",
            "Quantum chaos &amp; thermalisation",
            "Tidal disruption &amp; wormholes",
        ],
        "members": ["Arjun", "Apratim", "Diptarka", "Gautam", "Nilay", "Tapobrata"],
        "link": ("https://sites.google.com/view/st-iitk/home", "String theory group site"),
    },
]


# ==========================================================================
# FIGURES  —  the slideshow inside each research area
# ==========================================================================
# FIGURES["theory"], FIGURES["experiment"] and FIGURES["string"] each hold the
# slides shown in that area, in order. One { ... } block = one slide:
#
#   "faculty"  whose paper it is (not shown on the page; helps you keep track)
#   "caption"  one or two plain sentences saying what the figure shows
#   "paper"    title of the paper (shown as a link to arXiv)
#   "arxiv"    arXiv number of the paper, e.g. "2604.03832"
#   "files"    the figure's file name(s) exactly as INSPIRE-HEP lists them;
#              two or three names are placed side by side (left / right panels)
#   "image"    where the finished picture is saved, inside assets/
#
# Make the pictures with:   python3 _source/build_research.py --figures
# A slide whose picture does not exist yet is left out of the page. An area
# with no pictures at all shows its line drawing instead.
FIGURES = {
    # ---------------------------------------------------------- Particle Theory
    "theory": [
        {
            "faculty": "Dipankar Chakrabarti",
            "caption": "Isotropic transverse pressure carried by the down quark (left) and the up "
                       "quark (right), mapped against the quark's transverse momentum.",
            "paper": "Gravitational transverse momentum distribution of proton",
            "arxiv": "2604.03832",
            "files": ["pkd.png", "pku.png"],
            "image": "Research/chakrabarti-2604-03832.webp",
        },
        {
            "faculty": "Joydeep Chakrabortty",
            "caption": "Contours of the potential (left) and its minima against temperature "
                       "(right): the jump between minima shrinks as the Polyakov-loop parameter grows.",
            "paper": "Polyakov Loops Tame Phase Transitions",
            "arxiv": "2607.06203",
            "files": ["barrier_with_bosons.png", "phases_with_bosons_grid.png"],
            "image": "Research/chakrabortty-2607-06203.webp",
        },
        {
            "faculty": "Sabyasachi Chakraborty",
            "caption": "Gravitational-wave spectra predicted for several benchmark points of a "
                       "first-order phase transition, set against the reach of future detectors.",
            "paper": "Feasibility of ultrarelativistic bubbles in SMEFT",
            "arxiv": "2402.02914",
            "files": ["sensitivity-curve.png"],
            "image": "Research/chakraborty-2402-02914.webp",
        },
        {
            "faculty": "Debtosh Chowdhury",
            "caption": "The dark matter power spectrum for different free-streaming horizons when "
                       "the early universe passes through a matter-dominated era.",
            "paper": "Dark matter cooling during early matter-domination boosts sub-earth halos",
            "arxiv": "2408.08360",
            "files": ["powervsk_paper.png"],
            "image": "Research/chowdhury-2408-08360.webp",
        },
        {
            "faculty": "Kaushik Bhattacharya",
            "caption": "The potential around a compact object that could pass for a black hole, "
                       "shown for two values of its compactness C.",
            "paper": "A Potential Black Hole Mimicker From Non-Minimal Coupling",
            "arxiv": "2606.19291",
            "files": ["Vz_vs_Z.png"],
            "image": "Research/bhattacharya-2606-19291.webp",
        },
        {
            "faculty": "Dipankar Chakrabarti",
            "caption": "Light-front distributions of the gluons' mass (left) and angular momentum "
                       "(right) inside the proton, against distance from its centre.",
            "paper": "Gluon gravitational form factors of the proton in a light-front spectator model",
            "arxiv": "2503.12574",
            "files": ["2Dmassdistribution.png", "2Dangulardistribution.png"],
            "image": "Research/chakrabarti-2503-12574.webp",
        },
        {
            "faculty": "Joydeep Chakrabortty",
            "caption": "Where first-order phase transitions occur as the Polyakov-loop phase "
                       "changes (left), and how strong they are (right).",
            "paper": "Higher-dimensional operators and Polyakov loop in hot Scalar QED from the heat kernel",
            "arxiv": "2606.09779",
            "files": ["TcPolyakov.png", "alphaPolyakov.png"],
            "image": "Research/chakrabortty-2606-09779.webp",
        },
        {
            "faculty": "Sabyasachi Chakraborty",
            "caption": "Regions of heavy QCD axion masses and couplings ruled out because supernovae "
                       "would produce too many of them from photons.",
            "paper": "Photoproduction of heavy QCD axions in supernovae",
            "arxiv": "2403.12169",
            "files": ["plot_axion_final.png"],
            "image": "Research/chakraborty-2403-12169.webp",
        },
        {
            "faculty": "Debtosh Chowdhury",
            "caption": "Couplings and masses of ultralight dark matter that could explain the "
                       "gravitational-wave signal reported by the NANOGrav pulsar timing array.",
            "paper": "Ultralight dark matter explanation of NANOGrav observations",
            "arxiv": "2311.10148",
            "files": ["param_g_m_updated.png"],
            "image": "Research/chowdhury-2311-10148.webp",
        },
        {
            "faculty": "Kaushik Bhattacharya",
            "caption": "Phase space of constant-roll warm inflation, coloured by the different "
                       "dynamical regions the early universe can pass through.",
            "paper": "Dynamical systems approach to Cold and Warm Inflation within slow-roll and beyond",
            "arxiv": "2504.10454",
            "files": ["phase_crwi.png"],
            "image": "Research/bhattacharya-2504-10454.webp",
        },
    ],

    # ----------------------------------------------------- Particle Experiments
    "experiment": [
        {
            "faculty": "Sanmay Ganguly",
            "caption": "Average Lund-plane emission density for 1-prong, 2-prong and 3-prong jets "
                       "— the patterns a machine-learning tagger learns to tell apart.",
            "paper": "Explainable AI for Jet Tagging: A Comparative Study of GNNExplainer, "
                     "GNNShap, and GradCAM for Jet Tagging in the Lund Jet Plane",
            "arxiv": "2604.25885",
            "files": ["raw_lund_plane_qcd.png", "raw_lund_plane_hcc.png", "raw_lund_plane_tbqq.png"],
            "image": "Research/ganguly-2604-25885.webp",
        },
        {
            "faculty": "Navaneeth Poonthottathil",
            "caption": "The neutrino beam enters from the left and passes the front muon veto, the "
                       "gadolinium-loaded water tank with its light sensors, and the muon range detector.",
            "paper": "Reconstruction of neutrino events in the Accelerator Neutrino Neutron "
                     "Interaction Experiment: Part I",
            "arxiv": "2510.26050",
            "files": ["annieschematic.png"],
            "image": "Research/poonthottathil-2510-26050-detector.webp",
        },
        {
            "faculty": "Swagata Mukherjee",
            "caption": "The smallest signal a vector-like B′ quark would need for a 5σ discovery "
                       "or 2σ sensitivity at the FCC-hh, as a function of its mass.",
            "paper": "Boosted top tagging via lepton-in-jet topology for vector-like quark "
                     "searches in FCC-hh",
            "arxiv": "2610.05104",
            "files": ["Bprime_reach_10_percent.png"],
            "image": "Research/mukherjee-2610-05104.webp",
        },
        {
            "faculty": "Sanmay Ganguly",
            "caption": "The small circuit of attention heads found to do the work inside a "
                       "top-jet tagging network, coloured by how much each one matters.",
            "paper": "Mechanistic interpretability of a particle-based top-jet tagger",
            "arxiv": "2605.09881",
            "files": ["fig55n_circuit.png"],
            "image": "Research/ganguly-2605-09881.webp",
        },
        {
            "faculty": "Swagata Mukherjee",
            "caption": "Dark matter and mediator masses excluded by a CMS search, for an "
                       "axial-vector (left) and a vector (right) mediator.",
            "paper": "Search for dark matter produced in association with a low-multiplicity jet "
                     "in proton-proton collisions at √s = 13 TeV",
            "arxiv": "2610.00995",
            "files": ["Figure_009-a.png", "Figure_009-b.png"],
            "image": "Research/mukherjee-2610-00995.webp",
        },
        {
            "faculty": "Navaneeth Poonthottathil",
            "caption": "An ANNIE beam event and the plot used to find its Cherenkov ring (top), "
                       "with a simulated event of similar shape for comparison (bottom).",
            "paper": "Reconstruction of neutrino events in the Accelerator Neutrino Neutron "
                     "Interaction Experiment: Part I",
            "arxiv": "2510.26050",
            "files": ["eta3.png"],
            "image": "Research/poonthottathil-2510-26050-event.webp",
        },
        {
            "faculty": "Swagata Mukherjee",
            "caption": "The masses and lifetimes of a doubly charged scalar that experiments have "
                       "already explored, and the room left for the HL-LHC.",
            "paper": "Hunting long-lived doubly charged scalars at the HL-LHC",
            "arxiv": "2608.27251",
            "files": ["summary_limits_Yukawa_revised_2.png"],
            "image": "Research/mukherjee-2608-27251.webp",
        },
        {
            "faculty": "Swagata Mukherjee",
            "caption": "The allowed region of two compositeness parameters, W and Y, from a CMS fit "
                       "to high-mass dilepton events.",
            "paper": "Search for Higgs boson compositeness effects in high-mass dilepton final "
                     "states in proton-proton collisions at √s = 13 and 13.6 TeV",
            "arxiv": "2610.04782",
            "files": ["Figure_003.png"],
            "image": "Research/mukherjee-2610-04782.webp",
        },
    ],

    # ------------------------------------------------------------ String Theory
    "string": [
        {
            "faculty": "Arjun Bagchi",
            "caption": "A heuristic picture of an acoustic black hole: a flat band of waves sits on "
                       "the horizon while Poincaré waves fluctuate around it.",
            "paper": "Carroll in Shallow Water",
            "arxiv": "2411.04190",
            "files": ["wave-bh.png"],
            "image": "Research/bagchi-2411-04190.webp",
        },
        {
            "faculty": "Gautam Sengupta",
            "caption": "A black string with a brane (red), the Hartman–Maldacena surface (blue) and "
                       "the island surfaces (green) used to compute entropies holographically.",
            "paper": "Reflected entropy in BCFTs on a black hole background",
            "arxiv": "2311.17023",
            "files": ["Braneworld-eps-converted-to.png"],
            "image": "Research/sengupta-2311-17023.webp",
        },
        {
            "faculty": "Diptarka Das",
            "caption": "Snapshots of the time evolution of the classical string profile behind a "
                       "class of string scattering amplitudes.",
            "paper": "Classical string profile for a class of DDF amplitudes",
            "arxiv": "2506.23974",
            "files": ["figure.png"],
            "image": "Research/das-2506-23974.webp",
        },
        {
            "faculty": "Tapobrata Sarkar",
            "caption": "Simulated debris of a star 0.55 days after it is disrupted by a black hole "
                       "(left) and by a wormhole (right) of the same mass.",
            "paper": "Relativistic Tidal Disruption in Black Hole and Wormhole Backgrounds",
            "arxiv": "2603.26442",
            "files": ["bh_late.png", "wh_late.png"],
            "image": "Research/sarkar-2603-26442.webp",
        },
        {
            "faculty": "Apratim Kaviraj",
            "caption": "Renormalisation-group flow of a disordered surface defect in the Ising "
                       "model, with two ordered fixed points (red) and one disordered (blue).",
            "paper": "Ising surface defects can get dirty",
            "arxiv": "2605.22628",
            "files": ["flowplot2.png"],
            "image": "Research/kaviraj-2605-22628.webp",
        },
        {
            "faculty": "Arjun Bagchi",
            "caption": "A Penrose diagram of the Schwarzschild black hole with its near-horizon "
                       "region in blue; the inset shows how the horizon is reached from it.",
            "paper": "Black hole Near Horizons through the Looking Glass",
            "arxiv": "2602.20267",
            "files": ["Penrose.png"],
            "image": "Research/bagchi-2602-20267.webp",
        },
        {
            "faculty": "Nilay Kundu",
            "caption": "The maximal analytic extension of the self-similar charged Vaidya "
                       "spacetime; dashed lines mark surfaces of constant z.",
            "paper": "Homothetic Killing horizons in generic Vaidya spacetimes",
            "arxiv": "2604.09760",
            "files": ["RNV_1_alt.png"],
            "image": "Research/kundu-2604-09760.webp",
        },
        {
            "faculty": "Diptarka Das",
            "caption": "Energy density in a periodically driven conformal field theory: it "
                       "localises in the heating phase (left) and oscillates in the non-heating phase (right).",
            "paper": "Exactly Solvable Floquet Dynamics for Conformal Field Theories in "
                     "Dimensions Greater than Two",
            "arxiv": "2311.13468",
            "files": ["fig5a.png"],
            "image": "Research/das-2311-13468.webp",
        },
        {
            "faculty": "Tapobrata Sarkar",
            "caption": "Simulated debris of a white-dwarf binary falling onto an intermediate-mass "
                       "black hole: before, shortly after and long after it fragments.",
            "paper": "Tidal disruptions of close white dwarf binaries by intermediate mass black holes",
            "arxiv": "2508.03463",
            "files": ["clump_1.png", "clump_2.png", "clump_3.png"],
            "image": "Research/sarkar-2508-03463.webp",
        },
        {
            "faculty": "Arjun Bagchi",
            "caption": "A heuristic sketch of a class of Carroll (tensionless) strings wrapping "
                       "around the event horizon of a black hole.",
            "paper": "The Tensionless Lives of Null Strings",
            "arxiv": "2601.20959",
            "files": ["String_wrapping_blackhole.png"],
            "image": "Research/bagchi-2601-20959.webp",
        },
    ],
}


# ==========================================================================
# PAGE LAYOUT  —  you rarely need to change anything below
# ==========================================================================


def slideshow(area, label):
    """Slideshow for one research area; "" when none of its pictures exist yet."""
    figs = FIGURES.get(area, [])
    slides = [f for f in figs if os.path.exists(os.path.join(OUT, IMG_DIR, f["image"]))]
    if len(slides) < len(figs):
        print(f"  note: {len(figs) - len(slides)} {area} figure(s) not in {IMG_DIR}/Research yet — "
              "run  python3 _source/build_research.py --figures")
    if not slides:
        return ""
    total = len(slides)
    items, dots = [], []
    for i, f in enumerate(slides, 1):
        alt = f"Figure from {f['paper']}: {f['caption']}"
        items.append(f"""                <li class="carousel__slide" role="group" aria-roledescription="slide" aria-label="{i} of {total}">
                  <figure class="slide">
                    <a class="slide__img" href="{IMG_DIR}/{f['image']}" target="_blank" rel="noopener" title="Open the full-size figure">{img(f['image'], alt)}</a>
                    <figcaption class="slide__cap">
                      <p class="slide__text">{f['caption']}</p>
                      <a class="slide__paper" href="https://arxiv.org/abs/{f['arxiv']}" target="_blank" rel="noopener">{f['paper']} <span>arXiv:{f['arxiv']}</span></a>
                    </figcaption>
                  </figure>
                </li>""")
        dots.append(f'<button type="button" class="carousel__dot" aria-label="Show figure {i} of {total}"></button>')
    return f"""<div class="carousel" data-carousel aria-roledescription="carousel" aria-label="Figures from recent {label} papers">
              <ul class="carousel__track" tabindex="0">
{chr(10).join(items)}
              </ul>
              <div class="carousel__controls">
                <div class="carousel__dots">{''.join(dots)}</div>
                <span class="carousel__count" aria-hidden="true"><b data-carousel-current>01</b> / {total:02d}</span>
                <div class="carousel__buttons">
                  <button type="button" class="carousel__btn" data-carousel-prev aria-label="Previous figure">{ICON['arrow-left']}</button>
                  <button type="button" class="carousel__btn" data-carousel-play aria-label="Pause the slideshow">{ICON['pause']}{ICON['play']}</button>
                  <button type="button" class="carousel__btn" data-carousel-next aria-label="Next figure">{ICON['arrow-right']}</button>
                </div>
              </div>
            </div>"""


def build():
    """Research page, with a figure slideshow inside each research area."""
    blocks = []
    for t in THRUSTS:
        topics = "".join(f"<li>{x}</li>" for x in t["topics"])
        members = "".join(f'<li><span class="pill pill--accent">{m}</span></li>' for m in t["members"])
        link = ""
        if t["link"]:
            link = f'<p class="mt-4">{ext(t["link"][0], t["link"][1], "globe")}</p>'
        blocks.append(f"""      <div class="thrust {t['accent']}" id="{t['id']}" data-reveal>
        <div class="thrust__head">
          <span class="thrust__num">{t['num']}</span>
          <h2>{t['title']}</h2>
        </div>
        <div class="thrust__body">
          <div>
            <p class="muted">{t['about']}</p>
            <ul class="thrust__topics mt-4">{topics}</ul>
          </div>
          <div class="thrust__side">
            {slideshow(t['id'], t['title']) or f'<figure class="thrust__illus">{img(*ART[t["art"]])}</figure>'}
            <h3>Faculty in this area</h3>
            <ul class="pill-list mt-4">{members}</ul>
            {link}
          </div>
        </div>
      </div>""")

    body = head(
        "Research",
        "Particle theory, particle experiment and string theory at IIT Kanpur — from "
        "effective field theory and collider phenomenology to holography and black holes.",
        "research.html",
    )
    body += page_head_band(
        "Research",
        "The group's work spans three overlapping subgroups. Collaboration across them — "
        "theory feeding searches, experiment sharpening models — is actively encouraged.",
        art="research",
    )

    body += f"""
  <section class="section">
    <div class="wrap">
{''.join(blocks)}
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="callout accent-maroon" data-reveal>
        <h3>Collaborating across subgroups</h3>
        <p class="muted mb-0">
          Several projects sit deliberately between the subgroups — effective field theory
          matched to LHC measurements, dark sector models tested against intensity-frontier
          data, machine learning methods shared between lattice and collider work. Prospective
          students and postdocs are encouraged to talk to more than one faculty member.
        </p>
      </div>
    </div>
  </section>
"""
    body += footer().replace(
        '<script src="assets/app.js" defer></script>',
        '<script src="assets/app.js" defer></script>\n<script src="assets/carousel.js" defer></script>')
    write("research.html", body)


def fetch_figures(force=False):
    """Download every figure in FIGURES and save it as .webp.

    Run with:  python3 _source/build_research.py --figures          (only missing pictures)
               python3 _source/build_research.py --figures --force  (re-download all)

    Needs:  sudo apt install imagemagick poppler-utils ghostscript
    """
    import io
    import json
    import shutil
    import subprocess
    import tarfile
    import tempfile
    import time
    import urllib.request

    magick = shutil.which("magick") or shutil.which("convert")
    if not magick:
        sys.exit("ImageMagick is missing. Install it with:  sudo apt install imagemagick")
    agent = {"User-Agent": "hepiitk-website-builder (https://hepiitk.github.io/website/)"}

    def download(url):
        req = urllib.request.Request(url, headers=agent)
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read()

    def from_inspire(arxiv, names, folder):
        url = f"https://inspirehep.net/api/literature?q=arxiv:{arxiv}&fields=figures"
        hits = json.loads(download(url))["hits"]["hits"]
        figures = hits[0]["metadata"].get("figures", []) if hits else []
        by_name = {fig.get("filename"): fig for fig in figures}
        paths = []
        for name in names:
            fig = by_name.get(name)
            if not fig:
                raise LookupError(f"{name} is not among the paper's figures on INSPIRE-HEP")
            link = fig.get("url") or f"https://inspirehep.net/files/{fig['key']}"
            path = os.path.join(folder, name)
            with open(path, "wb") as fh:
                fh.write(download(link))
            paths.append(path)
        return paths

    def from_arxiv(arxiv, names, folder):
        # INSPIRE stores figures as .png, but the paper's own file may be .pdf/.eps/.jpg
        data = download(f"https://arxiv.org/e-print/{arxiv}")
        tar = tarfile.open(fileobj=io.BytesIO(data), mode="r:*")
        members = {os.path.basename(m.name): m for m in tar.getmembers() if m.isfile()}
        paths = []
        for name in names:
            stem = os.path.splitext(name)[0]
            match = members.get(name) or next(
                (m for base, m in members.items()
                 if os.path.splitext(base)[0] == stem
                 and base.lower().endswith((".png", ".jpg", ".jpeg", ".pdf", ".eps", ".ps"))),
                None)
            if not match:
                raise LookupError(f"{name} not found in the arXiv source of {arxiv}")
            src = os.path.join(folder, "src-" + os.path.basename(match.name))
            with open(src, "wb") as fh:
                fh.write(tar.extractfile(match).read())
            paths.append(to_png(src, folder))
        return paths

    def to_png(src, folder):
        low = src.lower()
        out = os.path.splitext(src)[0] + ".png"
        if low.endswith(".pdf"):
            if not shutil.which("pdftoppm"):
                sys.exit("pdftoppm is missing. Install it with:  sudo apt install poppler-utils")
            subprocess.run(["pdftoppm", "-png", "-r", "200", "-singlefile", src,
                            os.path.splitext(src)[0]], check=True)
        elif low.endswith((".eps", ".ps")):
            if not shutil.which("gs"):
                sys.exit("Ghostscript is missing. Install it with:  sudo apt install ghostscript")
            subprocess.run(["gs", "-q", "-dSAFER", "-dBATCH", "-dNOPAUSE", "-dEPSCrop",
                            "-sDEVICE=png16m", "-r200", f"-sOutputFile={out}", src], check=True)
        else:
            out = src
        return out

    def to_webp(pngs, target):
        os.makedirs(os.path.dirname(target), exist_ok=True)
        cmd = [magick]
        for p in pngs:
            # flatten transparency onto white, trim empty margins
            cmd += ["(", p, "-background", "white", "-alpha", "remove", "-alpha", "off",
                    "-trim", "+repage", "-resize", "x1000>", ")"]
        cmd += ["-background", "white", "-gravity", "center"]
        if len(pngs) > 1:
            cmd += ["+append"]
        cmd += ["-bordercolor", "white", "-border", "24",
                "-resize", "1400x900>", "-quality", "85", target]
        subprocess.run(cmd, check=True)

    done = failed = 0
    for f in [f for area in FIGURES.values() for f in area]:
        target = os.path.join(OUT, IMG_DIR, f["image"])
        if os.path.exists(target) and not force:
            print(f"  have     {f['image']}")
            continue
        folder = tempfile.mkdtemp(prefix="hep-fig-")
        try:
            try:
                pngs = from_inspire(f["arxiv"], f["files"], folder)
                source = "INSPIRE-HEP"
            except Exception as err:
                print(f"  ...      {f['arxiv']}: INSPIRE-HEP failed ({err}); trying the arXiv source")
                time.sleep(3)
                pngs = from_arxiv(f["arxiv"], f["files"], folder)
                source = "arXiv source"
            to_webp(pngs, target)
            kb = os.path.getsize(target) // 1024
            print(f"  saved    {f['image']}  ({kb} KB, from {source})")
            done += 1
        except Exception as err:
            print(f"  FAILED   {f['image']}: {err}")
            failed += 1
        finally:
            shutil.rmtree(folder, ignore_errors=True)
        time.sleep(1)  # be polite to INSPIRE-HEP / arXiv
    print(f"\n{done} figure(s) saved, {failed} failed.")

    # pictures in assets/Research that no slide uses any more
    used = {os.path.basename(f["image"]) for area in FIGURES.values() for f in area}
    folder = os.path.join(OUT, IMG_DIR, "Research")
    unused = sorted(n for n in os.listdir(folder) if n.endswith(".webp") and n not in used) \
        if os.path.isdir(folder) else []
    if unused:
        print("\nNot used by any slide any more (you can delete these):")
        for n in unused:
            print(f"  {IMG_DIR}/Research/{n}")


if __name__ == "__main__":
    if "--figures" in sys.argv:
        fetch_figures(force="--force" in sys.argv)
        print()
    build()
    build_index()  # the Home page shows the three research areas, so refresh it too