---
yaiml-revision: "0.3.5c8c73de392f1650"
role: maintainer
title: EntroPy maintainer guide
purpose: Current setup, verification, recovery, and YAIML provenance.
not-here: Product roadmap, architecture inventory, or raw logs.
durability: Current procedures; replace obsolete claims.
budget: 850 words
update-when: Setup, checks, delivery routes, or initialization evidence changes.
agent-guidance: Read changes.md for pending corrections; preserve environmental and evidence limits.
---
# Working with EntroPy

## Run and check

Python 3.10+ is declared. Create a virtual environment and install with
`python -m pip install -e ".[dev]"`. A local `.venv` was prepared with Python
3.12 for this checkout; do not copy machine-specific paths into shared guidance.

- Quick start: `python run.py`; see `docs/LOCAL_DEMO.md` for the shareable walkthrough.
- Browser/manual: `python -m information serve` then open `http://127.0.0.1:8765`.
  Keep that process running while using the UI; Ctrl+C stops it. `--port`
  selects another loopback port. The server is not an installed background task.
- Demo/report: `python -m information demo`; installed `entropy-audit` exposes
  the same demo/analyze/serve commands. Full examples belong in `readme.md`.
- Tests: `python -m unittest discover -v`.
- Documentation figures: `python scripts/render_graphics.py`.
- Packaging: `python -m build`. Assets and the stock sample are package data.

Inspect rendered UI after visual edits. Exercise a built-in example and a
real upload path; check changed states and narrow widths, not only startup.
Missing values and inconsistent columns should produce actionable errors.
When changing numerical behavior, preserve independently known answers and
SciPy cross-checks. Do not replace these with identities that merely mirror
the implementation.

## Verification evidence

On 2026-11-07, 51 tests passed on Python 3.12.10, pandas 3.1.1, NumPy 2.5.4.
The prior 38-test core/CLI suite also passed Python 3.10.11 / pandas 2.3.3.
The tests include known entropy/KL values, shared support/binning, conditional
probabilities, transfer direction and lags, CSV reports, HTTP API behavior,
asset serving, origin/path rejection, weather validation/cache/failure handling,
and shuffled-pair invariants. Full staged whitespace checks passed after normalizing generated SVG whitespace
and extra final blank lines. `.gitattributes` preserves exact YAIML source LF bytes.

Browser inspection verified live Seattle/Denver weather, plain company names,
the machine lesson, shuffle comparison, stock and sensor examples, target changes,
relationships/drift tabs, CSV selection and recalculation, missing-value error
handling, guide open/close, and JSON export. The downloaded report was parsed
and contained the expected 160 observations. A 390px viewport reflowed without
horizontal page overflow; desktop and mobile were visually inspected. No
browser console errors were reported. Remote CI and native mobile devices
were not run. Local sdist/wheel builds and packaged web/data assets were checked separately
from browser verification. A clean temporary checkout ran `run.py --setup-only`,
installed dependencies, and passed real audit/shuffle smoke checks.

## Recovery and boundaries

If the browser cannot connect, check the local server process and selected
port. Uploads are not persisted; weather is cached in memory for 30 minutes. Reload
fetches/reuses weather; stock and machine stories remain available offline.
User report downloads are explicit. The CLI is available for larger samples.
Mathematical contracts and sample provenance are in `docs/methods.md`.
Existing exploratory notebook environments are not required for this workflow.
No project-wide license or release/publishing policy was invented. Application
version remains 0.2.0 in `pyproject.toml`, independent of YAIML versions.

## YAIML provenance and activation

YAIML — Yet Another AI Markup Language, by Jeff Wirsing.
Source: https://github.com/wirsingj/YAIML. This acquisition resolved exact
`refs/tags/latest` once to commit
`b9b53e8b3725d25da64dfd4c51e209f9ffb7bfd7`. The tag directly identified that
commit; no same-named branch or substitute release was used. Bootstrap product
identity is 0.6.0, experimental; the operating guide's source stamp is
0.54.58ecbd56ad7274ae. These are provenance, not EntroPy history or release labels.

Twenty-five unmodified resources were acquired only from the reference tree
and root license. `source-manifest.json` records their original Git blob hashes;
all matched byte-for-byte on verification. No upstream project-memory tree,
root instructions, or completed source examples were acquired. Legal terms
are preserved in YAIML_NOTICE.md and apply to copied YAIML material only.

Root AGENTS.md routes ordinary work to YAIML_GUIDE.md and discovery.
Thirteen thin `.agents/skills/<name>/SKILL.md` entries forward unchanged
arguments to canonical local methods, including the compatibility alias.
Acquired method bodies were not modified; wrappers/core memory use prospective
local revision 0.1.46b565251e398e76. Earlier target memory iterations are unknown.
No other host instruction routes were found. Relevant existing usage and
methods documents are indexed rather than copied.

Local resources, reference paths, wrappers, discovery, and receipt can be
checked without the source repository. On the next user turn, the host supplied
metadata for all thirteen local skills, and the Git wrapper was read successfully.
Native skill discovery is observed; a separate fresh-session startup, interactive
menu behavior, and execution of every method remain unverified.
Memory maintenance is offline. No polling, delegation, or backlog execution is
authorized. Use YAIML_GUIDE.md and VERSIONING.md for maintenance; changes.md
locates the retained audit. This task has one active writer, so its initial
memory can be consolidated without overwriting another contributor's memory.
