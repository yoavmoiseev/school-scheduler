from flask import Blueprint, request, jsonify

groups_bp = Blueprint('groups', __name__)

# Will be initialized by app.py
excel_service = None


def init_routes(excel_svc):
    global excel_service
    excel_service = excel_svc


@groups_bp.route('/api/groups', methods=['GET'])
def get_groups():
    """List all groups"""
    groups = excel_service.get_groups()


    # Compute totals per group based on Subjects sheet:
    # total_required = sum(hours_per_week for all subjects in the group)
    # total_assigned = sum(hours_per_week for subjects in the group that have a teacher assigned)
    subjects = excel_service.get_subjects()
    teachers = excel_service.get_teachers()

    # Build a map of subject key -> hours for quick lookup
    # key: (subject_name, group_name)
    subj_hours = {}
    for s in subjects:
        key = (s.get('name'), s.get('group') or '')
        try:
            subj_hours[key] = int(s.get('hours_per_week', 0) or 0)
        except Exception:
            subj_hours[key] = 0

    # total_required per group: sum of all subject hours for that group
    req_map = {}
    for (name, grp), hours in subj_hours.items():
        req_map[grp] = req_map.get(grp, 0) + hours

    # total_assigned (unique): for each group, collect unique subject keys that are assigned to any teacher
    assigned_unique_map = {}
    # total_assigned_by_teachers: sum directly from teachers' subject entries (may reflect subgroup splits or duplicates)
    assigned_by_teachers_map = {}

    # Build set of assigned subject keys from Teachers data (teacher.subjects entries)
    assigned_keys = set()
    for t in teachers:
        for sub in t.get('subjects', []):
            key = (sub.get('name'), sub.get('group') or '')
            assigned_keys.add(key)
            # add to by-teachers sum using the hours from teacher entry (if present)
            try:
                hrs = int(sub.get('hours', 0) or 0)
            except Exception:
                hrs = 0
            grp = key[1]
            assigned_by_teachers_map[grp] = assigned_by_teachers_map.get(grp, 0) + hrs

    # Also consider subjects sheet 'teacher' column as assigned (in case assignments are stored there)
    for s in subjects:
        if s.get('teacher'):
            key = (s.get('name'), s.get('group') or '')
            assigned_keys.add(key)

    # Now compute unique assigned totals per group using subj_hours lookup
    for key in assigned_keys:
        name, grp = key
        hours = subj_hours.get(key, 0)
        assigned_unique_map[grp] = assigned_unique_map.get(grp, 0) + hours

    # Attach totals to groups
    out = []
    for g in groups:
        name = g.get('name')
        g_copy = dict(g)
        g_copy['total_required'] = req_map.get(name, 0)
        # primary: unique assigned (do not multiply for subgroups)
        g_copy['total_assigned'] = assigned_unique_map.get(name, 0)
        # secondary/diagnostic: sum from teachers' entries (may include subgroup splits)
        g_copy['total_assigned_by_teachers'] = assigned_by_teachers_map.get(name, 0)
        out.append(g_copy)

    return jsonify(out)


@groups_bp.route('/api/groups/<name>', methods=['GET'])
def get_group(name):
    """Get group details"""
    groups = excel_service.get_groups()
    group = next((g for g in groups if g['name'] == name), None)
    if not group:
        return jsonify({'error': 'Group not found'}), 404
    return jsonify(group)


@groups_bp.route('/api/groups', methods=['POST'])
def create_group():
    """Create new group"""
    data = request.json
    
    # Validate
    if not data.get('name'):
        return jsonify({'error': 'Name required'}), 400
    
    # Get existing groups
    groups = excel_service.get_groups()
    
    # Check if already exists
    if any(g['name'] == data['name'] for g in groups):
        return jsonify({'error': 'Group already exists'}), 400
    
    # Add new group
    groups.append(data)
    excel_service.save_groups(groups)
    
    return jsonify({'success': True, 'group': data}), 201


@groups_bp.route('/api/groups/<name>', methods=['PUT'])
def update_group(name):
    """Update group"""
    data = request.json
    groups = excel_service.get_groups()
    
    print(f"[DEBUG] update_group: URL name={name}, data={data}")
    
    # Find group
    group_idx = next((i for i, g in enumerate(groups) if g['name'] == name), None)
    if group_idx is None:
        print(f"[DEBUG] update_group: Group '{name}' not found in groups list")
        return jsonify({'error': 'Group not found'}), 404
    
    old_name = name
    new_name = data.get('name')
    
    print(f"[DEBUG] update_group: old_name={old_name}, new_name={new_name}")
    
    # Update group
    groups[group_idx] = data
    excel_service.save_groups(groups)
    print(f"[DEBUG] update_group: Group updated in Groups sheet")
    
    # If name changed, update references in Subjects and Teachers
    if old_name != new_name:
        print(f"[DEBUG] update_group: Name changed, updating references...")
        # Update Subjects sheet: group field
        subjects = excel_service.get_subjects()
        updated_subjects = False
        for subj in subjects:
            if subj.get('group') == old_name:
                subj['group'] = new_name
                updated_subjects = True
                print(f"[DEBUG] update_group: Updated subject '{subj.get('name')}' group reference")
        if updated_subjects:
            excel_service.save_subjects(subjects)
            print(f"[DEBUG] update_group: Subjects sheet saved")
        
        # Update Teachers sheet: subjects[].group field
        teachers = excel_service.get_teachers()
        updated_teachers = False
        for teacher in teachers:
            for subj_entry in teacher.get('subjects', []):
                if subj_entry.get('group') == old_name:
                    subj_entry['group'] = new_name
                    updated_teachers = True
                    print(f"[DEBUG] update_group: Updated teacher '{teacher.get('name')}' subject '{subj_entry.get('name')}' group reference")
        if updated_teachers:
            excel_service.save_teachers(teachers)
            print(f"[DEBUG] update_group: Teachers sheet saved")
    
    print(f"[DEBUG] update_group: Completed successfully")
    return jsonify({'success': True, 'group': data})


@groups_bp.route('/api/groups/<name>', methods=['DELETE'])
def delete_group(name):
    """Delete group"""
    groups = excel_service.get_groups()
    
    # Find and remove group
    group_idx = next((i for i, g in enumerate(groups) if g['name'] == name), None)
    if group_idx is None:
        return jsonify({'error': 'Group not found'}), 404
    
    groups.pop(group_idx)
    excel_service.save_groups(groups)
    
    return jsonify({'success': True})


@groups_bp.route('/api/groups/<name>/move', methods=['POST'])
def move_group(name):
    """Move group up or down in the list"""
    data = request.json
    direction = data.get('direction', 'up')

    groups = excel_service.get_groups()
    grp_idx = next((i for i, g in enumerate(groups) if g['name'] == name), None)
    if grp_idx is None:
        return jsonify({'error': 'Group not found'}), 404

    if direction == 'up' and grp_idx > 0:
        groups[grp_idx], groups[grp_idx - 1] = groups[grp_idx - 1], groups[grp_idx]
    elif direction == 'down' and grp_idx < len(groups) - 1:
        groups[grp_idx], groups[grp_idx + 1] = groups[grp_idx + 1], groups[grp_idx]

    excel_service.save_groups(groups)
    return jsonify({'success': True})
