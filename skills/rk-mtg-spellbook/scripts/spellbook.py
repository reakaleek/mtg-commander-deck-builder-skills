#!/usr/bin/env python3
"""Commander Spellbook helper: combos and bracket estimates."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

API = "https://backend.commanderspellbook.com"
USER_AGENT = "mtg-commander-deck-builder-skills/1.0 (spellbook helper)"
MIN_INTERVAL_SEC = 0.55
CACHE_TTL_SEC = 24 * 60 * 60
DEFAULT_CACHE = Path.home() / ".cache" / "spellbook"
LINE_QTY_RE = re.compile(r"^(\d+)\s*x?\s+(.*)$", re.IGNORECASE)
SET_CODE_RE = re.compile(r"^[A-Za-z0-9]{2,6}$")
ZONE_COMMAND = {
    "commander",
    "commanders",
    "command zone",
    "command",
    "cmdr",
    "companion",
    "partner",
    "partners",
    "background",
    "backgrounds",
}

_last_call = 0.0


def _wait() -> None:
    global _last_call
    elapsed = time.monotonic() - _last_call
    if _last_call and elapsed < MIN_INTERVAL_SEC:
        time.sleep(MIN_INTERVAL_SEC - elapsed)


def http_json(method: str, url: str, body: dict[str, Any] | None = None, retries: int = 2) -> dict[str, Any]:
    global _last_call
    data = None
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    last_error: Exception | None = None
    for attempt in range(retries + 1):
        _wait()
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            _last_call = time.monotonic()
            return payload
        except urllib.error.HTTPError as e:
            payload = e.read().decode("utf-8", errors="replace")
            _last_call = time.monotonic()
            if e.code == 429 and attempt < retries:
                time.sleep(30)
                last_error = RuntimeError(f"Spellbook HTTP 429: {payload}")
                continue
            raise RuntimeError(f"Spellbook HTTP {e.code}: {payload}") from e
        except urllib.error.URLError as e:
            last_error = e
            if attempt < retries:
                time.sleep(2)
                continue
            raise RuntimeError(f"Spellbook request failed: {e}") from e
    raise RuntimeError(f"Spellbook request failed: {last_error}")


def parse_name(rest: str) -> str:
    rest = rest.strip()
    lab = re.search(r"\s+\^([^^]+)\^\s*$", rest)
    if lab:
        rest = rest[: lab.start()].rstrip()
    while True:
        cat = re.search(r"\s+\[([^\]]+)\]\s*$", rest)
        if not cat:
            break
        rest = rest[: cat.start()].rstrip()
    tick = re.search(r"\s+`([^`]+)`\s*$", rest)
    if tick:
        rest = rest[: tick.start()].rstrip()
    foil_m = re.search(r"\s+\*[Ff]\*\s*$", rest)
    if foil_m:
        rest = rest[: foil_m.start()].rstrip()
    set_cn = re.search(r"\s+\(([^)]+)\)\s+(\S+)\s*$", rest)
    if set_cn and SET_CODE_RE.fullmatch(set_cn.group(1)):
        rest = rest[: set_cn.start()].rstrip()
    else:
        set_only = re.search(r"\s+\(([^)]+)\)\s*$", rest)
        if set_only and SET_CODE_RE.fullmatch(set_only.group(1)):
            rest = rest[: set_only.start()].rstrip()
    return rest.strip()


def categories_of(raw: str) -> list[str]:
    cats: list[str] = []
    for match in re.finditer(r"\[([^\]]+)\]", raw):
        cats.extend(p.strip() for p in match.group(1).split(",") if p.strip())
    return cats


def parse_deck(text: str) -> tuple[list[dict[str, Any]], list[str]]:
    rows: list[dict[str, Any]] = []
    file_commanders: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith(("#", "//")):
            continue
        match = LINE_QTY_RE.match(line)
        if not match:
            continue
        qty = int(match.group(1))
        name = parse_name(match.group(2))
        if not name:
            continue
        rows.append({"card": name, "quantity": qty})
        if any(c.lower() in ZONE_COMMAND for c in categories_of(line)):
            if name not in file_commanders:
                file_commanders.append(name)
    return rows, file_commanders


def deck_payload(text: str, commanders: list[str]) -> dict[str, Any]:
    rows, file_commanders = parse_deck(text)
    command_names = [n for n in commanders if n] or file_commanders
    command_set = {n.lower() for n in command_names}
    command_qty: dict[str, int] = {n: 1 for n in command_names}
    main: list[dict[str, Any]] = []
    for row in rows:
        if row["card"].lower() in command_set:
            command_qty[row["card"]] = row["quantity"]
            continue
        main.append(row)
    return {
        "commanders": [{"card": name, "quantity": command_qty.get(name, 1)} for name in command_names],
        "main": main,
    }


def cache_path(cache_dir: Path, kind: str, body: dict[str, Any]) -> Path:
    digest = hashlib.sha256(json.dumps(body, sort_keys=True).encode("utf-8")).hexdigest()[:16]
    return cache_dir / kind / f"{digest}.json"


def fetch_cached(
    kind: str,
    url: str,
    body: dict[str, Any],
    cache_dir: Path,
    fresh: bool,
) -> tuple[dict[str, Any], bool]:
    dest = cache_path(cache_dir, kind, body)
    if not fresh and dest.exists():
        age = time.time() - dest.stat().st_mtime
        if age < CACHE_TTL_SEC:
            return json.loads(dest.read_text(encoding="utf-8")), True
    payload = http_json("POST", url, body)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload), encoding="utf-8")
    return payload, False


def card_name(entry: Any) -> str | None:
    if isinstance(entry, dict):
        card = entry.get("card")
        if isinstance(card, dict):
            return card.get("name")
        if isinstance(card, str):
            return card
        return entry.get("name")
    if isinstance(entry, str):
        return entry
    return None


def produces(item: dict[str, Any]) -> list[str]:
    out: list[str] = []
    for part in item.get("produces") or []:
        if isinstance(part, dict):
            feature = part.get("feature")
            name = feature.get("name") if isinstance(feature, dict) else part.get("name")
            if name:
                out.append(str(name))
        elif part:
            out.append(str(part))
    return out


def owned_names(body: dict[str, Any]) -> set[str]:
    names: set[str] = set()
    for row in (body.get("commanders") or []) + (body.get("main") or []):
        name = row.get("card") if isinstance(row, dict) else None
        if name:
            names.add(name.lower())
    return names


def slim_combo(item: dict[str, Any], owned: set[str]) -> dict[str, Any]:
    cards: list[str] = []
    for entry in item.get("uses") or []:
        name = card_name(entry)
        if name:
            cards.append(name)
    if not cards:
        for entry in item.get("cards") or []:
            name = card_name(entry)
            if name:
                cards.append(name)
    missing = [name for name in cards if name.lower() not in owned]
    prereq = item.get("notablePrerequisites") or item.get("easyPrerequisites") or None
    return {
        "id": item.get("id"),
        "cards": cards,
        "prerequisites": prereq or None,
        "produces": produces(item),
        "description": item.get("description"),
        "missing": missing,
        "bracketTag": item.get("bracketTag"),
    }


def results_block(payload: dict[str, Any]) -> dict[str, Any]:
    results = payload.get("results")
    if isinstance(results, dict):
        return results
    return payload


def cmd_combos(args: argparse.Namespace) -> int:
    text = sys.stdin.read() if args.file == "-" else Path(args.file).read_text(encoding="utf-8")
    body = deck_payload(text, args.commander)
    if not body["main"] and not body["commanders"]:
        print("No cards parsed", file=sys.stderr)
        return 1
    payload, cached = fetch_cached(
        "combos",
        f"{API}/find-my-combos",
        body,
        Path(args.cache_dir).expanduser(),
        args.fresh,
    )
    results = results_block(payload)
    owned = owned_names(body)
    included = [slim_combo(x, owned) for x in (results.get("included") or []) if isinstance(x, dict)]
    almost = [slim_combo(x, owned) for x in (results.get("almostIncluded") or []) if isinstance(x, dict)]
    json.dump(
        {
            "kind": "combos",
            "cached": cached,
            "commanders": body["commanders"],
            "included": included,
            "almostIncluded": almost,
        },
        sys.stdout,
        indent=2,
        ensure_ascii=False,
    )
    sys.stdout.write("\n")
    return 0


def cmd_bracket(args: argparse.Namespace) -> int:
    text = sys.stdin.read() if args.file == "-" else Path(args.file).read_text(encoding="utf-8")
    body = deck_payload(text, args.commander)
    if not body["main"] and not body["commanders"]:
        print("No cards parsed", file=sys.stderr)
        return 1
    payload, cached = fetch_cached(
        "bracket",
        f"{API}/estimate-bracket",
        body,
        Path(args.cache_dir).expanduser(),
        args.fresh,
    )
    cards: list[dict[str, Any]] = []
    for row in payload.get("cards") or []:
        if not isinstance(row, dict):
            continue
        card = row.get("card") if isinstance(row.get("card"), dict) else {}
        cards.append(
            {
                "name": card.get("name"),
                "game_changer": row.get("gameChanger"),
                "mass_land_denial": row.get("massLandDenial"),
                "extra_turn": row.get("extraTurn"),
                "banned": row.get("banned"),
            }
        )
    slim = {
        "kind": "bracket",
        "cached": cached,
        "commanders": body["commanders"],
        "bracket_tag": payload.get("bracketTag") or payload.get("bracket") or payload.get("estimate"),
        "justifications": payload.get("justifications")
        or payload.get("justification")
        or payload.get("reasons")
        or payload.get("explanations"),
        "cards": cards,
        "combo_count": len(payload.get("combos") or []),
    }
    json.dump(slim, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


def add_shared(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("file", help="Decklist path, or - for stdin")
    parser.add_argument(
        "--commander",
        action="append",
        default=[],
        help="Command-zone card (repeatable)",
    )
    parser.add_argument("--fresh", action="store_true")
    parser.add_argument("--cache-dir", default=str(DEFAULT_CACHE))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    combos = sub.add_parser("combos", help="POST /find-my-combos")
    add_shared(combos)
    combos.set_defaults(func=cmd_combos)

    bracket = sub.add_parser("bracket", help="POST /estimate-bracket")
    add_shared(bracket)
    bracket.set_defaults(func=cmd_bracket)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except RuntimeError as e:
        print(e, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
