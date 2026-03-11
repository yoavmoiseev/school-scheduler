from flask import Blueprint, request, jsonify
import os
import logging
from werkzeug.utils import secure_filename

# ─── Import routes debug logger ─────────────────────────────────────────────────
_rlog = logging.getLogger('import_routes_debug')
if not _rlog.handlers:
    _rh = logging.FileHandler('import_debug.log', encoding='utf-8')
    _rh.setFormatter(logging.Formatter('%(asctime)s  %(levelname)s  %(message)s'))
    _rlog.addHandler(_rh)
    _rlog.setLevel(logging.DEBUG)
# ────────────────────────────────────────────────────────────────────────────────

import_bp = Blueprint('import', __name__)

# Will be initialized by app.py
import_service = None


def init_routes(import_svc):
    global import_service
    import_service = import_svc


@import_bp.route('/api/import/from-file', methods=['POST'])
def import_from_file():
    """Import data from external Excel file"""
    data = request.json
    filename = data.get('filename')
    _rlog.info(f'[/api/import/from-file] REQUEST filename={filename!r}')
    
    if not filename:
        return jsonify({
            'success': False,
            'error': 'Filename is required'
        }), 400
    
    # Check if file exists in ExcelExamples folder
    file_path = os.path.join('ExcelExamples', filename)
    _rlog.info(f'[/api/import/from-file] file_path={file_path!r}  exists={os.path.exists(file_path)}')
    
    if not os.path.exists(file_path):
        _rlog.error(f'[/api/import/from-file] File not found: {file_path!r}')
        return jsonify({
            'success': False,
            'error': f'File not found: {filename}'
        }), 404
    
    # Import data
    _rlog.info(f'[/api/import/from-file] calling import_service.import_from_file...')
    result = import_service.import_from_file(file_path)
    _rlog.info(f'[/api/import/from-file] RESULT: {result}')
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 500


@import_bp.route('/api/import/upload', methods=['POST'])
def import_upload():
    """Upload an Excel file (multipart/form-data) and import it."""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'}), 400

    f = request.files.get('file')
    if not f or f.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'}), 400

    _rlog.info(f'[/api/import/upload] original filename={f.filename!r}')

    # Save to temporary uploads folder
    tmp_dir = os.path.join('uploads', 'tmp')
    os.makedirs(tmp_dir, exist_ok=True)
    # Preserve extension for non-ASCII filenames (Hebrew, Russian, etc.)
    _, ext = os.path.splitext(f.filename)
    filename = secure_filename(f.filename)
    if not filename.endswith(ext):
        filename = filename + ext
    save_path = os.path.join(tmp_dir, filename)
    _rlog.info(f'[/api/import/upload] saving to={save_path!r}')
    try:
        f.save(save_path)
        _rlog.info(f'[/api/import/upload] file saved, size={os.path.getsize(save_path)} bytes')
    except Exception as e:
        _rlog.error(f'[/api/import/upload] save failed: {e}')
        return jsonify({'success': False, 'error': str(e)}), 500

    # Call import service
    _rlog.info(f'[/api/import/upload] calling import_service.import_from_file...')
    try:
        result = import_service.import_from_file(save_path)
    except Exception as e:
        _rlog.error(f'[/api/import/upload] import_from_file raised exception: {e}')
        return jsonify({'success': False, 'error': str(e)}), 500

    _rlog.info(f'[/api/import/upload] RESULT: {result}')
    return jsonify(result), (200 if result.get('success') else 500)


@import_bp.route('/api/import/list-files', methods=['GET'])
def list_import_files():
    """List available Excel files in ExcelExamples folder"""
    try:
        excel_dir = 'ExcelExamples'
        if not os.path.exists(excel_dir):
            return jsonify({
                'success': True,
                'files': []
            })
        
        files = []
        for filename in os.listdir(excel_dir):
            if filename.endswith(('.xlsx', '.xls')):
                file_path = os.path.join(excel_dir, filename)
                file_size = os.path.getsize(file_path)
                files.append({
                    'name': filename,
                    'size': file_size,
                    'path': file_path
                })
        
        return jsonify({
            'success': True,
            'files': files
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
