---
name: rk-mtg-commander-deck-playbook
description: Write a piloting playbook for an existing Commander deck. Use when the user wants a deck playbook, how to pilot or play an EDH list, a mulligan guide, sequencing, combo lines, or a recovery plan.
---

# Commander deck playbook

Explain the submitted deck as it exists. Do not replace cards. Do not silently optimize the list.

If analysis finds a deckbuilding problem, state the play limitation. Offer a handoff to `rk-mtg-commander-deck-builder` only if the user wants changes.

The section outline lives in [playbook.md](playbook.md). That file is structure, not a sample guide. Do not put card names or preset turn or count targets in this skill.

## Preflight

This skill needs `rk-mtg-scryfall`. `rk-mtg-spellbook` and `rk-mtg-goldfish` are optional. The Skills CLI does not install dependencies for you.

If `rk-mtg-scryfall` is missing from this session, stop. Tell the user to install the full repo:

```
npx skills add reakaleek/mtg-commander-deck-builder-skills
```

If `rk-mtg-spellbook` is missing, ground combo lines in Oracle text only and say the catalog was skipped. If `rk-mtg-goldfish` is missing, skip sample hands.

Find each helper from the installed skill directory that contains its `SKILL.md`. Run `scripts/<name>.py` from that folder, or pass the full path. Do not search the repo and read the `.py` source. If a flag is unclear, run `--help`. Open the source only if the command fails.

Do not replace helpers with ad-hoc HTTP.

This skill may accept a deck produced by `rk-mtg-commander-deck-builder`. It does not depend on that skill and must not rewrite the builder's file.

## Input

Accept Archidekt exports and clean quantity-plus-name lists through `rk-mtg-scryfall`:

```
python scripts/scryfall.py parse-deck FILE
python scripts/scryfall.py collection FILE
```

Prefer the canonical deck file when the user supplies it. The playbook is read-only. Never write that file.

If the export does not identify command-zone cards, confirm them.

Ask about player experience, desired guide depth, and any interactions they especially want explained. Reuse table rules they already stated.

## Grounding

Fetch Oracle text for every card, including all faces. Ground every interaction in that text.

Do not invent combos. Distinguish guaranteed lines from conditional synergies.

When `rk-mtg-spellbook` is available, run `spellbook.py combos FILE --commander NAME`. Reject a line that neither Spellbook nor Oracle text supports.

For each line, note prerequisites, resource requirements, likely interruption points, and recovery options.

When `rk-mtg-goldfish` is available, you may run `goldfish.py new` for two or three opening hands. Label them as samples, not evidence.

## Output

Write a standalone Markdown playbook in chat. Follow [playbook.md](playbook.md).

Save it to a file only when the user asks.

Runtime card names belong in the generated playbook. Keep them out of this skill's instructions.
