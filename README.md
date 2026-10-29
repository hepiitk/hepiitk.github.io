# High Energy Physics @ IIT Kanpur — group website

The website of the High Energy Physics group, Department of Physics, IIT Kanpur.

**Live site → <https://hepiitk.github.io/>**

The site is plain HTML and CSS, written by **five small Python scripts** in the
`_source/` folder. The names, photos, news, dates and links sit in simple lists
inside them. To update a page you edit the list, run the script, push the
result to the **`web`** branch on GitHub, and then merge it into **`main`** with a
**pull request**. About a minute after the merge, the live site updates.

**Repository → <https://github.com/hepiitk/hepiitk.github.io>**

This guide is written for a new editor who has never used Git, Python or edited a
website before. Read [How the site is published](#how-the-site-is-published) and Part 1 once to
get set up. After that you only need Part 2 (the everyday routine) and Part 3
(how to update each page).

---

## Contents

- [Where everything is](#where-everything-is)
- [How the site is published: the `web` and `main` branches](#how-the-site-is-published)
- [Part 1 — One-time setup](#part-1--one-time-setup)
- [Part 2 — The everyday routine: pull → edit → build → check → commit → push → pull request → merge](#part-2--the-everyday-routine)
- [Part 3 — How to update each page](#part-3--how-to-update-each-page)
- [Part 4 — When something goes wrong](#part-4--when-something-goes-wrong)
- [Part 5 — Quick reference](#part-5--quick-reference)

---

## Where everything is

```
index.html          Home page
members.html        Faculty, postdocs, graduate students, alumni
research.html       Research areas, each with a slideshow of figures from recent papers
seminars.html       Seminar calendar and journal clubs
conferences.html    In-house symposia, conferences and workshops
news.html           News, postdoc positions, PMRF fellows, funding
contact.html        Contact details and the editor team

_source/                  The five scripts that write the pages above
  build_members.py        → members.html      + refreshes index.html
  build_news.py           → news.html         + refreshes index.html
  build_conferences.py    → conferences.html  + refreshes index.html
  build_research.py       → research.html     + refreshes index.html
  build_all.py            → ALL seven pages. Also holds everything the pages share
                            (menu, footer, e-mail, phone) and the pages that rarely
                            change: Home, Seminars, Contact.

assets/style.css    The design: colours, fonts, spacing, layout (all pages share it)
assets/app.js       Small scripts: mobile menu, member search, slide-in effects
assets/carousel.js  The figure slideshows on the Research page
assets/merger.js    The neutron-star animation on the Home page
assets/Members/     Member photos, named after the person: priya-nair.webp
assets/ConferenceWorkshop/   Symposium posters: symposium-2026.webp
assets/Research/    Figures for the Research slideshows (made by build_research.py --figures)
assets/img/         Line drawings beside page titles and on the Home page cards
.gitignore          Tells Git to ignore Python's __pycache__ folder and stray .DS_Store files
```

> **The one rule to remember: change the script, not the HTML.**
> Every time a script runs it **rewrites its page** from the lists inside it.
> Anything typed straight into that `.html` file is lost. So for `members.html`
> you edit `_source/build_members.py`, for `news.html` you edit
> `_source/build_news.py`, and so on.
>
> - `_source/` should contain **only these five `.py` files**.
> - `assets/style.css` and the `.js` files in `assets/` are *not* written by any
>   script, so you edit them directly.

---

## How the site is published

The repository has two branches (two versions of the site side by side):

| Branch | What it is | Who can change it |
|---|---|---|
| **`main`** | **The live site.** GitHub Pages publishes whatever is on `main` to <https://hepiitk.github.io/>. | Nobody pushes to it directly. Changes reach it **only through a pull request**. |
| **`web`** | **The shared working branch.** Editors commit and push their changes here. Pushing to `web` does **not** change the live site. | Every editor. |
| *your own branch* (optional) | A separate copy for a bigger or experimental change, e.g. `new-research-figures`. See [Working on your own branch](#working-on-your-own-branch). | Whoever made it. |

```
 your computer ──push──▶  web  (or your own branch) ──pull request + merge──▶  main ──▶  hepiitk.github.io
```

**Who can do what.**

| Who | Role on the repository | Can |
|---|---|---|
| The **editor** team (`@hepiitk/editor`) | Maintain | push to `web` and to their own branches, open pull requests into `main`, and merge them |
| Repository and organisation admins | Admin | the same, plus the repository settings |

**The rules on `main`** (a *ruleset* named **main**, under **Settings → Rules → Rulesets**):

- **A pull request is required.** Every change to `main` comes from another branch through a pull request.
- **No approval is needed.** You can merge your own pull request. For a big change, ask another editor to look at it first anyway.
- **The merge method is *Merge*.** The **Merge pull request** button keeps every commit.
- **`main` can't be deleted or force-pushed.**
- Admins are on the ruleset's *bypass list*, so GitHub would let them push straight to `main`.
  **Please use a pull request anyway**, so every change to the live site is recorded in one place.

---

## Part 1 — One-time setup

You only do this once per computer.

### 1.1 Get access to the repository

1. Make a free account at <https://github.com> if you don't have one.
2. Send your GitHub username to a current editor (see [contact.html](https://hepiitk.github.io/contact.html))
   and ask an admin to add you to the **editor** team of the `hepiitk` organisation.
   The team has the **Maintain** role on the repository, which is everything an editor needs.
   *An admin does this on GitHub: <https://github.com/orgs/hepiitk/teams/editor> → **Add a member**.*
3. Accept the invitation from the email GitHub sends you. You can also accept it on
   <https://github.com/hepiitk> while signed in.

### 1.2 Install the tools

These instructions are for **Debian-based Linux** (Debian, Ubuntu, Linux Mint, Pop!_OS…).

You need: **Git** (tracks changes and talks to GitHub), **Python 3** (runs the
page scripts), **ImageMagick** (shrinks photos, see [3.7](#37-photos-and-images)),
**poppler-utils** and **Ghostscript** (convert research figures, see
[3.4](#34-research--_sourcebuild_researchpy)) and **VS Code** (the editor you'll work in).

Open a terminal (`Ctrl+Alt+T`) and run:

```bash
sudo apt update
sudo apt install git python3 imagemagick poppler-utils ghostscript
```

For **VS Code**, download the **`.deb`** package from <https://code.visualstudio.com>,
then install it from the folder you downloaded it to:

```bash
cd ~/Downloads
sudo apt install ./code_*.deb
```

Start it from your applications menu, or by typing `code` in a terminal.

Nothing else is needed. The scripts use only what comes with Python.

Check everything works:

```bash
git --version
python3 --version
mogrify -version
```

Each should print a version number.

**Recommended VS Code extensions.** Open the **Extensions** panel (the
four-squares icon on the left, or `Ctrl+Shift+X`) and install:

- **Python** (by Microsoft): colours the scripts and underlines mistakes in red.
- **Live Server** (by Ritwick Dey): shows the pages in your browser and refreshes them as they change.

### 1.3 Tell Git who you are

Git labels every change with a name and email. In the VS Code terminal, run
these two lines with your own details:

```bash
git config --global user.name  "Your Name"
git config --global user.email "your-email@iitk.ac.in"
```

Use the same email as your GitHub account if you can. Your commits then show up
on your GitHub profile.

Also run this once. It tells Git to *merge* when you pull changes that someone
else made, so a pull never stops with a question about "divergent branches":

```bash
git config --global pull.rebase false
```

### 1.4 Download (clone) the website to your computer

1. Open VS Code.
2. Click the **Source Control** icon on the left: three dots joined by lines, or
   `Ctrl+Shift+G`.
3. Click **Clone Repository**. Alternatively, press `Ctrl+Shift+P`, type **Git: Clone** and press Enter.
4. Paste this address and press Enter:
   ```
   https://github.com/hepiitk/hepiitk.github.io.git
   ```
5. Choose a folder to keep it in, for example `Documents`. A folder called
   `hepiitk.github.io` is created there.
6. When VS Code asks **"Would you like to open the cloned repository?"**, click **Open**.
7. The first time you push, VS Code asks you to **sign in to GitHub**. Click
   **Allow**, finish the sign-in in your browser, then come back to VS Code.

8. **Switch to the `web` branch.** The bottom-left corner of VS Code shows the
   branch you're on, probably `main`. Click it, and in the list that opens choose
   **`origin/web`**. VS Code makes a local `web` branch linked to the one on
   GitHub. The bottom-left corner now says **`web`**.

You now have your own copy of the site. You won't need to clone again. VS Code
remembers the branch, so next time it opens on `web`.

---

## Part 2 — The everyday routine

Every time you update the site, follow these eight steps in this order. Steps
1–6 happen in VS Code on the **`web`** branch. Steps 7–8 happen on the GitHub
website and are what put the change on the live site.

```
 1. PULL  →  2. EDIT  →  3. BUILD  →  4. CHECK  →  5. COMMIT  →  6. PUSH  →  7. PULL REQUEST  →  8. MERGE
 (get the    (change     (run the     (look at it  (save a       (send it    (ask to copy        (copy it to
  latest)     the         script)      in a         snapshot)     to web on   web into main)      main: it goes
              script)                  browser)                   GitHub)                         live)
```

### Step 1 — Pull: get the latest version first

Other editors may have changed the site since you last worked on it. Always pull
before you start, or you'll end up editing an old copy.

- In VS Code, open the **hepiitk.github.io** folder (**File → Open Recent**).
- Check that the bottom-left corner says **`web`**. If it says `main`, click it and
  choose `web` (see [1.4](#14-download-clone-the-website-to-your-computer), step 8).
  **Never work on `main`**: GitHub refuses pushes to it.
- Go to **Source Control** → click **⋯** (*Views and More Actions*) at the top of the panel → **Pull**.
- Or click the **circular arrows** next to the branch name `web` in the bottom-left status bar.

### Step 2 — Edit the page's script

In the **Explorer** panel (the two-pages icon), open the `_source` folder and then
the script for the page you want to change, for example `build_members.py` for
the Members page. Each script starts with a short note explaining every field,
followed by the lists you edit, under headings like:

```python
# ==========================================================================
# GRADUATE STUDENTS
# ==========================================================================
```

Part 3 shows exactly what to change for each task. Save with `Ctrl+S`.

> Lower down, under *"PAGE LAYOUT — you rarely need to change anything below"*,
> is the code that turns the lists into HTML. You don't need to touch it to
> add people, news or events.

### Step 3 — Build: run the script

In the VS Code terminal (**Terminal → New Terminal**; it opens in the
`hepiitk.github.io` folder), run the script you edited:

```bash
python3 _source/build_members.py
```

It prints which pages it wrote: its own page, and then the Home page, which
shows the member counts, the latest news and the research areas:

```
wrote members.html (74 KB)
wrote index.html (15 KB)
```

**Even easier:** with the script open in VS Code, click the **▶ Run Python File**
button at the top right of the editor. It does the same thing.

Edited `build_all.py`, or not sure which script to run? `python3 _source/build_all.py`
rebuilds all seven pages. It's always safe.

If you see an error instead of `wrote …`, nothing was changed. See
[Python errors](#a-python-error-appeared-when-i-ran-a-script) in Part 4.

### Step 4 — Check it in the browser

Never push a change you haven't looked at.

- **With Live Server:** right-click the `.html` file in the Explorer → **Open with
  Live Server**. A browser tab opens. Each time you re-run the script, it refreshes.
- **Without it:** open the file from your file manager, or run `xdg-open members.html` in the terminal.

Check that:

- the page looks right and nothing has shifted or disappeared,
- any new photo appears (not just the person's initials),
- any new links open the right page.

> The Google calendar and schedule sheets only load when you're online. If they
> look blank in your preview while you're offline, that's normal.

### Step 5 — Commit: save a labelled snapshot

1. Open **Source Control** (`Ctrl+Shift+G`). Your changed files are listed under
   **Changes**. You should see **both** the script you edited (e.g.
   `_source/build_members.py`) **and** the page(s) it wrote (e.g. `members.html`,
   `index.html`). Commit them together.
2. **Click each file** to see exactly what changed: red is removed, green is
   added. Make sure you only changed what you meant to.
3. Hover over **Changes** and click **+** (*Stage All Changes*). The files move to **Staged Changes**.
4. Type a short message in the box at the top saying **what** you changed, e.g.
   - `Add Priya Nair to graduate students`
   - `News: Humboldt fellowship for Rahul Verma`
   - `Add 2027 symposium`
5. Click **✓ Commit**.

> **Only a `.py` file changed, and no `.html`?** You forgot Step 3. Run the
> script, then stage the `.html` files too. GitHub publishes the `.html` files,
> not the scripts.

You can make several commits on `web` (one per change) before going on to
Step 6, or push after each one.

### Step 6 — Push: send it to the `web` branch

After committing, the blue button changes to **Sync Changes ↑1**. Click it.
This pushes your commit to the `web` branch on GitHub and also pulls anything new.

**The live site has not changed yet.** Your commit is now on `web`, waiting to be
merged into `main`.

### Step 7 — Open a pull request from `web` into `main`

A *pull request* (PR) is GitHub's way of saying "please copy these commits from
`web` into `main`". It shows exactly what will change before anything goes live.

1. Open <https://github.com/hepiitk/hepiitk.github.io>.
2. **If a pull request from `web` is already open**, you don't need a new one: the
   **Pull requests** tab shows it (for example *#1*), and your new commits have
   been added to it automatically. Go to Step 8.
3. Otherwise, GitHub shows a yellow bar *"web had recent pushes"*. Click
   **Compare & pull request**. If the bar isn't there: **Pull requests** tab →
   **New pull request**, then set **base: `main`** ← **compare: `web`**.
4. Give it a title saying what changed (e.g. `Add Priya Nair to graduate students`)
   and click **Create pull request**.
5. Open the **Files changed** tab and check that only what you meant to change is there.

### Step 8 — Merge: put it on the live site

1. On the pull request page, click **Merge pull request** → **Confirm merge**.
   No approval is needed, so you can merge your own pull request. For a big
   change, ask another editor to look at the **Files changed** tab first.
2. GitHub then offers a **Delete branch** button. **Don't delete `web`**: everyone
   works on it. (Deleting your *own* branch after its merge is fine.)
3. Check that it's live:
   - Open the repository's **Actions** tab. The newest run, **pages build and
     deployment**, turns from a **yellow dot** into a **green tick ✓** in about
     1–2 minutes. (You can also see it under **Deployments → github-pages** on the
     repository's front page.)
   - Open <https://hepiitk.github.io/> and do a **hard refresh**
     (`Ctrl+Shift+R`) so your browser doesn't show an old copy.

> **The Merge button is grey?**
> - *"This branch is out-of-date with the base branch"*: click **Update branch**,
>   then merge. Then **Pull** in VS Code before your next edit.
> - *"This branch has conflicts that must be resolved"*: see
>   [Merge conflict](#merge-conflict) in Part 4.

That's the whole routine.

### Working on your own branch

For a bigger change that will take several days, or one you want someone to
look at before it goes live (a new page layout, a batch of research figures),
make your own branch instead of using `web`:

1. Click the branch name in the bottom-left corner → **Create new branch from…** →
   choose **`origin/main`** → type a short name with hyphens, e.g.
   `new-research-figures`, and press Enter.
2. Work as usual (Steps 2–5).
3. The first time, the **Sync Changes** button says **Publish Branch**. Click it.
4. Open a pull request with **base: `main`** ← **compare: `new-research-figures`**
   (Step 7), and merge it when it's ready (Step 8). This time you *can* click
   **Delete branch** afterwards.
5. Back in VS Code, click the branch name and switch back to **`web`**, then **Pull**.

> If someone merged their own branch into `main`, `web` no longer has their
> changes. GitHub shows this on your next pull request as *"out-of-date"*;
> click **Update branch** there (Step 8) and then **Pull** in VS Code.

---

## Part 3 — How to update each page

### 3.0 Reading the lists: just enough Python

The data in the scripts looks like this. You only need these few rules:

```python
STUDENTS = [                                  # a list starts with [
    {                                         # one person = one { … } block
        "name": "Amit Sharma",                # "field": value,
        "photo": "amit-sharma.webp",
        "web": None,
        "inspire": "1111111",
    },                                        # the block ends with },
    {
        "name": "Neha Gupta",
        …
    },
]                                             # … and the list ends with ]
```

- **Text goes in double quotes:** `"Priya Nair"`. Keep both quote marks.
- **Every line is `"field": value,`.** Keep the field name exactly as it is
  (lowercase), the **colon** after it, and the **comma** at the end.
- **`None`** (capital N, no quotes) means "nothing here", e.g. no personal website.
- **`True` / `False`** (capital first letter, no quotes) switch something on or off.
- **Every block ends with `},`**, including the last one. A missing comma is the most common mistake.
- **Lines starting with `#` are notes** for humans. Python ignores them.
- **Write `&` as `&amp;`** inside text (e.g. `"Cosmology &amp; astroparticle physics"`),
  because the text goes into HTML.
- **The order in the list is the order on the page.**
- **The safest way to add anything:** copy an existing block, paste it where the
  new one should go, and change only the text inside the quotes.

---

### 3.1 Members — `_source/build_members.py`

Builds `members.html`, then refreshes `index.html`. The member counts on both
pages (*"14 faculty, 8 postdoctoral fellows…"* and the big numbers on the Home
page) are **counted automatically**. You never type them.

Everything about a person (name, photo, links, interests) is in **their own
`{ … }` block**. There is no separate photo list.

#### Add a graduate student or postdoc

1. Put their photo in `assets/Members/`, named after them: `priya-nair.webp`
   (see [3.7](#37-photos-and-images)).
2. Find the `GRADUATE STUDENTS` heading (or `POSTDOCTORAL FELLOWS`), copy any
   block, paste it where the new person should appear, and fill it in:

```python
    {
        "name": "Priya Nair",
        "photo": "priya-nair.webp",
        "web": "https://example.com/priya-nair/",
        "inspire": "2912345",
    },
```

| Field | What to put | If there's nothing |
|---|---|---|
| `"name"` | Full name, exactly as it should appear | — |
| `"photo"` | Just the **file name** of the picture in `assets/Members/` (not the folder) | `None` → their initials are shown |
| `"web"` | Personal web page, starting with `https://` | `None` → no globe icon |
| `"inspire"` | Just the number from their INSPIRE profile address (`inspirehep.net/authors/`**`2912345`**), or a full `https://…` link to any publication list | `None` → no publications icon |

3. Run `python3 _source/build_members.py`.

A new student with no photo and no links yet is simply:

```python
    {
        "name": "Priya Nair",
        "photo": None,
        "web": None,
        "inspire": None,
    },
```

#### Add a faculty member

Faculty blocks (under the `FACULTY` heading) have one more field, the interests:

```python
    {
        "name": "Priya Nair",
        "photo": "priya-nair.webp",
        "web": "https://example.com/priya-nair/",
        "inspire": "1234567",
        "interests": "Neutrino physics, detector development.",
    },
```

The search box on the page searches both the name and the interests automatically.

#### Add or change someone's photo

Put the picture in `assets/Members/` and write its file name in that person's
`"photo"` field. To replace a photo, either overwrite the old file with a new
picture of **the same name** (no script needed), or add the new file and change
`"photo"`.

#### Someone finishes their PhD, or leaves

1. **Delete** their whole `{ … },` block from `STUDENTS` (or `POSTDOCS` / `FACULTY`).
2. **Add** a line under the `ALUMNI` heading, in the position you want on the page:
   ```python
       {"name": "Priya Nair", "role": "PhD 2026", "now": "Postdoc, University of Bonn, Germany."},
   ```
   If their next position isn't known yet, write `"now": ""`. The page shows `—`.
3. Their photo file can stay in `assets/Members/`. Alumni are listed without photos.
4. Run `python3 _source/build_members.py`.

#### Change someone's interests, links or name

Search for their name (`Ctrl+F`), edit the text in the quotes, and run the script.

---

### 3.2 News — `_source/build_news.py`

Builds `news.html`, then refreshes `index.html` (the Home page shows the
**4 newest** items automatically).

#### Add a news item

Find `NEWS = [` and paste a new block **at the top**, because the list is newest first:

```python
NEWS = [
    {
        "tag": "Award",
        "title": "Humboldt Research Fellowship for Rahul Verma",
        "body": "Rahul Verma has been awarded a Humboldt Research Fellowship "
                "for postdocs. Congratulations, Rahul!",
        "link": None,
    },
    {
        "tag": "Symposium",
        …the older items stay below…
```

- `"tag"`: the small label above the title: *Symposium*, *New faculty*, *Award*, *Placement*…
- `"body"`: a long text can be split across lines like above. Each piece in its own
  quotes, with a **space before the closing quote** so words don't run together.
- `"link"`: `None`, or a button under the item written as `("address", "button text")`, e.g.
  ```python
          "link": ("conferences.html#symposium-2027", "Schedule and details"),
  ```

#### PMRF fellows

`PMRF = ["Amit Sharma", "Neha Gupta", "Rahul Verma"]`. Add or remove
a name in quotes, separated by commas.

#### Postdoc positions text

The *Postdoctoral positions* paragraph is written inside `build()` lower down.
Search for `Postdoctoral positions` and edit the sentences or the link there.

---

### 3.3 Conferences and symposia — `_source/build_conferences.py`

Builds `conferences.html`, then refreshes `index.html`.

#### Add next year's in-house symposium

1. Put the poster in `assets/ConferenceWorkshop/`, named `symposium-2027.webp`.
2. In `SYMPOSIA = [`, copy the **first** `{ … },` block and paste it **above** it:

```python
SYMPOSIA = [
    {
        "year": "2027",
        "poster": "symposium-2027.webp",
        "title": "In-House Symposium 2027",
        "dates": "29 &amp; 30 January 2027",
        "body": "The HEP group at IIT Kanpur is organising an in-house symposium. Join us!",
        "sheet": "1AbCdEfGhIjKlMnOpQrStUvWxYz0123456789abcdef",
        "gid": None,
        "highlight": True,
        "open": False,
    },
    {
        "year": "2026",
        …
        "highlight": False,      ← switch the previous year's highlight off
```

| Field | Meaning |
|---|---|
| `year` | Shown in the badge. Also makes the page address `conferences.html#symposium-2027`, which news items can link to. |
| `poster` | Just the **file name** of the poster in `assets/ConferenceWorkshop/`. Clicking the poster opens it full size. |
| `dates` | Free text; write `&` as `&amp;`. |
| `sheet` | The programme's Google Sheet ID: the long code in its address, `docs.google.com/spreadsheets/d/`**`THIS-PART`**`/edit`. |
| `gid` | If the programme is on a **later tab** of the sheet, the number after `#gid=` in the address, in quotes (`"1929783250"`). Otherwise `None`. |
| `highlight` | `True` gives the badge the maroon colour. Use it for the newest edition only. |
| `open` | `True` shows the programme unfolded when the page opens; `False` keeps it behind the **Show the programme** button. |

> The schedule sheet must be shared on Google as **"Anyone with the link — Viewer"**,
> or it shows up blank on the site.

#### Add a conference or workshop

In `CONFERENCES = [`, add a line (newest first):

```python
    ("Strings Attached 3.0", "2027",
     "The third edition of the group's string theory meeting.",
     "https://sites.google.com/view/…"),
```

The four parts are: name, year, one-line description, meeting website.

---

### 3.4 Research — `_source/build_research.py`

Builds `research.html`, then refreshes `index.html` (the Home page shows the
three research areas). Run it with:

```bash
python3 _source/build_research.py
```

It holds two lists.

**`THRUSTS`** has one `{ … }` block per research area (Particle Theory, Particle
Experiments, String Theory). Leave `id`, `art`, `num`, `accent` and `icon` as they
are, and edit:

| Field | Where it shows |
|---|---|
| `"blurb"` | one **short** line on the **Home page** card |
| `"about"` | the full paragraph at the top of the area on the **Research page** |
| `"topics": [ … ]` | the topic list on the Research page (one topic per line, in quotes, comma after each). The Home page card shows the **first four** on one line, so put the most important first. |
| `"members": [ … ]` | the first names under **Faculty in this area** |
| `"link"` | `None`, or a button such as `("https://…", "String theory group site")` |

**`FIGURES`** holds the slideshow of paper figures inside each area, in three
lists: `FIGURES["theory"]`, `FIGURES["experiment"]` and `FIGURES["string"]`.
Each slide moves on by itself every 6 seconds; visitors can also use the dots,
the arrow buttons, the arrow keys or a swipe, and pause it. One slide is one block:

```python
    "theory": [
        {
            "faculty": "Priya Nair",
            "caption": "One or two plain sentences saying what the figure shows.",
            "paper": "Title of the paper",
            "arxiv": "2604.03832",
            "files": ["pkd.png", "pku.png"],
            "image": "Research/nair-2604-03832.webp",
        },
        …
```

| Field | What to put |
|---|---|
| `"faculty"` | whose paper it is. Not shown on the page; it helps you keep track. |
| `"caption"` | one or two plain sentences, shown under the figure |
| `"paper"`, `"arxiv"` | the paper's title and arXiv number, shown as a link to `arxiv.org/abs/<number>` |
| `"files"` | the figure's **file name as INSPIRE-HEP lists it**. Two or three names are placed side by side (left/right panels). |
| `"image"` | where the finished picture is saved inside `assets/`. Name it `surname-arxivnumber.webp`; add a word at the end if you use two figures from the same paper. |

**Finding a figure's file name:** open this address in your browser, with the
paper's arXiv number at the end:

```
https://inspirehep.net/api/literature?fields=figures&q=arxiv:2604.03832
```

Each figure has a `"filename"` (e.g. `pku.png`) next to its `"caption"`, in the
order the figures appear in the paper. Firefox shows it as a tidy list; in
other browsers use the **Raw Data** or **Pretty Print** view.

**Making the pictures.** One command downloads every figure that isn't in
`assets/Research/` yet, trims and shrinks it to WebP, then rebuilds the page:

```bash
python3 _source/build_research.py --figures
```

It prints one line per figure: `saved`, `have` (already there) or `FAILED` with
the reason. It takes the figure from INSPIRE-HEP; if INSPIRE-HEP doesn't have it,
it unpacks the paper's source files from arXiv and converts the matching `.pdf`,
`.eps` or `.png` itself (this needs `poppler-utils` and `ghostscript`, see
[1.2](#12-install-the-tools)). To replace a picture, delete its `.webp` and run
the command again, or add `--force` to re-download all of them. At the end it
lists any pictures in `assets/Research/` that no slide uses any more, so you
can delete them.

- **Look at every new picture before you push.** Open `research.html` and step
  through each slideshow; if a figure doesn't read well, use another figure from
  the same paper.
- A slide whose picture doesn't exist yet is **left out of the page**, and an area
  with no pictures at all shows its line drawing instead.
- **To remove a slide**, delete its block, run the script, and delete its `.webp`.
- Commit the new files in `assets/Research/` together with `research.html`.
- To change how long each slide stays up, edit `CAROUSEL_DELAY = 6000`
  (milliseconds) at the top of `assets/carousel.js`.

---

### 3.5 Home, Seminars, Contact, menu and footer — `_source/build_all.py`

These change rarely, so they live together in `build_all.py`, along with the
parts every page shares. The file is divided into numbered sections; use
`Ctrl+F` to jump to one. **After any change in this file, run
`python3 _source/build_all.py`**, which rebuilds all seven pages.

| To change… | Look in section | What to edit |
|---|---|---|
| Group e-mail, phone, site name, the menu | **1. SITE-WIDE SETTINGS** | `EMAIL`, `PHONE`, `SITE_NAME`, `NAV` (they appear on every page) |
| The line drawings beside page titles | **2b. IMAGES** | `ART` (see below) |
| Home page heading and welcome text | **4. HOME PAGE** | the `<h1>` and the text inside `<p class="lede dropcap">` in `build_index()`. Keep `<em>…</em>` round the words you want in maroon italic. |
| Seminars page text or links | **6. SEMINARS PAGE** | the text inside `build_seminars()` |
| Editor team | **7. CONTACT PAGE** | `EDITORS`: one editor is `("Name", "email@iitk.ac.in"),` |

The Home page's member counts, latest news and research areas are filled in
automatically from the other scripts, so you don't edit those here.

> **Seminars** themselves come from the group's Google Calendar
> (`hepiitk@gmail.com`). To add or change a seminar, **edit the Google Calendar,
> not the website**. The page picks it up automatically.

#### The animation on the Home page

The two neutron stars that spiral together, collide and leave a black hole,
with the gravitational-wave signal drawn underneath, are drawn by
**`assets/merger.js`**. `HERO_ART` in `build_all.py` only places it on the page,
and its size is set by the `.merger` rules in `assets/style.css`.

To change how it moves or looks, edit the `MERGER` settings at the top of
`assets/merger.js`; no rebuild is needed, just refresh the page:

| Setting | What it does |
|---|---|
| `cycle` | seconds for one full loop |
| `inspiral` | seconds the stars orbit before they collide |
| `turns` | how many orbits they make |
| `starA`, `starB` | the two stars' colours, each as three RGB colours: highlight, body, rim |

The animation pauses when it's scrolled off screen, and visitors who have
"reduce motion" switched on see a still picture.

#### The line drawings beside page titles

Each inner page can show a line drawing beside its title (the blackboard on
Seminars, the auditorium on Conferences, and so on). They are `.svg` files in
`assets/img/`, listed in `ART` in `build_all.py`:

```python
    "seminar": ("img/seminar.svg", "Blackboard with an equation and a lectern"),
```

The first part is the file, the second a short description for screen readers.
A page shows its drawing through the `art="…"` line in its call to
`page_head_band(…)`, for example `art="seminar"` in `build_seminars()`.

- **To change a drawing**, replace the `.svg` file with one of the same name and
  refresh the page. Nothing needs rebuilding.
- **To add one to another page**, put the `.svg` in `assets/img/`, add a line
  to `ART`, add `art="your-key"` to that page's `page_head_band(…)` call, and run
  `python3 _source/build_all.py`.
- Keep new drawings in the same style: a `420 × 276` canvas, an off-white
  background (`#fbfaf6`), thin ink lines (`#101216`) and the maroon `#7d1f2c`,
  navy `#1d3557` and gold `#8a6a24` accents.

---

### 3.6 Colours, fonts, spacing and animations

All the design lives in **`assets/style.css`**. No script writes this file, so
you edit it directly and nothing needs rebuilding. Every colour is defined once
at the top, in the `:root { … }` block, so changing a value there changes it
everywhere. For example, `--maroon: #7d1f2c;` is the main accent colour. Change
the design only if you're comfortable with CSS, and always preview several pages
before pushing. Your browser may keep an old copy of `style.css`, so
hard-refresh (`Ctrl+Shift+R`) after a change.

Three small scripts in `assets/` add the moving parts. Like `style.css`, no
build script writes them:

| File | What it does |
|---|---|
| `app.js` | mobile menu, member search, the slide-in effect, the counting numbers |
| `carousel.js` | the figure slideshows on the Research page |
| `merger.js` | the neutron-star animation on the Home page |

The size of the Home page heading and introduction is set in the hero section
of `style.css` (search for `/* ---------- 5. Hero`): `.hero h1 { font-size: … }`
and `.hero .lede { font-size: … }`.

---

### 3.7 Photos and images

**Always shrink a photo and convert it to WebP before adding it.** A phone
photo is often 3–5 MB; the same picture as a 600 px WebP is around 30–80 KB.
Small images keep the pages fast and the repository small. GitHub Pages has
usage limits: the published site may be at most **1 GB**, and there is a soft
**bandwidth limit of 100 GB per month**
([GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)).
Every visitor downloads the images, so large files use that up quickly.

#### Shrink and convert with ImageMagick (`mogrify`)

ImageMagick is installed in [1.2](#12-install-the-tools). If `mogrify` is
missing, install it with:

```bash
sudo apt install imagemagick
```

Then, in the `hepiitk.github.io` folder, with the original photo saved there as
`priya-nair.jpg` (already named after the person, see step 2 below):

```bash
mogrify -path assets/Members -resize 600x600\> -quality 85 -format webp priya-nair.jpg
```

| Part | What it does |
|---|---|
| `-path assets/Members` | Writes the result into `assets/Members/` (the folder must already exist). The original `priya-nair.jpg` is **not** changed. |
| `-resize 600x600\>` | Shrinks the picture so neither side is bigger than 600 px, keeping its shape. The `\>` means "only shrink, never enlarge". A 4:5 portrait becomes 480 × 600 px. |
| `-quality 85` | Good quality at a small size. Lower it (e.g. `75`) for an even smaller file. |
| `-format webp` | Saves it as `priya-nair.webp`. |
| `priya-nair.jpg` | The photo to convert. Works with `.jpg`, `.jpeg` and `.png` too. |

The result is `assets/Members/priya-nair.webp`. Check its size with
`ls -lh assets/Members/priya-nair.webp`, then delete the original `.jpg` from
the `hepiitk.github.io` folder so you don't commit it by accident.

- **Several photos at once:** `mogrify -path assets/Members -resize 600x600\> -quality 85 -format webp *.jpg`
- **A symposium poster:** keep it larger so the text stays readable:
  `mogrify -path assets/ConferenceWorkshop -resize 1600x1600\> -quality 85 -format webp symposium-2027.jpg`

All options are explained on the ImageMagick page: <https://imagemagick.org/mogrify/>

#### Then add it to the site

1. **Member portraits:** crop to a **4:5 portrait** with the face in the upper part
   before converting (any image viewer or editor such as GIMP can crop).
2. **Name it after the person or event, in lowercase, with hyphens and no spaces**:
   `priya-nair.webp`, `symposium-2027.webp`. All existing files follow this pattern,
   so you can always tell whose photo a file is.
3. Make sure it is in the right folder (`assets/Members/` for people,
   `assets/ConferenceWorkshop/` for posters).
4. Write **exactly** that file name in the `"photo"` / `"poster"` field and re-run the script.

> ⚠️ **Capital letters matter.** Linux and GitHub Pages treat `Priya-Nair.webp`
> and `priya-nair.webp` as **different files**. If a photo shows only
> **initials**, check the capital letters and the extension (`.webp` vs `.jpg`)
> in both the file name and the script.

Remember to **commit the image file too**. It appears under **Changes** with a **U** (untracked).

---

### 3.8 Editing an `.html` file directly (only for an emergency fix)

You *can* fix a typo straight in an `.html` file (or with the pencil ✏️ on
GitHub). It works, but **it will be overwritten** the next time anyone runs that
page's script. If you do it, make the **same change in the script** in the same
commit, so nothing is lost later.

On GitHub, switch to the **`web`** branch first (the branch menu above the file
list), then click the pencil. If you start from `main`, GitHub won't let you commit
there. Instead it offers to **create a new branch for this commit and start a
pull request**, which also works. Either way, finish with Steps 7–8.

---

## Part 4 — When something goes wrong

### "A Python error appeared when I ran a script"

Nothing was written, so the site is unchanged. Python tells you the **file** and
**line number**: `File "_source/build_members.py", line 112`. Go to that line
(`Ctrl+G` in VS Code) and look at it **and the line above it**.

| The error says | Usually means |
|---|---|
| `SyntaxError: invalid syntax. Perhaps you forgot a comma?` | A missing **comma** at the end of a `"field": value` line, or after the `}` that closes a block |
| `SyntaxError: ':' expected after dictionary key` | A missing **colon** between a field and its value: `"photo": "priya-nair.webp",` |
| `SyntaxError: unterminated string literal` | A missing **quote mark** `"` |
| `SyntaxError: closing parenthesis ']' does not match …` or `'{' was never closed` | A missing `}`, `)` or `]` |
| `NameError: name 'none' is not defined` | `None`, `True`, `False` must start with a capital letter |
| `KeyError: 'name'` (or another field) | A block is missing that field, or its name is misspelt (`"Name"` instead of `"name"`). Copy a complete block. |
| `ValueError: not enough values to unpack` | A `( … )` line in `CONFERENCES` or `EDITORS` has too few parts |
| `FAILED … is not among the paper's figures` (from `--figures`) | The name in `"files"` doesn't match INSPIRE-HEP's file name exactly. Check it at the INSPIRE address in [3.4](#34-research--_sourcebuild_researchpy). |

For the last two, the line number points into the page-building code lower
down. The real mistake is in the entry you just added.

The red squiggly underline from the **Python** extension usually points at the problem before you even run it.

### "`python3` is not recognised / command not found"

Python isn't installed. Install it with your package manager (see
[1.2](#12-install-the-tools)), for example `sudo apt install python3`, then
**close and reopen VS Code**.

### "My change disappeared"

Someone ran a script after you edited the `.html` file directly, so the page was
rewritten. Make the change in the script instead. See [3.8](#38-editing-an-html-file-directly-only-for-an-emergency-fix).
The old text is still in GitHub's **History** for that file.

### "I made a mess of a file and haven't committed yet"

**Source Control** → right-click the file under **Changes** → **Discard Changes**.
The file goes back to the last committed version. Do it for the `.py` and the
`.html` files.

### "I committed but haven't pushed yet, and want to undo it"

**Source Control** → **⋯** → **Commit** → **Undo Last Commit**. Your edits stay in
the files, so you can fix them and commit again.

### "I already pushed a mistake"

- **Pushed to `web` but not merged yet:** fix the script, run it, then commit and
  push again. The open pull request picks up the fix by itself.
- **Already merged into `main` (it's on the live site):** fix it on `web` as usual
  and open a new pull request (Steps 7–8). To undo a whole merge quickly, open the
  merged pull request on GitHub and click **Revert**. GitHub makes a new pull
  request that undoes it, and you merge that.

Every earlier version is kept on GitHub (open the file on GitHub → **History**),
so nothing is ever truly lost.

### "Push was rejected" / "Updates were rejected because the remote contains work…"

Someone else pushed to `web` while you were working. Click **⋯ → Pull**, then
**Sync Changes** again. Usually that's all it takes.

### "Push declined … Changes must be made through a pull request" (GH013)

You committed on **`main`**, which only accepts pull requests. Your work is not
lost:

1. Click the branch name in the bottom-left corner → **Create new branch…** and
   name it, e.g. `my-fix`. The new branch keeps your commits.
2. Click **Publish Branch**.
3. Open a pull request from `my-fix` into `main` and merge it (Steps 7–8).
4. Switch back to **`web`** and **Pull** before your next change.

### "Merge conflict"

This happens when you and another editor changed the **same lines**. VS Code
marks the file with a **!** and shows both versions:

- **Current Change** = yours, **Incoming Change** = theirs.
- In the **script**, click **Accept Current**, **Accept Incoming** or **Accept Both**
  above each conflict, or edit the text by hand so the list is right.
- For a conflict in a **generated `.html` file**, don't edit it by hand: fix the
  script, then run it again. That rewrites the page cleanly.
- Save, **Stage** (**+**), **Commit**, then **Sync Changes**.

**On GitHub** a conflict shows up on the pull request as *"This branch has
conflicts that must be resolved"*. Resolve it in VS Code: on the `web` branch,
**⋯ → Pull**, then **⋯ → Branch → Merge…** → choose **`origin/main`**. Fix the
conflicts as above, then commit and **Sync Changes**. The pull request updates and
can be merged.

To avoid conflicts: **pull before you start**, keep each change small, and
**push and merge as soon as you're done**.

### "My change isn't showing on the live site"

1. **Did you merge the pull request into `main`?** Pushing to `web` alone does not
   publish anything. Check the **Pull requests** tab (Steps 7–8).
2. Did you run the script, and commit the **`.html`** file, not just the `.py`?
3. In the repository's **Actions** tab, check that the newest **pages build and
   deployment** run has a **green tick ✓**. A **red ✗** means publishing failed:
   click it to see why, or ask another editor.
4. Hard-refresh the page: `Ctrl+Shift+R`.
5. Wait two minutes and try again.

### "A photo shows only initials"

Either the person's `"photo"` is `None`, the file name there doesn't match the
file, or the file isn't in `assets/Members/`. Check the spelling, the **capital
letters** and the **extension**. See [3.7](#37-photos-and-images).

---

## Part 5 — Quick reference

### Which script do I run?

| I changed… | Run |
|---|---|
| people, photos, alumni | `python3 _source/build_members.py` |
| news, PMRF, positions | `python3 _source/build_news.py` |
| symposia, conferences | `python3 _source/build_conferences.py` |
| research areas or their figure slideshows | `python3 _source/build_research.py` (add `--figures` to download new figures) |
| anything in `build_all.py` (menu, footer, e-mail, phone, Home text, Seminars, Contact, drawings list), or not sure | `python3 _source/build_all.py` |
| `assets/style.css`, a `.js` file in `assets/`, or a drawing in `assets/img/` | nothing, just save and refresh |

The first four also refresh the Home page (`index.html`) every time.

### The routine in VS Code

| Step | Where |
|---|---|
| Check / switch branch | bottom-left corner of VS Code: it should say **`web`** |
| Pull | Source Control → **⋯** → **Pull** |
| Build | open the script → **▶ Run Python File**, or type the command in the terminal |
| Preview | right-click an `.html` file → **Open with Live Server** |
| See your changes | Source Control → click a file under **Changes** |
| Stage | **+** next to **Changes** |
| Commit | type a message → **✓ Commit** |
| Push to `web` | **Sync Changes** |
| Pull request | GitHub → **Compare & pull request** (base `main` ← compare `web`), or the one already open |
| Publish | on the pull request → **Merge pull request** → **Confirm merge** (don't delete `web`) |
| Check it's live | GitHub → **Actions** → green tick ✓, then `Ctrl+Shift+R` on the site |

### The same thing in a terminal

Run these in the `hepiitk.github.io` folder (VS Code: **Terminal → New Terminal**):

```bash
git switch web                             # make sure you're on the web branch
git pull                                   # 1. get the latest
mogrify -path assets/Members -resize 600x600\> -quality 85 -format webp priya-nair.jpg  # shrink a new photo
# … edit the script and save …
python3 _source/build_members.py           # 2. rebuild the page
git status                                 # see which files changed
git diff                                   # see exactly what changed (press q to quit)
git add .                                  # 3. stage everything you changed
git commit -m "Add Priya Nair to students" # 4. commit with a message
git push                                   # 5. send it to web on GitHub
git log --oneline -5                       # the last five commits
```

Then open the pull request and merge it on GitHub (Steps 7–8).

Your own branch, made from `main`:

```bash
git fetch
git switch -c new-research-figures origin/main   # make the branch and switch to it
# … edit, build, commit as above …
git push -u origin new-research-figures          # the first push of a new branch
```

Download the site on a new computer:

```bash
git clone https://github.com/hepiitk/hepiitk.github.io.git
cd hepiitk.github.io
git switch web
```

### Before you push — checklist

- [ ] I'm on the **`web`** branch (or my own branch), **not `main`**.
- [ ] I pulled before I started.
- [ ] I edited the **script**, not the `.html` file, and I **ran** it with no errors.
- [ ] I previewed the page in a browser and it looks right.
- [ ] New photos are shrunk to WebP (tens of KB, not MB), show on the page (not initials), and their file names are lowercase.
- [ ] I'm not committing the large original photo (`.jpg` / `.png`).
- [ ] New research figures look right in their slideshow, and unused ones are deleted from `assets/Research/`.
- [ ] I'm committing the `.py` file, the `.html` file(s) it wrote, and any new images.
- [ ] My commit message says what I changed.
- [ ] After pushing, I opened (or reused) the pull request into `main`, checked
      **Files changed**, merged it, and the **pages build and deployment** run is green.

---

## Maintainers

The site is maintained by the group's editor team (`@hepiitk/editor` on GitHub).
See [contact.html](https://hepiitk.github.io/contact.html). Questions,
corrections and news go to **hepiitk@gmail.com**.

**For admins:**

- **Add an editor:** <https://github.com/orgs/hepiitk/teams/editor> → **Add a member**.
  Remember to add them to `EDITORS` in `build_all.py` too, so they appear on the Contact page.
- **Remove an editor:** remove them from the team. They keep read access as members of
  the organisation, but can no longer push.
- **Protection of `main`:** repository **Settings → Rules → Rulesets → main**.
- **Publishing:** repository **Settings → Pages**. The site is built from the `main` branch.
