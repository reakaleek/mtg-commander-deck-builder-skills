---
name: archidekt
description: "Derive an Archidekt API URL from a deck page URL and fetch that deck's JSON. Use when the user shares an Archidekt deck link, asks how to read or parse an Archidekt URL, or wants a deck fetched directly from Archidekt instead of pasting an export."
---

# Archidekt

Derive the API URL, then run the helper next to this file. Do not scrape the deck HTML page. Do not reimplement curl.

The helper is `scripts/archidekt.py` in this skill directory, the folder that contains this `SKILL.md`. Run it from that folder, or pass the full path to that file. Do not read the `.py` source. The commands below are enough. If a flag is unclear, run `--help`. Open the source only if the command fails.

```
python scripts/archidekt.py <command>
python scripts/archidekt.py --help
```

This skill returns Archidekt's own deck JSON, converted into `quantity + exact name` rows with a zone per card. Oracle text, legality, and prices live on `scryfall`. Synergy and inclusion live on `edhrec`. Do not call other deckbuilding skills from here.

## Reading an Archidekt URL

A deck page URL looks like:

```
https://archidekt.com/decks/<id>/<slug>
```

The numeric `<id>` is the only part that matters. The API URL for the same deck is:

```
https://archidekt.com/api/decks/<id>/
```

The helper derives this from either a full deck URL or a bare id. It does not need the slug.

```bash
python scripts/archidekt.py url 'https://archidekt.com/decks/19345263/my_deck'
python scripts/archidekt.py fetch 'https://archidekt.com/decks/19345263/my_deck'
python scripts/archidekt.py fetch 19345263
python scripts/archidekt.py fetch 'https://archidekt.com/decks/19345263/my_deck' --out deck.txt
```

`url` only prints the derived API URL. `fetch` calls it and returns the parsed deck. `--out` writes a clean `quantity + name` import list, the same shape `scryfall` `write-deck` produces, so it can feed straight into `scryfall` `validate-deck` or `write-deck`.

A private deck returns HTTP 404 from the API even though it exists. Ask the user to make it public or unlisted, or to paste an export instead.

## Fetch output

`fetch` returns:

- `cards`: every row with `qty`, `name`, `set`, `collector_number`, `foil`, `categories`, and `zone`
- `in_deck`: `cards` minus sideboard, maybeboard, and out-of-deck rows
- `command`: the command-zone subset of `in_deck`
- `excluded`: sideboard, maybeboard, and out-of-deck rows
- `import_block`: `in_deck` as pasteable `quantity + exact name` lines
- `written_to`: the `--out` path, or `null`

Zone comes from Archidekt's own categories on each card (`Commander`, `Sideboard`, `Maybeboard`, and similar), the same category vocabulary `scryfall` `parse-deck` recognizes for pasted exports. Never silently count sideboard or maybeboard cards in the deck.

## Headers and limits

```
User-Agent: mtg-commander-deck-builder-skills/1.0 (archidekt helper)
Accept: application/json
```

This is an unofficial, undocumented endpoint. No API key, no SLA, shapes can change. Wait at least 500ms between requests. On HTTP 429, stop, wait at least 30s, then retry slower.
