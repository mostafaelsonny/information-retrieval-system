.PHONY: install test run status clean

install:
	pip install -r requirements.txt

test:
	pytest tests/

run:
	python src/main.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache
