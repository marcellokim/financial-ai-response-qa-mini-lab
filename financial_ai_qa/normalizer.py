from __future__ import annotations

from typing import Any

from financial_ai_qa.data_io import SOURCE_REQUIRED_FIELDS, validate_source_record


def normalize_source_record(record: dict[str, Any]) -> dict[str, Any]:
    validated = validate_source_record(record)
    return {field_name: validated[field_name] for field_name in SOURCE_REQUIRED_FIELDS}


def normalize_source_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    seen_case_ids: set[str] = set()
    for record in records:
        normalized_record = normalize_source_record(record)
        case_id = normalized_record["case_id"]
        if case_id in seen_case_ids:
            raise ValueError(f"duplicate source record case_id: {case_id}")
        seen_case_ids.add(case_id)
        normalized.append(normalized_record)
    return normalized
