from flask import Blueprint, request, jsonify, session

config_bp = Blueprint('config', __name__)

# Will be initialized by app.py
excel_service = None


def init_routes(excel_svc):
    global excel_service
    excel_service = excel_svc


@config_bp.route('/api/config', methods=['GET'])
def get_config():
    """Get configuration"""
    config = excel_service.get_config()
    return jsonify(config)


@config_bp.route('/api/config', methods=['POST'])
def save_config():
    """Save configuration"""
    config = request.json
    excel_service.save_config(config)
    
    # Update session language if it was changed
    if 'GUI_LANGUAGE' in config:
        session['login_language'] = config['GUI_LANGUAGE']
    
    return jsonify({'success': True})


@config_bp.route('/api/time-slots', methods=['GET'])
def get_time_slots():
    """Get all time slots"""
    time_slots = excel_service.get_time_slots()
    return jsonify(time_slots)


@config_bp.route('/api/time-slots', methods=['POST'])
def save_time_slot():
    """
    Add or update a single time slot
    Request body: { "lesson": 1, "time": "09:15-10:00" }
    """
    data = request.json
    lesson_num = data.get('lesson')
    time_range = data.get('time')
    
    if not lesson_num or not time_range:
        return jsonify({'error': 'Missing lesson or time'}), 400
    
    try:
        lesson_num = int(lesson_num)
        if lesson_num < 1 or lesson_num > 30:
            return jsonify({'error': 'Lesson number must be between 1 and 30'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid lesson number'}), 400
    
    # Get current time slots
    time_slots = excel_service.get_time_slots()
    time_slots[lesson_num] = time_range
    
    # Save back to Excel
    excel_service.save_time_slots(time_slots)
    
    return jsonify({'success': True, 'time_slots': time_slots})


@config_bp.route('/api/time-slots/<int:lesson_num>', methods=['DELETE'])
def delete_time_slot(lesson_num):
    """Delete a time slot by lesson number"""
    time_slots = excel_service.get_time_slots()
    
    if lesson_num in time_slots:
        del time_slots[lesson_num]
        excel_service.save_time_slots(time_slots)
        return jsonify({'success': True, 'time_slots': time_slots})
    else:
        return jsonify({'error': 'Time slot not found'}), 404
