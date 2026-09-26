#!/usr/bin/env python3
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]

def main() -> int:
    errors=[]
    contract=yaml.safe_load((ROOT/"gpt-builder-1.5-contract.yaml").read_text(encoding="utf-8"))
    project=yaml.safe_load((ROOT/"gpt-project.yaml").read_text(encoding="utf-8"))
    canonical=(ROOT/project["instructions"]["canonical"]).read_bytes()
    legacy=(ROOT/project["instructions"]["legacy_source"]).read_bytes()
    text=canonical.decode("utf-8")
    version=(ROOT/"VERSION").read_text(encoding="utf-8").strip()

    if contract["builder"]["target_version"]!="1.5.0":
        errors.append("target builder version must be 1.5.0")
    if contract["builder"]["behavior_preserving"] is not True:
        errors.append("migration must remain behavior-preserving")
    if canonical!=legacy:
        errors.append("canonical and legacy instruction must remain byte-identical")
    if version!="1.0.0":
        errors.append(f"VERSION changed during migration: {version!r}")

    expected=[
        "age-complexity-guide.md",
        "layout-and-print-guide.md",
        "fallback-prompt-guide.md",
    ]
    for name in expected:
        if not (ROOT/"knowledge"/name).is_file():
            errors.append(f"missing Knowledge file: {name}")

    markers=[
        "Skapa i första hand en A4-stående bild, lämplig för utskrift.",
        "Small fully colored reference illustration at the top.",
        "The colored reference must fill maximum 25% of the page height.",
        "No shading.",
        "No gray tones.",
        "Anpassa alltid detaljnivån:",
        "Om användaren ger ett komplett önskemål, skapa bilden direkt utan att ställa onödiga frågor.",
        "Föreslå en alternativ prompt som behåller känslan, temat, färgerna, åldersnivån och layouten",
    ]
    for marker in markers:
        if marker not in text:
            errors.append(f"canonical instruction missing behavior marker: {marker}")

    b=contract["behavior"]
    if b["default_page_format"]!="A4_portrait":
        errors.append("default page format must remain A4_portrait")
    if b["default_mode_when_subject_and_age_only"]!="colored_reference_plus_coloring":
        errors.append("default mode changed")
    if b["max_reference_height_percent"]!=25:
        errors.append("reference image max height must remain 25%")
    if b["coloring_section_may_use_grayscale"] is not False:
        errors.append("grayscale must remain forbidden in coloring section")
    if b["coloring_section_may_use_shading"] is not False:
        errors.append("shading must remain forbidden in coloring section")
    if b["age_complexity_adaptation_required"] is not True:
        errors.append("age complexity adaptation must remain required")

    if errors:
        print("GPT BUILDER 1.5 CONTRACT: FAIL")
        for e in errors: print("-",e)
        return 1

    print("GPT BUILDER 1.5 CONTRACT: PASS")
    print("VERSION 1.0.0; 3/3 Knowledge; A4/coloring behavior preserved")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
