---
name: scryfall
description: "Query Scryfall via the REST API, search syntax, collection batches, cheapest-print prices, Archidekt deck parsing, and bulk data dumps. Use when looking up Magic cards, writing Scryfall searches, fetching a decklist, resolving card names, pricing a list, or parsing Archidekt text."
---

# Scryfall

Pick the cheapest Scryfall path, then run the helper next to this file. Do not reimplement curl.

```
python scripts/scryfall.py <command>
```

Search operators: [syntax.md](syntax.md)

This skill returns Oracle text, legality, printings, and prices. Inclusion and commander-specific synergy live elsewhere. Do not call other deckbuilding skills from here.

## Pick the method

- One known name: `named`
- Two or more known names: `collection`
- Discover or filter unknown cards: `search` with `unique:cards`
- Value a list in a requested currency: `prices`
- Parse or check an Archidekt export: `parse-deck` / `validate-deck`
- Repeated lookups or prices at scale: `bulk` (`oracle_cards`)

Never call `/cards/named` once per decklist line. Never paginate a search just to resolve names you already have. A `/cards/collection` object is one printing, not the cheapest printing.

## Helper

```bash
python scripts/scryfall.py search 'QUERY'
python scripts/scryfall.py named 'CARD NAME'
python scripts/scryfall.py named 'fuzzy fragment' --fuzzy
python scripts/scryfall.py collection decklist.txt --fuzzy-missing
python scripts/scryfall.py prices decklist.txt --currency eur
python scripts/scryfall.py parse-deck decklist.txt
python scripts/scryfall.py validate-deck decklist.txt
python scripts/scryfall.py write-deck deck.txt
python scripts/scryfall.py bulk oracle_cards
```

`search` defaults to `--max 40` and slim `--fields`. Raise `--max` only if you need more. Use `--unique prints` only when printings, prices, or art matter.

`--fuzzy` needs a recognizable fragment. A wild typo 404s or can match the wrong card. Check the returned `name`.

If the script cannot run, call `https://api.scryfall.com` with the same headers and spacing.

## Headers and limits

Every API request:

```
User-Agent: mtg-commander-deck-builder-skills/1.0 (scryfall helper)
Accept: application/json
```

Generic clients without a descriptive User-Agent get blocked.

| Endpoint | Limit |
|----------|-------|
| `/cards/search`, `/cards/named`, `/cards/random`, `/cards/collection` | 2/sec (wait ≥500ms) |
| `/cards/manifest` | 10/min |
| Other API methods | 10/sec |
| `*.scryfall.io` bulk files | No rate limit |

On HTTP 429: stop, wait at least 30s, then retry slower. Do not ignore 429s.

Cache fetched JSON for the session. Prices go stale after 24 hours. Oracle text rarely needs a refresh more than weekly.

## Search

`GET /cards/search?q=...`

- Default uniqueness is `unique:cards`. `unique:prints` explodes page count.
- Pages are 175 cards. Follow `has_more` / `next_page` only until you have enough.
- Tighten the query before fetching another page.

Do not mix these up:

| Query | Means |
|-------|--------|
| `f:commander` | Legal in Commander |
| `is:commander` | Can be your commander |
| `id:` | Color identity |
| `c:` | Card color |

## Collection

`POST /cards/collection` accepts at most 75 identifiers per call.

Valid identifier shapes: `{name}`, `{name,set}`, `{set,collector_number}`, or an `id` / `oracle_id`.

Response `data` is found cards. `not_found` is unresolved identifiers. Order is not a reliable 1:1 map when some names miss. Resolve leftovers with `named --fuzzy`, not another full collection.

## Prices

`prices FILE|- --currency <code>` values a parsed list.

- Supported codes are Scryfall's: `usd`, `eur`, `tix`.
- If a line has a set or collector number, price that printing.
- Otherwise use the cheapest available printing in that currency.
- Quantities are preserved. Missing prices stay unknown. Never treat a missing price as zero.
- Output includes coverage, unresolved names, and cache freshness.

## Archidekt lists

`parse-deck` reads minimal `quantity + name` lines and common Archidekt exports (optional `x`, set, collector number, foil marker, categories, labels). It splits command-zone, sideboard, maybeboard, and out-of-deck entries.

`validate-deck` checks syntax, quantities, and leakage of excluded piles into the import block. `--final` also checks Commander construction (legal size, commander present). `--resolve` asks Scryfall whether names exist.

`write-deck FILE` writes a clean import list atomically (quantity + exact name only).

The clean import block is only:

```
1 Card Name
```

No headings, prices, categories, or comments.

## Bulk

`GET /bulk-data`, then download `jsonl_download_uri`. Prefer `oracle_cards` for gameplay lookups. Cache under `~/.cache/scryfall/`.
