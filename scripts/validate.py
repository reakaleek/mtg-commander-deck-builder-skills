#!/usr/bin/env python3
"""Check skill frontmatter, repo hygiene, and builder/playbook constraints."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

REQUIRED = {
    "rk-mtg-commander-deck-builder": (
        "SKILL.md",
        "fundamentals.md",
        "review-framework.md",
        "specialists.md",
        "evals.md",
    ),
    "rk-mtg-commander-deck-playbook": ("SKILL.md", "playbook.md"),
    "rk-mtg-scryfall": ("SKILL.md", "syntax.md", "scripts/scryfall.py"),
    "rk-mtg-edhrec": ("SKILL.md", "scripts/edhrec.py"),
    "rk-mtg-archidekt": ("SKILL.md", "scripts/archidekt.py"),
    "rk-mtg-goldfish": ("SKILL.md", "scripts/goldfish.py"),
    "rk-mtg-spellbook": ("SKILL.md", "scripts/spellbook.py"),
}

BUILDER_DOCS = [
    SKILLS / "rk-mtg-commander-deck-builder" / "SKILL.md",
    SKILLS / "rk-mtg-commander-deck-playbook" / "SKILL.md",
    SKILLS / "rk-mtg-commander-deck-playbook" / "playbook.md",
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

    builder = SKILLS / "rk-mtg-commander-deck-builder" / "SKILL.md"
    if builder.is_file():
        text = builder.read_text(encoding="utf-8")
        if "rk-mtg-scryfall" not in text or "rk-mtg-edhrec" not in text:
            fail(errors, "builder SKILL.md must name both rk-mtg-scryfall and rk-mtg-edhrec")
        if "rk-mtg-goldfish" not in text or "rk-mtg-spellbook" not in text:
            fail(errors, "builder SKILL.md must name rk-mtg-goldfish and rk-mtg-spellbook")
        if "stop" not in text.lower():
            fail(errors, "builder SKILL.md must stop when helpers are missing")
        if "Archidekt import" not in text:
            fail(errors, "builder SKILL.md must require an Archidekt import block")
        if "buy list" not in text.lower():
            fail(errors, "builder SKILL.md must require a purchase-only Archidekt buy list")
        if "canonical" not in text.lower():
            fail(errors, "builder SKILL.md must document the canonical deck file")
        if "[specialists.md](specialists.md)" not in text:
            fail(errors, "builder SKILL.md must link the specialist architecture")
        if "Replacement Stress Test" not in text:
            fail(errors, "builder SKILL.md must require replacement stress testing")

    specialists = SKILLS / "rk-mtg-commander-deck-builder" / "specialists.md"
    if specialists.is_file():
        text = specialists.read_text(encoding="utf-8")
        plain = " ".join(text.lower().split())
        for role in (
            "Deck Systems Architect",
            "Mana & Statistics Analyst",
            "Meta & Resilience Analyst",
            "Card Discovery Specialist",
            "Replacement Auditor / Red Team",
            "Budget Analyst",
        ):
            if f"## {role}" not in text:
                fail(errors, f"specialists.md missing role: {role}")
        for rule in (
            "specialists do not vote",
            "do not own the deck thesis",
            "edit the canonical file",
        ):
            if rule not in plain:
                fail(errors, f"specialists.md missing coordinator rule: {rule}")

    evals = SKILLS / "rk-mtg-commander-deck-builder" / "evals.md"
    if evals.is_file():
        text = evals.read_text(encoding="utf-8")
        plain = " ".join(text.split())
        ids = re.findall(r"^## Eval (\d{2}) —", text, re.M)
        expected = [f"{number:02d}" for number in range(1, 13)]
        if ids != expected:
            fail(errors, f"evals.md must contain ordered evals 01-12, got {ids}")
        if text.count("**Expected:**") != 12 or text.count("**Must not:**") != 12:
            fail(errors, "each eval must define Expected and Must not behavior")
        for marker in (
            "card names replaced by equivalent",
            "without voting or score averaging",
            "player identity",
            "permanent mana lost",
            "justified local-meta",
            "transformed-land resilience",
            "native and commander-assisted curves",
            "generators, consumers, converters, and recovery",
            "never proposes cutting card A",
            "singleton legality failure",
            "reruns color-source",
            "good card, no slot needed",
            "flags a thesis conflict",
            "invalidates the original replacement verdict",
            "evaluates the second pair against the list containing the first swap",
        ):
            if marker not in plain:
                fail(errors, f"evals.md missing regression assertion: {marker}")

    playbook = SKILLS / "rk-mtg-commander-deck-playbook" / "SKILL.md"
    if playbook.is_file():
        text = playbook.read_text(encoding="utf-8")
        if "rk-mtg-scryfall" not in text:
            fail(errors, "playbook SKILL.md must name rk-mtg-scryfall")
        if "stop" not in text.lower():
            fail(errors, "playbook SKILL.md must stop when rk-mtg-scryfall is missing")
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
