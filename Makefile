.PHONY: demo normalize evaluate report test clean

PYTHON ?= python3

demo:
	$(PYTHON) -m financial_ai_qa.cli demo

normalize:
	$(PYTHON) -m financial_ai_qa.cli normalize

evaluate:
	$(PYTHON) -m financial_ai_qa.cli evaluate

report:
	$(PYTHON) -m financial_ai_qa.cli report

test:
	$(PYTHON) -m unittest discover -s tests -v

clean:
	rm -f data/processed/evaluation_cases.json
	rm -f reports/sample_report.md
