#!/bin/bash

set -e

echo "======================================"
echo "Update Project - Setup & Run"
echo "======================================"

# Install requirements
echo "[*] Installing requirements..."
pip install -r requirements.txt

# Run Docker
echo "[*] Running Docker..."
python tables.py
python operations.py

# Run pytest
echo "[*] Running pytest..."
pytest test_operations.py -v

echo "[✓] All tasks completed!"
