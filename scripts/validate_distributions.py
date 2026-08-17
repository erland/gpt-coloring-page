#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json, zipfile

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
KNOWLEDGE = [
    "age-complexity-guide.md",
    "layout-and-print-guide.md",
    "fallback-prompt-guide.md",
]


def read(z, name):
    try:
        return z.read(name)
    except KeyError:
        raise SystemExit(f"Saknad fil i ZIP: {name}")


def hash_bytes(b):
    return hashlib.sha256(b).hexdigest()


def main(version):
    custom = DIST / f"coloring-page-custom-gpt-v{version}.zip"
    chat = DIST / f"coloring-page-chat-v{version}.zip"
    for p in (custom, chat):
        if not p.is_file():
            raise SystemExit(f"Saknad distribution: {p.name}")
        with zipfile.ZipFile(p) as z:
            bad = z.testzip()
            if bad:
                raise SystemExit(f"Korrupt ZIP {p.name}: {bad}")

    with zipfile.ZipFile(custom) as z:
        if read(z, "gpt-instructions.md") != (ROOT / "gpt-instructions.md").read_bytes():
            raise SystemExit("Custom GPT-instruktionen avviker")
        if read(z, "conversation-starters.md") != (ROOT / "conversation-starters.md").read_bytes():
            raise SystemExit("Custom GPT starters avviker")
        for f in KNOWLEDGE:
            if read(z, f"knowledge/{f}") != (ROOT / "knowledge" / f).read_bytes():
                raise SystemExit(f"Custom Knowledge avviker: {f}")
        if read(z, "VERSION").decode().strip() != version:
            raise SystemExit("Fel VERSION i Custom GPT-paket")

    with zipfile.ZipFile(chat) as z:
        if read(z, "assistant/instructions.md") != (ROOT / "gpt-instructions.md").read_bytes():
            raise SystemExit("Portable instruktion avviker")
        if read(z, "assistant/conversation-starters.md") != (ROOT / "conversation-starters.md").read_bytes():
            raise SystemExit("Portable starters avviker")
        for f in KNOWLEDGE:
            if read(z, f"knowledge/{f}") != (ROOT / "knowledge" / f).read_bytes():
                raise SystemExit(f"Portable Knowledge avviker: {f}")
        manifest = json.loads(read(z, "MANIFEST.json"))
        if manifest["version"] != version or manifest["knowledge_count"] != len(KNOWLEDGE):
            raise SystemExit("Fel version/knowledge_count i portable manifest")
        for name, expected in manifest["files"].items():
            if hash_bytes(read(z, name)) != expected:
                raise SystemExit(f"Hashfel i MANIFEST.json: {name}")
    print(f"OK: båda distributionerna för v{version} är validerade.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--version")
    args = ap.parse_args()
    version = args.version or (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    main(version)
