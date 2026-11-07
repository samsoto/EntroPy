"""Bounded, on-demand public weather data for the guided browser example."""

from datetime import date, datetime, timedelta, timezone
import json
from threading import Lock
from time import monotonic
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd

CITIES = {
    "seattle": ("Seattle", 47.61, -122.33),
    "denver": ("Denver", 39.74, -104.99),
    "new-york": ("New York", 40.71, -74.01),
    "london": ("London", 51.51, -0.13),
    "tokyo": ("Tokyo", 35.68, 139.69),
    "sydney": ("Sydney", -33.87, 151.21),
}
VARIABLES = ["rain", "cloud_cover", "relative_humidity_2m", "temperature_2m", "wind_speed_10m", "pressure_msl"]
_cache = {}
_lock = Lock()


class WeatherUnavailable(ValueError):
    """The public source did not provide a usable sample."""


def prepare_weather(raw, city, source_url, fetched_at):
    """Validate, categorize, and split the actual returned hours chronologically."""
    try:
        hourly = raw["hourly"]
        frame = pd.DataFrame({key: hourly[key] for key in ["time"] + VARIABLES})
        times = pd.to_datetime(frame.pop("time"), errors="raise", utc=True)
        if times.isna().any() or times.duplicated().any() or not times.is_monotonic_increasing:
            raise ValueError("Invalid timestamps")
        for key in VARIABLES:
            frame[key] = pd.to_numeric(frame[key], errors="raise")
        if not np.isfinite(frame.to_numpy(dtype=float)).all():
            raise ValueError("Incomplete weather sample")
        if len(frame) != 2160:
            raise ValueError("Unexpected weather sample length")
        if (times.diff().dropna() != pd.Timedelta(hours=1)).any():
            raise ValueError("Missing hours")
        if ((frame[["cloud_cover", "relative_humidity_2m"]] < 0) |
                (frame[["cloud_cover", "relative_humidity_2m"]] > 100)).any().any():
            raise ValueError("Invalid percentages")
        if (frame[["rain", "wind_speed_10m"]] < 0).any().any():
            raise ValueError("Invalid rain or wind")
    except (KeyError, TypeError, ValueError, OverflowError) as error:
        raise WeatherUnavailable("The weather source returned incomplete data. Try another city or the built-in examples.") from error

    states = pd.DataFrame({
        "Rain": np.where(frame.rain >= 0.1, "rainy", "dry"),
        "Cloud cover": pd.cut(frame.cloud_cover, [-np.inf, 25, 75, np.inf], labels=["mostly clear", "partly cloudy", "overcast"], right=False),
        "Humidity": pd.cut(frame.relative_humidity_2m, [-np.inf, 40, 70, np.inf], labels=["low (<40%)", "moderate (40–69%)", "high (70%+)"], right=False),
        "Temperature": pd.cut(frame.temperature_2m, [-np.inf, 10, 20, np.inf], labels=["cool (<10°C)", "mild (10–19°C)", "warm (20°C+)"], right=False),
        "Wind": pd.cut(frame.wind_speed_10m, [-np.inf, 10, 25, np.inf], labels=["light (<10 km/h)", "breezy (10–24 km/h)", "windy (25+ km/h)"], right=False),
        "Pressure": pd.cut(frame.pressure_msl, [-np.inf, 1010, 1020, np.inf], labels=["low (<1010 hPa)", "middle (1010–1019 hPa)", "high (1020+ hPa)"], right=False),
    })
    split = len(states) // 2
    current, reference = states.iloc[split:], states.iloc[:split]
    current_times = times.iloc[split:]
    daily = pd.DataFrame({"day": current_times.dt.strftime("%Y-%m-%d"), "rainy": current.Rain.eq("rainy")}).groupby("day").rainy.agg(["sum", "count"])
    return {
        "kind": "weather", "title": f"Rain in {CITIES[city][0]}", "target": "Rain", "bins": None,
        "description": "Hourly weather estimates, grouped into everyday conditions. We compare conditions in the same hour to see which tell us most about rain.",
        "csv": current.to_csv(index=False), "reference_csv": reference.to_csv(index=False),
        "source": {"name": "Open-Meteo · ERA5 reanalysis", "url": "https://open-meteo.com/en/docs/historical-weather-api", "request_url": source_url,
                   "fetched_at": fetched_at, "start": current_times.iloc[0].strftime("%Y-%m-%d"), "end": current_times.iloc[-1].strftime("%Y-%m-%d"),
                   "reference_start": times.iloc[0].strftime("%Y-%m-%d"), "reference_end": times.iloc[split-1].strftime("%Y-%m-%d"),
                   "note": "Model-based historical estimates, not live station readings. Dates are UTC; the window ends 7 days ago to allow for the archive delay. Rain means at least 0.1 mm in an hour. Snow is excluded.",
                   "license": "CC BY 4.0", "license_url": "https://creativecommons.org/licenses/by/4.0/"},
        "timeline": [{"day": day, "rainy": int(row["sum"]), "hours": int(row["count"])} for day, row in daily.iterrows()],
    }


def fetch_weather(city="seattle", today=None):
    if city not in CITIES:
        raise ValueError("Choose one of the listed cities.")
    today = today or date.today()
    key = (city, today.isoformat())
    # Serialize fetches to avoid duplicate requests when several tabs open together.
    with _lock:
        cached = _cache.get(key)
        if cached and monotonic() - cached[0] < 1800:
            return dict(cached[1], cached=True)
        _, latitude, longitude = CITIES[city]
        end = today - timedelta(days=7)
        url = "https://archive-api.open-meteo.com/v1/archive?" + urlencode({
            "latitude": latitude, "longitude": longitude, "start_date": end - timedelta(days=89), "end_date": end,
            "hourly": ",".join(VARIABLES), "models": "era5", "timezone": "UTC",
        })
        try:
            with urlopen(Request(url, headers={"User-Agent": "EntroPy-local-workbench/0.2"}), timeout=15) as response:
                body = response.read(1024 * 1024 + 1)
            if len(body) > 1024 * 1024:
                raise ValueError("Oversized response")
            raw = json.loads(body)
        except (URLError, OSError, ValueError) as error:
            raise WeatherUnavailable("Couldn't reach the weather source. Retry in a moment, or open Sam's stock study or the device lesson below—both work offline.") from error
        payload = prepare_weather(raw, city, url, datetime.now(timezone.utc).isoformat(timespec="seconds"))
        if len(_cache) >= len(CITIES):
            _cache.clear()
        _cache[key] = (monotonic(), payload)
        return dict(payload, cached=False)
