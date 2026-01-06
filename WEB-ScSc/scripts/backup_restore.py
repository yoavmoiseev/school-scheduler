#!/usr/bin/env python3
"""Simple backup/restore helper for the project.

Usage:
  - Local backup: python scripts/backup_restore.py backup
  - Local restore: python scripts/backup_restore.py restore <zip-file>
  - Use API backup: python scripts/backup_restore.py api-backup --url http://localhost:5000
  - Use API restore: python scripts/backup_restore.py api-restore --url http://localhost:5000 --name backup_2025-11-04_17-01-50

The script zips the `data/` and `uploads/` folders by default.
"""
import argparse
import datetime
import os
import shutil
import sys
import zipfile


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT, 'data')
UPLOADS_DIR = os.path.join(ROOT, 'uploads')
BACKUPS_DIR = os.path.join(ROOT, 'backups')


def ensure_backups_dir():
    os.makedirs(BACKUPS_DIR, exist_ok=True)


def make_local_backup():
    ensure_backups_dir()
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    fname = os.path.join(BACKUPS_DIR, f'backup_{ts}.zip')
    with zipfile.ZipFile(fname, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for base in (DATA_DIR, UPLOADS_DIR):
            if os.path.isdir(base):
                for root, dirs, files in os.walk(base):
                    for f in files:
                        full = os.path.join(root, f)
                        arcname = os.path.relpath(full, ROOT)
                        z.write(full, arcname)
    print('Created backup:', fname)


def list_local_backups():
    ensure_backups_dir()
    items = [f for f in os.listdir(BACKUPS_DIR) if f.endswith('.zip')]
    items.sort()
    for it in items:
        print(it)


def restore_local(zip_path):
    if not os.path.isfile(zip_path):
        print('Zip file not found:', zip_path)
        sys.exit(1)
    tmpdir = os.path.join(BACKUPS_DIR, '__tmp_restore')
    if os.path.exists(tmpdir):
        shutil.rmtree(tmpdir)
    os.makedirs(tmpdir)
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(tmpdir)
    # Copy extracted files back to project
    for top in ('data', 'uploads'):
        src = os.path.join(tmpdir, top)
        dst = os.path.join(ROOT, top)
        if os.path.isdir(src):
            if os.path.exists(dst):
                backup_old = dst + '.bak'
                if os.path.exists(backup_old):
                    shutil.rmtree(backup_old)
                shutil.move(dst, backup_old)
            shutil.move(src, dst)
    shutil.rmtree(tmpdir)
    print('Restore completed from', zip_path)


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest='cmd')

    sub.add_parser('backup')
    sub.add_parser('list')
    r = sub.add_parser('restore')
    r.add_argument('zip')

    # API modes (optional)
    api_b = sub.add_parser('api-backup')
    api_b.add_argument('--url', required=True)
    api_r = sub.add_parser('api-restore')
    api_r.add_argument('--url', required=True)
    api_r.add_argument('--name', required=True)

    args = p.parse_args()
    if args.cmd == 'backup':
        make_local_backup()
    elif args.cmd == 'list':
        list_local_backups()
    elif args.cmd == 'restore':
        restore_local(args.zip)
    elif args.cmd == 'api-backup':
        import requests
        resp = requests.post(args.url.rstrip('/') + '/api/admin/backup')
        print(resp.status_code, resp.text)
    elif args.cmd == 'api-restore':
        import requests
        resp = requests.post(args.url.rstrip('/') + '/api/admin/restore', json={'backup': args.name})
        print(resp.status_code, resp.text)
    else:
        p.print_help()


if __name__ == '__main__':
    main()
