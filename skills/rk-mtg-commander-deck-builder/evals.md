# Multi-agent review evals

These cases test coordinator behavior, not card memorization. Run each case
with the named facts treated as verified Oracle and deck-snapshot data.
Passing requires the expected decision and rationale. A specialist's
unsupported verdict does not pass.

## Suite-wide generic invariants

Run each case once as written and once with card names replaced by equivalent
role descriptions or different cards with the same functional relationship.
The second pass prevents memorized card verdicts from satisfying the eval.

Across the suite, require:

- one coordinator-owned snapshot, constraint/pod ledger, thesis, and decision;
- specialist briefs and outputs matching the schemas in `specialists.md`;
- evidence-based disagreement exposed without voting or score averaging;
- problem-first discovery and a full stress test for every recommended pair,
  including budget-driven substitutes;
- affected verdicts invalidated and rerun after a constraint or pod agreement
  changes;
- sequential swap evaluation and a complete batch audit before publication;
- interaction split by timing and job, and role compression credited only for
  demonstrated normal use;
- setup-engine saturation and win conversion checked where relevant;
- player identity and explicit meta exceptions preserved;
- no-change, sidegrade, and test verdicts treated as successful outcomes; and
- after a meaningful accepted batch, a request for actual game evidence before
  further theory.

## Eval 01 — Persistent ramp versus burst mana

**Input:** A deck uses Ashling, Rekindled. Proposed swap: Thran Dynamo to
Rapturous Moment. Dynamo is persistent colorless ramp. Moment is one-shot
colored burst mana and filtering. Ashling can validly help cast either.

**Expected:** Replacement Auditor identifies different primary roles, names
the permanent mana lost, tests commander-off performance, makes the strongest
case for Dynamo, and returns sidegrade or not recommended unless persistent
ramp is demonstrably excessive.

**Must not:** Call Moment a strict upgrade from synergy or net-mana comparison
alone.

## Eval 02 — Meta card with weak commander synergy

**Input:** Propaganda has little direct commander synergy. The player regularly
faces go-wide creature decks and needs setup turns for expensive engines.

**Expected:** Meta & Resilience classifies Propaganda as a justified local-meta
card and protects it unless equivalent early anti-swarm coverage exists.

**Must not:** Cut it solely for low commander synergy or low package overlap.

## Eval 03 — Similar engine comparison

**Input:** Compare Primal Amulet with Double Vision for one spell-copy engine
slot. Valid facts: Amulet costs less, reduces spell costs before transforming,
then becomes Primal Wellspring; land destruction is rare in the pod.

**Expected:** Compare the complete role packages pairwise, including front-side
setup value, effective commander-assisted cost, transformed-land resilience,
and the pod's removal pattern. Conclude that Double Vision is not clearly
better and may be unnecessary.

**Must not:** Evaluate both cards independently and recommend both because
spell copying is synergistic.

## Eval 04 — Commander-dependent top end

**Input:** A deck has a high density of mana-value seven and eight spells. Its
commander supplies two restricted mana that only some of those spells can use.
Test the commander being removed twice.

**Expected:** Mana & Statistics reports native and commander-assisted curves,
classifies each expensive card by functional cost, identifies stranded hard
top-end, and answers whether the commander is acceleration or life support.

**Must not:** Subtract two from every expensive spell or rely on average mana
value alone.

## Eval 05 — Conflicting resource economies

**Input:** The deck relies heavily on graveyard recursion while also running
many delve effects and effects that exile cards before the recursion package
can recover them.

**Expected:** Systems Architect maps generators, consumers, converters, and
recovery; identifies competition for finite graveyard material; and recommends
reducing the conflict before shopping for more recursion.

**Must not:** Praise every graveyard-adjacent card as independently synergistic.

## Eval 06 — Stale live deck

**Input:** Turn one uses an Archidekt URL containing card A. Before a new audit,
the user edits the live deck: card A is removed and card B is added.

**Expected:** Coordinator refetches before the audit, records the count and
delta, gives all specialists the new immutable snapshot, reconciles the ledger,
and never proposes cutting card A.

**Must not:** Treat a cached URL response or prior transcript list as current.

## Eval 07 — Duplicate singleton by printing

**Input:** A final deck contains two printings of the same nonbasic land under
different set and collector identifiers.

**Expected:** Coordinator resolves Oracle identity, reports the singleton
legality failure and correct live count before strategic analysis, and requires
the duplicate to be fixed.

**Must not:** Treat different printings as different legal cards or repair the
count with unrelated strategic cuts.

## Eval 08 — Budget land replacement

**Input:** A premium untapped dual costs EUR 14 and the deck exceeds its cap by
EUR 10. A cheap replacement is available but may alter colored-source and
tapped-land reliability.

**Expected:** Budget Analyst compares marginal fixing quality and substitutes,
then reruns color-source, pip, commander-casting, and tapped-land checks before
recommending the economy swap.

**Must not:** Choose the cheapest land without validating mana quality.

## Eval 09 — Good candidate, no slot needed

**Input:** Double Vision is a legal, synergistic candidate, but the live deck
already has adequate spell-copy engines and has a different demonstrated
structural problem.

**Expected:** Discovery may shortlist it, but the coordinator or Replacement
Auditor says “good card, no slot needed” and spends the slot on the diagnosed
problem or recommends no change.

**Must not:** Add it because it is popular, powerful, or on theme.

## Eval 10 — Archetype challenge before slot tuning

**Input:** A deck is presented as traditional control, but its commander
rewards proactive main-phase expensive spells and cannot efficiently support
reactive play.

**Expected:** Systems Architect flags a thesis conflict and tests a proactive
big-mana or proactive-control thesis before individual cuts. Other specialists
continue under only the coordinator-approved thesis.

**Must not:** Silently optimize each specialist toward a different archetype.

## Eval 11 — Constraint change invalidates a replacement

**Input:** A card is initially cut only because it enables a combo forbidden by
the pod. The player then clarifies that the pod permits the card as long as the
combo is not executed.

**Expected:** Coordinator invalidates the original replacement verdict, reruns
the full stress test without treating combo capability as a cut reason, and
shows the strongest case for keeping the card before updating the report.

**Must not:** Preserve the old cut, improvise a new replacement pair without a
stress test, or update a canvas from the stale verdict.

## Eval 12 — Individually valid swaps damage one package

**Input:** Two replacements each pass when compared against the original deck,
but both cuts remove different pieces from the same recursion-and-copy package.
The second addition duplicates creature removal that is already adequate.

**Expected:** Coordinator evaluates the second pair against the list containing
the first swap, reruns package counts and coverage, and rejects or revises the
combined batch when the shared package becomes too weak.

**Must not:** Publish both swaps merely because each pair passed independently.
