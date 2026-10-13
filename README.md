# High Energy Physics @ IIT Kanpur — group website

The website of the High Energy Physics group, Department of Physics, IIT Kanpur.

**Live site → <https://hepiitk.github.io/website/>**

The site is plain HTML and CSS, written by **four small Python scripts** in the
`_source/` folder. The names, photos, news, dates and links sit in simple lists
inside them. To update a page you edit the list, run the script, and push the
result to GitHub. About a minute later the live site updates.

This guide is written for a new editor who has never used Git, Python or edited a
website before. Read Part 1 once to get set up. After that you only need
Part 2 (the everyday routine) and Part 3 (how to update each page).

---

## Contents

- [Where everything is](#where-everything-is)
- [Part 1 — One-time setup](#part-1--one-time-setup)
- [Part 2 — The everyday routine: pull → edit → build → check → commit → push](#part-2--the-everyday-routine)
- [Part 3 — How to update each page](#part-3--how-to-update-each-page)
- [Part 4 — When something goes wrong](#part-4--when-something-goes-wrong)
- [Part 5 — Quick reference](#part-5--quick-reference)

---

## Where everything is

```
index.html          Home page
members.html        Faculty, postdocs, graduate students, alumni
research.html       Research areas and the "Selected figures" gallery
seminars.html       Seminar calendar and journal clubs
conferences.html    In-house symposia, conferences and workshops
news.html           News, postdoc positions, PMRF fellows, funding
contact.html        Contact details and the editor team

_source/                  The four scripts that write the pages above
  build_members.py        → members.html      + refreshes index.html
  build_news.py           → news.html         + refreshes index.html
  build_conferences.py    → conferences.html  + refreshes index.html
  build_all.py            → ALL seven pages. Also holds everything the pages share
                            (menu, footer, e-mail, phone) and the pages that rarely
                            change: Home, Research, Seminars, Contact.

assets/style.css    The design: colours, fonts, spacing, layout (all pages share it)
assets/app.js       Small scripts: mobile menu, member search, animations
assets/Members/     Member photos, named after the person: priya-nair.webp
assets/ConferenceWorkshop/   Symposium posters: symposium-2026.webp
assets/img/         Line drawings used across the site
.gitignore          Tells Git to ignore Python's __pycache__ folder and stray .DS_Store files
```

> **The one rule to remember: change the script, not the HTML.**
> Every time a script runs it **rewrites its page** from the lists inside it.
> Anything typed straight into that `.html` file is lost. So for `members.html`
> you edit `_source/build_members.py`, for `news.html` you edit
> `_source/build_news.py`, and so on.
>
> - `_source/` should contain **only these four `.py` files**. Delete any older
>   ones you find there (`build.py`, `common.py`, `build_index.py`, …).
> - `styles.css` in the top folder (if it's still there) is left over from the old
>   site and isn't used. The real stylesheet is **`assets/style.css`**, which is
>   *not* written by any script, so you edit it directly.

---

## Part 1 — One-time setup

You only do this once per computer.

### 1.1 Get access to the repository

1. Make a free account at <https://github.com> if you don't have one.
2. Send your GitHub username to a current editor (see [contact.html](https://hepiitk.github.io/website/contact.html))
   and ask them to give you **write access** to `hepiitk/website`.
   *They do this on GitHub: the repository → **Settings** → **Collaborators** → **Add people**.*
3. Accept the invitation from the email GitHub sends you, or at
   <https://github.com/hepiitk/website/invitations>.

### 1.2 Install the tools

These instructions are for **Debian-based Linux** (Debian, Ubuntu, Linux Mint, Pop!_OS…).

You need four things: **Git** (tracks changes and talks to GitHub), **Python 3**
(runs the page scripts), **ImageMagick** (shrinks photos, see [3.6](#36-photos-and-images))
and **VS Code** (the editor you'll work in).

Open a terminal (`Ctrl+Alt+T`) and run:

```bash
sudo apt update
sudo apt install git python3 imagemagick
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

### 1.4 Download (clone) the website to your computer

1. Open VS Code.
2. Click the **Source Control** icon on the left: three dots joined by lines, or
   `Ctrl+Shift+G`.
3. Click **Clone Repository**. Alternatively, press `Ctrl+Shift+P`, type **Git: Clone** and press Enter.
4. Paste this address and press Enter:
   ```
   https://github.com/hepiitk/website.git
   ```
5. Choose a folder to keep it in, for example `Documents`. A folder called
   `website` is created there.
6. When VS Code asks **"Would you like to open the cloned repository?"**, click **Open**.
7. The first time you push, VS Code asks you to **sign in to GitHub**. Click
   **Allow**, finish the sign-in in your browser, then come back to VS Code.

You now have your own copy of the site. You won't need to clone again.

---

## Part 2 — The everyday routine

Every time you update the site, follow these six steps in this order.

```
 1. PULL  →  2. EDIT   →  3. BUILD   →  4. CHECK   →  5. COMMIT  →  6. PUSH
 (get the    (change the   (run the     (look at it   (save a       (send it to
  latest)     script)       script)      in a browser) snapshot)     GitHub)
```

### Step 1 — Pull: get the latest version first

Other editors may have changed the site since you last worked on it. Always pull
before you start, or you'll end up editing an old copy.

- In VS Code, open the **website** folder (**File → Open Recent**).
- Go to **Source Control** → click **⋯** (*Views and More Actions*) at the top of the panel → **Pull**.
- Or click the **circular arrows** next to the branch name `main` in the bottom-left status bar.

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

In the VS Code terminal (**Terminal → New Terminal**; it opens in the `website`
folder), run the script you edited:

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

### Step 6 — Push: publish it

After committing, the blue button changes to **Sync Changes ↑1**. Click it.
This pushes your commit to GitHub and also pulls anything new.

Then check that it's live:

1. Go to <https://github.com/hepiitk/website> and wait for the small **yellow dot**
   next to the latest commit to turn into a **green tick ✓**. That takes about 1–2 minutes.
2. Open <https://hepiitk.github.io/website/> and do a **hard refresh**
   (`Ctrl+Shift+R`) so your browser doesn't show an old copy.

That's the whole routine.

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
   (see [3.6](#36-photos-and-images)).
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

### 3.4 Home, Research, Seminars, Contact, menu and footer — `_source/build_all.py`

These change rarely, so they live together in `build_all.py`, along with the
parts every page shares. The file is divided into numbered sections; use
`Ctrl+F` to jump to one. **After any change in this file, run
`python3 _source/build_all.py`**, which rebuilds all seven pages.

| To change… | Look in section | What to edit |
|---|---|---|
| Group e-mail, phone, site name, the menu | **1. SITE-WIDE SETTINGS** | `EMAIL`, `PHONE`, `SITE_NAME`, `NAV` (they appear on every page) |
| Home page photo or welcome text | **4. HOME PAGE** | `HERO_PHOTO`, and the text inside `build_index()` |
| Research topics or faculty per area | **5. RESEARCH PAGE** | In `THRUSTS`, one `{ … }` per subgroup: `"topics": [ … ]` (one topic per line, in quotes, comma after each), `"members": [ … ]`, `"blurb"`. Leave `id`, `art`, `accent`, `icon` as they are. |
| *Selected figures* gallery | **5. RESEARCH PAGE** | `RESEARCH_FIGURES`: one figure is `("Research/file.webp", "Short title", "Caption or empty"),`, with the image in `assets/Research/` |
| Seminars page text or links | **6. SEMINARS PAGE** | the text inside `build_seminars()` |
| Editor team | **7. CONTACT PAGE** | `EDITORS`: one editor is `("Name", "email@iitk.ac.in"),` |

The Home page's member counts, latest news and research areas are filled in
automatically from the other files, so you don't edit those here.

> **Seminars** themselves come from the group's Google Calendar
> (`hepiitk@gmail.com`). To add or change a seminar, **edit the Google Calendar,
> not the website**. The page picks it up automatically.

---

### 3.5 Colours, fonts, spacing and animations

All the design lives in **`assets/style.css`**. No script writes this file, so
you edit it directly and nothing needs rebuilding. Every colour is defined once
at the top, in the `:root { … }` block, so changing a value there changes it
everywhere. For example, `--maroon: #7d1f2c;` is the main accent colour. Change
the design only if you're comfortable with CSS, and always preview several pages
before pushing.

---

### 3.6 Photos and images

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

Then, in the `website` folder, with the original photo saved there as
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
the `website` folder so you don't commit it by accident.

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

### 3.7 Editing an `.html` file directly (only for an emergency fix)

You *can* fix a typo straight in an `.html` file (or with the pencil ✏️ on
GitHub). It works, but **it will be overwritten** the next time anyone runs that
page's script. If you do it, make the **same change in the script** in the same
commit, so nothing is lost later.

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

For the last two, the line number points into the page-building code lower
down. The real mistake is in the entry you just added.

The red squiggly underline from the **Python** extension usually points at the problem before you even run it.

### "`python3` is not recognised / command not found"

Python isn't installed. Install it with your package manager (see
[1.2](#12-install-the-tools)), for example `sudo apt install python3`, then
**close and reopen VS Code**.

### "My change disappeared"

Someone ran a script after you edited the `.html` file directly, so the page was
rewritten. Make the change in the script instead. See [3.7](#37-editing-an-html-file-directly-only-for-an-emergency-fix).
The old text is still in GitHub's **History** for that file.

### "I made a mess of a file and haven't committed yet"

**Source Control** → right-click the file under **Changes** → **Discard Changes**.
The file goes back to the last committed version. Do it for the `.py` and the
`.html` files.

### "I committed but haven't pushed yet, and want to undo it"

**Source Control** → **⋯** → **Commit** → **Undo Last Commit**. Your edits stay in
the files, so you can fix them and commit again.

### "I already pushed a mistake"

Fix the script, run it, then commit and push again as usual. That's the simplest
way. Every earlier version is kept on GitHub (open the file on GitHub → **History**),
so nothing is ever truly lost.

### "Push was rejected" / "Updates were rejected because the remote contains work…"

Someone else pushed while you were working. Click **⋯ → Pull**, then **Sync
Changes** again. Usually that's all it takes.

### "Merge conflict"

This happens when you and another editor changed the **same lines**. VS Code
marks the file with a **!** and shows both versions:

- **Current Change** = yours, **Incoming Change** = theirs.
- In the **script**, click **Accept Current**, **Accept Incoming** or **Accept Both**
  above each conflict, or edit the text by hand so the list is right.
- For a conflict in a **generated `.html` file**, don't edit it by hand: fix the
  script, then run it again. That rewrites the page cleanly.
- Save, **Stage** (**+**), **Commit**, then **Sync Changes**.

To avoid conflicts: **pull before you start**, keep each change small, and
**push as soon as you're done**.

### "My change isn't showing on the live site"

1. Did you run the script, and commit the **`.html`** file, not just the `.py`?
2. On <https://github.com/hepiitk/website>, check that your commit is there with a **green tick ✓**.
   A **red ✗** means publishing failed: click it to see why, or ask another editor.
3. Hard-refresh the page: `Ctrl+Shift+R`.
4. Wait two minutes and try again.

### "A photo shows only initials"

Either the person's `"photo"` is `None`, the file name there doesn't match the
file, or the file isn't in `assets/Members/`. Check the spelling, the **capital
letters** and the **extension**. See [3.6](#36-photos-and-images).

---

## Part 5 — Quick reference

### Which script do I run?

| I changed… | Run |
|---|---|
| people, photos, alumni | `python3 _source/build_members.py` |
| news, PMRF, positions | `python3 _source/build_news.py` |
| symposia, conferences | `python3 _source/build_conferences.py` |
| anything in `build_all.py` (menu, footer, e-mail, phone, Home, Research, Seminars, Contact), or not sure | `python3 _source/build_all.py` |
| `assets/style.css` | nothing, just save |

The first three also refresh the Home page (`index.html`) every time.

### The routine in VS Code

| Step | Where |
|---|---|
| Pull | Source Control → **⋯** → **Pull** |
| Build | open the script → **▶ Run Python File**, or type the command in the terminal |
| Preview | right-click an `.html` file → **Open with Live Server** |
| See your changes | Source Control → click a file under **Changes** |
| Stage | **+** next to **Changes** |
| Commit | type a message → **✓ Commit** |
| Push | **Sync Changes** |

### The same thing in a terminal

Run these in the `website` folder (VS Code: **Terminal → New Terminal**):

```bash
git pull                                   # 1. get the latest
mogrify -path assets/Members -resize 600x600\> -quality 85 -format webp priya-nair.jpg  # shrink a new photo
# … edit the script and save …
python3 _source/build_members.py           # 2. rebuild the page
git status                                 # see which files changed
git diff                                   # see exactly what changed (press q to quit)
git add .                                  # 3. stage everything you changed
git commit -m "Add Priya Nair to students" # 4. commit with a message
git push                                   # 5. publish
git log --oneline -5                       # the last five commits
```

Download the site on a new computer:

```bash
git clone https://github.com/hepiitk/website.git
```

### Before you push — checklist

- [ ] I pulled before I started.
- [ ] I edited the **script**, not the `.html` file, and I **ran** it with no errors.
- [ ] I previewed the page in a browser and it looks right.
- [ ] New photos are shrunk to WebP (tens of KB, not MB), show on the page (not initials), and their file names are lowercase.
- [ ] I'm not committing the large original photo (`.jpg` / `.png`).
- [ ] I'm committing the `.py` file, the `.html` file(s) it wrote, and any new images.
- [ ] My commit message says what I changed.

---

## Maintainers

The site is maintained by the group's editor team. See
[contact.html](https://hepiitk.github.io/website/contact.html). Questions,
corrections and news go to **hepiitk@gmail.com**.
