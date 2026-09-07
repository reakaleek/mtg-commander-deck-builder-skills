#!/usr/bin/env python3
"""Archidekt helper: derive the API URL from a deck URL and fetch deck JSON."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

API_DECK = "https://archidekt.com/api/decks/{deck_id}/"
URL_RE = re.compile(r"archidekt\.com/decks/(\d+)", re.IGNORECASE)
USER_AGENT = "mtg-commander-deck-builder-skills/1.0 (archidekt helper)"
MIN_INTERVAL_SEC = 0.55

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
ZONE_SIDE = {"sideboard", "sb"}
ZONE_MAYBE = {"maybeboard", "maybe", "considering"}
ZONE_OUT = {"not included", "not in deck", "out of deck", "unused"}

_last_call = 0.0


def deck_id(url_or_id: str) -> str:
    raw = url_or_id.strip()
    if raw.isdigit():
        return raw
    m = URL_RE.search(raw)
    if not m:
        raise RuntimeError(
            f"Could not find a deck id in {url_or_id!r}. "
            "Pass an archidekt.com/decks/<id> URL or a bare numeric id."
        )
    return m.group(1)


def api_url(url_or_id: str) -> str:
    return API_DECK.format(deck_id=deck_id(url_or_id))


def _wait() -> None:
    global _last_call
    elapsed = time.monotonic() - _last_call
    if _last_call and elapsed < MIN_INTERVAL_SEC:
        time.sleep(MIN_INTERVAL_SEC - elapsed)


def http_json(url: str, retries: int = 2) -> dict[str, Any]:
    global _last_call
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        _wait()
        req = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            _last_call = time.monotonic()
            return payload
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            _last_call = time.monotonic()
            if e.code == 429 and attempt < retries:
                time.sleep(30)
                last_error = RuntimeError(f"Archidekt HTTP 429: {body}")
                continue
            if e.code == 404:
                raise RuntimeError(f"Archidekt HTTP 404: no deck at {url}. Check the id or privacy setting.") from e
            raise RuntimeError(f"Archidekt HTTP {e.code}: {body}") from e
        except urllib.error.URLError as e:
            last_error = e
            if attempt < retries:
                time.sleep(2)
                continue
            raise RuntimeError(f"Archidekt request failed: {e}") from e
    raise RuntimeError(f"Archidekt request failed: {last_error}")


def fetch_deck(url_or_id: str) -> dict[str, Any]:
    url = api_url(url_or_id)
    try:
        return http_json(url)
    except RuntimeError as e:
        raise RuntimeError(f"Archidekt request failed for {url}: {e}") from e


def classify_zone(categories: list[str]) -> str:
    labels = [c.lower() for c in categories]
    for label in labels:
        if label in ZONE_OUT:
            return "out"
        if label in ZONE_MAYBE:
            return "maybeboard"
        if label in ZONE_SIDE:
            return "sideboard"
        if label in ZONE_COMMAND:
            return "command"
    return "main"


def deck_card(entry: dict[str, Any]) -> dict[str, Any] | None:
    card = entry.get("card") or {}
    oracle = card.get("oracleCard") or {}
    name = oracle.get("name") or card.get("displayName")
    if not name:
        return None

    edition = card.get("edition") or {}
    categories = [c for c in entry.get("categories") or [] if c]
    return {
        "qty": entry.get("quantity") or 1,
        "name": name,
        "set": edition.get("editioncode"),
        "collector_number": card.get("collectorNumber"),
        "foil": "foil" in (entry.get("modifier") or "").lower(),
        "categories": categories,
        "zone": classify_zone(categories),
    }


def parse_deck(data: dict[str, Any]) -> list[dict[str, Any]]:
    cards = []
    for entry in data.get("cards") or []:
        parsed = deck_card(entry)
        if parsed is not None:
            cards.append(parsed)
    return cards


def import_block(cards: list[dict[str, Any]]) -> str:
    lines = [f"{int(c['qty'])} {c['name']}" for c in cards]
    return "\n".join(lines) + ("\n" if lines else "")


def cmd_url(args: argparse.Namespace) -> int:
    json.dump({"api_url": api_url(args.url)}, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


def cmd_fetch(args: argparse.Namespace) -> int:
    resolved_url = api_url(args.url)
    data = fetch_deck(args.url)
    cards = parse_deck(data)
    in_deck = [c for c in cards if c["zone"] not in {"sideboard", "maybeboard", "out"}]
    command = [c for c in in_deck if c["zone"] == "command"]
    excluded = [c for c in cards if c["zone"] in {"sideboard", "maybeboard", "out"}]
    block = import_block(in_deck)

    written_to = None
    if args.out:
        if not in_deck:
            print("No in-deck cards to write", file=sys.stderr)
            return 1
        dest = Path(args.out)
        dest.parent.mkdir(parents=True, exist_ok=True)
        tmp = dest.with_suffix(dest.suffix + ".tmp")
        tmp.write_text(block, encoding="utf-8")
        tmp.replace(dest)
        written_to = str(dest)

    json.dump(
        {
            "api_url": resolved_url,
            "deck_name": data.get("name"),
            "cards": cards,
            "in_deck": in_deck,
            "command": command,
            "excluded": excluded,
            "import_block": block,
            "in_deck_count": sum(int(c["qty"]) for c in in_deck),
            "written_to": written_to,
        },
        sys.stdout,
        indent=2,
        ensure_ascii=False,
    )
    sys.stdout.write("\n")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    url = sub.add_parser("url", help="Derive the API URL from a deck URL or id")
    url.add_argument("url", help="Archidekt deck URL, e.g. https://archidekt.com/decks/<id>/<slug>, or a bare id")
    url.set_defaults(func=cmd_url)

    fetch = sub.add_parser("fetch", help="GET the API URL derived from a deck URL or id")
    fetch.add_argument("url", help="Archidekt deck URL, e.g. https://archidekt.com/decks/<id>/<slug>, or a bare id")
    fetch.add_argument("--out", default=None, help="Optional path to write the clean import list")
    fetch.set_defaults(func=cmd_fetch)

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
