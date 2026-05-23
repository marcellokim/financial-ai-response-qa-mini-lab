import json
from pathlib import Path
import unittest

from financial_ai_qa.evaluator import evaluate_response


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class EvaluatorTest(unittest.TestCase):
    def setUp(self):
        self.case = {
            "case_id": "CASE_1",
            "source_name": "Example Source",
            "source_url": "https://example.com/source",
            "accessed_at": "2026-05-22",
            "required_terms": ["1억원", "원금", "이자"],
            "forbidden_terms": ["전액", "무조건"],
            "date_terms": ["2026-05-22", "접근"],
            "evidence_terms": ["example.com", "Example Source"],
        }

    def test_baseline_response_gets_full_score(self):
        candidate = {
            "response_id": "CASE_1_BASELINE",
            "candidate_type": "baseline",
            "response_text": "2026-05-22 접근 기준 Example Source는 원금과 이자를 합해 1억원까지 설명합니다. Source: https://example.com/source",
            "expected_failure_tags": [],
        }
        result = evaluate_response(self.case, candidate)
        self.assertEqual(result["total_score"], 12)
        self.assertEqual(result["failure_tags"], [])

    def test_unsupported_full_protection_is_tagged(self):
        candidate = {
            "response_id": "CASE_1_BAD",
            "candidate_type": "unsupported_claim",
            "response_text": "무조건 전액 보호됩니다.",
            "expected_failure_tags": ["unsupported_claim"],
        }
        result = evaluate_response(self.case, candidate)
        self.assertIn("unsupported_claim", result["failure_tags"])
        self.assertIn("missing_required_term", result["failure_tags"])
        self.assertIn("missing_timing_boundary", result["failure_tags"])
        self.assertIn("missing_evidence_trace", result["failure_tags"])
        self.assertLess(result["total_score"], 8)

    def test_real_candidate_expected_failure_tags_match_evaluator(self):
        cases = {
            case["case_id"]: case
            for case in json.loads(
                (PROJECT_ROOT / "data/processed/evaluation_cases.json").read_text()
            )
        }
        candidates = json.loads(
            (PROJECT_ROOT / "data/raw/response_candidates.json").read_text()
        )

        for candidate in candidates:
            with self.subTest(response_id=candidate["response_id"]):
                result = evaluate_response(cases[candidate["case_id"]], candidate)
                self.assertEqual(
                    candidate["expected_failure_tags"],
                    result["failure_tags"],
                )

    def test_unsupported_recommendation_overreach_is_tagged(self):
        case = {
            "case_id": "CASE_2",
            "source_name": "Financial API Source",
            "source_url": "https://api.example.com/source",
            "required_terms": ["지원대상", "금리"],
            "forbidden_terms": ["개인 맞춤 추천"],
            "date_terms": ["2026-05-22"],
            "evidence_terms": ["api.example.com", "Financial API Source"],
        }
        candidate = {
            "response_id": "CASE_2_BAD",
            "candidate_type": "unsafe_advice",
            "response_text": "이 API를 보면 본인에게 가장 좋은 상품을 바로 고를 수 있고 승인도 받을 수 있습니다.",
        }

        result = evaluate_response(case, candidate)

        self.assertIn("unsupported_claim", result["failure_tags"])
        self.assertIn("unsafe_financial_advice", result["failure_tags"])

    def test_unsupported_recommendation_overreach_exposes_unsupported_hits(self):
        case = {
            "case_id": "CASE_2",
            "source_name": "Financial API Source",
            "source_url": "https://api.example.com/source",
            "required_terms": ["지원대상", "금리"],
            "forbidden_terms": ["개인 맞춤 추천"],
            "date_terms": ["2026-05-22"],
            "evidence_terms": ["api.example.com", "Financial API Source"],
        }
        candidate = {
            "response_id": "CASE_2_BAD",
            "candidate_type": "unsafe_advice",
            "response_text": "이 API를 보면 본인에게 가장 좋은 상품을 바로 고를 수 있고 승인도 받을 수 있습니다.",
        }

        result = evaluate_response(case, candidate)

        self.assertEqual(
            ["승인도 받을 수", "바로 고를 수", "가장 좋은 상품"],
            result["unsupported_hits"],
        )
        self.assertEqual([], result["forbidden_hits"])

    def test_partial_evasive_answer_gets_partial_grounded_accuracy(self):
        candidate = {
            "response_id": "CASE_1_PARTIAL",
            "candidate_type": "missing_condition",
            "response_text": "이 답변은 공개 출처에 나온 원금 조건을 일부만 설명합니다.",
            "expected_failure_tags": [],
        }

        result = evaluate_response(self.case, candidate)

        self.assertEqual(result["dimension_scores"]["grounded_accuracy"], 2)
        self.assertIn("missing_required_term", result["failure_tags"])
        self.assertIn("missing_timing_boundary", result["failure_tags"])
        self.assertIn("missing_evidence_trace", result["failure_tags"])

    def test_source_linked_evasive_answer_gets_partial_grounded_accuracy(self):
        candidate = {
            "response_id": "CASE_1_SOURCE_LINKED_EVASIVE",
            "candidate_type": "missing_condition",
            "response_text": "2026-05-22 접근 기준 Example Source를 확인해야 합니다. Source: https://example.com/source",
            "expected_failure_tags": [],
        }

        result = evaluate_response(self.case, candidate)

        self.assertEqual(result["evidence_hits"], ["Example Source", "https://example.com/source", "example.com"])
        self.assertEqual(result["dimension_scores"]["grounded_accuracy"], 1)
        self.assertIn("missing_required_term", result["failure_tags"])

    def test_evasive_answer_without_positive_support_gets_partial_grounded_accuracy(self):
        candidate = {
            "response_id": "CASE_1_EVASIVE",
            "candidate_type": "missing_condition",
            "response_text": "상황에 따라 달라질 수 있으므로 자세한 기준을 확인해야 합니다.",
            "expected_failure_tags": [],
        }

        result = evaluate_response(self.case, candidate)

        self.assertEqual(result["dimension_scores"]["grounded_accuracy"], 0)
        self.assertIn("missing_required_term", result["failure_tags"])
        self.assertIn("missing_timing_boundary", result["failure_tags"])
        self.assertIn("missing_evidence_trace", result["failure_tags"])

    def test_evidence_traceability_ignores_topical_non_source_terms(self):
        case = {
            **self.case,
            "evidence_terms": ["예금자보호법"],
            "source_name": "찾기쉬운 생활법령정보",
            "source_url": "https://www.easylaw.go.kr/example",
        }
        candidate = {
            "response_id": "CASE_1_TOPICAL_EVIDENCE_ONLY",
            "candidate_type": "missing_evidence",
            "response_text": "2026-05-22 기준 예금자보호법은 원금과 이자를 합해 1억원까지 설명합니다.",
            "expected_failure_tags": [],
        }

        result = evaluate_response(case, candidate)

        self.assertNotIn("예금자보호법", result["evidence_hits"])
        self.assertIn("missing_evidence_trace", result["failure_tags"])
        self.assertEqual(result["dimension_scores"]["evidence_traceability"], 0)


if __name__ == "__main__":
    unittest.main()
