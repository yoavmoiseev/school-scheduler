import os
import sys

# Adjust this path if you place the repo elsewhere on PythonAnywhere
project_home = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Load .env if present (simple KEY=VALUE parser)
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

# Ensure environment variables for production
os.environ.setdefault('FLASK_ENV', 'production')

# Import the Flask WSGI application
from app import app as application
