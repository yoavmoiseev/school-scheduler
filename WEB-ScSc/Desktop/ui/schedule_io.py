# schedule_io.py
import os
from tkinter import messagebox
from school_scheduler.helpers import json_io, data_utils
import school_scheduler.data.consts as consts
from school_scheduler.ui.translations import GUI_TEXT

load_data = data_utils.load_data
load_schedules = data_utils.load_schedules
write_save_dict = json_io.write_save_dict


def reload_all(app):
    # Save current selections before reload
    selected_group = app.group_var.get() if hasattr(app, 'group_var') else ""
    selected_teacher = app.teacher_var.get() if hasattr(app, 'teacher_var') else ""
    
    app.teachers, app.groups, app.subjects = load_data()
    app.schedules = load_schedules()
    app.regenerate_derived_schedules(app.teachers, app.groups)

    # обновление таблиц
    app.teachers_tree.delete(*app.teachers_tree.get_children())
    for t in app.teachers:
        subj_display = ";  ".join(f"{s['name']} : {s['hours']} : {s.get('group','')}" for s in t.subjects)
        assigned = sum([int(s.get('hours', 0)) for s in t.subjects])
        
        # Calculate available lessons from availability slots
        available = 0
        if hasattr(t, 'available_slots') and t.available_slots:
            for day, intervals in t.available_slots.items():
                for start, end in intervals:
                    # Count lessons in range (inclusive)
                    available += (end - start + 1)
        
        lessons_display = f"{assigned}/{available}" if available > 0 else str(assigned)
        app.teachers_tree.insert("", "end", values=(t.name, subj_display, lessons_display))

    app.groups_tree.delete(*app.groups_tree.get_children())
    for g in app.groups:
        # Calculate total hours for this group from subjects
        total_hours = 0
        for s in app.subjects:
            subject_group = getattr(s, "group", "") or ""
            if subject_group == g.name:
                total_hours += s.hours_per_week
        
        app.groups_tree.insert("", "end", values=(g.name, g.comment, total_hours))

    app.subjects_tree.delete(*app.subjects_tree.get_children())
    for s in app.subjects:
        grp_name = getattr(s, "group", "") or ""
        app.subjects_tree.insert("", "end", values=(s.name, s.hours_per_week, grp_name))

    app.day_var.set("")
    app.build_day_table([g.name for g in app.groups])
    
    # обновление значений в комбобоксах
    if hasattr(app, "group_cb") and app.group_cb: # проверка на существование
        app.group_cb["values"] = [g.name for g in app.groups]
    if hasattr(app, "teacher_cb") and app.teacher_cb:
        app.teacher_cb["values"] = [t.name for t in app.teachers]

    # Restore selections and trigger recoloring
    if selected_group and selected_group in [g.name for g in app.groups]:
        app.group_var.set(selected_group)
        app.root.after(50, lambda: app.on_group_selected())
    else:
        app.group_var.set("")
        app.update_combobox_values(app.group_cells, [])
    
    if selected_teacher and selected_teacher in [t.name for t in app.teachers]:
        app.teacher_var.set(selected_teacher)
        app.root.after(50, lambda: app.on_teacher_selected())
    else:
        app.teacher_var.set("")
        app.update_combobox_values(app.teacher_cells, [])


def save_group_schedule(app, group_name, cells_map, user_confirmation=True):
    if not group_name:
        messagebox.showerror(GUI_TEXT[67], GUI_TEXT[161])  # "Error", "Select a group to save"
        return
    data = app.grid_to_data(cells_map)
    app.schedules.setdefault('groups', {})[group_name] = data
    app.regenerate_derived_schedules(app.teachers, app.groups)
    write_save_dict(consts.SCHEDULES_FILE, app.schedules)
    if user_confirmation:
        messagebox.showinfo(GUI_TEXT[162], GUI_TEXT[163].format(group_name=group_name))  # "Saved", "Group schedule for {group_name} saved"


def save_teacher_schedule(app, teacher_name, cells_map):
    if not teacher_name:
        messagebox.showerror(GUI_TEXT[67], GUI_TEXT[164])  # "Error", "Select a teacher to save"
        return
    data = app.grid_to_data(cells_map)
    app.schedules.setdefault('teachers', {})[teacher_name] = data
    write_save_dict(consts.SCHEDULES_FILE, app.schedules)
    messagebox.showinfo(GUI_TEXT[162], GUI_TEXT[165].format(teacher_name=teacher_name))  # "Saved", "Teacher schedule for {teacher_name} saved"


def regenerate_derived_schedules(app, teachers_list, groups_list):
    app.schedules.setdefault('groups', {})
    global_map = {}
    for gname, lessons in app.schedules.get('groups', {}).items():
        for lesson_str, day_map in (lessons or {}).items():
            for day, subj in (day_map or {}).items():
                global_map.setdefault(lesson_str, {}).setdefault(day, []).append(subj)

    global_out = {}
    for lesson_str, day_map in global_map.items():
        global_out[lesson_str] = {}
        for day, subj_list in day_map.items():
            global_out[lesson_str][day] = " / ".join(subj_list)
    app.schedules['global'] = global_out

    teacher_out = {}
    for t in teachers_list:
        teacher_out[t.name] = {}

    for gname, lessons in app.schedules.get('groups', {}).items():
        for lesson_str, day_map in (lessons or {}).items():
            for day, subj in (day_map or {}).items():
                # Find ALL teachers that teach this subject to this group
                matching_teachers = []
                for t in teachers_list:
                    for se in getattr(t, "subjects", []):
                        if not isinstance(se, dict):
                            continue
                        se_name = se.get("name")
                        se_group = se.get("group", "") or ""
                        if se_name == subj and (se_group == gname or se_group == ""):
                            matching_teachers.append(t.name)
                            break  # prevent adding same teacher twice if they have duplicate entries
                
                # Assign the lesson to ALL matching teachers
                for teacher_name in matching_teachers:
                    teacher_out.setdefault(teacher_name, {}).setdefault(lesson_str, {})[day] = subj
    
    app.schedules['teachers'] = teacher_out
