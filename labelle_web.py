#!/usr/bin/env python3
"""Web keyboard for the Labelle 202 LA Express, sending IR via the iTach IP2IR.

Serves web/index.html and a small JSON API:
  POST /api/press  {"sys": 0|1|4, "cmd": 0-63, "label": "...", "held": false}
  POST /api/type   {"text": "HELLO"}
  GET  /api/status -> iTach version / reachability

Usage: labelle_web.py [--listen 0.0.0.0] [--http-port 8765] [--host 192.168.1.187] [--port 1]
Then open http://<this machine>:8765/ on the phone and Add to Home Screen.
"""
import argparse
import json
import os
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

import labelle_gc

WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")


class Sender:
    """Serializes access to one persistent iTach connection."""

    def __init__(self, host, ir_port, repeat, timing):
        self.tach = labelle_gc.ITach(host, ir_port, repeat, 0, False, timing)
        self.lock = threading.Lock()

    def _retry(self, fn):
        with self.lock:
            try:
                return fn()
            except (OSError, ConnectionError):
                self.tach.close()
                self.tach.sock = None
                return fn()

    def press(self, system, command, label, held):
        return self._retry(lambda: self.tach.press(system, command, label, held))

    def version(self):
        return self._retry(lambda: self.tach.command("getversion"))


class Handler(SimpleHTTPRequestHandler):
    sender = None

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=WEB_DIR, **kw)

    def log_message(self, fmt, *args):
        pass  # key presses are logged by ITach.press

    def _json(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def end_headers(self):
        if not self.path.startswith("/api/"):
            self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def do_GET(self):
        if self.path == "/api/status":
            try:
                self._json(200, {"ok": True, "version": self.sender.version(),
                                 "host": self.sender.tach.host,
                                 "port": self.sender.tach.ir_port,
                                 "timing": self.sender.tach.timing})
            except Exception as e:  # noqa: BLE001 - report any failure to the page
                self._json(200, {"ok": False, "error": str(e)})
            return
        super().do_GET()

    def do_POST(self):
        try:
            n = int(self.headers.get("Content-Length", 0))
            req = json.loads(self.rfile.read(n) or b"{}")
            if self.path == "/api/press":
                system, command = int(req["sys"]), int(req["cmd"])
                if system not in range(32) or command not in range(64):
                    raise ValueError("sys must be 0-31, cmd 0-63")
                toggle = self.sender.press(system, command, req.get("label", ""),
                                           bool(req.get("held")))
                self._json(200, {"ok": True, "toggle": toggle})
            elif self.path == "/api/timing":
                timing = str(req.get("timing"))
                if timing not in labelle_gc.TIMINGS:
                    raise ValueError(f"timing must be one of {list(labelle_gc.TIMINGS)}")
                self.sender.tach.timing = timing
                print(f"-- timing now {timing}")
                self._json(200, {"ok": True, "timing": timing})
            elif self.path == "/api/type":
                # Resolve every character first so a bad one sends nothing.
                keys = []
                for ch in str(req.get("text", "")):
                    try:
                        keys.append(labelle_gc.parse_key(ch.upper() if ch.isalpha() else ch))
                    except KeyError:
                        raise ValueError(f"no key for {ch!r}; nothing was sent") from None
                for s, c, label in keys:
                    self.sender.press(s, c, label, False)
                self._json(200, {"ok": True})
            else:
                self._json(404, {"ok": False, "error": "not found"})
        except KeyError as e:
            self._json(400, {"ok": False, "error": f"unknown key {e}"})
        except Exception as e:  # noqa: BLE001
            self._json(500, {"ok": False, "error": str(e)})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--listen", default="0.0.0.0")
    ap.add_argument("--http-port", type=int, default=8765)
    ap.add_argument("--host", default=labelle_gc.DEFAULT_HOST, help="iTach address")
    ap.add_argument("--port", type=int, default=1, help="iTach IR port")
    ap.add_argument("--repeat", type=int, default=2, help="RC5 frames per press")
    ap.add_argument("--timing", choices=labelle_gc.TIMINGS, default=labelle_gc.DEFAULT_TIMING)
    args = ap.parse_args()
    sys.stdout.reconfigure(line_buffering=True)  # log each key press as it's sent
    Handler.sender = Sender(args.host, args.port, args.repeat, args.timing)
    srv = ThreadingHTTPServer((args.listen, args.http_port), Handler)
    print(f"Labelle web keyboard on http://{args.listen}:{args.http_port}/ "
          f"-> iTach {args.host} IR port {args.port}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
