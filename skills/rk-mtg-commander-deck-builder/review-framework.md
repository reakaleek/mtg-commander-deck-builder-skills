# Review framework

Optimize the deck as a system. A pile of individually strong cards can still
be structurally poor. Diagnose before recommending a single swap.

Answer, in order, before proposing changes:

1. What is this deck trying to do?
2. Does the commander materially enable that plan?
3. Is the deck structurally capable of executing it?
4. How reliable are its functional packages?
5. What happens when the main plan fails?
6. How does the deck actually win?
7. What threats can and cannot it answer?
8. Which cards are the weakest contributors?
9. Only then: what swaps solve the identified problems?

These audits do not need to appear as separate headings in every reply. Scale
depth to what the user asked for. A request to "analyze statistically" stops
after structure, reliability, mana, and coverage unless a critical issue
surfaces. A request to "optimize" or "review and upgrade" runs the full
sequence before any swap is proposed.

Normalize the interview into the constraint ledger in `SKILL.md` before
analysis.

## Commander fit audit

Evaluate the commander on its own before judging the 99:

- Does it directly advance the deck thesis, or is it a color-identity anchor
  the deck plays around?
- Which functional roles does it supply, and at what turn or mana threshold
  does each come online?
- How commander-dependent is the deck? What happens if the commander is
  removed twice in a game?
- Does the commander help close games, or only set them up?
- Is the color identity unusually weak at a role the deck's plan requires?

## Static structural audit

Give every card exactly one primary functional role for counting; secondary
roles are tags, not additional slots. Report both the raw count and the
percentage of the complete deck per role. Treat the ranges in
`fundamentals.md` as diagnostic priors, not quotas.

## Functional reliability audit

A raw count can overstate real function. For each important package, split
quantity from reliability:

- **Ramp:** early unconditional acceleration versus conditional catch-up,
  expensive ramp, combat-dependent ramp, and delayed or tapped mana.
- **Card advantage:** unconditional, conditional, repeatable, burst,
  combat-dependent, commander-dependent, and opponent-dependent draw. Call
  out independent card velocity explicitly.
- **Interaction and protection:** apply the zone, phase, mode, and floor
  rule in `fundamentals.md`. Split low-mana versus 3+ mana, permanent versus
  temporary, immediate versus delayed.

For each package report a raw count, a reliable count, a conditional count,
and the key dependency that limits it.

## Dependency audit

For any questionable or important card, ask what already has to be true for
it to perform. Classify roughly as independent, light, moderate, or heavy.
Do not cut a card merely for being dependent; combo pieces and payoffs are
supposed to be. Look instead for an excess concentration of dependent cards
that collapses together when one engine is disrupted, and flag internal
contradictions (a token payoff with sparse token generation, proliferate
with too few counters, sacrifice payoffs with too few outlets, graveyard
recursion whose key effects exile themselves).

## Resource-economy audit

Use the generator, converter, consumer, and recovery map in
`fundamentals.md`. Count only resources the current list can repeatedly use.
Flag packages that consume the same graveyard, exile, hand, token, counter, or
library material; then test what remains after the most important consumer
resolves. A card can be individually synergistic while making the whole
economy less reliable.

## Engine / enabler / payoff / theme classification

For strategy cards, classify as an engine, an enabler, a payoff, a redundant
functional copy, or a low-leverage synergy slot that only matches a theme.
A card should not survive review merely because it shares a tribe, mentions
the deck's keyword, or scores high on EDHREC inclusion. Call these slots
"theme-only" or "low-leverage," not "cute."

Also split setup engines, which improve later actions, from immediate engines
that replace value now. Compare setup density with payoff and finisher density.
When several permanents all need another spell and another turn to matter,
flag setup-engine saturation even when every card is on theme.

## Redundancy audit

Group cards by the job they do, not their card type. Apply the addition-
justification rule in `SKILL.md` and the same-job rule in `fundamentals.md`.
When three or more cards already do the same job, compare their floors and
name the weakest copy before adding another version.

## Win-condition audit

"Good value" or "eventually attacks" is not a sufficient plan. List each
realistic win path and, for each, note the cards required, whether the
commander is required, the mana and board state needed, whether it works
from parity or from behind, whether it survives a board wipe, whether one
removal spell answers it, and the expected turn range for the stated
bracket. Distinguish an engine, a payoff, a finisher, and the actual win
condition. Ground catalogued combos with `rk-mtg-spellbook` `combos`.

## Answer matrix

Do not judge interaction by count alone. Rate coverage (strong, acceptable,
weak, or color-identity limitation) against the threats this format
produces: creatures, other commanders, artifacts, enchantments,
planeswalkers, graveyards, problematic lands, wide boards, indestructible
boards, spells on the stack, activated and triggered abilities, combo
pieces, and combat alpha strikes. When the color identity lacks a clean
answer, say so instead of relabeling an adjacent effect.

## Mana and curve audit

Use `rk-mtg-scryfall` `deck-stats` for the histogram, early-play count, pips,
colored sources, and the tapped-land heuristic. Then judge whether the deck can
meaningfully deploy mana during its first several turns at the speed its
bracket expects.

Two numbers from `deck-stats` sharpen that judgement. The tipping point is the
mana value that gets 65% of the nonland spells online; it describes the deck's
real speed better than an average, and a tipping point well above the bracket's
expected pace is a curve problem no single swap fixes. Playability is the
per-spell chance of casting on curve from lands alone, so its hardest-to-cast
list separates cards that are too expensive from cards whose colors the mana
base does not support. Those two failures need different fixes.

Feed the tipping point to `rk-mtg-goldfish` `stats` as `--mana-target` and read
the sweet spot alongside the opening-hand and per-turn land odds. Quote the
thresholds with the number.

Build a top-end budget by classifying every expensive spell using the
functional-cost classes in `fundamentals.md`. Report a native curve and a
commander-assisted curve; never subtract commander mana from a spell that
cannot strategically use it. Repeat the practical curve test after the
commander is removed twice. Identify stranded hard top-end separately from
modal, self-discounting, and independently discounted cards that retain a
usable floor.

For critical roles, count functional copies rather than names and use a stated
draw model when useful. Report the chance of seeing at least one relevant copy
by the turn that role matters. Do not hide timing, conditionality, or
commander-dependence inside a redundancy count.

## Opening-hand and goldfish audit

This is a heuristic, not a real multiplayer game. Where practical, reason
through more than one representative opening hand rather than a single
ideal one, checking for a workable land count and colors, an early play
before the commander, ramp if the commander is expensive, card velocity,
and interaction when the bracket expects it. Then goldfish turns one
through five: likely commander turn, unused mana, development before the
commander lands, cards left in hand, and whether the deck can hold up
interaction. Optional: `rk-mtg-goldfish` `new` for two or three sample hands,
labelled as samples. Before sending a swap list, ask whether those swaps
would have changed the stated failure; if not, revise them.

Rate candidate swaps for opening-hand quality as well as late-game ceiling. A
replacement that is powerful only after the commander and an engine are
online can worsen the exact hands the deck needs to repair.

## Adversarial scenario audit

Test only the scenarios relevant to this archetype, for example: the
commander is removed twice, the board is wiped around the mid-game, the
primary engine is removed, opponents refuse to engage with the intended
pattern, the deck becomes the archenemy, an opponent resolves a combo, the
deck is topdecking, the graveyard is exiled when the plan depends on it, a
key permanent is exiled, or a land drop is missed. For each, note whether
the deck still operates, which cards go dead, what recovery tools exist,
and whether that outcome is acceptable for the target bracket.

## Role compression

Credit cards that meaningfully perform more than one job in normal play.
Only credit a secondary role when it is realistically relevant, not merely
present in the text.

## Weakest-slot ranking

Before searching for any addition, rank the current weakest five to ten
cards against the deck thesis, floor when behind, dependency, mana
efficiency, redundancy, role necessity, commander reliance, matchup
relevance, and budget efficiency. Use a plain tier such as core, strong,
replaceable, or weak. The order of work is "these are the weakest slots,
does a candidate materially improve one of them," never the reverse.

`rk-mtg-scryfall` `deck-stats --market-index` gives one optional prior here:
cards the market prices and plays far below the rest of the list. It measures
what the market thinks of a card in the abstract, not what the card does in
this deck, so it cannot rank a slot on its own. A cheap, unpopular card that
serves the thesis stays; a card the index likes that serves nothing still gets
cut. Use it to notice slots you skimmed, then rank them on the criteria above.

## Problem-first upgrade search

Every proposed addition must trace back to a named problem or a stated
strategy improvement. Follow the swap-report format in `SKILL.md`. For each
swap state what capability the cut loses, what the add gains, why the add
beats no change and beats the weakest existing functional copy, any
dependency it introduces or removes, the budget delta, and any Game
Changer or bracket impact.

Use two stages. First, fast-screen 10–20 candidates for role fit, timing,
functional cost, commander-on and commander-off floor, resource fit, and
budget fit; shortlist only what survives. Second, run the full Replacement
Stress Test on the best three to five candidates before recommending any swap.

## Mandatory replacement gate

Every recommended cut-to-add pair must pass the complete Replacement Stress
Test before it appears in a report, canvas, buy list, or canonical update.
Small, obvious, budget-driven, and constraint-mandated swaps are not
exceptions.

The user-facing recommendation must include:

- the strongest case for keeping the current card;
- capability lost and capability gained;
- whether the lost capability remains adequately covered;
- commander-on and commander-off performance;
- opening-hand quality and floor when behind;
- the replacement's new failure mode; and
- exactly one permitted verdict.

A specialist's private analysis does not satisfy this gate. The coordinator
must expose the decisive tradeoffs in the report.

If the user changes a constraint, pod agreement, deck thesis, budget, or
intended play pattern, invalidate every affected replacement verdict and rerun
the test before updating the recommendation.

## Replacement Stress Test

Do not recommend a replacement until the coordinator or Replacement Auditor
compares the pair. Start with the strongest possible case for keeping the
current card, then evaluate:

1. current card's primary role;
2. current card's secondary roles;
3. replacement's primary role;
4. capability lost by making the cut;
5. capability gained;
6. whether the lost capability is covered elsewhere;
7. normal mana cost;
8. effective mana cost with valid commander assistance;
9. performance without the commander;
10. timing compatibility;
11. opening-hand quality;
12. floor when behind;
13. ceiling when ahead;
14. immediate versus delayed impact;
15. persistent versus one-shot value;
16. resource-economy interactions;
17. engine and package interactions;
18. pod or meta effect;
19. budget impact; and
20. the new failure mode introduced.

Pairwise comparisons matter when cards compete for the same engine slot:
compare their complete role packages, costs before payoff, resilience by
permanent type, and local removal patterns rather than rating each in
isolation.

Return exactly one verdict: **strict upgrade**, **contextual upgrade**,
**sidegrade**, **meta choice**, **test**, or **not recommended**. Different
primary roles are not interchangeable merely because both involve mana,
cards, copying, or another broad category. “Good card, no slot needed” and
“the proposal does not survive deeper review” are valid conclusions.

## Recommendation states

Track card status separately from replacement verdicts:

- **CORE:** foundational to the architecture.
- **KEEP:** good fit with no current structural reason to remove.
- **TEST:** promising hypothesis requiring game evidence.
- **FLEX / META:** slot depends materially on pod pressures or preference.
- **CUT WATCH:** below alternatives, but not urgent.
- **CUT:** strong structural case to remove now.

Do not present experimental ideas with the same certainty as structural fixes.

## Replacement batch audit

Evaluate swaps sequentially against the deck produced by the preceding swaps,
not only against the original snapshot. After every pair passes individually,
audit the complete proposed batch:

1. Recount every functional category.
2. Recheck package density and redundancy.
3. Identify capabilities weakened by multiple cuts.
4. Recheck win conditions, interaction coverage, mana, budget, bracket, and
   table rules.
5. Confirm that the combined changes preserve the deck thesis.
6. Remove or revise any individually acceptable swap that becomes harmful in
   combination.

An individually valid swap can fail the batch audit. Do not publish the batch
until both levels pass.

## Budget efficiency

When a budget exists, judge marginal improvement per unit of currency
rather than spending toward the cap. Prioritize, unless the deck's own gaps
say otherwise: essential engine pieces, unique role players, functional
consistency, interaction, mana-base upgrades, then luxury staples. Do not
fund premium lands by skipping a demonstrated functional gap unless mana
reliability is the demonstrated problem.

For a budget-driven land replacement, rerun colored source, pip, tapped-land,
and commander-casting checks. State whether the money buys unique function or
only marginal fixing or efficiency; never save money by silently creating a
new mana failure.

## Legality, bracket, and Game Changer audit

Run `rk-mtg-scryfall` `validate-deck --final --resolve` and `--bracket N` when they
named a bracket, plus `rk-mtg-spellbook` `bracket`. Print a concise compliance
line per constraint the user actually supplied. Never claim compliance for
a price or a rule that is unresolved.

## Pod fit

When the user shares pod or meta information, separate theoretical deck
quality from pod fit. A strong list can still be a poor fit if it
duplicates another regular pod deck, ignores a stated meta threat, or
produces a gameplay experience the table already said it dislikes.

## Commander recommendation mode

When the user has a strategy but no commander, compare candidates on
criteria instead of popularity: direct strategy enablement, forced versus
merely incentivized behavior, card advantage, mana generation, interaction
access from the colors, resilience, commander dependency, finishing
ability, budget friendliness, bracket ceiling, and pod duplication or
social fit. Give a short ranked shortlist with tradeoffs. High EDHREC deck
count is not a reason by itself.

## Report structure

Scale which of these appear to what the user asked for. A full review, in
order: Deck Thesis, Commander Fit, Static Composition, Functional
Reliability, Mana & Curve, Card Advantage, Interaction Coverage, Strategy
Packages, Win Conditions, Resilience, Weakest Slots, Upgrade Strategy,
Ranked Swaps, Constraint Compliance, then the Archidekt import blocks. Keep
numeric findings reproducible; do not assign a single false-precision power
score. Prefer qualitative findings such as structurally sound, adequate but
conditional, commander-dependent, or insufficient independent recovery.

## Build mode reuse

Apply the same lenses proactively while constructing a new list, before
declaring it final: establish the thesis, verify commander fit, assign
every card one primary role, check package reliability and dependencies,
audit redundancy, confirm realistic win lines, run the answer matrix,
audit mana and curve, run the opening-hand and goldfish heuristic, test
commander-removal and wipe scenarios, and improve the weakest slots found
before verifying budget, bracket, and legality.
