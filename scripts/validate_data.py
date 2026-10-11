"""Check the data files before they're merged.

Runs automatically on every pull request (see .github/workflows/check-data.yml).
To run it yourself:  python3 scripts/validate_data.py

It exits with an error and prints a plain-English list of problems if anything is wrong.
"""

import datetime
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "docs" / "data"
THIS_YEAR = datetime.date.today().year

problems = []


def problem(msg):
    problems.append(msg)


def load(name):
    path = DATA / name
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        problem(f"{name}: file is missing")
    except json.JSONDecodeError as e:
        problem(f"{name}: not valid JSON (line {e.lineno}, column {e.colno}): {e.msg}. "
                "Look for a missing comma or quote near that spot.")
    return None


def is_link(value):
    return isinstance(value, str) and value.startswith("https://")


# ---------- breakthroughs.json ----------
bt = load("breakthroughs.json")
adoption = load("adoption.json")

series_ids = set()
if isinstance(adoption, dict):
    series_ids = {s.get("id") for s in adoption.get("series", []) if isinstance(s, dict)}

if isinstance(bt, dict):
    items = bt.get("breakthroughs")
    if not isinstance(items, list) or not items:
        problem("breakthroughs.json: needs a non-empty \"breakthroughs\" list")
        items = []
    seen = set()
    last_year = None
    for i, b in enumerate(items, start=1):
        label = f"breakthroughs.json, entry {i}"
        if not isinstance(b, dict):
            problem(f"{label}: should be an object in curly braces")
            continue
        if b.get("title"):
            label += f" ({b['title']})"
        for field in ("id", "title", "why"):
            if not isinstance(b.get(field), str) or not b.get(field).strip():
                problem(f"{label}: missing \"{field}\"")
        bid = b.get("id")
        if bid in seen:
            problem(f"{label}: id \"{bid}\" is used twice; ids must be unique")
        seen.add(bid)
        year = b.get("year")
        if not isinstance(year, int) or isinstance(year, bool):
            problem(f"{label}: \"year\" must be a whole number like 1876 (no quotes)")
        elif not 1000 <= year <= THIS_YEAR:
            problem(f"{label}: year {year} is outside 1000-{THIS_YEAR}")
        else:
            if last_year is not None and year < last_year:
                problem(f"{label}: entries should be in year order; {year} comes after {last_year}")
            last_year = year
        if not is_link(b.get("source")):
            problem(f"{label}: needs a \"source\" link starting with https://")
        why = b.get("why") or ""
        if len(why) > 240:
            problem(f"{label}: \"why\" is {len(why)} characters; keep it under 240")
        link = b.get("adoption_series")
        if link is not None and series_ids and link not in series_ids:
            problem(f"{label}: adoption_series \"{link}\" doesn't match any series id in adoption.json")

# ---------- adoption.json ----------
if isinstance(adoption, dict):
    series = adoption.get("series")
    if not isinstance(series, list) or not series:
        problem("adoption.json: needs a non-empty \"series\" list")
        series = []
    seen = set()
    for i, s in enumerate(series, start=1):
        label = f"adoption.json, series {i}"
        if not isinstance(s, dict):
            problem(f"{label}: should be an object in curly braces")
            continue
        if s.get("label"):
            label += f" ({s['label']})"
        for field in ("id", "label", "measure"):
            if not isinstance(s.get(field), str) or not s.get(field).strip():
                problem(f"{label}: missing \"{field}\"")
        if s.get("id") in seen:
            problem(f"{label}: id \"{s.get('id')}\" is used twice")
        seen.add(s.get("id"))
        if not is_link(s.get("source")):
            problem(f"{label}: needs a \"source\" link starting with https://")
        launch = s.get("launch_year")
        if not isinstance(launch, (int, float)) or isinstance(launch, bool):
            problem(f"{label}: needs a numeric \"launch_year\"")
        points = s.get("points")
        if not isinstance(points, list) or len(points) < 2:
            problem(f"{label}: needs at least two points")
            continue
        prev = None
        for j, p in enumerate(points, start=1):
            plabel = f"{label}, point {j}"
            y, pct = (p.get("year"), p.get("pct")) if isinstance(p, dict) else (None, None)
            if not isinstance(y, (int, float)) or isinstance(y, bool):
                problem(f"{plabel}: \"year\" must be a number")
                continue
            if not isinstance(pct, (int, float)) or isinstance(pct, bool) or not 0 <= pct <= 100:
                problem(f"{plabel}: \"pct\" must be a number from 0 to 100")
            if prev is not None and y <= prev:
                problem(f"{plabel}: years must increase ({y} follows {prev})")
            if isinstance(launch, (int, float)) and y < launch:
                problem(f"{plabel}: year {y} is before the launch year {launch}")
            prev = y

if problems:
    print(f"Found {len(problems)} problem(s) in the data:\n")
    for p in problems:
        print(f"  ✗ {p}")
    sys.exit(1)

n_bt = len(bt["breakthroughs"]) if isinstance(bt, dict) else 0
n_s = len(adoption["series"]) if isinstance(adoption, dict) else 0
print(f"✓ Data looks good: {n_bt} breakthroughs, {n_s} adoption series.")
