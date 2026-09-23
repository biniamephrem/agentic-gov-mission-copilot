from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def audit(event_type: str, mission_id: str, payload: dict[str, Any]) -> None:
    path = Path(os.getenv("AUDIT_LOG_PATH", "./audit.jsonl"))
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "mission_id": mission_id,
        "payload": payload,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
