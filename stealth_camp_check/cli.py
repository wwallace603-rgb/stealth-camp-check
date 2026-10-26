"""stealth-camp-check — overnight parking & rest area rules by state.

Data is a snapshot of state DOT pages and statutes for rest-area vehicle
sleeping, plus BLM / national-forest / big-box guidance. This is a
community reference, not legal advice — confirm high-stakes situations
with the specific agency or a local call.

Web tool (all states, interactive): https://carsteader.com/tools/stealth-camp-check/
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

WEB = "https://carsteader.com/tools/stealth-camp-check/"
GUIDES = {
    "legal":   "https://carsteader.com/legal-stealth-camping-usa/",
    "gear":    "https://carsteader.com/stealth-camping-gear-list/",
}

_DATA_PATH = Path(__file__).parent / "states.json"


def _load():
    return json.loads(_DATA_PATH.read_text())


DATA = _load()
BLM = set(DATA["blmStates"])
STATUS_LABEL = {"ok": "OK", "limited": "LIMITED", "no": "NO", "signs": "SIGNS GOVERN"}

USE_COLOR = sys.stdout.isatty() and not __import__("os").environ.get("NO_COLOR")


def _c(code: str, s: str) -> str:
    return f"\x1b[{code}m{s}\x1b[0m" if USE_COLOR else str(s)


STATUS_COLOR = {"ok": "32", "limited": "33", "no": "31", "signs": "97"}


def find_state(arg: str):
    a = arg.strip().lower()
    for s in DATA["states"]:
        if s["ab"].lower() == a or s["name"].lower() == a:
            return s
    return None


def print_detail(s: dict) -> None:
    print()
    print(_c("1", s["name"]))
    limit = f" — {s['limit']}" if s.get("limit") else ""
    print(f"Rest areas: {_c(STATUS_COLOR[s['status']], STATUS_LABEL[s['status']])}{limit}")
    if s.get("note"):
        print("  " + s["note"])
    print()
    blm = "Yes — 14-day rule applies (western states)" if s["ab"] in BLM else "Not a primary BLM state"
    print(f"  BLM land ........ {blm}")
    print("  National forests  Dispersed camping generally OK unless posted (7–21 day limits vary)")
    print("  Big-box lots .... Private property, store-by-store — ask at the entrance")
    if s.get("src"):
        print()
        print("  Source: " + s["src"])
    print()
    print(_c("36", "More from CarSteader:"))
    print(f"  Web tool ........ {WEB}?state={s['ab']}")
    print(f"  Legal guide ..... {GUIDES['legal']}")
    print(f"  Stealth gear .... {GUIDES['gear']}")
    print()


def print_list() -> None:
    print()
    for s in DATA["states"]:
        ab = _c("1", s["ab"].ljust(3))
        st = _c(STATUS_COLOR[s["status"]], STATUS_LABEL[s["status"]].ljust(12))
        limit = (s.get("limit") or "—")[:52]
        print(f"  {ab} {st} {limit}")
    print()
    print(_c("36", WEB))
    print()


def usage() -> None:
    lines = [
        "",
        _c("1", "stealth-camp-check") + " — overnight parking & rest area rules by state",
        "",
        "Usage:",
        '  stealth-camp-check <state>         Rules for one state (code or name), e.g. "tx" or "Texas"',
        "  stealth-camp-check --list          Table of all 50 states + DC",
        "  stealth-camp-check <state> --json  Raw JSON for one state",
        "",
        "Examples:",
        "  stealth-camp-check tx",
        "  stealth-camp-check georgia",
        "  stealth-camp-check --list",
        "",
        _c("36", "Interactive web tool (all states): ") + WEB,
        "",
    ]
    print("\n".join(lines))


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or "--help" in args or "-h" in args:
        usage()
        return 0
    if "--list" in args or "-l" in args:
        print_list()
        return 0
    want_json = "--json" in args
    state_arg = next((a for a in args if not a.startswith("-")), None)
    if not state_arg:
        usage()
        return 1
    s = find_state(state_arg)
    if not s:
        print(f'Unknown state: "{state_arg}". Try --list to see codes.', file=sys.stderr)
        return 1
    if want_json:
        print(json.dumps(s, indent=2))
        return 0
    print_detail(s)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
