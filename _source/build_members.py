#!/usr/bin/env python3
"""
build_members.py — builds members.html, then refreshes index.html

    python3 _source/build_members.py

Every person is ONE { ... } block. To add someone, copy a block, paste it
where they should appear (the order here is the order on the page), and
change the text inside the quotes.

  "name"       full name, as it should appear
  "photo"      picture file inside assets/Members/, e.g. "priya-nair.webp"
               None  -> the person's initials are shown instead
  "web"        personal web page (https://...), or None
  "inspire"    INSPIRE author number, e.g. "1043091", or any full https:// link
               to a publication list, or None
  "interests"  (faculty only) one line of research interests

ALUMNI are one line each: "name", "role" (e.g. "PhD 2026") and "now" (present
position, or "" if not known).

Write "&" as "&amp;" inside text. Member counts on the Members and Home pages
are counted automatically.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_all import *  # noqa: F401,F403  (shared helpers: head, footer, img, ICON, build_index, ...)


# ==========================================================================
# FACULTY
# ==========================================================================
FACULTY = [
    {
        "name": "Arjun Bagchi",
        "photo": "arjun-bagchi.webp",
        "web": "https://sites.google.com/view/arjunbagchi/",
        "inspire": "1043091",
        "interests": "String theory, gauge&nbsp;/&nbsp;gravity dualities, holography, CFTs.",
    },
    {
        "name": "Kaushik Bhattacharya",
        "photo": "kaushik-bhattacharya.webp",
        "web": "https://www.iitk.ac.in/dr-kaushik-bhattacharya",
        "inspire": "1019786",
        "interests": "Astroparticle physics, cosmology, gravitation.",
    },
    {
        "name": "Dipankar Chakrabarti",
        "photo": "dipankar-chakrabarti.webp",
        "web": "https://home.iitk.ac.in/~dipankar/",
        "inspire": "1014130",
        "interests": "QCD, lattice gauge theory and lightcone field theories.",
    },
    {
        "name": "Joydeep Chakrabortty",
        "photo": "joydeep-chakrabortty.webp",
        "web": "https://home.iitk.ac.in/~joydeep/",
        "inspire": "1023458",
        "interests": "Beyond the Standard Model, effective field theories, supergravity, supersymmetry.",
    },
    {
        "name": "Sabyasachi Chakraborty",
        "photo": "sabyasachi-chakraborty.webp",
        "web": "https://home.iitk.ac.in/~sabyac/",
        "inspire": "1250995",
        "interests": "Beyond the Standard Model, effective field theory, axions, phase transitions, supersymmetry.",
    },
    {
        "name": "Debtosh Chowdhury",
        "photo": "debtosh-chowdhury.webp",
        "web": "https://home.iitk.ac.in/~debtoshc/",
        "inspire": "1034163",
        "interests": "Beyond the Standard Model, cosmology and astroparticle physics, flavour physics, supersymmetry.",
    },
    {
        "name": "Diptarka Das",
        "photo": "diptarka-das.webp",
        "web": "https://home.iitk.ac.in/~didas/",
        "inspire": "1233200",
        "interests": "Non-equilibrium physics, two-dimensional theories, large-N theories.",
    },
    {
        "name": "Sanmay Ganguly",
        "photo": "sanmay-ganguly.webp",
        "web": "https://www.iitk.ac.in/sanmay-ganguly",
        "inspire": "1071689",
        "interests": "Experimental high energy physics, machine learning for HEP, BSM searches, jet studies at the LHC.",
    },
    {
        "name": "Apratim Kaviraj",
        "photo": "apratim-kaviraj.webp",
        "web": "https://www.iitk.ac.in/apratim-kaviraj",
        "inspire": "1238225",
        "interests": "Theoretical high energy physics, conformal field theories, critical phenomena.",
    },
    {
        "name": "Nilay Kundu",
        "photo": "nilay-kundu.webp",
        "web": "https://home.iitk.ac.in/~nilayhep/",
        "inspire": "1274025",
        "interests": "Classical and quantum gravity, quantum field theory, string theory, AdS/CFT.",
    },
    {
        "name": "Swagata Mukherjee",
        "photo": "swagata-mukherjee.webp",
        "web": "https://www.iitk.ac.in/swagata-mukherjee",
        "inspire": "1077596",
        "interests": "Collider physics, the CMS experiment at the LHC, BSM searches, machine learning.",
    },
    {
        "name": "Navaneeth Poonthottathil",
        "photo": "navaneeth-poonthottathil.webp",
        "web": "https://neutrinos-iitk.com/",
        "inspire": "1191574",
        "interests": "Experimental high energy physics, neutrino physics, long-baseline neutrino experiments.",
    },
    {
        "name": "Tapobrata Sarkar",
        "photo": "tapobrata-sarkar.webp",
        "web": "https://www.iitk.ac.in/dr-tapobrata-sarkar",
        "inspire": "990296",
        "interests": "String theory, gravity, information geometry, classical and quantum phase transitions, cosmology.",
    },
    {
        "name": "Gautam Sengupta",
        "photo": "gautam-sengupta.webp",
        "web": "https://home.iitk.ac.in/~sengupta/",
        "inspire": "1037280",
        "interests": "String theory, quantum gravity, holographic quantum entanglement.",
    },
]

# ==========================================================================
# POSTDOCTORAL FELLOWS
# ==========================================================================
POSTDOCS = [
    {
        "name": "Rituparna Ghosh",
        "photo": None,
        "web": None,
        "inspire": "2079276",
    },
    {
        "name": "Sudipta Show",
        "photo": "sudipta-show.webp",
        "web": None,
        "inspire": "https://inspirehep.net/authors?sort=bestmatch&size=25&page=1&q=Sudipto%20Show",
    },
    {
        "name": "Siddhartha Karmakar",
        "photo": None,
        "web": None,
        "inspire": "2663673",
    },
    {
        "name": "Sachin Grover",
        "photo": "sachin-grover.webp",
        "web": None,
        "inspire": "2139519",
    },
    {
        "name": "Baishali Roy",
        "photo": "baishali-roy.webp",
        "web": None,
        "inspire": "1912629",
    },
    {
        "name": "Ankit Anand",
        "photo": None,
        "web": None,
        "inspire": "1771806",
    },
    {
        "name": "Astha Kakkar",
        "photo": "astha-kakkar.webp",
        "web": None,
        "inspire": "2016459",
    },
    {
        "name": "Saikat Mondal",
        "photo": None,
        "web": None,
        "inspire": "2619972",
    },
]

# ==========================================================================
# GRADUATE STUDENTS
# ==========================================================================
STUDENTS = [
    {
        "name": "Abhijit Kishore",
        "photo": "abhijit-kishore.webp",
        "web": None,
        "inspire": "2870898",
    },
    {
        "name": "Ankit Gill",
        "photo": "ankit-gill.webp",
        "web": None,
        "inspire": "2851564",
    },
    {
        "name": "Sandip Biswas",
        "photo": None,
        "web": None,
        "inspire": "2209125",
    },
    {
        "name": "Himanshu Chourasiya",
        "photo": "himanshu-chourasiya.webp",
        "web": None,
        "inspire": "2026028",
    },
    {
        "name": "Arpan Hait",
        "photo": "arpan-hait.webp",
        "web": None,
        "inspire": "2514156",
    },
    {
        "name": "Saikat Biswas",
        "photo": None,
        "web": None,
        "inspire": "2727294",
    },
    {
        "name": "Amartya Saha",
        "photo": "amartya-saha.webp",
        "web": None,
        "inspire": "2126544",
    },
    {
        "name": "Ankur Dey",
        "photo": "ankur-dey.webp",
        "web": None,
        "inspire": "2750533",
    },
    {
        "name": "Anurag Sarkar",
        "photo": "anurag-sarkar.webp",
        "web": None,
        "inspire": "2773293",
    },
    {
        "name": "Priyanka Saha",
        "photo": "priyanka-saha.webp",
        "web": None,
        "inspire": "2338279",
    },
    {
        "name": "Subrata Samanta",
        "photo": "subrata-samanta.webp",
        "web": "https://home.iitk.ac.in/~samantaphy20/",
        "inspire": "2685933",
    },
    {
        "name": "Santanu Mandal",
        "photo": "santanu-mandal.webp",
        "web": None,
        "inspire": "2729840",
    },
    {
        "name": "Ritwika Ghoshal",
        "photo": None,
        "web": None,
        "inspire": None,
    },
    {
        "name": "Pushkar Soni",
        "photo": "pushkar-soni.webp",
        "web": None,
        "inspire": "2801474",
    },
    {
        "name": "Shibam Das",
        "photo": "shibam-das.webp",
        "web": None,
        "inspire": "3118318",
    },
    {
        "name": "Atanu Samanta",
        "photo": "atanu-samanta.webp",
        "web": None,
        "inspire": "2860792",
    },
    {
        "name": "Sharang Rajesh Iyer",
        "photo": "sharang-rajesh-iyer.webp",
        "web": None,
        "inspire": "3072837",
    },
    {
        "name": "Mudit Kumar",
        "photo": "mudit-kumar.webp",
        "web": None,
        "inspire": "2752420",
    },
    {
        "name": "Anuj Gupta",
        "photo": "anuj-gupta.webp",
        "web": None,
        "inspire": "2752428",
    },
    {
        "name": "MD Sariful Islam",
        "photo": "md-sariful-islam.webp",
        "web": None,
        "inspire": "2819696",
    },
    {
        "name": "Aryabrat Mahapatra",
        "photo": "aryabrat-mahapatra.webp",
        "web": "https://sites.google.com/view/web-profile-",
        "inspire": "2136625",
    },
    {
        "name": "Debmalya Dey",
        "photo": "debmalya-dey.webp",
        "web": None,
        "inspire": "2865271",
    },
    {
        "name": "Adarsh Panday",
        "photo": "adarsh-panday.webp",
        "web": None,
        "inspire": "2903795",
    },
    {
        "name": "Kaushik Kangsabanik",
        "photo": "kaushik-kangsabanik.webp",
        "web": None,
        "inspire": "2670488",
    },
    {
        "name": "Shashank Sharma",
        "photo": "shashank-sharma.webp",
        "web": None,
        "inspire": None,
    },
    {
        "name": "Kauship Saha",
        "photo": "kauship-saha.webp",
        "web": None,
        "inspire": None,
    },
    {
        "name": "Deepanshu Bisht",
        "photo": "deepanshu-bisht.webp",
        "web": "https://sites.google.com/view/deepdives",
        "inspire": "2817636",
    },
    {
        "name": "Nabin Kumar Pidikaka",
        "photo": "nabin-kumar-pidikaka.webp",
        "web": None,
        "inspire": None,
    },
    {
        "name": "Rounak Nath",
        "photo": "rounak-nath.webp",
        "web": None,
        "inspire": None,
    },
    {
        "name": "Debanjan Balui",
        "photo": "debanjan-balui.webp",
        "web": None,
        "inspire": "2893850",
    },
    {
        "name": "Niles Mondal",
        "photo": "niles-mondal.webp",
        "web": None,
        "inspire": None,
    },
    {
        "name": "Kowsona Chakraborty",
        "photo": "kowsona-chakraborty.webp",
        "web": None,
        "inspire": None,
    },
    {
        "name": "Saurabh Rai",
        "photo": "saurabh-rai.webp",
        "web": None,
        "inspire": None,
    },
    {
        "name": "Sandipan Rakshit",
        "photo": "sandipan-rakshit.webp",
        "web": "https://sites.google.com/view/sandipanr/home",
        "inspire": None,
    },
    {
        "name": "Saswata Chatterjee",
        "photo": "saswata-chatterjee.webp",
        "web": None,
        "inspire": None,
    },
    {
        "name": "Astha Tiwari",
        "photo": "astha-tiwari.webp",
        "web": None,
        "inspire": None,
    },
    {
        "name": "Suprajaa D",
        "photo": "suprajaa-d.webp",
        "web": None,
        "inspire": None,
    },
    {
        "name": "Adil Imam",
        "photo": "adil-imam.webp",
        "web": None,
        "inspire": None,
    },
    {
        "name": "Arkachur Bhattacharya",
        "photo": "arkachur-bhattacharya.webp",
        "web": None,
        "inspire": "3072456",
    },
    {
        "name": "Sunny Keshri",
        "photo": "sunny-keshri.webp",
        "web": None,
        "inspire": None,
    },
    {
        "name": "Siddhartha Bandyopadhyay",
        "photo": "siddhartha-bandyopadhyay.webp",
        "web": None,
        "inspire": "2833773",
    },
]

# ==========================================================================
# ALUMNI  (newest at the bottom, as on the page)
# ==========================================================================
ALUMNI = [
    {"name": "Prabwal Phukon", "role": "PhD 2014", "now": "Assistant Professor, Department of Physics, Dibrugarh University."},
    {"name": "Subhash Mahapatra", "role": "PhD 2015", "now": "Assistant Professor, Department of Physics, NIT Rourkela."},
    {"name": "Chandan Mondal", "role": "PhD 2016", "now": "Associate Professor, Institute of Modern Physics, Lanzhou, China."},
    {"name": "Anshuman Dey", "role": "PhD 2017", "now": "Postdoc, University of Santiago de Compostela, Spain."},
    {"name": "Jishnu Goswami", "role": "PhD 2017", "now": "Postdoc, Advanced Institute for Computational Science, RIKEN, Japan."},
    {"name": "Tripurari Srivastava", "role": "PhD 2018", "now": "D. S. Kothari Fellow, Delhi University."},
    {"name": "Pratim Roy", "role": "PhD 2018", "now": "Postdoc, HRI, India."},
    {"name": "Aditya Mehra", "role": "PhD 2018", "now": "University of Edinburgh."},
    {"name": "Tanmay Maji", "role": "PhD 2018", "now": "Assistant Professor, NIT Kurukshetra."},
    {"name": "Dipanjan Dey", "role": "PhD 2019", "now": "Postdoc, Dalhousie University, Canada."},
    {"name": "Saikat Chakraborty", "role": "PhD 2019", "now": "Postdoc, North West University, South Africa."},
    {"name": "Pulastya Parekh", "role": "PhD 2020", "now": "Postdoc, CECS, Valdivia, Chile."},
    {"name": "Suvankar Paul", "role": "PhD 2020", "now": "Lecturer in Physics, Maynaguri Govt. Polytechnic, West Bengal."},
    {"name": "Rinku Maji", "role": "PhD 2022", "now": "Postdoc, South Korea."},
    {"name": "Supratim Das Bakshi", "role": "PhD 2022", "now": "Postdoc, University of Granada."},
    {"name": "Anisha", "role": "PhD 2022", "now": "Postdoc, University of Glasgow."},
    {"name": "Poulami Nandi", "role": "PhD 2022", "now": "Postdoc, IIT Gandhinagar."},
    {"name": "Pritam Banerjee", "role": "PhD 2022", "now": "NPDF, IIT Kharagpur."},
    {"name": "Sandip Chowdhury", "role": "PhD 2022", "now": ""},
    {"name": "Himadri Roy", "role": "PhD 2023", "now": ""},
    {"name": "Bidyut Dey", "role": "PhD 2023", "now": "University of Calabria (INFN), Cosenza, Italy."},
    {"name": "Kunal Pal", "role": "PhD 2023", "now": ""},
    {"name": "Kuntal Pal", "role": "PhD 2023", "now": ""},
    {"name": "Sanchari Pal", "role": "PhD 2023", "now": ""},
    {"name": "Shakeel Ur Rahaman", "role": "PhD 2023", "now": "Durham University, IPPP."},
    {"name": "Suraj Prakash", "role": "PhD 2023", "now": "University of Valencia, IFIC, Spain."},
    {"name": "Saddam Hussain", "role": "PhD 2023", "now": ""},
    {"name": "Shaswata Chowdhury", "role": "PhD 2023", "now": "IMSc, Chennai."},
    {"name": "Minhajul Islam", "role": "PhD 2023", "now": ""},
    {"name": "Poonam Choudhary", "role": "PhD 2024", "now": ""},
    {"name": "Mamta Gautam", "role": "PhD 2024", "now": ""},
    {"name": "Prateksh Dhivakar", "role": "PhD 2024", "now": "University of Victoria, Canada."},
    {"name": "Nitesh Jaiswal", "role": "PhD 2024", "now": "IIT Bombay."},
    {"name": "Punit Sharma", "role": "PhD 2024", "now": ""},
    {"name": "Upalaparna Banerjee", "role": "PhD 2024", "now": "University of Mainz, Germany."},
    {"name": "Ankur Singha", "role": "PhD 2024", "now": "TU Berlin."},
    {"name": "Vinayak Raj", "role": "PhD 2024", "now": "Huzhou University (ZJHU)."},
    {"name": "Mir Afrasiar", "role": "PhD 2024", "now": "Shanghai University (SHU)."},
    {"name": "Debojyoti Garain", "role": "PhD 2024", "now": "Clemson University."},
    {"name": "Bheemsehan Gurjar", "role": "PhD 2024", "now": "IIT Kanpur."},
    {"name": "Sudipta Dutta", "role": "PhD 2024", "now": "Université Libre de Bruxelles, Belgium."},
    {"name": "Ritankar Chatterjee", "role": "PhD 2024", "now": "IIT Ropar, India."},
    {"name": "Pinaki Banerjee", "role": "Postdoc", "now": "IAS Princeton."},
    {"name": "Sunanda Patra", "role": "Postdoc", "now": "Assistant Professor, Vidyasagar College, Kolkata."},
    {"name": "Shankhadeep Chakrabortty", "role": "Postdoc", "now": "Assistant Professor, IIT Ropar."},
    {"name": "Zodinmawia", "role": "Postdoc", "now": "Assistant Professor, Department of Physics, Mizoram University, Aizawl."},
    {"name": "Suchetan Das", "role": "Postdoc", "now": ""},
    {"name": "Mangesh Mandlik", "role": "Postdoc", "now": "Assistant Professor, IIT (ISM) Dhanbad."},
    {"name": "Kedar S. Kolekar", "role": "Postdoc", "now": "Postdoc, Tsinghua University, Beijing."},
    {"name": "Debangshu Mukherjee", "role": "Postdoc", "now": "Postdoc, APCTP, Pohang."},
    {"name": "Taniya Mandal", "role": "Postdoc", "now": "SERB–Ramanujan Fellow, NISER, Bhubaneswar."},
    {"name": "Anirban Chatterjee", "role": "Postdoc", "now": "Ningbo University (NBU)."},
    {"name": "Jaydeb Das", "role": "Postdoc 2024", "now": "IIT Guwahati, India."},
    {"name": "Sarath N", "role": "Postdoc 2025", "now": "Assistant Professor, SR University, Warangal."},
    {"name": "Poulami Mondal", "role": "Postdoc 2025", "now": "TIFR Mumbai."},
    {"name": "Nabarun Chakrabarty", "role": "INSPIRE Faculty", "now": "Assistant Professor, Visva-Bharati University, West Bengal."},
    {"name": "Indrani Chakraborty", "role": "INSPIRE Faculty", "now": "Assistant Professor (Senior Grade), Jaypee Institute of Information Technology."},
    {"name": "Subhendra Mohanty", "role": "Visiting Faculty", "now": "IISER Bhopal."},
]

# ==========================================================================
# PAGE LAYOUT  —  you rarely need to change anything below
# ==========================================================================
INSPIRE = "https://inspirehep.net/authors/"


def pub_url(ref):
    if not ref:
        return None
    if ref.startswith("http"):
        return ref
    return INSPIRE + ref + "?ui-citation-summary=true"


def person_card(p, variant=""):
    name, web, interests = p["name"], p.get("web"), p.get("interests", "")
    pu = pub_url(p.get("inspire"))
    links = []
    if web:
        links.append(ext(web, "Web", "globe"))
    if pu:
        links.append(ext(pu, "Publications", "doc"))
    else:
        links.append('<span class="chip chip--muted">' + ICON["doc"] + "<span>Publications</span></span>")
    key = html.escape((name + " " + (interests or "")).lower(), quote=True)
    photo = img("Members/" + p["photo"], name) if p.get("photo") else ""
    return f"""        <article class="person {variant}" data-person="{key}">
          <span class="person__avatar">{photo}<span aria-hidden="true">{initials(name)}</span></span>
          <div class="person__body">
            <h3 class="person__name">{name}</h3>
            <p class="person__interests"><b>Interests</b> {interests}</p>
            <div class="person__links">{''.join(links)}</div>
          </div>
        </article>"""


def roster_item(p):
    name, web = p["name"], p.get("web")
    pu = pub_url(p.get("inspire"))
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
    photo = img("Members/" + p["photo"], name) if p.get("photo") else ""
    return f"""          <li data-person="{key}"><div class="wall__item">
            <span class="wall__photo">{photo}<span aria-hidden="true">{initials(name)}</span></span>
            <span class="wall__name">{name}</span>
            <span class="wall__links">{''.join(links)}</span>
          </div></li>"""


def build():
    fac = "\n".join(person_card(p) for p in FACULTY)
    post = "\n".join(roster_item(p) for p in POSTDOCS)
    stud = "\n".join(roster_item(p) for p in STUDENTS)
    alum = "\n".join(
        f'          <li data-person="{html.escape((a["name"] + " " + a["now"]).lower(), quote=True)}">'
        f'<span class="alumni__name">{a["name"]}</span>'
        f'<span class="alumni__year">{a["role"]}</span>'
        f'<span class="alumni__now">{a["now"] or "—"}</span></li>'
        for a in ALUMNI
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
      art="members",
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
      <div class="people" data-reveal="once">
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


if __name__ == "__main__":
    build()
    build_index()  # refresh the Home page (index.html) too
