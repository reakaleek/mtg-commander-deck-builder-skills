# Commander deck builder skills

Five Agent Skills for building, reviewing, and piloting Commander decks. Archidekt text is the list format. Install the whole repo. The Skills CLI does not resolve skill-to-skill dependencies, so installing only a high-level skill is incomplete.

The repository is private. GitHub auth is required.

```bash
npx skills add reakaleek/mtg-commander-deck-builder-skills
npx skills add reakaleek/mtg-commander-deck-builder-skills --list
```

Confirm the list shows all five names: `commander-deck-builder`, `commander-deck-playbook`, `scryfall`, `edhrec`, and `archidekt`.

## Usage

Talk to the agent in plain language. The skill descriptions decide which skill starts. You do not run the helpers yourself unless you want a raw lookup.

### Build a new deck

Ask to build a Commander deck. `commander-deck-builder` should start.

Bring what you already know:

- Commander, or say you want help picking one
- Theme and how you want to win
- Power or bracket, pet cards, house bans
- Budget only if you have one, plus currency. Say whether that means total list value or extra upgrade spend, whether owned cards count, and whether proxies are allowed.
- A path for the canonical deck file

The skill interviews first. It does not guess commander, budget, pets, or table rules. The last question is whether anything else matters. Answers there are hard constraints.

It then writes one Archidekt-safe text file at the path you approved. That file is the accepted list: only `quantity + exact Oracle name` per line. Partial builds may sit in the file until you call the deck final.

You get category counts, package notes, and a copy-only **Archidekt import** block that matches the file. After import, mark the command-zone card or cards as Commander or Premier in Archidekt. The text block cannot keep that flag.

The builder may offer a playbook when the list is final. It will not write one unless you ask.

### Review an existing list

Ask to review an EDH list, find synergies, or propose upgrades. Same skill.

Bring a pasted Archidekt export, an Archidekt deck URL, or a local file. If you already have a local file, say whether it should become the canonical file before anything overwrites it.

The review writes an upgrade strategy first, then ranked cut-to-add swaps. Each swap shows both Oracle texts. Proposed swaps stay in the report. The file changes only after you accept a swap or a batch.

You get two copy-only Archidekt blocks: the full accepted list, then a **buy list** of only the cards you still need to purchase. Say which cards you already own, and whether a proxy counts as owned. The buy list is not written into the canonical deck file.

If you set a budget, prices come from `scryfall` in the currency you named. Additional-spend budgets price the buy list. Missing prices stay unknown. Low EDHREC inclusion is not a cut reason by itself.

### Pilot a finished deck

Ask for a deck playbook, how to play the list, mulligans, sequencing, combo lines, or a recovery plan. `commander-deck-playbook` should start.

Bring the canonical file or the same Archidekt export. Confirm the command-zone cards if the export does not mark them. Say how experienced you are and how deep you want the guide.

The playbook explains the submitted list. It does not replace cards. If a line is missing a piece, it states the play limit and can hand you back to the builder. It writes Markdown in chat. It saves a file only if you ask.

This skill needs `scryfall` so it can parse the list and read Oracle text. It does not need `edhrec`. Metagame synergy is for choosing cards, not for teaching the cards already in the file.

### Look up cards, prices, EDHREC pages, or an Archidekt URL

Ask about a card, a search, a price, or an Archidekt parse. `scryfall` should start.

Ask what people play with a commander, inclusion, or high synergy. `edhrec` should start.

Share an Archidekt deck link, or ask how to read one. `archidekt` should start.

Those three skills return data. They do not build or review a deck, and they do not call the builder.

### Example prompts

These are job shapes. Fill in your commander, list, path, and budget when you have them. Do not treat the wording below as table rules.

**Build**

> Build a Commander deck. I will give the commander and the rest in chat. Ask until the constraints are clear, then write the canonical file.

> Help me pick a commander for a theme I will describe, then build the list. Ask about power, pets, and whether I have a budget before you write anything.

**Review**

> Review this Archidekt export. Write an upgrade strategy, then ranked swaps. End with a buy list of only the cards I still need to purchase. Do not change the file until I accept a swap.

> Review the list in this file. Ask if that file should become canonical. I will mark cards I already own. Propose budget-aware swaps only if I set a cap and a currency.

**Playbook**

> Write a playbook for this list. Cover mulligans, sequencing, and win lines. Do not change the deck.

> How do I pilot this deck? I want combo steps and a recovery plan. Save the playbook only if I ask.

**Lookups**

> Price this list in my currency using cheapest prints unless a printing is supplied.

> Parse this Archidekt export and show the clean import block. Keep sideboard and maybeboard out of the deck.

> What do people play with this commander on EDHREC? Show high synergy and inclusion, not a new decklist.

> Fetch this Archidekt deck URL and show the clean import block.

## What each skill needs

| Skill | Needs | Does |
| --- | --- | --- |
| `commander-deck-builder` | `scryfall`, `edhrec`, and `archidekt` | Interview, build or review, keep the canonical file |
| `commander-deck-playbook` | `scryfall` | Write a piloting guide. Never rewrite the deck file |
| `scryfall` | nothing else | Oracle, legality, search, prices, parse, validate, write |
| `edhrec` | nothing else | Unofficial inclusion, synergy, and average-deck JSON |
| `archidekt` | nothing else | Derive the API URL from a deck URL and fetch that deck's JSON |

If a high-level skill stops and tells you to install the full repo, a helper is missing. Run the install command above again. Do not point the agent at a guessed disk path.

## Skills

- `commander-deck-builder` interviews, then builds or reviews a list and keeps one canonical Archidekt-safe file
- `commander-deck-playbook` writes a piloting guide for a finished list and does not change that file
- `scryfall` looks up Oracle text, legality, searches, prices, and Archidekt parse or validate
- `edhrec` reads unofficial `json.edhrec.com` inclusion, synergy, and average-deck pages
- `archidekt` derives the API URL from an Archidekt deck URL and fetches that deck's JSON
