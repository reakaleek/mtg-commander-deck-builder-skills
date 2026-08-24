#!/usr/bin/env python3
"""Scryfall helper: search, named, collection, prices, Archidekt lists, bulk."""

from __future__ import annotations

import argparse
import gzip
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

API = "https://api.scryfall.com"
USER_AGENT = "mtg-commander-deck-builder-skills/1.0 (scryfall helper)"
COLLECTION_BATCH = 75
MIN_INTERVAL_SEC = 0.55
SLOW_ENDPOINTS = ("/cards/search", "/cards/named", "/cards/random", "/cards/collection")
DEFAULT_CACHE = Path.home() / ".cache" / "scryfall"
PRICE_TTL_SEC = 24 * 60 * 60
DEFAULT_FIELDS = (
    "name,mana_cost,cmc,type_line,oracle_text,color_identity,"
    "colors,legalities,game_changer,scryfall_uri"
)
DEFAULT_SEARCH_MAX = 40
BULK_TYPES = ("oracle_cards", "default_cards", "rulings")
PRICE_CURRENCIES = ("usd", "eur", "tix")
PRICE_BATCH = 12
COMMANDER_TOTAL = 100

LINE_QTY_RE = re.compile(r"^(\d+)\s*x?\s+(.*)$", re.IGNORECASE)
SKIP_PREFIXES = ("//", "#")
SET_CODE_RE = re.compile(r"^[A-Za-z0-9]{2,6}$")
HEADER_RE = re.compile(r"^[A-Za-z][^:]*?(?:\s+\(\d+\))?$")

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

_last_slow_call = 0.0


def _is_slow(url: str) -> bool:
    return any(path in url for path in SLOW_ENDPOINTS)


def _wait_slow(url: str) -> None:
    global _last_slow_call
    if not _is_slow(url):
        return
    elapsed = time.monotonic() - _last_slow_call
    if _last_slow_call and elapsed < MIN_INTERVAL_SEC:
        time.sleep(MIN_INTERVAL_SEC - elapsed)


def http_json(
    method: str,
    url: str,
    body: dict[str, Any] | None = None,
    retries: int = 2,
) -> dict[str, Any]:
    global _last_slow_call
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
        _wait_slow(url)
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            if _is_slow(url):
                _last_slow_call = time.monotonic()
            return payload
        except urllib.error.HTTPError as e:
            payload = e.read().decode("utf-8", errors="replace")
            if _is_slow(url):
                _last_slow_call = time.monotonic()
            if e.code == 429 and attempt < retries:
                time.sleep(30)
                last_error = RuntimeError(f"Scryfall HTTP 429: {payload}")
                continue
            raise RuntimeError(f"Scryfall HTTP {e.code}: {payload}") from e
        except urllib.error.URLError as e:
            last_error = e
            if attempt < retries:
                time.sleep(2)
                continue
            raise RuntimeError(f"Scryfall request failed: {e}") from e
    raise RuntimeError(f"Scryfall request failed: {last_error}")


def download_file(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    req = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT},
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=300) as resp, tmp.open("wb") as out:
        while True:
            chunk = resp.read(1024 * 256)
            if not chunk:
                break
            out.write(chunk)
    tmp.replace(dest)


def read_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def classify_zone(categories: list[str], section: str | None = None) -> str:
    labels = [c.lower() for c in categories]
    if section:
        labels.append(section.lower())
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


def section_from_header(header: str) -> str | None:
    name = re.sub(r"\s+\(\d+\)\s*$", "", header).strip().lower()
    if name in ZONE_COMMAND or name in ZONE_SIDE or name in ZONE_MAYBE or name in ZONE_OUT:
        return name
    if name in {"deck", "main", "mainboard", "main deck"}:
        return "main"
    return None


def parse_card_line(line: str) -> dict[str, Any] | None:
    raw = line.strip()
    if not raw or raw.startswith(SKIP_PREFIXES):
        return None
    if raw.lower() in {
        "sideboard",
        "maybeboard",
        "commander",
        "commanders",
        "deck",
        "mainboard",
    }:
        return {"header": raw}

    m = LINE_QTY_RE.match(raw)
    if not m:
        if HEADER_RE.match(raw) and not raw[0].isdigit():
            return {"header": raw}
        return None

    qty = int(m.group(1))
    rest = m.group(2).strip()
    label = None
    categories: list[str] = []
    foil = False
    set_code = None
    collector = None

    lab = re.search(r"\s+\^([^^]+)\^\s*$", rest)
    if lab:
        label = lab.group(1).strip()
        rest = rest[: lab.start()].rstrip()

    while True:
        cat = re.search(r"\s+\[([^\]]+)\]\s*$", rest)
        if not cat:
            break
        categories.extend(p.strip() for p in cat.group(1).split(",") if p.strip())
        rest = rest[: cat.start()].rstrip()

    tick = re.search(r"\s+`([^`]+)`\s*$", rest)
    if tick:
        categories.append(tick.group(1).strip())
        rest = rest[: tick.start()].rstrip()

    foil_m = re.search(r"\s+\*[Ff]\*\s*$", rest)
    if foil_m:
        foil = True
        rest = rest[: foil_m.start()].rstrip()

    set_cn = re.search(r"\s+\(([^)]+)\)\s+(\S+)\s*$", rest)
    if set_cn and SET_CODE_RE.fullmatch(set_cn.group(1)):
        set_code = set_cn.group(1).lower()
        collector = set_cn.group(2)
        rest = rest[: set_cn.start()].rstrip()
    else:
        set_only = re.search(r"\s+\(([^)]+)\)\s*$", rest)
        if set_only and SET_CODE_RE.fullmatch(set_only.group(1)):
            set_code = set_only.group(1).lower()
            rest = rest[: set_only.start()].rstrip()

    name = rest.strip()
    if not name:
        return None
    return {
        "qty": qty,
        "name": name,
        "set": set_code,
        "collector_number": collector,
        "foil": foil,
        "categories": categories,
        "label": label,
    }


def parse_deck_text(text: str) -> dict[str, Any]:
    cards: list[dict[str, Any]] = []
    headers: list[str] = []
    ambiguous: list[str] = []
    section: str | None = None

    for raw in text.splitlines():
        parsed = parse_card_line(raw)
        if parsed is None:
            continue
        if "header" in parsed:
            headers.append(parsed["header"])
            section = section_from_header(parsed["header"])
            continue

        cats = list(parsed["categories"])
        zone = classify_zone(cats, section)
        known = ZONE_COMMAND | ZONE_SIDE | ZONE_MAYBE | ZONE_OUT
        extra = [c for c in cats if c.lower() not in known]
        if extra and zone == "main" and section is None:
            for c in extra:
                if c not in ambiguous:
                    ambiguous.append(c)

        parsed["zone"] = zone
        cards.append(parsed)

    return {
        "cards": cards,
        "headers": headers,
        "ambiguous_categories": ambiguous,
    }


def deck_cards(parsed: dict[str, Any], include_out: bool = False) -> list[dict[str, Any]]:
    out = []
    for card in parsed.get("cards") or []:
        zone = card.get("zone")
        if zone in {"sideboard", "maybeboard", "out"} and not include_out:
            continue
        out.append(card)
    return out


def import_block(cards: list[dict[str, Any]]) -> str:
    lines = []
    for card in cards:
        qty = int(card.get("qty") or 1)
        name = card.get("name") or ""
        if name:
            lines.append(f"{qty} {name}")
    return "\n".join(lines) + ("\n" if lines else "")


def parse_names(text: str) -> list[str]:
    parsed = parse_deck_text(text)
    names: list[str] = []
    seen: set[str] = set()
    for card in deck_cards(parsed):
        name = card["name"]
        if name not in seen:
            seen.add(name)
            names.append(name)
    return names


def oracle_text(card: dict[str, Any]) -> str | None:
    bits: list[str] = []
    if card.get("oracle_text"):
        bits.append(card["oracle_text"])
    for face in card.get("card_faces") or []:
        if face.get("oracle_text"):
            label = face.get("name") or "face"
            bits.append(f"[{label}] {face['oracle_text']}")
    return "\n".join(bits) if bits else None


def project_fields(card: dict[str, Any], fields: list[str]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for field in fields:
        if field == "oracle_text":
            out[field] = oracle_text(card)
            continue
        if field == "mana_cost" and not card.get("mana_cost"):
            faces = card.get("card_faces") or []
            out[field] = faces[0].get("mana_cost") if faces else None
            continue
        out[field] = card.get(field)
    return out


def parse_fields(raw: str | None) -> list[str] | None:
    if raw is None:
        return None
    fields = [part.strip() for part in raw.split(",") if part.strip()]
    return fields or None


def fetch_collection(identifiers: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    cards: list[dict[str, Any]] = []
    missing: list[dict[str, Any]] = []
    for i in range(0, len(identifiers), COLLECTION_BATCH):
        batch = identifiers[i : i + COLLECTION_BATCH]
        result = http_json(
            "POST",
            f"{API}/cards/collection",
            {"identifiers": batch},
        )
        cards.extend(result.get("data") or [])
        missing.extend(result.get("not_found") or [])
    return cards, missing


def resolve_fuzzy(name: str) -> dict[str, Any] | None:
    q = urllib.parse.urlencode({"fuzzy": name})
    try:
        return http_json("GET", f"{API}/cards/named?{q}")
    except RuntimeError:
        return None


def cmd_search(args: argparse.Namespace) -> int:
    params = {"q": args.query, "unique": args.unique}
    if args.order:
        params["order"] = args.order
    url = f"{API}/cards/search?{urllib.parse.urlencode(params)}"
    fields = parse_fields(args.fields)
    cards: list[dict[str, Any]] = []
    total: int | None = None

    while url and len(cards) < args.max:
        result = http_json("GET", url)
        total = result.get("total_cards", total)
        batch = result.get("data") or []
        for card in batch:
            cards.append(project_fields(card, fields) if fields else card)
            if len(cards) >= args.max:
                break
        url = result.get("next_page") if result.get("has_more") and len(cards) < args.max else None

    json.dump(
        {
            "query": args.query,
            "unique": args.unique,
            "total_cards": total,
            "returned": len(cards),
            "cards": cards,
        },
        sys.stdout,
        indent=2,
        ensure_ascii=False,
    )
    sys.stdout.write("\n")
    return 0


def cmd_named(args: argparse.Namespace) -> int:
    params: dict[str, str] = {}
    if args.fuzzy:
        params["fuzzy"] = args.name
    else:
        params["exact"] = args.name
    if args.set:
        params["set"] = args.set
    url = f"{API}/cards/named?{urllib.parse.urlencode(params)}"
    card = http_json("GET", url)
    fields = parse_fields(args.fields)
    json.dump(project_fields(card, fields) if fields else card, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


def cmd_collection(args: argparse.Namespace) -> int:
    text = read_text(args.file)
    names = parse_names(text)
    if not names:
        print("No card names parsed", file=sys.stderr)
        return 1

    cards, not_found = fetch_collection([{"name": n} for n in names])
    aliases: dict[str, dict[str, Any]] = {}
    still_missing = []
    for item in not_found:
        n = item.get("name") if isinstance(item, dict) else None
        if n:
            still_missing.append(n)

    if still_missing and args.fuzzy_missing:
        unresolved = []
        for n in still_missing:
            card = resolve_fuzzy(n)
            if card:
                aliases[n] = card
            else:
                unresolved.append(n)
        still_missing = unresolved

    by_name = {c["name"]: c for c in cards if c.get("name")}
    fields = parse_fields(args.fields)
    ordered: list[dict[str, Any]] = []
    for n in names:
        card = by_name.get(n) or aliases.get(n)
        if card:
            ordered.append(project_fields(card, fields) if fields else card)

    json.dump(
        {
            "unique_names_requested": len(names),
            "cards_fetched": len(ordered),
            "not_found": still_missing,
            "cards": ordered,
        },
        sys.stdout,
        indent=2,
        ensure_ascii=False,
    )
    sys.stdout.write("\n")
    if still_missing:
        print(f"Warning: {len(still_missing)} name(s) not found", file=sys.stderr)
        return 2
    return 0


def price_value(card: dict[str, Any], currency: str) -> float | None:
    prices = card.get("prices") or {}
    raw = prices.get(currency)
    if raw is None:
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def price_cache_path(cache_dir: Path, currency: str, key: str) -> Path:
    safe = re.sub(r"[^a-z0-9._-]+", "-", key.lower()).strip("-")
    return cache_dir / "prices" / currency / f"{safe}.json"


def load_price_cache(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    age = time.time() - path.stat().st_mtime
    if age > PRICE_TTL_SEC:
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def store_price_cache(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def fetch_printing(name: str, set_code: str | None, collector: str | None) -> dict[str, Any] | None:
    ident: dict[str, Any]
    if set_code and collector:
        ident = {"set": set_code, "collector_number": str(collector)}
    elif name and set_code:
        ident = {"name": name, "set": set_code}
    else:
        ident = {"name": name}
    cards, _missing = fetch_collection([ident])
    return cards[0] if cards else None


def search_cheapest(names: list[str], currency: str) -> dict[str, dict[str, Any]]:
    found: dict[str, dict[str, Any]] = {}
    if not names:
        return found
    quoted = " or ".join(f'!"{n}"' for n in names)
    q = f"({quoted}) cheapest:{currency}"
    url = f"{API}/cards/search?{urllib.parse.urlencode({'q': q, 'unique': 'cards'})}"
    try:
        result = http_json("GET", url)
    except RuntimeError:
        return found
    for card in result.get("data") or []:
        name = card.get("name")
        if name:
            found[name] = card
    return found


def cmd_prices(args: argparse.Namespace) -> int:
    currency = args.currency.lower()
    if currency not in PRICE_CURRENCIES:
        print(f"Unsupported currency {args.currency!r}", file=sys.stderr)
        return 1
    parsed = parse_deck_text(read_text(args.file))
    cards = deck_cards(parsed)
    if not cards:
        print("No in-deck cards parsed", file=sys.stderr)
        return 1

    cache_dir = Path(args.cache_dir).expanduser()
    priced: list[dict[str, Any]] = []
    missing: list[str] = []
    need_search: list[str] = []
    cached_hits = 0

    for card in cards:
        name = card["name"]
        key = f"{name}|{card.get('set') or ''}|{card.get('collector_number') or ''}|{int(card.get('foil') or 0)}"
        cache_file = price_cache_path(cache_dir, currency, key)
        cached = None if args.fresh else load_price_cache(cache_file)
        if cached:
            cached_hits += 1
            unit = cached.get("unit")
            qty = int(card["qty"])
            priced.append(
                {
                    "name": name,
                    "qty": qty,
                    "unit": unit,
                    "line": None if unit is None else round(unit * qty, 2),
                    "printing": cached.get("printing"),
                    "cheapest": cached.get("cheapest"),
                    "cached": True,
                    "missing": unit is None,
                }
            )
            if unit is None:
                missing.append(name)
            continue

        if card.get("set") or card.get("collector_number"):
            printing = fetch_printing(name, card.get("set"), card.get("collector_number"))
            unit = price_value(printing, currency) if printing else None
            payload = {
                "unit": unit,
                "printing": None
                if not printing
                else f"{printing.get('set')}#{printing.get('collector_number')}",
                "cheapest": False,
            }
            store_price_cache(cache_file, payload)
            qty = int(card["qty"])
            priced.append(
                {
                    "name": name,
                    "qty": qty,
                    "unit": unit,
                    "line": None if unit is None else round(unit * qty, 2),
                    "printing": payload["printing"],
                    "cheapest": False,
                    "cached": False,
                    "missing": unit is None,
                }
            )
            if unit is None:
                missing.append(name)
        else:
            need_search.append(name)

    unique_search = []
    seen = set()
    for n in need_search:
        if n not in seen:
            seen.add(n)
            unique_search.append(n)

    cheapest_map: dict[str, dict[str, Any]] = {}
    for i in range(0, len(unique_search), PRICE_BATCH):
        batch = unique_search[i : i + PRICE_BATCH]
        cheapest_map.update(search_cheapest(batch, currency))

    qty_by_name: dict[str, int] = {}
    for card in cards:
        if card.get("set") or card.get("collector_number"):
            continue
        qty_by_name[card["name"]] = qty_by_name.get(card["name"], 0) + int(card["qty"])

    already = {p["name"] for p in priced}
    for name, qty in qty_by_name.items():
        if name in already:
            continue
        card = cheapest_map.get(name)
        unit = price_value(card, currency) if card else None
        printing = None
        if card:
            printing = f"{card.get('set')}#{card.get('collector_number')}"
        payload = {"unit": unit, "printing": printing, "cheapest": True if card else None}
        store_price_cache(price_cache_path(cache_dir, currency, f"{name}|||0"), payload)
        priced.append(
            {
                "name": name,
                "qty": qty,
                "unit": unit,
                "line": None if unit is None else round(unit * qty, 2),
                "printing": printing,
                "cheapest": bool(card),
                "cached": False,
                "missing": unit is None,
            }
        )
        if unit is None:
            missing.append(name)

    known = [p for p in priced if p["line"] is not None]
    subtotal = round(sum(p["line"] for p in known), 2)
    coverage = 0.0 if not priced else round(len(known) / len(priced), 4)

    json.dump(
        {
            "currency": currency,
            "basis": "supplied printing, else cheapest available",
            "freshness": "cached up to 24h",
            "cached_hits": cached_hits,
            "cards": priced,
            "subtotal_known": subtotal,
            "missing": missing,
            "coverage": coverage,
            "strictly_under_budget": None,
        },
        sys.stdout,
        indent=2,
        ensure_ascii=False,
    )
    sys.stdout.write("\n")
    return 0 if not missing else 2


def cmd_parse_deck(args: argparse.Namespace) -> int:
    parsed = parse_deck_text(read_text(args.file))
    in_deck = deck_cards(parsed)
    command = [c for c in in_deck if c.get("zone") == "command"]
    excluded = [c for c in parsed["cards"] if c.get("zone") in {"sideboard", "maybeboard", "out"}]
    block = import_block(in_deck)
    json.dump(
        {
            "cards": parsed["cards"],
            "in_deck": in_deck,
            "command": command,
            "excluded": excluded,
            "ambiguous_categories": parsed["ambiguous_categories"],
            "headers": parsed["headers"],
            "import_block": block,
            "in_deck_count": sum(int(c["qty"]) for c in in_deck),
        },
        sys.stdout,
        indent=2,
        ensure_ascii=False,
    )
    sys.stdout.write("\n")
    return 0


def cmd_validate_deck(args: argparse.Namespace) -> int:
    parsed = parse_deck_text(read_text(args.file))
    in_deck = deck_cards(parsed)
    errors: list[str] = []
    if not in_deck:
        errors.append("no in-deck cards")

    block = import_block(in_deck)
    for line in block.splitlines():
        if line and not LINE_QTY_RE.match(line):
            errors.append(f"import block has non-card line: {line}")

    leaked = [c["name"] for c in parsed["cards"] if c.get("zone") in {"sideboard", "maybeboard", "out"}]
    if leaked and args.warn_excluded:
        pass

    total = sum(int(c["qty"]) for c in in_deck)
    command = [c for c in in_deck if c.get("zone") == "command"]
    if args.final:
        if total != COMMANDER_TOTAL:
            errors.append(f"legal Commander size is {COMMANDER_TOTAL} including command-zone cards, found {total}")
        if not command:
            errors.append("no command-zone cards identified")

    unresolved: list[str] = []
    if args.resolve and in_deck:
        names = []
        seen = set()
        for c in in_deck:
            if c["name"] not in seen:
                seen.add(c["name"])
                names.append(c["name"])
        _cards, missing = fetch_collection([{"name": n} for n in names])
        for item in missing:
            n = item.get("name") if isinstance(item, dict) else None
            if n:
                unresolved.append(n)
        if unresolved:
            errors.append(f"unresolved names: {', '.join(unresolved)}")

    ok = not errors
    json.dump(
        {
            "ok": ok,
            "errors": errors,
            "in_deck_count": total,
            "command": [c["name"] for c in command],
            "excluded": [c["name"] for c in parsed["cards"] if c.get("zone") in {"sideboard", "maybeboard", "out"}],
            "ambiguous_categories": parsed["ambiguous_categories"],
            "unresolved": unresolved,
            "import_block": block,
        },
        sys.stdout,
        indent=2,
        ensure_ascii=False,
    )
    sys.stdout.write("\n")
    return 0 if ok else 2


def cmd_write_deck(args: argparse.Namespace) -> int:
    text = sys.stdin.read() if args.file_in is None else Path(args.file_in).read_text(encoding="utf-8")
    parsed = parse_deck_text(text)
    in_deck = deck_cards(parsed)
    if not in_deck:
        print("No in-deck cards to write", file=sys.stderr)
        return 1
    dest = Path(args.dest)
    if dest.exists() and not args.force:
        sample = dest.read_text(encoding="utf-8")[:200]
        if sample.strip() and not any(
            LINE_QTY_RE.match(line.strip())
            for line in sample.splitlines()
            if line.strip()
        ):
            print(f"Refusing to overwrite non-deck file: {dest}", file=sys.stderr)
            return 1
    block = import_block(in_deck)
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".tmp")
    tmp.write_text(block, encoding="utf-8")
    tmp.replace(dest)
    json.dump(
        {
            "path": str(dest),
            "in_deck_count": sum(int(c["qty"]) for c in in_deck),
            "cards": len(in_deck),
        },
        sys.stdout,
        indent=2,
        ensure_ascii=False,
    )
    sys.stdout.write("\n")
    return 0


def cmd_bulk(args: argparse.Namespace) -> int:
    cache_dir = Path(args.cache_dir).expanduser()
    cache_dir.mkdir(parents=True, exist_ok=True)
    manifest = http_json("GET", f"{API}/bulk-data")
    item = None
    for entry in manifest.get("data") or []:
        if entry.get("type") == args.type:
            item = entry
            break
    if item is None:
        print(f"Unknown bulk type {args.type!r}", file=sys.stderr)
        return 1

    updated = item.get("updated_at") or "unknown"
    download_uri = item.get("jsonl_download_uri")
    if not download_uri:
        print("Bulk item has no jsonl_download_uri", file=sys.stderr)
        return 1

    dest = cache_dir / f"{args.type}.jsonl.gz"
    meta_path = cache_dir / f"{args.type}.meta.json"
    meta: dict[str, Any] = {}
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            meta = {}

    skipped = dest.exists() and meta.get("updated_at") == updated
    if not skipped:
        download_file(download_uri, dest)
        meta_path.write_text(
            json.dumps({"type": args.type, "updated_at": updated}, indent=2) + "\n",
            encoding="utf-8",
        )

    with gzip.open(dest, "rb") as gz:
        gz.read(1)

    json.dump(
        {
            "type": args.type,
            "updated_at": updated,
            "path": str(dest),
            "downloaded": not skipped,
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

    search = sub.add_parser("search", help="GET /cards/search")
    search.add_argument("query")
    search.add_argument("--unique", choices=("cards", "prints", "art"), default="cards")
    search.add_argument("--order", default=None)
    search.add_argument("--max", type=int, default=DEFAULT_SEARCH_MAX, dest="max")
    search.add_argument("--fields", default=DEFAULT_FIELDS)
    search.set_defaults(func=cmd_search)

    named = sub.add_parser("named", help="GET /cards/named")
    named.add_argument("name")
    named.add_argument("--fuzzy", action="store_true")
    named.add_argument("--set", default=None)
    named.add_argument("--fields", default=None)
    named.set_defaults(func=cmd_named)

    collection = sub.add_parser("collection", help="POST /cards/collection from a list")
    collection.add_argument("file")
    collection.add_argument("--fuzzy-missing", action="store_true")
    collection.add_argument("--fields", default=DEFAULT_FIELDS)
    collection.set_defaults(func=cmd_collection)

    prices = sub.add_parser("prices", help="Value a list in a Scryfall currency")
    prices.add_argument("file")
    prices.add_argument("--currency", required=True, choices=PRICE_CURRENCIES)
    prices.add_argument("--fresh", action="store_true")
    prices.add_argument("--cache-dir", default=str(DEFAULT_CACHE))
    prices.set_defaults(func=cmd_prices)

    parse_deck = sub.add_parser("parse-deck", help="Parse Archidekt or quantity/name text")
    parse_deck.add_argument("file")
    parse_deck.set_defaults(func=cmd_parse_deck)

    validate = sub.add_parser("validate-deck", help="Validate a decklist or import block")
    validate.add_argument("file")
    validate.add_argument("--final", action="store_true")
    validate.add_argument("--resolve", action="store_true")
    validate.add_argument("--warn-excluded", action="store_true")
    validate.set_defaults(func=cmd_validate_deck)

    write = sub.add_parser("write-deck", help="Atomically write a clean import list")
    write.add_argument("dest")
    write.add_argument("--file-in", default=None, help="Source list; default stdin")
    write.add_argument("--force", action="store_true")
    write.set_defaults(func=cmd_write_deck)

    bulk = sub.add_parser("bulk", help="Download a Scryfall bulk jsonl.gz file")
    bulk.add_argument("type", choices=BULK_TYPES, nargs="?", default="oracle_cards")
    bulk.add_argument("--cache-dir", default=str(DEFAULT_CACHE))
    bulk.set_defaults(func=cmd_bulk)

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
