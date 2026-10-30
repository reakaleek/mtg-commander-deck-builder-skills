# Commander archetypes

What each common archetype needs, what pulls against it, and what hurts it. The plan step (SKILL.md A.2, B.3) names one archetype, or a declared hybrid of two. A third theme is a side plan (§4 one direction, trap 3).

General numbers (role targets, curve, lands, evals) stay in [principles.md](principles.md). This file holds only archetype-specific ones.

Sources: **D1** Draftsim "27 EDH Archetypes Plus Example Decks" (Timothy Zaccagnino, updated 2026-06-03): definitions and core parts · **ED** EDHREC tag pages (`json.edhrec.com/pages/tags/…`), read live through `rk-mtg-edhrec`: popularity, signature cards, top commanders · **V1**, **V2**, **V4**, **V5** as in principles.md · **card text**: what a hate piece does, read from its Oracle text.

Anything else is marked *own opinion*. No source gives per-archetype counts beyond the few cited here.

## How to use it

1. **Find candidates.** Take the commander's `rk-mtg-edhrec themes` (always include its top few: they can name a shape this file has no block for, such as cost-reduced spells), add the archetypes below that fit its text, and run `archetype-match <deck> --colors <WUBRG> --tag …` with 3–5 slugs. The top score is the likely archetype. A lower tag with several `exclusive` cards is a possible side package or the second half of a hybrid: read them, and the playbook if there is one, before calling it either. Tags that share most of their matches and have no `exclusive` cards are one plan seen from two angles, not two plans.
2. **Confirm with the user.** The archetype decides which cards count as Enabler, Payoff or off-plan (§1), so confirm it before tagging.
3. **Check the block** for that archetype (E28): parts present, floors met, no contention package, weak points covered. The blocks describe the usual shape. When the commander supplies or inverts a part (§4 commander role), map the parts to this deck before counting: say which cards fill each part, and count the commander's own text as that part only under the parts rule below.
4. **Find adds** with `rk-mtg-edhrec tag <slug> --colors <WUBRG> --exclude <deck>` alongside the commander's `candidates`. Tag pages cover all commanders, so check every card against this commander's text (scryfall finding-cards fit check).

**Parts rule** (*own extension of §5's copy math, not from a source*): every part listed under **Parts** needs at least 3 cards, the §5 count that gives about a 59% chance to see one in ~25 cards. Only the commander covers a part on its own, and then only if the deck survives its removal (E8). A part with fewer than 3 cards is an E28 failure.

## Archetypes

Each block lists: **Wins** · **Parts** (the plan's steps, in §1 tag terms) · **Floors** · **Contention** · **Weak to** · **Speed** (§1a early-weak or late-weak) · **Hybrids** · **Slugs** (EDHREC tags).

### Go-wide tokens
- **Wins**: flood the board, then turn the army into a win with an Overrun- or Impact Tremors-style effect (D1).
- **Parts**: token makers (Enabler); mass pump or "creature enters" drain (Payoff); token doublers (Enhancer, D1 calls them staples).
- **Floors**: none sourced; E4 applies.
- **Contention**: go-wide pump vs. sacrifice drain; an overrun finisher vs. death-trigger payoffs (V1, §4).
- **Weak to**: creature wipes; see §1a for what it can skip.
- **Speed**: late-weak once boards stall (*own opinion*); check §1a.
- **Hybrids**: aristocrats, sharing "a creature enters/dies" fodder; commit to one finisher (V1).
- **Slugs**: `tokens`.

### Aristocrats / sacrifice
- **Wins**: drains from death triggers, sometimes via a combo loop (D1).
- **Parts**: sacrifice outlets, fodder, death-trigger payoffs: "three key elements" (D1). Fodder and outlets are Enablers; drain triggers are Payoffs.
- **Floors**: Parts rule for each of the three.
- **Contention**: counters vs. sacrificing their holders; hoard vs. sacrifice clues (V1, §4).
- **Weak to**: graveyard exile and "dies" trigger stoppers (card text: Rest in Peace exiles instead of dying-to-graveyard, which turns off "dies" triggers); creature wipes are less harmful because the deck sacrifices in response (*own opinion*).
- **Speed**: early-weak while assembling outlet + payoff (*own opinion*).
- **Hybrids**: tokens; reanimator for recursion of fodder.
- **Slugs**: `aristocrats`, `sacrifice`.

### +1/+1 counters
- **Wins**: grow huge threats and win through combat damage (D1).
- **Parts**: counter placers (Enabler); "has a counter" payoffs (Payoff); counter doublers (Enhancer, "force multipliers", D1).
- **Floors**: none sourced; E4 applies.
- **Contention**: counters vs. sacrificing their holders (V1).
- **Weak to**: creature wipes, since the counters go with the creatures (*own opinion*).
- **Speed**: late-weak against blockers (*own opinion*).
- **Slugs**: `plus-1-plus-1-counters`.

### Voltron
- **Wins**: suit up one creature, usually the commander, into a hard-to-stop threat; few other creatures (D1).
- **Parts**: equipment or auras (Enabler); evasion and protection (Enabler per §1 plan row); the commander as the threat.
- **Floors**: Parts rule for protection: the plan dies with the one creature (E8).
- **Contention**: a go-wide package; auras vs. equipment are compatible only with payoffs for both (*own opinion*).
- **Weak to**: edicts, chump blockers, Maze of Ith-style lands and enchantment-based answers (V5, §1a).
- **Speed**: late-weak; needs closers that clear blockers (§1a).
- **Slugs**: `voltron`, `equipment`, `auras`.

### Spellslinger
- **Wins**: instants and sorceries trigger payoffs ("whenever you cast…").
- **Parts**: cheap instants and sorceries (Enabler); cast triggers (Payoff); copy effects (Enhancer).
- **Floors**: 25–30 instants and sorceries before spell payoffs work (V2).
- **Contention**: a creature-combat package that takes spell slots (*own opinion*).
- **Weak to**: counterspells and taxes on noncreature spells (card text); creature wipes barely touch it (*own opinion*).
- **Speed**: holds mana up; prefer instant-speed answers (§1a on-plan answers).
- **Cost-reduction variant**: when the commander or affinity makes the spells cheap (e.g. "spells cost {1} less for each creature you control"), the shape inverts: what the reduction counts (creatures, artifacts) is the Enabler and the big or X spells are the Payoff, so few "whenever you cast" cards is expected. The 25–30 floor still applies (V2).
- **Hybrids**: storm, wheels.
- **Slugs**: `spellslinger`, `storm`; for the cost-reduction variant also `affinity`, `x-spells`.

### Reanimator / graveyard
- **Wins**: fill the graveyard and use it as a second hand (D1).
- **Parts**: self-mill and discard (Enabler); reanimation and recursion (Payoff); big creatures worth returning.
- **Floors**: non-stacking effects need only 2–3 copies with self-mill and recursion (V1, §5 E5).
- **Contention**: exiling your own graveyard for value (*own opinion*).
- **Weak to**: graveyard hate, both continuous and one-shot (card text: Rest in Peace, Grafdigger's Cage); it also feeds opponents' graveyard decks, so it runs extra graveyard hate itself (V5, §1a).
- **Speed**: can be fast; check E14 power fit.
- **Slugs**: `reanimator`, `graveyard`, `self-mill`.

### Blink / flicker
- **Wins**: reuse enter-the-battlefield value until it buries the table.
- **Parts**: ETB creatures (Enabler); blink effects (Payoff, or Enhancer if they double triggers).
- **Floors**: Parts rule for blink effects.
- **Weak to**: ETB-trigger stoppers (card text: Torpor Orb); wipes take ETB creatures and repeatable blinkers together (*own opinion*).
- **Speed**: early-weak; value accrues slowly (*own opinion*).
- **On-plan answers**: ETB-removal creatures (V5, §1a).
- **Slugs**: `blink`.

### Lands / landfall
- **Wins**: uses lands beyond tapping for mana, often via landfall triggers (D1).
- **Parts**: extra land drops and fetches (Enabler); landfall payoffs (Payoff).
- **Weak to**: land destruction and "enters tapped" or "lands don't untap" taxes (card text).
- **On-plan answers**: removal lands (V5, §1a). Lands are the hardest permanent type to remove (V4, §4 rebuild).
- **Slugs**: `landfall`, `lands-matter`.

### Artifacts
- **Wins**: artifact count or artifact triggers power the plan (D1 "Affinity/Artifacts").
- **Parts**: cheap artifacts and makers (Enabler); artifact-count or artifact-enters payoffs (Payoff).
- **Contention**: hoard clues vs. sacrifice clues (V1).
- **Weak to**: artifact wipes (card text).
- **Slugs**: `artifacts`.

### Enchantress
- **Wins**: enchantments drive draw and payoffs (D1).
- **Parts**: enchantments (Enabler); "whenever you cast an enchantment" draw (Payoff).
- **Weak to**: enchantment wipes (card text).
- **Slugs**: `enchantress`.

### Typal
- **Wins**: rewards for one creature type (D1). Generic typal support plus type-specific payoffs (D1).
- **Parts**: on-type creatures (Enabler); lords and typal payoffs (Payoff).
- **Floors**: none sourced; E4 applies.
- **Weak to**: creature wipes (*own opinion*).
- **Slugs**: the tribe itself (`elves`, `dragons`, …); list them with `tags --all --grep <type>`.

### Lifegain
- **Wins**: gain life and trigger lifegain payoffs; often a one-shot finisher; naturally harder to kill (D1).
- **Parts**: repeatable lifegain (Enabler); lifegain triggers (Payoff); one-shot finishers (Wincon, non-stacking per §5).
- **Weak to**: a deck that gains life but has no closer stalls (E2, *own opinion*).
- **Slugs**: `lifegain`.

### Aikido / group slug
- **Wins**: damage or punish the whole table, or turn opponents' damage back on them (aikido: redirect and reflect effects; *own opinion* from player usage, no editorial source found).
- **Parts**: "each opponent" punishers or redirect effects (Payoff); effects that keep the deck alive while they work (Enabler).
- **Scaling**: "each opponent" triggers fire 3× as often in four-player games (V4, §5).
- **Weak to**: lifegain and a single fast opponent; the deck needs the game to last (*own opinion*).
- **Speed**: early-weak (*own opinion*).
- **Slugs**: `group-slug`, `aikido`.

### Stax / control
- **Wins**: control answers threats at instant speed and has few wincons; it often adds a combo finish (D1). Stax slows everyone with taxes and locks (D1 lists it).
- **Parts**: counters, wipes, flash threats (D1) as Enablers; a small set of wincons (Payoff).
- **Floors**: disruption above the §1 targets; grindy control runs 20+ (V5, §1a).
- **Weak to**: running out of wincons; check E2 and E23 (*own opinion*).
- **Speed**: early-weak (§1a).
- **Table**: Mass-heavy decks are disliked (V2, §1); check pod rules (E14).
- **Slugs**: `control`, `stax`.

### Group hug
- **Wins**: hands out resources and wins through a closer or politics (D1 lists it).
- **Parts**: symmetric draw and ramp (Enabler); a way to cash it in first (Payoff).
- **Scaling**: symmetric "any player" triggers fire only 2× as often (V4, §5).
- **Weak to**: feeding the strongest opponent (*own opinion*).
- **Slugs**: `group-hug`.

### Combo
- **Wins**: assembles a few specific cards, with tutors and dig to find them; fewer pieces are easier (D1).
- **Parts**: combo pieces (Wincon); tutors and dig (Selection, Draw); protection.
- **Floors**: check the table's combo rules first (E1, `rk-mtg-spellbook`).
- **Weak to**: graveyard or artifact hate that hits the pieces; answers that share a weakness (trap 4).
- **Slugs**: `combo`.

### Aggro
- **Wins**: kills with damage as fast as possible, through combat or burn; vulnerable to wipes; plays the most efficient threat at each point on the curve (D1).
- **Parts**: cheap threats (Enabler); pump and haste (Payoff).
- **Speed**: late-weak; needs closers that clear blockers (§1a). Disruption can run below target, never zero (§1a).
- **Slugs**: `aggro`.

### Power-matters / stompy
- **Wins**: casts creatures with high power, and payoffs keyed to power (draw, damage, cost reduction) turn each cast into value; the bodies close in combat (ED `power-matters` and `stompy` tags; the rest of this block is *own opinion*, drafted from a deep review).
- **Parts**: high-power creature spells (Enabler); ways to cast them cheaply that still count as casting: cost reducers, warp, evoke, foretell, and cheap bodies with a drawback (Enabler); power payoffs (Payoff); closers that give haste or trample (Enabler per the §1 plan row). Count a creature by its power on the stack if the payoff checks the spell, so a body that enters with -1/-1 or stun counters still counts at full power.
- **Floors**: about 20 creature spells at the payoff's power threshold, so a cast trigger fires about once a turn (*own opinion*). Parts rule for each part.
- **Contention**: cheats that put creatures onto the battlefield (they skip cast triggers) vs. the cast-trigger payoff; sacrifice value vs. bodies kept for combat (*own opinion*).
- **Weak to**: losing the commander when it is the payoff (E8); creature wipes; chump blockers and fogs for the combat half. Countered creature spells still fire cast triggers (card text) (*own opinion*).
- **Speed**: early-weak while ramping, then late-strong (*own opinion*); check §1a.
- **Table**: a commander that damages each opponent shows its clock and draws attacks (§4 hide the finish, E23). Prefer burst turns from hand over early pings.
- **Hybrids**: Ramp / big spells; +1/+1 counters when the payoff grows the commander.
- **Slugs**: `power-matters`, `stompy`.

### Ramp / big spells
- **Wins**: drops finishers ahead of schedule; often skips mid-game 4- and 5-drops (D1).
- **Parts**: ramp above the §1 target (§1 "ramp-matters plan"); big threats (Payoff).
- **Speed**: early-weak (§1a).
- **Slugs**: `ramp`.

### Wheels
- **Wins**: everyone discards and draws new hands; payoffs for draw, discard, draw hate or the graveyard (D1).
- **Parts**: wheel effects (Enabler); draw and discard payoffs (Payoff).
- **Contention**: refilling opponents' hands without a payoff that punishes it (*own opinion*).
- **Slugs**: `wheels`.
