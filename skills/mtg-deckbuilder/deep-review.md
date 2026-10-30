# Deep review

An opt-in version of workflow B. Four subagents review the same deck in parallel, each from one profile, and a fifth checks the merged swap set. It costs several times a normal review, so run it only when the user asks for a deep, thorough or full review.

Every number still lives in [principles.md](principles.md). The briefs below cite sections and never restate targets.

## 1. Packet (orchestrator, before fan-out)

Run B.1–B.4 as usual, including the user's confirmation of the plan in B.3. Tag every card **once**, here: all lenses work from the same counts. Then check E1 (constraints) yourself.

Write the packet to a `deep-review/` folder in the session scratchpad (or a temp folder if there is none):

| File | Contents |
|---|---|
| `deck.txt` | the list, `1 Card Name` lines |
| `oracle.json` | `rk-mtg-scryfall collection` output: full oracle text for every card, never truncated |
| `stats.json` | `rk-mtg-scryfall deck-stats` output |
| `prices.json` | `rk-mtg-scryfall prices` output |
| `tags.md` | the B.4 tag table: one row per card, lands and basics included (`Qty` for basics), columns `Qty \| Card \| Primary \| Secondaries \| MV \| Hits` |
| `counts.json` | `scripts/role_counts.py tags.md --commander <name> --stats stats.json`. Every count in the packet comes from here; don't sum by hand. Its `avg_mv_nonland_excl_mdfc` is the §3 avgMV (deck-stats' average includes the commander and MDFCs), and `land_formula` is the §3 result |
| `archetype.json` | the B.3 `rk-mtg-edhrec archetype-match` output |
| `context.md` | the commander and its full oracle text; the B.1 play-experience answers (cards that win games, what kills the deck, how the table treats it); the plan as the user confirmed it in B.3 (archetype or hybrid, log line, steps, commander role, early/late-weak guess); table rules from `~/mtg/AGENTS.md`; this deck's notes (vouched and disliked cards); any conflict between sources of table rules (e.g. a playbook header vs the rules file), keeping the user's rules file and flagging the rest; E1 result and any violation; the full `~/mtg/<deck>.log.md` if it exists |

## 2. Fan-out

Spawn all four lenses **in one message** so they run in parallel. Give each one the shared preamble, its own brief, and the absolute paths of the packet, `principles.md`, `archetypes.md` and `scripts/role_counts.py`. Each eval has exactly one owner; the orchestrator keeps E1 and E13.

| Lens | Reads | Owns |
|---|---|---|
| Mana & curve | §2, §3, §3a, §3b | E9 E10 E11 E17 E18 E19 |
| Vegetables & interaction | §1, §1a | E6 E7 E12 E16 E24 E25 E26 E27 |
| Plan & synergy | §4, §5, §6, archetypes.md | E2 E3 E4 E5 E15 E20 E22 E28 |
| Opponent at the table | §4, §1a, §7 symptom table, the deck's archetypes.md block | E8 E14 E21 E23 |

If the Agent tool isn't available, run the briefs one after another inline, in this order, and tell the user.

### Shared preamble (every lens)

```
You are one lens in a parallel Commander deck review. Read the packet in <packet dir>
(deck.txt, stats.json, prices.json, tags.md, counts.json, archetype.json, context.md) and the sections of
<principles.md> named in your brief. principles.md holds every target; cite its
section and eval numbers, and don't use targets from memory.

Rules:
- Use tags.md and counts.json as given. If you disagree with a tag, list it under
  "Disputed tags"; don't recount with your own tags. For any other count, run
  <role_counts.py> rather than summing by hand.
- Judge only your own evals. Mention something outside them only if it is severe,
  in one line under "Outside my lens".
- Cards the user vouched for in context.md are not cut candidates. The playtest log and
  the B.1 play-experience answers outrank the targets (principles intro).
- Read each card's full oracle text in oracle.json before tagging, judging or cutting it.
- Don't write or edit any file. Resolve any card you suggest via rk-mtg-scryfall;
  never guess names, prices or the Game Changer flag.

Return exactly these sections, in Markdown:
1. Evals: table `# | pass/fail | number behind it` for every eval you own.
2. Problems: claim · number · eval · severity (3 = costs games, 1 = polish).
3. Cut candidates: card · role · why · interaction with the commander's text (one line,
   or "none"). A card that multiplies or protects the commander's engine is not a cut
   candidate; list it under "Central to the plan" instead.
4. Needs: role plus constraints, e.g. "Targeted, MV ≤ 2, hits enchantments, white".
5. Suggested adds (optional): card · role it fills · price.
6. Disputed tags / Outside my lens (only if any).
```

### Mana & curve

```
Your lens: mana and curve. Read §2, §3, §3a, §3b. Own E9, E10, E11, E17, E18, E19.
Show the land-formula arithmetic (avgMV, cheap, MDFC credit) and the §3b source math
for each color's most demanding card, partial credits applied. For E10, run at least
3 goldfish games with rk-mtg-goldfish, or say they weren't run. Flag any tapped land
without a named upside.
```

### Vegetables & interaction

```
Your lens: the vegetables and the disruption package. Read §1, §1a. Own E6, E7, E12,
E16, E24, E25, E26, E27. Classify the deck early-weak, late-weak or both from the plan
steps in context.md before judging timing. Show the Targeted split by what it hits,
after §1a's shifts for Mass coverage, goad and creature count. Name the permanent
types that stop this deck's plan and how many answers each has.
```

### Plan & synergy

```
Your lens: the game plan. Read §4, §5, §6, and the block in <archetypes.md> for the
archetype in context.md. Own E2, E3, E4, E5, E15, E20, E22, E28.
Count enablers, payoffs and enhancers (multipliers that aren't the plan's payoffs
count as enhancers). For E28, count each part the archetype block lists against its
parts rule, check its floors, and its contention themes and weak points. List
non-stacking effects with copy counts. Name any payoff groups in contention and any
off-plan package, using the `exclusive` cards in archetype.json as evidence after
reading them. For each cut candidate, say which same-role card would replace it (§5);
for a missing part, find adds with rk-mtg-edhrec `tag <slug> --colors <deck colors>
--exclude <deck.txt>` and check each against the commander's text.
```

### Opponent at the table

```
Your lens: you are the other three players. Read §4 (resilience, rebuild, build for
being behind, hide the finish), §1a, the §7 symptom table, and the pod meta and
bracket in context.md. Own E8, E14, E21, E23.
Play three archetypes that fit the bracket against this list: fast aggro or Voltron,
control with wipes, and a value engine or combo deck. For each, say:
- how it beats this deck, and on roughly which turn;
- which of this deck's cards it answers first, and why that card;
- the common hate piece or wipe that hurts most, and what this deck has left after it.
  Start from the "Weak to" line of the deck's archetypes.md block.
Every finding maps to an eval number or a §7 symptom row. No free-floating opinions.
```

## 3. Merge (orchestrator)

1. Assemble one 28-row eval table: your E1, the lenses' rows, E13 pending. If a lens skipped an owned row, run it yourself.
2. Resolve disputed tags. If one changes a count, recheck the rows that depend on it yourself.
3. Dedupe problems across lenses and rank the top 3–5 as in B.6: impact first, then §6's most-common order. A problem raised by two lenses usually outranks one raised by one.
4. **Resolve conflicts** before building swaps:
   - A card any lens lists as "Central to the plan" (it multiplies or protects the commander's engine) is not cut, even if another lens names it; ask the user if you still think it should go.
   - A card one lens cuts and another counts on (e.g. a 5-drop that is one of two enchantment answers): keep it, or replace it with one card that fills both roles (§5).
   - Two lenses wanting the same slot: the higher-severity problem gets it.
   - An add that breaks another lens's eval (curve, colors, budget): drop it or find one that doesn't.
5. Build swaps per B.7: cut → add, reason, price delta. A swap is same-role, or moves a slot from an over-target role to an under-target one (B.7). A cut from a role that is already under target needs a named eval reason (e.g. E17 for a hard-cast 6-drop) and is shown to the user as a conflict.
6. Recount with `role_counts.py --cut … --add …` and put its before → after numbers in the swap set you hand the verifier.

## 4. Verify

Spawn one verifier with the packet paths, `principles.md`, and the proposed swap set:

```
You check a proposed change set for a Commander deck. Read the packet in <packet dir>
and <principles.md>. Apply these swaps: <cut → add list>.
- Recount (E13) with <role_counts.py> --cut/--add, checking the tags it gives each
  added card against oracle text: every §1 role, the curve, the §3 land formula with its
  arithmetic (`land_formula` before → after), the §3b sources for any color a swap touched, total price and Game
  Changer count against context.md.
- Re-run every eval in <failed evals> and every eval that touches a changed card.
- Check no swap cuts a vouched card or adds a disliked one, and each is same-role (§5)
  or moves a slot from an over-target role to an under-target one (B.7).
- For every cut, read the card's oracle text against the commander's: flag any cut that
  multiplies or protects the commander's engine (pumps its power, adds counters, copies
  its triggers, protects it) unless the swap set names that interaction and the user's OK.
Don't write any file. Return only discrepancies: what you expected, what the swap set
claims, and the number. Return "No discrepancies" if there are none.
```

Fix what it finds. Then present as in B.6–B.8, adding one line per lens conflict you resolved and how. Stop and wait for the user's OK.
