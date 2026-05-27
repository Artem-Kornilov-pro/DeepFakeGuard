.PHONY: install install-dev lint format test test-cov clean docker-up docker-down

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pre-commit install

format:
	black src/ tests/ desktop/
	isort src/ tests/ desktop/

lint:
	black --check src/ tests/ desktop/
	isort --check src/ tests/ desktop/
	ruff check src/ tests/ desktop/
	mypy src/

test:
	pytest

test-cov:
	pytest --cov=src --cov-report=term-missing

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache .coverage htmlcov

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down -v