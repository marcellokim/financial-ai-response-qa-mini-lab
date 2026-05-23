import tempfile
import unittest
from pathlib import Path

from financial_ai_qa.data_io import (
    load_json,
    load_response_candidates,
    load_source_records,
    load_validated_dataset,
    validate_response_candidate,
    validate_response_candidates_against_sources,
    validate_source_record,
    write_json,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA = PROJECT_ROOT / "data" / "raw"


def valid_source_record():
    return {
        "case_id": "CASE_1",
        "source_type": "public_qna",
        "source_name": "source",
        "source_url": "https://example.com/source",
        "accessed_at": "2026-05-22",
        "case_origin": "public_qna",
        "license_or_permission_note": "Public source record used with citation.",
        "transformation_note": "Fields were extracted into a compact evaluation case.",
        "question": "question",
        "reference_answer": "answer",
        "evidence_fields": {},
        "required_terms": [],
        "forbidden_terms": [],
        "date_terms": [],
        "evidence_terms": [],
        "risk_tags": [],
        "allowed_claims": [],
        "forbidden_claims": [],
    }


def valid_response_candidate():
    return {
        "case_id": "CASE_1",
        "response_id": "CASE_1_BASELINE",
        "candidate_type": "baseline",
        "license_or_permission_note": "Derived from a cited public source record.",
        "transformation_note": "Public source record rewritten as an evaluation candidate.",
        "response_text": "text",
        "expected_failure_tags": [],
    }


class DataIOTest(unittest.TestCase):
    def test_load_json_reads_list(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "records.json"
            path.write_text('[{"case_id": "CASE_1"}]', encoding="utf-8")
            self.assertEqual(load_json(path), [{"case_id": "CASE_1"}])

    def test_load_source_records_reads_valid_fixture(self):
        records = load_source_records(RAW_DATA / "public_source_records.json")
        self.assertEqual(len(records), 3)

    def test_load_response_candidates_reads_valid_fixture(self):
        candidates = load_response_candidates(RAW_DATA / "response_candidates.json")
        self.assertEqual(len(candidates), 5)

    def test_load_validated_dataset_reads_valid_fixtures(self):
        sources, candidates = load_validated_dataset(
            RAW_DATA / "public_source_records.json",
            RAW_DATA / "response_candidates.json",
        )
        self.assertEqual(len(sources), 3)
        self.assertEqual(len(candidates), 5)

    def test_validate_source_record_requires_source_url(self):
        record = valid_source_record()
        del record["source_url"]
        with self.assertRaisesRegex(ValueError, "CASE_1.*source_url"):
            validate_source_record(record)

    def test_validate_source_record_rejects_non_object(self):
        with self.assertRaisesRegex(ValueError, "<unknown source record>.*object"):
            validate_source_record(["not", "an", "object"])

    def test_validate_source_record_rejects_non_string_source_url(self):
        record = valid_source_record()
        record["source_url"] = 123
        with self.assertRaisesRegex(ValueError, "CASE_1.*source_url.*string"):
            validate_source_record(record)

    def test_validate_source_record_rejects_invalid_source_type(self):
        record = valid_source_record()
        record["source_type"] = "private_note"
        with self.assertRaisesRegex(ValueError, "CASE_1.*source_type"):
            validate_source_record(record)

    def test_validate_source_record_requires_provenance_notes(self):
        record = valid_source_record()
        del record["transformation_note"]
        with self.assertRaisesRegex(ValueError, "CASE_1.*transformation_note"):
            validate_source_record(record)

    def test_validate_response_candidate_requires_known_candidate_type(self):
        candidate = valid_response_candidate()
        candidate["response_id"] = "CASE_1_BAD"
        candidate["candidate_type"] = "invented_type"
        with self.assertRaisesRegex(ValueError, "CASE_1_BAD.*candidate_type"):
            validate_response_candidate(candidate)

    def test_validate_response_candidate_requires_transformation_note(self):
        candidate = valid_response_candidate()
        del candidate["transformation_note"]
        with self.assertRaisesRegex(ValueError, "CASE_1_BASELINE.*transformation_note"):
            validate_response_candidate(candidate)

    def test_validate_response_candidate_rejects_non_object(self):
        with self.assertRaisesRegex(ValueError, "<unknown response candidate>.*object"):
            validate_response_candidate("not an object")

    def test_validate_response_candidate_rejects_non_string_response_text(self):
        candidate = valid_response_candidate()
        candidate["response_text"] = None
        with self.assertRaisesRegex(ValueError, "CASE_1_BASELINE.*response_text.*string"):
            validate_response_candidate(candidate)

    def test_load_source_records_rejects_duplicate_case_id(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "sources.json"
            first = valid_source_record()
            first["case_id"] = "DUPLICATE"
            second = valid_source_record()
            second["case_id"] = "DUPLICATE"
            second["source_url"] = "https://example.com/2"
            write_json(path, [first, second])
            with self.assertRaisesRegex(ValueError, "duplicate.*case_id.*DUPLICATE"):
                load_source_records(path)

    def test_load_response_candidates_rejects_duplicate_response_id(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "candidates.json"
            first = valid_response_candidate()
            first["response_id"] = "DUPLICATE"
            second = valid_response_candidate()
            second["response_id"] = "DUPLICATE"
            write_json(path, [first, second])
            with self.assertRaisesRegex(ValueError, "duplicate.*response_id.*DUPLICATE"):
                load_response_candidates(path)

    def test_validate_response_candidates_against_sources_rejects_non_object_source(self):
        with self.assertRaisesRegex(ValueError, "<unknown source record>.*object"):
            validate_response_candidates_against_sources([valid_response_candidate()], ["not an object"])

    def test_validate_response_candidates_against_sources_rejects_source_missing_case_id(self):
        source = valid_source_record()
        del source["case_id"]
        with self.assertRaisesRegex(ValueError, "<unknown source record>.*case_id"):
            validate_response_candidates_against_sources([valid_response_candidate()], [source])

    def test_validate_response_candidates_against_sources_rejects_non_object_candidate(self):
        with self.assertRaisesRegex(ValueError, "<unknown response candidate>.*object"):
            validate_response_candidates_against_sources(["not an object"], [valid_source_record()])

    def test_validate_response_candidates_against_sources_rejects_orphan_case_id(self):
        sources = [valid_source_record()]
        candidate = valid_response_candidate()
        candidate["case_id"] = "MISSING_CASE"
        with self.assertRaisesRegex(ValueError, "CASE_1_BASELINE.*case_id.*MISSING_CASE"):
            validate_response_candidates_against_sources([candidate], sources)

    def test_validate_response_candidates_against_sources_rejects_candidate_missing_case_id(self):
        candidate = valid_response_candidate()
        del candidate["case_id"]
        with self.assertRaisesRegex(ValueError, "CASE_1_BASELINE.*case_id"):
            validate_response_candidates_against_sources([candidate], [valid_source_record()])


if __name__ == "__main__":
    unittest.main()
