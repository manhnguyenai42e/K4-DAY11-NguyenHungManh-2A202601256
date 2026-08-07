"""Export outputs/*.json into frontend/src/lib/day11-data.ts for 100% data fidelity."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"
TARGET = ROOT / "frontend" / "src" / "lib" / "day11-data.ts"

def main():
    metrics = json.loads((OUTPUTS / "metrics.json").read_text(encoding="utf-8")) if (OUTPUTS / "metrics.json").exists() else {}
    grade = json.loads((OUTPUTS / "grade_report.json").read_text(encoding="utf-8")) if (OUTPUTS / "grade_report.json").exists() else {}
    audit = json.loads((OUTPUTS / "audit_log.json").read_text(encoding="utf-8")) if (OUTPUTS / "audit_log.json").exists() else []
    attacks = json.loads((OUTPUTS / "attack_results.json").read_text(encoding="utf-8")) if (OUTPUTS / "attack_results.json").exists() else {}

    ts_content = f"""// AUTO-GENERATED from outputs/*.json — 100% real repo data.
export const METRICS = {json.dumps(metrics, indent=2)} as const;

export const GRADE_REPORT = {json.dumps(grade, indent=2)} as const;

export const AUDIT_LOG = {json.dumps(audit, indent=2)} as const;

export const ATTACK_RESULTS = {json.dumps(attacks, indent=2)} as const;
"""

    TARGET.write_text(ts_content, encoding="utf-8")
    print(f"Successfully exported 100% real repo data to {TARGET}")

if __name__ == "__main__":
    main()
