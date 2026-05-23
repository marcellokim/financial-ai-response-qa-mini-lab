import unittest
from pathlib import Path

from financial_ai_qa.data_io import SOURCE_REQUIRED_FIELDS, load_json, load_source_records
from financial_ai_qa.normalizer import normalize_source_record, normalize_source_records


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"


class NormalizerTest(unittest.TestCase):
    def test_normalize_source_record_preserves_public_traceability(self):
        source = {
            "case_id": "CASE_1",
            "source_type": "public_qna",
            "source_name": "Example Source",
            "source_url": "https://example.com/source",
            "accessed_at": "2026-05-22",
            "case_origin": "public_qna",
            "license_or_permission_note": "Public source record used with citation.",
            "transformation_note": "Fields were extracted into a compact evaluation case.",
            "question": "What is protected?",
            "reference_answer": "The source says 1억원 is the limit.",
            "evidence_fields": {"limit": "1억원"},
            "required_terms": ["1억원"],
            "forbidden_terms": ["전액"],
            "date_terms": ["2026-05-22"],
            "evidence_terms": ["example.com"],
            "risk_tags": ["deposit_protection"],
            "allowed_claims": ["limit explanation"],
            "forbidden_claims": ["full protection"],
        }
        normalized = normalize_source_record(source)
        self.assertEqual(normalized["case_id"], "CASE_1")
        self.assertEqual(normalized["case_origin"], "public_qna")
        self.assertEqual(normalized["source_url"], "https://example.com/source")
        self.assertEqual(normalized["required_terms"], ["1억원"])

    def test_normalized_keys_match_validated_source_fields(self):
        source = {
            "case_id": "CASE_1",
            "source_type": "public_qna",
            "source_name": "Example Source",
            "source_url": "https://example.com/source",
            "accessed_at": "2026-05-22",
            "case_origin": "public_qna",
            "license_or_permission_note": "Public source record used with citation.",
            "transformation_note": "Fields were extracted into a compact evaluation case.",
            "question": "Question",
            "reference_answer": "Answer",
            "evidence_fields": {},
            "required_terms": [],
            "forbidden_terms": [],
            "date_terms": [],
            "evidence_terms": [],
            "risk_tags": [],
            "allowed_claims": [],
            "forbidden_claims": [],
            "unexpected_field": "must not leak",
        }
        normalized = normalize_source_record(source)
        self.assertEqual(list(normalized.keys()), list(SOURCE_REQUIRED_FIELDS))

    def test_normalize_source_records_rejects_duplicate_case_id(self):
        source = {
            "case_id": "CASE_1",
            "source_type": "public_qna",
            "source_name": "Example Source",
            "source_url": "https://example.com/source",
            "accessed_at": "2026-05-22",
            "case_origin": "public_qna",
            "license_or_permission_note": "Public source record used with citation.",
            "transformation_note": "Fields were extracted into a compact evaluation case.",
            "question": "Question",
            "reference_answer": "Answer",
            "evidence_fields": {},
            "required_terms": [],
            "forbidden_terms": [],
            "date_terms": [],
            "evidence_terms": [],
            "risk_tags": [],
            "allowed_claims": [],
            "forbidden_claims": [],
        }
        with self.assertRaisesRegex(ValueError, "duplicate source record case_id: CASE_1"):
            normalize_source_records([source, dict(source)])

    def test_processed_evaluation_cases_match_normalized_raw_sources(self):
        raw_sources = load_source_records(RAW_DATA / "public_source_records.json")
        processed_cases = load_json(PROCESSED_DATA / "evaluation_cases.json")
        self.assertEqual(normalize_source_records(raw_sources), processed_cases)


if __name__ == "__main__":
    unittest.main()
