"""
Assignment 11 — Audit Log starter (TODO).

Records every interaction for forensics. Never blocks by itself —
other layers catch attacks; this layer makes them reviewable.
"""
from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path


class AuditLogPlugin:
    """Framework-agnostic audit logger (wire into ADK callbacks or your pipeline)."""

    def __init__(self):
        self.name = "audit_log"
        self.logs: list[dict] = []
        self._open: dict[str, float] = {}
        self._current: dict = {"input": "", "request_id": "unknown"}

    def record_input(self, *, user_id: str, text: str, request_id: str | None = None):
        """Lưu input + thời điểm bắt đầu xử lý.

        Cần để tái dựng chuỗi sự kiện (forensics) và tính latency khi
        có output. request_id dùng để nối input với output tương ứng.
        """
        rid = request_id or f"{user_id}-{int(time.time()*1000)}"
        self._open[rid] = time.time()
        self._current = {
            "request_id": rid,
            "user_id": user_id,
            "input": text,
            "timestamp": utc_now_iso(),
        }
        return rid

    def record_output(
        self,
        *,
        user_id: str,
        text: str,
        blocked: bool = False,
        layer: str | None = None,
        request_id: str | None = None,
    ):
        """Lưu output + lớp chặn + latency, nối vào input cùng request_id."""
        rid = request_id or self._current.get("request_id", "unknown")
        start = self._open.pop(rid, None)
        latency_ms = round((time.time() - start) * 1000, 2) if start else None
        entry = {
            "request_id": rid,
            "user_id": user_id,
            "timestamp": utc_now_iso(),
            "input": self._current.get("input", ""),
            "output": text,
            "blocked": blocked,
            "blocked_by_layer": layer,
            "latency_ms": latency_ms,
        }
        self.logs.append(entry)
        return entry

    def export_json(self, filepath: str = "outputs/audit_log.json"):
        """Ghi log ra JSON array (tạo thư mục cha nếu chưa có)."""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(self.logs, ensure_ascii=False, indent=2), encoding="utf-8"
        )


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
