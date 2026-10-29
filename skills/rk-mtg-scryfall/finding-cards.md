# Finding cards that fit

A search method for "what should go in this slot". It returns candidates; the caller judges them. Syntax details: [syntax.md](syntax.md).

## 0. Order of sources

1. **EDHREC first** for picks that players agree fit the commander: `rk-mtg-edhrec candidates <commander> --theme <the deck's themes> --exclude <deck file>`.
2. **Scryfall next** for what EDHREC under-samples: underplayed fits, new cards, and budget picks. Use the searches below.
3. **Then widen**, if the pool is thin: EDHREC `card` on the deck's key engine piece, or `candidates` for the commanders in `similar`.

## 1. Lock the frame first

Start every candidate search with the deck's hard filters, so nothing illegal, off-budget, or already in the deck shows up:

```
search '-t:land <role or theme terms>' --commander '<Commander>' --exclude <deck file>
```

`--commander` adds `id<=<identity> f:commander game:paper`, and `--exclude` drops the deck's current cards. Without the helper, write the frame by hand: `id<=<commander colors> f:commander game:paper -t:land`.

Add as the table requires: `-is:gamechanger` once the Game Changer cap is used, `eur<N` / `usd<N` for a per-card ceiling (any printing counts, see syntax.md), `-is:reserved` when reprint risk matters.

## 2. Four ways in

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

**b. From the commander's own words.** Lift its trigger phrase and search it in both directions:
- payoffs that share the trigger: `o:"whenever you cast a creature spell"`
- cards that cause the event: if the commander rewards power 4+, `t:creature pow>=4 mv<=3`

Use `fo:` when the mechanic lives in reminder text, and regex when the wording varies (`o:/whenever .* (dies|is put into a graveyard)/`).

**c. From a card that already works.** Copy its exact template wording into `o:"..."`; the precise phrase cuts noise far more than a keyword. Or find its tags:
1. List candidate tags with `tags <theme word>`.
2. Confirm one with `search '!"Card Name" otag:<tag>'`; 1 result means the card has it.
3. Search that tag inside the frame.

**d. By theme tag.** Families worth grepping with `tags`: `synergy-*`, `*-matters`, `repeatable-*`, `gives-*`, `cast-trigger*`, `death-trigger*`, `landfall`, `counter-*`.

## 3. Rank, then look past the top

- `order:edhrec` puts the most-played fits first: good for a baseline.
- **Underplayed fits:** keep the same query and add `edhrec>N` (a higher rank number means less played), or sort `order:edhrec direction:desc`.
- **New cards:** `date>=<newest set code>` or `year=<year> not:reprint`.
- **Budget:** `order:eur` with `cheapest:eur`.

## 4. Verify before proposing

- **Read every candidate's Oracle text.** Tags and `o:` are leads, not verdicts. `o:draw` also matches "can't draw", and tags are community-made and incomplete.
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

Sources: Scryfall syntax, regex and Tagger tag docs; Doug Young, "The Ultimate Scryfall Primer" (Commander's Herald, 2024); Cooper Gottfried, "Guide to Scryfall Syntax" (EDHREC); Sheldon Menery, "Finding Priceless Treasures in Commander" (Star City Games, 2015).
