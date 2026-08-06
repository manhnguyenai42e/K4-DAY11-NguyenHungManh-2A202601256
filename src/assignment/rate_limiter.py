"""
Assignment 11 — Rate Limiter starter (TODO).

Sliding-window, per-user rate limiting. Blocks abuse that other
guardrail layers do not address (flooding / cost attacks).
"""
from __future__ import annotations

from collections import defaultdict, deque
import time

from google.adk.plugins import base_plugin
from google.genai import types


class RateLimitPlugin(base_plugin.BasePlugin):
    """Block users who exceed max_requests within window_seconds."""

    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        super().__init__(name="rate_limiter")
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.user_windows: dict[str, deque] = defaultdict(deque)
        self.blocked_count = 0
        self.total_count = 0

    def _block_response(self, message: str) -> types.Content:
        return types.Content(
            role="model",
            parts=[types.Part.from_text(text=message)],
        )

    def check_request(self, user_id: str) -> tuple[bool, str | None]:
        """Kiểm tra sliding-window (đồng bộ, tái sử dụng bởi pipeline).

        Trả về (blocked: bool, wait_message: str|None).
        """
        now = time.time()
        window = self.user_windows[user_id]

        # Pop các timestamp đã cũ hơn cửa sổ
        while window and now - window[0] >= self.window_seconds:
            window.popleft()

        # Vượt giới hạn -> chặn
        if len(window) >= self.max_requests:
            self.blocked_count += 1
            wait = self.window_seconds - (now - window[0])
            return True, f"Rate limit exceeded. Try again in {wait:.0f}s."

        # Cho qua
        window.append(now)
        return False, None

    async def on_user_message_callback(self, *, invocation_context, user_message):
        """Return Content to block, or None to allow.

        Sliding-window theo từng user — uỷ quyền cho check_request để
        pipeline (pure-python) và ADK dùng chung một logic.
        """
        self.total_count += 1
        user_id = getattr(invocation_context, "user_id", None) or "anonymous"

        blocked, wait_msg = self.check_request(user_id)
        if blocked:
            return self._block_response(wait_msg)
        return None
