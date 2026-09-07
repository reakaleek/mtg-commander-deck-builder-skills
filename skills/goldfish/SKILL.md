---
name: goldfish
description: "Solitaire and multi-seat Commander goldfishing: shuffle a decklist, take an opening hand, mulligan, and play turns round by round, or run a Monte Carlo mana-base check. Use when the user wants to goldfish a deck, test opening hands, simulate draws turn by turn, playtest solo or with multiple seats, or check land-flood or land-screw odds."
---

# Goldfish

Run the helper next to this file for every step. Do not hand-simulate shuffles or draws yourself, and do not reimplement the state file.

The helper is `scripts/goldfish.py` in this skill directory, the folder that contains this `SKILL.md`. Run it from that folder, or pass the full path to that file. Do not read the `.py` source. The commands below are enough. If a flag is unclear, run `--help`. Open the source only if a command fails.

```
python scripts/goldfish.py <command>
python scripts/goldfish.py --help
```

This skill only tracks zones (library, hand, battlefield, graveyard, exile, command zone) and turn structure. It does not know Oracle text, mana costs, or legality: it cannot tell you whether a play is legal or what a card does. Look those up with `scryfall` first, then use this skill to move cards between zones as the game plays out.

## Decklist input

Any file of `quantity + name` lines works, the same shape the other skills read and write. Optional `[Categories]` tags and set/collector suffixes are ignored for card identity. Pass `-` to read from stdin.

Commander decks usually store the canonical file as plain `quantity + name` lines with no way to mark the command zone (the text block cannot keep that flag, see the `commander-deck-builder` skill). Pass `--commander "Exact Name"` once per commander or background so those cards start in the command zone instead of the shuffled library.

## Play one seat round by round

Each command reads and rewrites a small JSON state file, so separate invocations share one game. Give each seat in a multiplayer goldfish its own `--state` path (for example `seat1.json`, `seat2.json`), each started from that seat's own decklist.

```bash
python scripts/goldfish.py new deck.txt --state seat1.json --seed 42 --commander "Krenko, Mob Boss"
python scripts/goldfish.py mulligan --state seat1.json
python scripts/goldfish.py keep --state seat1.json --bottom "Mountain"
python scripts/goldfish.py next-turn --state seat1.json
python scripts/goldfish.py play "Mountain" --state seat1.json
python scripts/goldfish.py move --name "Krenko, Mob Boss" --from command --to battlefield --state seat1.json
python scripts/goldfish.py tap "Mountain" --state seat1.json
python scripts/goldfish.py state --state seat1.json
```

- `new` parses the decklist, shuffles the library, and draws the opening hand. `--on-draw` marks this seat as not going first. Omit `--seed` for a fresh random shuffle each run, or set it for a reproducible one.
- `mulligan` is London style: shuffle the whole hand back in, draw a fresh hand of the same size, and increment the mulligan count. Repeatable.
- `keep` locks in the current hand. It requires bottoming exactly one card per mulligan taken, named with one `--bottom NAME` per card. Turns cannot start before `keep`.
- `next-turn` untaps every permanent, then draws a card, except turn 1 for the seat that is on the play, which skips that draw.
- `play NAME` moves one copy of a card from hand to `--zone battlefield` (default), `graveyard`, `exile`, or `command`.
- `move` is the general zone-to-zone tool for anything `play` does not cover: tutoring, discarding, milling a specific card, bouncing a permanent, casting from the command zone, or putting a card on the bottom of the library with `--from library --bottom`. Omit `--name` when moving from `library` to take the top card.
- `mill --count N` moves N cards from the top of the library to the graveyard or `--zone-to exile`.
- `tap` / `untap` mark a permanent by name, or `--all` for the whole battlefield.
- `shuffle` reshuffles the library in place, for a tutor or fetch effect that shuffles after.
- `state` prints the full current state: turn, hand, battlefield, graveyard, exile, command zone, library size, and a short log.

The state file is plain JSON. Read it directly, or always re-run `state` after each step, to decide what to play next.

## Mana-base check without playing a game

`stats` runs a fast Monte Carlo simulation over many random shuffles instead of a single playthrough. It never touches a state file.

This skill has no Oracle data of its own, so it does not know which cards are lands. Get that from `scryfall` instead of guessing or asking the user to list every land by hand:

```bash
python ../scryfall/scripts/scryfall.py collection deck.txt --fields name,type_line > types.json
python scripts/goldfish.py stats deck.txt --types types.json --iterations 5000 --turns 8
```

`--types PATH` reads that scryfall `collection` (or `search`) JSON and counts every card whose `type_line` contains `Land` as a land, basic or not. Use `--land NAME` instead, or in addition, only for a card that should count as a land for this check despite its type line (a land-cycling card kept in hand as a land substitute, for example), or when `scryfall` cannot be run. At least one of `--types` or `--land` is required.

It reports the average lands in the opening hand, the share of opening hands with 0-1 or 6-plus lands, and the average cumulative lands seen by each turn. Use it to judge whether a land count or curve is likely to flood or screw before playing out individual games.

## Multiplayer goldfishing

For a 4-player simulation, run `new` once per seat with that seat's own decklist and its own `--state` file, then advance seats independently with `next-turn` in whatever order the table's turn order requires. This skill does not model combat, life totals, or interaction between seats: track outside effects (damage, removal, stolen permanents) with `move` calls between the affected seats' state files.
