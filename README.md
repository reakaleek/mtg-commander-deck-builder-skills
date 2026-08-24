# Commander deck builder skills

Four Agent Skills for building, reviewing, and piloting Commander decks. Archidekt text is the list format. Install the whole repo. The Skills CLI does not resolve skill-to-skill dependencies, so installing only a high-level skill is incomplete.

The repository is private. GitHub auth is required.

```bash
npx skills add reakaleek/mtg-commander-deck-builder-skills
npx skills add reakaleek/mtg-commander-deck-builder-skills --list
```

## Skills

- `commander-deck-builder` interviews, then builds or reviews a list and keeps one canonical Archidekt-safe file
- `commander-deck-playbook` writes a piloting guide for a finished list and does not change that file
- `scryfall` looks up Oracle text, legality, searches, prices, and Archidekt parse or validate
- `edhrec` reads unofficial `json.edhrec.com` inclusion, synergy, and average-deck pages

`commander-deck-builder` needs `scryfall` and `edhrec`. `commander-deck-playbook` needs `scryfall`.
