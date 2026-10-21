# Deckbuilding principles

The single source of truth for every number the skill uses. SKILL.md never repeats these.

Sources: **V1** Command Zone #767 "Stop Falling for these Commander Deckbuilding Traps" ·
**V2** Command Zone #658 "Commander Deckbuilding Template for the New Era" ·
**V3** Commander Challenge "How to Win at Commander Every Time" ·
**TCG** TCGplayer "How Many Lands Do You Need in Your Deck? An Updated Analysis" (2022, Karsten regression) ·
**DS** Draftsim "MTG Mana Curve" (David Royale, 2026).

All targets are starting points for an untested deck. Once the user has played it, their experience wins (V2: "trust yourself after you've played it").

## 1. Skeleton: role targets (V2)

| Role | Target | Counts | Does not count |
|---|---|---|---|
| Lands | formula, §3 | lands, MDFC lands, channel lands; 1-mana landcyclers optional | |
| Ramp | 10 (12 with a 4-MV commander or ramp-matters plan) | dorks, rocks, land ramp: permanent extra mana | rituals, one-shot treasure bursts, cost reducers (tag them `Enabler`) |
| Card advantage | ≥12, more is fine | net more cards: draw-2+, repeatable draw engines, impulse draw, Land Tax | cantrips, looters/rummagers, "draw extra when you draw" enhancers, scry; self-mill counts ⅔ and only in decks that play from the graveyard |
| Targeted disruption | 12 | 1-for-1 answers: removal, counters, bounce, land destruction, single-target graveyard exile, tappers | your own protection spells |
| Mass disruption | 6, split ~2–3 creature wipes, ~1 artifact/enchantment sweeper, ~1 graveyard hate | wipes, one-sided wipes, fogs, Teferi's Protection-style, Propaganda/tax pieces, mass graveyard hate | |
| Plan | ~30 | enablers > payoffs > enhancers; protection and recursion count as enablers | |

- These total 108 on purpose. Cards that fill two roles are what make it fit. An MDFC or channel land counts **fully** in both its land role and its spell role (V2).
- A modal card (Cyclonic Rift, Vandalblast) goes in **one** bucket, chosen by how you normally cast it. Don't count it twice (V2).
- Tags (one primary, plus optional secondaries): `Land` `Ramp` `Draw` `Selection` `Targeted` `Mass` `Protection` `Enabler` `Payoff` `Enhancer` `Wincon`.
  `Selection` (looting, cantrips, tutors, self-mill outside graveyard decks) is tracked but never counts toward Draw. V3 counts it more broadly; V2's strict definition keeps real draw from being overstated.
- Protection has no target number; no source gives one. It is capped by the redundancy rule in §5.

## 2. Curve (V2, DS)

- Nonland target, 62 cards: **1 MV: 9 · 2: 18 · 3: 15 · 4: 10 · 5: 5 · 6+: 5** (V2). Two should be the largest slot; if it isn't, look for cheaper versions (V2).
- Keep 6+ drops to about 5, and every expensive card must be great when it resolves (V1, V2). Five-drops are awkward; the good ones are flexible instants or bombs (V2).
- Shape follows the plan (DS): aggro is ladder-shaped, midrange is a triangle, control peaks late. **Ramp or cheat-into-play decks** look like an oval: heavy 1–3 MV ramp, a thin middle, and more 5+ payoffs. That is the one accepted reason to exceed the 6+ cap.
- Judge the curve by **effective** cost. Cost reducers, convoke and cheat effects can make a high-MV card cheap in practice (DS). The land formula still uses printed MV (§3).
- If a curve peaks at 3 (DS: Commander games run long), flag it, but it is not a fault when the 3s are the plan's engines. Default to V2's peak at 2.

## 3. Land count (TCG)

```
lands = 31.42 + 3.13 × avgMV − 0.28 × cheap
```

- `avgMV`: average printed MV of the nonland cards in the 99. Exclude the commander and land/spell MDFCs.
- `cheap`: nonland cards with MV ≤ 2 that draw cards or produce or fetch mana. Fixing-only ramp still counts if it is ≤ 2 MV, but it does not reduce lands beyond that (DS).
- Count MDFCs toward the land total as **0.38** each, or **0.74** if mythic (TCG). (V2 counts them as full lands, DS as ⅓; TCG is measured and newest.)
- Fine-tune: efficient or reliable cheap pieces (1-mana draw, rocks, land search) cut about one land per 2–3; fragile ones (dorks, 2-mana cantrips) cut one per 4–5 (TCG).
- If several big cards are normally cast via self-reduction, warp or evoke, also show the result using their usual cost. Mana value can misstate a card's real mana appetite in either direction (TCG, DS). Present both numbers and let play experience pick.
- The model's error is about ±2.75 lands. Push the count up for 3+ colors, heavy pips, or many utility lands (TCG). Round **up**, because everyone cuts lands (V1, V2).
- Sanity check: V2's template curve (avgMV ≈ 3.0) with 10 cheap pieces gives 38.0. Typical results land between 37 and 40 (V2, DS).
- Mana base: colored sources must match colored pips (V3, DS; use deck-stats `color_requirements`). Run enough basics for every fetch and land-search effect (V1).
- Reference odds at 38 lands: 3+ lands in the opening 7 is 54.8%; 2+ is 82.8% (V2).

## 4. Game plan (V1, V2, V3)

- **Log line**: one sentence of what the deck does, plus how it wins. No nameable wincon means no plan yet (V1, V3).
- **Two steps, three at most.** Step 1 must be good on its own (e.g. "lots of creatures"). Step 3 is gravy, never required (V1).
- **Commander role** (V2): payoff commander → the deck is mostly enablers. Enabler commander → protection and haste, and room for more payoffs. Enhancer commander → as many enablers as possible.
- **Enablers are the biggest plan bucket**, about 25–30 cards that start the plan (V1). Enhancers: only the best 4–5 (V2).
- **Resilience** (V3): build the plan around not losing. Layer resilience into the plan's own cards: lifegain, threats on artifacts or enchantments, recursion, land ramp (lands rarely die). A "layer" that needs its own package is a side plan (V1 trap).
- **Survives losing the commander?** Count how many cards go dead if the commander is answered (V1).
- **Instant speed** (V3): prefer modal, instant-speed and activated options so decisions can wait until the end step before your turn.
- **Clear win check** (V3): goldfish to the target win turn and ask: can I win? Is there a card that would win from here? Is there enough value on board? Is there enough draw to find the wincon? If not, add wincon density or on-plan draw.

## 5. Cuts and replacements (V1, V2)

- **Swap within a role**: removal for removal, enabler for enabler. Never cut a land, ramp, draw or disruption card to fit a payoff (V1).
- A card that fills two roles is the best replacement: it keeps a role and adds one (V1).
- **Recount the whole deck after every batch** of changes. Many single-card edits drift the numbers (e.g. 34 lands, 6 removal) (V1).
- Cut order when over 99: (1) bring 6+ drops down to the cap; (2) cut excess non-stacking effects; (3) cut off-plan cards; (4) lands and draw last (V1, V2).
- **Non-stacking effects** (Crucible-style, fogs, evasion granters, one-shot finishers like Craterhoof): run about 3–5. Over ~25 cards seen: 3 copies is 59% to see one; 5 copies is 77% to see one and 37% to see two; 7 copies is 88% to see one but 57% to see two, which is too many. More draw lowers the count needed (V1).
- Ramp must fit the commander's MV: 2-MV ramp for a 4-MV commander, 3-MV ramp for a 5-MV commander, and with a 2–3-MV commander use 1-MV ramp or 3-MV ramp that brings extra value (V1, V2, DS). Cheaper is better. Big rocks need a reason: an expensive commander, X spells, or colorless payoffs (V1).
- Draw needs a mix: cheap instant draw to hit land drops, plus engines for the late game. Seven-mana draw doesn't fix early screw (V1).

## 6. Traps checklist (V1 unless tagged)

1. EDHREC average deck copied blindly: it mixes themes. Use theme pages and check every card.
2. Plan too complex (more than 3 steps).
3. Trying to do too much: payoffs in contention (hoard vs. sacrifice, Craterhoof vs. Blood Artist), side plans splashed in.
4. Hyper-focused: one hate piece shuts it off, or your answers share the weakness (all removal on ETB creatures).
5. Only late, expensive interaction; there is no cheap early removal.
6. Hedging against silver bullets the pod never plays.
7. Single-card edits without a recount.
8. Enablers cut for payoffs or enhancers.
9. Too little draw, or only expensive draw.
10. Ramp mismatched with the commander's MV.
11. High or awkward curve (too many 5s, 6+ over the cap). The opposite, too many cheap cards, runs out of gas (DS).
12. Too few lands or basics. Too many lands floods (DS).
13. Not goldfishing.
14. Tuned past the pod's power level.
15. Colored sources short of pips (V3, DS).
16. No clear way to win (V3).
