#!/usr/bin/env python3
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]

def main() -> int:
    errors=[]
    r=yaml.safe_load((ROOT/"runtime-distribution-registry.yaml").read_text(encoding="utf-8"))
    if r["builder_contract"]["target_version"]!="1.5.0":
        errors.append("builder target must be 1.5.0")
    if r.get("active_targets")!=["chat","custom-gpt"]:
        errors.append(f"active targets must be exactly chat/custom-gpt, found {r.get('active_targets')}")
    for name in r["active_targets"]:
        t=r["targets"].get(name)
        if not t or t.get("status")!="active":
            errors.append(f"active target {name} missing active target definition")
    for name in ("claude","opencode","openai_plugin"):
        if name not in r.get("inactive_targets",{}):
            errors.append(f"inactive runtime missing: {name}")
    if r["release"].get("wildcard_runtime_selection") is not False:
        errors.append("wildcard runtime selection must be false")
    if r["release"].get("exact_artifact_set") is not True:
        errors.append("release must require exact artifact set")
    if errors:
        print("RUNTIME REGISTRY: FAIL")
        for e in errors: print("-",e)
        return 1
    print("RUNTIME REGISTRY: PASS")
    print("Active targets: chat, custom-gpt")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
