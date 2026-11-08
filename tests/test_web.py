import json
from http.server import ThreadingHTTPServer
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from information.web import WorkbenchHandler, analyze_payload, demo_payload, read_observations, shuffle_payload


class WebTests(unittest.TestCase):
    def test_shuffle_preserves_counts_but_breaks_known_pairing(self):
        payload = demo_payload("sensor")
        result = shuffle_payload(dict(payload, feature="Temperature"))
        self.assertEqual(result["before_bits"], 1)
        self.assertLess(result["after_bits"], 0.05)
        self.assertEqual(result["target_entropy_bits"], 1)
        self.assertTrue(result["counts_preserved"])
        self.assertEqual(result, shuffle_payload(dict(payload, feature="Temperature")))
        with self.assertRaises(ValueError):
            shuffle_payload(dict(payload, feature="Machine condition"))

    def test_sensor_demo_uses_real_audit(self):
        payload = demo_payload("sensor")
        result = analyze_payload(payload)
        features = {row["feature"]: row["mutual_information_bits"] for row in result["report"]["features"]}
        self.assertEqual(features["Temperature"], 1)
        self.assertAlmostEqual(features["Warning light"], 0.2780719051126377)
        example = result["explanation"]["examples"]["Temperature"]
        self.assertEqual(example["total"], 80)
        self.assertEqual(result["explanation"]["event"], "broken")

    def test_stock_demo_is_categorical_and_has_reference(self):
        payload = demo_payload("stocks")
        result = analyze_payload(payload)
        self.assertEqual(result["report"]["target"], "MSFT")
        self.assertEqual(result["report"]["rows"], 502)
        self.assertEqual(result["report"]["reference_rows"], 502)
        self.assertEqual(set(read_observations(payload["csv"]).MSFT), {"up", "flat", "down"})

    def test_empty_duplicate_and_excess_columns_rejected(self):
        for text in ["", "a,a\n1,2", "a,\n1,2", "a\n", ",".join(str(i) for i in range(61)) + "\n" + ",".join("0" for _ in range(61))]:
            with self.subTest(text=text[:20]), self.assertRaises(ValueError):
                read_observations(text)

    def test_missing_values_are_visible_then_rejected(self):
        payload = {"csv": "x,y\n1,a\n,b", "target": "x"}
        with self.assertRaisesRegex(ValueError, "missing"):
            analyze_payload(payload)

    def test_bins_validate_and_support_numeric_target(self):
        payload = {"csv": "x,y\n1,a\n2,b\n3,c", "target": "x", "bins": 2}
        self.assertTrue(analyze_payload(payload)["distribution_binned"])
        for bins in [True, 1, 101, "8"]:
            with self.assertRaises(ValueError):
                analyze_payload(dict(payload, bins=bins))

    def test_http_assets_api_and_origin_boundary(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), WorkbenchHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_port}"
        try:
            with urlopen(base) as response:
                self.assertIn(b'id="weather-load"', response.read())
                self.assertIn("frame-ancestors 'none'", response.headers["Content-Security-Policy"])
            body = json.dumps(demo_payload("sensor")).encode()
            request = Request(base + "/api/analyze", data=body, headers={"Content-Type": "application/json"})
            with urlopen(request) as response:
                self.assertEqual(json.load(response)["report"]["rows"], 160)
            request.add_header("Origin", "https://unrelated.example")
            with self.assertRaises(HTTPError) as caught:
                urlopen(request)
            self.assertEqual(caught.exception.code, 403)
            with self.assertRaises(HTTPError) as caught:
                urlopen(base + "/../pyproject.toml")
            self.assertEqual(caught.exception.code, 404)
        finally:
            server.shutdown(); server.server_close(); thread.join()


if __name__ == "__main__":
    unittest.main()
