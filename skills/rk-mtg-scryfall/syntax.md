# Scryfall search cheatsheet

Full reference: https://scryfall.com/docs/syntax

Terms combine with AND unless you write `or`. Group with `( )`. Negate with `-` or `not:`.

## Color vs color identity

| Operator | Matches |
|----------|---------|
| `c:` / `color:` | The card's colors |
| `id:` / `identity:` | Color identity |

Letters: `w u b r g`. Nicknames work for guilds, shards, and wedges. `id:c` is colorless identity.

## Format vs commander-ness

| Query | Means |
|-------|--------|
| `f:commander` / `format:commander` | Legal in Commander |
| `banned:commander` | Banned in Commander |
| `is:commander` | Can be your commander |
| `is:gamechanger` | Commander Game Changer list |
| `is:partner` | Any Partner-style pairing |

`edhrec<=N` is the EDHREC rank ceiling (lower number is more popular).

## Oracle text

| Query | Means |
|-------|--------|
| `o:` / `oracle:` | Phrase in Oracle text |
| `o:"whenever ~"` | `~` is the card's name |
| `kw:` / `keyword:` | Keyword ability |
| `o:/^{T}:/` | Regex. Use when you need anchors |
| `fo:` / `fulloracle:` | Includes reminder text |

## Costs and stats

| Query | Means |
|-------|--------|
| `mv` / `manavalue` | Mana value |
| `m:` / `mana:` | Symbols in the cost |
| `produces:` | Makes that mana |
| `pow` `tou` `loy` | Combat / loyalty stats |

`is:hybrid` and `is:phyrexian` filter those cost shapes.

## Dedup, sort, prefer

| Query | When |
|-------|------|
| `unique:cards` | Default. One gameplay object per name |
| `unique:prints` | Every printing. Prices and art only |
| `unique:art` | Unique illustrations |
| `order:edhrec` `order:cmc` `order:usd` `order:eur` `order:released` | Sort |
| `prefer:usd-low` `prefer:eur-low` `prefer:newest` | Which printing to show |
| `cheapest:usd` `cheapest:eur` `cheapest:tix` | Cheapest print of each card |

## Lands

`is:fetchland`, `is:shockland`, `is:checkland`, `is:fastland`, `is:painland`, `is:slowland`, `is:dual`, `is:bounceland`, `is:surveilland`, `is:pathway`, `is:tricycleland`, `is:filterland`.
