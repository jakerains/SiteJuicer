.PHONY: help clean test lint format install dev-install

help:
	@echo "Available commands:"
	@echo "  make help        - Show this help message"
	@echo "  make clean       - Remove build artifacts and cache directories"
	@echo "  make test        - Run tests"
	@echo "  make lint        - Run linting checks"
	@echo "  make format      - Format code with black and isort"
	@echo "  make install     - Install package"
	@echo "  make dev-install - Install package in development mode with all extras"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

test:
	python -m pytest tests/ -v

lint:
	flake8 .
	mypy .
	black --check .
	isort --check .

format:
	black .
	isort .

install:
	pip install .

dev-install:
	pip install -e ".[all,dev]" 