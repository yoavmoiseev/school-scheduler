from flask import Blueprint, request, jsonify

schedules_bp = Blueprint('schedules', __name__)

# Will be initialized by app.py
excel_service = None
autofill_service = None


def init_routes(excel_svc, autofill_svc):
    global excel_service, autofill_service
    excel_service = excel_svc
    autofill_service = autofill_svc


@schedules_bp.route('/api/schedules/group/<group_name>', methods=['GET'])
def get_group_schedule(group_name):
    """Get schedule for a specific group"""
    schedules = excel_service.get_group_schedules()
    schedule = schedules.get(group_name, {})
    return jsonify(schedule)


@schedules_bp.route('/api/schedules/teacher/<teacher_name>', methods=['GET'])
def get_teacher_schedule(teacher_name):
    """Get schedule for a specific teacher"""
    schedules = excel_service.get_teacher_schedules()
    schedule = schedules.get(teacher_name, {})
    return jsonify(schedule)


@schedules_bp.route('/api/schedules/group/<group_name>', methods=['POST'])
def save_group_schedule(group_name):
    """Save schedule for a specific group"""
    schedule = request.json
    excel_service.save_group_schedule(group_name, schedule)
    excel_service.rebuild_teacher_schedules()
    return jsonify({'success': True})


@schedules_bp.route('/api/schedules/group/<group_name>/lesson', methods=['POST'])
def add_lesson(group_name):
    """Add or update a single lesson in group schedule"""
    data = request.json
    day = data.get('day')
    lesson = data.get('lesson')
    lesson_data = data.get('lesson_data')
    
    if not all([day, lesson, lesson_data]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Get current schedule
    schedules = excel_service.get_group_schedules()
    schedule = schedules.get(group_name, {})
    
    # Add lesson
    if day not in schedule:
        schedule[day] = {}
    schedule[day][int(lesson)] = lesson_data
    
    # Save
    excel_service.save_group_schedule(group_name, schedule)
    excel_service.rebuild_teacher_schedules()
    
    return jsonify({'success': True})


@schedules_bp.route('/api/schedules/group/<group_name>/lesson', methods=['DELETE'])
def delete_lesson(group_name):
    """Delete a single lesson from group schedule"""
    data = request.json
    day = data.get('day')
    lesson = data.get('lesson')
    
    if not all([day, lesson]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Get current schedule
    schedules = excel_service.get_group_schedules()
    schedule = schedules.get(group_name, {})
    
    # Remove lesson
    if day in schedule and int(lesson) in schedule[day]:
        del schedule[day][int(lesson)]
    
    # Save
    excel_service.save_group_schedule(group_name, schedule)
    excel_service.rebuild_teacher_schedules()
    
    return jsonify({'success': True})


@schedules_bp.route('/api/schedules/autofill', methods=['POST'])
def autofill_schedule():
    """Autofill schedule for a group"""
    data = request.json
    group_name = data.get('group')
    
    if not group_name:
        return jsonify({'error': 'Group name required'}), 400
    
    # Get max retries from config
    config = excel_service.get_config()
    max_retries = int(config.get('max_autofill_retries', 100))
    
    # Run autofill
    success, schedule, info = autofill_service.autofill_group(group_name, max_retries)
    
    # ALWAYS save the schedule, even if not all lessons were placed
    # This allows viewing partial results and manual completion
    if schedule and any(schedule.values()):  # If any day has lessons
        excel_service.save_group_schedule(group_name, schedule)
        excel_service.rebuild_teacher_schedules()
    
    return jsonify({
        'success': success,
        'schedule': schedule,
        'errors': info.get('errors', []) if isinstance(info, dict) else (info or []),
        'incomplete': info.get('incomplete', []) if isinstance(info, dict) else []
    })


@schedules_bp.route('/api/schedules/clear', methods=['POST'])
def clear_all_schedules():
    """Clear all schedules"""
    excel_service.clear_all_schedules()
    return jsonify({'success': True})


@schedules_bp.route('/api/schedules/export-pdf', methods=['POST'])
def export_pdf():
    """Export schedule to PDF"""
    data = request.json
    group_name = data.get('group')
    teacher_name = data.get('teacher')
    
    config = excel_service.get_config()
    
    if group_name:
        schedules = excel_service.get_group_schedules()
        schedule = schedules.get(group_name, {})
        title = f"Schedule - {group_name}"
        filename = f"schedule_{group_name}.pdf"
    elif teacher_name:
        schedules = excel_service.get_teacher_schedules()
        schedule = schedules.get(teacher_name, {})
        title = f"Schedule - {teacher_name}"
        filename = f"schedule_{teacher_name}.pdf"
    else:
        return jsonify({'error': 'Group or teacher name required'}), 400
    
    # Generate PDF
    import os
    output_path = os.path.join('uploads', filename)
    os.makedirs('uploads', exist_ok=True)
    
    pdf_service.export_schedule(schedule, config, title, output_path)
    
    return jsonify({
        'success': True,
        'filename': filename,
        'path': output_path
    })


@schedules_bp.route('/api/schedules/all-groups', methods=['GET'])
def get_all_group_schedules():
    """Get all group schedules"""
    schedules = excel_service.get_group_schedules()
    return jsonify(schedules)


@schedules_bp.route('/api/schedules/all-teachers', methods=['GET'])
def get_all_teacher_schedules():
    """Get all teacher schedules"""
    schedules = excel_service.get_teacher_schedules()
    return jsonify(schedules)
