# 금융 응답 점검 포트폴리오

공개 금융 원문과 공개 Q&A를 평가 케이스로 만들고, 인공지능 응답 후보를 정확성, 완성도, 시점 표시, 안전성, 자연스러움, 출처 추적성 기준으로 점검하는 개인 포트폴리오 프로젝트입니다.

핵심은 금융 서비스를 만들었다는 주장이 아니라, 인공지능 응답을 감으로 평가하지 않고 기준, 실패 유형, 근거, 보고서로 남기는 과정을 보여주는 것입니다.

## 빠른 확인

```bash
git clone https://github.com/marcellokim/financial-ai-response-qa-mini-lab.git
cd financial-ai-response-qa-mini-lab
make verify
```

`make verify`는 생성물을 지우고, 공개 자료 기반 샘플을 정규화하고, 응답 후보를 평가하고, 보고서를 만든 뒤, 전체 테스트를 실행합니다.

`make`를 사용할 수 없으면 아래처럼 직접 실행할 수 있습니다.

```bash
python3 -m financial_ai_qa.cli demo
python3 -m unittest discover -s tests -v
```

## 무엇을 보여주는가

- 공개 출처 기반 평가 케이스 관리
- 금융 응답 품질을 여섯 가지 기준으로 나누는 평가표
- 누락, 근거 없는 주장, 오래된 기준일, 위험한 조언, 출처 부족 같은 실패 유형 분류
- 점수 요약과 개선 포인트가 포함된 Markdown 보고서 생성
- 공개 데이터 기반 포트폴리오의 안전한 설명 범위
- 테스트로 데이터 검증, 정규화, 평가, 보고서 생성을 확인하는 흐름

## 하지 않는 것

이 프로젝트는 아래 내용을 주장하지 않습니다.

- 은행 또는 금융사의 실제 인공지능 서비스
- 금융 자문 또는 투자 권유
- 실제 고객 상담 데이터 사용
- 금융기관 내부 데이터 사용
- 특정 회사 운영 모델 평가
- 실제 모델 개선 또는 운영 지표 개선

기본 데모와 테스트는 네트워크와 API 키 없이 실행됩니다.

## 기술 구성

- Python 3 표준 라이브러리
- `unittest`
- `make`
- GitHub Actions 기반 데모와 테스트 검증
- Markdown 보고서

## 프로젝트 구조

```text
.github/workflows/       데모와 테스트 검증용 CI
data/raw/                 공개 출처 요약과 응답 후보
data/processed/           정규화된 평가 케이스
financial_ai_qa/          데이터 검증, 정규화, 평가, 보고서 생성 코드
reports/sample_report.md  생성되는 샘플 점검 보고서
docs/owner_guide.md       프로젝트를 끝까지 설명하기 위한 한국어 가이드
docs/interview_notes.md   면접에서 가능한 표현과 금지 표현
docs/user_qa_report.md    실제 사용자 관점 로컬 점검 메모
```

## 주요 명령

```bash
make verify              # clean -> demo -> test
make demo                # 정규화, 응답 평가, 보고서 생성
make normalize           # 공개 출처 기반 레코드 정규화
make evaluate            # 응답 후보 평가
make report              # Markdown 보고서 생성
make test                # unittest 실행
make clean               # 생성 산출물 삭제
```

생성되는 주요 산출물은 아래와 같습니다.

- `data/processed/evaluation_cases.json`
- `reports/sample_report.md`

## 데이터 출처와 경계

기본 데모는 공개 페이지와 공개 데이터 포털에서 정리한 작은 샘플을 사용합니다. 실시간 API 호출은 필요하지 않고, API 키도 커밋되어 있지 않습니다.

출처 목록과 자격 증명 규칙은 `data_sources.md`를 참고하세요.

## 검증 기준

기본 검증 경로는 로컬에서 결정적으로 재현됩니다.

```bash
make verify
```

마지막 로컬 확인: 2026-05-27 KST.

검증 시 확인하는 내용은 다음과 같습니다.

- 공개 자료 레코드 검증
- 평가 케이스 정규화
- 응답 후보 평가
- 실패 유형 집계
- 샘플 보고서 생성
- 테스트와 공개 주장 안전성 점검

## 리뷰용 문서

- `docs/owner_guide.md`: 프로젝트를 끝까지 직접 설명하기 위한 한국어 가이드
- `docs/interview_notes.md`: 면접에서 가능한 표현과 금지 표현
- `docs/user_qa_report.md`: 로컬 사용자 점검 메모
- `reports/sample_report.md`: 검토자가 바로 볼 수 있는 샘플 보고서

## 면접에서의 안전한 설명

> 공개 금융 원문과 공개 Q&A를 기준으로 인공지능 응답 후보를 평가한 개인 포트폴리오입니다. 응답 품질을 정확성, 완성도, 시점 표시, 자연스러움, 안전성, 출처 추적성으로 나누고 실패 유형과 보고서로 남겼습니다.

이 표현을 넘어서 금융 자문, 고객 데이터 분석, 특정 회사 운영 모델 평가를 수행했다고 말하지 않습니다.

## 배포 여부

이 프로젝트는 CLI와 보고서 중심의 포트폴리오입니다. 별도 서버나 배포 환경은 필요하지 않습니다. GitHub 저장소와 생성 보고서가 주요 리뷰 표면입니다.

## 라이선스

MIT License. `LICENSE` 파일을 참고하세요.
