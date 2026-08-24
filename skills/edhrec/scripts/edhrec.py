#!/usr/bin/env python3
"""EDHREC helper: commander, card, and average-deck pages."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

BASE = "https://json.edhrec.com/pages"
USER_AGENT = "mtg-commander-deck-builder-skills/1.0 (edhrec helper)"
MIN_INTERVAL_SEC = 0.55
CACHE_TTL_SEC = 24 * 60 * 60
DEFAULT_CACHE = Path.home() / ".cache" / "edhrec"
DEFAULT_MAX = 10
KIND_PATH = {
    "commander": "commanders",
    "card": "cards",
    "average-deck": "average-decks",
}
TYPE_COUNT_KEYS = (
    "creature",
    "instant",
    "sorcery",
    "artifact",
    "enchantment",
    "land",
    "planeswalker",
    "battle",
)

_last_call = 0.0


def slugify(name: str) -> str:
    if "//" in name:
        name = name.split("//", 1)[0]
    name = name.lower().strip()
    name = name.replace("'", "").replace("’", "").replace(",", "").replace(".", "")
    name = re.sub(r"[^a-z0-9\s-]", "", name)
    name = re.sub(r"[\s_]+", "-", name)
    return re.sub(r"-{2,}", "-", name).strip("-")


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
            payload = e.read().decode("utf-8", errors="replace")
            _last_call = time.monotonic()
            if e.code == 429 and attempt < retries:
                time.sleep(30)
                last_error = RuntimeError(f"EDHREC HTTP 429: {payload}")
                continue
            if e.code in (403, 404):
                raise RuntimeError(
                    f"EDHREC HTTP {e.code}: no page at {url}. "
                    "Use the exact Oracle name (resolve with Scryfall if needed)."
                ) from e
            raise RuntimeError(f"EDHREC HTTP {e.code}: {payload}") from e
        except urllib.error.URLError as e:
            last_error = e
            if attempt < retries:
                time.sleep(2)
                continue
            raise RuntimeError(f"EDHREC request failed: {e}") from e
    raise RuntimeError(f"EDHREC request failed: {last_error}")


def cache_path(cache_dir: Path, kind: str, slug: str) -> Path:
    return cache_dir / kind / f"{slug}.json"


def fetch_page(
    kind: str,
    slug: str,
    cache_dir: Path,
    fresh: bool,
) -> tuple[dict[str, Any], bool]:
    dest = cache_path(cache_dir, kind, slug)
    if not fresh and dest.exists():
        age = time.time() - dest.stat().st_mtime
        if age < CACHE_TTL_SEC:
            return json.loads(dest.read_text(encoding="utf-8")), True

    path = KIND_PATH[kind]
    url = f"{BASE}/{path}/{urllib.parse.quote(slug)}.json"
    payload = http_json(url)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload), encoding="utf-8")
    return payload, False


def json_dict(page: dict[str, Any]) -> dict[str, Any]:
    container = page.get("container")
    if isinstance(container, dict):
        inner = container.get("json_dict")
        if isinstance(inner, dict):
            return inner
    return {}


def slim_cardview(view: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {"name": view.get("name")}
    for key in ("synergy", "num_decks", "potential_decks"):
        if key in view:
            out[key] = view[key]
    return out


def slim_lists(
    page: dict[str, Any],
    max_cards: int,
    list_filters: list[str],
) -> list[dict[str, Any]]:
    raw_lists = json_dict(page).get("cardlists") or []
    filters = [f.lower() for f in list_filters]
    out: list[dict[str, Any]] = []
    for cl in raw_lists:
        if not isinstance(cl, dict):
            continue
        header = cl.get("header") or cl.get("tag") or ""
        if filters and not any(f in str(header).lower() for f in filters):
            continue
        views = cl.get("cardviews") or []
        cards = [slim_cardview(v) for v in views[:max_cards] if isinstance(v, dict)]
        out.append({"header": header, "cards": cards})
    return out


def flatten_deck(deck: Any) -> dict[str, int]:
    counts: dict[str, int] = {}
    if not isinstance(deck, dict):
        return counts
    cards = deck.get("cards")
    if not isinstance(cards, dict):
        return counts
    for rows in cards.values():
        if not isinstance(rows, list):
            continue
        for row in rows:
            if not isinstance(row, (list, tuple)) or not row:
                continue
            name = row[0]
            qty = row[1] if len(row) > 1 else 1
            try:
                counts[str(name)] = counts.get(str(name), 0) + int(qty)
            except (TypeError, ValueError):
                counts[str(name)] = counts.get(str(name), 0) + 1
    return counts


def type_counts(page: dict[str, Any]) -> dict[str, int]:
    out: dict[str, int] = {}
    for key in TYPE_COUNT_KEYS:
        val = page.get(key)
        if isinstance(val, int):
            out[key] = val
    return out


def cmd_lists(args: argparse.Namespace, kind: str) -> int:
    slug = slugify(args.name)
    if not slug:
        print("Empty card name", file=sys.stderr)
        return 1
    page, cached = fetch_page(kind, slug, Path(args.cache_dir).expanduser(), args.fresh)
    card = json_dict(page).get("card") or {}
    payload = {
        "kind": kind,
        "name": card.get("name") or page.get("header") or args.name,
        "slug": slug,
        "cached": cached,
        "num_decks": card.get("num_decks"),
        "rank": card.get("rank"),
        "salt": card.get("salt"),
        "lists": slim_lists(page, args.max, args.list),
    }
    json.dump(payload, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


def cmd_average_deck(args: argparse.Namespace) -> int:
    slug = slugify(args.name)
    if not slug:
        print("Empty card name", file=sys.stderr)
        return 1
    page, cached = fetch_page(
        "average-deck",
        slug,
        Path(args.cache_dir).expanduser(),
        args.fresh,
    )
    card = json_dict(page).get("card") or {}
    deck = flatten_deck(page.get("deck"))
    commanders = []
    raw_deck = page.get("deck")
    if isinstance(raw_deck, dict):
        commanders = raw_deck.get("commander") or []
    payload = {
        "kind": "average-deck",
        "name": card.get("name") or args.name,
        "slug": slug,
        "cached": cached,
        "commanders": commanders,
        "num_decks": card.get("num_decks"),
        "rank": card.get("rank"),
        "type_counts": type_counts(page),
        "deck_size": sum(deck.values()),
        "deck": deck,
    }
    json.dump(payload, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


def add_shared_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("name", help="Exact Oracle card or commander name")
    parser.add_argument("--max", type=int, default=DEFAULT_MAX, dest="max")
    parser.add_argument(
        "--list",
        action="append",
        default=[],
        help="Keep lists whose header contains this text (repeatable)",
    )
    parser.add_argument("--fresh", action="store_true", help="Bypass the 24h cache")
    parser.add_argument("--cache-dir", default=str(DEFAULT_CACHE))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    commander = sub.add_parser("commander", help="GET /pages/commanders/{slug}.json")
    add_shared_flags(commander)
    commander.set_defaults(func=lambda a: cmd_lists(a, "commander"))

    card = sub.add_parser("card", help="GET /pages/cards/{slug}.json")
    add_shared_flags(card)
    card.set_defaults(func=lambda a: cmd_lists(a, "card"))

    average = sub.add_parser("average-deck", help="GET /pages/average-decks/{slug}.json")
    add_shared_flags(average)
    average.set_defaults(func=cmd_average_deck)

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
