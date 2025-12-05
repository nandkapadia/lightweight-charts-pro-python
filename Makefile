.PHONY: help install install-dev install-docs test lint format type-check clean build publish docs

help:
	@echo "Lightweight Charts Pro Python - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install          - Install package"
	@echo "  make install-dev      - Install package with dev dependencies"
	@echo "  make install-docs     - Install documentation dependencies"
	@echo "  make pre-commit       - Install pre-commit hooks"
	@echo ""
	@echo "Testing:"
	@echo "  make test             - Run tests"
	@echo "  make test-cov         - Run tests with coverage"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint             - Run linters"
	@echo "  make format           - Format code with black and isort"
	@echo "  make type-check       - Run type checking with mypy"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs             - Build HTML documentation"
	@echo "  make docs-live        - Build docs with auto-reload"
	@echo "  make docs-check       - Validate documentation"
	@echo ""
	@echo "Build & Release:"
	@echo "  make clean            - Remove build artifacts"
	@echo "  make build            - Build distribution packages"
	@echo "  make publish          - Publish to PyPI"
	@echo "  make publish-test     - Publish to Test PyPI"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev,test]"
	pre-commit install
	pre-commit install --hook-type commit-msg

install-docs:
	pip install -r docs/requirements.txt

pre-commit:
	pre-commit install
	pre-commit install --hook-type commit-msg
	@echo "✅ Pre-commit hooks installed!"

test:
	pytest tests/ -v --tb=short

test-cov:
	pytest --cov=lightweight_charts_pro --cov-report=html --cov-report=term-missing

lint:
	ruff check lightweight_charts_pro
	pylint lightweight_charts_pro

format:
	black lightweight_charts_pro tests
	isort lightweight_charts_pro tests

type-check:
	mypy lightweight_charts_pro --ignore-missing-imports

# Documentation targets
docs:
	cd docs && make html
	@echo "✅ Documentation built! Open docs/build/html/index.html"

docs-live:
	cd docs && make livehtml

docs-clean:
	cd docs && make clean

docs-check:
	cd docs && make strict
	cd docs && make linkcheck
	cd docs && make coverage
	@echo "✅ Documentation validation complete!"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

build: clean
	python -m build

publish: build
	python -m twine upload dist/*

publish-test: build
	python -m twine upload --repository testpypi dist/*
