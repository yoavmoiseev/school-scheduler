# app_core.py
import tkinter as tk
from tkinter import ttk
from school_scheduler.helpers.ui_helpers import color_cb_by_content
from school_scheduler.helpers import json_io, data_utils
import school_scheduler.data.consts as consts

# импортируем функции для построения UI и обработки событий
from school_scheduler.ui.ui_build import build_ui
from school_scheduler.ui.ui_handlers import (
    edit_selected_teacher, delete_selected_teacher,
    on_teacher_selected
)
from school_scheduler.ui.ui_handlers_additional import (
    edit_selected_group, delete_selected_group,
    edit_selected_subject, delete_selected_subject,
    on_group_selected, on_day_selected,
    move_teacher_up, move_teacher_down,
    move_group_up, move_group_down,
    move_subject_up, move_subject_down
)
# импортируем функции для загрузки/сохранения расписаний
from school_scheduler.ui.schedule_io import (
    reload_all, save_group_schedule, save_teacher_schedule,
    regenerate_derived_schedules
)
# импортируем вспомогательные функции для таблиц и авто-заполнения
from school_scheduler.ui.grid_utils import (
    build_day_table, data_to_grid_day, grid_to_data, data_to_grid, create_lessons_lable
)
# импортируем функции для авто-заполнения расписаний
from school_scheduler.ui.autofill import (
    autofill_group, build_teacher_busy_map, count_subject_assignments
)

# основной класс приложения
class ScheduleApp:
    """Главный класс приложения расписаний."""

    def __init__(self, root):
        self.root = root
        self.root.title(consts.app_name)
        self.root.geometry(consts.app_size)
        print("INIT ScheduleApp", __file__, id(self))

        # Bring window to foreground
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)
        self.root.focus_force()

        # данные
        self.teachers = [] # список учителей
        self.groups = [] # список групп
        self.subjects = [] # список предметов
        self.schedules = {"groups": {}, "teachers": {}}

        # UI ссылки
        self.teachers_tree = None # дерево учителей
        self.groups_tree = None
        self.subjects_tree = None
        self.day_cells = {}
        self.group_cells = {}
        self.teacher_cells = {}

        # селекторы
        self.day_var = tk.StringVar() # выбранный день
        self.group_var = tk.StringVar() # выбранная группа
        self.teacher_var = tk.StringVar() # 

        build_ui(self)
        self.reload_all()
        
        # Auto-select first group after initialization to trigger coloring
        if self.groups and hasattr(self, 'group_cb') and self.group_cb:
            first_group = self.groups[0].name
            self.group_var.set(first_group)
            self.root.after(100, lambda: self.on_group_selected())

    # -------------------- делегаты вспомогательных функций --------------------
    def create_lessons_lable(self,frame, lesson, r):
        return create_lessons_lable(self,frame, lesson, r)
    
    def build_day_table(self, groups_list):
        return build_day_table(self, groups_list)

    def data_to_grid_day(self, selected_day):
        return data_to_grid_day(self, selected_day)

    def grid_to_data(self, cells_map):
        return grid_to_data(cells_map)

    def data_to_grid(self, cells_map, data):
        return data_to_grid(self, cells_map, data)
    
    def clear_cells(self, cells_map):
        """Очистить все combobox в указанной карте ячеек."""
        for cb in cells_map.values():
            try:
                cb.set("")
                color_cb_by_content(cb)
            except Exception:
                pass

    def count_subject_assignments(self, grid_data):
        return count_subject_assignments(grid_data)

    def build_teacher_busy_map(self, existing_schedule, teachers_list, debug=False):
        return build_teacher_busy_map(existing_schedule, teachers_list, debug)

    def autofill_group(self, group_name, cells_map, subjects_list, teachers_list, _attempt=1):
        return autofill_group(self, group_name, cells_map, subjects_list, teachers_list, _attempt=_attempt)

    def update_combobox_values(self, cells_map, choices, group_name=None):
        """Оригинальная логика из старого файла — обновление значений комбо-боксов."""
        if not choices:
            for cb in cells_map.values():
                try:
                    cb["values"] = [""]
                    cb.set("")
                    color_cb_by_content(cb)
                except Exception:
                    pass
            return

        if group_name is None:
            try:
                group_name = self.group_var.get()
            except Exception:
                group_name = ""

        subj_teachers = {name: [] for name in choices}

        try:
            existing_schedule = self.schedules or data_utils.load_schedules()
        except Exception:
            existing_schedule = data_utils.load_schedules()
        teacher_busy = self.build_teacher_busy_map(existing_schedule, self.teachers)

        teacher_avail = {}
        for t in self.teachers:
            subj_hours = {}
            for se in getattr(t, "subjects", []) or []:
                if not isinstance(se, dict):
                    continue
                nm = se.get("name")
                grp = se.get("group", "") or ""
                try:
                    hrs = int(se.get("hours", 0))
                except Exception:
                    hrs = 0
                if nm in subj_teachers and (grp == group_name or grp == ""):
                    subj_hours[nm] = subj_hours.get(nm, 0) + max(0, hrs)
            if not subj_hours:
                continue

            slots = set()
            if getattr(t, "available_slots", None):
                for day, intervals in (t.available_slots or {}).items():
                    for iv in intervals:
                        try:
                            start, end = iv[0], iv[1]
                            for l in range(start, end + 1):
                                if (day, l) not in teacher_busy.get(t.name, set()):
                                    slots.add((day, l))
                        except Exception:
                            continue

            if not slots:
                continue

            teacher_avail[t.name] = {"slots": slots, "teacher_obj": t, "subj_hours": subj_hours}
            for nm in subj_hours.keys():
                subj_teachers[nm].append(t.name)

        day_index = {i + 1: d for i, d in enumerate(consts.WEEKDAYS)}

        for (r, c), cb in cells_map.items():
            day = day_index.get(c)
            lesson = int(r)
            allowed = []
            for subj in choices:
                teacher_names = subj_teachers.get(subj, [])
                if not teacher_names:
                    continue
                for tn in teacher_names:
                    info = teacher_avail.get(tn)
                    if info and (day, lesson) in info["slots"]:
                        allowed.append(subj)
                        break
            allowed = sorted(dict.fromkeys(allowed))
            cur = cb.get().strip()
            values = [""] + allowed
            try:
                cb["values"] = values
                if cur and cur not in values:
                    cb.set(cur)
                color_cb_by_content(cb)
                cb.bind("<<ComboboxSelected>>", lambda e, cb=cb: color_cb_by_content(cb))
            except Exception:
                pass


    # -------------------- делегаты бизнес-логики --------------------
    def reload_all(self):
        reload_all(self)

    def save_group_schedule(self, group_name, cells_map, user_confirmation = True):
        save_group_schedule(self, group_name, cells_map, user_confirmation)

    def save_teacher_schedule(self, teacher_name, cells_map):
        save_teacher_schedule(self, teacher_name, cells_map)

    def regenerate_derived_schedules(self, teachers, groups):
        regenerate_derived_schedules(self, teachers, groups)

    # -------------------- редактирование / выбор --------------------
    def edit_selected_teacher(self): edit_selected_teacher(self)
    def delete_selected_teacher(self): delete_selected_teacher(self)
    def edit_selected_group(self): edit_selected_group(self)
    def delete_selected_group(self): delete_selected_group(self)
    def edit_selected_subject(self): edit_selected_subject(self)
    def delete_selected_subject(self): delete_selected_subject(self)
    def on_group_selected(self): on_group_selected(self)
    def on_teacher_selected(self): on_teacher_selected(self)
    def on_day_selected(self): on_day_selected(self)
    
    # -------------------- перемещение элементов --------------------
    def move_teacher_up(self): move_teacher_up(self)
    def move_teacher_down(self): move_teacher_down(self)
    def move_group_up(self): move_group_up(self)
    def move_group_down(self): move_group_down(self)
    def move_subject_up(self): move_subject_up(self)
    def move_subject_down(self): move_subject_down(self)

    # -------------------- запуск --------------------
    def run(self):
        self.root.mainloop()
