from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


ALLOWED_TOOLS = {
    "request_resource_allocation",
    "create_mission_note",
}


def execute_tool(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if tool_name not in ALLOWED_TOOLS:
        raise ValueError(f"Tool is not allow-listed: {tool_name}")

    if tool_name == "request_resource_allocation":
        return {
            "status": "submitted_simulation_only",
            "request_id": f"SIM-{int(datetime.now(timezone.utc).timestamp())}",
            "resource": arguments.get("resource"),
            "quantity": arguments.get("quantity", 1),
            "notice": "No real operational system was changed.",
        }

    return {
        "status": "saved_simulation_only",
        "note": arguments.get("note", ""),
    }
