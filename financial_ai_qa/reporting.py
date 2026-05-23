from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from financial_ai_qa.evaluator import DIMENSIONS


def _dimension_average_scores(results: list[dict[str, Any]]) -> dict[str, float]:
    totals: dict[str, float] = {dimension: 0.0 for dimension in DIMENSIONS}
    counts: dict[str, int] = {dimension: 0 for dimension in DIMENSIONS}

    for result in results:
        dimension_scores = result.get("dimension_scores", {})
        if not isinstance(dimension_scores, dict):
            continue
        for dimension in DIMENSIONS:
            score = dimension_scores.get(dimension)
            if isinstance(score, (int, float)):
                totals[dimension] += score
                counts[dimension] += 1

    return {
        dimension: totals[dimension] / counts[dimension]
        for dimension in DIMENSIONS
        if counts[dimension]
    }


def build_report(cases: list[dict[str, Any]], results: list[dict[str, Any]]) -> str:
    failure_counts = Counter(tag for result in results for tag in result["failure_tags"])
    dimension_averages = _dimension_average_scores(results)
    average_score = sum(result["total_score"] for result in results) / len(results) if results else 0
    max_scores = {result["max_score"] for result in results}
    if len(max_scores) > 1:
        raise ValueError(f"inconsistent max_score values: {sorted(max_scores)}")
    max_score = next(iter(max_scores)) if max_scores else None
    average_score_text = f"{average_score:.1f} / {max_score}" if max_score is not None else "0"

    lines = [
        "# Financial AI Response QA Sample Report",
        "",
        "## Scope",
        "",
        "This report evaluates public-source-derived response candidates against public finance information. It is not financial advice, not a production AI evaluation, and not based on customer data.",
        "",
        "## Source Catalog Summary",
        "",
    ]
    for case in cases:
        lines.append(f"- `{case['case_id']}`: {case['source_name']} ({case['source_url']})")

    lines.extend([
        "",
        "## Score Summary",
        "",
        f"- Cases: {len(cases)}",
        f"- Response candidates: {len(results)}",
        f"- Average score: {average_score_text}",
        "",
        "## Failure Tag Frequency",
        "",
    ])
    if failure_counts:
        for tag, count in sorted(failure_counts.items()):
            lines.append(f"- `{tag}`: {count}")
    else:
        lines.append("- No failure tags.")

    lines.extend([
        "",
        "## Dimension Score Summary",
        "",
    ])
    if dimension_averages:
        for dimension in DIMENSIONS:
            if dimension in dimension_averages:
                lines.append(f"- `{dimension}`: {dimension_averages[dimension]:.1f} / 2")
    else:
        lines.append("- No dimension scores.")

    lines.extend([
        "",
        "## Case Reviews",
        "",
    ])
    for result in results:
        lines.extend([
            f"### {result['response_id']}",
            "",
            f"- Case: `{result['case_id']}`",
            f"- Candidate type: `{result['candidate_type']}`",
            f"- Score: {result['total_score']} / {result['max_score']}",
            f"- Failure tags: {', '.join(result['failure_tags']) if result['failure_tags'] else 'none'}",
            f"- Improvement insight: {result['suggested_improvement']}",
            "",
        ])

    lines.extend([
        "## Limitations",
        "",
        "- The default dataset is a small curated public-source sample.",
        "- The evaluator is rule-based and does not judge truth beyond configured public evidence fields.",
        "- The project does not recommend products, assess eligibility, or improve a real model.",
        "- Live API calls are not required for the default demo.",
        "",
    ])
    return "\n".join(lines)


def write_report(path: str | Path, report: str) -> None:
    report_path = Path(path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")
