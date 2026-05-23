from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from financial_ai_qa.data_io import load_source_records, load_validated_dataset, write_json
from financial_ai_qa.evaluator import evaluate_response
from financial_ai_qa.normalizer import normalize_source_records
from financial_ai_qa.reporting import build_report, write_report


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_SOURCES = PROJECT_ROOT / "data" / "raw" / "public_source_records.json"
RAW_CANDIDATES = PROJECT_ROOT / "data" / "raw" / "response_candidates.json"
PROCESSED_CASES = PROJECT_ROOT / "data" / "processed" / "evaluation_cases.json"
SAMPLE_REPORT = PROJECT_ROOT / "reports" / "sample_report.md"


def run_normalize() -> list[dict]:
    source_records = load_source_records(RAW_SOURCES)
    cases = normalize_source_records(source_records)
    write_json(PROCESSED_CASES, cases)
    return cases


def run_evaluate() -> tuple[list[dict], list[dict]]:
    source_records, candidates = load_validated_dataset(RAW_SOURCES, RAW_CANDIDATES)
    cases = normalize_source_records(source_records)
    write_json(PROCESSED_CASES, cases)
    case_by_id = {case["case_id"]: case for case in cases}
    results = []
    for candidate in candidates:
        results.append(evaluate_response(case_by_id[candidate["case_id"]], candidate))
    return cases, results


def run_demo() -> Path:
    cases, results = run_evaluate()
    report = build_report(cases, results)
    write_report(SAMPLE_REPORT, report)
    failure_counts = Counter(tag for result in results for tag in result["failure_tags"])
    failure_count = sum(failure_counts.values())
    print(f"Cases: {len(cases)}")
    print(f"Responses: {len(results)}")
    print(f"Failure tags: {failure_count}")
    for tag, count in sorted(failure_counts.items()):
        print(f"- {tag}: {count}")
    print(f"Report: {SAMPLE_REPORT.relative_to(PROJECT_ROOT)}")
    return SAMPLE_REPORT


def main() -> None:
    parser = argparse.ArgumentParser(description="Financial AI response QA mini lab")
    parser.add_argument("command", choices=("normalize", "evaluate", "report", "demo"))
    args = parser.parse_args()

    if args.command == "normalize":
        cases = run_normalize()
        print(f"Wrote {len(cases)} cases to {PROCESSED_CASES.relative_to(PROJECT_ROOT)}")
    elif args.command == "evaluate":
        _, results = run_evaluate()
        print(f"Evaluated {len(results)} response candidates")
    else:
        run_demo()


if __name__ == "__main__":
    main()
