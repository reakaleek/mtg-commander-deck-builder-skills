---
name: commander-deck-playbook
description: Write a piloting playbook for an existing Commander deck. Use when the user wants a deck playbook, how to pilot or play an EDH list, a mulligan guide, sequencing, combo lines, or a recovery plan.
---

# Commander deck playbook

Explain the submitted deck as it exists. Do not replace cards. Do not silently optimize the list.

If analysis finds a deckbuilding problem, state the play limitation. Offer a handoff to `commander-deck-builder` only if the user wants changes.

The section outline lives in [playbook.md](playbook.md). That file is structure, not a sample guide. Do not put card names or preset turn or count targets in this skill.

## Preflight

This skill needs `scryfall`. The Skills CLI does not install dependencies for you.

If that skill is missing from this session, stop. Tell the user to install the full repo:

```
npx skills add reakaleek/mtg-commander-deck-builder-skills
```

Find `scryfall` from the installed skill directory that contains its `SKILL.md`. Run `scripts/scryfall.py` from that folder, or pass the full path to the file. Do not search the repo and read the `.py` source. If a flag is unclear, run `--help`. Open the source only if the command fails.

Do not replace its helper with ad-hoc HTTP.

This skill may accept a deck produced by `commander-deck-builder`. It does not depend on that skill and must not rewrite the builder's file.

## Input

Accept Archidekt exports and clean quantity-plus-name lists through `scryfall`:

```
python scripts/scryfall.py parse-deck FILE
python scripts/scryfall.py collection FILE
```

Those commands live in the `scryfall` skill. Run them from that skill's directory. Do not read `scryfall.py`.

Prefer the canonical deck file when the user supplies it. The playbook is read-only. Never write that file.

If the export does not identify command-zone cards, confirm them.

Ask about player experience, desired guide depth, and any interactions they especially want explained. Reuse table rules they already stated.

## Grounding

Fetch Oracle text for every card, including all faces. Ground every interaction in that text.

Do not invent combos. Distinguish guaranteed lines from conditional synergies.

For each line, note prerequisites, resource requirements, likely interruption points, and recovery options.

## Output

Write a standalone Markdown playbook in chat. Follow [playbook.md](playbook.md).

Save it to a file only when the user asks.

Runtime card names belong in the generated playbook. Keep them out of this skill's instructions.
