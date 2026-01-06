import random
from tkinter import messagebox
from school_scheduler.helpers import data_utils
from school_scheduler.helpers.ui_helpers import color_cb_by_content
import school_scheduler.data.consts as consts

def count_subject_assignments(grid_data):
    counts = {}
    for lesson_str, day_map in grid_data.items():
        for day, subj in (day_map or {}).items():
            counts[subj] = counts.get(subj, 0) + 1
    return counts

def normalize_day(col, day_index):
    if isinstance(col, int):
        return day_index.get(col)
    if isinstance(col, str):
        s = col.strip()
        if s.isdigit():
            return day_index.get(int(s))
        for v in day_index.values():
            if v.lower() == s.lower():
                return v
    return None

def build_teacher_busy_map(existing_schedule, teachers_list, debug=False):
    busy = {}
    groups = {}
    teachers_map_from_schedule = {}
    if not existing_schedule:
        return busy
    if isinstance(existing_schedule, dict) and "groups" in existing_schedule:
        groups = existing_schedule.get("groups", {}) or {}
        teachers_map_from_schedule = existing_schedule.get("teachers", {}) or {}
    else:
        groups = existing_schedule or {}

    def norm(s):
        try:
            return str(s).strip().lower()
        except Exception:
            return ""

    for gname, gdata in groups.items():
        if not isinstance(gdata, dict):
            continue
        for lesson_key, daymap in gdata.items():
            try:
                lesson = int(lesson_key)
            except Exception:
                continue
            if not isinstance(daymap, dict):
                continue
            for day, subj_entry in daymap.items():
                if subj_entry is None:
                    continue
                subj_names = []
                if isinstance(subj_entry, str):
                    parts = [p.strip() for p in subj_entry.split("/") if p.strip()]
                    subj_names.extend(parts)
                elif isinstance(subj_entry, dict):
                    sname = subj_entry.get("subject") or subj_entry.get("name") or ""
                    if sname:
                        parts = [p.strip() for p in str(sname).split("/") if p.strip()]
                        subj_names.extend(parts)
                else:
                    try:
                        s = str(subj_entry)
                        parts = [p.strip() for p in s.split("/") if p.strip()]
                        subj_names.extend(parts)
                    except Exception:
                        continue
                for subj_name in subj_names:
                    if not subj_name:
                        continue
                    norm_subj = norm(subj_name)
                    for t in teachers_list:
                        for se in getattr(t, "subjects", []):
                            if not isinstance(se, dict):
                                continue
                            se_name = norm(se.get("name") or "")
                            if se_name and se_name == norm_subj:
                                busy.setdefault(t.name, set()).add((day, lesson))
    if isinstance(teachers_map_from_schedule, dict):
        for tname, lessons_map in teachers_map_from_schedule.items():
            if not isinstance(lessons_map, dict):
                continue
            for lesson_key, daymap in lessons_map.items():
                try:
                    lesson = int(lesson_key)
                except Exception:
                    continue
                if not isinstance(daymap, dict):
                    continue
                for day, subj_entry in daymap.items():
                    busy.setdefault(tname, set()).add((day, lesson))
    if debug:
        out = {k: sorted(list(v)) for k, v in busy.items()}
        print("build_teacher_busy_map ->", out)
    return busy