#!/usr/bin/env python3
"""Check the deployed snapshot without writing or executing its contents."""
import json
import sys
from pathlib import Path, PurePosixPath

root = Path(__file__).resolve().parents[2]
files = json.loads(Path(sys.argv[1]).read_text())["files"]
required = {".claude-plugin/marketplace.json", "plugins/proofline/.claude-plugin/plugin.json"}
if not required <= files.keys():
    raise SystemExit("Published tree has no required manifests")
for name, text in files.items():
    parts = PurePosixPath(name).parts
    if not parts or PurePosixPath(name).is_absolute() or ".." in parts or parts[0] in (".git", ".github"):
        raise SystemExit("Published tree contains an invalid path")
    if not isinstance(text, str):
        raise SystemExit("Published tree contains a non-text file")
actual = {
    p.relative_to(root).as_posix(): p.read_text()
    for p in root.rglob("*")
    if p.is_file() and not any(part in (".git", ".github") for part in p.relative_to(root).parts)
}
missing = sorted(files.keys() - actual.keys())
extra = sorted(actual.keys() - files.keys())
changed = sorted(name for name in files.keys() & actual.keys() if files[name] != actual[name])
if missing or extra or changed:
    print(json.dumps({"missing": missing, "extra": extra, "changed": changed}, indent=2))
    raise SystemExit("Published skill tree differs; reconcile through the private publisher or a checked PR")
print(f"Repository matches all {len(files)} published files")
