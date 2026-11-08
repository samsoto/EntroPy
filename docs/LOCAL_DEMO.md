# Run EntroPy locally

This branch gives Sam's entropy and time-series experiments a browser interface.
It uses the Python library to calculate the results. No AI service, API key,
account, spreadsheet, database, or frontend build is required.

## Quick start

Install **Python 3.10 or newer** (3.12 recommended), then:

```sh
git clone --branch feature/jw-1 https://github.com/wirsingj/EntroPy.git
cd EntroPy
python run.py
```

On macOS/Linux, use `python3 run.py` if `python` is unavailable. On Windows,
`py -3.12 run.py` is another option if Python 3.12 is installed.

The launcher creates `.venv`, installs the dependencies on first use, and opens
**http://127.0.0.1:8765**. Keep the terminal open. **Ctrl+C** stops the app.
Subsequent launches reuse the environment. First setup needs internet; the two
built-in stories work offline afterward. The weather story needs internet.

If you already have Sam's checkout, use a separate clone above to keep your own
work intact, or fetch this branch into your normal review workflow.

## A three-minute demo

1. **Start with weather.** The app fetches recent weather estimates for Seattle.
   Read the takeaway: a specific condition, actual rainy-hour counts, and the
   overall rain rate. Pick another city to fetch and compare a different sample.
2. **Open “Does a warning light mean trouble?”** This is a deliberately simple
   fictional machine. Temperature perfectly identifies broken/working; the
   warning light gets one check in five wrong; the room gives no information.
3. **Click Temperature, then “Mix up temperature.”** It starts at 100% of outcome
   uncertainty removed. After the fixed shuffle it falls to about zero, although
   the numbers of hot and normal readings stay identical. Information lives in
   the pairing. This experiment illustrates the idea; it is not a significance test.
4. **Open “Do stocks move together?”** This uses six companies from Sam's original
   2013–2017 sample. Company names replace ticker jargon. Read a same-day example,
   then try **What changed?** to compare the earlier and later periods.

“Uncertainty removed” is mutual information divided by outcome entropy. It is
**not prediction accuracy**. Weather is same-hour and stocks are same-day;
neither story predicts the future. The UI explains these limits beside results.

## Manual setup / troubleshooting

```sh
python -m venv .venv
# Windows:
.venv\Scripts\python -m pip install -e .
.venv\Scripts\python -m information serve
# macOS/Linux:
.venv/bin/python -m pip install -e .
.venv/bin/python -m information serve
```

- Browser didn't open: visit **http://127.0.0.1:8765** yourself.
- Port in use: `python run.py --port 8766`.
- Weather unavailable: retry or choose either built-in story. No fake weather is
  silently substituted. The archive ends seven days ago and the fetched date is shown.
- Linux reports missing `venv`/`ensurepip`: install your distribution's Python
  venv package, then rerun setup.
- Need a terminal-only launch: `python run.py --no-browser`.

The service binds only to this machine. CSV uploads are optional, processed
locally, and not written to disk. Only the selected city's public coordinates,
dates, and requested weather fields go to Open-Meteo. Its free API is intended
for non-commercial use; check its terms before deploying a commercial product.

## Development checks

With the environment active, or using its Python path:

```sh
python -m pip install -e ".[dev]"
python -m unittest discover -v
python -m information demo
python -m build
```

The automated tests use deterministic weather fixtures, not a network dependency.
See [methods](methods.md) for mathematical contracts, provenance, and limitations.
