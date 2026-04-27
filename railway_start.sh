#!/bin/bash
set -e

echo "=== Running Database Initialization ==="
python scripts/init_db.py

echo "=== Starting Health Check Server ==="
python scripts/health_server.py &

echo "=== Starting Bot ==="
python -m app.main

