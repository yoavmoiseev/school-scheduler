from flask import Blueprint, request, jsonify

teachers_bp = Blueprint('teachers', __name__)

# Will be initialized by app.py
excel_service = None


def init_routes(excel_svc):
    global excel_service
    excel_service = excel_svc


@teachers_bp.route('/api/teachers', methods=['GET'])
def get_teachers():
    """List all teachers"""
    teachers = excel_service.get_teachers()
    return jsonify(teachers)


@teachers_bp.route('/api/teachers/<name>', methods=['GET'])
def get_teacher(name):
    """Get teacher details"""
    teachers = excel_service.get_teachers()
    teacher = next((t for t in teachers if t['name'] == name), None)
    if not teacher:
        return jsonify({'error': 'Teacher not found'}), 404
    return jsonify(teacher)


@teachers_bp.route('/api/teachers', methods=['POST'])
def create_teacher():
    """Create new teacher"""
    data = request.json
    
    # Validate
    if not data.get('name'):
        return jsonify({'error': 'Name required'}), 400
    
    # Get existing teachers
    teachers = excel_service.get_teachers()
    
    # Check if already exists
    if any(t['name'] == data['name'] for t in teachers):
        return jsonify({'error': 'Teacher already exists'}), 400
    
    # Add new teacher
    teachers.append(data)
    excel_service.save_teachers(teachers)
    
    return jsonify({'success': True, 'teacher': data}), 201


@teachers_bp.route('/api/teachers/<name>', methods=['PUT'])
def update_teacher(name):
    """Update teacher"""
    data = request.json
    
    # DEBUG: Log incoming data
    print(f"\n=== UPDATE TEACHER: {name} ===")
    print(f"Incoming data: {data}")
    print(f"check_in_hours: {data.get('check_in_hours', 'NOT PROVIDED')}")
    print(f"check_out_hours: {data.get('check_out_hours', 'NOT PROVIDED')}")
    print(f"available_slots: {data.get('available_slots', 'NOT PROVIDED')}")
    
    teachers = excel_service.get_teachers()
    
    # Find teacher
    teacher_idx = next((i for i, t in enumerate(teachers) if t['name'] == name), None)
    if teacher_idx is None:
        return jsonify({'error': 'Teacher not found'}), 404
    
    # Merge with existing data to preserve fields
    existing_teacher = teachers[teacher_idx]
    
    print(f"Existing teacher before merge: {existing_teacher}")
    
    # Update only provided fields
    for key, value in data.items():
        existing_teacher[key] = value
    
    # Ensure required fields exist
    if 'check_in_hours' not in existing_teacher:
        existing_teacher['check_in_hours'] = {}
    if 'check_out_hours' not in existing_teacher:
        existing_teacher['check_out_hours'] = {}
    if 'available_slots' not in existing_teacher:
        existing_teacher['available_slots'] = {}
    
    print(f"Teacher after merge: {existing_teacher}")
    print("=" * 50 + "\n")
    
    teachers[teacher_idx] = existing_teacher
    excel_service.save_teachers(teachers)
    
    return jsonify({'success': True, 'teacher': existing_teacher})


@teachers_bp.route('/api/teachers/<name>', methods=['DELETE'])
def delete_teacher(name):
    """Delete teacher"""
    teachers = excel_service.get_teachers()
    
    # Find and remove teacher
    teacher_idx = next((i for i, t in enumerate(teachers) if t['name'] == name), None)
    if teacher_idx is None:
        return jsonify({'error': 'Teacher not found'}), 404
    
    teachers.pop(teacher_idx)
    excel_service.save_teachers(teachers)
    
    return jsonify({'success': True})


@teachers_bp.route('/api/teachers/<name>/move', methods=['POST'])
def move_teacher(name):
    """Move teacher up or down in the list"""
    data = request.json
    direction = data.get('direction', 'up')
    
    teachers = excel_service.get_teachers()
    teacher_idx = next((i for i, t in enumerate(teachers) if t['name'] == name), None)
    
    if teacher_idx is None:
        return jsonify({'error': 'Teacher not found'}), 404
    
    if direction == 'up' and teacher_idx > 0:
        teachers[teacher_idx], teachers[teacher_idx - 1] = teachers[teacher_idx - 1], teachers[teacher_idx]
    elif direction == 'down' and teacher_idx < len(teachers) - 1:
        teachers[teacher_idx], teachers[teacher_idx + 1] = teachers[teacher_idx + 1], teachers[teacher_idx]
    
    excel_service.save_teachers(teachers)
    
    return jsonify({'success': True})
