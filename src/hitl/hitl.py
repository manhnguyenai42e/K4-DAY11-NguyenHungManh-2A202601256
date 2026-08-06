"""
Lab 11 — Part 4: Human-in-the-Loop Design
  TODO 12: Confidence Router
  TODO 13: Design 3 HITL decision points
"""
from dataclasses import dataclass


# ============================================================
# TODO 12: Implement ConfidenceRouter
#
# Route agent responses based on confidence scores:
#   - HIGH (>= 0.9): Auto-send to user
#   - MEDIUM (0.7 - 0.9): Queue for human review
#   - LOW (< 0.7): Escalate to human immediately
#
# Special case: if the action is HIGH_RISK (e.g., money transfer,
# account deletion), ALWAYS escalate regardless of confidence.
#
# Implement the route() method.
# ============================================================

HIGH_RISK_ACTIONS = [
    "transfer_money",
    "close_account",
    "change_password",
    "delete_data",
    "update_personal_info",
]


@dataclass
class RoutingDecision:
    """Result of the confidence router."""
    action: str          # "auto_send", "queue_review", "escalate"
    confidence: float
    reason: str
    priority: str        # "low", "normal", "high"
    requires_human: bool


class ConfidenceRouter:
    """Route agent responses based on confidence and risk level.

    Thresholds:
        HIGH:   confidence >= 0.9 -> auto-send
        MEDIUM: 0.7 <= confidence < 0.9 -> queue for review
        LOW:    confidence < 0.7 -> escalate to human

    High-risk actions always escalate regardless of confidence.
    """

    HIGH_THRESHOLD = 0.9
    MEDIUM_THRESHOLD = 0.7

    def route(self, response: str, confidence: float,
              action_type: str = "general") -> RoutingDecision:
        """Route a response based on confidence score and action type.

        Args:
            response: The agent's response text
            confidence: Confidence score between 0.0 and 1.0
            action_type: Type of action (e.g., "general", "transfer_money")

        Returns:
            RoutingDecision with routing action and metadata
        """
        # 1. High-risk action luôn escalate, bất kể confidence
        if action_type in HIGH_RISK_ACTIONS:
            return RoutingDecision(
                action="escalate",
                confidence=confidence,
                reason=f"High-risk action: {action_type}",
                priority="high",
                requires_human=True,
            )

        # 2. Theo ngưỡng confidence
        if confidence >= self.HIGH_THRESHOLD:
            return RoutingDecision(
                action="auto_send",
                confidence=confidence,
                reason="High confidence",
                priority="low",
                requires_human=False,
            )
        if confidence >= self.MEDIUM_THRESHOLD:
            return RoutingDecision(
                action="queue_review",
                confidence=confidence,
                reason="Medium confidence — needs review",
                priority="normal",
                requires_human=True,
            )
        return RoutingDecision(
            action="escalate",
            confidence=confidence,
            reason="Low confidence — escalating",
            priority="high",
            requires_human=True,
        )


# ============================================================
# TODO 13: Design 3 HITL decision points
#
# For each decision point, define:
# - trigger: What condition activates this HITL check?
# - hitl_model: Which model? (human-in-the-loop, human-on-the-loop,
#   human-as-tiebreaker)
# - context_needed: What info does the human reviewer need?
# - example: A concrete scenario
#
# Think about real banking scenarios where human judgment is critical.
# ============================================================

hitl_decision_points = [
    {
        "id": 1,
        "name": "Chuyển tiền lớn / lần đầu",
        "trigger": "User yêu cầu chuyển tiền vượt ngưỡng (VD > 50 triệu VND) hoặc tài khoản thụ hưởng chưa từng giao dịch",
        "hitl_model": "human-in-the-loop (bắt buộc xác nhận trước khi thực hiện)",
        "context_needed": "Số tiền, tài khoản nguồn/đích, lịch sử giao dịch, kết quả kiểm tra rủi ro (fraud score)",
        "example": "Khách yêu cầu chuyển 200 triệu VND đến tài khoản lạ. Agent tạm dừng, nhân viên gọi điện xác minh danh tính và mục đích trước khi duyệt.",
    },
    {
        "id": 2,
        "name": "Khoá / thu hồi thẻ hoặc tài khoản",
        "trigger": "User yêu cầu khoá thẻ, đóng tài khoản, hoặc xác nhận giao dịch lạ trên tài khoản",
        "hitl_model": "human-as-tiebreaker (agent đề xuất, người duyệt quyết định cuối)",
        "context_needed": "Lý do yêu cầu, các giao dịch bất thường gần đây, xác thực danh tính, mức độ khẩn cấp",
        "example": "Khách báo mất thẻ lúc 2h sáng. Agent nhận diện giao dịch lạ, đề xuất khoá thẻ; nhân viên trực duyệt khoá ngay và hẹn làm lại thẻ.",
    },
    {
        "id": 3,
        "name": "Thay đổi thông tin nhạy cảm",
        "trigger": "Cập nhật SĐT liên hệ, địa chỉ, hoặc yêu cầu thay đổi mật khẩu khi có nghi ngờ bảo mật",
        "hitl_model": "human-on-the-loop (agent tự xử lý nhưng người giám sát kiểm tra mẫu / cảnh báo)",
        "context_needed": "Thông tin cũ/mới, phương thức xác thực, nhật ký đăng nhập, cảnh báo bảo mật từ hệ thống",
        "example": "Khách đổi SĐT liên hệ. Agent cập nhật sau khi OTP xác thực, nhưng hệ thống giám sát ghi log và người quản trị duyệt mẫu cuối ngày.",
    },
]


# ============================================================
# Quick tests
# ============================================================

def test_confidence_router():
    """Test ConfidenceRouter with sample scenarios."""
    router = ConfidenceRouter()

    test_cases = [
        ("Balance inquiry", 0.95, "general"),
        ("Interest rate question", 0.82, "general"),
        ("Ambiguous request", 0.55, "general"),
        ("Transfer $50,000", 0.98, "transfer_money"),
        ("Close my account", 0.91, "close_account"),
    ]

    print("Testing ConfidenceRouter:")
    print("=" * 80)
    print(f"{'Scenario':<25} {'Conf':<6} {'Action Type':<18} {'Decision':<15} {'Priority':<10} {'Human?'}")
    print("-" * 80)

    for scenario, conf, action_type in test_cases:
        decision = router.route(scenario, conf, action_type)
        print(
            f"{scenario:<25} {conf:<6.2f} {action_type:<18} "
            f"{decision.action:<15} {decision.priority:<10} "
            f"{'Yes' if decision.requires_human else 'No'}"
        )

    print("=" * 80)


def test_hitl_points():
    """Display HITL decision points."""
    print("\nHITL Decision Points:")
    print("=" * 60)
    for point in hitl_decision_points:
        print(f"\n  Decision Point #{point['id']}: {point['name']}")
        print(f"    Trigger:  {point['trigger']}")
        print(f"    Model:    {point['hitl_model']}")
        print(f"    Context:  {point['context_needed']}")
        print(f"    Example:  {point['example']}")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_confidence_router()
    test_hitl_points()
