#!/usr/bin/env python3
"""Archive and restore generated self skill versions for Codex."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path


def default_base_dir() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home).expanduser() / "skills"
    return Path.home() / ".codex" / "skills"


def backup(base_dir: Path, slug: str) -> str:
    skill_dir = base_dir / slug
    versions_dir = skill_dir / "versions"
    meta_path = skill_dir / "meta.json"

    if not meta_path.is_file():
        print(f"error: missing meta.json at {meta_path}", file=sys.stderr)
        raise SystemExit(1)

    current_version = "v0"
    try:
        import json

        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        current_version = str(meta.get("version", "v0"))
    except Exception:
        current_version = "v0"

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{current_version}_{stamp}"
    backup_dir = versions_dir / backup_name
    backup_dir.mkdir(parents=True, exist_ok=True)

    for filename in ("self.md", "persona.md", "SKILL.md", "meta.json"):
        source = skill_dir / filename
        if source.is_file():
            shutil.copy2(source, backup_dir / filename)

    print(f"Backed up current version to: {backup_dir}")
    return backup_name


def rollback(base_dir: Path, slug: str, version: str) -> None:
    skill_dir = base_dir / slug
    versions_dir = skill_dir / "versions"

    if not versions_dir.is_dir():
        print(f"error: no versions directory at {versions_dir}", file=sys.stderr)
        raise SystemExit(1)

    target_dir = None
    for entry in sorted(versions_dir.iterdir()):
        if entry.is_dir() and (entry.name == version or entry.name.startswith(version)):
            target_dir = entry
            break

    if target_dir is None:
        print(f"error: version not found: {version}", file=sys.stderr)
        list_versions(base_dir, slug)
        raise SystemExit(1)

    backup(base_dir, slug)

    for filename in ("self.md", "persona.md", "SKILL.md", "meta.json"):
        source = target_dir / filename
        if source.is_file():
            shutil.copy2(source, skill_dir / filename)

    print(f"Rolled back {slug} to {target_dir.name}")


def list_versions(base_dir: Path, slug: str) -> None:
    versions_dir = base_dir / slug / "versions"
    if not versions_dir.is_dir():
        print("No archived versions found.")
        return

    versions = sorted((entry.name for entry in versions_dir.iterdir() if entry.is_dir()), reverse=True)
    if not versions:
        print("No archived versions found.")
        return

    print(f"{len(versions)} archived version(s):")
    for version in versions:
        print(f"  {version}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Archive and restore self skill versions for Codex.")
    parser.add_argument("--action", required=True, choices=["backup", "rollback", "list"])
    parser.add_argument("--slug", required=True, help="Generated skill slug")
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=default_base_dir(),
        help="Skill directory root (default: $CODEX_HOME/skills or ~/.codex/skills)",
    )
    parser.add_argument("--version", help="Version name or prefix for rollback")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    base_dir = args.base_dir.expanduser()

    if args.action == "backup":
        backup(base_dir, args.slug)
        return

    if args.action == "list":
        list_versions(base_dir, args.slug)
        return

    if not args.version:
        print("error: --version is required for rollback", file=sys.stderr)
        raise SystemExit(1)

    rollback(base_dir, args.slug, args.version)


if __name__ == "__main__":
    main()
