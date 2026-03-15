from flask import Blueprint, request, jsonify

schedules_bp = Blueprint('schedules', __name__)

# Will be initialized by app.py
excel_service = None
autofill_service = None


def init_routes(excel_svc, autofill_svc):
    global excel_service, autofill_service
    excel_service = excel_svc
    autofill_service = autofill_svc


@schedules_bp.route('/api/schedules/group/<path:group_name>', methods=['GET'])
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


@schedules_bp.route('/api/schedules/group/<path:group_name>', methods=['POST'])
def save_group_schedule(group_name):
    """Save schedule for a specific group"""
    schedule = request.json
    excel_service.save_group_schedule(group_name, schedule)
    excel_service.rebuild_teacher_schedules()
    return jsonify({'success': True})


@schedules_bp.route('/api/schedules/group/<path:group_name>/lesson', methods=['POST'])
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


@schedules_bp.route('/api/schedules/group/<path:group_name>/lesson', methods=['DELETE'])
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

    # ── Pre-step: handle united groups ──────────────────────────────────────
    # Find all united groups that contain this group as a sub-group.
    # For each such united group, ensure its schedule is built and force-inserted
    # into this group's slots BEFORE autofill runs — exactly like Rebuild All does.
    all_groups = excel_service.get_groups()
    groups_map = {g['name']: g for g in all_groups if isinstance(g, dict) and g.get('name')}
    united_parents = [
        g for g in all_groups
        if isinstance(g, dict) and g.get('is_united') and group_name in (g.get('sub_groups') or [])
    ]
    united_issues = []  # collect incomplete placements from united parent groups
    if united_parents:
        for united_group in united_parents:
            united_name = united_group['name']
            # Check if united group already has a saved schedule
            existing_schedules = excel_service.get_group_schedules()
            united_schedule = existing_schedules.get(united_name, {})
            # Always run autofill for the united group so any incomplete placements
            # are caught and reported — even if a partial schedule already exists.
            # Use preserve_existing=True if a schedule exists (fill gaps only),
            # preserve_existing=False if starting from scratch.
            preserve_u = bool(united_schedule and any(united_schedule.values()))
            try:
                u_success, u_schedule, u_info = autofill_service.autofill_group(
                    united_name, max_retries=max_retries, preserve_existing=preserve_u
                )
                if u_schedule and any(u_schedule.values()):
                    excel_service.save_group_schedule(united_name, u_schedule)
                    excel_service.rebuild_teacher_schedules()
                    united_schedule = u_schedule
                # Always capture incomplete placements (regardless of success flag)
                if not u_success and isinstance(u_info, dict):
                    for item in (u_info.get('incomplete') or []):
                        united_issues.append(dict(item, united_group=united_name))
                    for err in (u_info.get('errors') or []):
                        united_issues.append({'united_group': united_name, 'error': err})
            except Exception as e:
                united_issues.append({'united_group': united_name, 'error': str(e)})
            # Force-insert united group's lessons into this sub-group's slots
            if united_schedule and any(united_schedule.values()):
                excel_service.force_merge_into_group_schedule(group_name, united_schedule)
        excel_service.rebuild_teacher_schedules()
    # ────────────────────────────────────────────────────────────────────────

    # Run autofill
    success, schedule, info = autofill_service.autofill_group(group_name, max_retries)
    
    # ALWAYS save the schedule, even if not all lessons were placed
    # This allows viewing partial results and manual completion
    if schedule and any(schedule.values()):  # If any day has lessons
        excel_service.save_group_schedule(group_name, schedule)
        excel_service.rebuild_teacher_schedules()

        # If this is a united group, propagate its lessons to each sub-group's schedule
        groups = excel_service.get_groups()
        group_obj = next((g for g in groups if g['name'] == group_name), None)
        if group_obj and group_obj.get('is_united') and group_obj.get('sub_groups'):
            for sub_group_name in group_obj['sub_groups']:
                excel_service.merge_into_group_schedule(sub_group_name, schedule)
            # Rebuild teacher schedules again after sub-group updates
            excel_service.rebuild_teacher_schedules()

    return jsonify({
        'success': success,
        'schedule': schedule,
        'errors': info.get('errors', []) if isinstance(info, dict) else (info or []),
        'incomplete': info.get('incomplete', []) if isinstance(info, dict) else [],
        'united_issues': united_issues
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
