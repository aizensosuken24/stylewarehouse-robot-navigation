#!/bin/bash
# run_tests.sh — Run the full test suite
echo "================================================"
echo "  StyleWarehouse Robot Navigation — Test Suite"
echo "================================================"
python -m pytest tests/ -v --tb=short
