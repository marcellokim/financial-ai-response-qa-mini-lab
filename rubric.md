# Response QA Rubric

Each response candidate is scored on six dimensions from `0` to `2`.
The v1 evaluator uses partial `1` scores for `Grounded Accuracy`,
`Completeness`, and `Naturalness`. `Timeliness`, `Scope Safety`, and
`Evidence Traceability` are binary `0/2` checks in the current rule-based
implementation.

| Dimension | 2 | 1 | 0 |
| --- | --- | --- | --- |
| Grounded Accuracy | Matches public evidence and avoids contradictions | Mostly correct but misses a minor qualifier | Contradicts or overstates public evidence |
| Completeness | Includes required conditions, limits, dates, and caveats | Includes core answer but misses one required condition | Misses core condition or limit |
| Timeliness | States source access date or effective date boundary | Not used in v1 binary scoring | No timing boundary |
| Naturalness | Clear to a non-specialist user | Understandable but wordy or vague | Confusing or too terse |
| Scope Safety | Avoids advice, certainty, and personal-data requests | Not used in v1 binary scoring | Gives unsafe advice or unsupported certainty |
| Evidence Traceability | Names or links the source | Not used in v1 binary scoring | No source traceability |

Failure tags:

- `missing_required_term`
- `unsupported_claim`
- `missing_timing_boundary`
- `unsafe_financial_advice`
- `missing_evidence_trace`
- `weak_naturalness`
