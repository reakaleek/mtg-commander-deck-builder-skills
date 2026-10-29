#!/usr/bin/env python3
"""EDHREC helper: commander, card, average-deck pages, and merged candidates."""

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
DEFAULT_CANDIDATES_MAX = 40
KIND_PATH = {
    "commander": "commanders",
    "card": "cards",
    "average-deck": "average-decks",
}
# Cross-type lists; a card's category comes from its type list instead.
META_LISTS = {
    "New Cards",
    "Top Cards",
    "High Synergy Cards",
    "High Lift Cards",
    "Game Changers",
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


def cache_path(cache_dir: Path, kind: str, slug: str, suffix: str | None = None) -> Path:
    name = f"{slug}--{suffix}" if suffix else slug
    return cache_dir / kind / f"{name}.json"


def fetch_page(
    kind: str,
    slug: str,
    cache_dir: Path,
    fresh: bool,
    suffix: str | None = None,
) -> tuple[dict[str, Any], bool]:
    dest = cache_path(cache_dir, kind, slug, suffix)
    if not fresh and dest.exists():
        age = time.time() - dest.stat().st_mtime
        if age < CACHE_TTL_SEC:
            return json.loads(dest.read_text(encoding="utf-8")), True

    path = KIND_PATH[kind]
    if suffix:
        url = f"{BASE}/{path}/{urllib.parse.quote(slug)}/{urllib.parse.quote(suffix)}.json"
    else:
        url = f"{BASE}/{path}/{urllib.parse.quote(slug)}.json"
    payload = http_json(url)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload), encoding="utf-8")
    return payload, False


def theme_slugs(page: dict[str, Any], commander_slug: str) -> list[dict[str, Any]]:
    panels = page.get("panels") if isinstance(page.get("panels"), dict) else {}
    links = panels.get("taglinks") or []
    found: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in links:
        if not isinstance(item, dict):
            continue
        slug = item.get("slug")
        if not slug or slug in seen:
            continue
        seen.add(slug)
        found.append({
            "slug": slug,
            "name": item.get("value"),
            "count": item.get("count"),
        })
    return found


def json_dict(page: dict[str, Any]) -> dict[str, Any]:
    container = page.get("container")
    if isinstance(container, dict):
        inner = container.get("json_dict")
        if isinstance(inner, dict):
            return inner
    return {}


def name_key(name: Any) -> str:
    return str(name or "").split("//", 1)[0].strip().lower()


def read_deck_names(path: str) -> set[str]:
    """Card names from `qty name` lines; headers, comments, and blanks are skipped."""
    text = sys.stdin.read() if path == "-" else Path(path).expanduser().read_text(encoding="utf-8")
    names: set[str] = set()
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith(("#", "//")):
            continue
        m = re.match(r"^(\d+)\s*x?\s+(.+)$", line, re.IGNORECASE)
        if not m:
            continue
        # Drop Archidekt extras: "(set) 123 *F* [Category] ^Label^".
        name = re.split(r"\s+\(|\s+\[|\s+\^|\s+\*", m.group(2), maxsplit=1)[0]
        names.add(name_key(name))
    return names


def slim_cardview(view: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {"name": view.get("name")}
    for key in ("synergy", "lift", "trend_zscore", "num_decks", "potential_decks"):
        if key in view:
            value = view[key]
            out[key] = round(value, 3) if isinstance(value, float) else value
    decks, potential = view.get("num_decks"), view.get("potential_decks")
    if isinstance(decks, (int, float)) and isinstance(potential, (int, float)) and potential:
        out["inclusion"] = round(decks / potential, 3)
    return out


def slim_lists(
    page: dict[str, Any],
    max_cards: int,
    list_filters: list[str],
    exclude: set[str] | None = None,
) -> tuple[list[dict[str, Any]], int]:
    raw_lists = json_dict(page).get("cardlists") or []
    filters = [f.lower() for f in list_filters]
    exclude = exclude or set()
    excluded: set[str] = set()
    out: list[dict[str, Any]] = []
    for cl in raw_lists:
        if not isinstance(cl, dict):
            continue
        header = cl.get("header") or cl.get("tag") or ""
        if filters and not any(f in str(header).lower() for f in filters):
            continue
        cards: list[dict[str, Any]] = []
        for v in cl.get("cardviews") or []:
            if not isinstance(v, dict):
                continue
            if name_key(v.get("name")) in exclude:
                excluded.add(name_key(v.get("name")))
                continue
            if len(cards) < max_cards:
                cards.append(slim_cardview(v))
        out.append({"header": header, "cards": cards})
    return out, len(excluded)


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
    suffix = None
    if kind == "commander":
        if getattr(args, "budget", False) and getattr(args, "theme", None):
            print("Use only one of --theme or --budget", file=sys.stderr)
            return 1
        if getattr(args, "budget", False):
            suffix = "budget"
        elif getattr(args, "theme", None):
            suffix = slugify(args.theme)
            if not suffix:
                print("Empty theme slug", file=sys.stderr)
                return 1
    page, cached = fetch_page(kind, slug, Path(args.cache_dir).expanduser(), args.fresh, suffix)
    card = json_dict(page).get("card") or {}
    exclude = read_deck_names(args.exclude) if args.exclude else set()
    lists, excluded = slim_lists(page, args.max, args.list, exclude)
    payload = {
        "kind": kind,
        "name": card.get("name") or page.get("header") or args.name,
        "slug": slug,
        "theme": suffix,
        "cached": cached,
        "num_decks": card.get("num_decks"),
        "rank": card.get("rank"),
        "salt": card.get("salt"),
    }
    if kind == "commander":
        payload["similar"] = similar_commanders(page)
    if args.exclude:
        payload["excluded"] = excluded
    payload["lists"] = lists
    json.dump(payload, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


def similar_commanders(page: dict[str, Any]) -> list[str]:
    out: list[str] = []
    for item in page.get("similar") or []:
        name = item.get("name") if isinstance(item, dict) else item
        if isinstance(name, str):
            out.append(name)
    return out


def cmd_candidates(args: argparse.Namespace) -> int:
    slug = slugify(args.name)
    if not slug:
        print("Empty card name", file=sys.stderr)
        return 1
    suffixes: list[str | None] = [None]
    for theme in args.theme:
        suffix = slugify(theme)
        if not suffix:
            print("Empty theme slug", file=sys.stderr)
            return 1
        suffixes.append(suffix)
    if args.budget:
        suffixes.append("budget")

    cache_dir = Path(args.cache_dir).expanduser()
    exclude = read_deck_names(args.exclude) if args.exclude else set()
    excluded: set[str] = set()
    merged: dict[str, dict[str, Any]] = {}
    pages: list[dict[str, Any]] = []
    name = args.name
    similar: list[str] = []
    for suffix in suffixes:
        page, cached = fetch_page("commander", slug, cache_dir, args.fresh, suffix)
        page_name = suffix or "base"
        pages.append({"page": page_name, "cached": cached})
        if suffix is None:
            name = (json_dict(page).get("card") or {}).get("name") or name
            similar = similar_commanders(page)
        for cl in json_dict(page).get("cardlists") or []:
            if not isinstance(cl, dict):
                continue
            header = str(cl.get("header") or cl.get("tag") or "")
            if "land" in header.lower() and not args.lands:
                continue
            for view in cl.get("cardviews") or []:
                if not isinstance(view, dict) or not view.get("name"):
                    continue
                key = name_key(view["name"])
                if key in exclude:
                    excluded.add(key)
                    continue
                slim = slim_cardview(view)
                entry = merged.setdefault(key, {"name": view["name"], "inclusion": {}, "sources": []})
                if header not in META_LISTS and "category" not in entry:
                    entry["category"] = header
                for stat in ("synergy", "lift", "trend_zscore"):
                    if stat in slim and (stat not in entry or slim[stat] > entry[stat]):
                        entry[stat] = slim[stat]
                if "inclusion" in slim:
                    entry["inclusion"][page_name] = slim["inclusion"]
                entry["sources"].append(f"{page_name}: {header}")

    sort_key = {"synergy": "synergy", "lift": "lift", "trend": "trend_zscore"}.get(args.sort)

    def rank(entry: dict[str, Any]) -> tuple[float, int]:
        if sort_key:
            value = entry.get(sort_key)
        else:
            value = max(entry["inclusion"].values(), default=None)
        pages_hit = len({s.split(":", 1)[0] for s in entry["sources"]})
        return (value if isinstance(value, (int, float)) else float("-inf"), pages_hit)

    cards = list(merged.values())
    if args.min_synergy is not None:
        cards = [c for c in cards if isinstance(c.get("synergy"), (int, float)) and c["synergy"] >= args.min_synergy]
    cards.sort(key=rank, reverse=True)
    payload: dict[str, Any] = {
        "kind": "candidates",
        "name": name,
        "slug": slug,
        "pages": pages,
        "sort": args.sort,
        "similar": similar,
        "total": len(cards),
        "returned": min(len(cards), args.max),
    }
    if args.exclude:
        payload["excluded"] = len(excluded)
    payload["cards"] = cards[: args.max]
    json.dump(payload, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


def cmd_themes(args: argparse.Namespace) -> int:
    slug = slugify(args.name)
    if not slug:
        print("Empty card name", file=sys.stderr)
        return 1
    page, cached = fetch_page(
        "commander",
        slug,
        Path(args.cache_dir).expanduser(),
        args.fresh,
    )
    card = json_dict(page).get("card") or {}
    payload = {
        "kind": "themes",
        "name": card.get("name") or page.get("header") or args.name,
        "slug": slug,
        "cached": cached,
        "themes": theme_slugs(page, slug),
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


def add_exclude_flag(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--exclude",
        default=None,
        help="Decklist file (or -) whose cards are dropped from the output",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    commander = sub.add_parser("commander", help="GET /pages/commanders/{slug}.json")
    add_shared_flags(commander)
    commander.add_argument("--theme", default=None, help="Theme subpage slug")
    commander.add_argument("--budget", action="store_true", help="Budget subpage")
    add_exclude_flag(commander)
    commander.set_defaults(func=lambda a: cmd_lists(a, "commander"))

    candidates = sub.add_parser(
        "candidates",
        help="Merge the commander page and theme subpages into one ranked list",
    )
    candidates.add_argument("name", help="Exact Oracle commander name")
    candidates.add_argument(
        "--theme",
        action="append",
        default=[],
        help="Theme subpage slug to merge in (repeatable)",
    )
    candidates.add_argument("--budget", action="store_true", help="Also merge the budget subpage")
    candidates.add_argument(
        "--sort",
        choices=("inclusion", "synergy", "lift", "trend"),
        default="synergy",
        help="inclusion uses the best page; ties go to cards on more pages",
    )
    candidates.add_argument("--min-synergy", type=float, default=None)
    candidates.add_argument("--lands", action="store_true", help="Keep land lists")
    candidates.add_argument("--max", type=int, default=DEFAULT_CANDIDATES_MAX, dest="max")
    add_exclude_flag(candidates)
    candidates.add_argument("--fresh", action="store_true", help="Bypass the 24h cache")
    candidates.add_argument("--cache-dir", default=str(DEFAULT_CACHE))
    candidates.set_defaults(func=cmd_candidates)

    themes = sub.add_parser("themes", help="List theme slugs advertised on a commander page")
    add_shared_flags(themes)
    themes.set_defaults(func=cmd_themes)

    card = sub.add_parser("card", help="GET /pages/cards/{slug}.json")
    add_shared_flags(card)
    add_exclude_flag(card)
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
