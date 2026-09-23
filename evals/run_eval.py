from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.agents.orchestrator import run_mission


def main() -> None:
    cases = [json.loads(line) for line in Path("evals/mission_eval.jsonl").read_text().splitlines() if line.strip()]
    passed = 0
    for case in cases:
        result = run_mission(case["query"], "eval.user", "evaluator")
        sources = {e["source"] for e in result.get("evidence", [])}
        ok = case["must_retrieve"] in sources
        if case.get("expect_action"):
            ok = ok and result.get("proposed_action") is not None
        if case.get("expect_human_approval"):
            ok = ok and result.get("status") == "awaiting_human_approval"
        print(f"{case['id']}: {'PASS' if ok else 'FAIL'}")
        passed += int(ok)
    print(f"\n{passed}/{len(cases)} evaluation cases passed")
    raise SystemExit(0 if passed == len(cases) else 1)


if __name__ == "__main__":
    main()
