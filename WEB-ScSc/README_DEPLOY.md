# Deployment Guide

This document explains two simple deployment paths for the School Scheduler app: PythonAnywhere (very easy) and Railway (CI/CD). Follow the steps below to publish your app.

## Common prep

1. Ensure your repo contains `requirements.txt` and `app.py` at root.
2. Add sensitive values to environment variables (do NOT commit `.env`):
   - `SECRET_KEY` (random string)
   - `DEBUG=False`

## Option A — PythonAnywhere (fast, very simple)

1. Create a free account at https://www.pythonanywhere.com
2. In Dashboard → Files, push your project files or clone your GitHub repo.
3. Go to Web → Add a new web app → Manual configuration → Flask.
4. Set the path to your project and WSGI entry to `app:app` (adjust if different).
5. In the "Virtualenv" section, create/point to a virtualenv and install dependencies:
   ```bash
   pip install -r /path/to/requirements.txt
   ```
6. In the "Environment variables" section set `SECRET_KEY` and `DEBUG=False`.
7. Reload the web app.

Pros: easiest for a first-time deployment. Cons: limited free resources.

## Option B — Railway (better for CI/CD)

1. Create a GitHub repo for your project and push code (see commands below).
2. Sign up at https://railway.app and create a new project → Deploy from GitHub.
3. Connect your repo and configure build. Railway detects Python apps automatically.
4. Add environment variables in Project Settings → Variables: `SECRET_KEY`, `DEBUG=False`.
5. If needed add a `Procfile` with:
   ```text
   web: gunicorn app:app --bind 0.0.0.0:$PORT
   ```
6. Deploy; Railway will provide a public URL.

Pros: automated deploys on push, easy to scale. Cons: free tier limited.

## Git commands to push your project (run locally)

```bash
# initialize (if not already a git repo)
git init
git add .
git commit -m "Initial commit"
# create repo on GitHub manually, then add remote
git remote add origin https://github.com/<your-username>/<repo-name>.git
git branch -M main
git push -u origin main
```

## After deploy

- Restart app on the host if required.
- Hard-refresh browser (Ctrl+F5) to pick up client-side changes.

