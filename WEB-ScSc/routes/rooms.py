from flask import Blueprint, request, jsonify

rooms_bp = Blueprint('rooms', __name__)

# Will be initialized by app.py
excel_service = None


def init_routes(excel_svc):
    global excel_service
    excel_service = excel_svc


@rooms_bp.route('/api/rooms', methods=['GET'])
def get_rooms():
    """List all rooms"""
    rooms = excel_service.get_rooms()
    return jsonify(rooms)


@rooms_bp.route('/api/rooms', methods=['POST'])
def create_room():
    """Create a new room"""
    data = request.json
    if not data.get('name'):
        return jsonify({'error': 'Name required'}), 400

    rooms = excel_service.get_rooms()
    if any(r['name'] == data['name'] for r in rooms):
        return jsonify({'error': 'Room already exists'}), 400

    rooms.append({'name': data['name'], 'description': data.get('description', '')})
    excel_service.save_rooms(rooms)
    return jsonify({'success': True}), 201


@rooms_bp.route('/api/rooms/<path:name>', methods=['PUT'])
def update_room(name):
    """Update an existing room"""
    data = request.json
    rooms = excel_service.get_rooms()
    idx = next((i for i, r in enumerate(rooms) if r['name'] == name), None)
    if idx is None:
        return jsonify({'error': 'Room not found'}), 404

    new_name = data.get('name', name)
    # If name changed, update groups that reference this room
    if new_name != name:
        groups = excel_service.get_groups()
        for g in groups:
            if g.get('room') == name:
                g['room'] = new_name
        excel_service.save_groups(groups)

    rooms[idx] = {'name': new_name, 'description': data.get('description', '')}
    excel_service.save_rooms(rooms)
    return jsonify({'success': True})


@rooms_bp.route('/api/rooms/<path:name>', methods=['DELETE'])
def delete_room(name):
    """Delete a room"""
    rooms = excel_service.get_rooms()
    original = len(rooms)
    rooms = [r for r in rooms if r['name'] != name]
    if len(rooms) == original:
        return jsonify({'error': 'Room not found'}), 404

    # Clear room from all groups referencing it
    groups = excel_service.get_groups()
    for g in groups:
        if g.get('room') == name:
            g['room'] = ''
    excel_service.save_groups(groups)

    excel_service.save_rooms(rooms)
    return jsonify({'success': True})


@rooms_bp.route('/api/rooms/free', methods=['GET'])
def get_free_rooms():
    """Return rooms that are free at a specific day+lesson slot.
    Query params: day=<day>&lesson=<lesson_num>
    A room is free if the group assigned to that room has no lesson at that slot.
    """
    day = request.args.get('day', '')
    lesson = request.args.get('lesson', '')
    if not day or not lesson:
        return jsonify({'error': 'day and lesson params required'}), 400

    try:
        lesson_num = int(lesson)
    except ValueError:
        return jsonify({'error': 'lesson must be integer'}), 400

    rooms = excel_service.get_rooms()
    groups = excel_service.get_groups()
    schedules = excel_service.get_group_schedules()

    # Map room -> list of groups that use this room
    room_to_groups = {}
    for g in groups:
        rm = g.get('room', '').strip()
        if rm:
            room_to_groups.setdefault(rm, []).append(g['name'])

    result = []
    for room in rooms:
        rname = room['name']
        occupying_groups = room_to_groups.get(rname, [])
        is_free = True
        for gname in occupying_groups:
            sched = schedules.get(gname, {})
            day_sched = sched.get(day, {})
            # lesson key may be int or str
            if day_sched.get(lesson_num) or day_sched.get(str(lesson_num)):
                is_free = False
                break
        result.append({'name': rname, 'description': room.get('description', ''), 'free': is_free})

    return jsonify(result)
