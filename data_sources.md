# Data Sources

Access date for v1 samples: 2026-05-22 KST.

## Sources Used In Default Demo

| Source ID | Source | URL | Use | Boundary |
| --- | --- | --- | --- | --- |
| EASYLAW_DEPOSIT_PROTECTION_LIMIT | 찾기쉬운 생활법령정보 금융소비자 보호 100문100답 | https://www.easylaw.go.kr/CSP/CnpClsMain.laf?ccfNo=3&cciNo=1&cnpClsNo=1&csmSeq=1771&menuType=onhunqna&popMenu=ov | Public Q&A baseline for deposit protection wording | Store a small case record with URL and short evidence fields, not a copied corpus |
| FSC_MICROFINANCE_PRODUCT_INFO_API | 금융위원회_서민금융상품기본정보 | https://www.data.go.kr/data/15094787/openapi.do | Public API metadata for product fields such as product name, eligibility, rate, limit, repayment method, and institution | Default demo stores source metadata and derived evaluation fields, not an API dump |
| KINFA_LOAN_PRODUCTS_API | 서민금융진흥원_대출상품한눈에 정보 서비스 | https://www.data.go.kr/data/15106208/openapi.do | Public API metadata for loan product comparison fields | Default demo stores source metadata and derived evaluation fields, not an API dump |
| LAW_OPEN_API_GUIDE | 국가법령정보 공동활용 | https://open.law.go.kr/LSO/openApi/guideList.do | Optional traceability source for statute references | No live API call in default demo |

## Credential Rule

Do not commit API keys, cookies, account identifiers, or private request logs. If live API fetching is added later, keep it optional and read credentials from environment variables.
