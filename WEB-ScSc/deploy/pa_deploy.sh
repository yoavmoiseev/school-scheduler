#!/usr/bin/env bash
set -euo pipefail

# PythonAnywhere automatic deploy script
# Intended to be run inside PythonAnywhere Bash console after cloning the repo.

REPO_DIR="$PWD"
VENV_DIR="$HOME/venv-school-scheduler"
PYTHON_BIN="python3.11"

echo "Auto-deploy script starting in: $REPO_DIR"

if [ ! -f "$REPO_DIR/requirements.txt" ]; then
  echo "requirements.txt not found in $REPO_DIR. Aborting." >&2
  exit 1
fi

echo "Creating virtualenv at $VENV_DIR (if missing)"
if [ ! -d "$VENV_DIR" ]; then
  $PYTHON_BIN -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"
pip install -U pip
pip install -r "$REPO_DIR/requirements.txt"

echo "Ensuring folders exist"
mkdir -p "$REPO_DIR/uploads" "$REPO_DIR/data"

# Create .env with SECRET_KEY if not present
ENV_FILE="$REPO_DIR/.env"
if [ -f "$ENV_FILE" ]; then
  echo ".env already exists; leaving unchanged." 
else
  echo "Generating SECRET_KEY and writing .env"
  SECRET_KEY=$(python - <<'PY'
import secrets
print(secrets.token_urlsafe(48))
PY
)
  cat > "$ENV_FILE" <<EOF
SECRET_KEY=${SECRET_KEY}
FLASK_ENV=production
EOF
  echo ".env created at $ENV_FILE"
fi

# Write the WSGI helper file into the project (so user can copy into PythonAnywhere WSGI editor)
WSGI_TARGET="$REPO_DIR/pythonanywhere_wsgi.py"
cat > "$WSGI_TARGET" <<'PYW'
import os
import sys
project_home = os.path.abspath(os.path.dirname(__file__))
if project_home not in sys.path:
    sys.path.insert(0, project_home)
# Load .env
env_path = os.path.join(project_home, '.env')
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k and v and k not in os.environ:
                os.environ[k] = v
os.environ.setdefault('FLASK_ENV', 'production')
from app import app as application
PYW

echo "WSGI helper written to $WSGI_TARGET"

echo "Done. Next steps (one-time, in the PythonAnywhere Web tab):"
echo "1) Go to the Web tab → Source code: set to $REPO_DIR if not already."
echo "2) In the WSGI configuration editor, replace contents with the contents of $WSGI_TARGET (open file and paste)."
echo "3) Set Virtualenv to: $VENV_DIR"
echo "4) Click 'Reload' in the Web tab."

echo "If you need me to set the Web tab values via API, you can create an API token in Account -> API token and provide it securely."

echo "Auto-deploy script finished. Access logs in the Web tab if the app fails to start."
