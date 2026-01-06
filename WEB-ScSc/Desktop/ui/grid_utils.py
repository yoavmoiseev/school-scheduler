import tkinter as tk
from tkinter import ttk
import school_scheduler.data.consts as consts
from school_scheduler.helpers.ui_helpers import color_cb_by_content

def create_lessons_lable(self, frame, lesson, r):
    time_text = consts.TIME_SLOTS.get(lesson, "")  # пустая строка, если нет ключа
    tk.Label(
        frame,
        text=f"{lesson}- {time_text}",
        borderwidth=1,
        relief="solid",
        width=9,
        height=2,
        font=("Arial", 10, "bold"),
        bg="#eee"
         ).grid(row=r, column=0, sticky="nsew")


def build_day_table(app, groups_list):
    """Create headers and comboboxes for the Day view (columns = groups_list)."""
    for w in app.table_frame.winfo_children():
        w.destroy()
    app.day_cells = {}
    tk.Label(app.table_frame, text="", borderwidth=1, relief="solid", width=8, height=2, bg="#ddd").grid(row=0, column=0, sticky="nsew")
    for c, gname in enumerate(groups_list, start=1):
        tk.Label(app.table_frame, text=gname, borderwidth=1, relief="solid", width=18, height=2, bg="#ddd").grid(row=0, column=c, sticky="nsew")
    
    for r, lesson in enumerate(consts.LESSONS, start=1):
        app.create_lessons_lable(app.table_frame, lesson, r)
        for c, gname in enumerate(groups_list, start=1):
            cb = ttk.Combobox(app.table_frame, values=[""], state="readonly", width=18, justify="center")
            cb.grid(row=r, column=c, sticky="nsew", padx=1, pady=1)
            app.day_cells[(r, gname)] = cb
            
    for c in range(len(groups_list) + 1):
        app.table_frame.grid_columnconfigure(c, weight=1)
    for r in range(len(consts.LESSONS) + 1):
        app.table_frame.grid_rowconfigure(r, weight=1)

def data_to_grid_day(app, selected_day):
    """Load subjects for the selected day into the day_cells using app.schedules."""
    for cb in app.day_cells.values():
        cb.set("")
    if not selected_day:
        return
    for (r, gname), cb in app.day_cells.items():
        grp_schedule = app.schedules.get('groups', {}).get(gname, {})
        lesson_map = grp_schedule.get(str(r), {}) if isinstance(grp_schedule, dict) else {}
        subj = lesson_map.get(selected_day, "")
        if subj:
            cb.set(subj)
            color_cb_by_content(cb)

def grid_to_data(cells_map):
    """Convert grid combobox state -> schedule dict {lesson_str: {day: subj}}."""
    out = {}
    day_index = {i+1: d for i, d in enumerate(consts.WEEKDAYS)}
    for (r, c), cb in cells_map.items():
        subj = cb.get().strip()
        if not subj:
            continue
        lesson = r
        day = day_index.get(c)
        if day is None:
            continue
        out.setdefault(str(lesson), {})[day] = subj
    return out

def data_to_grid(app, cells_map, data):
    """Populate comboboxes from schedule data. Uses app.clear_cells to reset first."""
    app.clear_cells(cells_map)
    if not data:
        return
    day_index = {d: i+1 for i, d in enumerate(consts.WEEKDAYS)}
    for lesson_str, day_map in (data or {}).items():
        try:
            lesson = int(lesson_str)
        except Exception:
            continue
        for day, subj in (day_map or {}).items():
            c = day_index.get(day)
            if c is None:
                continue
            cb = cells_map.get((lesson, c))
            if cb:
                cb.set(subj)
                color_cb_by_content(cb)
