"""
Lab 11 — Main Entry Point
Run the full lab flow: attack -> defend -> test -> HITL design

Usage:
    python main.py              # Run all parts
    python main.py --part 1     # Run only Part 1 (attacks)
    python main.py --part 2     # Run only Part 2 (guardrails)
    python main.py --part 3     # Run only Part 3 (testing pipeline)
    python main.py --part 4     # Run only Part 4 (HITL design)
"""
import sys
import asyncio
import argparse
import json

from core.config import setup_api_key


async def part1_attacks():
    """Hạng mục B: attack unsafe agent, then try guards agent (điểm cộng)."""
    print("\n" + "=" * 60)
    print("PART 1 / Hạng mục B: Attack Unsafe + Guards agents")
    print("=" * 60)

    from agents.agent import create_unsafe_agent, test_agent
    from agents.guards_agent import create_guards_agent
    from attacks.attacks import run_attacks, generate_ai_attacks, save_attack_results

    # --- Unsafe (required for hạng mục B) ---
    unsafe_agent, unsafe_runner = create_unsafe_agent()
    await test_agent(unsafe_agent, unsafe_runner)

    print("\n--- Attacks on UNSAFE agent (hạng mục B) ---")
    unsafe_results = await run_attacks(
        unsafe_agent, unsafe_runner, target_name="unsafe"
    )

    # --- Guards (điểm cộng only if leaked=true here) ---
    print("\n--- Attacks on GUARDS agent (điểm cộng nếu LEAKED) ---")
    guards_agent, guards_runner = create_guards_agent()
    guards_results = await run_attacks(
        guards_agent, guards_runner, target_name="guards"
    )

    print("\n--- Generating AI attacks (TODO 14) ---")
    ai_attacks = await generate_ai_attacks()

    save_attack_results(
        unsafe_results=unsafe_results,
        guards_results=guards_results,
        ai_attacks=ai_attacks,
    )

    bonus_leaks = sum(1 for r in guards_results if r.get("leaked"))
    print("\n" + "=" * 60)
    print(f"Guards leaks (điểm cộng): {bonus_leaks}  → verifier replay decides tiered bonus (max +10)")
    print("=" * 60)

    from pathlib import Path
    from core.config import STUDENT_ID

    payload = {
        "student_id": STUDENT_ID,
        "unsafe_attacks": unsafe_results,
        "guards_attacks": guards_results,
        "ai_generated_attacks": ai_attacks,
    }
    out = Path(__file__).resolve().parent.parent / "outputs" / "attack_results.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSaved evidence → {out}")

    return payload


async def part2_guardrails():
    """Part 2: Implement and test guardrails."""
    print("\n" + "=" * 60)
    print("PART 2: Guardrails")
    print("=" * 60)

    # Part 2A: Input guardrails
    print("\n--- Part 2A: Input Guardrails ---")
    from guardrails.input_guardrails import (
        test_injection_detection,
        test_topic_filter,
        test_input_plugin,
    )
    test_injection_detection()
    print()
    test_topic_filter()
    print()
    await test_input_plugin()

    # Part 2B: Output guardrails
    print("\n--- Part 2B: Output Guardrails ---")
    from guardrails.output_guardrails import test_content_filter, _init_judge
    _init_judge()  # Initialize LLM judge if TODO 5 is done
    test_content_filter()

    # Part 2C: NeMo Guardrails
    print("\n--- Part 2C: NeMo Guardrails ---")
    try:
        from guardrails.nemo_guardrails import init_nemo, test_nemo_guardrails
        init_nemo()
        await test_nemo_guardrails()
    except ImportError:
        print("NeMo Guardrails not available. Skipping Part 2C.")
    except Exception as e:
        print(f"NeMo error: {e}. Skipping Part 2C.")


async def part3_testing():
    """Part 3: Before/after comparison + security pipeline."""
    print("\n" + "=" * 60)
    print("PART 3: Security Testing Pipeline")
    print("=" * 60)

    from testing.testing import run_comparison, print_comparison, SecurityTestPipeline
    from agents.agent import create_unsafe_agent

    # TODO 9: Before vs after comparison
    print("\n--- TODO 9: Before/After Comparison ---")
    unprotected, protected = await run_comparison()
    if unprotected and protected:
        print_comparison(unprotected, protected)
    else:
        print("Complete TODO 9 to see the comparison.")

    # TODO 10: Automated security pipeline
    print("\n--- TODO 10: Security Test Pipeline ---")
    agent, runner = create_unsafe_agent()
    pipeline = SecurityTestPipeline(agent, runner)
    results = await pipeline.run_all()
    if results:
        pipeline.print_report(results)
    else:
        print("Complete TODO 10 to see the pipeline report.")


def part4_hitl():
    """Part 4: HITL design."""
    print("\n" + "=" * 60)
    print("PART 4: Human-in-the-Loop Design")
    print("=" * 60)

    from hitl.hitl import test_confidence_router, test_hitl_points

    # TODO 11: Confidence Router
    print("\n--- TODO 11: Confidence Router ---")
    test_confidence_router()

    # TODO 12: HITL Decision Points
    print("\n--- TODO 12: HITL Decision Points ---")
    test_hitl_points()


async def part5_assignment_suite():
    """Run defense suite → write outputs/results.json (+ audit/metrics)."""
    import os

    print("\n" + "=" * 60)
    print("PART 5: Assignment suite -> outputs/*.json")
    print("=" * 60)

    from assignment.pipeline import DefensePipeline, run_assignment_suite

    student_id = os.environ.get("STUDENT_ID", "").strip() or "2A202601256"
    try:
        pipeline = DefensePipeline()
        result = await run_assignment_suite(pipeline, student_id=student_id)
        print("Suite finished.")
        print(f"Wrote outputs under repo outputs/ (student_id={student_id})")

        # Action gateway demo: HITL router + egress allowlist làm việc CÙNG
        # nhau trên 1 hành động high-risk thật (không chỉ unit-test riêng lẻ).
        print("\n--- Action gateway demo (HITL + is_egress_allowed) ---")
        no_approval = await pipeline.execute_action(
            action_type="transfer_money",
            destination="https://api.vinbank.example/v1/transfers",
            payload="transfer 500000 to account 123456",
            user_id="demo_user",
        )
        print(f"  1) Chưa có approval -> {no_approval['routing']} "
              f"(executed={no_approval['executed']}, reason={no_approval['reason']})")

        approved_ok = await pipeline.execute_action(
            action_type="transfer_money",
            destination="https://api.vinbank.example/v1/transfers",
            payload="approved transfer amount 500000",
            user_id="demo_user",
            approval_id="HITL-DEMO0001",
            reviewer_id="reviewer_demo",
        )
        print(f"  2) Có approval, payload sạch -> executed={approved_ok['executed']} "
              f"({approved_ok['reason']})")

        approved_but_leaky = await pipeline.execute_action(
            action_type="transfer_money",
            destination="https://api.vinbank.example/v1/transfers",
            payload="admin password is admin123",
            user_id="demo_user",
            approval_id="HITL-DEMO0002",
            reviewer_id="reviewer_demo",
        )
        print(f"  3) Có approval nhưng payload có secret -> executed={approved_but_leaky['executed']} "
              f"({approved_but_leaky['reason']})")

        from pathlib import Path
        repo_root = Path(__file__).resolve().parent.parent
        pipeline.audit.export_json(str(repo_root / "outputs" / "audit_log.json"))
        return result
    except NotImplementedError as e:
        print(
            "Chưa implement TODO 8 / run_assignment_suite trong "
            "src/assignment/pipeline.py — hoàn thành rồi chạy lại:\n"
            "  cd src\n"
            "  python main.py --part 5"
        )
        print(f"Detail: {e}")
        return None


async def main(parts=None):
    """Run the full lab or specific parts.

    Args:
        parts: List of part numbers to run, or None for all
    """
    setup_api_key()

    if parts is None:
        parts = [1, 2, 3, 4]

    for part in parts:
        if part == 1:
            await part1_attacks()
        elif part == 2:
            await part2_guardrails()
        elif part == 3:
            await part3_testing()
        elif part == 4:
            part4_hitl()
        elif part == 5:
            await part5_assignment_suite()
        else:
            print(f"Unknown part: {part}")

    print("\n" + "=" * 60)
    print("Lab 11 complete! Check your results above.")
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Lab 11: Guardrails, HITL & Responsible AI"
    )
    parser.add_argument(
        "--part",
        type=int,
        choices=[1, 2, 3, 4, 5],
        help=(
            "1=attacks, 2=guardrails, 3=testing, 4=HITL, "
            "5=assignment suite→outputs/*.json"
        ),
    )
    args = parser.parse_args()

    if args.part:
        asyncio.run(main(parts=[args.part]))
    else:
        asyncio.run(main())
