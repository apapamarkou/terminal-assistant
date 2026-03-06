.PHONY: install test clean check help

help:
	@echo "Terminal Assistant - Development Commands"
	@echo ""
	@echo "  make install    Install package in development mode"
	@echo "  make test       Run tests"
	@echo "  make check      Run setup verification"
	@echo "  make clean      Remove build artifacts"
	@echo "  make help       Show this help message"

install:
	pip install -e ".[dev]"

test:
	pytest

check:
	python setup_check.py

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
