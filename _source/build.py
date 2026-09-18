#!/usr/bin/env python3
"""
Build the HEP@IITK static site.

All page content lives in this file, so updating the site means editing the
data structures below and re-running:

    python3 _source/build.py

Output: index.html, members.html, research.html, seminars.html,
        conferences.html, news.html, contact.html  (next to assets/)
"""

import html
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, ".."))

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

# --------------------------------------------------------------------------
# Icons (inline SVG, currentColor)
# --------------------------------------------------------------------------
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
    "news": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 5h12a1 1 0 0 1 1 1v13H5a1 1 0 0 1-1-1z"/><path d="M17 9h2a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1h-2M7 9h6M7 13h6M7 17h4"/></svg>',
}

# Line-engraving detector, used when assets/Home/... is not present.
HERO_ART = """
<svg viewBox="0 0 420 420" role="img" aria-label="Line drawing of a particle detector cross-section with collision tracks">
  <g fill="none" stroke="#c5bfae">
    <circle cx="210" cy="210" r="196" stroke-width="0.8"/>
    <g class="detector-ring">
      <circle cx="210" cy="210" r="178" stroke-width="0.8" stroke-dasharray="3 7"/>
      <circle cx="210" cy="210" r="160" stroke-width="9" stroke-dasharray="22 7" opacity=".5"/>
    </g>
    <g class="detector-ring detector-ring--rev">
      <circle cx="210" cy="210" r="134" stroke-width="13" stroke-dasharray="3 12" opacity=".55"/>
      <circle cx="210" cy="210" r="114" stroke-width="0.8" stroke-dasharray="2 5"/>
    </g>
    <circle cx="210" cy="210" r="94" stroke-width="0.8"/>
    <circle cx="210" cy="210" r="62" stroke-width="0.8" opacity=".8"/>
  </g>

  <!-- tracks out of the interaction point -->
  <g fill="none" stroke-width="1.3" stroke-linecap="round">
    <path class="trace" stroke="#7d1f2c" d="M210 210C244 188 286 190 330 150"/>
    <path class="trace" stroke="#1d3557" d="M210 210C240 240 250 288 240 352"/>
    <path class="trace" stroke="#7d1f2c" d="M210 210C176 226 132 226 78 260"/>
    <path class="trace" stroke="#8a6a24" d="M210 210C196 172 166 140 112 112"/>
    <path class="trace" stroke="#1d3557" d="M210 210C252 214 300 240 344 292"/>
    <path class="trace" stroke="#7d1f2c" d="M210 210C206 164 214 112 252 62"/>
    <path class="trace" stroke="#2f5d43" d="M210 210C170 208 120 188 70 148"/>
    <path class="trace" stroke="#1d3557" d="M210 210C222 252 206 308 150 348"/>
  </g>

  <g fill="#7d1f2c">
    <circle cx="330" cy="150" r="2.6"/><circle cx="240" cy="352" r="2.4"/>
    <circle cx="78" cy="260" r="2.6"/><circle cx="112" cy="112" r="2.2"/>
    <circle cx="344" cy="292" r="2.4"/><circle cx="252" cy="62" r="2.2"/>
    <circle cx="70" cy="148" r="2.4"/><circle cx="150" cy="348" r="2.2"/>
  </g>

  <circle cx="210" cy="210" r="5" fill="#101216"/>
  <circle cx="210" cy="210" r="13" fill="none" stroke="#101216" stroke-width="0.7" opacity=".5"/>
</svg>
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

# --------------------------------------------------------------------------
# Images
#
# Paths are relative to the site root, e.g. assets/Members/<file>.jpg.
# Copy the folders Members/, News/, Research/, ConferenceWorkshop/, Home/ and
# Seminars/ from the old site export into assets/ and every image below
# resolves. Anything missing simply removes itself from the page — no broken
# image icons — so it is safe to add the folders one at a time.
# --------------------------------------------------------------------------
IMG_DIR = "assets"

# Institute emblem in the masthead: copy either top-level .jpg from the old
# export to assets/iitk-logo.jpg. Falls back to the drawn mark above.
LOGO = "iitk-logo.jpg"

BANNERS = {
    "members.html": ("Members/83f67e8a4473bc04a0eb7e214f6ec665.jpg", "pic courtesy: Super-Kamiokande"),
    "research.html": ("Research/a7914909f3dacbbb0adac5caa6732a1a.jpg", "pic courtesy: CERN"),
    "seminars.html": ("Seminars/53cd435926fdef35e2e5cf2d12b4fffb.jpg", ""),
    "conferences.html": ("ConferenceWorkshop/53cd435926fdef35e2e5cf2d12b4fffb.jpg", ""),
}

HERO_PHOTO = ("Home/e8e5c3c4d0f40b553317792526dc596a.jpg", "pic courtesy: CERN")

# Research figures, in the order they appeared in the old carousel
RESEARCH_FIGURES = [
    ("Research/0e27760f5774b747e27861a5fd15d2d0.jpg",
     "Axion searches at the intensity frontier", ""),
    ("Research/30614a063c51707a4e62ad9c48541579.jpg",
     "Two-point susceptibility",
     "Comparison between a conditional normalizing-flow model and the HMC result."),
    ("Research/80446916e28ea1385c5cf01e3481c8fb.jpg",
     "Dark matter production",
     "Effect of an intermediate matter-dominated era on DM production."),
    ("Research/fd872102dbb79ce5a6bae91ad0dbdb90.jpg",
     "EFT to models", ""),
    ("Research/0e3de9cddac55583368e2e9beeb66b52.jpg",
     "Status of the 2HDM", "After 13 TeV of LHC data."),
    ("Research/54df9e05619f5de560f4e389154b30d0.jpg",
     "Dark photon searches at Belle II", ""),
]

NEWS_FUNDERS_IMG = "News/a39433749708ab3151f2293a95201dd1.jpg"

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
}

# Which drawing sits beside each page masthead
PAGE_ART = {
    "seminars.html": "seminar",
    "conferences.html": "symposium",
    "news.html": "news",
    "contact.html": "contact",
}

# name -> portrait file in assets/Members/
PHOTOS = {
    "Arjun Bagchi": "dcb8440f1f9f245daee02fd5600735b6.jpg",
    "Kaushik Bhattacharya": "3d3cd8297a517b4a07d8e2146c97f326.jpg",
    "Dipankar Chakrabarti": "6936b371c48645bab3eb67ab2b4ae61d.jpg",
    "Joydeep Chakrabortty": "c7415c8bf45134d14d6caaa28e2090ea.jpg",
    "Sabyasachi Chakraborty": "f2f23e59533f898bf0239b41f3b12364.jpg",
    "Debtosh Chowdhury": "b9b02ac605d6ab59d498fee23fb5b5a6.jpg",
    "Diptarka Das": "5ab606be08d5219b8a1cf2c0baa267ac.jpg",
    "Sanmay Ganguly": "69606ac9dcdd80ac6f06bf1ec6ae8e5d.jpg",
    "Swagata Mukherjee": "aa6609794987e8ff4866bd7e31a11aec.jpg",
    "Apratim Kaviraj": "332719920fd7187d9d1575fa5709c58f.jpg",
    "Nilay Kundu": "24a11ab192c8fd8acf11450276103742.jpg",
    "Navaneeth Poonthottathil": "589c503b3c8a8f4cb2ce16024b7d645a.jpg",
    "Tapobrata Sarkar": "012de8da05a05352953ca770089fbfc2.jpg",
    "Gautam Sengupta": "dd0fe405f3fb7b44acf42284e0bde174.jpg",

    "Rituparna Ghosh": "109f1453b60b8c9e572c94a675860875.jpg",
    "Sudipta Show": "0d0417a7f4326c118fc832cfeff15623.jpg",
    "Siddhartha Karmakar": "109f1453b60b8c9e572c94a675860875.jpg",
    "Sachin Grover": "c4f029eef54990ea9645b4779e4d4b1f.jpg",
    "Baishali Roy": "2ab5cbba8223d89a8914d8daa1c212d6.jpg",
    "Ankit Anand": "109f1453b60b8c9e572c94a675860875.jpg",
    "Astha Kakkar": "90e31213a462864ee8cb4093e605aa7e.jpg",
    "Saikat Mondal": "84c7fea58e64c7d4b3ff2fcc445b0101.jpg",

    "Abhijit Kishore": "868d2b32cfb4c134ca0aae2837a52886.jpg",
    "Ankit Gill": "e9c30aec7e9f4c2a900d8e9bc5b476b5.jpg",
    "Sandip Biswas": "b964753633dafc2c2c9125ef04fb3898.jpg",
    "Himanshu Chourasiya": "a6bb41540db03ace7ae91e8ee7f869e2.jpg",
    "Arpan Hait": "68312b2859da6a3a7d9b3e101c42077f.jpg",
    "Saikat Biswas": "b964753633dafc2c2c9125ef04fb3898.jpg",
    "Amartya Saha": "fab3698af75abbf2fa928b932590e00d.jpg",
    "Ankur Dey": "5448e215be33c0c16d8ea3801bba6d10.jpg",
    "Anurag Sarkar": "bcafc860dcac2235f410b5d59152ad33.jpg",
    "Priyanka Saha": "e9d895c0738a9ca4aebcc5666bc396da.jpg",
    "Subrata Samanta": "2d55ff96dd3dfc4833490db82333872b.jpg",
    "Santanu Mandal": "f764994f2927ee020e7dd111da68f8c0.jpg",
    "Ritwika Ghoshal": "b964753633dafc2c2c9125ef04fb3898.jpg",
    "Puskhar Soni": "50ab0b7425e176a5282a2bf004ce9cf6.jpg",
    "Shibam Das": "a40da19610d2fbde232b5138d550b1b6.jpg",
    "Atanu Samanta": "c1c102a3bb35ef7b9c0369fec852ed81.jpg",
    "Sharang Rajesh Iyer": "e5fae74ac3e51735a9af9aae4f5a3949.jpg",
    "Mudit Kumar": "6b767a1c83304ddfdaa41830858e50a3.jpg",
    "Anuj Gupta": "93daf54631d8ededf8e1030aab43bbd1.jpg",
    "MD Sariful Islam": "18da9f68e4b9e228a930637bee220466.jpg",
    "Aryabrat Mahapatra": "c6d48c0c845aedcae2ef190db634840a.jpg",
    "Debmalya Dey": "f689dc9ef5c789c71ef9dfc181885309.jpg",
    "Adarsh Panday": "fca0f226e73d0a2c8b4ed9492ada483d.jpg",
    "Kaushik Kangsabanik": "6783e7bbeb7449b22c82d2007813c41f.jpg",
    "Shashank Sharma": "d0b3c209f1d75ac474d605ba97e7d835.jpg",
    "Kauship Saha": "8d33b2263477f51fcbfe5f96dd459048.jpg",
    "Deepanshu Bisht": "930eae77412c3cbd4f5b37d7dd4a8b58.jpg",
    "Nabin Kumar Pidikaka": "dcaefdb84f635a503a0b8b7d9dfad403.jpg",
    "Rounak Nath": "8a21ec2bba9615602968786af50c9ede.jpg",
    "Debanjan Balui": "f9d182b34b7f1bfdbfbbe4fd5367bab2.jpg",
    "Niles Mondal": "7ef73cfe138d32d8c0de692696c6355f.jpg",
    "Kowsona Chakraborty": "220571b33bc66fc9c8fe5b8e06bf1a24.jpg",
    "Saurabh Rai": "e827262668828e46b2c12780f2c6fe57.jpg",
    "Sandipan Rakshit": "1638a1915548726bd726f82e316e5ac8.jpg",
    "Saswata Chatterjee": "810e20af4a5ebebbe912c66d795d91b4.jpg",
    "Astha Tiwari": "02714eeecfdc096d12de92f00562e624.jpg",
    "Suprajaa D": "dc9752ee6c3cdc47eff3ca07bb8a91d6.jpg",
    "Adil Imam": "638152a27fb876fcff9e07c35fb84c45.jpg",
    "Arkachur Bhattacharya": "24619f7fa298be2b98fc4a14e5e7bfdc.jpg",
    "Sunny Keshri": "dad02c3b8d951c1de11a5c96f4da58c7.jpg",
}


# --------------------------------------------------------------------------
# Data
# --------------------------------------------------------------------------
INSPIRE = "https://inspirehep.net/authors/"

# (name, web, inspire-id-or-url, interests)
FACULTY = [
    ("Arjun Bagchi", "https://sites.google.com/view/arjunbagchi/", "1043091",
     "String theory, gauge&nbsp;/&nbsp;gravity dualities, holography, CFTs."),
    ("Kaushik Bhattacharya", None, "1019786",
     "Astroparticle physics, cosmology, gravitation."),
    ("Dipankar Chakrabarti", "https://home.iitk.ac.in/~dipankar/", "1014130",
     "QCD, lattice gauge theory and lightcone field theories."),
    ("Joydeep Chakrabortty", None, "1023458",
     "Beyond the Standard Model, effective field theories, supergravity, supersymmetry."),
    ("Sabyasachi Chakraborty", "https://home.iitk.ac.in/~sabyac/", "1250995",
     "Beyond the Standard Model, effective field theory, axions, phase transitions, supersymmetry."),
    ("Debtosh Chowdhury", "https://home.iitk.ac.in/~debtoshc/", "1034163",
     "Beyond the Standard Model, cosmology and astroparticle physics, flavour physics, supersymmetry."),
    ("Diptarka Das", "https://home.iitk.ac.in/~didas/", "1233200",
     "Non-equilibrium physics, two-dimensional theories, large-N theories."),
    ("Sanmay Ganguly", None, "1071689",
     "Experimental high energy physics, machine learning for HEP, BSM searches, jet studies at the LHC."),
    ("Apratim Kaviraj", None, "1238225",
     "Theoretical high energy physics, conformal field theories, critical phenomena."),
    ("Nilay Kundu", "https://home.iitk.ac.in/~nilayhep/", "1274025",
     "Classical and quantum gravity, quantum field theory, string theory, AdS/CFT."),
    ("Swagata Mukherjee", None, "1077596",
     "Collider physics, the CMS experiment at the LHC, BSM searches, machine learning."),
    ("Navaneeth Poonthottathil", "https://neutrinos-iitk.com/", "1191574",
     "Experimental high energy physics, neutrino physics, long-baseline neutrino experiments."),
    ("Tapobrata Sarkar", None, "990296",
     "String theory, gravity, information geometry, classical and quantum phase transitions, cosmology."),
    ("Gautam Sengupta", "https://home.iitk.ac.in/~sengupta/", "1037280",
     "String theory, quantum gravity, holographic quantum entanglement."),
]

POSTDOCS = [
    ("Rituparna Ghosh", None, "2079276"),
    ("Sudipta Show", None,
     "https://inspirehep.net/authors?sort=bestmatch&size=25&page=1&q=Sudipto%20Show"),
    ("Siddhartha Karmakar", None, "2663673"),
    ("Sachin Grover", None, "2139519"),
    ("Baishali Roy", None, "1912629"),
    ("Ankit Anand", None, "1771806"),
    ("Astha Kakkar", None, "2016459"),
    ("Saikat Mondal", None, "2619972"),
]

STUDENTS = [
    ("Abhijit Kishore", None, "2870898"),
    ("Ankit Gill", None, "2851564"),
    ("Sandip Biswas", None, "2209125"),
    ("Himanshu Chourasiya", None, "2026028"),
    ("Arpan Hait", None, "2514156"),
    ("Saikat Biswas", None, "2727294"),
    ("Amartya Saha", None, "2126544"),
    ("Ankur Dey", None, "2750533"),
    ("Anurag Sarkar", None, "2773293"),
    ("Priyanka Saha", None, "2338279"),
    ("Subrata Samanta", "https://home.iitk.ac.in/~samantaphy20/", "2685933"),
    ("Santanu Mandal", None, "2729840"),
    ("Ritwika Ghoshal", None, None),
    ("Puskhar Soni", None, "2801474"),
    ("Shibam Das", None, None),
    ("Atanu Samanta", None, "2860792"),
    ("Sharang Rajesh Iyer", None, "3072837"),
    ("Mudit Kumar", None, "2752420"),
    ("Anuj Gupta", None, "2752428"),
    ("MD Sariful Islam", None, "2819696"),
    ("Aryabrat Mahapatra", "https://sites.google.com/view/web-profile-", "2136625"),
    ("Debmalya Dey", None, "2865271"),
    ("Adarsh Panday", None, "2903795"),
    ("Kaushik Kangsabanik", None, "2670488"),
    ("Shashank Sharma", None, None),
    ("Kauship Saha", None, None),
    ("Deepanshu Bisht", "https://sites.google.com/view/deepdives", "2817636"),
    ("Nabin Kumar Pidikaka", None, None),
    ("Rounak Nath", None, None),
    ("Debanjan Balui", None, "2893850"),
    ("Niles Mondal", None, None),
    ("Kowsona Chakraborty", None, None),
    ("Saurabh Rai", None, None),
    ("Sandipan Rakshit", "https://sites.google.com/view/sandipanr/home", None),
    ("Saswata Chatterjee", None, None),
    ("Astha Tiwari", None, None),
    ("Suprajaa D", None, None),
    ("Adil Imam", None, None),
    ("Arkachur Bhattacharya", None, "3072456"),
    ("Sunny Keshri", None, None),
]

# (name, role/year, present position)
ALUMNI = [
    ("Prabwal Phukon", "PhD 2014", "Assistant Professor, Department of Physics, Dibrugarh University."),
    ("Subhash Mahapatra", "PhD 2015", "Assistant Professor, Department of Physics, NIT Rourkela."),
    ("Chandan Mondal", "PhD 2016", "Associate Professor, Institute of Modern Physics, Lanzhou, China."),
    ("Anshuman Dey", "PhD 2017", "Postdoc, University of Santiago de Compostela, Spain."),
    ("Jishnu Goswami", "PhD 2017", "Postdoc, Advanced Institute for Computational Science, RIKEN, Japan."),
    ("Tripurari Srivastava", "PhD 2018", "D. S. Kothari Fellow, Delhi University."),
    ("Pratim Roy", "PhD 2018", "Postdoc, HRI, India."),
    ("Aditya Mehra", "PhD 2018", "University of Edinburgh."),
    ("Tanmay Maji", "PhD 2018", "Assistant Professor, NIT Kurukshetra."),
    ("Dipanjan Dey", "PhD 2019", "Postdoc, Dalhousie University, Canada."),
    ("Saikat Chakraborty", "PhD 2019", "Postdoc, North West University, South Africa."),
    ("Pulastya Parekh", "PhD 2020", "Postdoc, CECS, Valdivia, Chile."),
    ("Suvankar Paul", "PhD 2020", "Lecturer in Physics, Maynaguri Govt. Polytechnic, West Bengal."),
    ("Rinku Maji", "PhD 2022", "Postdoc, South Korea."),
    ("Supratim Das Bakshi", "PhD 2022", "Postdoc, University of Granada."),
    ("Anisha", "PhD 2022", "Postdoc, University of Glasgow."),
    ("Poulami Nandi", "PhD 2022", "Postdoc, IIT Gandhinagar."),
    ("Pritam Banerjee", "PhD 2022", "NPDF, IIT Kharagpur."),
    ("Sandip Chowdhury", "PhD 2022", ""),
    ("Himadri Roy", "PhD 2023", ""),
    ("Bidyut Dey", "PhD 2023", "University of Calabria (INFN), Cosenza, Italy."),
    ("Kunal Pal", "PhD 2023", ""),
    ("Kuntal Pal", "PhD 2023", ""),
    ("Sanchari Pal", "PhD 2023", ""),
    ("Shakeel Ur Rahaman", "PhD 2023", "Durham University, IPPP."),
    ("Suraj Prakash", "PhD 2023", "University of Valencia, IFIC, Spain."),
    ("Saddam Hussain", "PhD 2023", ""),
    ("Shaswata Chowdhury", "PhD 2023", "IMSc, Chennai."),
    ("Minhajul Islam", "PhD 2023", ""),
    ("Poonam Choudhary", "PhD 2024", ""),
    ("Mamta Gautam", "PhD 2024", ""),
    ("Prateksh Dhivakar", "PhD 2024", "University of Victoria, Canada."),
    ("Nitesh Jaiswal", "PhD 2024", "IIT Bombay."),
    ("Punit Sharma", "PhD 2024", ""),
    ("Upalaparna Banerjee", "PhD 2024", "University of Mainz, Germany."),
    ("Ankur Singha", "PhD 2024", "TU Berlin."),
    ("Vinayak Raj", "PhD 2024", "Huzhou University (ZJHU)."),
    ("Mir Afrasiar", "PhD 2024", "Shanghai University (SHU)."),
    ("Debojyoti Garain", "PhD 2024", "Clemson University."),
    ("Bheemsehan Gurjar", "PhD 2024", "IIT Kanpur."),
    ("Sudipta Dutta", "PhD 2024", "Université Libre de Bruxelles, Belgium."),
    ("Ritankar Chatterjee", "PhD 2024", "IIT Ropar, India."),
    ("Pinaki Banerjee", "Postdoc", "IAS Princeton."),
    ("Sunanda Patra", "Postdoc", "Assistant Professor, Vidyasagar College, Kolkata."),
    ("Shankhadeep Chakrabortty", "Postdoc", "Assistant Professor, IIT Ropar."),
    ("Zodinmawia", "Postdoc", "Assistant Professor, Department of Physics, Mizoram University, Aizawl."),
    ("Suchetan Das", "Postdoc", ""),
    ("Mangesh Mandlik", "Postdoc", "Assistant Professor, IIT (ISM) Dhanbad."),
    ("Kedar S. Kolekar", "Postdoc", "Postdoc, Tsinghua University, Beijing."),
    ("Debangshu Mukherjee", "Postdoc", "Postdoc, APCTP, Pohang."),
    ("Taniya Mandal", "Postdoc", "SERB–Ramanujan Fellow, NISER, Bhubaneswar."),
    ("Anirban Chatterjee", "Postdoc", "Ningbo University (NBU)."),
    ("Jaydeb Das", "Postdoc 2024", "IIT Guwahati, India."),
    ("Sarath N", "Postdoc 2025", "Assistant Professor, SR University, Warangal."),
    ("Poulami Mondal", "Postdoc 2025", "TIFR Mumbai."),
    ("Nabarun Chakrabarty", "INSPIRE Faculty", "Assistant Professor, Visva-Bharati University, West Bengal."),
    ("Indrani Chakraborty", "INSPIRE Faculty",
     "Assistant Professor (Senior Grade), Jaypee Institute of Information Technology."),
    ("Subhendra Mohanty", "Visiting Faculty", "IISER Bhopal."),
]

THRUSTS = [
    {
        "id": "theory",
        "art": "theory",
        "num": "01",
        "title": "Particle Theory",
        "accent": "accent-maroon",
        "icon": "atom",
        "blurb": "Model building beyond the Standard Model, effective field theory and "
                 "precision calculations, together with the QCD, cosmology and flavour "
                 "questions that connect them to data.",
        "topics": [
            "Beyond Standard Model theory",
            "Effective field theory",
            "Precision physics",
            "Perturbative and non-perturbative QCD",
            "Cosmology &amp; astroparticle physics",
            "Neutrino and flavour physics",
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
        "blurb": "Collider and neutrino experiment: triggering and reconstruction, new-physics "
                 "searches at the LHC, oscillation measurements with DUNE and ANNIE, and the "
                 "detector and machine-learning work that makes them possible.",
        "topics": [
            "High-level trigger in collider experiments",
            "Particle-flow reconstruction in CMS",
            "Data scouting",
            "Dark photon search",
            "R-parity violating SUSY search",
            "Long-lived particles",
            "Machine learning",
            "Neutrino oscillation physics (DUNE &amp; ANNIE)",
            "Leptonic CP violation",
            "Sterile neutrinos &amp; dark matter search",
            "Neutrino–nucleus interaction measurements",
            "State-of-the-art detector technology",
            "Higgs precision measurements at the LHC",
            "Jet studies at the LHC",
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
        "blurb": "Holography and quantum gravity, black hole physics, out-of-equilibrium "
                 "dynamics and the bootstrap — from AdS/CFT to quantum thermalisation.",
        "topics": [
            "String theory",
            "AdS/CFT, holography",
            "General relativity",
            "Black hole physics",
            "Out-of-equilibrium physics",
            "Quantum thermalisation",
            "Conformal bootstrap",
        ],
        "members": ["Arjun", "Apratim", "Diptarka", "Gautam", "Nilay", "Tapobrata"],
        "link": ("https://sites.google.com/view/st-iitk/home", "String theory group site"),
    },
]

SYMPOSIA = [
    {
        "year": "2026",
        "poster": "ConferenceWorkshop/7912f0e53c363a0de0d81da366cf424f.jpg",
        "title": "In-House Symposium 2026",
        "dates": "31 January &amp; 1 February 2026",
        "body": "The HEP group at IIT Kanpur is organising an in-house symposium. Join us!",
        "sheet": "1ZX2D_ekNjg2hT5NVX8TgTxvaQ5XAxYSDIR8cY_kvVFw",
        "sheet_label": "HEP_symposium_2026",
        "gid": None,
        "upcoming": True,
    },
    {
        "year": "2025",
        "poster": "ConferenceWorkshop/8939251ee7f19254324f8fd3ab5c6692.jpg",
        "title": "In-House Symposium 2025",
        "dates": "22 &amp; 23 March 2025",
        "body": "The HEP group at IIT Kanpur organised an in-house symposium across both days.",
        "sheet": "13BAoV9avu8Uj0lWPkF5D7oqi47VkHMRknYoY67ZOV6g",
        "sheet_label": "HEP_Symposium_Schedule",
        "gid": "1929783250",
        "upcoming": False,
    },
    {
        "year": "2024",
        "poster": "ConferenceWorkshop/5e37e552b967739f9ddade57f2270f30.jpg",
        "title": "In-House Symposium 2024",
        "dates": "2 &amp; 3 February 2024",
        "body": "Two days of talks across the theory, experiment and string subgroups.",
        "sheet": "15Nq03RAkqwOqRto4QZPhdWVYTuY2QAqFZZJ2mBIgmlo",
        "sheet_label": "In_House_Symposium_24",
        "gid": None,
        "upcoming": False,
    },
    {
        "year": "2023",
        "poster": "ConferenceWorkshop/c4e7cb7fda048b2f4d0bed4b91e272a9.jpg",
        "title": "In-House Symposium 2023",
        "dates": "2023",
        "body": "The first of the recent series of in-house symposia.",
        "sheet": "1NLZrcR9scQTlMbO4JUFqWcmVNvZK5allDG643ur7AXM",
        "sheet_label": "In_House_Symposium",
        "gid": None,
        "upcoming": False,
    },
]

CONFERENCES = [
    ("Aspects of CFTs", "2024",
     "A focused meeting on conformal field theory, hosted at IIT Kanpur.",
     "https://sites.google.com/view/iitkcft/home"),
    ("Strings Attached 2.0", "2023",
     "The second edition of the group's string theory meeting.",
     "https://sites.google.com/view/arjunbagchi/events/strings-attached-2-0?authuser=0"),
]

NEWS = [
    {
        "tag": "Symposium",
        "title": "In-House Symposium 2026",
        "body": "The HEP group at IIT Kanpur is organising an in-house symposium on "
                "31 January &amp; 1 February 2026. Join us!",
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

EDITORS = [
    ("Subrata Samanta", "samantaphy20@iitk.ac.in"),
    ("Atanu Samanta", "asamanta23@iitk.ac.in"),
    ("Debmalya Dey", "debmalyad23@iitk.ac.in"),
    ("Pushkar Soni", "pushkars21@iitk.ac.in"),
    ("Shibam Das", "shibamdas23@iitk.ac.in"),
]


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def initials(name):
    parts = [p for p in re.split(r"\s+", name) if p]
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()


def pub_url(ref):
    if not ref:
        return None
    if ref.startswith("http"):
        return ref
    return INSPIRE + ref + "?ui-citation-summary=true"


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


def banner(page):
    """Wide photographic strip under a page masthead, as the old site had."""
    if page not in BANNERS:
        return ""
    path, credit = BANNERS[page]
    cap = f"<figcaption>{credit}</figcaption>" if credit else ""
    return f'\n  <figure class="banner">{img(path, "", eager=True)}{cap}</figure>\n'


def person_card(name, web, pub, interests, variant=""):
    pu = pub_url(pub)
    links = []
    if web:
        links.append(ext(web, "Web", "globe"))
    if pu:
        links.append(ext(pu, "Publications", "doc"))
    else:
        links.append('<span class="chip chip--muted">' + ICON["doc"] + "<span>Publications</span></span>")
    key = html.escape((name + " " + (interests or "")).lower(), quote=True)
    photo = img("Members/" + PHOTOS[name], name) if name in PHOTOS else ""
    return f"""        <article class="person {variant}" data-person="{key}">
          <span class="person__avatar">{photo}<span aria-hidden="true">{initials(name)}</span></span>
          <div class="person__body">
            <h3 class="person__name">{name}</h3>
            <p class="person__interests"><b>Interests</b> {interests}</p>
            <div class="person__links">{''.join(links)}</div>
          </div>
        </article>"""


def roster_item(name, web, pub):
    pu = pub_url(pub)
    links = []
    if web:
        links.append(
            f'<a class="icon-link" href="{web}" target="_blank" rel="noopener" '
            f'title="{name} — personal site"><span class="visually-hidden">'
            f"{name} personal site</span>{ICON['globe']}</a>"
        )
    if pu:
        links.append(
            f'<a class="icon-link" href="{pu}" target="_blank" rel="noopener" '
            f'title="{name} — publications"><span class="visually-hidden">'
            f"{name} publications</span>{ICON['doc']}</a>"
        )
    key = html.escape(name.lower(), quote=True)
    photo = img("Members/" + PHOTOS[name], name) if name in PHOTOS else ""
    return f"""          <li data-person="{key}"><div class="wall__item">
            <span class="wall__photo">{photo}<span aria-hidden="true">{initials(name)}</span></span>
            <span class="wall__name">{name}</span>
            <span class="wall__links">{''.join(links)}</span>
          </div></li>"""


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
<link rel="icon" href="assets/favicon.png" type="image/svg+xml">
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


def page_head_band(title, desc, extra="", page=None):
    art = ""
    if page in PAGE_ART:
        path, alt = ART[PAGE_ART[page]]
        art = f'      <figure class="page-head__illus">{img(path, alt, eager=True)}</figure>\n'
    inner = f"""      <div>
        <p class="eyebrow">{SITE_SHORT}</p>
        <h1>{title}</h1>
        <p>{desc}</p>
        {extra}
      </div>
{art}"""
    grid_open, grid_close = ('    <div class="page-head__grid">\n', "    </div>\n") if art else ("", "")
    if not art:
        inner = inner.replace("      <div>\n", "").replace("\n      </div>\n", "\n")
    return f"""  <section class="page-head">
    <div class="wrap">
{grid_open}{inner}{grid_close}    </div>
  </section>
{banner(page) if page else ""}"""


def write(name, body):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    print("wrote", name, f"({len(body)//1024} KB)")


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------
def build_home():
    cards = []
    for t in THRUSTS:
        top = "".join(f"<li><span class='pill'>{x}</span></li>" for x in t["topics"][:5])
        art_path, art_alt = ART[t["art"]]
        cards.append(f"""      <a class="card card--link {t['accent']}" href="research.html#{t['id']}" data-reveal>
        <span class="card__art">{img(art_path, art_alt)}</span>
        <h3>{t['title']}</h3>
        <p>{t['blurb']}</p>
        <ul class="pill-list mt-4">{top}</ul>
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
        <h1>Probing matter, spacetime and the <em>early universe</em></h1>
        <div class="hero__rule"></div>
        <p class="lede dropcap">
          Our group at IIT Kanpur works on different aspects of high energy physics —
          astroparticle physics, cosmology, particle theory and experiment, and string
          theory. We are faculty, postdoctoral fellows and graduate students who actively
          encourage and pursue collaborations across the subgroups.
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
    body += footer()
    write("index.html", body)


def build_members():
    fac = "\n".join(person_card(n, w, p, i) for n, w, p, i in FACULTY)
    post = "\n".join(roster_item(n, w, p) for n, w, p in POSTDOCS)
    stud = "\n".join(roster_item(n, w, p) for n, w, p in STUDENTS)
    alum = "\n".join(
        f'          <li data-person="{html.escape((n + " " + now).lower(), quote=True)}">'
        f'<span class="alumni__name">{n}</span>'
        f'<span class="alumni__year">{role}</span>'
        f'<span class="alumni__now">{now or "—"}</span></li>'
        for n, role, now in ALUMNI
    )

    body = head(
        "Members",
        "Faculty, postdoctoral fellows, graduate students and alumni of the high energy "
        "physics group at IIT Kanpur.",
        "members.html",
    )
    body += page_head_band(
        "Members",
        f"{len(FACULTY)} faculty, {len(POSTDOCS)} postdoctoral fellows and "
        f"{len(STUDENTS)} graduate students, with {len(ALUMNI)} alumni now spread across "
        "institutions worldwide.",
        f"""<div class="cluster mt-6">
        <label class="field">
          <span class="visually-hidden">Search members by name or research interest</span>
          {ICON['search']}
          <input id="member-search" type="search" placeholder="Search by name or interest…" autocomplete="off">
        </label>
        <span id="filter-status" class="dim" style="font-size:var(--step--1)" role="status" aria-live="polite"></span>
      </div>""",
        page="members.html",
    )
    body += f"""
  <div class="subnav">
    <div class="wrap">
      <ul>
        <li><a href="#faculty">Faculty</a></li>
        <li><a href="#postdocs">Postdocs</a></li>
        <li><a href="#students">Graduate students</a></li>
        <li><a href="#alumni">Alumni</a></li>
      </ul>
    </div>
  </div>

  <section class="section section--tight" id="faculty" data-person-group>
    <div class="wrap">
      <div class="section-head">
        <h2>Faculty</h2>
        <span class="section-head__aside">{len(FACULTY)} members</span>
      </div>
      <div class="people">
{fac}
      </div>
    </div>
  </section>

  <section class="section" id="postdocs" data-person-group>
    <div class="wrap">
      <div class="section-head">
        <h2>Postdoctoral fellows</h2>
        <span class="section-head__aside">{len(POSTDOCS)} members</span>
      </div>
      <div class="accent-navy">
        <ul class="wall">
{post}
        </ul>
      </div>
    </div>
  </section>

  <section class="section" id="students" data-person-group>
    <div class="wrap">
      <div class="section-head">
        <h2>Graduate students</h2>
        <span class="section-head__aside">{len(STUDENTS)} members</span>
      </div>
      <div class="accent-maroon">
        <ul class="wall">
{stud}
        </ul>
      </div>
    </div>
  </section>

  <section class="section" id="alumni" data-person-group>
    <div class="wrap">
      <div class="section-head">
        <h2>Alumni</h2>
        <span class="section-head__aside">{len(ALUMNI)} former members</span>
      </div>
      <ul class="alumni">
{alum}
      </ul>
    </div>
  </section>
"""
    body += footer()
    write("members.html", body)


def build_research():
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
            <p class="muted">{t['blurb']}</p>
            <ul class="thrust__topics mt-4">{topics}</ul>
          </div>
          <div class="thrust__side">
            <figure class="thrust__illus">{img(*ART[t['art']])}</figure>
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
        page="research.html",
    )
    gallery = "\n".join(
        "        " + figure(path, title, cap) for path, title, cap in RESEARCH_FIGURES
    )

    body += f"""
  <section class="section">
    <div class="wrap">
{''.join(blocks)}
    </div>
  </section>

  <section class="section section--band" id="figures">
    <div class="wrap">
      <div class="section-head">
        <h2>Selected figures</h2>
        <span class="section-head__aside">from recent work</span>
      </div>
      <div class="gallery" data-reveal>
{gallery}
      </div>
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
    body += footer()
    write("research.html", body)


def build_seminars():
    cal_src = (
        "https://calendar.google.com/calendar/embed?src=hepiitk%40gmail.com"
        "&ctz=Asia%2FKolkata&color=%239fe1e7&mode=AGENDA&showTitle=0&showPrint=0"
    )
    body = head(
        "Seminars",
        "HEP seminars, the particle journal club and the string journal club at IIT Kanpur.",
        "seminars.html",
    )
    body += page_head_band(
        "Seminars",
        "A weekly HEP seminar plus two journal clubs, one for particle physics and one for "
        "string theory. Everything runs on the group calendar below.",
        page="seminars.html",
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
      <div class="embed embed--calendar" data-reveal>
        <div class="embed__bar">
          <span>hepiitk@gmail.com</span>
          {ext("https://calendar.google.com/calendar/embed?src=hepiitk%40gmail.com&ctz=Asia%2FKolkata", "Open calendar", "external")}
        </div>
        <iframe src="{cal_src}" title="HEP@IITK seminar calendar" loading="lazy"></iframe>
      </div>
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
{sheet_embed("1anX0qlXKS1CVkrHNJprBONlXY60kgFt8gxzGX6w_rms", "Journal_Club@IITK", "0")}
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


def build_conferences():
    blocks = []
    for s in SYMPOSIA:
        badge = '<span class="pill pill--accent">Upcoming</span>' if s["upcoming"] else \
                f'<span class="pill">{s["year"]}</span>'
        blocks.append(f"""      <article class="symposium" id="symposium-{s['year']}" data-reveal>
        {figure(s['poster'], "", "", cls="poster")}
        <div class="symposium__body">
          <div class="cluster" style="margin-bottom:var(--sp-3)">
            {badge}
            <h2 style="margin:0;font-size:var(--step-2)">{s['title']}</h2>
          </div>
          <p class="muted">{s['body']} <strong>{s['dates']}</strong></p>
{sheet_embed(s['sheet'], s['sheet_label'], s['gid'])}
        </div>
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
        page="conferences.html",
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
{''.join(blocks)}
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


def build_news():
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
        page="news.html",
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


def build_contact():
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
        page="contact.html",
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


if __name__ == "__main__":
    build_home()
    build_members()
    build_research()
    build_seminars()
    build_conferences()
    build_news()
    build_contact()
    print("\nDone. Open index.html in a browser.")
