from flask import Blueprint, request, jsonify

subjects_bp = Blueprint('subjects', __name__)

# Will be initialized by app.py
excel_service = None


def init_routes(excel_svc):
    global excel_service
    excel_service = excel_svc


@subjects_bp.route('/api/subjects', methods=['GET'])
def get_subjects():
    """List all subjects"""
    subjects = excel_service.get_subjects()
    return jsonify(subjects)


@subjects_bp.route('/api/subjects/<name>', methods=['GET'])
def get_subject(name):
    """Get subject details"""
    subjects = excel_service.get_subjects()
    subject = next((s for s in subjects if s['name'] == name), None)
    if not subject:
        return jsonify({'error': 'Subject not found'}), 404
    return jsonify(subject)


@subjects_bp.route('/api/subjects', methods=['POST'])
def create_subject():
    """Create new subject"""
    data = request.json
    
    # Validate
    if not data.get('name'):
        return jsonify({'error': 'Name required'}), 400
    if not data.get('group'):
        return jsonify({'error': 'Group required'}), 400
    
    # Get existing subjects
    subjects = excel_service.get_subjects()
    
    # Add new subject
    subjects.append(data)
    excel_service.save_subjects(subjects)
    
    return jsonify({'success': True, 'subject': data}), 201


@subjects_bp.route('/api/subjects/<name>', methods=['PUT'])
def update_subject(name):
    """Update subject"""
    data = request.json
    subjects = excel_service.get_subjects()
    
    # Find subject
    subject_idx = next((i for i, s in enumerate(subjects) if s['name'] == name), None)
    if subject_idx is None:
        return jsonify({'error': 'Subject not found'}), 404
    
    # Update subject
    subjects[subject_idx] = data
    excel_service.save_subjects(subjects)
    # Propagate changes to Teachers sheet for matching subject entries
    try:
        excel_service.update_subject_in_teachers(name, data)
    except Exception:
        pass
    
    return jsonify({'success': True, 'subject': data})


@subjects_bp.route('/api/subjects/<name>', methods=['DELETE'])
def delete_subject(name):
    """Delete subject"""
    subjects = excel_service.get_subjects()
    
    # Find and remove subject
    subject_idx = next((i for i, s in enumerate(subjects) if s['name'] == name), None)
    if subject_idx is None:
        return jsonify({'error': 'Subject not found'}), 404
    
    subjects.pop(subject_idx)
    excel_service.save_subjects(subjects)
    # Remove subject references from Teachers sheet
    try:
        excel_service.remove_subject_from_teachers(name)
    except Exception:
        pass
    
    return jsonify({'success': True})


@subjects_bp.route('/api/subjects/<name>/move', methods=['POST'])
def move_subject(name):
    """Move subject up or down in the list"""
    data = request.json
    direction = data.get('direction', 'up')

    subjects = excel_service.get_subjects()
    subj_idx = next((i for i, s in enumerate(subjects) if s['name'] == name), None)
    if subj_idx is None:
        return jsonify({'error': 'Subject not found'}), 404

    if direction == 'up' and subj_idx > 0:
        subjects[subj_idx], subjects[subj_idx - 1] = subjects[subj_idx - 1], subjects[subj_idx]
    elif direction == 'down' and subj_idx < len(subjects) - 1:
        subjects[subj_idx], subjects[subj_idx + 1] = subjects[subj_idx + 1], subjects[subj_idx]

    excel_service.save_subjects(subjects)
    return jsonify({'success': True})
