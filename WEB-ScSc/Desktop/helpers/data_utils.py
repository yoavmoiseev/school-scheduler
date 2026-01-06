# data_utils.py
import os
import json
from school_scheduler.helpers import json_io
import school_scheduler.data.consts as consts
from models.teacher import Teacher
from models.group import Group
from models.subject import Subject

def _normalize_teacher_entry(entry):
    """ Normalize teacher entry to have consistent subjects format. """
    subs = entry.get("subjects", [])
    normalized = []
    for s in subs or []:
        if isinstance(s, dict):
            name = s.get("name")
            try:
                hours = int(s.get("hours", 0))
            except Exception:
                hours = 0
            group = s.get("group", "") or ""
        else:
            if ":" in str(s):
                parts = str(s).split(":", 1)
                name = parts[0].strip()
                try:
                    hours = int(parts[1].strip())
                except Exception:
                    hours = 0
            else:
                name = str(s)
                hours = 0
            group = ""
        normalized.append({"name": name, "hours": hours, "group": group})
    
    # Normalize check_in_hours and check_out_hours to lists for backward compatibility
    check_in_hours = entry.get("check_in_hours", {})
    check_out_hours = entry.get("check_out_hours", {})
    available_slots = entry.get("available_slots", {})
    
    # Convert string values to lists matching number of intervals per day
    normalized_check_in = {}
    normalized_check_out = {}
    
    for day, intervals in available_slots.items():
        num_intervals = len(intervals) if isinstance(intervals, list) else 1
        
        # Handle check_in_hours
        day_check_in = check_in_hours.get(day, "")
        if isinstance(day_check_in, str):
            # Old format: single string, replicate for all intervals
            normalized_check_in[day] = [day_check_in] * num_intervals if day_check_in else []
        elif isinstance(day_check_in, list):
            # New format: already a list
            normalized_check_in[day] = day_check_in
        else:
            normalized_check_in[day] = []
        
        # Handle check_out_hours
        day_check_out = check_out_hours.get(day, "")
        if isinstance(day_check_out, str):
            # Old format: single string, replicate for all intervals
            normalized_check_out[day] = [day_check_out] * num_intervals if day_check_out else []
        elif isinstance(day_check_out, list):
            # New format: already a list
            normalized_check_out[day] = day_check_out
        else:
            normalized_check_out[day] = []
    
    return {
        "name": entry.get("name"),
        "subjects": normalized,
        "available_slots": available_slots,
        "check_in_hours": normalized_check_in,
        "check_out_hours": normalized_check_out
    }

def load_data():
    """Load teachers, groups, subjects and return model instances lists."""
    # Use DATA_DIR from consts which handles both dev and frozen modes
    data_dir = consts.DATA_DIR
    teachers_raw = json_io._load_json(os.path.join(data_dir, "teachers.json"), key="teachers")
    groups_raw = json_io._load_json(os.path.join(data_dir, "groups.json"), key="groups")
    subjects_raw = json_io._load_json(os.path.join(data_dir, "subjects.json"), key="subjects")
    teachers_raw = [ _normalize_teacher_entry(t) for t in teachers_raw ]
    teachers = [Teacher(**t) for t in teachers_raw]
    groups = [Group(**g) for g in groups_raw]
    subjects = [Subject(**s) for s in subjects_raw]
    return teachers, groups, subjects

def load_schedules():
    # Use SCHEDULES_FILE from consts which handles both dev and frozen modes
    schedules_file = consts.SCHEDULES_FILE
    if not os.path.exists(schedules_file):
        return {"groups": {}, "teachers": {}}
    with open(schedules_file, "r", encoding="utf-8") as f:
        return json.load(f)

# The rest of helpers from original refactor: build_teacher_busy_map, normalize_day, count_subject_assignments, ...