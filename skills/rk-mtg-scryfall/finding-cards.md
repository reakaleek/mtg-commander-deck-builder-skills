# Finding cards that fit

A search method for "what should go in this slot". It returns candidates; the caller judges them. Syntax details: [syntax.md](syntax.md).

## 0. Order of sources

1. **EDHREC first** for picks that players agree fit the commander: `rk-mtg-edhrec candidates <commander> --theme <the deck's themes> --exclude <deck file>`.
2. **Scryfall next** for what EDHREC under-samples: underplayed fits, new cards, and budget picks. Use the searches below.
3. **Then widen**, if the pool is thin: EDHREC `card` on the deck's key engine piece, or `candidates` for the commanders in `similar`.

Start with Scryfall instead for a brand-new commander, a rare partner pairing, or a build unlike the usual one. EDHREC has little data there, and its lists partly repeat what earlier builders copied from it.

## 1. Lock the frame first

Start every candidate search with the deck's hard filters, so nothing illegal, off-budget, or already in the deck shows up:

```
search '-t:land <role or theme terms>' --commander '<Commander>' --exclude <deck file>
```

`--commander` adds `id<=<identity> f:commander game:paper`, and `--exclude` drops the deck's current cards. Without the helper, write the frame by hand: `id<=<commander colors> f:commander game:paper -t:land`.

Add as the table requires: `-is:gamechanger` once the Game Changer cap is used, `eur<N` / `usd<N` for a per-card ceiling (any printing counts, see syntax.md), `-is:reserved` when reprint risk matters, `-is:ub` when the table or the theme rules out Universes Beyond.

## 2. Five ways in

**a. By role.** Use the tag that matches the role, not the broadest one. Verified on live searches (counts drift; names were checked against Scryfall's tag list):

| Role | Use | Watch out |
|------|-----|-----------|
| Ramp | `otag:mana-rock`, `otag:mana-dork`, `otag:land-ramp`, `otag:cost-reducer` | `otag:ramp` also includes rituals |
| Draw (net card gain) | `otag:draw-engine`, `otag:repeatable-draw`, `otag:impulse-draw` | `otag:draw` and `otag:card-advantage` include cantrips and looters; `otag:repeatable-pure-draw` still has one-shot cards |
| Selection / tutors | `otag:cantrip`, `otag:loot`, `otag:tutor`, `otag:wheel` | Not net card advantage |
| Targeted answers | `otag:creature-removal`, `otag:artifact-removal`, `otag:enchantment-removal`, `otag:removal-exile`, `otag:edict`, `otag:counterspell`, `otag:removal-fight` | `otag:removal` is very broad |
| Mass answers | `otag:sweeper` (aliases `board-wipe`, `mass-removal`), `otag:fog`, `otag:graveyard-hate` | |
| Protection | `otag:protects-creature`, `otag:gives-indestructible`, `otag:gives-hexproof`, `otag:protection` | |
| Engines and outlets | `otag:sacrifice-outlet`, `otag:discard-outlet`, `otag:reanimate`, `otag:recursion-permanent`, `otag:blink`, `otag:theft`, `otag:gives-haste` | |
| Combat-damage payoffs | `otag:saboteur` | Catches "one or more creatures deal combat damage" wording that `o:"deals combat damage"` misses |
| Counters and mana sinks | `otag:counters-matter`, `otag:mana-sink` | |

**b. From the commander's own words.** Lift its trigger phrase and search it in both directions:
- payoffs that share the trigger: `o:"whenever you cast a creature spell"`
- cards that cause the event: if the commander rewards power 4+, `t:creature pow>=4 mv<=3`

Use `fo:` when the mechanic lives in reminder text, and regex when the wording varies (`o:/whenever .* (dies|is put into a graveyard)/`).

**c. From a card that already works.** The commander itself is a good first choice. Copy its exact template wording into `o:"..."`; the precise phrase cuts noise far more than a keyword. Or find its tags:
1. Run `card-tags '<Card Name>' --pattern <theme word>` to see which matching tags the card has. Try a few words: the pattern narrows what gets tested.
2. Search a tag inside the frame.
3. If a result shows wording you had not thought of, take that phrase into `o:"..."` and search again.

**d. By theme tag.** Families worth grepping with `tags`: `synergy-*`, `*-matters`, `repeatable-*`, `gives-*`, `cast-trigger*`, `death-trigger*`, `landfall`, `counter-*`.

**e. By flavor.** For a themed deck, use `art:<subject>` with `unique:art`, which also finds alternate printings of cards you already know, and `lore:<name>` for cards that name a character in the title or flavor text. Check the printing the art is on before proposing a card for its art.

## 3. Rank, then look past the top

- `order:edhrec` puts the most-played fits first: good for a baseline.
- **Underplayed fits:** keep the same query and add `edhrec>N` (a higher rank number means less played), or sort `order:edhrec direction:desc`.
- **New cards:** `date>=<newest set code>` or `year=<year> not:reprint`.
- **Budget:** `order:eur` with `cheapest:eur`.

## 4. Verify before proposing

- **Read every candidate's Oracle text.** Tags and `o:` are leads, not verdicts. `o:draw` also matches "can't draw", and tags are community-made and incomplete.
- **Tighten text searches.** Separate `o:` terms match anywhere on the card: `o:draw o:card` finds Smothering Tithe, which never draws you a card. Use `kw:` for keywords, and `o:cards` to drop cantrips that draw one card.
- **For recall, union tag and text:** `(otag:sweeper or o:"destroy all")`.
- **Check `unknown_tags` is empty.** A misspelled tag returns nothing on its own, and inside `or` or `-` it silently changes the results.
- **Check the deck still passes.** Run `validate-deck --resolve` for legality, identity and Game Changers, and `prices` for the real cheapest-print cost.

## 5. Fit check

A candidate that matches the search does not yet fit the deck. Before proposing it, write one line for each check:

- **Job:** the plan step it advances or the failed eval it fixes. "Good card" is not a job.
- **Curve:** its mana value fills a gap in `deck-stats`, or at least does not add to the biggest bulge.
- **Roles:** it fills two roles, or the line says why one is enough here.
- **Price:** it fits the budget left for this slot, priced the cheapest way.
- **Swap:** in this deck, judged on Oracle text and not on tags, it does more than the card it replaces.

Drop candidates that fail a check. Show the user the best 3–5 per slot, not the whole list.

Sources: Scryfall syntax, regex and Tagger tag docs; Doug Young, "The Ultimate Scryfall Primer" (Commander's Herald, 2024); Cooper Gottfried, "Guide to Scryfall Syntax" (EDHREC); Sheldon Menery, "Finding Priceless Treasures in Commander" (Star City Games, 2015); "Master Deck Building w/ These Scryfall Hacks" (The Command Zone #608).
