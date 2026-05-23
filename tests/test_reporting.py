import io
import unittest
from contextlib import redirect_stdout

from financial_ai_qa.cli import SAMPLE_REPORT, run_demo
from financial_ai_qa.reporting import build_report


class ReportingTest(unittest.TestCase):
    def test_build_report_includes_summary_and_limitations(self):
        cases = [
            {
                "case_id": "CASE_1",
                "source_name": "Example Source",
                "source_url": "https://example.com/source",
                "question": "Question",
            }
        ]
        results = [
            {
                "case_id": "CASE_1",
                "response_id": "CASE_1_BAD",
                "candidate_type": "unsupported_claim",
                "dimension_scores": {
                    "grounded_accuracy": 0,
                    "completeness": 1,
                    "timeliness": 0,
                    "naturalness": 2,
                    "scope_safety": 0,
                    "evidence_traceability": 0,
                },
                "total_score": 4,
                "max_score": 12,
                "failure_tags": ["unsupported_claim", "missing_evidence_trace"],
                "suggested_improvement": "Remove overbroad wording. Add the source name or URL.",
            }
        ]
        report = build_report(cases, results)
        self.assertIn("# Financial AI Response QA Sample Report", report)
        self.assertIn("Example Source", report)
        self.assertIn("unsupported_claim", report)
        self.assertIn("Limitations", report)
        self.assertIn("not financial advice", report)
        self.assertIn("## Dimension Score Summary", report)
        self.assertIn("`grounded_accuracy`: 0.0 / 2", report)
        self.assertIn("## Case Reviews", report)
        self.assertNotIn("Representative Case Reviews", report)

    def test_build_report_uses_result_max_score_in_summary(self):
        report = build_report(
            [],
            [
                {
                    "case_id": "CASE_1",
                    "response_id": "CASE_1_SMALL_RUBRIC",
                    "candidate_type": "baseline",
                    "dimension_scores": {
                        "grounded_accuracy": 2,
                        "completeness": 2,
                    },
                    "total_score": 4,
                    "max_score": 8,
                    "failure_tags": [],
                    "suggested_improvement": "No major revision needed.",
                }
            ],
        )

        self.assertIn("- Average score: 4.0 / 8", report)
        self.assertIn("- Score: 4 / 8", report)

    def test_build_report_summarizes_each_dimension_score(self):
        report = build_report(
            [],
            [
                {
                    "case_id": "CASE_1",
                    "response_id": "CASE_1_BASELINE",
                    "candidate_type": "baseline",
                    "dimension_scores": {
                        "grounded_accuracy": 2,
                        "completeness": 2,
                        "timeliness": 2,
                        "naturalness": 2,
                        "scope_safety": 2,
                        "evidence_traceability": 2,
                    },
                    "total_score": 12,
                    "max_score": 12,
                    "failure_tags": [],
                    "suggested_improvement": "No major revision needed.",
                },
                {
                    "case_id": "CASE_2",
                    "response_id": "CASE_2_BAD",
                    "candidate_type": "unsupported_claim",
                    "dimension_scores": {
                        "grounded_accuracy": 0,
                        "completeness": 1,
                        "timeliness": 0,
                        "naturalness": 2,
                        "scope_safety": 0,
                        "evidence_traceability": 0,
                    },
                    "total_score": 3,
                    "max_score": 12,
                    "failure_tags": ["unsupported_claim"],
                    "suggested_improvement": "Remove overbroad wording.",
                },
            ],
        )

        self.assertIn("## Dimension Score Summary", report)
        for dimension in (
            "grounded_accuracy",
            "completeness",
            "timeliness",
            "naturalness",
            "scope_safety",
            "evidence_traceability",
        ):
            self.assertIn(f"`{dimension}`", report)

    def test_build_report_rejects_inconsistent_max_scores(self):
        results = [
            {
                "case_id": "CASE_1",
                "response_id": "CASE_1_SCORE_12",
                "candidate_type": "baseline",
                "total_score": 10,
                "max_score": 12,
                "failure_tags": [],
                "suggested_improvement": "No major revision needed.",
            },
            {
                "case_id": "CASE_2",
                "response_id": "CASE_2_SCORE_8",
                "candidate_type": "baseline",
                "total_score": 7,
                "max_score": 8,
                "failure_tags": [],
                "suggested_improvement": "No major revision needed.",
            },
        ]

        with self.assertRaisesRegex(ValueError, "inconsistent max_score values"):
            build_report([], results)

    def test_build_report_handles_empty_results(self):
        report = build_report([], [])

        self.assertIn("- Response candidates: 0", report)
        self.assertIn("- Average score: 0\n", report)
        self.assertIn("- No failure tags.", report)
        self.assertIn("- No dimension scores.", report)
        self.assertIn("## Case Reviews", report)

    def test_run_demo_regenerates_sample_report_from_fixtures(self):
        if SAMPLE_REPORT.exists():
            SAMPLE_REPORT.unlink()

        output = io.StringIO()
        with redirect_stdout(output):
            report_path = run_demo()

        self.assertEqual(SAMPLE_REPORT, report_path)
        self.assertIn("Report: reports/sample_report.md", output.getvalue())
        report = SAMPLE_REPORT.read_text(encoding="utf-8")
        self.assertIn("- Cases: 3", report)
        self.assertIn("- Response candidates: 5", report)
        self.assertIn("## Dimension Score Summary", report)
        self.assertIn("## Case Reviews", report)
        self.assertIn("- missing_required_term:", output.getvalue())


if __name__ == "__main__":
    unittest.main()
