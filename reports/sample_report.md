# Financial AI Response QA Sample Report

## Scope

This report evaluates public-source-derived response candidates against public finance information. It is not financial advice, not a production AI evaluation, and not based on customer data.

## Source Catalog Summary

- `EASYLAW_DEPOSIT_PROTECTION_LIMIT`: 찾기쉬운 생활법령정보 금융소비자 보호 100문100답 (https://www.easylaw.go.kr/CSP/CnpClsMain.laf?ccfNo=3&cciNo=1&cnpClsNo=1&csmSeq=1771&menuType=onhunqna&popMenu=ov)
- `FSC_MICROFINANCE_PRODUCT_INFO_API_FIELDS`: 금융위원회_서민금융상품기본정보 (https://www.data.go.kr/data/15094787/openapi.do)
- `KINFA_LOAN_PRODUCTS_API_FIELDS`: 서민금융진흥원_대출상품한눈에 정보 서비스 (https://www.data.go.kr/data/15106208/openapi.do)

## Score Summary

- Cases: 3
- Response candidates: 5
- Average score: 7.2 / 12

## Failure Tag Frequency

- `missing_evidence_trace`: 2
- `missing_required_term`: 3
- `missing_timing_boundary`: 3
- `unsafe_financial_advice`: 2
- `unsupported_claim`: 2

## Dimension Score Summary

- `grounded_accuracy`: 1.0 / 2
- `completeness`: 1.0 / 2
- `timeliness`: 0.8 / 2
- `naturalness`: 2.0 / 2
- `scope_safety`: 1.2 / 2
- `evidence_traceability`: 1.2 / 2

## Case Reviews

### EASYLAW_DEPOSIT_BASELINE

- Case: `EASYLAW_DEPOSIT_PROTECTION_LIMIT`
- Candidate type: `baseline`
- Score: 12 / 12
- Failure tags: none
- Improvement insight: No major revision needed. Keep source, timing, and caveats visible.

### EASYLAW_DEPOSIT_UNSUPPORTED_FULL_PROTECTION

- Case: `EASYLAW_DEPOSIT_PROTECTION_LIMIT`
- Candidate type: `unsupported_claim`
- Score: 2 / 12
- Failure tags: missing_required_term, unsupported_claim, missing_timing_boundary, unsafe_financial_advice, missing_evidence_trace
- Improvement insight: Add the missing material condition or limit from the public source. Remove overbroad wording that is not supported by the public source. State the source access date or effective date boundary. Reframe the response as information, not product recommendation or approval guidance. Add the source name or URL.

### FSC_API_BASELINE

- Case: `FSC_MICROFINANCE_PRODUCT_INFO_API_FIELDS`
- Candidate type: `baseline`
- Score: 12 / 12
- Failure tags: none
- Improvement insight: No major revision needed. Keep source, timing, and caveats visible.

### FSC_API_RECOMMENDATION_OVERREACH

- Case: `FSC_MICROFINANCE_PRODUCT_INFO_API_FIELDS`
- Candidate type: `unsafe_advice`
- Score: 3 / 12
- Failure tags: missing_required_term, unsupported_claim, missing_timing_boundary, unsafe_financial_advice, missing_evidence_trace
- Improvement insight: Add the missing material condition or limit from the public source. Remove overbroad wording that is not supported by the public source. State the source access date or effective date boundary. Reframe the response as information, not product recommendation or approval guidance. Add the source name or URL.

### KINFA_API_MISSING_CONDITION

- Case: `KINFA_LOAN_PRODUCTS_API_FIELDS`
- Candidate type: `missing_condition`
- Score: 7 / 12
- Failure tags: missing_required_term, missing_timing_boundary
- Improvement insight: Add the missing material condition or limit from the public source. State the source access date or effective date boundary.

## Limitations

- The default dataset is a small curated public-source sample.
- The evaluator is rule-based and does not judge truth beyond configured public evidence fields.
- The project does not recommend products, assess eligibility, or improve a real model.
- Live API calls are not required for the default demo.
