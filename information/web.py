"""Local browser workbench backed by the same Python audit as the CLI."""

import csv
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import StringIO
import json
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import pandas as pd

from information.audit import audit, demo_data
from information.weather import fetch_weather, WeatherUnavailable

ASSETS = Path(__file__).with_name("web_assets")
MAX_BODY = 6 * 1024 * 1024
MAX_ROWS = 50000
MAX_COLUMNS = 60


def read_observations(text):
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Choose a CSV with a header row and at least one observation.")
    if len(text.encode("utf-8")) > MAX_BODY // 2:
        raise ValueError("Use a CSV smaller than 3 MB in this lightweight workbench.")
    text = text.lstrip("\ufeff")
    header = next(csv.reader(StringIO(text)), [])
    if not header or len(set(header)) != len(header) or any(not name.strip() for name in header):
        raise ValueError("CSV column names must be present and unique.")
    if len(header) > MAX_COLUMNS:
        raise ValueError(f"Choose up to {MAX_COLUMNS} columns for a browser audit.")
    data = pd.read_csv(StringIO(text), nrows=MAX_ROWS + 1)
    if len(data) > MAX_ROWS:
        raise ValueError(f"Choose up to {MAX_ROWS:,} observations for a browser audit.")
    if data.empty:
        raise ValueError("The CSV has headers but no observations.")
    return data


def preview(data):
    return {
        "rows": len(data),
        "columns": list(data.columns),
        "sample": json.loads(data.head(8).to_json(orient="records")),
        "missing": int(data.isna().sum().sum()),
    }


def distribution(data, column):
    if data is None:
        return []
    counts = data[column].value_counts(dropna=False)
    # Categories are rendered as text by the client, never HTML.
    return [{"state": str(state), "count": int(count), "fraction": float(count / len(data))}
            for state, count in counts.head(10).items()]


def analyze_payload(payload):
    data = read_observations(payload.get("csv"))
    reference = read_observations(payload["reference_csv"]) if payload.get("reference_csv") else None
    target = payload.get("target")
    if not isinstance(target, str):
        raise ValueError("Choose the outcome column you want to understand.")
    bins = payload.get("bins")
    if bins is not None and (isinstance(bins, bool) or not isinstance(bins, int) or not 2 <= bins <= 100):
        raise ValueError("Choose a whole number of bins between 2 and 100.")
    report = audit(data, target, reference, bins)
    from utilities.pyutils import discretize_pair, discretize
    if reference is not None:
        current_target, reference_target = discretize_pair(data[[target]], reference[[target]], bins)
        current_target.columns = reference_target.columns = [target]
    else:
        current_target, reference_target = discretize(data[[target]], bins), None
    return {
        "report": report,
        "preview": preview(data),
        "target_distribution": distribution(current_target, target),
        "reference_distribution": distribution(reference_target, target),
        "distribution_binned": bins is not None and pd.api.types.is_numeric_dtype(data[target]),
        "explanation": explain(data, target, bins, report),
    }


def explain(data, target, bins, report):
    """Concrete descriptive counts using the same bins as feature ranking."""
    from utilities.pyutils import discretize
    prepared = discretize(data, bins)
    values = prepared[target].value_counts()
    preferred = {"Rain": "rainy", "Machine condition": "broken", "fault": "fault", "MSFT": "up"}.get(target)
    event = preferred if preferred in values.index else values.index[0]
    outcome = prepared[target].eq(event)
    baseline = float(outcome.mean())
    examples = {}
    for row in report["features"]:
        feature = row["feature"]
        candidates = []
        for value, group in prepared.groupby(feature, observed=True):
            if len(group) < max(5, len(prepared) * 0.05):
                continue
            count = int(group[target].eq(event).sum())
            candidates.append({"state": str(value), "count": count, "total": len(group), "rate": count / len(group)})
        if candidates:
            examples[feature] = max(candidates, key=lambda item: (abs(item["rate"] - baseline), item["total"]))
    return {"event": str(event), "count": int(outcome.sum()), "total": len(prepared), "rate": baseline,
            "examples": examples, "unit": "hours" if target == "Rain" else "observations"}


def shuffle_payload(payload):
    """One repeatable teaching experiment; not a significance test."""
    result = analyze_payload(dict(payload, reference_csv=None))
    target, feature = result["report"]["target"], payload.get("feature")
    row = next((item for item in result["report"]["features"] if item["feature"] == feature), None)
    if row is None:
        raise ValueError("Choose a clue other than the outcome to mix up.")
    from utilities.pyutils import discretize
    from information.entropy import EntroPy
    data = discretize(read_observations(payload["csv"]), payload.get("bins"))
    shuffled = data[[feature]].sample(frac=1, random_state=7).set_axis(data.index)
    shared = EntroPy.mutual_information(data[[target]], shuffled)
    entropy = result["report"]["target_entropy_bits"]
    return {"feature": feature, "before_bits": row["mutual_information_bits"], "after_bits": shared,
            "before_fraction": row["fraction_of_target_information"], "after_fraction": min(1, shared / entropy) if entropy else 0,
            "target_entropy_bits": entropy, "counts_preserved": data[feature].value_counts().sort_index().equals(shuffled[feature].value_counts().sort_index()),
            "note": "One fixed shuffle, seed 7. Individual counts stay the same; row pairings change. This is an illustration, not a significance test; shuffling also destroys time ordering."}


def demo_payload(kind):
    if kind == "sensor":
        current, reference = demo_data()
        names = {"fault": "Machine condition", "thermal_state": "Temperature", "alarm": "Warning light", "zone": "Room"}
        current = current.drop(columns="batch").rename(columns=names).replace({"fault": "broken", "healthy": "working", "on": "lit", "east": "Room A", "west": "Room B"})
        reference = reference.drop(columns="batch").rename(columns=names).replace({"fault": "broken", "healthy": "working", "on": "lit", "east": "Room A", "west": "Room B"})
        title = "Does a warning light mean trouble?"
        detail = "Imagine checking a machine 160 times. Half the checks find it working; half find it broken. We made up its temperature, warning light, and room to show which clues are useful."
        target = "Machine condition"
    elif kind == "stocks":
        states = pd.read_csv(Path(__file__).with_name("data") / "stock-demo.csv", index_col="Date")
        split = len(states) // 2
        reference, current = states.iloc[:split], states.iloc[split:]
        title = "Sam's stock study"
        detail = (f"Original historical sample: {current.index[0]} to {current.index[-1]}. "
                  "Daily price moves: down below -0.5%, up above +0.5%, otherwise flat. Earlier dates form the reference.")
        target = "MSFT"
    else:
        raise ValueError("Unknown example. Choose stocks or sensor.")
    return {"kind": kind, "title": title, "description": detail, "target": target, "bins": None,
            "csv": current.to_csv(index=False), "reference_csv": reference.to_csv(index=False)}


class WorkbenchHandler(BaseHTTPRequestHandler):
    server_version = "EntroPy"

    def _send(self, status, body, content_type="application/json; charset=utf-8"):
        if not isinstance(body, bytes):
            body = json.dumps(body, allow_nan=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; connect-src 'self'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(body)

    def _local_request(self):
        allowed = {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"}
        if self.headers.get("Host") not in allowed:
            self._send(403, {"error": "This workbench accepts localhost requests only."})
            return False
        origin = self.headers.get("Origin")
        if origin and origin not in {"http://" + host for host in allowed}:
            self._send(403, {"error": "Open the workbench directly on localhost."})
            return False
        return True

    def do_GET(self):
        if not self._local_request():
            return
        request = urlsplit(self.path)
        if request.path == "/api/weather":
            try:
                self._send(200, fetch_weather(parse_qs(request.query).get("city", ["seattle"])[0]))
            except WeatherUnavailable as error:
                self._send(502, {"error": str(error)})
            except ValueError as error:
                self._send(400, {"error": str(error)})
            return
        if request.path == "/api/demo":
            try:
                self._send(200, demo_payload(parse_qs(request.query).get("kind", ["stocks"])[0]))
            except ValueError as error:
                self._send(400, {"error": str(error)})
            return
        files = {"/": ("index.html", "text/html; charset=utf-8"),
                 "/app.js": ("app.js", "text/javascript; charset=utf-8"),
                 "/style.css": ("style.css", "text/css; charset=utf-8")}
        if request.path not in files:
            self._send(404, {"error": "Not found"})
            return
        name, mime = files[request.path]
        self._send(200, (ASSETS / name).read_bytes(), mime)

    def do_POST(self):
        if not self._local_request():
            return
        if self.path not in {"/api/preview", "/api/analyze", "/api/shuffle"}:
            self._send(404, {"error": "Not found"})
            return
        if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
            self._send(415, {"error": "Send JSON input."})
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= MAX_BODY:
                raise ValueError("The upload is empty or exceeds the 6 MB request limit.")
            payload = json.loads(self.rfile.read(size))
            if not isinstance(payload, dict):
                raise ValueError("Expected an object containing CSV data.")
            if self.path == "/api/preview":
                result = preview(read_observations(payload.get("csv")))
            elif self.path == "/api/shuffle":
                result = shuffle_payload(payload)
            else:
                result = analyze_payload(payload)
        except (ValueError, TypeError, pd.errors.ParserError) as error:
            self._send(400, {"error": str(error)})
            return
        self._send(200, result)

    def log_message(self, format, *args):
        # Do not log uploaded data. Keep normal successful local requests quiet.
        if len(args) > 1 and str(args[1]) not in {"200", "304"}:
            super().log_message(format, *args)


def serve(port=8765, open_browser=False):
    server = ThreadingHTTPServer(("127.0.0.1", port), WorkbenchHandler)
    print(f"EntroPy workbench: http://127.0.0.1:{server.server_port}", flush=True)
    print("Keep this process running. Press Ctrl+C to stop.", flush=True)
    if open_browser:
        import webbrowser
        webbrowser.open(f"http://127.0.0.1:{server.server_port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
