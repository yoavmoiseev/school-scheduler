#!/usr/bin/env bash
# Helper script to create a virtualenv and install dependencies (UNIX/PythonAnywhere)
set -e

VENV_DIR="${1:-~/venv-school-scheduler}"
PROJECT_DIR="${2:-$(pwd)}"

echo "Creating virtualenv at $VENV_DIR"
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"
pip install -U pip
pip install -r "$PROJECT_DIR/requirements.txt"

echo "Virtualenv ready. Activate with: source $VENV_DIR/bin/activate"
