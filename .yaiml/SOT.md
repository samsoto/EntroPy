---
yaiml-revision: "0.3.5c8c73de392f1650"
role: sot
title: EntroPy current state
purpose: Current human direction, capabilities, evidence, and open decisions.
not-here: Architecture details, command inventory, or session history.
durability: Current; replace superseded state.
budget: 600 words
update-when: Direction, verified capability, risks, or immediate priorities change.
agent-guidance: Read changes.md for pending corrections; distinguish observed behavior from intent.
---
# EntroPy

## Direction and authority

This is Sam's old repository (`samsoto/EntroPy`). The user wants corrected
calculations, refreshed graphics, a useful purpose, and an approachable UI that
honors **Sam's direction**. Original entropy lessons, Alice/Bob guessing examples,
stock experiments, and notebooks establish the original teaching/time-series
scope. A separate roadmap directly approved by Sam is not available.

The user found raw tickers, thermal-state/alarm/batch/zone labels, file uploads,
and unexplained statistics inaccessible. The app must bring its own data, tell
users what results mean, and provide an interesting demonstration for Sam.
Preserve the mathematical library rather than replacing it with generated
claims. The user explicitly wants Sam’s original pictures displayed in the
README alongside the new work. Preserve those image files and visible examples
in future documentation edits. Root AGENTS.md retains visual preferences and
publication boundaries.

The user subsequently authorized packaging on **feature/jw-1**, pushing, and
opening a pull request with clear local instructions. Upstream access is read-only;
a public `wirsingj/EntroPy` fork was created for this review. Merge and deployment
are not authorized. Git and PR state, rather than this snapshot, establish
whether the handoff has reached the remote.

## Current capabilities

- Corrected discrete Shannon, joint, conditional, cross, relative, mutual, and
  transfer information measures, with explicit binning and input validation.
- CLI reports and reproducible SVG/PNG graphics; original experiments retained.
- A local browser lab fetches recent weather for six cities, explains actual
  counts, and offers Sam's stock study and a fictional warning-light lesson.
- Plain company/condition names, empirical takeaway text, a daily rain strip,
  relationship/change views, source dates, optional CSVs, and JSON export.
- A fixed shuffle experiment preserves marginal counts while changing pairings,
  demonstrating why shared information depends on relationships.
- `python run.py` creates/reuses a local environment, installs dependencies as
  needed, and opens the browser. The detailed walkthrough is docs/LOCAL_DEMO.md.

## Evidence and limits

On 2026-11-07, all 51 tests passed on Python 3.12 / pandas 3.1.1. Earlier core/CLI
validation passed 38 tests on Python 3.10 / pandas 2.3.3. Browser inspection
covered live weather, examples, plain labels, shuffle, drift, and a 390px layout;
prior checks covered uploads, errors, export, and help. Source data was fetched
successfully. No browser console errors were observed. Packaging and clean
installation evidence belong in the Maintainer Guide.

These are empirical associations, not forecasts, causal estimates, or prediction
accuracy. Adjacent time samples are dependent. The one-shuffle illustration is
not a significance test. Weather uses model-based ERA5 estimates ending seven
days ago. Original stock provenance/adjustment policy remain unknown. Hosted
operation and commercial weather API access need separate decisions.

## Next decisions

Share the branch/PR and local demo with Sam; use his feedback to decide further
direction. No autonomous backlog, merge, release, or hosted deployment follows.
