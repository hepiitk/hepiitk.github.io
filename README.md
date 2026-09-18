# High Energy Physics @ IIT Kanpur — group website

The website of the High Energy Physics group at the Department of Physics,
Indian Institute of Technology Kanpur.

**Live site → <https://hepiitk.github.io/website/>**

Plain static HTML and CSS: seven pages, one stylesheet, no framework, no build
pipeline. GitHub Pages serves the files in `main` exactly as they are, so a
commit to `main` *is* a deployment.

---

## Repository layout

```
index.html            Home — group blurb, counts, research areas, latest news
members.html          Faculty · postdocs · graduate students · alumni (live search)
research.html         The three subgroups, then a gallery of result figures
seminars.html         Seminar calendar, particle journal club, string journal club
conferences.html      In-house symposia with posters, conferences & workshops
news.html             Updates, postdoc positions, PMRF, funding
contact.html          Group contact details, editor team

assets/style.css      The whole design system (~1250 lines, commented by section)
assets/app.js         Mobile menu, member search, scroll reveal, count-up
assets/favicon.svg    Tab icon
assets/img/*.svg      Seven line drawings made for this site (see below)

assets/Members/       Member portraits              ─┐
assets/Research/      Result figures                 │  photographs carried over
assets/News/          Funding-agency logo strip      │  from the old Google Sites
assets/ConferenceWorkshop/  Symposium posters        │  site
assets/Home/          Home page photo                │
assets/Seminars/      Seminars banner               ─┘
assets/iitk-logo.jpg  Institute emblem in the masthead

_source/build.py      Page generator — all site content lives here
```

`_source/` is not part of the published site; it holds the generator that
writes the seven HTML files.

---

## Making a change

Two routes. Pick whichever suits the edit.

### A. Small fix — edit the HTML directly

Every page is plain, readable HTML. Fixing a typo or a link in
`members.html` through GitHub's web editor is perfectly fine. Commit to `main`
and the live site updates in a minute or two.

### B. Anything structural — edit `_source/build.py` and regenerate

All content lives in named Python lists at the top of that file, and the
generator writes every page from them. This keeps the seven pages consistent
and keeps the counts on the home page honest.

```bash
git clone https://github.com/hepiitk/website.git
cd website
python3 _source/build.py        # rewrites the seven .html files
python3 -m http.server 8000     # then open http://localhost:8000
```

Commit the regenerated `.html` files together with your change to
`build.py`.

| To change… | Edit |
|---|---|
| Faculty (name, homepage, INSPIRE id, interests) | `FACULTY` |
| Postdocs, graduate students | `POSTDOCS`, `STUDENTS` |
| Alumni (name, degree + year, current position) | `ALUMNI` |
| Which portrait belongs to whom | `PHOTOS` |
| Research subgroups, topic lists, accent colour | `THRUSTS` |
| In-house symposia (dates, poster, schedule sheet) | `SYMPOSIA` |
| Other conferences and workshops | `CONFERENCES` |
| News items | `NEWS` |
| PMRF fellows, editor team | `PMRF`, `EDITORS` |
| Banners, home photo, research figures, funding strip | `BANNERS`, `HERO_PHOTO`, `RESEARCH_FIGURES`, `NEWS_FUNDERS_IMG` |
| The drawn illustrations and where they appear | `ART`, `PAGE_ART` |

### Worked examples

**A new graduate student.** Two lines — one in `STUDENTS`, one in `PHOTOS`:

```python
STUDENTS = [
    ...
    ("Priya Nair", None, "2912345"),        # name, personal site, INSPIRE author id
]

PHOTOS = {
    ...
    "Priya Nair": "priya-nair.jpg",         # file goes in assets/Members/
}
```

Only the INSPIRE **author id** is needed — the full citation-summary URL is
built automatically. Use `None` for a missing personal page or INSPIRE profile;
the Publications chip is then shown greyed out rather than linking nowhere. The
"40 graduate students" figure on the home page and in the section heading is
counted from the list, so it can never drift.

**A news item.** Newest first, at the top of `NEWS`:

```python
{
    "tag": "Award",
    "title": "Humboldt Fellowship for …",
    "body": "One or two sentences. &amp; for an ampersand.",
    "link": None,                            # or ("conferences.html#symposium-2026", "Schedule")
},
```

The four most recent items also appear on the home page automatically.

**Someone finishing their PhD.** Move their tuple from `STUDENTS` to `ALUMNI`
with the year and where they have gone:

```python
("Priya Nair", "PhD 2026", "Postdoc, University of Bonn, Germany."),
```

---

## Images

Photographs live in the `assets/` subfolders listed above, under the filenames
the pages reference. **Every image degrades gracefully** — each one carries a
failure handler, so a file that is missing or misnamed removes itself instead of
leaving a broken-image icon:

| Missing file | What a visitor sees |
|---|---|
| A member portrait | The person's initials in a framed box, same size |
| `assets/iitk-logo.jpg` | The drawn atom mark in the masthead |
| The home page photo | A line engraving of a detector with collision tracks |
| A page banner | No banner, and no gap |
| A symposium poster | The entry without its poster |
| Every research figure | The "Selected figures" section disappears entirely |
| The funding strip | Dashed agency-name placeholders |

So images can be added or replaced one at a time without ever breaking the
site.

### The drawn artwork (already in the repo)

Seven original line drawings in `assets/img/`, in the site's own ink-and-maroon
palette. Nothing to download, nothing to license:

| File | Where it appears |
|---|---|
| `theory.svg` — one-loop Feynman diagram | Home card and Particle Theory panel |
| `experiment.svg` — detector barrel with jet cones | Home card and Particle Experiments panel |
| `string.svg` — AdS cylinder with a bulk geodesic | Home card and String Theory panel |
| `seminar.svg` — blackboard and lectern | Seminars masthead |
| `symposium.svg` — auditorium and screen | Conference / Workshop masthead |
| `news.svg` — noticeboard | News masthead |
| `contact.svg` — letter and department building | Contact masthead |

To put a photograph in place of one, drop it in `assets/img/` and change the
path in `ART` in `_source/build.py`.

---

## Embedded Google content

The seminar calendar and every symposium schedule are live embeds pointing at
the group's existing Google Calendar and Sheets — nothing was re-uploaded. They
must stay shared as **"anyone with the link can view"** or they will render
blank for visitors.

---

## Design and accessibility notes

- **Design tokens.** Every colour, type step, space step and radius is a CSS
  custom property in `:root` in `assets/style.css`. Changing `--maroon`
  re-tints the whole site; `--paper` sets the paper tone.
- **Typography.** EB Garamond for display, Source Serif 4 for text, Inter for
  the small uppercase labels, loaded from Google Fonts with Georgia/system
  fallbacks — the site stays fully legible if that request is blocked.
- **Member photographs are large**, as on the old site: faculty portraits at 4:5
  beside their interests, and postdocs and students as a photo wall six across
  on a wide screen.
- **Accessibility.** Skip link, one `<h1>` per page, ordered headings, visible
  focus rings, `prefers-reduced-motion` honoured, keyboard-dismissable mobile
  menu, `alt` text on every image, and all text at 4.5:1 contrast or better.
- **Print.** A dedicated print stylesheet drops the navigation, banners and
  embeds, prints link targets in parentheses, and keeps member entries from
  splitting across pages — so the member list and schedules print cleanly.
- **JavaScript is optional.** `assets/app.js` only adds the mobile menu, the
  member search, the reveal animation and the count-up. With JS disabled
  everything is still present and readable.

---

## Housekeeping

- [ ] `styles.css` in the repository root is left over from the previous site
      and is not referenced by any page — safe to delete.
- [ ] Add an empty `.nojekyll` file at the root. GitHub Pages runs Jekyll by
      default, which skips folders beginning with an underscore and may
      reinterpret braces in page content; `.nojekyll` turns that off and
      publishes the files verbatim.
- [ ] The postdoc advertisement on `news.html` still describes the 2022–23
      round (as the old site did) and says so explicitly — update the text and
      the portal link when the next call opens.
- [ ] A few alumni entries have no current position recorded.

---

## Maintainers

The site is maintained by the group's editor team — see
[contact.html](https://hepiitk.github.io/website/contact.html). For
corrections, new publications or news items, write to
**hepiitk@gmail.com**, or open an issue or pull request here.
