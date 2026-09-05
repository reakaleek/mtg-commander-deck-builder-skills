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

## Deck contract

Normalize the interview into a compact ledger before analysis. Split hard
constraints from preferences, per the constraint-ledger rules in `SKILL.md`.
Cover, when relevant: commander and command-zone configuration, color
identity, budget basis (total value versus additional spend, owned cards,
proxies), bracket or power target, Game Changer cap, combo and tutor policy,
mass land denial / extra-turn / stax / house restrictions, pet cards and
exclusions, desired play experience, intended win pattern, and pod or meta
information. Never silently violate a hard constraint; pause and ask when two
hard constraints conflict.

## Commander fit audit

Evaluate the commander on its own before judging the 99:

- Does it directly advance the deck thesis, or is it a color-identity anchor
  the deck plays around?
- Which functional roles does it supply: mana, cards, board development,
  interaction, protection, inevitability, a win condition?
- At what turn or mana threshold does each supplied role actually come
  online? A role that only starts in the mid or late game is not equivalent
  to an early, independent version of that role.
- How commander-dependent is the deck? What happens if the commander is
  removed twice in a game?
- Does the commander help close games, or only set them up?
- Is the color identity unusually weak at a role the deck's plan requires?

## Static structural audit

Give every card exactly one primary functional role for counting; secondary
roles are tags, not additional slots. Report both the raw count and the
percentage of the complete deck per role, and note that primary-role
percentages sum to the whole deck while overlapping secondary tags do not.
Treat the ranges in `fundamentals.md` as diagnostic priors, not quotas; adapt
them for commander text, curve, land strategy, fast mana, colors, archetype,
bracket, and pod.

## Functional reliability audit

A raw count can overstate real function. For each important package, split
quantity from reliability instead of reporting one number:

- **Ramp:** early unconditional acceleration versus conditional catch-up,
  expensive ramp, combat-dependent ramp, and delayed or tapped mana. A deck
  with a healthy nominal ramp count but few pieces usable by the turn the
  commander wants to act does not have reliable ramp.
- **Card advantage:** unconditional draw, conditional draw, repeatable
  engines, burst draw, combat-dependent draw, commander-dependent draw, and
  opponent-dependent draw. Call out independent card velocity, the draw that
  keeps working with the commander gone, explicitly.
- **Interaction:** low-mana versus 3+ mana answers, conditional versus
  unconditional, permanent versus temporary (bounce is delay, not removal),
  and proactive versus reactive.
- **Protection:** immediate versus delayed, board-wide versus commander-only,
  and recursion that only masquerades as protection because it does not stop
  the removal itself.

For each package report a raw count, a reliable count, a conditional count,
and the key dependency that limits it.

## Dependency audit

For any questionable or important card, ask what already has to be true for
it to perform: the commander must be present, another permanent or token
must exist, the graveyard must hold targets, an opponent must attack or
connect with combat damage, counters must already exist, another spell must
already be on the stack, the player must be ahead or holding excess mana, or
an opponent must take a specific action. Classify roughly as independent,
light, moderate, or heavy dependency. Do not cut a card merely for being
dependent; combo pieces and payoffs are supposed to be. Look instead for an
excess concentration of dependent cards that collapses together when one
engine is disrupted, and flag internal contradictions directly, such as a
card that rewards being attacked inside a deck built to prevent attacks, a
token payoff with sparse token generation, a proliferate package with too few
counters, a sacrifice payoff with too few outlets, or graveyard recursion in
a deck whose key effects exile themselves.

## Engine / enabler / payoff / theme classification

For strategy cards, classify conceptually as an engine (repeatedly produces
the deck's advantage), an enabler (makes the engine function), a payoff
(converts a successful setup into advantage or a win), a redundant functional
copy, or a low-leverage synergy slot that only matches a theme, creature
type, or keyword without moving the plan. Use this to catch theme
saturation: a card should not survive review merely because it shares a
tribe, mentions the deck's keyword, or scores high on EDHREC inclusion. Avoid
dismissive language; call these slots "theme-only" or "low-leverage," not
"cute."

## Redundancy audit

Group cards by the job they do, not their card type: attack taxes, forced
combat, targeted creature removal, artifact/enchantment removal, commander
protection, token generation, sacrifice outlets, graveyard recursion,
finishers, and similar jobs specific to this list. For each job, ask how many
copies the deck needs to see one consistently, whether drawing multiples is
still desirable, and whether a unique effect exists that should survive even
though it shares a broad category with weaker cards. When three or more cards
already do the same job, compare their floors and name the weakest copy
before adding another version of that effect, matching the addition-
justification rule in `SKILL.md`.

## Win-condition audit

"Good value" or "eventually attacks" is not a sufficient plan. List each
realistic win path and, for each, note the cards required, whether the
commander is required, the mana and board state needed, whether it works
from parity or from behind, whether it survives a board wipe, whether one
removal spell answers it, and the expected turn range for the stated bracket
or pod. Distinguish an engine, a payoff, a finisher, and the actual win
condition; a political, pillow-fort, control, or group-hug deck must still
answer "after surviving the table, how does it eliminate the remaining
players?"

## Answer matrix

Do not judge interaction by count alone. Rate coverage (strong, acceptable,
weak, or color-identity limitation) against the threats this format
produces: creatures, other commanders, artifacts, enchantments,
planeswalkers, graveyards, problematic lands, wide creature boards,
indestructible boards, spells on the stack, activated and triggered
abilities, combo pieces, and combat alpha strikes. Do not expect every color
identity to answer everything equally; when the color identity lacks a clean
answer, say so instead of relabeling an adjacent effect (a fog is not a
wrath).

## Mana and curve audit

Go beyond a land count. Check land structure (MDFCs that function as lands,
always-tapped lands, conditional untapped lands, colorless utility lands,
lands with type requirements), colored source counts against actual pip
pressure from turn 1 through the commander's cost, how much ramp is usable
by the deck's early turns, and the mana-value distribution including top-end
clumps and the count of meaningful early plays. The question that matters is
whether the deck can meaningfully deploy mana during its first several turns
at the speed its bracket expects, not whether the average mana value looks
acceptable in isolation.

## Opening-hand and goldfish audit

This expands the shared pre-swap check in `SKILL.md`; keep that heuristic
labelling. Where practical, reason through more than one representative
opening hand rather than a single ideal one, checking for a workable land
count and colors, an early play before the commander, ramp if the commander
is expensive, card velocity, and interaction when the bracket expects it.
Then goldfish turns one through five: likely commander turn, unused mana,
development before the commander lands, cards left in hand, and whether the
deck can hold up interaction. Use this to catch top-heavy curves, tapped-
land drag, ramp that is nominally present but actually delayed, and a slow
start, not to claim a multiplayer win rate.

## Adversarial scenario audit

Test only the scenarios relevant to this archetype, for example: the
commander is removed twice, the board is wiped around the mid-game, the
primary engine is removed, opponents refuse to engage with the deck's
intended combat or political pattern, the deck becomes the archenemy, an
opponent resolves a combo, the deck is topdecking, the graveyard is exiled
when the plan depends on it, a key permanent is exiled instead of destroyed,
or a land drop is missed. For each relevant scenario, note whether the deck
still operates, which cards go dead, what recovery tools exist, and whether
that outcome is acceptable for the target bracket.

## Role compression

Credit cards that meaningfully perform more than one job in normal play, such
as removal with political leverage, protection that can also finish, ramp
that also draws, an MDFC that is a land or a spell, or a wipe with
asymmetric protection built in. Only credit a secondary role when it is
realistically relevant, not merely present in the text, and call these cards
out when explaining why a slot is kept over a nominally more powerful
alternative.

## Weakest-slot ranking

Before searching for any addition, rank the current weakest five to ten
cards against the deck thesis, floor when behind, dependency, mana
efficiency, redundancy, role necessity, commander reliance, matchup
relevance, and budget efficiency. Use a plain tier such as core, strong,
replaceable, or weak rather than a numeric score. The order of work is
"these are the weakest slots, does a candidate materially improve one of
them," never "found a card, now find something to cut."

## Problem-first upgrade search

Every proposed addition must trace back to a named problem or a stated
strategy improvement, never to a card found first. State the problem (for
example, insufficient independent card velocity, too few early untapped
colored sources, weak graveyard coverage, excess commander dependency,
redundant expensive finishers, thin protection, or a win condition that
needs too much setup), then search for and compare candidates against it.
Follow the existing swap-report format in `SKILL.md`, and for each swap state
what capability the cut loses, what the add gains, why the add beats no
change and beats the weakest existing functional copy, any dependency it
introduces or removes, the budget delta, and any Game Changer or bracket
impact.

## Budget efficiency

When a budget exists, judge marginal improvement per unit of currency rather
than spending toward the cap. Prioritize, unless the deck's own gaps say
otherwise: essential engine pieces, unique or irreplaceable role players,
functional consistency, interaction, mana-base upgrades, then luxury staples.
An expensive card must justify itself against several cheaper upgrades that
could fill the same budget. Recognize diminishing returns on mana-base
polish; do not fund premium lands by skipping a demonstrated functional gap
unless mana reliability is the demonstrated problem.

## Legality, bracket, and Game Changer audit

Run this against current Scryfall data, not memory, before final
recommendations: commander legality and color identity, singleton
construction and any stated exceptions, 100-card construction when the deck
is declared final, Game Changer count against the user's cap, bracket
constraints, and any user-defined combo, tutor, MLD, or house restriction.
Print a concise compliance line per constraint the user actually supplied.
Never claim compliance for a price or a rule that is unresolved; report it as
unknown instead.

## Pod fit

When the user shares pod or meta information, separate theoretical deck
quality from pod fit. A strong list can still be a poor fit if it duplicates
another regular pod deck, ignores a stated meta threat (fast combo, board
wipes, graveyard hate), or produces a gameplay experience the table already
said it dislikes.

## Commander recommendation mode

When the user has a strategy but no commander, compare candidates on
criteria instead of popularity: direct strategy enablement, forced versus
merely incentivized behavior, card advantage, mana generation, interaction
access from the colors, resilience, commander dependency, finishing ability,
budget friendliness, bracket ceiling, and pod duplication or social fit. Give
a short ranked shortlist with tradeoffs. High EDHREC deck count is not a
reason by itself.

## Report structure

Scale which of these appear to what the user asked for. A full review, in
order: Deck Contract, Deck Thesis, Commander Fit, Static Composition,
Functional Reliability, Mana & Curve, Card Advantage, Interaction Coverage,
Strategy Packages, Win Conditions, Resilience, Weakest Slots, Upgrade
Strategy, Ranked Swaps, Constraint Compliance, then the Archidekt import
blocks. Keep numeric findings reproducible; do not assign a single
false-precision power score (an "8.3/10") unless the repository defines a
rigorous model for it. Prefer qualitative findings such as structurally
sound, adequate but conditional, strong permanent interaction but weak stack
interaction, commander-dependent, top-heavy for the target bracket, or
insufficient independent recovery.

## Build mode reuse

Apply the same lenses proactively while constructing a new list, before
declaring it final: establish the contract and thesis, verify commander fit,
assign every card one primary role, check package reliability and
dependencies, audit redundancy, confirm realistic win lines, run the answer
matrix, audit mana and curve, run the opening-hand and goldfish heuristic,
test commander-removal and wipe scenarios, and improve the weakest slots
found before verifying budget, bracket, and legality. This keeps a first
draft from carrying too many theme-only slots or too little independent
infrastructure.
