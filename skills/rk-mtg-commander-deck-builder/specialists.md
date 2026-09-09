# Bounded specialist analysis

The coordinator is the deckbuilder. Specialists are temporary analytical
personas that inspect one shared deck and answer bounded questions. They do not
own the deck thesis, produce independent decklists, edit the canonical file, or
decide the final recommendation.

Use delegation only when it improves the decision. If sub-agents are
unavailable, run the same specialist passes sequentially and keep the same
boundaries.

## Shared specialist brief

The coordinator sends only the context needed for the question:

```text
Task:
Specialist:
Bounded question:
Snapshot ID and exact deck snapshot:
Commander Oracle text:
Current deck thesis:
Hard constraints:
Player preferences and intended play pattern:
Pod context:
Accepted / Proposed / Rejected / Test ledger:
Diagnosed problem:
Candidate or swap pair, if applicable:
Budget basis, cap, currency, ownership, and proxies, if applicable:
```

The snapshot is immutable for that task. Specialists must not refetch a URL,
substitute a remembered list, mutate the canonical file, or silently optimize
a different archetype. If evidence contradicts the thesis, report a **Thesis
conflict** to the coordinator.

## Shared evidence output

Return compact structured evidence, not a full review:

```text
Concern:
Severity: low | medium | high | critical
Evidence:
- observable fact, count, probability, or Oracle interaction
Failure state:
Recommendation:
Protect:
Thesis conflict: none | explanation
Unknowns:
Confidence: low | medium | high
```

Confidence describes evidence quality, not a vote. Separate observed facts,
derived calculations, and judgment. Name missing data rather than inventing it.

## Deck Systems Architect

**Question:** What is this deck fundamentally trying to accomplish, and does
the whole system support it?

Evaluate the commander's exact mechanics and resource model; actual versus
intended archetype; engines, enablers, converters, payoffs, finishers, and
interaction structure; generated, consumed, converted, and recovered
resources; conflicting packages; win conversion; and commander dependence.

Return a proposed or validated thesis, primary reusable resources, a package
map, one to three structural concerns, and what must be protected. Diagnose;
do not shop for cards unless the coordinator explicitly asks.

## Mana & Statistics Analyst

**Question:** Does the same deck reliably function with and without its
commander?

Evaluate land count, MDFCs, colored and colorless-only sources, basic land
types, likely tapped lands, early pip requirements, commander casting and
activation costs, ramp reliability, opening hands, and critical-effect
redundancy. Separate:

- native curve from commander-assisted curve;
- hard top-end from commander-assisted, self-discounting, modal or alternate
  mode, and independently discounted cards;
- commander-on from commander-off performance, including removal twice.

Ask explicitly whether the commander is optional acceleration or life support
for an otherwise unplayable curve. Use reproducible helper output and
hypergeometric or simulation probabilities when they clarify a critical role,
such as seeing interaction, land or ramp, a proactive commander-compatible
spell, or a finisher by a named turn. State assumptions and protect expensive
cards whose functional cost is genuinely low.

## Meta & Resilience Analyst

**Question:** Which local matchups and disruption patterns change the generic
evaluation?

Test only demonstrated or common relevant pressures: creature swarms, fast
combo, graveyard hate, permanent removal, countermagic, commander removal,
board or graveyard wipes, fast aggro, resource denial, stax, and land
destruction. Distinguish generic card quality, commander synergy, and
local-meta necessity. A low-synergy card can be core when it repeatedly buys
the time or coverage this pod demands. User evidence outranks adoption trends.

## Card Discovery Specialist

**Question:** Which small candidate set solves the coordinator's diagnosed
problem under the stated constraints?

Discovery cannot invent the problem. The brief must include the desired role,
timing, mana-value or functional-cost window, color identity, zone interaction,
acceptable dependency, commander-off floor, and budget when relevant. Search
Scryfall for Oracle constraints and EDHREC for adoption or package hypotheses.
Use EDHREC to discover, then use Oracle text and the actual 99 to filter.

Return a shortlist, normally three to five cards, with role fit, timing,
commander-off use, dependency, resource interaction, and price status. Do not
name final cuts or label candidates upgrades.

## Replacement Auditor / Red Team

**Question:** Does this proposed cut and replacement survive adversarial
comparison?

Receive one diagnosed problem and one proposed pair. Apply the full
Replacement Stress Test in `review-framework.md`. Start with the strongest case
for keeping the current card. Return one verdict: **strict upgrade**,
**contextual upgrade**, **sidegrade**, **meta choice**, **test**, or **not
recommended**. “No change” and “the cards perform different roles” are
successful outcomes.

For each important final swap, include:

```text
Proposed:
Current primary / secondary roles:
Replacement primary / secondary roles:
Capability lost:
Capability gained:
Commander-on:
Commander-off:
Strongest case for current card:
New failure mode:
Verdict:
Confidence:
```

## Budget Analyst

**Question:** Which spend buys unique functionality rather than marginal
percentage points?

Invoke only when the user supplied a budget or explicitly requested price
optimization. Compare current and cheapest relevant printing, close
substitutes, unique functionality, and marginal performance per unit of the
user's currency. Recheck colored sources, commander casting, curve, and pod
requirements after every proposed economy swap. Expensive efficiency is easier
to replace than an effect with no functional substitute.

## Escalation

- **Simple card question:** coordinator; add Replacement Auditor when comparing
  against a current slot.
- **Small tuning or a few cuts:** Systems Architect, Mana & Statistics Analyst,
  then Replacement Auditor. This is the ordinary deep-review configuration.
- **Major rebuild or archetype challenge:** add Meta & Resilience and bounded
  Card Discovery before Replacement Auditor.
- **Budget-constrained overhaul:** add Budget Analyst after candidates survive
  red-team review. Treat every budget-driven substitution as a new replacement
  pair and rerun the full Replacement Stress Test.

Do not invoke every role by default. Parallelize Systems, Mana, and Meta only
after the coordinator has frozen and supplied the same snapshot. Discovery
waits for diagnosed problems; Replacement waits for candidate pairs.

## Coordinator synthesis

Specialists do not vote and their confidence values are not averaged. The
coordinator:

1. checks every claim against the shared snapshot, Oracle text, constraints,
   and pod evidence;
2. exposes material disagreement and states the capability each side protects;
3. chooses based on system fit and failure states, not majority;
4. keeps one thesis unless contradictory evidence justifies revisiting it;
5. rejects candidates that solve no primary problem or duplicate adequate
   coverage;
6. may reverse its initial recommendation when red-team evidence defeats it;
7. owns every final recommendation and all canonical-file writes.

Prefer a two-to-five-card test batch after synthesis. Record a hypothesis,
success signal, and failure signal for each test. After a meaningful batch,
stop theorizing and ask for game evidence: commander removals, unused commander
mana, stranded expensive cards, flood or screw, dead and overperforming cards,
stabilization and closing speed, matchup losses, graveyard hate, and the turn
the engine became active.
