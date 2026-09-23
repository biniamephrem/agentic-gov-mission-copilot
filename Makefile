.PHONY: install run test eval

install:
	python -m pip install -r requirements.txt

run:
	uvicorn app.main:app --reload

test:
	pytest -q

eval:
	python evals/run_eval.py
