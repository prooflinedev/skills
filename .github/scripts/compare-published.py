#!/usr/bin/env python3
"""Check the deployed snapshot without writing or executing its contents."""
import base64
import json
import sys
from pathlib import Path, PurePosixPath

root = Path(__file__).resolve().parents[2]
published = json.loads(Path(sys.argv[1]).read_text())
files = published["files"]
binary = published.get("binary", {})
required = {".claude-plugin/marketplace.json", "plugins/proofline/.claude-plugin/plugin.json"}
if not required <= files.keys():
    raise SystemExit("Published tree has no required manifests")
if files.keys() & binary.keys():
    raise SystemExit("Published tree lists a file both as text and as bytes")
for name, text in {**files, **binary}.items():
    parts = PurePosixPath(name).parts
    if str(PurePosixPath(name)) != name or not parts or PurePosixPath(name).is_absolute() or ".." in parts or parts[0] in (".git", ".github"):
        raise SystemExit("Published tree contains an invalid path")
    if not isinstance(text, str):
        raise SystemExit("Published tree contains a malformed file")
# Images are published in base64; every other file is UTF-8 text.
files = {name: text.encode() for name, text in files.items()}
files.update((name, base64.b64decode(text, validate=True)) for name, text in binary.items())
actual = {
    p.relative_to(root).as_posix(): p.read_bytes()
    for p in root.rglob("*")
    if p.is_file() and p.relative_to(root).parts[0] not in (".git", ".github")
}
missing = sorted(files.keys() - actual.keys())
extra = sorted(actual.keys() - files.keys())
changed = sorted(name for name in files.keys() & actual.keys() if files[name] != actual[name])
if missing or extra or changed:
    print(json.dumps({"missing": missing, "extra": extra, "changed": changed}, indent=2))
    raise SystemExit("Published skill tree differs; reconcile through the private publisher or a checked PR")
print(f"Repository matches all {len(files)} published files")
