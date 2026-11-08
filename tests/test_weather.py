from copy import deepcopy
from datetime import date
from io import BytesIO
import json
import unittest
from unittest.mock import patch
from urllib.error import URLError

import pandas as pd

from information import weather
from information.web import analyze_payload, read_observations


def weather_fixture():
    # Independent known answer: rain and cloud cover agree perfectly;
    # all other measurements are constant. This is a contract fixture, not live data.
    n = 2160
    return {"hourly": {
        "time": pd.date_range("2026-01-01", periods=n, freq="h").strftime("%Y-%m-%dT%H:%M").tolist(),
        "rain": [0.0, 0.1] * (n // 2), "cloud_cover": [0, 90] * (n // 2),
        "relative_humidity_2m": [50] * n, "temperature_2m": [15] * n,
        "wind_speed_10m": [5] * n, "pressure_msl": [1015] * n,
    }}


class WeatherTests(unittest.TestCase):
    def setUp(self):
        weather._cache.clear()

    def test_chronological_split_counts_and_independent_known_answer(self):
        payload = weather.prepare_weather(weather_fixture(), "seattle", "https://example.test", "2026-04-07T00:00:00Z")
        result = analyze_payload(payload)
        self.assertEqual(result["report"]["rows"], 1080)
        self.assertEqual(result["report"]["reference_rows"], 1080)
        self.assertEqual(result["report"]["features"][0]["feature"], "Cloud cover")
        self.assertAlmostEqual(result["report"]["features"][0]["mutual_information_bits"], 1)
        self.assertEqual(result["explanation"]["count"], 540)
        self.assertEqual(len(payload["timeline"]), 45)
        self.assertEqual(sum(day["rainy"] for day in payload["timeline"]), 540)
        self.assertLess(payload["source"]["reference_end"], payload["source"]["start"])

    def test_threshold_boundaries(self):
        raw = weather_fixture()
        raw["hourly"]["rain"][-3:] = [0, 0.09, 0.1]
        raw["hourly"]["cloud_cover"][-3:] = [24.9, 25, 75]
        data = read_observations(weather.prepare_weather(raw, "seattle", "url", "now")["csv"])
        self.assertEqual(data.Rain.tail(3).tolist(), ["dry", "dry", "rainy"])
        self.assertEqual(data["Cloud cover"].tail(3).tolist(), ["mostly clear", "partly cloudy", "overcast"])

    def test_incomplete_nonfinite_and_disordered_samples_are_rejected(self):
        original = weather_fixture()
        for variable, replacement in [("rain", None), ("rain", -1), ("cloud_cover", 101), ("temperature_2m", float("inf")), ("time", "2026-01-01T00:00")]:
            raw = deepcopy(original)
            raw["hourly"][variable][-1] = replacement
            with self.subTest(variable=variable, replacement=replacement), self.assertRaises(weather.WeatherUnavailable):
                weather.prepare_weather(raw, "seattle", "url", "now")
        raw = deepcopy(original)
        for values in raw["hourly"].values():
            values.pop()
        with self.assertRaises(weather.WeatherUnavailable):
            weather.prepare_weather(raw, "seattle", "url", "now")

    def test_fixed_source_cache_and_invalid_city(self):
        body = json.dumps(weather_fixture()).encode()
        with patch.object(weather, "urlopen", return_value=BytesIO(body)) as fetch:
            first = weather.fetch_weather("seattle", date(2026, 4, 7))
            second = weather.fetch_weather("seattle", date(2026, 4, 7))
            self.assertFalse(first["cached"])
            self.assertTrue(second["cached"])
            self.assertEqual(fetch.call_count, 1)
            url = fetch.call_args.args[0].full_url
            self.assertTrue(url.startswith("https://archive-api.open-meteo.com/v1/archive?"))
            self.assertIn("start_date=2026-01-01", url)
            self.assertIn("end_date=2026-03-31", url)
            with self.assertRaises(ValueError):
                weather.fetch_weather("http://localhost")
            self.assertEqual(fetch.call_count, 1)

    def test_upstream_failure_is_actionable_and_never_fake_weather(self):
        with patch.object(weather, "urlopen", side_effect=URLError("offline")):
            with self.assertRaisesRegex(weather.WeatherUnavailable, "offline"):
                weather.fetch_weather()
        self.assertFalse(weather._cache)

    def test_no_rain_has_no_explainable_uncertainty(self):
        raw = weather_fixture()
        raw["hourly"]["rain"] = [0] * 2160
        result = analyze_payload(weather.prepare_weather(raw, "seattle", "url", "now"))
        self.assertEqual(result["report"]["target_entropy_bits"], 0)
        self.assertEqual(result["explanation"]["event"], "dry")
        self.assertTrue(all(row["mutual_information_bits"] == 0 for row in result["report"]["features"]))


if __name__ == "__main__":
    unittest.main()
