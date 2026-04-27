#!/bin/bash
set -e

echo "=== Running Database Initialization ==="
python scripts/init_db.py

echo "=== Starting Bot ==="
python -m app.main
