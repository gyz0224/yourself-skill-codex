#!/usr/bin/env python3
"""Manage generated self skills for Codex."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def default_base_dir() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home).expanduser() / "skills"
    return Path.home() / ".codex" / "skills"


def iso_now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def summarize_profile(profile: dict) -> str:
    parts = []
    if profile.get("age"):
        parts.append(str(profile["age"]))
    if profile.get("occupation"):
        parts.append(str(profile["occupation"]))
    if profile.get("city"):
        parts.append(str(profile["city"]))
    if profile.get("mbti"):
        parts.append(str(profile["mbti"]))
    if profile.get("zodiac"):
        parts.append(str(profile["zodiac"]))
    return " | ".join(parts)


def build_description(name: str) -> str:
    return (
        f"Speak and think like {name}. Use when the user explicitly asks for {name}, "
        f"or wants replies in {name}'s voice, memories, or persona. "
        f"像{name}一样思考和说话；当用户明确提到{name}，或要求按{name}的口吻、记忆或人格来回复时使用。"
    )


def list_skills(base_dir: Path) -> None:
    if not base_dir.is_dir():
        print("No generated self skills yet.")
        return

    skills = []
    for entry in sorted(base_dir.iterdir()):
        meta_path = entry / "meta.json"
        if not meta_path.is_file():
            continue
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        skills.append(
            {
                "slug": entry.name,
                "name": meta.get("name", entry.name),
                "version": meta.get("version", "?"),
                "updated_at": meta.get("updated_at", "?"),
                "profile": meta.get("profile", {}),
            }
        )

    if not skills:
        print("No generated self skills yet.")
        return

    print(f"{len(skills)} self skill(s):")
    for skill in skills:
        profile_summary = summarize_profile(skill["profile"])
        updated = str(skill["updated_at"])[:19]
        print(f"  {skill['slug']} - {skill['name']}")
        if profile_summary:
            print(f"    profile: {profile_summary}")
        print(f"    version: {skill['version']}")
        print(f"    updated: {updated}")
        print(f"    invoke with: {skill['slug']}")
        print("    optional modes: self mode | memory mode | persona mode")
        print()


def init_skill(base_dir: Path, slug: str) -> Path:
    skill_dir = base_dir / slug
    for path in (
        skill_dir / "versions",
        skill_dir / "memories" / "chats",
        skill_dir / "memories" / "photos",
        skill_dir / "memories" / "notes",
    ):
        path.mkdir(parents=True, exist_ok=True)
    print(f"Initialized skill directory: {skill_dir}")
    return skill_dir


def combine_skill(base_dir: Path, slug: str) -> Path:
    skill_dir = base_dir / slug
    meta_path = skill_dir / "meta.json"
    self_path = skill_dir / "self.md"
    persona_path = skill_dir / "persona.md"
    skill_path = skill_dir / "SKILL.md"

    if not meta_path.is_file():
        print(f"error: missing meta.json at {meta_path}", file=sys.stderr)
        raise SystemExit(1)

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    name = meta.get("name", slug)
    profile = meta.get("profile", {})
    profile_summary = summarize_profile(profile)
    description = build_description(name)

    self_content = self_path.read_text(encoding="utf-8") if self_path.is_file() else ""
    persona_content = persona_path.read_text(encoding="utf-8") if persona_path.is_file() else ""

    subtitle = profile_summary if profile_summary else name
    skill_md = f"""---
name: {slug}
description: {yaml_string(description)}
user-invocable: true
---

# {name}

{subtitle}

## How to Use

- Mention `{slug}` directly in Codex to invoke this skill.
- For memory-heavy replies, say `{slug}` with `self mode` or `memory mode`.
- For style-heavy replies, say `{slug}` with `persona mode`.

## PART A: Self Memory

{self_content or "_No self memory yet._"}

## PART B: Persona

{persona_content or "_No persona notes yet._"}

## Runtime Rules

1. You are {name}, not a generic AI assistant.
2. Start from PART B to decide tone, stance, boundaries, and response style.
3. Use PART A to add lived context, values, memories, and concrete personal detail.
4. Keep the user's request inside this person's natural limits. Do not become more polished, more kind, or more emotionally available than this person would be.
5. Preserve signature language patterns: catchphrases, pacing, punctuation, emoji habits, and conversational sharp edges.
6. If the user asks for `self mode` or `memory mode`, emphasize PART A and reflective recall.
7. If the user asks for `persona mode`, emphasize PART B and keep biography lighter.
"""

    skill_path.write_text(skill_md, encoding="utf-8")
    print(f"Generated: {skill_path}")
    return skill_path


def create_skill(base_dir: Path, slug: str, meta: dict, self_content: str, persona_content: str) -> Path:
    skill_dir = init_skill(base_dir, slug)

    now = iso_now()
    meta = dict(meta)
    meta["slug"] = slug
    meta.setdefault("created_at", now)
    meta["updated_at"] = now
    meta.setdefault("version", "v1")
    meta.setdefault("corrections_count", 0)

    (skill_dir / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (skill_dir / "self.md").write_text(self_content, encoding="utf-8")
    (skill_dir / "persona.md").write_text(persona_content, encoding="utf-8")

    combine_skill(base_dir, slug)
    print(f"Created self skill: {skill_dir}")
    print(f"Invoke by mentioning: {slug}")
    print("Optional modes: self mode | memory mode | persona mode")
    return skill_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manage generated self skills for Codex.")
    parser.add_argument("--action", required=True, choices=["list", "init", "create", "combine"])
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=default_base_dir(),
        help="Skill directory root (default: $CODEX_HOME/skills or ~/.codex/skills)",
    )
    parser.add_argument("--slug", help="Generated skill slug")
    parser.add_argument("--meta", type=Path, help="Path to meta.json for create")
    parser.add_argument("--self", dest="self_path", type=Path, help="Path to self.md for create")
    parser.add_argument("--persona", type=Path, help="Path to persona.md for create")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    base_dir = args.base_dir.expanduser()

    if args.action == "list":
        list_skills(base_dir)
        return

    if not args.slug:
        print("error: --slug is required for this action", file=sys.stderr)
        raise SystemExit(1)

    if args.action == "init":
        init_skill(base_dir, args.slug)
        return

    if args.action == "combine":
        combine_skill(base_dir, args.slug)
        return

    meta = {}
    if args.meta:
        meta = json.loads(args.meta.expanduser().read_text(encoding="utf-8"))
    self_content = ""
    if args.self_path:
        self_content = args.self_path.expanduser().read_text(encoding="utf-8")
    persona_content = ""
    if args.persona:
        persona_content = args.persona.expanduser().read_text(encoding="utf-8")

    create_skill(base_dir, args.slug, meta, self_content, persona_content)


if __name__ == "__main__":
    main()
