#!/usr/bin/env python3
"""Check skill frontmatter, repo hygiene, and builder/playbook constraints."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

REQUIRED = {
    "commander-deck-builder": ("SKILL.md", "guides.md"),
    "commander-deck-playbook": ("SKILL.md", "playbook.md"),
    "scryfall": ("SKILL.md", "syntax.md", "scripts/scryfall.py"),
    "edhrec": ("SKILL.md", "scripts/edhrec.py"),
}

BUILDER_DOCS = [
    SKILLS / "commander-deck-builder" / "SKILL.md",
    SKILLS / "commander-deck-builder" / "guides.md",
    SKILLS / "commander-deck-playbook" / "SKILL.md",
    SKILLS / "commander-deck-playbook" / "playbook.md",
]

BANNED_SUBSTRINGS = (
    "~/.cursor/skills/",
    "mtg-commander-review",
)

BANNED_CARD_NAMES = (
    "Sol Ring",
    "Command Tower",
    "Arcane Signet",
    "Rhystic Study",
    "Smothering Tithe",
    "Demonic Tutor",
    "Cyclonic Rift",
    "Fierce Guardianship",
    "Deflecting Swat",
    "Teferi's Protection",
    "Dockside Extortionist",
    "Jeweled Lotus",
    "Mana Crypt",
    "Mana Vault",
    "The One Ring",
    "Atraxa",
    "The Ur-Dragon",
    "Korvold",
    "Kenrith",
    "Yuriko",
    "Wilhelt",
    "Edgar Markov",
    "Muldrotha",
    "Kinnan",
    "Najeela",
    "Winota",
    "Tymna",
    "Thrasios",
    "Kraum",
    "Rograkh",
    "Silas Renn",
    "Kodama of the East Tree",
)

TARGET_PATTERNS = (
    re.compile(r"\b\d+\s+(lands?|ramp|draw|rocks?|tutors?|interaction)\b", re.I),
    re.compile(r"\bstart at\b", re.I),
    re.compile(r"\bdefault (?:budget|cap|land count)\b", re.I),
    re.compile(r"\b250\s*(?:eur|usd|€|\$)?\b", re.I),
    re.compile(r"\bcommand zone recipe\b", re.I),
    re.compile(r"\bfor example,?\s+if they\b", re.I),
    re.compile(r"\bno extra turns\b", re.I),
    re.compile(r"\bmy playgroup\b", re.I),
)

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def scan_repo_text() -> list[Path]:
    skip_dirs = {".git", "__pycache__"}
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if any(part in skip_dirs for part in path.parts):
            continue
        if path.is_file() and path.suffix in {".md", ".py", ".txt"}:
            files.append(path)
    return files


def main() -> int:
    errors: list[str] = []

    for name, rels in REQUIRED.items():
        skill_dir = SKILLS / name
        if not skill_dir.is_dir():
            fail(errors, f"missing skill directory: {name}")
            continue
        for rel in rels:
            if not (skill_dir / rel).is_file():
                fail(errors, f"missing {name}/{rel}")

        skill = skill_dir / "SKILL.md"
        if skill.is_file():
            meta = frontmatter(skill.read_text(encoding="utf-8"))
            if meta.get("name") != name:
                fail(errors, f"{name}/SKILL.md name must be {name!r}")
            if not meta.get("description"):
                fail(errors, f"{name}/SKILL.md missing description")

    for path in scan_repo_text():
        if path.resolve() == Path(__file__).resolve():
            continue
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        for banned in BANNED_SUBSTRINGS:
            if banned in text:
                fail(errors, f"{rel} contains {banned}")

    builder = SKILLS / "commander-deck-builder" / "SKILL.md"
    if builder.is_file():
        text = builder.read_text(encoding="utf-8")
        if "scryfall" not in text or "edhrec" not in text:
            fail(errors, "builder SKILL.md must name both scryfall and edhrec")
        if "stop" not in text.lower():
            fail(errors, "builder SKILL.md must stop when helpers are missing")
        if "Archidekt import" not in text:
            fail(errors, "builder SKILL.md must require an Archidekt import block")
        if "canonical" not in text.lower():
            fail(errors, "builder SKILL.md must document the canonical deck file")

    playbook = SKILLS / "commander-deck-playbook" / "SKILL.md"
    if playbook.is_file():
        text = playbook.read_text(encoding="utf-8")
        if "scryfall" not in text:
            fail(errors, "playbook SKILL.md must name scryfall")
        if "stop" not in text.lower():
            fail(errors, "playbook SKILL.md must stop when scryfall is missing")
        if "never write" not in text.lower() and "must never" not in text.lower() and "Never write" not in text:
            fail(errors, "playbook SKILL.md must refuse to rewrite the deck file")

    for path in BUILDER_DOCS:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        for name in BANNED_CARD_NAMES:
            if name in text:
                fail(errors, f"{rel} names a card example: {name}")
        for pattern in TARGET_PATTERNS:
            if pattern.search(text):
                fail(errors, f"{rel} has a prescribed target or sample story: {pattern.pattern}")

    if errors:
        print("validate failed:")
        for item in errors:
            print(f"  - {item}")
        return 1

    print("validate ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
