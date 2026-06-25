#!/usr/bin/env bash
# run_tests.sh — run the full test suite with coverage
set -e

echo "=== Installing test dependencies ==="
pip install -r requirements.txt -r requirements-web.txt --quiet

echo ""
echo "=== Running tests ==="
python -m pytest tests/ \
  -v \
  --tb=short \
  --cov=src \
  --cov-report=term-missing \
  --cov-report=html:htmlcov \
  "$@"

echo ""
echo "=== Coverage report written to htmlcov/index.html ==="
