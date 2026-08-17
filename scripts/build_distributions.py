#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json, os, re, shutil, zipfile

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
KNOWLEDGE = [
    "age-complexity-guide.md",
    "layout-and-print-guide.md",
    "fallback-prompt-guide.md",
]


def validate_version(v: str) -> str:
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:[+-][0-9A-Za-z.-]+)?", v):
        raise SystemExit(f"Ogiltig version: {v}")
    return v


def copy_file(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def zip_dir(src: Path, out: Path):
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(src.rglob("*")):
            if p.is_file():
                info = zipfile.ZipInfo(str(p.relative_to(src)).replace(os.sep, "/"))
                info.date_time = (2020, 1, 1, 0, 0, 0)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                z.writestr(info, p.read_bytes())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build(version: str):
    version = validate_version(version)
    for f in KNOWLEDGE:
        if not (ROOT / "knowledge" / f).is_file():
            raise SystemExit(f"Saknad Knowledge-fil: {f}")

    shutil.rmtree(DIST, ignore_errors=True)
    DIST.mkdir(parents=True)
    stage = ROOT / ".build-distributions"
    shutil.rmtree(stage, ignore_errors=True)
    custom, chat = stage / "custom", stage / "chat"
    custom.mkdir(parents=True)
    chat.mkdir(parents=True)

    # Custom GPT package: preserve current behavior-bearing files byte-for-byte.
    for rel in ["README.md", "gpt-instructions.md", "conversation-starters.md"]:
        copy_file(ROOT / rel, custom / rel)
    for f in KNOWLEDGE:
        copy_file(ROOT / "knowledge" / f, custom / "knowledge" / f)
    if (ROOT / "examples/example-prompts.md").is_file():
        copy_file(ROOT / "examples/example-prompts.md", custom / "examples/example-prompts.md")
    (custom / "VERSION").write_text(version + "\n", encoding="utf-8")

    # Portable chat package.
    copy_file(ROOT / "portable/START-HERE.md", chat / "START-HERE.md")
    copy_file(ROOT / "gpt-instructions.md", chat / "assistant/instructions.md")
    copy_file(ROOT / "conversation-starters.md", chat / "assistant/conversation-starters.md")
    for f in KNOWLEDGE:
        copy_file(ROOT / "knowledge" / f, chat / "knowledge" / f)
    if (ROOT / "examples/example-prompts.md").is_file():
        copy_file(ROOT / "examples/example-prompts.md", chat / "examples/example-prompts.md")
    (chat / "VERSION").write_text(version + "\n", encoding="utf-8")

    files = {}
    for p in sorted(chat.rglob("*")):
        if p.is_file() and p.name != "MANIFEST.json":
            files[str(p.relative_to(chat)).replace(os.sep, "/")] = sha256(p)
    (chat / "MANIFEST.json").write_text(json.dumps({
        "package": "coloring-page",
        "format": "portable-chat-assistant",
        "version": version,
        "entrypoint": "START-HERE.md",
        "instructions": "assistant/instructions.md",
        "knowledge_count": len(KNOWLEDGE),
        "files": files,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    zip_dir(custom, DIST / f"coloring-page-custom-gpt-v{version}.zip")
    zip_dir(chat, DIST / f"coloring-page-chat-v{version}.zip")
    shutil.rmtree(stage, ignore_errors=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--version")
    args = ap.parse_args()
    version = args.version or (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    build(version)
