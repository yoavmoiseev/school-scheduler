# ui_handlers_additional.py
import os
import tkinter as tk
from tkinter import ttk, messagebox
from school_scheduler.helpers.ui_helpers import color_cb_by_content
from school_scheduler.helpers import json_io
import school_scheduler.data.consts as consts
from .translations import GUI_TEXT

# ---------------- GROUPS ----------------
def edit_selected_group(app):
    sel = app.groups_tree.selection()
    if not sel:
        messagebox.showerror(GUI_TEXT[67], GUI_TEXT[166])  # "Error", "Select a group to edit"
        return
    vals = app.groups_tree.item(sel[0], "values")
    orig_name = vals[0]
    g = next((x for x in app.groups if x.name == orig_name), None)
    if not g:
        messagebox.showerror(GUI_TEXT[67], GUI_TEXT[167])  # "Error", "Group not found"
        return

    def submit():
        name = name_e.get().strip()
        if not name:
            messagebox.showerror(GUI_TEXT[67], GUI_TEXT[72])  # "Error", "Name required"
            return
        comment = comment_e.get().strip()
        g.name = name
        g.comment = comment
        items = [{"name": x.name, "comment": x.comment} for x in app.groups]
        json_io.write_save_json(os.path.join(consts.DATA_DIR, "groups.json"), "groups", items)
        app.reload_all()
        popup.destroy()

    popup = tk.Toplevel(app.root)
    popup.title(GUI_TEXT[149])  # "Edit Subject" - reusing this, or we can add "Edit Group"
    tk.Label(popup, text=GUI_TEXT[59]).grid(row=0, column=0, sticky=tk.W, padx=6, pady=4)  # "Name"
    name_e = tk.Entry(popup, width=40)
    name_e.grid(row=0, column=1, padx=6, pady=4)
    name_e.insert(0, g.name)
    tk.Label(popup, text=GUI_TEXT[196]).grid(row=1, column=0, sticky=tk.W, padx=6, pady=4)  # "Comment"
    comment_e = tk.Entry(popup, width=40)
    comment_e.grid(row=1, column=1, padx=6, pady=4)
    comment_e.insert(0, g.comment)
    tk.Button(popup, text=GUI_TEXT[138], command=submit).grid(row=2, column=0, columnspan=2, pady=8)  # "Save Changes"


def delete_selected_group(app):
    sel = app.groups_tree.selection()
    if not sel:
        messagebox.showerror(GUI_TEXT[67], GUI_TEXT[168])  # "Error", "Select a group to delete"
        return
    vals = app.groups_tree.item(sel[0], "values")
    name = vals[0]
    if not messagebox.askyesno(GUI_TEXT[153], GUI_TEXT[169].format(name=name)):  # "Confirm", "Delete group '{name}'?":
        return
    for i, x in enumerate(app.groups):
        if x.name == name:
            del app.groups[i]
            break
    items = [{"name": x.name, "comment": x.comment} for x in app.groups]
    json_io.write_save_json(os.path.join(consts.DATA_DIR, "groups.json"), "groups", items)
    app.reload_all()


# ---------------- SUBJECTS ----------------
def edit_selected_subject(app):
    sel = app.subjects_tree.selection()
    if not sel:
        messagebox.showerror(GUI_TEXT[67], GUI_TEXT[170])  # "Error", "Select a subject to edit"
        return
    vals = app.subjects_tree.item(sel[0], "values")
    orig_name = vals[0]
    s = next((x for x in app.subjects if x.name == orig_name), None)
    if not s:
        messagebox.showerror(GUI_TEXT[67], GUI_TEXT[171])  # "Error", "Subject not found"
        return

    def submit():
        name = name_e.get().strip()
        if not name:
            messagebox.showerror("Error", "Name required")
            return
        try:
            hours = int(hours_e.get().strip() or 0)
        except ValueError:
            messagebox.showerror(GUI_TEXT[67], GUI_TEXT[69])  # "Error", "Hours must be integer"
            return
        group_sel = group_var.get().strip()
        
        # Save old name to find this subject in teachers
        old_name = s.name
        
        # Update subject data
        s.name = name
        s.hours_per_week = hours
        s.group = group_sel
        
        # Update this subject in all teachers
        for teacher in app.teachers:
            for t_subj in teacher.subjects:
                if t_subj.get('name') == old_name:
                    # Update name, hours, and group
                    t_subj['name'] = name
                    t_subj['hours'] = hours
                    t_subj['group'] = group_sel
        
        # Save subjects
        items = [{"name": x.name, "hours_per_week": x.hours_per_week, "group": getattr(x, "group", "")} for x in app.subjects]
        json_io.write_save_json(os.path.join(consts.DATA_DIR, "subjects.json"), "subjects", items)
        
        # Save teachers with updated subject data
        teachers_items = [
            {
                "name": t.name,
                "subjects": t.subjects,
                "available_slots": getattr(t, "available_slots", {}),
                "check_in_hours": getattr(t, "check_in_hours", {}),
                "check_out_hours": getattr(t, "check_out_hours", {})
            }
            for t in app.teachers
        ]
        json_io.write_save_json(os.path.join(consts.DATA_DIR, "teachers.json"), "teachers", teachers_items)
        
        app.reload_all()
        popup.destroy()

    popup = tk.Toplevel(app.root)
    popup.title(GUI_TEXT[149])  # "Edit Subject"
    tk.Label(popup, text=GUI_TEXT[84]).grid(row=0, column=0, sticky=tk.W, padx=6, pady=4)  # "Name"
    name_e = tk.Entry(popup, width=40)
    name_e.grid(row=0, column=1, padx=6, pady=4)
    name_e.insert(0, s.name)
    tk.Label(popup, text=GUI_TEXT[150]).grid(row=1, column=0, sticky=tk.W, padx=6, pady=4)  # "Hours per week (int)"
    hours_e = tk.Entry(popup, width=40)
    hours_e.grid(row=1, column=1, padx=6, pady=4)
    hours_e.insert(0, str(s.hours_per_week))
    tk.Label(popup, text=GUI_TEXT[151]).grid(row=2, column=0, sticky=tk.W, padx=6, pady=4)  # "Group (required)"
    group_var = tk.StringVar()
    group_cb = ttk.Combobox(popup, textvariable=group_var, values=[g.name for g in app.groups], state="readonly", width=37)
    group_cb.grid(row=2, column=1, padx=6, pady=4)
    group_var.set(getattr(s, "group", "") or "")
    tk.Button(popup, text=GUI_TEXT[94], command=submit).grid(row=3, column=0, columnspan=2, pady=8)  # "Save"


def delete_selected_subject(app):
    sel = app.subjects_tree.selection()
    if not sel:
        messagebox.showerror(GUI_TEXT[67], GUI_TEXT[152])  # "Error", "Select a subject to delete"
        return
    vals = app.subjects_tree.item(sel[0], "values")
    name = vals[0]
    if not messagebox.askyesno(GUI_TEXT[153], f"{GUI_TEXT[154]} '{name}'?"):  # "Confirm", "Delete subject"
        return
    
    # Delete subject from subjects list
    for i, x in enumerate(app.subjects):
        if x.name == name:
            del app.subjects[i]
            break
    
    # Remove subject from all teachers' assignments
    for teacher in app.teachers:
        teacher.subjects = [s for s in teacher.subjects if s.get('name') != name]
        teacher.total_hours = sum(s.get('hours', 0) for s in teacher.subjects)
    
    # Save subjects
    items = [{"name": x.name, "hours_per_week": x.hours_per_week, "group": getattr(x, "group", "")} for x in app.subjects]
    json_io.write_save_json(os.path.join(consts.DATA_DIR, "subjects.json"), "subjects", items)
    
    # Save teachers with updated assignments
    teachers_items = [
        {"name": t.name, "subjects": t.subjects, "available_slots": getattr(t, "available_slots", {})}
        for t in app.teachers
    ]
    json_io.write_save_json(os.path.join(consts.DATA_DIR, "teachers.json"), "teachers", teachers_items)
    
    app.reload_all()


# ---------------- SELECTION HANDLERS ----------------
def on_group_selected(app):
    """Выбор группы и обновление расписания группы."""
    
    name = app.group_var.get() # выбранное имя группы

    # фильтрация предметов по группе
    group_subjects = [s.name for s in app.subjects if getattr(s, 'group', '') == name] 

    if not group_subjects: # если нет предметов для группы, показываем все предметы
        group_subjects = [s.name for s in app.subjects] # все предметы
    app.update_combobox_values(app.group_cells, group_subjects) # обновление значений комбобоксов
    data = app.schedules.get('groups', {}).get(name, {}) # получение расписания группы
    app.data_to_grid(app.group_cells, data) # заполнение сетки данными
    for cb in app.group_cells.values(): # окраска комбобоксов по содержимому
        color_cb_by_content(cb) # окраска по содержимому
        try:
            cb.config(state="readonly") # установка состояния readonly
        except Exception:
            pass


def on_day_selected(app):
    day = app.day_var.get()
    grp_names = [g.name for g in app.groups]
    app.build_day_table(grp_names)
    for (r, gname), cb in app.day_cells.items():
        group_subjects = [s.name for s in app.subjects if getattr(s, "group", "") == gname]
        if not group_subjects:
            group_subjects = [s.name for s in app.subjects]
        try:
            cb["values"] = [""] + group_subjects
        except Exception:
            pass
    app.data_to_grid_day(day)
    for cb in app.day_cells.values():
        color_cb_by_content(cb)
        try:
            cb.config(state="disabled")
        except Exception:
            pass


# ---------------- MOVE UP/DOWN FUNCTIONS ----------------
def move_teacher_up(app):
    """Move selected teacher up in the list"""
    sel = app.teachers_tree.selection()
    if not sel:
        messagebox.showwarning("Warning", "Select a teacher to move")
        return
    vals = app.teachers_tree.item(sel[0], "values")
    name = vals[0]
    
    # Find teacher index
    idx = next((i for i, t in enumerate(app.teachers) if t.name == name), None)
    if idx is None or idx == 0:
        return  # Already at top or not found
    
    # Swap with previous
    app.teachers[idx], app.teachers[idx - 1] = app.teachers[idx - 1], app.teachers[idx]
    
    # Save new order
    items = [{"name": t.name, "subjects": t.subjects, "available_slots": getattr(t, "available_slots", {})} 
             for t in app.teachers]
    json_io.write_save_json(os.path.join(consts.DATA_DIR, "teachers.json"), "teachers", items)
    
    # Reload and restore selection (delayed to allow GUI to update)
    app.reload_all()
    app.root.after(50, lambda: _select_item_in_tree(app.teachers_tree, name))


def move_teacher_down(app):
    """Move selected teacher down in the list"""
    sel = app.teachers_tree.selection()
    if not sel:
        messagebox.showwarning(GUI_TEXT[157], GUI_TEXT[172])  # "Warning", "Select a teacher to move"
        return
    vals = app.teachers_tree.item(sel[0], "values")
    name = vals[0]
    
    # Find teacher index
    idx = next((i for i, t in enumerate(app.teachers) if t.name == name), None)
    if idx is None or idx >= len(app.teachers) - 1:
        return  # Already at bottom or not found
    
    # Swap with next
    app.teachers[idx], app.teachers[idx + 1] = app.teachers[idx + 1], app.teachers[idx]
    
    # Save new order
    items = [{"name": t.name, "subjects": t.subjects, "available_slots": getattr(t, "available_slots", {})} 
             for t in app.teachers]
    json_io.write_save_json(os.path.join(consts.DATA_DIR, "teachers.json"), "teachers", items)
    
    # Reload and restore selection (delayed to allow GUI to update)
    app.reload_all()
    app.root.after(50, lambda: _select_item_in_tree(app.teachers_tree, name))


def move_group_up(app):
    """Move selected group up in the list"""
    sel = app.groups_tree.selection()
    if not sel:
        messagebox.showwarning(GUI_TEXT[157], GUI_TEXT[173])  # "Warning", "Select a group to move"
        return
    vals = app.groups_tree.item(sel[0], "values")
    name = vals[0]
    
    # Find group index
    idx = next((i for i, g in enumerate(app.groups) if g.name == name), None)
    if idx is None or idx == 0:
        return  # Already at top or not found
    
    # Swap with previous
    app.groups[idx], app.groups[idx - 1] = app.groups[idx - 1], app.groups[idx]
    
    # Save new order
    items = [{"name": g.name, "comment": g.comment} for g in app.groups]
    json_io.write_save_json(os.path.join(consts.DATA_DIR, "groups.json"), "groups", items)
    
    # Reload and restore selection (delayed to allow GUI to update)
    app.reload_all()
    app.root.after(50, lambda: _select_item_in_tree(app.groups_tree, name))


def move_group_down(app):
    """Move selected group down in the list"""
    sel = app.groups_tree.selection()
    if not sel:
        messagebox.showwarning(GUI_TEXT[157], GUI_TEXT[173])  # "Warning", "Select a group to move"
        return
    vals = app.groups_tree.item(sel[0], "values")
    name = vals[0]
    
    # Find group index
    idx = next((i for i, g in enumerate(app.groups) if g.name == name), None)
    if idx is None or idx >= len(app.groups) - 1:
        return  # Already at bottom or not found
    
    # Swap with next
    app.groups[idx], app.groups[idx + 1] = app.groups[idx + 1], app.groups[idx]
    
    # Save new order
    items = [{"name": g.name, "comment": g.comment} for g in app.groups]
    json_io.write_save_json(os.path.join(consts.DATA_DIR, "groups.json"), "groups", items)
    
    # Reload and restore selection (delayed to allow GUI to update)
    app.reload_all()
    app.root.after(50, lambda: _select_item_in_tree(app.groups_tree, name))


def move_subject_up(app):
    """Move selected subject up in the list"""
    sel = app.subjects_tree.selection()
    if not sel:
        messagebox.showwarning(GUI_TEXT[157], GUI_TEXT[174])  # "Warning", "Select a subject to move"
        return
    vals = app.subjects_tree.item(sel[0], "values")
    name = vals[0]
    
    # Find subject index
    idx = next((i for i, s in enumerate(app.subjects) if s.name == name), None)
    if idx is None or idx == 0:
        return  # Already at top or not found
    
    # Swap with previous
    app.subjects[idx], app.subjects[idx - 1] = app.subjects[idx - 1], app.subjects[idx]
    
    # Save new order
    items = [{"name": s.name, "hours_per_week": s.hours_per_week, "group": getattr(s, "group", "")} 
             for s in app.subjects]
    json_io.write_save_json(os.path.join(consts.DATA_DIR, "subjects.json"), "subjects", items)
    
    # Reload and restore selection (delayed to allow GUI to update)
    app.reload_all()
    app.root.after(50, lambda: _select_item_in_tree(app.subjects_tree, name))


def move_subject_down(app):
    """Move selected subject down in the list"""
    sel = app.subjects_tree.selection()
    if not sel:
        messagebox.showwarning(GUI_TEXT[157], GUI_TEXT[174])  # "Warning", "Select a subject to move"
        return
    vals = app.subjects_tree.item(sel[0], "values")
    name = vals[0]
    
    # Find subject index
    idx = next((i for i, s in enumerate(app.subjects) if s.name == name), None)
    if idx is None or idx >= len(app.subjects) - 1:
        return  # Already at bottom or not found
    
    # Swap with next
    app.subjects[idx], app.subjects[idx + 1] = app.subjects[idx + 1], app.subjects[idx]
    
    # Save new order
    items = [{"name": s.name, "hours_per_week": s.hours_per_week, "group": getattr(s, "group", "")} 
             for s in app.subjects]
    json_io.write_save_json(os.path.join(consts.DATA_DIR, "subjects.json"), "subjects", items)
    
    # Reload and restore selection (delayed to allow GUI to update)
    app.reload_all()
    app.root.after(50, lambda: _select_item_in_tree(app.subjects_tree, name))


def _select_item_in_tree(tree, name):
    """Helper function to select an item by name in a treeview"""
    children = tree.get_children()
    for item in children:
        vals = tree.item(item, "values")
        if vals and vals[0] == name:
            tree.selection_set(item)
            tree.see(item)  # Scroll to make it visible
            return

