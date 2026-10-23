import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import http_probe  # noqa: E402


class ProbeTests(unittest.TestCase):
    def test_probe_success(self) -> None:
        class Resp:
            status = 200

            def read(self) -> bytes:
                return b"ok"

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

        with patch("http_probe.urllib.request.urlopen", return_value=Resp()):
            result = http_probe.probe("https://example.com", timeout=5.0)
        self.assertTrue(result.ok)
        self.assertEqual(result.status, 200)
        self.assertEqual(result.bytes, 2)

    def test_probe_http_error(self) -> None:
        import urllib.error

        def raise_http(*_args, **_kwargs):
            raise urllib.error.HTTPError(
                "https://example.com", 500, "err", hdrs=None, fp=None
            )

        with patch("http_probe.urllib.request.urlopen", side_effect=raise_http):
            result = http_probe.probe("https://example.com", timeout=5.0)
        self.assertFalse(result.ok)
        self.assertEqual(result.status, 500)

    def test_cli_rejects_bad_timeout(self) -> None:
        with self.assertRaises(SystemExit):
            http_probe.main(["https://example.com", "--timeout", "0"])


if __name__ == "__main__":
    unittest.main()
