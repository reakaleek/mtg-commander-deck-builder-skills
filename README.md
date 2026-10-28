# Commander deck builder skills

Seven Agent Skills for building, reviewing, piloting, and goldfishing Commander decks. Archidekt text is the list format. Install the whole repo. The Skills CLI does not resolve skill-to-skill dependencies, so installing only a high-level skill is incomplete.

The repository is private. GitHub auth is required.

```bash
npx skills add reakaleek/mtg-commander-deck-builder-skills
npx skills add reakaleek/mtg-commander-deck-builder-skills --list
```

Confirm the list shows all seven names: `mtg-deckbuilder`, `rk-mtg-commander-deck-playbook`, `rk-mtg-scryfall`, `rk-mtg-edhrec`, `rk-mtg-archidekt`, `rk-mtg-goldfish`, and `rk-mtg-spellbook`.

## Usage

Talk to the agent in plain language. The skill descriptions decide which skill starts. You do not run the helpers yourself unless you want a raw lookup.

### Build, review, or tune a deck

Ask to build an EDH deck, review or trim a list, pick cuts, or tell it how a game went. `mtg-deckbuilder` should start.

The skill is grounded in a fixed set of sources: three Command Zone episodes, one Commander Challenge video, TCGplayer's land-count regression, and Draftsim's mana-curve guide. Every target number (role counts, curve, land formula) lives in its single reference file, `principles.md`. The targets are starting points; your play experience outranks them.

Before anything else it establishes the table rules: bracket, Game Changer limit, budget and price basis, combo rules, pod meta. It reads them from memory or asks; none are built in. It never writes a deck file without your explicit OK on the specific swaps, and it presents every change as cut → add with the role and price delta.

**Build.** It defines the plan in two or three steps, fills the skeleton by role from EDHREC theme pages, and sets the land count with the formula. It then checks budget, Game Changers, and Spellbook combos, and writes an Archidekt-importable `quantity + exact name` list to `~/mtg/<deck>.txt` once you approve. After import, mark the command-zone card or cards as Commander in Archidekt. The text block cannot keep that flag.

**Review / cuts.** Bring an Archidekt URL or a local file. It tags every card by role, compares counts, curve, and lands against the skeleton, and names the three to five biggest problems. It proposes same-role swaps, then recounts everything as it would look after the changes.

**Playtest loop.** Tell it how a game felt, in your own words. It appends a dated entry to `~/mtg/<deck>.log.md`, reads the whole log, and only acts on patterns across games. It asks one to three follow-up questions if the report is vague, and records the swaps you accept on that entry.

### Pilot a finished deck

Ask for a deck playbook, how to play the list, mulligans, sequencing, combo lines, or a recovery plan. `rk-mtg-commander-deck-playbook` should start.

Bring the canonical file or the same Archidekt export. Confirm the command-zone cards if the export does not mark them. Say how experienced you are and how deep you want the guide.

The playbook explains the submitted list. It does not replace cards. If a line is missing a piece, it states the play limit and can hand you to `mtg-deckbuilder`. It writes Markdown in chat. It saves a file only if you ask.

This skill needs `rk-mtg-scryfall` so it can parse the list and read Oracle text. It does not need `rk-mtg-edhrec`. Metagame synergy is for choosing cards, not for teaching the cards already in the file. Combo cataloging uses `rk-mtg-spellbook` when that skill is installed.

### Goldfish or simulate a deck

Ask to goldfish a deck, test opening hands, play out turns, or run a mana-base check. `rk-mtg-goldfish` should start.

Bring the canonical file or a decklist, and say which cards are commanders if the file cannot mark them. For a turn-by-turn session it shuffles the library, deals an opening hand, and lets you mulligan, keep, and advance turns one command at a time, moving cards between hand, battlefield, graveyard, exile, and the command zone as you play them. For a fast mana-base check it runs many random shuffles instead and reports opening-hand and per-turn land odds; that check needs `rk-mtg-scryfall` first to identify which cards are lands. A 4-player simulation is one seat per decklist, each with its own state file.

This skill does not know Oracle text, mana costs, or legality on its own. It only tracks zones and turns.

### Look up cards, prices, EDHREC pages, an Archidekt URL, or combos

Ask about a card, a search, a price, or an Archidekt parse. `rk-mtg-scryfall` should start.

Ask what people play with a commander, inclusion, or high synergy. `rk-mtg-edhrec` should start.

Share an Archidekt deck link, or ask how to read one. `rk-mtg-archidekt` should start.

Ask which combos are in a list, or what bracket Spellbook estimates. `rk-mtg-spellbook` should start.

Those four skills return data. They do not build or review a deck, and they do not call `mtg-deckbuilder`.

### Example prompts

These are job shapes. Fill in your commander, list, path, and budget when you have them. Do not treat the wording below as table rules.

**Build**

> Build a Commander deck. I will give the commander and the table rules in chat. Show the list by role before you write the file.

**Review**

> Review this Archidekt deck. Name the biggest problems and propose same-role swaps with price deltas. Do not change the file until I accept a swap.

**Playtest**

> Log tonight's game with this deck: I lost on turn nine, stuck on four lands, and ran out of cards after a wipe. Only suggest changes if it's a pattern.

**Playbook**

> Write a playbook for this list. Cover mulligans, sequencing, and win lines. Do not change the deck.

> How do I pilot this deck? I want combo steps and a recovery plan. Save the playbook only if I ask.

**Goldfish**

> Goldfish this deck. Draw an opening hand, let me mulligan, then play out turns as I tell you what I cast.

> Run a mana-base check on this list. How often do I flood or get stuck on lands over the first 8 turns?

**Lookups**

> Price this list in my currency using cheapest prints unless a printing is supplied.

> Parse this Archidekt export and show the clean import block. Keep sideboard and maybeboard out of the deck.

> What do people play with this commander on EDHREC? Show high synergy and inclusion, not a new decklist.

> Fetch this Archidekt deck URL and show the clean import block.

> Which combos are in this list, and what does Spellbook estimate for bracket?

## What each skill needs

| Skill | Needs | Does |
| --- | --- | --- |
| `mtg-deckbuilder` | `rk-mtg-scryfall`, `rk-mtg-archidekt`, `rk-mtg-edhrec`, `rk-mtg-spellbook`; `rk-mtg-goldfish` optional. Works with reduced checks if one is missing | Build, role-count review, and playtest log loop |
| `rk-mtg-commander-deck-playbook` | `rk-mtg-scryfall` | Write a piloting guide. Never rewrite the deck file |
| `rk-mtg-scryfall` | nothing else | Oracle, legality, search, prices, parse, validate, deck-stats, write |
| `rk-mtg-edhrec` | nothing else | Unofficial inclusion, synergy, theme pages, and average-deck JSON |
| `rk-mtg-archidekt` | nothing else | Derive the API URL from a deck URL and fetch that deck's JSON |
| `rk-mtg-goldfish` | `rk-mtg-scryfall` for the mana-base check only | Shuffle, mulligan, and play turns round by round, or run a mana-base Monte Carlo check with screw, flood, and sweet-spot odds |
| `rk-mtg-spellbook` | nothing else | Unofficial combo catalog and bracket estimate |

If a skill stops and tells you to install the full repo, a helper is missing. Run the install command above again. Do not point the agent at a guessed disk path.

## Skills

- `mtg-deckbuilder` builds, reviews by role counts and a land formula, and tunes from a dated playtest log
- `rk-mtg-commander-deck-playbook` writes a piloting guide for a finished list and does not change that file
- `rk-mtg-scryfall` looks up Oracle text, legality, searches, prices, deck-stats, and Archidekt parse or validate
- `rk-mtg-edhrec` reads unofficial `json.edhrec.com` inclusion, synergy, theme, and average-deck pages
- `rk-mtg-archidekt` derives the API URL from an Archidekt deck URL and fetches that deck's JSON
- `rk-mtg-goldfish` shuffles a decklist and plays it out round by round, or runs a mana-base Monte Carlo check reporting screw, flood, and sweet-spot odds (using `rk-mtg-scryfall` to identify lands)
- `rk-mtg-spellbook` looks up catalogued combos and a bracket estimate for a list
