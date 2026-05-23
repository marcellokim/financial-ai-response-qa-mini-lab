from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SOURCE_REQUIRED_FIELDS = (
    "case_id",
    "source_type",
    "source_name",
    "source_url",
    "accessed_at",
    "case_origin",
    "license_or_permission_note",
    "transformation_note",
    "question",
    "reference_answer",
    "evidence_fields",
    "required_terms",
    "forbidden_terms",
    "date_terms",
    "evidence_terms",
    "risk_tags",
    "allowed_claims",
    "forbidden_claims",
)

RESPONSE_REQUIRED_FIELDS = (
    "case_id",
    "response_id",
    "candidate_type",
    "license_or_permission_note",
    "transformation_note",
    "response_text",
    "expected_failure_tags",
)

ALLOWED_CASE_ORIGINS = {
    "public_qna",
    "public_api_record",
    "derived_from_public_record",
}

ALLOWED_SOURCE_TYPES = {
    "public_qna",
    "public_api_record",
}

ALLOWED_CANDIDATE_TYPES = {
    "baseline",
    "missing_condition",
    "unsupported_claim",
    "stale_or_no_date",
    "unsafe_advice",
    "no_evidence",
}


def load_json(path: str | Path) -> Any:
    json_path = Path(path)
    with json_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: str | Path, payload: Any) -> None:
    json_path = Path(path)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def _require_object(record: Any, record_label: str) -> None:
    if not isinstance(record, dict):
        raise ValueError(f"{record_label} must be an object")


def _require_fields(record: dict[str, Any], required_fields: tuple[str, ...], record_label: str) -> None:
    missing = [field for field in required_fields if field not in record]
    if missing:
        raise ValueError(f"{record_label} missing required field(s): {', '.join(missing)}")


def _require_string(record: dict[str, Any], field_name: str, record_label: str) -> None:
    if not isinstance(record[field_name], str):
        raise ValueError(f"{record_label} field '{field_name}' must be a string")


def _require_list(record: dict[str, Any], field_name: str, record_label: str) -> None:
    if not isinstance(record[field_name], list):
        raise ValueError(f"{record_label} field '{field_name}' must be a list")


def validate_source_record(record: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(record, dict):
        record_label = "<unknown source record>"
        _require_object(record, record_label)
    record_label = str(record.get("case_id", "<unknown source record>"))
    _require_fields(record, SOURCE_REQUIRED_FIELDS, record_label)
    for field_name in (
        "case_id",
        "source_type",
        "source_name",
        "source_url",
        "accessed_at",
        "case_origin",
        "license_or_permission_note",
        "transformation_note",
        "question",
        "reference_answer",
    ):
        _require_string(record, field_name, record_label)
    if record["source_type"] not in ALLOWED_SOURCE_TYPES:
        raise ValueError(f"{record_label} has invalid source_type: {record['source_type']}")
    if record["case_origin"] not in ALLOWED_CASE_ORIGINS:
        raise ValueError(f"{record_label} has invalid case_origin: {record['case_origin']}")
    if not record["source_url"].startswith("https://"):
        raise ValueError(f"{record_label} source_url must start with https://")
    if not isinstance(record["evidence_fields"], dict):
        raise ValueError(f"{record_label} evidence_fields must be an object")
    for field_name in (
        "required_terms",
        "forbidden_terms",
        "date_terms",
        "evidence_terms",
        "risk_tags",
        "allowed_claims",
        "forbidden_claims",
    ):
        _require_list(record, field_name, record_label)
    return record


def validate_response_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(candidate, dict):
        record_label = "<unknown response candidate>"
        _require_object(candidate, record_label)
    record_label = str(candidate.get("response_id", "<unknown response candidate>"))
    _require_fields(candidate, RESPONSE_REQUIRED_FIELDS, record_label)
    for field_name in (
        "case_id",
        "response_id",
        "candidate_type",
        "license_or_permission_note",
        "transformation_note",
        "response_text",
    ):
        _require_string(candidate, field_name, record_label)
    if candidate["candidate_type"] not in ALLOWED_CANDIDATE_TYPES:
        raise ValueError(f"{record_label} has invalid candidate_type: {candidate['candidate_type']}")
    if not isinstance(candidate["expected_failure_tags"], list):
        raise ValueError(f"{record_label} expected_failure_tags must be a list")
    if not candidate["response_text"].strip():
        raise ValueError(f"{record_label} response_text must not be empty")
    return candidate


def _reject_duplicate(records: list[dict[str, Any]], field_name: str, record_type: str) -> None:
    seen = set()
    for record in records:
        value = record[field_name]
        if value in seen:
            raise ValueError(f"duplicate {record_type} {field_name}: {value}")
        seen.add(value)


def load_source_records(path: str | Path) -> list[dict[str, Any]]:
    records = load_json(path)
    if not isinstance(records, list):
        raise ValueError("source records file must contain a JSON list")
    validated = [validate_source_record(record) for record in records]
    _reject_duplicate(validated, "case_id", "source record")
    return validated


def load_response_candidates(path: str | Path) -> list[dict[str, Any]]:
    candidates = load_json(path)
    if not isinstance(candidates, list):
        raise ValueError("response candidates file must contain a JSON list")
    validated = [validate_response_candidate(candidate) for candidate in candidates]
    _reject_duplicate(validated, "response_id", "response candidate")
    return validated


def validate_response_candidates_against_sources(
    candidates: list[dict[str, Any]],
    sources: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_case_ids = set()
    for source in sources:
        if not isinstance(source, dict):
            raise ValueError("<unknown source record> must be an object")
        record_label = str(source.get("case_id", "<unknown source record>"))
        if "case_id" not in source:
            raise ValueError(f"{record_label} missing required field(s): case_id")
        if not isinstance(source["case_id"], str):
            raise ValueError(f"{record_label} field 'case_id' must be a string")
        source_case_ids.add(source["case_id"])
    for candidate in candidates:
        validated_candidate = validate_response_candidate(candidate)
        record_label = validated_candidate["response_id"]
        case_id = validated_candidate["case_id"]
        if case_id not in source_case_ids:
            raise ValueError(f"{record_label} has orphan case_id: {case_id}")
    return candidates


def load_validated_dataset(
    source_path: str | Path,
    candidate_path: str | Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    sources = load_source_records(source_path)
    candidates = load_response_candidates(candidate_path)
    validate_response_candidates_against_sources(candidates, sources)
    return sources, candidates
