---
name: rk-mtg-spellbook
description: Look up catalogued Commander combos and bracket estimates from Commander Spellbook. Use when the user asks which combos are in a list, what a list is missing for a combo, or what bracket Spellbook estimates.
---

# Spellbook

This skill returns unofficial combo catalog and bracket-estimate data only. Oracle text and legality live on `rk-mtg-scryfall`. Do not call other deckbuilding skills from here.

The helper is `scripts/spellbook.py` in this skill directory, the folder that contains this `SKILL.md`. Run it from that folder, or pass the full path to the file. Do not read the `.py` source. The commands below are enough. If a flag is unclear, run `--help`. Open the source only if the command fails.

```
python scripts/spellbook.py <command>
python scripts/spellbook.py --help
```

These endpoints are unofficial. No API key, no SLA, shapes can change. Be polite. Do not replace the helper with ad-hoc HTTP.

## Pick the method

- Combos present or one card short: `combos`
- Bracket estimate and justifications: `bracket`

```bash
python scripts/spellbook.py combos deck.txt --commander 'COMMANDER NAME'
python scripts/spellbook.py bracket deck.txt --commander 'COMMANDER NAME'
```

Repeat `--commander` for partners or a background. Cards named with `--commander` go in the command-zone payload and are omitted from the main list. If the file already marks command-zone cards, those are used when `--commander` is omitted.

`combos` prints `included` lines (cards, prerequisites, result) and `almostIncluded` lines with the missing card. `bracket` prints the estimate and justifications. Treat both as catalog evidence, not as proof a line is good for this table.

## Headers and limits

```
User-Agent: mtg-commander-deck-builder-skills/1.0 (spellbook helper)
Accept: application/json
```

Wait at least 500ms between requests. On HTTP 429, stop, wait at least 30s, then retry slower.

Cache under `~/.cache/spellbook/` for 24 hours.
