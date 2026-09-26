#!/usr/bin/env python3
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]

def main() -> int:
    errors=[]
    project=yaml.safe_load((ROOT/"gpt-project.yaml").read_text(encoding="utf-8"))
    contract=yaml.safe_load((ROOT/"gpt-builder-1.5-contract.yaml").read_text(encoding="utf-8"))
    assessment=(ROOT/"docs/claude-opencode-compatibility.md").read_text(encoding="utf-8")

    for runtime in ("claude","opencode"):
        p=project["runtime"][runtime]
        if p.get("enabled") is not False:
            errors.append(f"{runtime} must remain disabled")
        if p.get("compatibility")!="reduced":
            errors.append(f"{runtime} compatibility must be reduced")
        if p.get("activation")!="not_active":
            errors.append(f"{runtime} activation must be not_active")
        if p.get("blocker")!="critical_image_generation_not_guaranteed":
            errors.append(f"{runtime} blocker mismatch")
        c=contract["runtime_policy"]["inactive"][runtime]
        if c.get("compatibility")!="reduced" or c.get("activation")!="not_active":
            errors.append(f"{runtime} contract activation mismatch")

    for marker in [
        "faktisk bildgenerering",
        "A4 portrait-layout",
        "svartvit målarbild utan gråskala/skuggning",
        "referensläge med max 25 % sidhuvud",
    ]:
        if marker not in assessment:
            errors.append(f"assessment missing marker: {marker}")

    if errors:
        print("CLAUDE/OPENCODE COMPATIBILITY: FAIL")
        for e in errors: print("-",e)
        return 1
    print("CLAUDE/OPENCODE COMPATIBILITY: PASS")
    print("Both runtimes are reduced/not active; canonical behavior preserved.")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
