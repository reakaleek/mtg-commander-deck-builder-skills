---
name: edhrec
description: Fetch EDHREC commander staples, card synergies, inclusion rates, and average decks from json.edhrec.com. Use when the user asks about EDHREC, high synergy cards, Commander staples, inclusion, average decklists, or what people play with a commander.
---

# EDHREC

Pick the page, slugify the exact Oracle name, then run the helper next to this file. Do not scrape HTML. Do not reimplement curl.

```
python scripts/edhrec.py <command>
```

These pages are unofficial frontend JSON. No API key, no SLA, shapes can change. Be polite.

This skill returns inclusion and commander-specific synergy. Oracle text and legality live on `scryfall`. Do not call deckbuilding skills from here.

## Pick the page

- Named commander, staples or synergy: `commander`
- Named card, who plays it or related cards: `card`
- Named commander, typical list: `average-deck`

```bash
python scripts/edhrec.py commander 'COMMANDER NAME'
python scripts/edhrec.py card 'CARD NAME'
python scripts/edhrec.py average-deck 'COMMANDER NAME'
```

`--max` defaults to 10 cards per list. `--list HEADER` keeps matching list titles. Repeatable. `--fresh` skips the 24h cache.

No fuzzy slugs. Missing pages often return HTTP 403 from the CDN, not 404. Resolve the Oracle name with the `scryfall` skill, then retry. Check the returned `name`.

## Slugs

Lowercase, drop commas, apostrophes, and periods, then turn spaces into hyphens. Double-faced cards use the front face only.

URLs:

- `https://json.edhrec.com/pages/commanders/{slug}.json`
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
- `num_decks` / `potential_decks` is inclusion in that commander's sample.
- Scryfall `edhrec_rank` is sitewide popularity. Use this skill when the question is "in this commander's decks."

If `cardlists` is missing, treat lists as empty. Do not guess staples from memory.
