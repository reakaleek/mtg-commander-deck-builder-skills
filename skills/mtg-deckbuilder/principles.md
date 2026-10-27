# Deckbuilding principles

The single source of truth for every number the skill uses. SKILL.md never repeats these.

Sources: **V1** Command Zone #767 "Stop Falling for these Commander Deckbuilding Traps" ·
**V2** Command Zone #658 "Commander Deckbuilding Template for the New Era" ·
**V3** Commander Challenge "How to Win at Commander Every Time" ·
**TCG** TCGplayer "How Many Lands Do You Need in Your Deck? An Updated Analysis" (2022, Karsten regression) ·
**DS** Draftsim "MTG Mana Curve" (David Royale, 2026) ·
**SV** ScrollVault "MTG Manabase Guide — Frank Karsten Math 2026" (Karsten's hypergeometric source counts plus ScrollVault's Monte Carlo runs) ·
**K22** Frank Karsten "How Many Sources Do You Need to Consistently Cast Your Spells? A 2022 Update" (TCGplayer/ChannelFireball, 2022) ·
**V4** YouTube gjS2jb5j_Xs "8 deckbuilding secrets" (a creator with 500+ Commander decks; their own experience, not measured data).

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
- Plan tags (V1): **Enabler** is the action the plan feeds on (the instant you cast, the card that makes two goblins). **Payoff** rewards it ("whenever you cast…, draw"; "goblins get +1/+1"). **Enhancer** multiplies it ("double it", "deal 3 instead"). A big spell that scales with the theme is still a payoff.
- Targeted disruption should include cheap answers (MV ≤ 2, ideally 1) that slow a threat before it snowballs, not only answers for when you are about to die. Treat removal as slowing opponents down, not stopping them. The best turns develop your board and remove something in the same turn (V1).
- Protection has no target number; no source gives one. It is capped by the redundancy rule in §5.
- **Why these counts** (V2, hypergeometric): 10 ramp is 54% to have one in the opening 7 and 63% by turn 2; 12 is 70.4% by turn 2. Reliably having 2-MV ramp on turn 2 takes 14–15. The same 70.4% is why Targeted is 12: the point is having one in hand when it's needed, so a card that hits several permanent types still counts once.
- **Ramp is the most overrated vegetable** (V2): a 2-MV land ramp spell is only ramp if you also hit every land drop, so prefer more lands over extra 2-MV ramp. Go to 12 when a 4-MV commander wants turn-2 ramp. Go lower with a 2–3-MV commander or a very cheap curve. cEDH uses 0–1-MV ramp and different numbers.
- **Draw borderline cases** (V2): Sylvan Library counts only if you will pay life with it. Mindstone and Sensei's Divining Top only replace themselves, so they don't count. The lower your card quality or the more specific pieces the plan needs, the more draw it needs. Run 15 if you can; draw makes up for being short in other roles.
- **Mass vs. Targeted** (V2): it's Mass if after casting it you are at card parity or better against **each** opponent (Grasp of Fate-style one-per-opponent counts). It's Targeted if any opponent comes out a card ahead. Fogs, Teferi's Protection-style effects, and static taxes or "enters tapped" pieces are Mass because they disrupt a whole turn. A deck heavy in Mass explains why opponents dislike playing against it.
- Tag by hand rather than trusting an auto-tagger; sorting cards yourself shows how the deck works and which cards fill two roles (V2).

## 2. Curve (V2, DS)

- Nonland target, 62 cards: **1 MV: 9 · 2: 18 · 3: 15 · 4: 10 · 5: 5 · 6+: 5** (V2). Two should be the largest slot; if it isn't, look for cheaper versions (V2).
- Keep 6+ drops to about 5, and every expensive card must be great when it resolves (V1, V2). Five-drops are awkward; the good ones are flexible instants or bombs (V2).
- **Use all your mana every turn** (V1). The player who spends the most mana over a game tends to win. Unspent mana means a weaker turn: spending 4 on turn 6 is a turn-4 turn, and the gap compounds. Cheap cards fit together like Tetris pieces (six mana = two 2s, a 1 and a 1), while a hand of 4-drops strands mana. The limit: a deck of only 2-drops runs out of cards and can't close, so keep a few high-impact cards and back them with cheap ramp and removal you can hold up beside them.
- Shape follows the plan (DS): aggro is ladder-shaped, midrange is a triangle, control peaks late. **Ramp or cheat-into-play decks** look like an oval: heavy 1–3 MV ramp, a thin middle, and more 5+ payoffs. That is the one accepted reason to exceed the 6+ cap.
- Judge the curve by **effective** cost. Cost reducers, convoke and cheat effects can make a high-MV card cheap in practice (DS). The land formula still uses printed MV (§3).
- If a curve peaks at 3 (DS: Commander games run long), flag it, but it is not a fault when the 3s are the plan's engines. Default to V2's peak at 2.
- What fills each slot (V2):
  - 0: almost none in casual.
  - 1: mostly ramp and targeted disruption.
  - 2: ramp, enablers and efficient creatures. The typical turn 3 is two 2-drops, or a 2-MV rock into a 4-drop.
  - 3: where engines start.
  - 4: powerful engine permanents.
  - 5: awkward; keep only flexible, usually instant-speed effects. Big sorcery-speed plays on turns 5–6 run into the turns when board wipes are most likely.
  - 6: modal spells, one-sided wipes and finishers. 6+ permanents only when they are cheated in, cost-reduced or reanimated.
  - 7+: haymakers that win on the spot, or leave value behind even if answered.
- Thin out the slot at the commander's MV; that turn is usually spent casting the commander (V2). Partner commanders change the math.

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
- Mana base: colored sources must match colored pips (V3, DS; use deck-stats `color_requirements`). Run enough basics for every fetch and land-search effect (V1). Details in §3a.
- Cross-check (SV Monte Carlo): typical Commander decks land at 35–38; battlecruiser decks (avgMV 3.5+, ~8 ramp) want 38–40; cEDH with heavy fast mana runs 29–31. If the formula disagrees with this by more than ~2, recheck avgMV and `cheap`.
- Rocks and dorks don't replace lands: they fix and accelerate but don't help hit land drops, and dorks die to removal (SV, V2).
- Reference odds at 38 lands: 3+ lands in the opening 7 is 54.8%; 2+ is 82.8%; about 75% to see a 3-land hand with the free mulligan (V2). V2 calls 38 "greedy": Karsten's 60-card math adapted to Commander gives about 43.
- Push lands up when the deck wants to mulligan for a specific piece (e.g. a turn-2 attack trigger): each mulligan for lands is one fewer for the piece (V2).
- Two-land keeps compound the risk: they make the 4th and 5th drops unlikely too, even with ramp in hand (V2). Play MDFCs as lands first; the spell side is for when you have spare lands (V2).
- A missed land drop can't be made up: you are a mana behind on every later turn, and ramp after a miss only pays to catch up (V1). V1's flat starting point is 38, counting MDFCs, channel lands and 1-mana cyclers. cEDH (bracket 5) uses different math (V1).

## 3a. Mana base: colors and land quality (SV)

- **Colored sources:** size each color to its most demanding card, not to its average pip share. Use the 99-card table and counting rules in §3b. A turn-1 single pip needs 19 sources, and a turn-2 double pip needs 30.
- Colorless utility lands count for no color. Rainbow lands (Command Tower-style) count fully for each color they make. Rocks, dorks and ramp spells count only partially (§3b).
- **Untapped vs. total.** For turn-1 plays only untapped sources count. From turn 2 on, Karsten counts tapped sources too, as long as the tapped-land count stays reasonable (K22).
- **Tapped lands:** 4–6 is acceptable in Commander; each tapped land costs a full mana on the turn it enters. Each one needs an upside (a third color, scry, a basic land type that fetches can find, a spell side). A plain tapped dual with no upside is the first cut for a basic or an untapped dual.
- **Land quality order:** fetch lands (they find any land with the right basic type, including typed duals) > shock lands > pain, fast and other untapped duals > check lands (weaker in Commander because there are fewer basics with the right type) > tapped duals.
- **Build order:**
  1. Count pips per color.
  2. Set the land count (§3).
  3. Fill the best duals first.
  4. Verify source counts per color.
  5. Trim tapped lands to the budget.
  6. Add utility lands last, only once color math passes.
- **Three or more colors** without real fixing (fetch, shock, triome-class) won't be consistent. Add fixing or reconsider the color count.
- **By plan:** an aggro or fast plan wants no tapped lands in its first few drops. Midrange values color consistency over speed. Combo plans run more lands than feels right, because a missed drop delays the combo turn into the opponents' interaction.
- **Test it:** goldfish 50+ opening hands, or run a Monte Carlo check (`rk-mtg-goldfish`) before trusting the mana.

## 3b. Karsten's colored-source math (K22)

**The model.** A card with mana value M and N pips of one color is "consistently castable" when:

```
P( ≥ N sources of that color by turn M  |  ≥ M lands by turn M )  ≥  (89 + M)%
```

- The target slides with cost: 90% for 1-drops, 91% for 2-drops, … up to 96% for 7-drops. Missing colors for a game-changing top-end card hurts more than missing them for a 1-drop.
- Probabilities are **on the play** and **conditional on hitting the land drops**. Games where you drew too few lands are thrown out, because that's a land-count problem (§3), not a color-ratio problem.
- It's computed by simulation over millions of games. Each game shuffles a deck of on-color sources, other lands and spells, applies mulligans, and draws to turn M. If at least M lands were drawn, the game counts as a success when at least N of them are on-color, otherwise as a failure. The answer is the smallest source count where successes / (successes + failures) meets the target.
- **Commander assumptions:**
  - 99 cards with 41 lands, treating rocks as partial lands.
  - Free first mulligan and a draw on turn 1 (CR 103.4c, 800.7).
  - London mulligan:
    - The free 7 is shipped with 0, 1, 2, 6 or 7 lands.
    - A normal 7 is shipped with 0, 1, 6 or 7 lands.
    - A 6 is shipped with 0, 1, 5 or 6 lands after bottoming.
    - A 5 is shipped with 0, 1 or 5 lands after bottoming.
    - Bottoming aims at about 3 lands, putting off-color lands on the bottom first.
  - Only lands make mana, with no card selection. The adjustments below correct for both.

**99-card table** (sources of that color; C = one colored pip):

| Cost | Sources | Cost | Sources | Cost | Sources |
|---|---|---|---|---|---|
| C | 19 | CC | 30 | CCC | 36 |
| 1C | 19 | 1CC | 28 | 1CCC | 33 |
| 2C | 18 | 2CC | 26 | 2CCC | 30 |
| 3C | 16 | 3CC | 23 | 3CCC | 28 |
| 4C | 15 | 4CC | 22 | 4CCC | 26 |
| 5C | 14 | 5CC | 20 | CCCC | 39 |
| | | | | 1CCCC | 36 |

For 6+ MV with one pip, use the 5C row; the target there is already 94%.

**Adjusting for land count.** The table assumes 41 lands. For a different count, scale it: `needed ≈ table × (your lands ÷ 41)`. Karsten's own phrasing is "18/25 of your lands should be blue". Count each 3–4 cheap draw or ramp spells as about one land in that land total. Fewer lands → fewer sources needed; more lands → more.

**Special costs**
- **Gold cards:** check each color alone, treating the other color's pips as generic, and add **+1**. Then check all the colored pips together as one color, also +1; that count is sources making *either* color. Example: `{1}{W}{U}` is 2C for W (18 + 1 = 19), 2C for U (19), and 1CC for W-or-U (28 + 1 = 29). Skip the +1 when one color is a splash in a deck whose every land makes the main color.
- **Hybrid:** sources of either color count together.
- **Convoke, delve, X spells and cost reducers:** use the lands you actually expect to tap (e.g. treat a 6-MV convoke card as `{1}{G}{G}`).
- **Alternate costs:** ignore the hard cost if you rarely pay it. If you sometimes pay it, being a few sources short is tolerable.
- **Colorless-specific (`{C}`) and snow costs** are colors of their own.

**Counting sources (partial credit)**

| Source | Counts as | Only for spells of |
|---|---|---|
| Basic or dual land, fetch that can find the color, Command Tower-style land | 1 of each color it can make | any MV (tapped ones from turn 2) |
| Fabled Passage-style fetch or Pathway | 1 in two-color decks; ⅔ of each color in 3+ colors | any MV |
| Land/spell MDFC | 0.8 (mythic: 1) of its color; the land count still uses 0.38/0.74 (§3) | any MV |
| Mana dork (if castable on turn 1) | ½ of each color | MV ≥ 2 |
| Mana rock | ¾ of each color | MV ≥ 3 |
| 2-MV land ramp (Rampant Growth-style) | ¾ of each color it can find | MV ≥ 3 |
| 3-MV land ramp (Cultivate-style) | ½ of each color it can find | MV ≥ 5 |
| Cheap cantrip (≤ 2 MV, castable on curve) | (lands of that color ÷ deck size), rounded down | MV ≥ 2 |
| Cheap scry 1 / scry 2, with 30 lands of the color in 99 | 0.2 / 0.3 | MV ≥ 2 |
| Cheap scry 1 / scry 2, with 15 lands of the color in 99 | 0.1 / 0.15 | MV ≥ 2 |
| Each Treasure from a cheap generator | ¼ of any color | MV ≥ 3 |
| Exotic Orchard / Fellwar Stone | ¾ / ½ of any color (1 / ¾ if an opponent's color is known) | as land / rock |

- Count at most 10 draw effects toward sources; the benefit diminishes after that.
- Ignore fixing that only works once you're already winning (Fires of Invention-style).
- The turn-1 row (C) counts **untapped** sources only.

**Tapped lands** (K22, 60-card guidance; §3a has the Commander budget). Avoid vanilla tapped duals. A conditional land, like a check land, counts as about ¼ of a tapped land.

**Worked example.** 38 lands, with the most demanding green card `{1}{G}{G}` (table 28). Scale: 28 × 38/41 ≈ 26 green sources. Credit for that 3-MV card: 4 Rampant Growth-style ramp × ¾ = 3, plus 2 green rocks × ¾ = 1.5, so ≈ 4.5. Green lands needed ≈ 21.5, round up to **22**. A `{G}` 1-drop (table 19, scaled ≈ 18) gets no nonland credit and needs 18 *untapped* green sources. The larger of the two numbers binds.

**Relation to `deck-stats color_requirements`.** It runs the same conditional hypergeometric check, with three differences:
- It uses a flat target with no mulligans and no free Commander draw, so it is stricter than the table (most at turn 1). It is also lenient for 4+ MV cards, which the sliding target holds to 93–96%.
- It counts land sources only; `nonland_producers_not_counted` lists the rest. Apply the partial credits above by hand.
- It ignores hybrid and Phyrexian pips and doesn't apply the gold +1.

When the helper and the table disagree, quote the table and show the arithmetic.

## 4. Game plan (V1, V2, V3)

- **Log line**: one sentence of what the deck does, plus how it wins. No nameable wincon means no plan yet (V1, V3).
- **Two steps, three at most.** Step 1 must be good on its own (e.g. "lots of creatures"). Step 3 is gravy, never required (V1). Each extra step can be disrupted and costs turns to rebuild. A deck that only works when everything goes right is a fault; one that can occasionally do it is fine (V1).
- Step 1 gets the most support because it is needed on turns 2–3. Payoffs are steps 2–3, needed around turns 4–5, so fewer copies suffice (V1). About 80–85% of the deck should serve the steps (V1).
- **One direction.** Card slots are limited, so every side plan weakens the main one. Watch for themes that look the same but pull against each other (hoard clues vs. sacrifice clues, go-wide pump vs. sacrifice drain, counters vs. sacrificing their holders). Keep the shared core (e.g. "an artifact enters") and commit to one side (V1).
- **Commander role** (V2). Payoff commander (e.g. "whenever a ninja deals damage"): the deck is mostly enablers, with only ~2 extra payoffs. Enabler commander (the commander *is* the plan, e.g. Kaalia): protection and haste count as enablers; V2's example runs 8–10 enablers and 15–18 payoffs. Enhancer commander (e.g. an attack-trigger doubler): as many enablers as possible (25+ triggers), and at most 1–2 extra enhancers, which are win-more.
- A plan-specific floor applies even when the commander helps: a spells deck needs 25–30 instants and sorceries before spell payoffs work (V2).
- **Enablers are the biggest plan bucket**, about 25–30 cards that start the plan (V1). Enhancers: only the best 4–5 (V2).
- **Resilience** (V3): build the plan around not losing. Layer resilience into the plan's own cards: lifegain, threats on artifacts or enchantments, recursion, land ramp (lands rarely die). A "layer" that needs its own package is a side plan (V1 trap).
- **Rebuild after a wipe** (V4): a full hand, a ramp lead, recursion and key pieces at MV ≤ 3 let the deck redeploy within a turn or two. Key pieces that aren't creatures dodge most wipes: removal gets scarcer from creature → artifact → enchantment → planeswalker → land, and vehicles or permanents that aren't creatures on opponents' turns dodge creature wipes. Cheap fodder means blocking doesn't cost an engine piece.
- **Survives losing the commander?** Count how many cards go dead if the commander is answered (V1).
- **Instant speed** (V3): prefer modal, instant-speed and activated options so decisions can wait until the end step before your turn.
- **Clear win check** (V3): goldfish to the target win turn and ask: can I win? Is there a card that would win from here? Is there enough value on board? Is there enough draw to find the wincon? If not, add wincon density or on-plan draw.

## 5. Cuts and replacements (V1, V2)

- **Swap within a role**: removal for removal, enabler for enabler. Never cut a land, ramp, draw or disruption card to fit a payoff (V1).
- A card that fills two roles is the best replacement: it keeps a role and adds one (V1). Every deck needs three things: card advantage, ramp (or cheating costs) and payoff. A card that does all three is the strongest pick, and a commander that does all three lets the 99 run cheap, plain cards (V4).
- **Score cards for four players** (V4). "Each opponent" and "on an opponent's turn" triggers fire 3× as often as in 1v1. Symmetric "any player" triggers fire only 2× as often. Rhystic Study and Smothering Tithe are staples for this reason. Attack triggers and effects that only work on your own turn fire once per four turns. That's a penalty, not a cut (Sol Ring scales badly too). Between two cards in the same role, prefer the one that scales.
- **Recount the whole deck after every batch** of changes. Many single-card edits drift the numbers (e.g. 34 lands, 6 removal) (V1).
- Cut order when over 99: (1) bring 6+ drops down to the cap; (2) cut excess non-stacking effects; (3) cut off-plan cards; (4) lands and draw last (V1, V2).
- **Non-stacking effects** (Crucible-style, fogs, evasion granters, one-shot finishers like Craterhoof, 7-drops): run about 3–5. Test: if a second copy in hand is dead, the effect doesn't stack. Over ~25 cards seen (8-turn game): 3 copies is 59% to see one; 5 copies is 77% to see one and 37% to see two; 7 copies is 88% to see one but 57% to see two, which is too many. More draw lowers the count needed. Self-mill decks with recursion need only 2–3. Replace extras with draw or with cards that fill two roles (V1).
- Ramp must fit the commander's MV: 2-MV ramp for a 4-MV commander, 3-MV ramp for a 5-MV commander, and with a 2–3-MV commander use 1-MV ramp or 3-MV ramp that brings extra value (V1, V2, DS). Cheaper is better: over an 8-turn game a 2-MV rock makes one more mana than a 3-MV one (6 vs. 5), and 2s chain into 2s and 4s (V1). Big rocks need a reason: an expensive commander, X spells, a storm turn, many colorless 3-drops, or enough draw to deploy several cards a turn while holding up mana (V1).
- Draw needs a mix: cheap instant draw to hit land drops, plus engines for the late game. Seven-mana draw doesn't fix early screw. Passive engines are best because they help you recover without spending a turn on it. Draw is the one effect that never stops stacking: err above the target, not below. Two extra draw spells can replace one enabler and one payoff, and you will still see those roles more often (V1).
- **Narrow answers** (e.g. "can't be forced to sacrifice") earn a slot only if the threat is common in the pod or hits this deck's own weak point (Voltron vs. edicts). Losing to a rare silver bullet is acceptable (V1).

## 6. Traps checklist (V1 unless tagged)

V1's most common mistakes, in order: **#3 trying to do too much**, **#8 enablers cut for payoffs**, **#11 high curve**. Rank them first when severity is otherwise tied.

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
14. Tuned past the pod's power level. Agree on limits with the pod (bracket, personal rules like no tutors) and raise power slowly. Toning a deck down after overbuilding rarely satisfies anyone, and some commanders can't be toned down at all.
15. Colored sources short of pips (V3, DS).
16. No clear way to win (V3).

## 7. Evals (V1 unless tagged)

Pass/fail checks for a finished list or a proposed change set. In a review, run every row and report failures with the number. A row passes if the user's play experience explains why it doesn't apply.

| # | Check | Pass when | Fix (§) |
|---|---|---|---|
| E1 | Constraints | Budget, Game Changer count, combo rules and bracket all within table rules | same-role swap (§5) |
| E2 | Plan | Log line names one finisher type; ≤3 steps; step 1 is useful alone | §4 |
| E3 | One direction | No two payoff groups in contention; no off-plan side packages | §4, trap 3 |
| E4 | Enablers | Enablers ≥ 25 and > payoffs + enhancers; enhancers ≤ best 4–5 | §4 |
| E5 | Non-stacking | Every effect whose second copy is dead has ≤5 copies (≤3 with self-mill + recursion) | §5 |
| E6 | Draw | Card advantage ≥ 12, with several at MV ≤ 3 | §1, §5 |
| E7 | Early interaction | Targeted disruption at target, with cheap (MV ≤ 2) answers present | §1 |
| E8 | Resilience | No single common hate piece (Torpor Orb, Rest in Peace, an edict, Maze of Ith) blanks most of the plan; the answers to it don't share the weakness; most of a hand still works with the commander removed; any card the plan can't run without has a backup in the 99 or protection (V4) | §4, trap 4 |
| E9 | Ramp fit | Ramp MV lines up with commander MV; every ramp at MV ≥ 4 has a named reason | §5 |
| E10 | Curve | 6+ at cap (or an oval ramp/cheat deck); 2 is the largest slot; goldfish turns 2–6 spend nearly all available mana | §2 |
| E11 | Lands | Count ≥ formula result, rounded up; basics cover every fetch effect; sources match pips | §3 |
| E12 | Narrow answers | Each one is justified by the pod meta or this deck's weak point | §5 |
| E13 | Recount | After any change set, every role, curve and land count is recounted and still on target | §5 |
| E14 | Power fit | Expected win turn and bracket match the pod's. Explosive effects (mana doublers, extra turns, cast-for-free engines) are the biggest bracket dial: roughly 2 in bracket 2, 3–5 in bracket 3, ~9 in bracket 4 (V4, one builder's rough guide) | trap 14 |
| E15 | Commander role | Enabler/payoff/enhancer mix matches the commander's role | §4 |
| E16 | Vegetables | Ramp, Draw, Targeted and Mass all at target; Mass covers creatures, artifacts/enchantments and the graveyard | §1 |
| E17 | Curve fit | 5s are flexible; 6+ permanents are cheated, reduced or reanimated; the commander's MV slot is thin | §2 |
| E18 | Colored sources | Each color meets §3b (table scaled to the land count, partial credits applied, gold +1) for its most demanding card; untapped sources cover turn-1 plays; utility lands aren't counted as colored | §3b |
| E19 | Land quality | Tapped lands within budget, each with a named upside; 3+ colors have real fixing | §3a |
| E20 | Multiplayer scaling | Engine and payoff cards that fire once per four turns (attack-only, your-turn-only) each have a named reason; where a version that scales with 3 opponents fits the same role, it's preferred (V4) | §5 |
| E21 | Rebuild | Goldfish a wipe at the deck's usual peak: it redeploys a working board within 1–2 turns from hand, recursion or cheap key pieces. Key engine pieces aren't all creatures, or they're protected or recurrable (V4) | §4 |
| E22 | Multi-role | The commander covers ≥ 2 of card advantage, ramp and payoff, or the 99 does. Most non-land slots fill 2 roles or are the best in their one role (V4) | §5 |

**Goldfish symptoms → role** (V1, V3), for `rk-mtg-goldfish` runs or the user's game reports:

| Symptom | Likely cause |
|---|---|
| ~2 cards in hand by mid-game; deck stalls, topdecking | Draw too low or too expensive (E6) |
| Missed land drops | Lands (E11), cheap draw (E6) |
| Enough lands but the wrong colors; colored cards stranded | Colored sources (E18) |
| Lands arriving tapped cost early plays | Land quality (E19) |
| Uncastable cards stuck in hand | Curve (E10), ramp fit (E9) |
| Mana left unspent on most turns | Curve too high or lumpy (E10) |
| Payoffs in hand with nothing to trigger them | Enablers (E4) |
| One half of the plan stranded (sac outlets but nothing to sacrifice, or the reverse) | Rebalance the plan's steps (E4, E15) (V2) |
| Reaches the target turn with no way to win | Plan or wincon density (E2) |
| Wins far faster than the pod | Power fit (E14) |
| One wipe ends the game for this deck | Rebuild (E21) |
| Engines trigger rarely; deck feels slow at a full table | Multiplayer scaling (E20) |

Goldfish before buying cards. Goldfishing also shows which opening hands to keep: mulligan hands with no draw (V1).
