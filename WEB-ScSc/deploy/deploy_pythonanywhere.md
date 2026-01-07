# Deploying to PythonAnywhere

This document explains how to deploy the project to PythonAnywhere (free tier) without adding any payment method.

1) Create account
- Sign up at https://www.pythonanywhere.com/ (free tier).

2) Upload repository files
- Option A (recommended): Push your repo to GitHub and use PythonAnywhere's Git integration to pull inside your home directory.
- Option B: Use the PythonAnywhere Files tab to upload a zip of your project and extract it into a folder (e.g. `/home/yourusername/school-scheduler`).

3) Create a virtualenv
- Open a Bash console on PythonAnywhere and create a virtualenv (use the Python version matching your `requirements.txt`, e.g. 3.11):

```bash
python3.11 -m venv ~/venv-school-scheduler
source ~/venv-school-scheduler/bin/activate
pip install -U pip
pip install -r ~/path/to/your/project/requirements.txt
```

4) Configure the Web app
- In the PythonAnywhere dashboard go to the "Web" tab and **Add a new web app**.
- Choose "Manual configuration" and select the same Python version you used for the virtualenv.
- Set the "Source code" folder to the project directory (for example `/home/yourusername/school-scheduler`).
- Set the Virtualenv path to the venv you created above (`/home/yourusername/venv-school-scheduler`).

5) WSGI configuration
- Open the WSGI configuration file in the Web tab and replace its contents with the contents of `deploy/pythonanywhere_wsgi.py` (copy the file into the PythonAnywhere WSGI editor). The helper file expects the Flask app to be importable from `app.py` (this repository's structure).

Example (copy into PythonAnywhere WSGI editor):

```python
import os
import sys
project_home = '/home/yourusername/school-scheduler'
if project_home not in sys.path:
    sys.path.insert(0, project_home)
os.environ.setdefault('FLASK_ENV', 'production')
from app import app as application
```

6) Environment variables
- In the Web tab, under "Environment variables", add at least the following:

- `SECRET_KEY`: set to a random secure value (do not use the development default).
- Optionally set `EXCEL_FILE` if you uploaded a custom Excel file outside the repository path.

7) Upload Excel file (if needed)
- If your app uses a custom Excel workbook, upload it to the project folder using the Files tab, and update `EXCEL_FILE` environment variable to point to the file path (for example `/home/yourusername/school-scheduler/data/SchoolScheduler.xlsx`). By default the app will use `data/SchoolScheduler.xlsx` inside the project.

8) Static files and uploads
- Static files are served by Flask's `static/` folder. Uploads created at runtime will be placed in the `uploads/` folder inside the project — ensure `uploads/` is writable by your app (PythonAnywhere gives write access to your home directory).

9) Reload and test
- After configuring the WSGI file and environment variables, click "Reload" in the Web tab and open the provided web URL. Check the error log (Web tab → Error log) if the site fails to start.

10) Common troubleshooting
- If you see ImportError, check that your virtualenv has all required packages installed.
- If you get permission errors writing files, double-check folders exist and are writable (`mkdir uploads data` if missing).
- Check `error.log` and `server.log` from the Web tab for stack traces.

If you want, I can create the needed WSGI file content, a short `README` with the exact commands, and a helper shell script to set up a venv locally; tell me and I'll add those files to the repo.
