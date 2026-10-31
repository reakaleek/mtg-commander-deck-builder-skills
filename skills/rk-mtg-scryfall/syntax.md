# Scryfall search cheatsheet

Full reference: https://scryfall.com/docs/syntax · Regex: https://scryfall.com/docs/regular-expressions

Terms combine with AND unless you write `or`. Group with `( )`. Negate any keyword with `-`; `not:x` is `-is:x`. `!"Exact Name"` matches one card.

`or` splits the whole query, so put it in parentheses when other terms follow. `t:instant or t:sorcery id:ur` applies the identity to sorceries only; `(t:instant or t:sorcery) id:ur` applies it to both. `--commander` adds these parentheses for you.

## Color vs color identity

| Query | Matches |
|-------|---------|
| `c:` / `color:` | The card's colors (`c:u` excludes lands and colorless cards for free) |
| `id:` / `identity:` / `ci:` | Color identity, that identity or less |
| `id<=sultai` | Playable under that commander. Same results as `id:sultai`; the `<=` is the clearer way to write it |
| `id=wgu is:commander` | Commanders of exactly those colors; `id=` is the exact match |
| `c=2`, `c:m`, `c:c` | Exactly two colors, multicolor, colorless |
| `id:m` | Multicolor identity, including lands and mana rocks that `c:m` misses |

Letters: `w u b r g`. Guild, shard, wedge, college (`quandrix`) and four-color (`chaos`, `aggression`, `altruism`, `growth`, `artifice`) nicknames work. `id:c` is colorless identity. Comparisons: `> < >= <= !=`.

## Types and text

| Query | Means |
|-------|--------|
| `t:` / `type:` | Any supertype, type, or subtype; partial words work (`t:legend`) |
| `o:` / `oracle:` | Phrase in current Oracle text; quote phrases with spaces |
| `fo:` / `fulloracle:` | Also searches reminder text (`fo:clue` finds investigate cards that `o:clue` misses) |
| `~` | The card's own name inside `o:` (`o:"~ enters tapped"`) |
| `kw:` / `keyword:` | Cards that have the keyword ability. `o:flying` also matches "destroy target creature with flying" |
| `lore:` | Name in the card's title or flavor text (`lore:chandra`) |
| `t:X or o:X` | Typal check: cards of a type plus cards that mention it |

## Costs and stats

| Query | Means |
|-------|--------|
| `mv` / `manavalue` / `cmc` | Mana value; `mv:even`, `mv:odd` |
| `m:` / `mana:` | Symbols in the cost; `m>3WU` compares cost sets; wrap hybrid/Phyrexian in braces `m:{R/P}` |
| `devotion:` | Devotion contributed, e.g. `devotion:{u/b}{u/b}` |
| `produces:` / `produces=wu` | Mana the card can make |
| `pow` `tou` `pt` `loy` | Stats; compare to numbers, each other, or mana value (`pow>tou`, `mv<tou`) |
| `is:hybrid` `is:phyrexian` | Cost shapes |

## Card kinds

`is:spell`, `is:permanent`, `is:historic`, `is:modal`, `is:vanilla`, `is:frenchvanilla`, `is:bear`, `is:manland`, `is:party`, `is:outlaw`, `is:etb` (cares about entering the battlefield), `is:ub` (Universes Beyond; `-is:ub` to exclude); faces: `is:mdfc`, `is:dfc`, `is:transform`, `is:split`, `is:flip`, `is:meld`.

## Format, Commander, popularity

| Query | Means |
|-------|--------|
| `f:commander` / `legal:edh` | Legal in Commander; `banned:commander` for the ban list |
| `is:commander` | Can be your commander; `is:partner` any partner-style pairing |
| `is:gamechanger` | On the Commander Game Changer list |
| `is:reserved` | Reserved List (rarely reprinted, often pricey) |
| `edhrec<=N` | EDHREC rank ceiling: lower number is more played. Use `edhrec>N` to find less-played cards |
| `game:paper` | Has a paper printing (drops digital-only Alchemy cards) |

## Prices

`eur<2`, `usd<=1`, `tix>5` match a card if **any** printing is in range. Add `cheapest:eur` (or `prefer:eur-low`) to show that cheapest print. Use the `prices` command, not search results, to total a list.

## Sets, dates, reprints

| Query | Means |
|-------|--------|
| `s:` / `e:` / `set:` | Set code. Commander decks often have their own code (`mkm` vs `mkc`) |
| `g:` / `group:` | The set plus its Commander, token, and other related sets |
| `st:commander` | Any Commander product |
| `year=2026`, `date>=2026-03-01` | Release window |
| `date>=CODE` | Released on or after that set (a set code stands in for its date); `date>now` for unreleased |
| `not:reprint` | New in that set; `-is:reprint` is the same |
| `is:firstprint` | Shows each card's original printing |
| `prints=1` / `papersets=1` | Printed once (often expensive or overlooked) |

## Regular expressions

Use `/.../` instead of quotes with `o:`, `t:`, `ft:`, `name:`. Case-insensitive. `^`/`$` anchor to each ability paragraph. No flags (`o:/x/i` fails), no backreferences; escape `/` as `\/`.

Scryfall shorthands: `~` card name, `\sm` any mana symbol, `\sc` colored mana symbol, `\ss` any card symbol, `\spt` X/X, `\spp` +X/+X, `\smm` -X/-X, `\smh` hybrid, `\smp` Phyrexian.

| Query | Finds |
|-------|-------|
| `t:creature o:/^{T}:/` | Creatures with a free tap ability |
| `t:instant o:/\spp/` | Instants that grant +X/+X |
| `o:/\borcs?\b/` | Mentions of orcs, not "sORCery" |
| `o:/put.*counter.* on ~/` | Puts counters on itself, with the words in that order |

## Tagger tags

`otag:` / `function:` / `oracletag:` search community function tags; `art:` / `atag:` / `arttag:` search illustration tags. Tag names are kebab-case and easy to guess wrong (`otag:card-draw` does not exist). Look names up with `tags <word>`, see which ones a card has with `card-tags '<name>' --pattern <word>`, and check `unknown_tags` in search output. `art:` matches any printing, so add `unique:art` to see every matching illustration. Role-to-tag map and caveats: [finding-cards.md](finding-cards.md).

## Dedup, sort, prefer

| Query | When |
|-------|------|
| `unique:cards` | Default. One gameplay object per name |
| `unique:prints` | Every printing. Prices and art only |
| `unique:art` | Unique illustrations |
| `order:edhrec` `order:cmc` `order:usd` `order:eur` `order:released` | Sort; add `direction:asc` or `direction:desc` |
| `prefer:usd-low` `prefer:eur-low` `prefer:newest` | Which printing to show |
| `cheapest:usd` `cheapest:eur` `cheapest:tix` | Cheapest print of each card |

## Lands

`is:fetchland`, `is:shockland`, `is:checkland`, `is:fastland`, `is:painland`, `is:slowland`, `is:dual`, `is:bounceland`, `is:surveilland`, `is:scryland`, `is:gainland`, `is:pathway`, `is:tricycleland`, `is:filterland`, `is:snarl` (`is:shadowland`), `is:bondland`, `is:canopyland`, `is:creatureland`.
