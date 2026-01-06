from flask import Blueprint, request, jsonify, session, send_file
import os
import json
import shutil
from datetime import datetime
import uuid

favorites_bp = Blueprint('favorites', __name__)


def _user_dir():
    uid = session.get('user_id')
    if not uid:
        return None
    base = os.path.join('uploads', 'favorites', str(uid))
    os.makedirs(base, exist_ok=True)
    return base


@favorites_bp.route('/api/favorites/list', methods=['GET'])
def list_favorites():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    ud = _user_dir()
    meta_path = os.path.join(ud, 'metadata.json')
    if not os.path.exists(meta_path):
        return jsonify({'success': True, 'favorites': []})
    try:
        stat = os.stat(meta_path)
        size = stat.st_size
    except Exception:
        size = None
    try:
        with open(meta_path, 'r', encoding='utf-8') as fh:
            content = fh.read()
        try:
            data = json.loads(content) or []
        except Exception as e:
            # log parse error and return empty list
            print(f"[favorites] Failed to parse metadata.json for user {session.get('user_id')}: {e}")
            print(f"[favorites] metadata.json content preview: {content[:500]}")
            data = []
        print(f"[favorites] Returning {len(data)} favorites (metadata.json size={size}) for user {session.get('user_id')}")
    except Exception as e:
        print(f"[favorites] Failed to read metadata.json for user {session.get('user_id')}: {e}")
        data = []
    return jsonify({'success': True, 'favorites': data})


@favorites_bp.route('/api/favorites/save', methods=['POST'])
def save_favorite():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    body = request.json or {}
    name = (body.get('name') or '').strip()
    # call existing export generator (admin.export_excel) if available
    try:
        from routes.admin_routes import export_excel
        resp = export_excel()
        # resp is a Flask Response; extract json
        try:
            res_json = resp.get_json()
        except Exception:
            import json as _j
            res_json = _j.loads(resp.get_data(as_text=True))
        if not res_json or not res_json.get('success'):
            return jsonify({'success': False, 'error': 'Export failed'}), 500
        src_fname = res_json.get('filename')
    except Exception as e:
        return jsonify({'success': False, 'error': f'Export failed: {e}'}), 500

    user_dir = _user_dir()
    meta_path = os.path.join(user_dir, 'metadata.json')
    # load metadata
    try:
        if os.path.exists(meta_path):
            with open(meta_path, 'r', encoding='utf-8') as fh:
                meta = json.load(fh) or []
        else:
            meta = []
    except Exception:
        meta = []

    if len(meta) >= 10:
        # inform client to delete one first
        # cleanup temporary export file
        try:
            os.remove(os.path.join('uploads', src_fname))
        except Exception:
            pass
        return jsonify({'success': False, 'error': 'max_favorites_reached', 'message': 'Maximum 10 favorites reached. Delete one before saving.'}), 400

    # build filename and move file
    if not name:
        name = f"Favorite {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    safe_id = str(uuid.uuid4())
    dest_fname = f"fav_{session.get('username','user')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_id}.xlsx"
    try:
        shutil.move(os.path.join('uploads', src_fname), os.path.join(user_dir, dest_fname))
    except Exception as e:
        return jsonify({'success': False, 'error': f'File move failed: {e}'}), 500

    entry = {
        'id': safe_id,
        'name': name,
        'filename': dest_fname,
        'created_at': datetime.now().isoformat()
    }
    meta.append(entry)
    try:
        with open(meta_path, 'w', encoding='utf-8') as fh:
            json.dump(meta, fh, ensure_ascii=False, indent=2)
    except Exception as e:
        return jsonify({'success': False, 'error': f'Failed to save metadata: {e}'}), 500

    return jsonify({'success': True, 'favorite': entry})


@favorites_bp.route('/api/favorites/download/<fav_id>', methods=['GET'])
def download_favorite(fav_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    ud = _user_dir()
    meta_path = os.path.join(ud, 'metadata.json')
    if not os.path.exists(meta_path):
        return jsonify({'success': False, 'error': 'Not found'}), 404
    try:
        with open(meta_path, 'r', encoding='utf-8') as fh:
            meta = json.load(fh) or []
    except Exception:
        meta = []
    item = next((m for m in meta if m.get('id') == fav_id), None)
    if not item:
        return jsonify({'success': False, 'error': 'Favorite not found'}), 404
    fpath = os.path.join(ud, item.get('filename'))
    if not os.path.exists(fpath):
        return jsonify({'success': False, 'error': 'File not found'}), 404
    return send_file(fpath, as_attachment=True)


@favorites_bp.route('/api/favorites/delete', methods=['POST'])
def delete_favorite():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    body = request.json or {}
    fid = body.get('id')
    if not fid:
        return jsonify({'success': False, 'error': 'id required'}), 400
    ud = _user_dir()
    meta_path = os.path.join(ud, 'metadata.json')
    try:
        with open(meta_path, 'r', encoding='utf-8') as fh:
            meta = json.load(fh) or []
    except Exception:
        meta = []
    item = next((m for m in meta if m.get('id') == fid), None)
    if not item:
        return jsonify({'success': False, 'error': 'Favorite not found'}), 404
    try:
        fpath = os.path.join(ud, item.get('filename'))
        if os.path.exists(fpath):
            os.remove(fpath)
    except Exception:
        pass
    meta = [m for m in meta if m.get('id') != fid]
    try:
        with open(meta_path, 'w', encoding='utf-8') as fh:
            json.dump(meta, fh, ensure_ascii=False, indent=2)
    except Exception as e:
        return jsonify({'success': False, 'error': f'Failed to update metadata: {e}'}), 500
    return jsonify({'success': True})


@favorites_bp.route('/api/favorites/rename', methods=['POST'])
def rename_favorite():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    body = request.json or {}
    fid = body.get('id')
    new_name = (body.get('name') or '').strip()
    if not fid or not new_name:
        return jsonify({'success': False, 'error': 'id and name required'}), 400
    ud = _user_dir()
    meta_path = os.path.join(ud, 'metadata.json')
    try:
        with open(meta_path, 'r', encoding='utf-8') as fh:
            meta = json.load(fh) or []
    except Exception:
        meta = []
    changed = False
    for m in meta:
        if m.get('id') == fid:
            m['name'] = new_name
            changed = True
            break
    if not changed:
        return jsonify({'success': False, 'error': 'Favorite not found'}), 404
    try:
        with open(meta_path, 'w', encoding='utf-8') as fh:
            json.dump(meta, fh, ensure_ascii=False, indent=2)
    except Exception as e:
        return jsonify({'success': False, 'error': f'Failed to update metadata: {e}'}), 500
    return jsonify({'success': True})
