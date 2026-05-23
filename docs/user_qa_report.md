# User QA Report

Date: 2026-05-23

## Scope

This QA pass reviewed the portfolio project as a real reviewer would first encounter it: open the local project files, read the public-facing docs, run the demo, inspect the generated report, and check whether the claims stay inside the public-data boundary.

This is a local review record. It is not a submission approval, upload instruction, or evidence of external submission.

## Method

- Used Computer Use with Google Chrome to open local project files through `file://` URLs.
- Reviewed `README.md`, `reports/sample_report.md`, `docs/owner_guide.md`, and `docs/interview_notes.md` in the browser.
- Used normal terminal execution for commands because Computer Use access to Terminal was blocked by the local safety policy.
- Re-ran the project demo and unit tests with `make clean && make demo && make test`.

## Scenario Results

### 1. First-read project comprehension

Result: Pass

Evidence: `README.md` clearly states what the lab demonstrates and what it does not claim.

Note: Local Chrome displays Markdown as raw text, so GitHub/editor rendering is better for review.

### 2. Public-data boundary review

Result: Pass

Evidence: README and interview notes state that the project uses public finance sources and public Q&A, not customer or internal data.

Note: This boundary should stay visible in any portfolio explanation.

### 3. Generated report review

Result: Pass

Evidence: `reports/sample_report.md` shows source summary, score summary, failure-tag frequency, dimension scores, case reviews, and limitations.

Note: The report is usable, but long raw Markdown lines reduce local browser readability.

### 4. Owner understanding review

Result: Pass

Evidence: `docs/owner_guide.md` explains project purpose, job relevance, data flow, scoring logic, demo flow, allowed claims, forbidden claims, and understanding checklist.

Note: This satisfies the goal of explaining the project as if built end to end.

### 5. Interview-safe positioning

Result: Pass

Evidence: `docs/interview_notes.md` separates allowed claims, forbidden claims, and a 30-second explanation.

Note: Short enough to rehearse before interview use.

### 6. Command-line verification

Result: Pass

Evidence: `make clean && make demo && make test` completed with 3 cases, 5 response candidates, 12 failure tags, and 42 passing tests.

Note: Demo regenerated `data/processed/evaluation_cases.json` and `reports/sample_report.md`.

## Findings

### P0 / P1

None found.

No blocker was found for using this as a portfolio seed in AI response QA or service-planning application workflows, provided the explanation stays within the documented public-data and personal-project boundary.

### P2

- Local browser review is readable but not polished because Chrome renders local Markdown files as plain text. If this project is shown live, a rendered GitHub page, editor preview, or optional HTML report would create a better first impression.

### P3

- The sample report has enough content for review, but the case-review section is dense in raw Markdown. A short executive summary at the top is already present, so this is a presentation issue rather than a correctness issue.

## Claim Safety Check

Allowed:

- Personal QA lab built from public finance sources and public Q&A.
- Test-case normalization, response-candidate evaluation, failure tagging, and Markdown reporting.
- Evidence that the applicant can structure AI response QA work and convert failures into improvement insights.

Do not claim:

- Production banking AI evaluation.
- Customer conversation analysis.
- Internal bank data use.
- Real model-performance improvement.
- Financial-product recommendation or eligibility decisioning.

## Verdict

Usable as a portfolio-supporting project for the application and interview narrative.

The strongest usage is not "I built an AI model." The strongest usage is "I turned public finance information into repeatable AI response QA cases, measured response failures by rubric, and documented improvement insights while keeping source, timing, and safety boundaries visible."
