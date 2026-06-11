"""Tests for the deployment-facing WSGI application."""
from __future__ import annotations

import json
import unittest
from io import BytesIO

from app import app


def request(path: str, method: str = "GET", body: bytes = b"", query_string: str = ""):
    captured = {}

    def start_response(status, headers):
        captured["status"] = status
        captured["headers"] = headers

    environ = {
        "REQUEST_METHOD": method,
        "PATH_INFO": path,
        "QUERY_STRING": query_string,
        "CONTENT_LENGTH": str(len(body)),
        "wsgi.input": BytesIO(body),
    }
    response = b"".join(app(environ, start_response))
    return captured["status"], dict(captured["headers"]), response


class TestWebApp(unittest.TestCase):
    def test_homepage_renders(self):
        status, headers, response = request("/")
        self.assertEqual(status, "200 OK")
        self.assertIn("text/html", headers["Content-Type"])
        self.assertIn(b"StyleWarehouse Robot Navigation", response)

    def test_health_endpoint(self):
        status, headers, response = request("/api/health")
        payload = json.loads(response.decode("utf-8"))
        self.assertEqual(status, "200 OK")
        self.assertIn("application/json", headers["Content-Type"])
        self.assertTrue(payload["ok"])

    def test_catalogue_search_endpoint(self):
        status, _, response = request("/api/catalogue", query_string="search=tee&limit=5")
        payload = json.loads(response.decode("utf-8"))
        self.assertEqual(status, "200 OK")
        self.assertGreaterEqual(payload["count"], 1)
        self.assertTrue(any(item["sku"] == "SW001" for item in payload["items"]))

    def test_simulate_order_endpoint(self):
        body = json.dumps(
            {"order_id": "API-TEST", "items": [{"sku": "SW001", "quantity": 1}]}
        ).encode("utf-8")
        status, _, response = request("/api/simulate-order", method="POST", body=body)
        payload = json.loads(response.decode("utf-8"))
        self.assertEqual(status, "200 OK")
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["order_id"], "API-TEST")

    def test_simulate_order_requires_items(self):
        body = json.dumps({"order_id": "EMPTY"}).encode("utf-8")
        status, _, response = request("/api/simulate-order", method="POST", body=body)
        payload = json.loads(response.decode("utf-8"))
        self.assertEqual(status, "400 Bad Request")
        self.assertFalse(payload["ok"])


if __name__ == "__main__":
    unittest.main()
