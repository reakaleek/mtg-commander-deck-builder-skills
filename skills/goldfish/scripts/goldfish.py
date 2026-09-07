#!/usr/bin/env python3
"""Goldfish helper: solitaire and multi-seat Commander simulation.

Tracks a shuffled library, hand, battlefield, graveyard, exile, and command
zone in a small JSON state file so an agent can play a game round by round
across separate command invocations. Also offers a Monte Carlo `stats`
command for mana-base analysis (land droughts and floods) without any
turn-by-turn play.
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
from pathlib import Path
from typing import Any

DEFAULT_HAND_SIZE = 7
DEFAULT_STATE = "goldfish-state.json"
MAX_LOG_ENTRIES = 50  # enough recent history for a session, without unbounded state-file growth

LINE_QTY_RE = re.compile(r"^(\d+)\s*x?\s+(.*)$", re.IGNORECASE)
SKIP_PREFIXES = ("//", "#")

ZONE_COMMAND = {"commander", "commanders", "command zone", "command", "cmdr"}
ZONE_SIDE = {"sideboard", "sb"}
ZONE_MAYBE = {"maybeboard", "maybe", "considering"}
ZONE_OUT = {"not included", "not in deck", "out of deck", "unused"}
ZONE_EXCLUDED = ZONE_SIDE | ZONE_MAYBE | ZONE_OUT
ZONE_MAIN_HEADERS = {"deck", "main", "mainboard", "main deck"}
KNOWN_LABELS = ZONE_COMMAND | ZONE_EXCLUDED
# Header lines are recognized only by an exact (count-stripped) match against
# this known set, e.g. "Sideboard" or "Sideboard (5)". A free-form heuristic
# ("any capitalized line") would risk silently swallowing a bare card name
# typed without its quantity, since Magic card names are also mostly Title
# Case. Canonical decklist files only ever use "quantity name" lines anyway.
KNOWN_HEADER_WORDS = KNOWN_LABELS | ZONE_MAIN_HEADERS
KNOWN_ZONES = {"library", "hand", "battlefield", "graveyard", "exile", "command"}


def read_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def parse_card_line(line: str) -> dict[str, Any] | None:
    raw = line.strip()
    if not raw or raw.startswith(SKIP_PREFIXES):
        return None

    header_name = re.sub(r"\s+\(\d+\)\s*$", "", raw).strip().lower()
    if header_name in KNOWN_HEADER_WORDS:
        return {"header": raw}

    m = LINE_QTY_RE.match(raw)
    if not m:
        raise RuntimeError(
            f"could not parse decklist line as a header or a 'quantity name' card line: {raw!r}"
        )

    qty = int(m.group(1))
    rest = m.group(2).strip()
    categories: list[str] = []

    while True:
        cat = re.search(r"\s+\[([^\]]+)\]\s*$", rest)
        if not cat:
            break
        categories.extend(p.strip() for p in cat.group(1).split(",") if p.strip())
        rest = rest[: cat.start()].rstrip()

    set_cn = re.search(r"\s+\(([A-Za-z0-9]{2,6})\)\s+\S+\s*$", rest)
    if set_cn:
        rest = rest[: set_cn.start()].rstrip()
    else:
        set_only = re.search(r"\s+\(([A-Za-z0-9]{2,6})\)\s*$", rest)
        if set_only:
            rest = rest[: set_only.start()].rstrip()

    name = rest.strip()
    if not name:
        return None
    return {"qty": qty, "name": name, "categories": categories}


def section_from_header(header: str) -> str | None:
    name = re.sub(r"\s+\(\d+\)\s*$", "", header).strip().lower()
    if name in KNOWN_LABELS:
        return name
    if name in ZONE_MAIN_HEADERS:
        return "main"
    return None


def classify_zone(categories: list[str], section: str | None) -> str:
    for cat in categories:
        label = cat.strip().lower()
        if label in ZONE_EXCLUDED:
            return "excluded"
        if label in ZONE_COMMAND:
            return "command"
    if section in ZONE_EXCLUDED:
        return "excluded"
    if section in ZONE_COMMAND:
        return "command"
    return "main"


def parse_deck_text(text: str, commander_names: list[str] | None = None) -> dict[str, Any]:
    forced_commanders = {n.strip().lower() for n in (commander_names or [])}
    library: list[str] = []
    command: list[str] = []
    section: str | None = None

    for raw in text.splitlines():
        parsed = parse_card_line(raw)
        if parsed is None:
            continue
        if "header" in parsed:
            section = section_from_header(parsed["header"])
            continue

        zone = classify_zone(parsed["categories"], section)
        if parsed["name"].strip().lower() in forced_commanders:
            zone = "command"
        for _ in range(parsed["qty"]):
            if zone == "excluded":
                continue
            if zone == "command":
                command.append(parsed["name"])
            else:
                library.append(parsed["name"])

    if not library and not command:
        raise RuntimeError("no in-deck cards found in decklist")
    return {"library": library, "command": command}


# --- state helpers ---------------------------------------------------------


def new_state(
    library: list[str],
    command: list[str],
    seed: int | None,
    on_play: bool,
    hand_size: int,
) -> dict[str, Any]:
    return {
        "seed": seed,
        "shuffle_count": 0,
        "hand_size": hand_size,
        "on_play": on_play,
        "turn": 0,
        "mulligans": 0,
        "kept": False,
        "deck_size": len(library) + len(command),
        "library": library,
        "hand": [],
        "battlefield": [],
        "graveyard": [],
        "exile": [],
        "command_zone": command,
        "deck_out": False,
        "log": [],
    }


def load_state(path: str) -> dict[str, Any]:
    p = Path(path)
    if not p.is_file():
        raise RuntimeError(f"no state file at {path}. Run 'new' first.")
    return json.loads(p.read_text(encoding="utf-8"))


def save_state(path: str, state: dict[str, Any]) -> None:
    dest = Path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".tmp")
    tmp.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(dest)


def rng_for(state: dict[str, Any]) -> random.Random:
    seed = state.get("seed")
    if seed is None:
        return random.Random()
    state["shuffle_count"] = int(state.get("shuffle_count", 0)) + 1
    return random.Random(f"{seed}:{state['shuffle_count']}")


def log(state: dict[str, Any], message: str) -> None:
    entries = state.setdefault("log", [])
    entries.append(message)
    del entries[:-MAX_LOG_ENTRIES]


def emit(state: dict[str, Any]) -> int:
    json.dump(state, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


# --- commands ----------------------------------------------------------


def cmd_new(args: argparse.Namespace) -> int:
    parsed = parse_deck_text(read_text(args.deck), args.commander)
    library = list(parsed["library"])
    command = list(parsed["command"])
    state = new_state(library, command, args.seed, not args.on_draw, args.hand_size)
    rng = rng_for(state)
    rng.shuffle(state["library"])
    state["hand"] = [state["library"].pop(0) for _ in range(min(args.hand_size, len(state["library"])))]
    log(state, f"opening hand drawn ({len(state['hand'])} cards)")
    save_state(args.state, state)
    return emit(state)


def cmd_mulligan(args: argparse.Namespace) -> int:
    state = load_state(args.state)
    if state["kept"]:
        raise RuntimeError("hand already kept for this game, cannot mulligan. Start a new game with 'new'.")
    state["library"].extend(state["hand"])
    state["hand"] = []
    rng = rng_for(state)
    rng.shuffle(state["library"])
    hand_size = state["hand_size"]
    state["hand"] = [state["library"].pop(0) for _ in range(min(hand_size, len(state["library"])))]
    state["mulligans"] += 1
    log(state, f"mulligan #{state['mulligans']} taken, new {len(state['hand'])}-card hand drawn")
    save_state(args.state, state)
    return emit(state)


def cmd_keep(args: argparse.Namespace) -> int:
    state = load_state(args.state)
    if state["kept"]:
        raise RuntimeError("hand already kept")
    bottom = list(args.bottom or [])
    if len(bottom) != state["mulligans"]:
        raise RuntimeError(
            f"London mulligan requires bottoming exactly {state['mulligans']} card(s), got {len(bottom)}"
        )
    for name in bottom:
        if name not in state["hand"]:
            raise RuntimeError(f"{name!r} is not in hand")
        state["hand"].remove(name)
        state["library"].append(name)
    state["kept"] = True
    log(state, f"kept {len(state['hand'])}-card hand, bottomed {len(bottom)} card(s)")
    save_state(args.state, state)
    return emit(state)


def cmd_draw(args: argparse.Namespace) -> int:
    state = load_state(args.state)
    count = args.count
    drawn = []
    for _ in range(count):
        if not state["library"]:
            state["deck_out"] = True
            log(state, "attempted to draw from an empty library")
            break
        drawn.append(state["library"].pop(0))
    state["hand"].extend(drawn)
    log(state, f"drew {len(drawn)} card(s): {', '.join(drawn) if drawn else '(none, library empty)'}")
    save_state(args.state, state)
    return emit(state)


def cmd_next_turn(args: argparse.Namespace) -> int:
    state = load_state(args.state)
    if not state["kept"]:
        raise RuntimeError("hand not kept yet, run 'keep' before starting turns")
    state["turn"] += 1
    for permanent in state["battlefield"]:
        permanent["tapped"] = False
    skip_draw = state["turn"] == 1 and state["on_play"]
    if skip_draw:
        log(state, f"turn {state['turn']} begins, on the play, draw skipped")
    else:
        if state["library"]:
            drawn = state["library"].pop(0)
            state["hand"].append(drawn)
            log(state, f"turn {state['turn']} begins, drew {drawn}")
        else:
            state["deck_out"] = True
            log(state, f"turn {state['turn']} begins, library empty, cannot draw")
    save_state(args.state, state)
    return emit(state)


def _remove_one(items: list[str], name: str) -> None:
    for i, item in enumerate(items):
        if item == name:
            del items[i]
            return
    raise RuntimeError(f"{name!r} not found")


def cmd_play(args: argparse.Namespace) -> int:
    state = load_state(args.state)
    if args.name not in state["hand"]:
        raise RuntimeError(f"{args.name!r} is not in hand")
    _remove_one(state["hand"], args.name)
    if args.zone == "battlefield":
        state["battlefield"].append({"name": args.name, "tapped": args.tapped})
    else:
        state[_zone_key(args.zone)].append(args.name)
    log(state, f"played {args.name} to {args.zone}")
    save_state(args.state, state)
    return emit(state)


def _zone_key(zone: str) -> str:
    return {
        "library": "library",
        "hand": "hand",
        "battlefield": "battlefield",
        "graveyard": "graveyard",
        "exile": "exile",
        "command": "command_zone",
    }[zone]


def _zone_list(state: dict[str, Any], zone: str) -> list[Any]:
    return state[_zone_key(zone)]


def cmd_move(args: argparse.Namespace) -> int:
    state = load_state(args.state)
    src = _zone_list(state, args.zone_from)
    dst = _zone_list(state, args.zone_to)

    if args.bottom and args.zone_from != "library":
        raise RuntimeError("--bottom only applies when --from library")

    if args.zone_from == "library":
        if args.name is not None:
            raise RuntimeError(
                "moving from 'library' always takes the top (or --bottom) card; "
                "--name is not supported for this direction"
            )
        if not src:
            raise RuntimeError("library is empty")
        card = src.pop(len(src) - 1 if args.bottom else 0)
    elif args.zone_from == "battlefield":
        if args.name is None:
            raise RuntimeError("--name is required when moving from battlefield")
        idx = next((i for i, p in enumerate(src) if p["name"] == args.name), None)
        if idx is None:
            raise RuntimeError(f"{args.name!r} not found on battlefield")
        card = src.pop(idx)["name"]
    else:
        if args.name is None:
            raise RuntimeError(f"--name is required when moving from {args.zone_from}")
        if args.name not in src:
            raise RuntimeError(f"{args.name!r} not found in {args.zone_from}")
        _remove_one(src, args.name)
        card = args.name

    if args.zone_to == "battlefield":
        dst.append({"name": card, "tapped": False})
    else:
        dst.append(card)

    log(state, f"moved {card} from {args.zone_from} to {args.zone_to}")
    save_state(args.state, state)
    return emit(state)


def cmd_mill(args: argparse.Namespace) -> int:
    state = load_state(args.state)
    dst = _zone_list(state, args.zone_to)
    milled = []
    for _ in range(args.count):
        if not state["library"]:
            state["deck_out"] = True
            break
        card = state["library"].pop(0)
        milled.append(card)
        dst.append(card)
    log(state, f"milled {len(milled)} card(s) to {args.zone_to}: {', '.join(milled) if milled else '(none)'}")
    save_state(args.state, state)
    return emit(state)


def cmd_tap(args: argparse.Namespace, tapped: bool) -> int:
    state = load_state(args.state)
    if args.all:
        matched = 0
        for permanent in state["battlefield"]:
            permanent["tapped"] = tapped
            matched += 1
        log(state, f"{'tapped' if tapped else 'untapped'} all ({matched}) permanents")
    else:
        permanent = next((p for p in state["battlefield"] if p["name"] == args.name), None)
        if permanent is None:
            raise RuntimeError(f"{args.name!r} not found on battlefield")
        permanent["tapped"] = tapped
        log(state, f"{'tapped' if tapped else 'untapped'} {args.name}")
    save_state(args.state, state)
    return emit(state)


def cmd_shuffle(args: argparse.Namespace) -> int:
    state = load_state(args.state)
    rng = rng_for(state)
    rng.shuffle(state["library"])
    log(state, "shuffled library")
    save_state(args.state, state)
    return emit(state)


def cmd_state(args: argparse.Namespace) -> int:
    state = load_state(args.state)
    return emit(state)


def land_names_from_types(path: str) -> set[str]:
    """Derive land card names from a scryfall `collection` (or `search`) JSON
    dump. Accepts either the full envelope (`{"cards": [...]}`) or a bare
    list of card objects, each needing at least `name` and `type_line`."""
    data = json.loads(read_text(path))
    rows = data.get("cards") if isinstance(data, dict) else data
    if not isinstance(rows, list):
        raise RuntimeError(f"{path!r} is not a scryfall card list ({{'cards': [...]}} or [...])")
    names = set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        name = row.get("name")
        type_line = row.get("type_line") or ""
        if name and "land" in type_line.lower():
            names.add(name.strip().lower())
    return names


def cmd_stats(args: argparse.Namespace) -> int:
    parsed = parse_deck_text(read_text(args.deck), args.commander)
    library = parsed["library"]
    land_names = {n.strip().lower() for n in (args.land or [])}
    if args.types:
        land_names |= land_names_from_types(args.types)
    if not land_names:
        raise RuntimeError(
            "no lands identified: pass --types PATH (scryfall 'collection' or "
            "'search' JSON with name + type_line) and/or --land NAME to identify lands"
        )

    deck_size = len(library)
    hand_size = args.hand_size
    iterations = args.iterations
    turns = args.turns
    rng = random.Random(args.seed) if args.seed is not None else random.Random()

    opening_land_counts: list[int] = []
    lands_by_turn_totals = [0] * (turns + 1)
    zero_or_one_land_hands = 0
    six_plus_land_hands = 0

    for _ in range(iterations):
        shuffled = list(library)
        rng.shuffle(shuffled)
        hand = shuffled[:hand_size]
        opening_lands = sum(1 for c in hand if c.strip().lower() in land_names)
        opening_land_counts.append(opening_lands)
        if opening_lands <= 1:
            zero_or_one_land_hands += 1
        if opening_lands >= 6:
            six_plus_land_hands += 1

        lands_seen = opening_lands
        cursor = hand_size
        for t in range(1, turns + 1):
            if not (t == 1 and args.on_play) and cursor < len(shuffled):
                if shuffled[cursor].strip().lower() in land_names:
                    lands_seen += 1
                cursor += 1
            lands_by_turn_totals[t] += lands_seen

    avg_opening = round(sum(opening_land_counts) / iterations, 3)
    avg_by_turn = [None] + [round(total / iterations, 3) for total in lands_by_turn_totals[1:]]

    json.dump(
        {
            "deck_size": deck_size,
            "lands_in_deck": sum(1 for c in library if c.strip().lower() in land_names),
            "iterations": iterations,
            "hand_size": hand_size,
            "on_play": args.on_play,
            "avg_opening_hand_lands": avg_opening,
            "opening_hand_0_1_lands_pct": round(100 * zero_or_one_land_hands / iterations, 2),
            "opening_hand_6_plus_lands_pct": round(100 * six_plus_land_hands / iterations, 2),
            "avg_cumulative_lands_seen_by_turn": avg_by_turn,
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

    def add_state_arg(p: argparse.ArgumentParser) -> None:
        p.add_argument("--state", default=DEFAULT_STATE, help=f"Path to the game state file (default {DEFAULT_STATE})")

    new = sub.add_parser("new", help="Start a game: parse a decklist, shuffle, draw an opening hand")
    new.add_argument("deck", help="Path to a decklist file, or - for stdin")
    add_state_arg(new)
    new.add_argument("--seed", type=int, default=None, help="Seed for reproducible shuffles")
    new.add_argument("--on-draw", action="store_true", help="This seat is on the draw, not on the play")
    new.add_argument("--hand-size", type=int, default=DEFAULT_HAND_SIZE)
    new.add_argument("--commander", action="append", default=[], help="Card name to start in the command zone (repeatable)")
    new.set_defaults(func=cmd_new)

    mull = sub.add_parser("mulligan", help="London mulligan: shuffle hand back in, draw a fresh hand")
    add_state_arg(mull)
    mull.set_defaults(func=cmd_mulligan)

    keep = sub.add_parser("keep", help="Keep the current hand, bottoming one card per mulligan taken")
    add_state_arg(keep)
    keep.add_argument("--bottom", action="append", default=[], help="Card name to bottom (repeat once per mulligan)")
    keep.set_defaults(func=cmd_keep)

    draw = sub.add_parser("draw", help="Draw card(s) from the library into hand")
    add_state_arg(draw)
    draw.add_argument("--count", type=int, default=1)
    draw.set_defaults(func=cmd_draw)

    nxt = sub.add_parser("next-turn", help="Advance to the next turn: untap, then draw (unless turn 1 on the play)")
    add_state_arg(nxt)
    nxt.set_defaults(func=cmd_next_turn)

    play = sub.add_parser("play", help="Move a card from hand to another zone (default battlefield)")
    add_state_arg(play)
    play.add_argument("name", help="Exact card name in hand")
    play.add_argument("--zone", choices=sorted(KNOWN_ZONES - {"hand", "library"}), default="battlefield")
    play.add_argument("--tapped", action="store_true", help="Enter the battlefield tapped")
    play.set_defaults(func=cmd_play)

    move = sub.add_parser("move", help="Move a card between any two zones")
    add_state_arg(move)
    move.add_argument("--name", default=None, help="Card name (omit to take the top of the library)")
    move.add_argument("--from", dest="zone_from", choices=sorted(KNOWN_ZONES), required=True)
    move.add_argument("--to", dest="zone_to", choices=sorted(KNOWN_ZONES), required=True)
    move.add_argument("--bottom", action="store_true", help="Take from the bottom of the library instead of the top")
    move.set_defaults(func=cmd_move)

    mill = sub.add_parser("mill", help="Move cards from the top of the library to graveyard or exile")
    add_state_arg(mill)
    mill.add_argument("--count", type=int, default=1)
    mill.add_argument("--zone-to", dest="zone_to", choices=["graveyard", "exile"], default="graveyard")
    mill.set_defaults(func=cmd_mill)

    tap = sub.add_parser("tap", help="Tap a permanent on the battlefield")
    add_state_arg(tap)
    tap.add_argument("name", nargs="?", default=None)
    tap.add_argument("--all", action="store_true", help="Tap every permanent")
    tap.set_defaults(func=lambda a: cmd_tap(a, True))

    untap = sub.add_parser("untap", help="Untap a permanent on the battlefield")
    add_state_arg(untap)
    untap.add_argument("name", nargs="?", default=None)
    untap.add_argument("--all", action="store_true", help="Untap every permanent")
    untap.set_defaults(func=lambda a: cmd_tap(a, False))

    shuffle = sub.add_parser("shuffle", help="Reshuffle the library in place")
    add_state_arg(shuffle)
    shuffle.set_defaults(func=cmd_shuffle)

    state_cmd = sub.add_parser("state", help="Print the current game state")
    add_state_arg(state_cmd)
    state_cmd.set_defaults(func=cmd_state)

    stats = sub.add_parser("stats", help="Monte Carlo mana-base analysis, no turn-by-turn state")
    stats.add_argument("deck", help="Path to a decklist file, or - for stdin")
    stats.add_argument(
        "--types",
        default=None,
        help="Path to scryfall 'collection' or 'search' JSON (name + type_line) to auto-detect lands",
    )
    stats.add_argument("--land", action="append", default=[], help="Card name that counts as a land (repeatable)")
    stats.add_argument("--commander", action="append", default=[], help="Card name excluded from the library (repeatable)")
    stats.add_argument("--iterations", type=int, default=1000)
    stats.add_argument("--turns", type=int, default=10)
    stats.add_argument("--hand-size", type=int, default=DEFAULT_HAND_SIZE)
    stats.add_argument("--on-play", dest="on_play", action="store_true", default=True)
    stats.add_argument("--on-draw", dest="on_play", action="store_false")
    stats.add_argument("--seed", type=int, default=None)
    stats.set_defaults(func=cmd_stats)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command in {"tap", "untap"} and not args.all and not args.name:
        parser.error("provide a card name or --all")
    try:
        return args.func(args)
    except RuntimeError as e:
        print(e, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
