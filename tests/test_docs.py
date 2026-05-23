import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class DocsTest(unittest.TestCase):
    def test_owner_guide_contains_end_to_end_understanding_sections(self):
        text = (PROJECT_ROOT / "docs" / "owner_guide.md").read_text(encoding="utf-8")
        required_sections = [
            "## 1. 프로젝트 한 줄 설명",
            "## 2. 왜 이 직무와 연결되는가",
            "## 3. 데이터 출처와 공개성",
            "## 4. 파이프라인 구조",
            "## 5. 평가 로직 설명",
            "## 6. 데모 실행 방법",
            "## 7. 면접에서 말할 수 있는 것과 말하면 안 되는 것",
            "## 8. 직접 구현 이해도 체크리스트",
        ]
        for section in required_sections:
            self.assertIn(section, text)

    def test_public_docs_do_not_make_positive_forbidden_claims(self):
        paths = [
            PROJECT_ROOT / "README.md",
            PROJECT_ROOT / "docs" / "owner_guide.md",
            PROJECT_ROOT / "docs" / "interview_notes.md",
            PROJECT_ROOT / "docs" / "user_qa_report.md",
        ]
        positive_forbidden_claims = [
            "특정 회사의 운영 AI를 평가했습니다",
            "production banking AI를 평가했습니다",
            "실제 고객 응답을 분석했습니다",
            "모델 성능을 개선했습니다",
            "금융상품을 추천하는 서비스입니다",
        ]
        for path in paths:
            text = path.read_text(encoding="utf-8")
            for phrase in positive_forbidden_claims:
                self.assertNotIn(phrase, text)

        owner_guide = (PROJECT_ROOT / "docs" / "owner_guide.md").read_text(encoding="utf-8")
        self.assertIn("실제 고객 응답을 분석했다고 말하지 않는다", owner_guide)
        self.assertIn("금융상품을 추천하는 서비스라고 말하지 않는다", owner_guide)

    def test_owner_guide_describes_actual_scoring_behavior(self):
        text = (PROJECT_ROOT / "docs" / "owner_guide.md").read_text(encoding="utf-8")
        required_phrases = [
            "1점",
            "grounded_accuracy",
            "completeness",
            "naturalness",
            "0/2",
            "timeliness",
            "scope_safety",
            "evidence_traceability",
        ]
        for phrase in required_phrases:
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
