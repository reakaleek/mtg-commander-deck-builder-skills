---
name: rk-mtg-edhrec
description: Fetch EDHREC commander staples, card synergies, inclusion rates, and average decks from json.edhrec.com. Use when the user asks about EDHREC, high synergy cards, Commander staples, inclusion, average decklists, or what people play with a commander.
---

# EDHREC

Pick the page, slugify the exact Oracle name, then run the helper next to this file. Do not scrape HTML. Do not reimplement curl.

The helper is `scripts/edhrec.py` in this skill directory, the folder that contains this `SKILL.md`. Run it from that folder, or pass the full path to that file. Do not read the `.py` source. The commands below are enough. If a flag is unclear, run `--help`. Open the source only if the command fails.

```
python scripts/edhrec.py <command>
python scripts/edhrec.py --help
```

These pages are unofficial frontend JSON. No API key, no SLA, shapes can change. Be polite.

This skill returns inclusion and commander-specific synergy. Oracle text and legality live on `rk-mtg-scryfall`. Do not call deckbuilding skills from here.

## Pick the page

- Named commander, ranked adds for a deck: `candidates`, with the deck's themes and `--exclude` set to the list
- Named commander, staples or synergy: `commander`
- Named commander, advertised theme slugs from the page's tag list: `themes`
- Named commander, theme or budget subpage: `commander --theme SLUG` or `--budget`
- Named card, who plays it or related cards: `card`
- Named commander, typical list: `average-deck`

```bash
python scripts/edhrec.py candidates 'COMMANDER NAME' --theme blink --theme control --exclude deck.txt
python scripts/edhrec.py commander 'COMMANDER NAME'
python scripts/edhrec.py themes 'COMMANDER NAME'
python scripts/edhrec.py commander 'COMMANDER NAME' --theme tokens
python scripts/edhrec.py commander 'COMMANDER NAME' --budget
python scripts/edhrec.py card 'CARD NAME'
python scripts/edhrec.py average-deck 'COMMANDER NAME'
```

`--max` defaults to 10 cards per list. `--list HEADER` keeps matching list titles. Repeatable. `--fresh` skips the 24h cache. `--exclude FILE` (`commander`, `card`, `candidates`; `-` for stdin) drops cards already in that decklist and reports how many were dropped.

`candidates` merges the base commander page with every `--theme` page (and the budget page with `--budget`) into one deduped list, 40 cards by default. Each card has its best `synergy`, `lift`, and `trend_zscore`, its `inclusion` on each page, `sources` (page and list), and `category` (its type list). `--sort synergy|inclusion|lift|trend` picks the order, and cards on more pages win ties. `--min-synergy X` drops weak fits. Land lists are left out unless you pass `--lands`, because the mana base is built separately.

No fuzzy slugs. Missing pages often return HTTP 403 from the CDN, not 404. Resolve the Oracle name with the `rk-mtg-scryfall` skill, then retry. Check the returned `name`.

## Slugs

Lowercase, drop commas, apostrophes, and periods, then turn spaces into hyphens. Double-faced cards use the front face only.

URLs:

- `https://json.edhrec.com/pages/commanders/{slug}.json`
- `https://json.edhrec.com/pages/commanders/{slug}/{theme}.json`
- `https://json.edhrec.com/pages/cards/{slug}.json`
- `https://json.edhrec.com/pages/average-decks/{slug}.json`

## Headers and limits

```
User-Agent: mtg-commander-deck-builder-skills/1.0 (edhrec helper)
Accept: application/json
```

Wait at least 500ms between requests. On HTTP 429, stop, wait at least 30s, then retry slower.

Cache under `~/.cache/edhrec/{kind}/{slug}.json` for 24 hours. Inclusion and prices are not live.

## How to read the numbers

- `synergy` is commander-specific lift, not quality. High synergy means the card shows up here more than its baseline. A generic staple can have high inclusion and low synergy.
- `inclusion` is `num_decks` / `potential_decks`: the share of that commander's (or theme's) decks that play the card.
- `lift` is how many times more often the card shows up here than in other decks that could play it. It is the same idea as synergy, expressed as a ratio.
- `trend_zscore` above about 2 means the card is rising right now, often because it is new. Check that it is not just hype.
- Synergy or lift measures fit with the commander, and inclusion measures consensus. A card high on both is the safest add. High synergy with low inclusion is a niche pick worth reading. High inclusion with low synergy is a generic staple, so compare it with the slot's role.
- `similar` lists commanders whose decks look like this one's. Their `candidates` pages are a second pool when this commander's sample is small.
- Scryfall `edhrec_rank` is sitewide popularity. Use this skill when the question is "in this commander's decks."

If `cardlists` is missing, treat lists as empty. Do not guess staples from memory.
