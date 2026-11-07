---
yaiml-revision: "0.1.46b565251e398e76"
role: architecture
title: EntroPy architecture
purpose: Durable component boundaries, data flow, and correctness invariants.
not-here: Task chronology, current priorities, or command reference.
durability: Durable; revise when boundaries change.
budget: 650 words
update-when: Estimators, delivery surfaces, state ownership, or data contracts change.
agent-guidance: Read changes.md for pending corrections; source and tests establish current behavior.
---
# System shape

The library accepts pandas observations. Utilities validate and discretize;
`BitPy` exposes empirical probabilities and per-state information;
`EntroPy` computes information measures. `probability.mvprob` supplies joint
and conditional frequencies. `information.audit.audit` assembles feature
associations, target uncertainty, and optional marginal drift into one report.

Two interfaces consume the audit. The CLI loads CSVs, serializes JSON, and
uses Matplotlib for SVG/PNG figures. The browser uses plain HTML/CSS/JavaScript
served by `information.web` with Python's standard HTTP server. Its JSON
endpoints preview CSV data, provide built-in examples, fetch weather, run a
fixed shuffle, and invoke the same audit. The browser renders the report; it does not reimplement the estimators.
There is no frontend build toolchain, external font/CDN requirement, database,
cloud upload, account, or persistent browser dataset store. `run.py` creates a
local venv, installs on a changed pyproject fingerprint, and launches this server.

## Data and invariants

- Rows are observations; multiple columns form a joint state. Inputs are not
  probability-weight arrays. `bins=None` preserves discrete symbols.
- All information uses bits. Cross-entropy weights the reference log-probability
  by the observed probability; KL is current/observed versus reference.
- Distribution comparisons match columns by position and use pooled numeric
  bin boundaries. A state absent from the reference produces infinity, encoded
  in audit JSON as null plus `unseen_in_reference`, without implicit smoothing.
- Paired measures require identical indexes and row order. Missing/nonfinite
  input values are rejected. Transfer entropy is target first, source second,
  with one historical state per variable at the requested row lag.
- Browser requests are bounded to 6 MB total, CSVs to 3 MB each, 50,000 rows,
  and 60 columns. The server binds 127.0.0.1, validates Host/Origin, exposes only
  explicit assets, and does not write uploads. User-provided strings are
  rendered as text. This local design is not a public-server security review.

## Examples and visual ownership

The CLI device example is a balanced synthetic construction with a perfect
thermal indicator, an imperfect alarm, and uninformative zone/batch columns.
The browser maps it to working/broken, temperature, warning light, and room,
omitting the constant batch. The packaged stock example derives six daily categorical movement series from
Sam's original bundled prices, split chronologically into reference/current
samples. The precise transformation belongs in `docs/methods.md`.

The weather adapter uses one fixed Open-Meteo archive endpoint, six city
coordinates, 90 hourly days split 45/45, fixed categorical thresholds, a bounded
15-second/1 MB fetch, and a 30-minute memory cache. It rejects incomplete data;
no sample is silently presented as fresh weather. Exact transformations and
provenance belong in docs/methods.md. Plain-language explanations use counted
states from the same feature-ranking bins. One seed-7 shuffle changes pairings
without changing marginal counts; it is a teaching comparison, not inference.

The UI uses an open editorial layout, paper/ink colors, restrained orange and
blue, serif headings, and directly labeled bars. The user rejects generic
navy/teal rounded-card dashboards. Graphics sources remain editable/reproducible.

## Retired and historical approaches

`driver.py` now runs a local demo instead of writing stock nodes to Neo4j.
Older notebooks, playground experiments, and source artwork are retained as
historical work, not supported launch paths. Do not silently restore their
hard-coded machine paths, database side effects, or obsolete pandas APIs.
