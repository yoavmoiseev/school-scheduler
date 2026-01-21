from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename

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
    
    if not filename:
        return jsonify({
            'success': False,
            'error': 'Filename is required'
        }), 400
    
    # Check if file exists in ExcelExamples folder
    file_path = os.path.join('ExcelExamples', filename)
    
    if not os.path.exists(file_path):
        return jsonify({
            'success': False,
            'error': f'File not found: {filename}'
        }), 404
    
    # Import data
    result = import_service.import_from_file(file_path)
    
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

    # Save to temporary uploads folder
    tmp_dir = os.path.join('uploads', 'tmp')
    os.makedirs(tmp_dir, exist_ok=True)
    # Preserve extension for non-ASCII filenames (Hebrew, Russian, etc.)
    _, ext = os.path.splitext(f.filename)
    filename = secure_filename(f.filename)
    if not filename.endswith(ext):
        filename = filename + ext
    save_path = os.path.join(tmp_dir, filename)
    try:
        f.save(save_path)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

    # Call import service
    try:
        result = import_service.import_from_file(save_path)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

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
