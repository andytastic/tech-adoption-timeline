# Breakthroughs and Adoption

A thousand years of technological breakthroughs, and how fast the modern ones spread across the US. Generative AI is plotted on the same curve.

**Live page:** `https://<your-username>.github.io/tech-adoption-timeline/` (once GitHub Pages is on)

---

## What's in here

```
tech-adoption-timeline/
├── docs/                         ← everything GitHub Pages publishes
│   ├── index.html                ← the page (timeline + adoption chart)
│   └── data/
│       ├── breakthroughs.json    ← one entry per breakthrough
│       └── adoption.json         ← adoption curves (share of the US, by year)
├── scripts/
│   └── validate_data.py          ← checks the data files for mistakes
└── .github/
    ├── workflows/check-data.yml  ← runs the check on every pull request
    ├── ISSUE_TEMPLATE/…          ← "Suggest a breakthrough" form
    └── pull_request_template.md  ← checklist shown on every PR
```

Most of your changes will be to `docs/data/breakthroughs.json`. The page reads it automatically.

---

## Part 1: Get it online (one time, ~15 minutes)

1. **Create the repo.** On github.com, click **New repository**. Name it `tech-adoption-timeline` and make it **Public**. Leave "Add a README" **unchecked**, because this folder already has one. Click **Create repository**.
2. **Install GitHub Desktop** (desktop.github.com) and sign in.
3. **Clone it.** In Desktop: **File → Clone repository** → pick `tech-adoption-timeline` → choose where to keep it on your Mac.
4. **Copy these files in.** Unzip this starter and copy everything into that folder.
   - The `.github` folder is hidden on a Mac. Press **Cmd + Shift + .** in Finder to show hidden files so it gets copied too.
5. **First commit.** Back in Desktop you'll see the files listed as changes. Type a summary such as `Initial version` and click **Commit to main**, then **Push origin**.
   - Committing straight to `main` is fine *once*, to get started. After this, every change goes through a branch and a pull request.
6. **Turn on Pages.** On github.com: **Settings → Pages → Build and deployment → Deploy from a branch → `main` / `/docs` → Save**. After a minute or two your page is live at the address shown there.
7. **Check the Actions tab.** You should see a "Check data" run with a green check ✓. That's the automated test.

---

## Part 2: The everyday loop (do this for every change)

```
branch → edit → commit → push → pull request → checks pass → merge → page updates
```

### Exercise 1: Your first pull request

Add a breakthrough. Some that are missing: photography (1839), the telegraph (1844), vaccines (1796), the Wright Flyer (1903), the integrated circuit (1958), GPS (1995).

1. In Desktop: **Branch → New branch** → name it `add-photography`.
2. Open `docs/data/breakthroughs.json` in any text editor. Copy an existing entry and paste it **in year order**, then edit it:
   ```json
   {
     "id": "photography",
     "year": 1839,
     "title": "Photography",
     "why": "One or two sentences on why it mattered.",
     "source": "https://…"
   },
   ```
   Every entry except the last needs a comma after its closing `}`.
3. In Desktop, write a summary (`Add photography`), click **Commit to add-photography**, then **Publish branch**.
4. Click **Create Pull Request**. GitHub opens in your browser with the PR checklist.
5. Wait for the **Check data** result at the bottom of the PR. Green means you can merge.
6. Click **Merge pull request**. Then in Desktop switch back to `main` and click **Fetch / Pull origin**.
7. Reload your Pages URL after a minute or two. The new dot is on the timeline.

### Exercise 2: Break it on purpose

Make a new branch and delete the `"source"` line from one entry. Commit, push and open a PR. The check turns **red ✗**. Click **Details** to see the plain-English error. Fix it on the same branch, push again, and watch it turn green. Reviewers rely on exactly this loop.

### Exercise 3: Issues and closing them from a PR

1. **Issues → New issue → Suggest a breakthrough.** Fill in the form. Note the issue number, e.g. `#3`.
2. Do Exercise 1 for that breakthrough. In the PR description, write `Closes #3`.
3. Merge the PR. The issue closes itself, with a link back to the change.

### Exercise 4: Protect `main`

**Settings → Branches → Add branch ruleset** (or "Add rule"). Target `main`, then turn on **Require a pull request before merging** and **Require status checks to pass** (pick "validate"). Now nobody can push straight to `main` or merge red work, including you. This is how most team repos are set up.

### Exercise 5: Tag a release

When you're happy with it: **Releases → Draft a new release → Choose a tag → type `v1.0` → Create new tag**. Write a few lines on what's in it and click **Publish release**. A release is a named snapshot you can point people to.

---

## Running the check yourself

```bash
python3 scripts/validate_data.py
```

To preview the page on your Mac before pushing:

```bash
cd docs
python3 -m http.server
```

Then open http://localhost:8000. Opening `index.html` by double-clicking won't load the data, because browsers block that for local files.

---

## Data and method

- **Breakthroughs:** each entry links to its own source.
- **Household adoption curves:** [Our World in Data, Technology Adoption](https://ourworldindata.org/technology-adoption), which collates Comin & Hobijn (2004), Horace Dediu and others. Sampled every few years and trimmed to the adoption phase.
- **Generative AI:** Bick, Blandin & Deming, *The Rapid Adoption of Generative AI*, Real-Time Population Survey, [via FRED](https://fred.stlouisfed.org/series/RPSGENAIUSAGESHAREALL). Share of US adults aged 18–64 who use generative AI for any purpose, quarterly. Last updated by the source in August 2026; check FRED for newer quarters.
- **Caveat:** the older series count *households* that own a technology. The AI series counts *adults* who use it at all. Treat the comparison as a sense of the trend, not a precise measurement.

## Ideas for later

- A scheduled GitHub Action that checks FRED for a new quarter of AI data and opens a PR when there is one.
- A second page charting active satellites in orbit over time.
