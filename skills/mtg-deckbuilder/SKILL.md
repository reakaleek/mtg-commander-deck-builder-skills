---
name: mtg-deckbuilder
description: "Build, review/cut, and playtest-tune Commander (EDH) decks by role counts, curve, and a land formula. Use when the user wants to build a new EDH deck, review or trim an existing list (Archidekt URL or ~/mtg/<deck>.txt), pick cuts or swaps, or report how games with a deck went."
---

# MTG Deckbuilder

Every number lives in [principles.md](principles.md). Read it before any workflow and cite it; don't restate targets from memory.

## Always first: table constraints

Before building or judging anything, establish the table rules. Check memory first, and ask only for what's missing:
- bracket / power level
- Game Changer limit
- budget cap: currency, pricing rule (e.g. cheapest print), approved exceptions
- combo rules (infinite? 2-card?)
- pod meta (what opponents play, how much removal and how many wipes)
- deck-specific notes: cards the user has vouched for, cards they dislike

Nothing pod-specific is hard-coded here.

## Ground rules

- **Never write to a deck file** without the user's explicit OK on the specific swaps. Propose first, then write only the accepted pairs.
- Present every change as **cut → add**, with: role (from principles §1), reason, and price delta in the table's currency.
- **User play experience beats stats.** If the user says a card works (e.g. a cost-reduced bomb that looks uncastable on paper), keep it and don't re-argue it. Ask before cutting a card the user hasn't commented on but that looks central to the plan.
- Only act on what the sources say (principles.md). If you go beyond them, label it as your own opinion.
- Name cards exactly (resolve via Scryfall). Never guess prices, legality or the Game Changer flag.

## Data helpers (reference by skill name)

| Need | Skill | Command |
|---|---|---|
| Load an Archidekt deck | `rk-mtg-archidekt` | `fetch <url> --out <file>` |
| Oracle text / types for tagging | `rk-mtg-scryfall` | `collection <file>` |
| Curve, pips, sources, GC list | `rk-mtg-scryfall` | `deck-stats <file>` |
| Prices | `rk-mtg-scryfall` | `prices <file> --currency <cur>` |
| Legality / GC count / singleton | `rk-mtg-scryfall` | `validate-deck <file> --final --resolve` |
| Candidates | `rk-mtg-edhrec`, `rk-mtg-scryfall` | `themes`, then `candidates <cmdr> --theme <slug> --exclude <file>`; `search --commander <cmdr> --exclude <file>` per scryfall's finding-cards guide, including its fit check |
| Combos / bracket estimate | `rk-mtg-spellbook` | `combos` / `bracket <file> --commander <name>` |
| Hand / screw-flood sanity (optional) | `rk-mtg-goldfish` | `stats <file> --types <json>` |

Plain `.txt` lists don't mark the commander, so always pass the commander name. If a helper is unavailable, say so and continue: tag from oracle text you can still get, ask the user for prices, or skip the optional checks and note what wasn't verified.

## A. BUILD

1. Ask for the commander and the table constraints (above).
2. **Define the plan** (principles §4): a log line, 2–3 steps, the commander's role, and the wincon(s). Confirm it with the user before filling slots.
3. **Fill the skeleton by role** (§1) using EDHREC theme pages, not the blended average deck (§6.1). Prefer cards that fill two roles. Fill the plan as enablers > payoffs > enhancers.
4. **Shape the curve** (§2) to the plan, and match ramp to the commander's MV (§5).
5. **Lands** via the formula (§3): run `deck-stats`, compute avgMV and the cheap count, show the arithmetic, round up. Then build the mana base per §3a and size colors with §3b (show the arithmetic): colored sources (untapped for turn-1 plays), tapped-land budget, basics for every fetch effect.
6. **Check constraints**: total price, Game Changer count, Spellbook combos against the combo rules, bracket estimate. Fix violations with same-role swaps.
7. **Run the evals** (§7) on the draft and fix failures with same-role swaps. Offer an `rk-mtg-goldfish` mana check before the user buys anything.
8. Show the list grouped by role, with counts vs. targets. After the user's OK, write an Archidekt-importable list (`1 Card Name` lines only) to `~/mtg/<deck>.txt` via `rk-mtg-scryfall write-deck`.

## B. REVIEW / CUTS

1. Load the deck (Archidekt URL → `fetch --out`, or `~/mtg/<deck>.txt`). Read `~/mtg/<deck>.log.md` if it exists, plus memory notes for this deck.
2. Run `deck-stats` and `prices`. Check budget and GC count first; constraint violations are problems before anything else.
3. **Tag every card** (§1 tags, with secondaries) from oracle text. Show the tag table compactly.
4. **Run the evals** (§7): every row, pass/fail, with the number behind each failure. They cover the §1–3 targets and the §6 traps.
5. **Name the 3–5 biggest problems**, most impactful first; break ties with §6's most-common order. Each one needs a number (e.g. "Draw 7 vs ≥12") or a failed eval/trap.
6. **Propose same-role swaps** (§5) that fix those problems: cut → add, role, reason, price delta. Prefer cuts from over-target roles, and adds that fill two roles.
7. **Recount after the proposed changes** (eval E13): show before → after for each role, the curve, the land formula and the total price, and re-run any eval that failed. Then stop and wait for the user's OK.

## C. PLAYTEST LOOP

Log file: `~/mtg/<deck>.log.md`, append-only. Create it with a `# <Deck> playtest log` header if missing.

1. The user reports a game in free text. If it's vague, ask **1–3 targeted questions**, e.g. "Did you miss land drops? By what turn?", "Which cards sat in hand uncast?", "What killed you or stalled you?"
2. **Append one entry** in exactly this format:

   ```
   ## YYYY-MM-DD — <W/L, turn, opponents if known>
   - Felt: <user's words, lightly trimmed>
   - Stars: … | Duds: … | Stuck in hand: …
   - Problems: <screw/flood, no answers, ran out of gas, too slow, …>
   - Changes made: <cut → add> (or "none")
   ```
3. **Read the whole log** before suggesting anything. Tally recurring problems and cards across entries, and show the tally.
4. **Act only on patterns**: a problem in 2+ games, or a card that disappointed repeatedly. A single flop is not a cut unless the user says so. When nothing is a pattern yet, say "no change yet" and what to watch for next game.
5. Map each pattern to a role with §7's symptom table (e.g. "ran out of gas" → Draw, "no answers" → Targeted/Mass, "screw" → lands/ramp, recomputed with §3). Propose same-role swaps as in B.6–7.
6. After the user decides, update **that entry's** `Changes made:` line with the accepted swaps (the only edit allowed to an existing entry). Then write the accepted swaps to the deck file.

## Output style

Lead with the problems and proposals, not a full card dump. Keep tables compact. Cite principles.md sections (e.g. "§5 non-stacking") rather than restating them.
