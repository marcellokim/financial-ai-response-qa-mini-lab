# Financial AI Response QA Mini Lab

Financial AI Response QA Mini Lab is a standard-library Python project that turns public finance sources into QA test cases and evaluates finance-related AI response candidates for evidence, completeness, timing, safety, naturalness, and source traceability.

It is built as a portfolio-safe mini lab: small enough to inspect quickly, but complete enough to show test-case management, rubric-based response review, failure tagging, report generation, and public-data boundaries.

## Key Features

- Public-source-based test case management
- Rule-based response QA against a written rubric
- Failure tagging for omissions, unsupported claims, stale timing, unsafe advice, and missing evidence
- Markdown report generation with score summaries and improvement insights
- Korean owner guide for explaining the project end to end
- Unit tests covering data validation, normalization, evaluation, reporting, and public-claim safety

## What This Does Not Claim

- It is not a banking AI service.
- It is not financial advice.
- It does not use real customer conversations.
- It does not use internal banking data.
- It does not evaluate any company's production AI.
- It does not improve a real model.

## Tech Stack

- Python 3, standard library only
- `unittest` for tests
- `make` as a thin command wrapper
- GitHub Actions CI for demo and test verification

## Quick Start

```bash
git clone https://github.com/marcellokim/financial-ai-response-qa-mini-lab.git
cd financial-ai-response-qa-mini-lab
make demo
make test
```

`make demo` normalizes curated public-source records, evaluates public-source-derived response variants, and writes `reports/sample_report.md`.

Expected demo summary:

```text
Cases: 3
Responses: 5
Failure tags: 12
Report: reports/sample_report.md
```

If `make` is unavailable, use the Python entry points directly:

```bash
python3 -m financial_ai_qa.cli demo
python3 -m unittest discover -s tests -v
```

## Environment Variables

No environment variables are required for the default demo. No API key is committed or needed.

## Project Structure

```text
.github/workflows/       CI workflow for demo and tests
data/raw/                 Curated public-source records and response variants
data/processed/           Generated normalized evaluation cases
financial_ai_qa/          Python standard-library implementation
reports/sample_report.md  Generated sample QA report
docs/owner_guide.md       Korean guide for explaining the project end to end
docs/interview_notes.md   Interview-safe usage notes
docs/user_qa_report.md    Real-user QA review notes
```

## Data Sources And Boundaries

The default demo uses small curated samples from public pages and public data portals. Live API fetching is not required for the demo, and no API key is committed.

See `data_sources.md` for the source catalog and credential rule.

## Portfolio Review Notes

- `docs/owner_guide.md`: file-by-file Korean guide for explaining the project as if built end to end.
- `docs/interview_notes.md`: allowed and forbidden claims for interview-safe positioning.
- `docs/user_qa_report.md`: local real-user QA review notes.

## Verification

Last local verification: 2026-05-23 KST.

```bash
make clean && make demo && make test
```

Result: 42 tests passed.

## Deployment

This is a CLI/reporting mini lab, not a web service. GitHub is the recommended review surface; no deployment target is required.

## License

MIT License. See `LICENSE`.
