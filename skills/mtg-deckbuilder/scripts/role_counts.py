#!/usr/bin/env python3
"""Count roles, curve and land-formula inputs from a deckbuilder tag table.

The tag table is Markdown with a header row naming its columns. Required:
Card, Primary. Optional: Qty, Secondaries, MV, Hits, Note. One row per card;
the commander row is excluded with --commander. A spell // land MDFC is a
row whose Secondaries include "Land". Hits (Targeted cards only) is one of
creature, artifact-enchantment, flexible, land, graveyard.

Swaps for a recount: --cut "Name" and --add "Name|Primary|Secondaries|MV|Hits"
(both repeatable); the output then has "before", "after" and "delta".
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

TAGS = (
    "Land", "Ramp", "Draw", "Selection", "Targeted", "Mass", "Protection",
    "Enabler", "Payoff", "Enhancer", "Wincon",
)
MDFC_LAND = {"default": 0.38, "mythic": 0.74}


def front(name: str) -> str:
    return name.split("//", 1)[0].strip().lower()


def split_tags(cell: str) -> list[str]:
    out = []
    for part in cell.replace(";", ",").split(","):
        word = part.strip().split(" ", 1)[0].strip("()")
        if word in TAGS:
            out.append(word)
    return out


def parse_mv(cell: str) -> int | None:
    digits = "".join(ch for ch in cell.split(" ", 1)[0] if ch.isdigit())
    return int(digits) if digits else None


def row_from(cells: dict[str, str]) -> dict[str, Any] | None:
    name = cells.get("card", "").strip()
    primary = split_tags(cells.get("primary", ""))
    if not name or not primary:
        return None
    qty_cell = cells.get("qty", "").strip()
    return {
        "name": name,
        "qty": int(qty_cell) if qty_cell.isdigit() else 1,
        "primary": primary[0],
        "secondaries": [t for t in split_tags(cells.get("secondaries", "")) if t != primary[0]],
        "mv": parse_mv(cells.get("mv", "")),
        "hits": cells.get("hits", "").strip().lower() or None,
    }


def parse_table(text: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    header: list[str] | None = None
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            header = None if not line else header
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if header is None:
            header = [c.lower() for c in cells]
            continue
        if set("".join(cells)) <= set("-: "):
            continue
        row = row_from(dict(zip(header, cells)))
        if row:
            rows.append(row)
    return rows


def parse_add(spec: str) -> dict[str, Any]:
    parts = (spec.split("|") + [""] * 5)[:5]
    row = row_from(dict(zip(("card", "primary", "secondaries", "mv", "hits"), parts)))
    if not row:
        raise SystemExit(f"bad --add {spec!r}: need Name|Primary|Secondaries|MV|Hits")
    return row


def summarize(rows: list[dict[str, Any]], mythic: set[str]) -> dict[str, Any]:
    primary: Counter[str] = Counter()
    any_tag: Counter[str] = Counter()
    hits: Counter[str] = Counter()
    cheap_targeted = 0
    curve: Counter[str] = Counter()
    mv_total = 0
    mv_cards = 0
    lands = 0
    mdfcs: list[str] = []
    no_mv: list[str] = []
    for row in rows:
        qty = row["qty"]
        primary[row["primary"]] += qty
        for tag in {row["primary"], *row["secondaries"]}:
            any_tag[tag] += qty
        if row["primary"] == "Land":
            lands += qty
            continue
        if "Land" in row["secondaries"]:
            mdfcs.append(row["name"])
        if row["primary"] == "Targeted":
            hits[row["hits"] or "unset"] += qty
            if row["mv"] is not None and row["mv"] <= 2:
                cheap_targeted += qty
        if row["mv"] is None:
            no_mv.append(row["name"])
            continue
        curve["6+" if row["mv"] >= 6 else str(row["mv"])] += qty
        if "Land" not in row["secondaries"]:
            mv_total += row["mv"] * qty
            mv_cards += qty
    mdfc_credit = sum(MDFC_LAND["mythic" if front(n) in mythic else "default"] for n in mdfcs)
    return {
        "cards": sum(r["qty"] for r in rows),
        "primary": dict(sorted(primary.items())),
        "primary_or_secondary": dict(sorted(any_tag.items())),
        "targeted_hits": dict(sorted(hits.items())),
        "targeted_mv_le_2": cheap_targeted,
        "curve_nonland": {k: curve.get(k, 0) for k in ("0", "1", "2", "3", "4", "5", "6+")},
        "lands": lands,
        "spell_land_mdfcs": mdfcs,
        "land_total_with_mdfc_credit": round(lands + mdfc_credit, 2),
        "avg_mv_nonland_excl_mdfc": round(mv_total / mv_cards, 3) if mv_cards else None,
        "rows_without_mv": no_mv,
    }


def delta(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key in ("primary", "primary_or_secondary", "targeted_hits", "curve_nonland"):
        keys = set(before[key]) | set(after[key])
        changed = {k: after[key].get(k, 0) - before[key].get(k, 0) for k in sorted(keys)}
        out[key] = {k: v for k, v in changed.items() if v}
    for key in ("lands", "land_total_with_mdfc_credit", "targeted_mv_le_2"):
        if after[key] != before[key]:
            out[key] = round(after[key] - before[key], 2)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("tags", help="Markdown file with the tag table")
    ap.add_argument("--commander", action="append", default=[], help="row to exclude (repeatable)")
    ap.add_argument("--stats", help="rk-mtg-scryfall deck-stats JSON, for MDFC rarity")
    ap.add_argument("--cut", action="append", default=[], help="card to remove (repeatable)")
    ap.add_argument("--add", action="append", default=[], help="Name|Primary|Secondaries|MV|Hits")
    args = ap.parse_args()

    skip = {front(n) for n in args.commander}
    rows = [r for r in parse_table(Path(args.tags).read_text(encoding="utf-8")) if front(r["name"]) not in skip]
    if not rows:
        print("No tag rows parsed; need a header row with Card and Primary", file=sys.stderr)
        return 1

    mythic: set[str] = set()
    if args.stats:
        stats = json.loads(Path(args.stats).read_text(encoding="utf-8"))
        mythic = {front(m["name"]) for m in stats.get("spell_land_mdfcs", []) if m.get("rarity") == "mythic"}

    before = summarize(rows, mythic)
    if not args.cut and not args.add:
        json.dump(before, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0

    names = {front(r["name"]) for r in rows}
    missing = [c for c in args.cut if front(c) not in names]
    if missing:
        print(f"--cut not in table: {', '.join(missing)}", file=sys.stderr)
        return 1
    cuts = {front(c) for c in args.cut}
    after_rows = [r for r in rows if front(r["name"]) not in cuts] + [parse_add(a) for a in args.add]
    after = summarize(after_rows, mythic)
    json.dump({"before": before, "after": after, "delta": delta(before, after)}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
