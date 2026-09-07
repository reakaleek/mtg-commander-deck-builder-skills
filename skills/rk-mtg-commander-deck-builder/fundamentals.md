# Commander deckbuilding fundamentals

Use these as a starting point for a normal Commander deck's 99, not as
unbreakable quotas. The commander's text, color identity, table, budget, and
chosen strategy take precedence. Count each card by its primary role when
reporting totals, and explain meaningful overlap.

Baseline ranges are diagnostic priors, never printed targets. Report raw
counts only. No target column.

## Functional baseline

- **36–38 lands:** Prefer reliable untapped mana and enough fixing for the
  deck's color requirements. Move up for expensive spells or land-centric
  strategies, and down only when the curve and reliable acceleration support it.
- **10–12 ramp:** Favor efficient acceleration, especially two-mana options,
  while considering land ramp, mana creatures, and rocks appropriate to the
  colors and strategy.
- **8–12 card draw:** Combine repeatable engines with burst draw or selection so
  the deck can recover after interaction.
- **8–10 single-target removal:** Prefer low-cost, instant-speed answers with
  useful flexibility across permanent types.
- **2–4 board wipes:** Include a reset package suited to the table, including an
  asymmetrical option when the color identity and strategy support one.
- **3–5 win conditions or finishers:** Include dedicated ways to convert an
  established advantage into a win; efficient interaction or a tutor is not
  automatically a win condition.
- **3–6 protection or other interaction:** Protect the commander and engines,
  and reserve interaction for the threats that matter.
- **25–30 synergy and core-strategy cards:** Spend the remaining space on the
  commander's plan, redundancy, payoffs, and recovery rather than unrelated
  generically powerful cards.

These categories are functional lenses, so their ranges are not intended to
sum mechanically to 99. A card may have secondary roles, but use one primary
role for the category table.

Ask whether this commander already supplies a category and when it normally
starts supplying it. Count that supply when you judge the list, but do not
call a late commander early ramp or draw. Distinguish cards that work alone
from cards that need another permanent, a graveyard, or a token.

## Brackets

Published Commander Bracket rules (WotC, February 2026 update). Honor the
user's stated bracket or power. House rules override this table when they
conflict. Tutors are not bracket-restricted; efficient tutors that are Game
Changers still count against the Game Changer cap.

| Bracket | Name | Game Changers | Mass land denial | Extra turns | Two-card infinites | Expected floor |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Exhibition | None | No | None | No intentional | At least 9 turns |
| 2 | Core | None | No | Low quantity; do not chain | No intentional | At least 8 turns |
| 3 | Upgraded | Up to 3 | No | Allowed; do not chain as the plan | No intentional early-game | At least 6 turns |
| 4 | Optimized | Unrestricted | Yes | Yes | Yes | At least 4 turns |
| 5 | cEDH | Unrestricted | Yes | Yes | Yes | Any turn |

Card-level Game Changer source: Scryfall `game_changer`. Combo catalog and
bracket estimate: `rk-mtg-spellbook` `combos` and `rk-mtg-spellbook` `bracket`. Print a
compliance line per constraint the user actually supplied. Never claim
compliance for a price or a rule that is unresolved.

Do not add a hidden power target. Bracket 1 may stretch card legality when
the user says the theme needs it; confirm that in the pregame conversation.

## Evaluation rules

1. Prefer a high density of cheap early plays (mana value 1–2) that work
   before the commander, then adjust for the commander's plan. Average mana
   value in isolation is not the question; `rk-mtg-scryfall` `deck-stats` reports
   the histogram, the early-play count, and the tipping point, the mana value
   that gets 65% of the nonland spells online. Quote the tipping point rather
   than the average when describing how fast a deck is.
2. State a one-sentence **Deck Thesis** before listing cards. Every nonland
   card should advance that thesis, supply a needed function, or be a clearly
   justified exception.
3. Build redundancy first: aim for roughly **6–8 functional copies** of each
   core mechanic, using the commander as a source only when it is reliably
   available.
4. Avoid win-more cards. Prefer pieces that develop the plan, stabilize from
   behind, or rebuild after a board wipe.
5. Check Commander legality with `rk-mtg-scryfall` `validate-deck --final --resolve`,
   plus `--bracket N` when they named a bracket.

## Commander resources

If the commander adds mana, a discount, or permission to cast that is limited
by phase, spell type, or zone, list what that resource cannot pay for. Do not
count it as generic mana or as interaction on other players' turns.

## Recursion

Which zone does the list reuse: graveyard, exile, or battlefield? Do proposed
adds leave cards in a zone this list cannot recover? If yes, say so. Do not
add a rescue package for a rare miss in the wrong zone.

## Mana base

Does land count and fixing match pip pressure and colored sources from
`rk-mtg-scryfall` `deck-stats`, color count, ramp density, and budget if any?

If a budget exists, prefer cheaper fixing that still makes the colors. Keep
basics in play when the manabase needs them. Count always-tapped lands and
other delayed mana sources. When a card checks a property of other cards,
check that property across the whole list, not only a count of one card type.

## Win conditions

How does this list actually close a game? Do those lines survive the table
rules they stated? Tutors count only if the pieces they find are present.
"Good cards" is not a win condition. Ground catalogued combos with
`rk-mtg-spellbook` `combos`.

## Playtesting and iteration

`rk-mtg-goldfish` `stats` and opening-hand checks are useful for finding mana and
curve problems, but they are not evidence of multiplayer performance. Test
the deck in real games at the intended table, record what actually failed,
and distinguish a repeatable problem from a single unlucky game. Adjust the
list toward the observed failure, then recheck the functional counts,
dependencies, and constraints.

## Design rules

These checks sit on top of the baseline. They decide whether a card belongs.

1. **Read restricted commander resources as written.** Phase-, type-, or
   zone-locked mana is not generic mana.
2. **Thesis over theme count.** Do not add a creature type or brand card just
   to raise a tribal or theme count.
3. **Stated failure beats generic advice.** Keep the cards that already fix
   the player's actual losses until a new game shows a different hole more
   than once.
4. **Finishers versus floor.** If the list already has enough dedicated ways
   to win, do not add more expensive value spells. Do not fund those adds by
   cutting early defense. Cheap selection raises the floor but can pull a
   high-mana commander plan off thesis; add it only after clunky opening
   hands show more than once.
5. **Do not replace a unique closer.** If only one card turns a large mana
   surplus into a win, do not swap it for a safer card that does a different
   job. Casting a spell without paying its mana cost sets X to 0.
6. **Same job, prefer the instant.** When two cards do the same job and one is
   an instant, the sorcery is the weaker copy unless the sorcery has a second
   use the list needs.
7. **Read the exact zone, phase, mode, and floor.** Do not equate effects that
   share a category. Attack taxes, attacker caps, and bouncing attackers are
   different jobs. Bounce is delay. A copy effect with no other mode is empty
   when the stack is empty. Recursion follows a zone.
8. **One-mode mana when decisions hurt.** If the player asked for low decision
   complexity, prefer a single-mode source or give one default rule.
9. **Unspent budget is allowed.** Do not spend leftover value on off-plan
   cards to hit a cap.
10. **One primary role.** A card that also draws or finishes still occupies
    one primary role. Judge cheap versus expensive answers and the stated
    failure, not the raw interaction total. If a card is cut, name the
    capability that leaves with it.

## Required build or analysis output

When building or analyzing a deck, present:

1. **Deck Thesis** — one sentence describing the primary objective.
2. **Commander Overview** — why the commander enables that objective.
3. **Category counts** — a structured table using the functional categories
   above, with raw counts and no misleading quota score.
4. **Key Synergies & Combos** — three or four important interactions,
   including prerequisites and what can interrupt a combo line.

For a review, ground card claims in current Oracle text and distinguish
guaranteed combos from conditional synergies. Treat common deckbuilding
ratios as a starting hypothesis, not evidence that a particular card belongs.
