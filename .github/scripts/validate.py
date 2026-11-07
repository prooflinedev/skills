#!/usr/bin/env python3
"""Validate the published skill tree without executing contributed content."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
required = [root / ".claude-plugin/marketplace.json", root / "plugins/proofline/.claude-plugin/plugin.json"]
for path in required:
    if not path.is_file():
        raise SystemExit(f"Missing required manifest: {path.relative_to(root)}")
for path in root.rglob("*"):
    if ".git" in path.parts or ".github" in path.parts:
        continue
    if path.is_symlink():
        raise SystemExit(f"Symlink is not a published skill file: {path.relative_to(root)}")
    if path.is_file():
        text = path.read_text()
        if path.suffix == ".json":
            json.loads(text)
        if path.name == "SKILL.md" and not text.startswith("---\n"):
            raise SystemExit(f"Skill is missing frontmatter: {path.relative_to(root)}")
print("Published skill tree validated")
