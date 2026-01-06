# ui/popups.py

import os
import tkinter as tk
from tkinter import ttk, messagebox
from school_scheduler.helpers.json_io import write_append_json, write_save_json
from school_scheduler.helpers import data_utils
from school_scheduler.data.consts import DATA_DIR
from .translations import *


def add_teacher_popup(parent, on_done):
    _, _, subjects_local = data_utils.load_data()
    popup = tk.Toplevel(parent)
    popup.title(GUI_TEXT[58])  # "Add Teacher"
    tk.Label(popup, text=GUI_TEXT[59]).grid(row=0, column=0, sticky=tk.W, padx=6, pady=4)  # "Name"
    name_e = tk.Entry(popup, width=40); name_e.grid(row=0, column=1, padx=6, pady=4)

    tk.Label(popup, text=GUI_TEXT[60]).grid(row=1, column=0, padx=6, pady=4, sticky="w")  # "Available subjects"
    avail_lb = tk.Listbox(popup, height=8, exportselection=False)
    avail_lb.grid(row=2, column=0, padx=6, pady=4, sticky="nsew")

    btns_frame = tk.Frame(popup); btns_frame.grid(row=2, column=1, padx=6, pady=4, sticky="n")
    tk.Label(btns_frame, text=GUI_TEXT[61]).pack(pady=(0, 4))  # "Hours/week"
    hours_e = tk.Entry(btns_frame, width=8); hours_e.pack(pady=(0, 8))
    tk.Label(btns_frame, text=GUI_TEXT[62]).pack(pady=(4, 2))  # "Group (optional)"
    group_e = tk.Entry(btns_frame, width=12); group_e.pack(pady=(0, 8))

    def add_subject_from_avail():
        sel = avail_lb.curselection()
        if not sel:
            messagebox.showerror(GUI_TEXT[67], GUI_TEXT[68])  # "Error", "Select a subject to add"
            return
        name = avail_lb.get(sel[0])
        subj_obj = next((x for x in subjects_local if x.name == name), None)
        default_hours = subj_obj.hours_per_week if subj_obj else 0
        default_group = subj_obj.group if subj_obj else ""
        try:
            h = int(hours_e.get().strip() or default_hours)
        except Exception:
            messagebox.showerror(GUI_TEXT[67], GUI_TEXT[69])  # "Error", "Hours must be integer"
            return
        grp_val = group_e.get().strip() or default_group
        existing = [selected_lb.get(i).split(":", 1)[0] for i in range(selected_lb.size())]
        if name in existing:
            messagebox.showinfo(GUI_TEXT[70], GUI_TEXT[71])  # "Info", "Subject already added"
            return
        selected_lb.insert(tk.END, f"{name}:{h}:{grp_val}")

    def remove_selected_from_selected():
        sel = selected_lb.curselection()
        if not sel:
            return
        for i in reversed(sel):
            selected_lb.delete(i)

    tk.Button(btns_frame, text=GUI_TEXT[63], command=add_subject_from_avail).pack(fill=tk.X, pady=2)  # "Add >>"
    tk.Button(btns_frame, text=GUI_TEXT[64], command=remove_selected_from_selected).pack(fill=tk.X, pady=2)  # "<< Remove"

    tk.Label(popup, text=GUI_TEXT[65]).grid(row=1, column=2, padx=6, pady=4, sticky="w")  # "Selected subjects (name:hours:group)"
    selected_lb = tk.Listbox(popup, height=8, exportselection=False)
    selected_lb.grid(row=2, column=2, padx=6, pady=4, sticky="nsew")

    for subj in subjects_local:
        avail_lb.insert(tk.END, subj.name)

    def submit():
        name = name_e.get().strip()
        if not name:
            messagebox.showerror(GUI_TEXT[67], GUI_TEXT[72])  # "Error", "Name required"
            return
        items = []
        for i in range(selected_lb.size()):
            entry = selected_lb.get(i)
            parts = entry.split(":", 2)
            nm = parts[0].strip()
            hrs = 0
            grp = ""
            if len(parts) >= 2:
                try:
                    hrs = int(parts[1].strip())
                except Exception:
                    hrs = 0
            if len(parts) >= 3:
                grp = parts[2].strip()
            items.append({"name": nm, "hours": hrs, "group": grp})
        item = {"name": name, "subjects": items}
        write_append_json(os.path.join(DATA_DIR, "teachers.json"), "teachers", item)
        on_done()
        popup.destroy()

    tk.Button(popup, text=GUI_TEXT[66], command=submit).grid(row=3, column=0, columnspan=3, pady=8)  # "Add"


def add_group_popup(parent, on_done):
    popup = tk.Toplevel(parent)
    popup.title(GUI_TEXT[73])  # "Add Group"
    tk.Label(popup, text=GUI_TEXT[59]).grid(row=0, column=0, sticky=tk.W, padx=6, pady=4)  # "Name"
    name_e = tk.Entry(popup, width=40); name_e.grid(row=0, column=1, padx=6, pady=4)
    tk.Label(popup, text=GUI_TEXT[196]).grid(row=1, column=0, sticky=tk.W, padx=6, pady=4)  # "Comment"
    comment_e = tk.Entry(popup, width=40); comment_e.grid(row=1, column=1, padx=6, pady=4)

    def submit():
        name = name_e.get().strip()
        if not name:
            messagebox.showerror(GUI_TEXT[67], GUI_TEXT[72])  # "Error", "Name required"
            return
        comment = comment_e.get().strip()
        item = {"name": name, "comment": comment}
        write_append_json(os.path.join(DATA_DIR, "groups.json"), "groups", item)
        on_done()
        popup.destroy()

    tk.Button(popup, text=GUI_TEXT[66], command=submit).grid(row=2, column=0, columnspan=2, pady=8)  # "Add"


def add_subject_popup(parent, on_done):
    _, groups_local, _ = data_utils.load_data()
    popup = tk.Toplevel(parent)
    popup.title(GUI_TEXT[76])  # "Add Subject"
    tk.Label(popup, text=GUI_TEXT[59]).grid(row=0, column=0, sticky=tk.W, padx=6, pady=4)  # "Name"
    name_e = tk.Entry(popup, width=40); name_e.grid(row=0, column=1, padx=6, pady=4)
    tk.Label(popup, text=GUI_TEXT[77]).grid(row=1, column=0, sticky=tk.W, padx=6, pady=4)  # "Hours per week (int)"
    hours_e = tk.Entry(popup, width=40); hours_e.grid(row=1, column=1, padx=6, pady=4)
    tk.Label(popup, text=GUI_TEXT[78]).grid(row=2, column=0, sticky=tk.W, padx=6, pady=4)  # "Group (required)"
    group_var = tk.StringVar()
    group_cb = ttk.Combobox(popup, textvariable=group_var, values=[g.name for g in groups_local], state="readonly", width=37)
    group_cb.grid(row=2, column=1, padx=6, pady=4)

    def submit():
        name = name_e.get().strip()
        if not name:
            messagebox.showerror(GUI_TEXT[67], GUI_TEXT[72])  # "Error", "Name required"
            return
        try:
            hours = int(hours_e.get().strip() or 0)
        except ValueError:
            messagebox.showerror(GUI_TEXT[67], GUI_TEXT[69])  # "Error", "Hours must be integer"
            return
        group_sel = group_var.get().strip()
        if not group_sel:
            messagebox.showerror(GUI_TEXT[67], GUI_TEXT[79])  # "Error", "Group required for subject"
            return
        item = {"name": name, "hours_per_week": hours, "group": group_sel}
        write_append_json(os.path.join(DATA_DIR, "subjects.json"), "subjects", item)
        on_done()
        popup.destroy()

    tk.Button(popup, text=GUI_TEXT[66], command=submit).grid(row=3, column=0, columnspan=2, pady=8)  # "Add"


# Edit popups (placeholders for now)
def edit_teacher_popup(parent, teacher_name, on_done):
    pass  # implement edit teacher popup


def edit_group_popup(parent, group_name, on_done):
    pass  # implement edit group popup


def edit_subject_popup(parent, subject_name, on_done):
    pass  # implement edit subject popup

# End of file marker (for localization reference)
# GUI_TEXT[80] "End of popups.py code file"
