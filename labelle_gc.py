#!/usr/bin/env python3
"""Send LaBelle 202 LA Express keyboard presses through a Global Cache iTach IP2IR.

The sign's IR keyboard sends Philips RC5: system 0 = plain, 1 = Shift,
4 = Control; the 6-bit command is the key position.  Standard RC5 timing
(36 kHz, 889 us half-bits) is used by default.

The iTach IP2IR (710-1005) speaks the TCP API on port 4998, not the REST API:
  sendir,1:<port>,<id>,<freq>,<repeat>,<offset>,<on>,<off>,...\r
  -> completeir,1:<port>,<id>

Usage:
  labelle_gc.py keys                       list key names and legends
  labelle_gc.py send KEY [KEY ...]         e.g.  run 0 1   ctrl+new 0 1   edit
  labelle_gc.py type "HELLO THERE"         type text (plain/shift characters)
  labelle_gc.py raw SYS CMD                send any RC5 system/command
  labelle_gc.py scan SYS [FROM TO]         step through commands, pausing between
  labelle_gc.py pronto SYS CMD [TOGGLE]    print Pronto hex (no iTach needed)
  labelle_gc.py codes                      CSV of all 144 key codes with Pronto hex
  labelle_gc.py                            interactive prompt (same commands)

Options (before the command):
  --host IP      iTach address (default 192.168.1.187)
  --port N       IR port 1-3 (default 1)
  --repeat N     RC5 frames per press (default 2, like a short key tap)
  --delay S      seconds between presses (default 0.4)
  --dry-run      print the sendir strings instead of sending
  --timing T     standard (RC5 spec, 889 us @ 36 kHz; default) or captured (as learned, 818 us)
"""
import argparse
import csv
import os
import shlex
import socket
import sys
import time

DEFAULT_HOST = "192.168.1.187"
GC_PORT = 4998
# (carrier Hz, half-bit, full-bit, inter-frame gap) in carrier cycles.
TIMINGS = {
    # As captured (Pronto 0x006a): 818 us half-bits, ~8% fast.
    "captured": (39104, 32, 65, 3276),
    # Philips RC5 spec: 36 kHz, 889 us half-bits, 113.8 ms frame period.
    "standard": (36000, 32, 64, 3200),
}
# Standard timing is the default: with captured timing the sign sometimes
# misread -> (cmd 3) as Z (cmd 1), a late-bit error from the fast half-bits.
DEFAULT_TIMING = "standard"
TOGGLE_FILE = os.path.expanduser("~/.cache/labelle-ir-toggle")

# RC5 command for each physical key (system 0 names), decoded from the IR file.
KEY_CMD = {
    "Z": 1, "SPACE": 2, "->": 3, "A": 4, "LAMP": 5, "Q": 6, "1": 7,
    "X": 9, "/": 10, "<-": 11, "S": 12, "=": 13, "W": 14, "2": 15,
    "C": 17, ";": 18, "RUN": 19, "D": 20, "-": 21, "E": 22, "3": 23,
    "V": 25, ".": 26, "EDIT": 27, "F": 28, "0": 29, "R": 30, "4": 31,
    "B": 33, "L": 34, "P": 35, "G": 36, "9": 37, "T": 38, "5": 39,
    "N": 41, ",": 42, "O": 43, "H": 44, "8": 45, "Y": 46, "6": 47,
    "M": 49, "K": 50, "I": 51, "J": 52, "7": 53, "U": 54,
}
PLAIN, SHIFT, CONTROL = 0, 1, 4

# Control-layer legends printed on the IR keyboard (blue/orange).
CONTROL_LEGEND = {
    "TWINKLE": "1", "TEAR": "2", "PAINT": "3", "WIGGLE": "4", "SLIDE": "5",
    "JAWS": "6", "SWIRL": "7", "SHOOT": "8", "F1": "9", "F2": "0",
    "F3": "-", "F4": "=", "CAPLOCK": "LAMP",
    "PAUSE": "Q", "WIDE": "W", "FLASH": "E", "BLINK": "R", "REVERSE": "T",
    "RANDOM": "Y", "OPEN": "U", "CLOSE": "I", "SCAN": "O", "WIPE": "P",
    "MEMORY": "EDIT", "NEW": "RUN",
    "TIME": "A", "DAY": "S", "DATE": "D", "IDLE": "F", "CENTER": "G",
    "ROTLEFT": "H", "ROTRIGHT": "J", "INSTANT": "K", "DROP": "L",
    "SCHEDULE": ";", "INSERT": "<-", "DELETE": "->",
    "SPEED": "Z", "GRAPHIC": "X", "TONE": "C", "SCROLLUP": "V",
    "SCROLLDOWN": "B", "KICKON": "N", "KICKOFF": "M", "OPTIONS": ",",
    "DEMO": ".", "CLEAREND": "/",
}
# Shift-layer legends: ↑/↓ on the arrow keys, punctuation on the rest.
SHIFT_LEGEND = {"UP": "<-", "DOWN": "->"}
SHIFT_CHARS = {
    "!": "1", '"': "2", "#": "3", "$": "4", "%": "5", "¢": "6", "&": "7",
    "*": "8", "(": "9", ")": "0", "'": "-", "+": "=", ":": ";", "<": ",",
    ">": ".", "?": "/", "£": "LAMP", "Ñ": "EDIT",
}
ALIASES = {"LEFT": "<-", "RIGHT": "->", "SPACEBAR": "SPACE", " ": "SPACE"}
# Plain arrows are swapped so they move the message the way the arrow points.
# Control+<- (Insert), Control+-> (Delete) and Shift (up/down) are unchanged.
PLAIN_SWAP = {"<-": "->", "->": "<-"}


def parse_key(token):
    """'run', 'ctrl+new', 'shift+run', 'control+1', '$', 'up' -> (system, command, label)."""
    if token == " ":  # typed space; strip() below would otherwise empty it
        return PLAIN, KEY_CMD["SPACE"], "SPACE"
    t = token.strip()
    parts = t.split("+") if len(t) > 1 else [t]
    mod, key = (parts[0].upper(), "+".join(parts[1:])) if len(parts) > 1 else (None, parts[0])
    ku = ALIASES.get(key.upper(), key.upper())
    ku = ku.replace(" ", "").replace("_", "") if ku not in KEY_CMD else ku
    if mod in ("CTRL", "CONTROL", "C"):
        base = CONTROL_LEGEND.get(ku, ku)
        return CONTROL, KEY_CMD[base], f"Control+{base}"
    if mod in ("SHIFT", "S"):
        base = SHIFT_LEGEND.get(ku, ku)
        return SHIFT, KEY_CMD[base], f"Shift+{base}"
    if mod is not None:
        raise KeyError(token)
    if key in SHIFT_CHARS:
        return SHIFT, KEY_CMD[SHIFT_CHARS[key]], f"Shift+{SHIFT_CHARS[key]}"
    if ku in SHIFT_LEGEND:
        return SHIFT, KEY_CMD[SHIFT_LEGEND[ku]], f"Shift+{SHIFT_LEGEND[ku]}"
    if ku in CONTROL_LEGEND and ku not in KEY_CMD:
        base = CONTROL_LEGEND[ku]
        return CONTROL, KEY_CMD[base], f"Control+{base}"
    return PLAIN, KEY_CMD[PLAIN_SWAP.get(ku, ku)], ku


def rc5_timings(system, command, toggle, timing=DEFAULT_TIMING):
    """Carrier-cycle on/off list for one RC5 frame (13 bits after start bit S1)."""
    _, short, long_, gap = TIMINGS[timing]
    bits = [1, 1, toggle] + [(system >> i) & 1 for i in range(4, -1, -1)] \
        + [(command >> i) & 1 for i in range(5, -1, -1)]
    halves = "".join("01" if b else "10" for b in bits)[1:].rstrip("0")
    runs, prev = [], None
    for h in halves:
        if h == prev:
            runs[-1] += 1
        else:
            runs.append(1)
        prev = h
    return [short if n == 1 else long_ for n in runs] + [gap]


def rc5_pronto(system, command, toggle=0, timing=DEFAULT_TIMING):
    """Pronto hex for one RC5 frame (durations are carrier cycles, as in sendir)."""
    freq = TIMINGS[timing][0]
    durs = rc5_timings(system, command, toggle, timing)
    words = [0, round(1e6 / (freq * 0.241246)), 0, len(durs) // 2] + durs
    return " ".join(f"{w:04x}" for w in words)


PRETTY = {"CAPLOCK": "Cap Lock", "ROTLEFT": "Rot ←", "ROTRIGHT": "Rot →",
          "KICKON": "Kick On", "KICKOFF": "Kick Off", "SCROLLUP": "Scroll ↑",
          "SCROLLDOWN": "Scroll ↓", "CLEAREND": "Clear End"}


def write_codes(out):
    """All 48 keys x plain/Shift/Control with Pronto hex for both toggle values."""
    ctrl = {k: PRETTY.get(n, n.title() if len(n) > 2 else n) for n, k in CONTROL_LEGEND.items()}
    shift = {k: c for c, k in SHIFT_CHARS.items()} | {"<-": "↑", "->": "↓"}
    cap = {"<-": "←", "->": "→", "SPACE": "Space", "LAMP": "Lamp", "EDIT": "Edit", "RUN": "Run"}
    w = csv.writer(out)
    w.writerow(["key", "layer", "legend", "rc5_system", "rc5_command",
                "pronto_toggle0", "pronto_toggle1"])
    for layer, system in (("plain", PLAIN), ("shift", SHIFT), ("control", CONTROL)):
        for key, cmd in sorted(KEY_CMD.items(), key=lambda kv: kv[1]):
            name = cap.get(key, key)
            legend = {"plain": name, "shift": shift.get(key, f"Shift+{name}"),
                      "control": ctrl.get(key, "")}[layer]
            w.writerow([name, layer, legend, system, cmd,
                        rc5_pronto(system, cmd, 0), rc5_pronto(system, cmd, 1)])


class Toggle:
    """RC5 toggle bit: flips on every new key press, persisted across runs."""

    def __init__(self):
        try:
            self.value = int(open(TOGGLE_FILE).read().strip()) & 1
        except (OSError, ValueError):
            self.value = 0

    def next(self):
        self.value ^= 1
        try:
            os.makedirs(os.path.dirname(TOGGLE_FILE), exist_ok=True)
            open(TOGGLE_FILE, "w").write(str(self.value))
        except OSError:
            pass
        return self.value


class ITach:
    def __init__(self, host, ir_port, repeat, delay, dry_run, timing=DEFAULT_TIMING):
        self.host, self.ir_port, self.timing = host, ir_port, timing
        self.repeat, self.delay, self.dry_run = repeat, delay, dry_run
        self.toggle = Toggle()
        self.seq = 0
        self.sock = None

    def _connect(self):
        if self.sock is None:
            self.sock = socket.create_connection((self.host, GC_PORT), timeout=5)
            self.buf = b""

    def _readline(self):
        while b"\r" not in self.buf:
            chunk = self.sock.recv(1024)
            if not chunk:
                raise ConnectionError("iTach closed the connection")
            self.buf += chunk
        line, self.buf = self.buf.split(b"\r", 1)
        return line.decode(errors="replace").strip()

    def command(self, text):
        self._connect()
        self.sock.sendall(text.encode() + b"\r")
        return self._readline()

    def press(self, system, command, label="", held=False):
        """Send one key press; held=True repeats the previous toggle (key still down)."""
        self.seq = (self.seq % 65535) + 1
        toggle = self.toggle.value if held else self.toggle.next()
        timings = rc5_timings(system, command, toggle, self.timing)
        cmd = (f"sendir,1:{self.ir_port},{self.seq},{TIMINGS[self.timing][0]},"
               f"{self.repeat},1," + ",".join(map(str, timings)))
        tag = f"{label or '?':16s} sys={system} cmd={command:2d} t={toggle} {self.timing[:3]}"
        if self.dry_run:
            print(f"{tag}\n  {cmd}")
            return
        reply = self.command(cmd)
        ok = reply.startswith("completeir")
        print(f"{tag}  {'ok' if ok else reply}")
        if not ok:
            raise RuntimeError(reply)
        time.sleep(self.delay)
        return toggle

    def close(self):
        if self.sock:
            self.sock.close()


def list_keys():
    print("Plain keys:  " + " ".join(k for k in KEY_CMD))
    print("  (aliases: left = <-, right = ->, space)")
    print("\nControl legends (ctrl+NAME, or just NAME):")
    for name, key in CONTROL_LEGEND.items():
        print(f"  {name.lower():11s} = Control+{key:5s} (sys 4 cmd {KEY_CMD[key]})")
    print("\nShift: up = Shift+<-, down = Shift+->, and the shifted characters "
          + " ".join(SHIFT_CHARS))
    print("\nExamples:  run 0 1 | ctrl+new 0 1 | shift+run | memory | type HELLO")


def run_command(tach, words):
    if not words:
        return
    op, args = words[0].lower(), words[1:]
    if op == "keys":
        list_keys()
    elif op == "send":
        for tok in args:
            tach.press(*parse_key(tok))
    elif op == "type":
        for ch in " ".join(args):
            tach.press(*parse_key(ch.upper() if ch.isalpha() else ch))
    elif op == "raw":
        tach.press(int(args[0]), int(args[1]), "raw")
    elif op == "scan":
        system = int(args[0])
        lo, hi = (int(args[1]), int(args[2])) if len(args) >= 3 else (0, 63)
        for c in range(lo, hi + 1):
            tach.press(system, c, "scan")
            input("  Enter for next, Ctrl-C to stop ")
    elif op == "pronto":
        print(rc5_pronto(int(args[0]), int(args[1]), int(args[2]) if len(args) > 2 else 0,
                         tach.timing))
    elif op == "codes":
        write_codes(sys.stdout)
    elif op == "cmd":
        print(tach.command(" ".join(args)))
    else:
        # Bare key names are sent directly: "run", "ctrl+new", "0", "1".
        for tok in words:
            tach.press(*parse_key(tok))


def interactive(tach):
    print(f"Labelle IR via iTach {tach.host} port {tach.ir_port}. "
          "Type 'keys' for names, 'quit' to exit.")
    while True:
        try:
            line = input("labelle> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if line.lower() in ("quit", "exit", "q"):
            return
        try:
            words = shlex.split(line)
            if words and words[0].lower() == "type":
                words = ["type", line.split(None, 1)[1] if " " in line else ""]
            run_command(tach, words)
        except KeyError as e:
            print(f"  unknown key {e}")
        except (OSError, RuntimeError, ValueError, IndexError) as e:
            print(f"  error: {e}")
            tach.close()
            tach.sock = None


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--host", default=DEFAULT_HOST)
    ap.add_argument("--port", type=int, default=1)
    ap.add_argument("--repeat", type=int, default=2)
    ap.add_argument("--delay", type=float, default=0.4)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--timing", choices=TIMINGS, default=DEFAULT_TIMING)
    ap.add_argument("-h", "--help", action="store_true")
    opts, rest = ap.parse_known_args()
    if opts.help:
        print(__doc__)
        return
    tach = ITach(opts.host, opts.port, opts.repeat, opts.delay, opts.dry_run, opts.timing)
    try:
        if rest:
            run_command(tach, rest)
        else:
            interactive(tach)
    except KeyError as e:
        sys.exit(f"unknown key {e} (try: keys)")
    finally:
        tach.close()


if __name__ == "__main__":
    main()
