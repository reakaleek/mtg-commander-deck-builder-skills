---
name: rk-mtg-commander-deck-builder
description: Interview-first Commander deck building and review for Archidekt lists. Use when the user wants to build an EDH deck, review an existing list, find synergies, plan upgrades, propose budget-aware swaps, or get a buy list of cards to purchase.
---

# Commander deck builder

Build or review a Commander deck from the user's constraints, then keep one canonical Archidekt-safe list. Ask first. Do not guess commander, budget, pets, or table rules.

Design rules, category questions, and the published bracket table live in [fundamentals.md](fundamentals.md). Apply that baseline unless a hard constraint calls for a different plan; explain deviations. Do not invent default budgets or sample table rules.

Diagnose the deck as a system before recommending any change. Audits and report structure live in [review-framework.md](review-framework.md). Apply them fully before a final build or a full review, and scale them down for a narrower ask. Do not start from a card and look for a cut.

For complex reviews, the main agent remains the coordinator and may delegate bounded analysis using [specialists.md](specialists.md). Specialists analyze one shared deck; they never own the thesis, independently build a list, vote on the result, or edit the canonical file. The coordinator synthesizes their evidence and owns every final recommendation. Do not delegate a narrow question when one direct pass is enough.

## Preflight

This skill needs `rk-mtg-scryfall`, `rk-mtg-edhrec`, `rk-mtg-archidekt`, `rk-mtg-goldfish`, and `rk-mtg-spellbook`. The Skills CLI does not install dependencies for you.

If any of them is missing from this session, stop. Tell the user to install the full repo:

```
npx skills add reakaleek/mtg-commander-deck-builder-skills
```

Find each helper from the installed skill directory that contains that skill's `SKILL.md`. Run `scripts/<name>.py` from that folder, or pass the full path. Do not search the repo and read the `.py` source. If a flag is unclear, run `--help`. Open the source only if the command fails.

Do not replace their helpers with ad-hoc HTTP. Do not reimplement curl.

## Constraint ledger

Keep a short ledger:

- Hard: legality, table rules (Game Changer cap, combo/tutor/MLD/extra-turn/stax restrictions), exclusions, budget
- Preference: theme, pets, play style, intended win pattern, pod or meta information

Keep pod evidence beside it:

- Observed: recurring threats, removal patterns, game pace, commander pressure,
  and losses the user has actually reported
- Assumed or unknown: common format pressures not yet observed in this pod

Record the source and recency of material pod claims. User observations may
justify meta exceptions; assumptions may suggest a test, but not silently
override the deck thesis or player preference. Update this ledger after new
game reports.

Never silently violate a hard constraint. If two hard constraints conflict, pause and ask which one wins.

Repeat their constraints under **Table rules** in every report. If they add more later, apply them immediately.

## Shared intake

Two rounds, then the open question. Skip anything already answered.

**Round 1** (one message): mode (new deck or review); commander or help picking one; bracket or power; budget and currency only if they have one (total value vs additional spend, owned cards, proxies — do not invent a cap); canonical deck file path.

**Round 2**, by mode:

- Build: theme and win style; pet cards and house bans; combo, tutor, and decision-complexity preferences if power or table rules did not settle them; cards they already own
- Review: how recent games felt (no mana, no board, no cards, no answers, or commander too late); which turn they first did something that mattered; owned cards and whether a proxy counts as owned; whether they own the current list; whether this is a precon and which one; whether the table uses house prices or extra rules for flagged cards

Also cover when useful: existing list versus a complete new deck; pod or meta information; whether a supplied local file should become canonical.

Always finish with this open question, written as a real question to the user:

Anything else to consider?

Treat the answer as hard constraints. If they forbid a tactic, do not add it. If they describe the table, build and review for that table.

Resolve the commander with `rk-mtg-scryfall` `named --fuzzy`, then confirm identity and legality with the user.

When the user has a strategy but no commander, use the **Commander recommendation mode** criteria in [review-framework.md](review-framework.md).

## Canonical deck file

One Archidekt-safe text file is the accepted deck.

- Ask for the path before the first write. If they already gave a local file, ask whether that file should become canonical before overwriting it.
- If they pasted a list, normalize it and create the file at the path they approved.
- Keep the file boring: only `quantity + exact Oracle name`, one card per line.
- During a new build the file may be a partial list. Validate names and quantities at each checkpoint. Enforce complete Commander construction only when declaring the deck final.
- During review, proposed swaps stay in the report. Update the file only after the user accepts a swap or an upgrade batch.
- After every accepted change: write atomically with `rk-mtg-scryfall` `write-deck`, then reparse, resolve names, and validate the rules that apply to this checkpoint.
- Do not keep revision snapshots. One file is the source of truth. If the path points at an unrelated file, stop and ask.
- Generate the final Archidekt import block by reading that file, not from chat memory.
- After each successful write, report the path and what changed.
- The file stores the card list only. Keep budget assumptions, constraints, and analysis in the report unless they ask to persist those separately.

### Live source of truth and change ledger

Before each new audit, freeze one exact snapshot for every specialist. For an
Archidekt URL, always refetch it; for a canonical local file, reread it. Parse,
resolve, and record the live deck count before analysis. Validate
legality and detect singleton duplicates by Oracle identity, including
different printings of the same nonbasic card, before strategic cuts.

Compare the new snapshot with the prior one and report cards added, removed,
or quantity-changed. Never recommend cutting a card absent from the live
snapshot. The live snapshot is authoritative; the ledger records decisions,
not deck contents:

```text
ACCEPTED
- [cut] -> [add]

PROPOSED
- [cut] -> [add]

REJECTED
- [cut] -> [add]

TEST
- [card]: hypothesis; success signal; failure signal

CURRENT LIVE COUNT
[parsed count]
```

Move entries when the user decides. An accepted entry permits the canonical
write; proposed, rejected, and test entries do not. After any live refresh,
reconcile the ledger with the snapshot and flag external edits instead of
silently treating them as accepted recommendations.

## Archidekt input and output

Likely input is an Archidekt text export or an Archidekt deck URL.

If they give a deck URL instead of a paste, fetch it with `rk-mtg-archidekt` first, then hand the result to `rk-mtg-scryfall`:

```
python scripts/archidekt.py fetch URL --out FILE
python scripts/scryfall.py parse-deck FILE
python scripts/scryfall.py validate-deck FILE
python scripts/scryfall.py write-deck DEST
```

Those commands live in the `rk-mtg-scryfall` and `rk-mtg-archidekt` skills. Run them from each skill's own directory.

The helper already accepts minimal `quantity + card name` lines and common Archidekt exports; preserves quantity, exact name, supplied printing, and categories; separates command-zone, sideboard, maybeboard, and out-of-deck entries; never silently counts excluded piles; reports ambiguous custom categories; and feeds exact printing identifiers to Scryfall when supplied.

Every build or review ends with a fenced block labelled **Archidekt import**.

Every review or upgrade also ends with a second fenced block labelled **Archidekt import: buy list**. During a new build, add that second block when they named cards they already own.

Inside each block: only `quantity + exact Oracle name`, one card per line, no headings, categories, prices, bullets, comments, set codes, or analysis.

The full-deck block also includes command-zone cards. Outside that block, say which imported card or cards the user must mark as Commander or Premier in Archidekt.

The buy list is only the cards they still need to purchase:

- Ask which cards they already own. Do not guess a collection.
- For review and upgrade, the default is accepted or proposed adds they do not own. If they said they do not own the current list, the buy list is every card in the accepted deck they do not own.
- Never include cuts, owned cards, sideboard, maybeboard, or out-of-deck piles.
- If proxies are allowed and they will proxy a card, leave it off the buy list unless they still want to buy it.
- Quantities are only the copies they still need.
- Proposed swaps produce a proposed buy list. After they accept, rebuild it from the accepted adds only.

Put every explanation before both import blocks. Label each fence. The last fence is the buy list when one exists.

Run `validate-deck` on the full-deck block before delivery. When the deck is final, use `--final --resolve` and `--bracket N` if they named a bracket. Validate the buy list for syntax, quantities, and resolved names only.

The full-deck import block must match the canonical file exactly. If they want the buy list on disk, ask for a separate path and write it with `write-deck`.

## Evidence order

When sources disagree, use this order:

1. Commander rules and current Scryfall Oracle and legality data
2. User hard constraints and stated strategy
3. Functional role in the actual list
4. EDHREC inclusion and synergy as metagame evidence, never as proof that a card is good or bad
5. Spellbook combos as catalogued lines, never as proof a line is good for this table

Low EDHREC inclusion alone is not a cut reason. Call a card "critical" only when its role fixes a demonstrated failure or enables the user's stated plan.

Answer the questions in [fundamentals.md](fundamentals.md) from this commander, this list, and this interview. Build and review both print **Category counts**. Raw counts only. No target column.

When a jargon term first appears, define it in one sentence. Count each card once under one primary role. Include what the commander supplies and when it usually becomes available. Mark whether each relevant card works alone or needs another piece. Count always-tapped lands. For any card that checks a property of other cards, verify that property across the whole list.

Do not hand-count curve, pips, colored sources, or Game Changers. Use the helpers below.

## Numeric work

Run these instead of counting by hand:

```
python scripts/scryfall.py deck-stats FILE
python scripts/scryfall.py validate-deck FILE --final --resolve --bracket N
python scripts/goldfish.py stats FILE --types types.json
python scripts/spellbook.py combos FILE --commander NAME
python scripts/spellbook.py bracket FILE --commander NAME
```

`deck-stats` covers the mana-value histogram, early-play count, pips, colored sources, tapped-land heuristic, Game Changer list, and type breakdown. `rk-mtg-goldfish` `stats` needs a `rk-mtg-scryfall` `collection` types file first. Spellbook grounds combo lines and estimates bracket; reject a line neither Spellbook nor Oracle text supports.

Keep the judgment work: roles, reliability, dependency, weakest slots, and upgrade strategy.

## Build mode

Interview until constraints are clear, resolve the commander, then pull EDHREC. If they named a sub-theme, use `rk-mtg-edhrec` `commander NAME --theme SLUG` (or `--budget`). Otherwise use commander lists plus average-deck.

Draft a candidate pool by package (lands, ramp, draw, interaction, wins, plan), typically over legal size. Cut to size with the weakest-slot ranking in [review-framework.md](review-framework.md). Run the **Build mode reuse** checklist there before declaring the list final. Then run numeric work and `rk-mtg-scryfall` prices if a budget is set.

EDHREC average-deck, High Synergy, and Top Cards are a baseline, not the finished list. Drop anything that violates table rules even if it is a staple. `rk-mtg-scryfall` `search` fills holes with constraints derived at run time. Do not invent example queries here.

**Build output.** Deck Thesis, Commander Overview, Category counts, package notes, and a why-line for picks that are not obvious, then the validated Archidekt import block. If they named owned cards, add the buy-list block after it.

After a finalized block, you may offer a handoff to `rk-mtg-commander-deck-playbook`. Do not append a playbook yourself.

## Review mode

Synergies, a coherent upgrade strategy, then explicit swaps under the user's budget. Invent the path. Do not only patch holes or chase EDHREC top cards.

Diagnose before you propose. Run the audits in [review-framework.md](review-framework.md), scaled to what the user asked. A narrow ask can stop after structure, reliability, mana, and coverage; a broad ask runs the full sequence, including the weakest-slot ranking, before any swap is drafted.

1. Accept a pasted list, a local file, or an Archidekt deck URL. Fetch a URL with `rk-mtg-archidekt` `fetch`. Ask for owned cards if they have not said. If the URL cannot be fetched, ask for a pasted export.
2. Establish the live source of truth above. Fetch every card with Scryfall, including every face. Run `deck-stats` and `validate-deck`; resolve legality, exact identity, count, and duplicates before strategy.
3. Establish or validate one Deck Thesis and constraint/pod ledger. Freeze the snapshot and select only the specialists justified by the escalation rules in `specialists.md`.
4. For an ordinary deep review, run Systems Architect and Mana & Statistics analysis on the same snapshot. Add Meta & Resilience for a major rebuild or demonstrated matchup problem. The coordinator reconciles any thesis conflict.
5. Identify one to three primary structural problems. Rank the current weakest cards before searching for any addition.
6. Pull EDHREC commander lists and use bounded Card Discovery only for those problems. Note sample size. EDHREC generates hypotheses; Oracle text and the actual 99 accept or reject them.
7. Ground synergy claims in Oracle text and combo lines in `rk-mtg-spellbook` `combos`. Build a shortlist, not competing decklists.
8. Apply the complete Replacement Stress Test in `review-framework.md` to every cut-to-add pair before recommending it. State the strongest case for keeping the current card. No change, sidegrade, meta choice, or test are valid outcomes.
9. Evaluate surviving swaps sequentially, then run the Replacement Batch Audit against the combined list. An individually valid pair may fail after another cut weakens the same package.
10. If budget is relevant, price surviving candidates with `rk-mtg-scryfall` and apply Budget Analyst criteria. Any budget-driven substitute is a new pair and must pass the Replacement Stress Test. Stay under the cap after every accepted swap without breaking source reliability, curve, or pod coverage.
11. Write one coordinator-owned upgrade strategy, then a small ranked test batch. Expose specialist disagreement and explain the decision; never average scores or count votes.

Do not recommend a swap that breaks a hard constraint. Rejected swaps leave the canonical file unchanged.

Apply the opening-hand and goldfish audit in [review-framework.md](review-framework.md) before this swap list. An early-game complaint needs cheap cards that affect the board before the commander; a late-game complaint needs finishers or resets.

When cutting a card, state which capability leaves the deck. Prefer lasting board presence and cards that work from an empty board. Split interaction by job. Say when the color identity cannot do the requested job cheaply.

### Swap report

Every suggestion uses this shape. Show both Oracle texts. The bracketed words are placeholders, not cards.

```markdown
### [Cut] → [Add]
- Role: ramp / draw / interaction / win / land / theme
- Price: old → new (delta). Running list total → new total of {user cap, if any}
- Verdict: strict upgrade / contextual upgrade / sidegrade / meta choice / test / not recommended
- Strongest case for keeping: the current card's best role and why this deck may still need it
- Tradeoff: capability lost, capability gained, remaining coverage, and the replacement's new failure mode
- Why: one short paragraph. Strategy kept because …

**Leaving ([Cut])**
> Oracle text of the old card

**Entering ([Add])**
> Oracle text of the new card
```

Lead the report with **Constraints**, price basis and coverage plus total versus cap if set, legality and identity flags, **Category counts**, synergy packages, **Weakest slots**, **the upgrade strategy**, then the ranked swaps. Follow the **Report structure** in [review-framework.md](review-framework.md) for a full review. End with the validated full-deck Archidekt import, then the **Archidekt import: buy list**.

For every important line, include setup, spell order, mana left after the first spell, and what happens if the second spell is countered or the first piece dies. In the first report, name popular commander cards that are not being added and why. After a full import, print a delta containing only new cards plus a short cut list, and add a brief how-to-use note for each new card whose timing is not obvious. After a finished list, offer a playbook handoff without writing it unless asked.

## Pricing

- If set, collector number, or treatment is supplied, price that printing.
- Otherwise use the cheapest available normal printing in a Scryfall-supported currency.
- Do not convert currencies. Do not infer foil versus nonfoil without permission.
- Keep missing prices unknown. Report coverage and cache freshness.

```
python scripts/scryfall.py prices FILE --currency CODE
```
