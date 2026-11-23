"""
WikiLife Core - Unit Tests for LocalYusraClient (PATH03-BR09)
Uses Python 3.12 stdlib unittest & mock so it passes cleanly in GitHub Actions without a live Ollama server.
"""

import io
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Ensure src/ is importable regardless of test runner working directory
SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from local_yusra import DEFAULT_MODEL, OLLAMA_HOST, LocalYusraClient


class TestLocalYusraClient(unittest.TestCase):
    def setUp(self) -> None:
        self.client = LocalYusraClient()

    def test_default_configuration(self) -> None:
        self.assertEqual(self.client.model, DEFAULT_MODEL)
        self.assertEqual(self.client.host, OLLAMA_HOST)

    @patch("urllib.request.urlopen")
    def test_is_alive_success(self, mock_urlopen: MagicMock) -> None:
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        self.assertTrue(self.client.is_alive())

    @patch("urllib.request.urlopen")
    def test_chat_non_streaming(self, mock_urlopen: MagicMock) -> None:
        fake_body = json.dumps({"message": {"content": "WikiLife Ready"}}).encode("utf-8")
        mock_resp = MagicMock()
        mock_resp.read.return_value = fake_body
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        reply = self.client.chat("Ping", stream=False)
        self.assertEqual(reply, "WikiLife Ready")

    @patch("urllib.request.urlopen")
    def test_chat_streaming(self, mock_urlopen: MagicMock) -> None:
        lines = [
            json.dumps({"message": {"content": "Hello "}, "done": False}).encode("utf-8") + b"\n",
            json.dumps({"message": {"content": "Yusra"}, "done": True}).encode("utf-8") + b"\n",
        ]
        mock_resp = MagicMock()
        mock_resp.__iter__.return_value = iter(lines)
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        tokens = list(self.client.chat("Hi", stream=True))
        self.assertEqual("".join(tokens), "Hello Yusra")

    @patch("urllib.request.urlopen")
    def test_unload_vram(self, mock_urlopen: MagicMock) -> None:
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        self.assertTrue(self.client.unload_vram())


if __name__ == "__main__":
    unittest.main(verbosity=2)
