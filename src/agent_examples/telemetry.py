from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .model_registry import get_chat_model_spec
from .settings import Settings


def log_event(event_type: str, payload: dict[str, Any]) -> None:
    settings = Settings()
    path = Path(settings.telemetry_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    model_spec = get_chat_model_spec(settings)
    record = {
        "ts_utc": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "payload": payload,
        "model": model_spec.model,
        "provider": model_spec.provider,
        "energy_wh": payload.get("energy_wh"),
    }
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=True) + "\n")
