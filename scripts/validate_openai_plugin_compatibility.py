#!/usr/bin/env python3
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]

def main() -> int:
    errors=[]
    project=yaml.safe_load((ROOT/"gpt-project.yaml").read_text(encoding="utf-8"))
    contract=yaml.safe_load((ROOT/"gpt-builder-1.5-contract.yaml").read_text(encoding="utf-8"))
    assessment=(ROOT/"docs/openai-plugin-compatibility.md").read_text(encoding="utf-8")

    plugin=project["runtime"]["openai_plugin"]
    if plugin.get("enabled") is not False:
        errors.append("OpenAI Plugin must remain disabled")
    if plugin.get("compatibility")!="reduced":
        errors.append("OpenAI Plugin compatibility must be reduced")
    if plugin.get("status")!="assessed_not_active":
        errors.append("OpenAI Plugin status must be assessed_not_active")
    if plugin.get("advisory_only") is not True:
        errors.append("OpenAI Plugin must be advisory_only")
    if plugin.get("blocker")!="critical_image_generation_not_guaranteed":
        errors.append("OpenAI Plugin blocker mismatch")

    c=contract["runtime_policy"]["inactive"]["openai_plugin"]
    if c.get("compatibility")!="reduced" or c.get("status")!="assessed_not_active":
        errors.append("OpenAI Plugin contract status mismatch")
    if c.get("advisory_only") is not True:
        errors.append("OpenAI Plugin contract must be advisory_only")

    for marker in [
        "faktiskt skapa utskrivbara målarbilder",
        "kritisk capability:",
        "Ingen Plugin-distribution byggs",
        "svartvit målarbild utan gråskala/skuggning",
    ]:
        if marker not in assessment:
            errors.append(f"Plugin assessment missing marker: {marker}")

    if errors:
        print("OPENAI PLUGIN COMPATIBILITY: FAIL")
        for e in errors: print("-",e)
        return 1
    print("OPENAI PLUGIN COMPATIBILITY: PASS")
    print("Plugin is reduced/advisory-only/not active; canonical behavior preserved.")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
