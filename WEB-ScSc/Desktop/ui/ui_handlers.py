# ui_handlers.py
import os
import tkinter as tk
from tkinter import ttk, messagebox
from school_scheduler.helpers.ui_helpers import color_cb_by_content
from school_scheduler.helpers import json_io
import school_scheduler.data.consts as consts

# import translations (GUI_TEXT_EN, GUI_TEXT_HE, GUI_TEXT_RU)
from .translations import *

# ---------------- TEACHER ----------------
def edit_selected_teacher(app):
    sel = app.teachers_tree.selection()
    if not sel:
        messagebox.showerror(GUI_TEXT[95], GUI_TEXT[82])  # "Error", "Select a teacher to edit"
        return
    vals = app.teachers_tree.item(sel[0], "values")
    orig_name = vals[0]
    t = next((x for x in app.teachers if x.name == orig_name), None)
    if not t:
        messagebox.showerror(GUI_TEXT[95], GUI_TEXT[83])  # "Error", "Teacher not found"
        return

    popup = tk.Toplevel(app.root)
    popup.title(GUI_TEXT[81])  # "Edit Teacher"
    popup.geometry("1020x850")  # Set larger window size
    
    # Create main frame with scrollbar
    main_frame = tk.Frame(popup)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Create canvas and scrollbar
    canvas = tk.Canvas(main_frame)
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Use scrollable_frame as parent for all widgets
    popup_parent = scrollable_frame
    
    tk.Label(popup_parent, text=GUI_TEXT[84]).grid(row=0, column=0, sticky=tk.W, padx=6, pady=4)  # "Name"
    name_e = tk.Entry(popup_parent, width=40)
    name_e.grid(row=0, column=1, padx=6, pady=4)
    name_e.insert(0, t.name)

    tk.Label(popup_parent, text=GUI_TEXT[85]).grid(row=1, column=0, padx=6, pady=4, sticky="w")  # "Available subjects"
    
    # Frame for Available Subjects listbox with scrollbar
    avail_frame = tk.Frame(popup_parent)
    avail_frame.grid(row=2, column=0, padx=6, pady=4)
    
    avail_lb = tk.Listbox(avail_frame, height=8, exportselection=False)
    avail_lb.pack(side="left", fill="both", expand=True)
    
    avail_scrollbar = tk.Scrollbar(avail_frame, orient="vertical", command=avail_lb.yview)
    avail_scrollbar.pack(side="right", fill="y")
    avail_lb.configure(yscrollcommand=avail_scrollbar.set)

    btns_frame = tk.Frame(popup_parent)
    btns_frame.grid(row=2, column=1, padx=6, pady=4, sticky="n")

    def add_subject_from_avail():
        sel_idx = avail_lb.curselection()
        if not sel_idx:
            return
        name_subj = avail_lb.get(sel_idx[0])
        subj_obj = next((x for x in app.subjects if x.name == name_subj), None)
        default_hours = subj_obj.hours_per_week if subj_obj else 0
        default_group = subj_obj.group if subj_obj else ""
        h = default_hours
        existing = [selected_lb.get(i).split(":", 1)[0] for i in range(selected_lb.size())]
        if name_subj in existing:
            messagebox.showinfo(GUI_TEXT[96], GUI_TEXT[87])  # "Info", "Subject already added"
            return
        
        # Check if this subject is already assigned to other teachers
        other_teachers = []
        for teacher in app.teachers:
            if teacher.name == t.name:  # Skip current teacher
                continue
            for subj in teacher.subjects:
                if subj.get('name') == name_subj:
                    other_teachers.append(teacher.name)
                    break
        
        if other_teachers:
            teachers_list = ", ".join(other_teachers)
            warning_msg = f"{GUI_TEXT[155]} {teachers_list}.\n\n{GUI_TEXT[156]}"
            result = messagebox.askokcancel(GUI_TEXT[157], warning_msg)
            popup.lift()  # Bring popup back to foreground
            popup.focus_force()
            if not result:
                return
        
        selected_lb.insert(tk.END, f"{name_subj}:{h}:{default_group}")

    def remove_selected_from_selected():
        sel_idx = selected_lb.curselection()
        for i in reversed(sel_idx):
            selected_lb.delete(i)

    tk.Button(btns_frame, text=GUI_TEXT[100], command=add_subject_from_avail).pack(fill=tk.X, pady=2)
    tk.Button(btns_frame, text=GUI_TEXT[101], command=remove_selected_from_selected).pack(fill=tk.X, pady=2)

    tk.Label(popup_parent, text=GUI_TEXT[88]).grid(row=1, column=2, padx=6, pady=4, sticky="w")  # "Selected subjects (name:hours:group)"
    
    # Frame for Selected Subjects listbox with scrollbar
    selected_frame = tk.Frame(popup_parent)
    selected_frame.grid(row=2, column=2, padx=6, pady=4)
    
    selected_lb = tk.Listbox(selected_frame, height=8, exportselection=False)
    selected_lb.pack(side="left", fill="both", expand=True)
    
    selected_scrollbar = tk.Scrollbar(selected_frame, orient="vertical", command=selected_lb.yview)
    selected_scrollbar.pack(side="right", fill="y")
    selected_lb.configure(yscrollcommand=selected_scrollbar.set)

    for subj in app.subjects:
        avail_lb.insert(tk.END, subj.name)
    for s_entry in t.subjects:
        selected_lb.insert(tk.END, f"{s_entry['name']}:{s_entry.get('hours', 0)}:{s_entry.get('group', '')}")

    # New row for Availability Hours input
    tk.Label(popup_parent, text=GUI_TEXT[129]).grid(row=5, column=0, columnspan=3, sticky="w", padx=6, pady=(10,4))  # "Availability Hours (Start-End)"
    day_cb2 = ttk.Combobox(popup_parent, values=consts.WEEKDAYS, state="readonly", width=12)
    day_cb2.grid(row=6, column=0, padx=2, pady=2)
    
    # Get time slots for dropdown
    time_slots_list = [f"{k}: {v}" for k, v in sorted(consts.TIME_SLOTS.items())]
    
    start_time_cb = ttk.Combobox(popup_parent, values=time_slots_list, state="readonly", width=15)
    start_time_cb.grid(row=6, column=1, padx=2, pady=2)
    start_time_cb.set(GUI_TEXT[133])  # "Start time (HH:MM)"
    
    end_time_cb = ttk.Combobox(popup_parent, values=time_slots_list, state="readonly", width=15)
    end_time_cb.grid(row=6, column=2, padx=2, pady=2)
    end_time_cb.set(GUI_TEXT[134])  # "End time (HH:MM)"

    # Third row for Real Hours input (Check In/Check Out time)
    tk.Label(popup_parent, text=GUI_TEXT[159]).grid(row=7, column=0, columnspan=3, sticky="w", padx=6, pady=(10,4))  # "Reporting : Dismissal Time"
    day_cb3 = ttk.Combobox(popup_parent, values=consts.WEEKDAYS, state="readonly", width=12)
    day_cb3.grid(row=8, column=0, padx=2, pady=2)
    
    # Entry fields for Check In and Check Out time (HH:MM format)
    checkin_e = tk.Entry(popup_parent, width=10)
    checkin_e.grid(row=8, column=1, padx=2, pady=2)
    checkin_e.insert(0, "HH:MM")
    
    checkout_e = tk.Entry(popup_parent, width=10)
    checkout_e.grid(row=8, column=2, padx=2, pady=2)
    checkout_e.insert(0, "HH:MM")

    # Replace Listbox with Treeview (4 columns)
    avail_tree = ttk.Treeview(popup_parent, columns=("day", "lessons", "timeslots", "avail_hours"), show="headings", height=10)
    avail_tree.heading("day", text=GUI_TEXT[130])  # "DAY"
    avail_tree.heading("lessons", text=GUI_TEXT[139])  # "LESSONS"
    avail_tree.heading("timeslots", text=GUI_TEXT[140])  # "TIME SLOTS"
    avail_tree.heading("avail_hours", text=GUI_TEXT[132])  # "REAL HOURS"
    avail_tree.column("day", width=80)
    avail_tree.column("lessons", width=80)
    avail_tree.column("timeslots", width=100)
    avail_tree.column("avail_hours", width=120)
    
    # Add scrollbar for treeview
    tree_scroll = tk.Scrollbar(popup_parent, orient="vertical", command=avail_tree.yview)
    avail_tree.configure(yscrollcommand=tree_scroll.set)
    
    avail_tree.grid(row=10, column=0, columnspan=4, padx=6, pady=4, sticky="nsew")
    tree_scroll.grid(row=10, column=4, sticky="ns", pady=4)

    def calculate_availability_hours(start_lesson, end_lesson):
        """Calculate total availability hours based on lesson range"""
        total_minutes = 0
        for lesson_num in range(start_lesson, end_lesson + 1):
            time_range = consts.TIME_SLOTS.get(lesson_num, "")
            if "-" in time_range:
                start_time, end_time = time_range.split("-")
                # Parse HH:MM format
                start_h, start_m = map(int, start_time.split(":"))
                end_h, end_m = map(int, end_time.split(":"))
                # Calculate minutes
                minutes = (end_h * 60 + end_m) - (start_h * 60 + start_m)
                total_minutes += minutes
        
        hours = total_minutes / 60
        return f"{hours:.2f}h"

    def convert_real_time_to_lessons(checkin_str, checkout_str):
        """Convert real check in/out time (HH:MM) to lesson numbers"""
        try:
            # Parse check in/out times
            checkin_h, checkin_m = map(int, checkin_str.split(":"))
            checkout_h, checkout_m = map(int, checkout_str.split(":"))
            checkin_minutes = checkin_h * 60 + checkin_m
            checkout_minutes = checkout_h * 60 + checkout_m
            
            if checkout_minutes <= checkin_minutes:
                return None, None
            
            first_lesson = None
            last_lesson = None
            
            # Find which lessons are covered by this time range
            for lesson_num in sorted(consts.TIME_SLOTS.keys()):
                time_range = consts.TIME_SLOTS[lesson_num]
                if "-" not in time_range:
                    continue
                    
                lesson_start, lesson_end = time_range.split("-")
                ls_h, ls_m = map(int, lesson_start.split(":"))
                le_h, le_m = map(int, lesson_end.split(":"))
                lesson_start_minutes = ls_h * 60 + ls_m
                lesson_end_minutes = le_h * 60 + le_m
                
                # Check if lesson is fully covered by check in/out time
                # Teacher must arrive BEFORE or AT lesson start AND leave AFTER or AT lesson end
                if checkin_minutes <= lesson_start_minutes and checkout_minutes >= lesson_end_minutes:
                    if first_lesson is None:
                        first_lesson = lesson_num
                    last_lesson = lesson_num
            
            return first_lesson, last_lesson
        except (ValueError, AttributeError):
            return None, None

    def add_hours_interval():
        day = day_cb2.get().strip()
        start_time_str = start_time_cb.get()
        end_time_str = end_time_cb.get()
        
        if not day:
            messagebox.showerror(GUI_TEXT[95], GUI_TEXT[91])  # "Error", "Choose a day"
            return
        if start_time_str == GUI_TEXT[133] or end_time_str == GUI_TEXT[134]:
            messagebox.showerror(GUI_TEXT[95], GUI_TEXT[175])  # "Error", "Please select start and end times"
            return
        
        # Parse lesson numbers from "1: 09:15-10:00" format
        try:
            start_lesson = int(start_time_str.split(":")[0])
            end_lesson = int(end_time_str.split(":")[0])
            
            if start_lesson > end_lesson:
                messagebox.showerror(GUI_TEXT[95], GUI_TEXT[176])  # "Error", "Start time must be before end time"
                return
            
            # Calculate time slots and availability hours
            time_start = consts.TIME_SLOTS.get(start_lesson, "").split("-")[0]
            time_end = consts.TIME_SLOTS.get(end_lesson, "").split("-")[1] if "-" in consts.TIME_SLOTS.get(end_lesson, "") else ""
            timeslots = f"{time_start}-{time_end}" if time_start and time_end else ""
            
            # Copy timeslots value to Teacher Weekly Hours column
            teacher_weekly_hours = timeslots
            
            # Insert into treeview
            avail_tree.insert("", "end", values=(day, f"{start_lesson}-{end_lesson}", timeslots, teacher_weekly_hours))
            
            # Reset comboboxes
            start_time_cb.set(GUI_TEXT[133])
            end_time_cb.set(GUI_TEXT[134])
        except (ValueError, IndexError):
            messagebox.showerror(GUI_TEXT[95], GUI_TEXT[177])  # "Error", "Invalid time format"
            return

    def add_real_hours_interval():
        """Add availability using real check in/out time (HH:MM)"""
        day = day_cb3.get().strip()
        checkin_str = checkin_e.get().strip()
        checkout_str = checkout_e.get().strip()
        
        if not day:
            messagebox.showerror(GUI_TEXT[95], GUI_TEXT[91])  # "Error", "Choose a day"
            return
        if checkin_str == "HH:MM" or checkout_str == "HH:MM":
            messagebox.showerror(GUI_TEXT[95], GUI_TEXT[178])  # "Error", "Please enter check in/out times"
            return
        
        # Convert real time to lessons
        first_lesson, last_lesson = convert_real_time_to_lessons(checkin_str, checkout_str)
        
        if first_lesson is None or last_lesson is None:
            messagebox.showerror(GUI_TEXT[95], GUI_TEXT[179])  # "Error", "No lessons found in this time range. Check your times."
            return
        
        # Calculate display values
        time_start = consts.TIME_SLOTS.get(first_lesson, "").split("-")[0]
        time_end = consts.TIME_SLOTS.get(last_lesson, "").split("-")[1] if "-" in consts.TIME_SLOTS.get(last_lesson, "") else ""
        timeslots = f"{time_start}-{time_end}" if time_start and time_end else ""
        
        # Show actual check in/out times in REAL HOURS column
        real_hours_display = f"{checkin_str}-{checkout_str}"
        
        # Insert into treeview
        avail_tree.insert("", "end", values=(day, f"{first_lesson}-{last_lesson}", timeslots, real_hours_display))
        
        # Reset entry fields
        checkin_e.delete(0, tk.END)
        checkin_e.insert(0, "HH:MM")
        checkout_e.delete(0, tk.END)
        checkout_e.insert(0, "HH:MM")

    def remove_interval():
        sel_items = avail_tree.selection()
        for item in sel_items:
            avail_tree.delete(item)

    tk.Button(popup_parent, text=GUI_TEXT[136], command=add_hours_interval).grid(row=6, column=3, padx=4, sticky="w")  # "Add Time Slots"
    tk.Button(popup_parent, text=GUI_TEXT[137], command=add_real_hours_interval).grid(row=8, column=3, padx=4, sticky="w")  # "Add Real Hours"
    tk.Button(popup_parent, text=GUI_TEXT[93], command=remove_interval).grid(row=9, column=0, columnspan=4, padx=6, pady=2)  # "Remove Interval"

    # Load existing availability slots
    if hasattr(t, "available_slots") and t.available_slots:
        # Get real hours for reference
        check_in_hours = getattr(t, "check_in_hours", {})
        check_out_hours = getattr(t, "check_out_hours", {})
        
        # PRIORITY: If check_in_hours/check_out_hours exist, recalculate available_slots from them
        # This ensures TIME_SLOTS changes are reflected correctly
        recalculated_slots = {}
        
        for day, intervals in t.available_slots.items():
            # Get check_in/check_out times for this day
            # They can be either a single string or a list of strings (for multiple intervals per day)
            day_check_ins = check_in_hours.get(day, [])
            day_check_outs = check_out_hours.get(day, [])
            
            # Ensure they are lists
            if isinstance(day_check_ins, str):
                day_check_ins = [day_check_ins] if day_check_ins else []
            if isinstance(day_check_outs, str):
                day_check_outs = [day_check_outs] if day_check_outs else []
            
            # Recalculate lessons from real hours if they exist
            if day_check_ins and day_check_outs:
                for idx in range(min(len(day_check_ins), len(day_check_outs))):
                    checkin_str = day_check_ins[idx]
                    checkout_str = day_check_outs[idx]
                    
                    if checkin_str and checkout_str and ":" in checkin_str and ":" in checkout_str:
                        try:
                            # Convert check in/out times to lesson numbers using current TIME_SLOTS
                            checkin_h, checkin_m = map(int, checkin_str.split(":"))
                            checkout_h, checkout_m = map(int, checkout_str.split(":"))
                            checkin_minutes = checkin_h * 60 + checkin_m
                            checkout_minutes = checkout_h * 60 + checkout_m
                            
                            if checkout_minutes > checkin_minutes:
                                first_lesson = None
                                last_lesson = None
                                
                                # Find which lessons are covered by this time range
                                for lesson_num in sorted(consts.TIME_SLOTS.keys()):
                                    time_range = consts.TIME_SLOTS[lesson_num]
                                    if "-" not in time_range:
                                        continue
                                    
                                    lesson_start, lesson_end = time_range.split("-")
                                    ls_h, ls_m = map(int, lesson_start.split(":"))
                                    le_h, le_m = map(int, lesson_end.split(":"))
                                    lesson_start_minutes = ls_h * 60 + ls_m
                                    lesson_end_minutes = le_h * 60 + le_m
                                    
                                    # Check if lesson is fully covered by check in/out time
                                    if checkin_minutes <= lesson_start_minutes and checkout_minutes >= lesson_end_minutes:
                                        if first_lesson is None:
                                            first_lesson = lesson_num
                                        last_lesson = lesson_num
                                
                                # Add recalculated interval
                                if first_lesson is not None and last_lesson is not None:
                                    recalculated_slots.setdefault(day, []).append((first_lesson, last_lesson))
                        except (ValueError, AttributeError):
                            # If conversion fails, use original interval
                            if idx < len(intervals):
                                recalculated_slots.setdefault(day, []).append(intervals[idx])
                    else:
                        # No valid check_in/check_out, use original interval
                        if idx < len(intervals):
                            recalculated_slots.setdefault(day, []).append(intervals[idx])
            else:
                # No check_in/check_out for this day, use original intervals
                recalculated_slots[day] = intervals
        
        # Use recalculated slots for display
        display_slots = recalculated_slots if recalculated_slots else t.available_slots
        
        for day, intervals in display_slots.items():
            # Get check_in/check_out times for display in Teacher Weekly Hours column
            day_check_ins = check_in_hours.get(day, [])
            day_check_outs = check_out_hours.get(day, [])
            
            # Ensure they are lists
            if isinstance(day_check_ins, str):
                day_check_ins = [day_check_ins] if day_check_ins else []
            if isinstance(day_check_outs, str):
                day_check_outs = [day_check_outs] if day_check_outs else []
            
            for idx, (s, e) in enumerate(intervals):
                # Calculate time slots for display using CURRENT TIME_SLOTS
                time_start = consts.TIME_SLOTS.get(s, "").split("-")[0]
                time_end = consts.TIME_SLOTS.get(e, "").split("-")[1] if "-" in consts.TIME_SLOTS.get(e, "") else ""
                timeslots = f"{time_start}-{time_end}" if time_start and time_end else ""
                
                # Get corresponding check_in/check_out for THIS specific interval
                check_in = day_check_ins[idx] if idx < len(day_check_ins) else ""
                check_out = day_check_outs[idx] if idx < len(day_check_outs) else ""
                real_hours_display = f"{check_in}-{check_out}" if (check_in and check_out) else ""
                
                # If no Teacher Weekly Hours, copy from timeslots
                if not real_hours_display and timeslots:
                    real_hours_display = timeslots
                
                # Show Real Hours for each specific interval
                avail_tree.insert("", "end", values=(day, f"{s}-{e}", timeslots, real_hours_display))

    def submit():
        name = name_e.get().strip()
        if not name:
            messagebox.showerror(GUI_TEXT[95], GUI_TEXT[84])  # "Error", "Name"
            return
        items = []
        for i in range(selected_lb.size()):
            entry = selected_lb.get(i)
            parts = entry.split(":", 2)
            nm = parts[0].strip()
            hrs = int(parts[1]) if len(parts) >= 2 and parts[1].isdigit() else 0
            grp = parts[2].strip() if len(parts) >= 3 else ""
            items.append({"name": nm, "hours": hrs, "group": grp})
        
        # Extract intervals and real hours from treeview
        intervals = {}
        check_in_hours = {}
        check_out_hours = {}
        
        # First pass: collect all intervals and real hours
        for item_id in avail_tree.get_children():
            values = avail_tree.item(item_id)["values"]
            day = values[0]
            lessons_str = values[1]  # Format: "1-7"
            real_hours_str = str(values[3]).strip()  # Format: "08:00-16:00" or empty
            
            start, end = map(int, lessons_str.split("-"))
            intervals.setdefault(day, []).append((start, end))
            
            # Parse real hours if present (format: "HH:MM-HH:MM")
            # Store as LIST to support multiple intervals per day
            if real_hours_str and "-" in real_hours_str and ":" in real_hours_str:
                try:
                    check_in, check_out = real_hours_str.split("-", 1)
                    # Initialize lists if not exists
                    if day not in check_in_hours:
                        check_in_hours[day] = []
                    if day not in check_out_hours:
                        check_out_hours[day] = []
                    # Append to lists (one entry per interval)
                    check_in_hours[day].append(check_in.strip())
                    check_out_hours[day].append(check_out.strip())
                except ValueError:
                    pass  # Not a valid time range, skip
        
        t.name = name
        t.subjects = items
        t.total_hours = sum(s["hours"] for s in t.subjects)
        t.available_slots = intervals
        t.check_in_hours = check_in_hours
        t.check_out_hours = check_out_hours
        
        items_save = [
            {
                "name": x.name,
                "subjects": x.subjects,
                "available_slots": getattr(x, "available_slots", {}),
                "check_in_hours": getattr(x, "check_in_hours", {}),
                "check_out_hours": getattr(x, "check_out_hours", {})
            }
            for x in app.teachers
        ]
        
        json_io.write_save_json(os.path.join(consts.DATA_DIR, "teachers.json"), "teachers", items_save)
        app.reload_all()
        popup.destroy()

    save_btn = tk.Button(popup_parent, text=GUI_TEXT[138], command=submit, font=("Arial", 13, "bold"))  # "Save Changes"
    save_btn.grid(row=11, column=0, columnspan=4, pady=8)


def delete_selected_teacher(app):
    sel = app.teachers_tree.selection()
    if not sel:
        messagebox.showerror(GUI_TEXT[95], GUI_TEXT[99])  # "Error", "Select a teacher to delete"
        return
    vals = app.teachers_tree.item(sel[0], "values")
    name = vals[0]
    if not messagebox.askyesno(GUI_TEXT[97], GUI_TEXT[98].format(name=name)):  # "Confirm", "Delete teacher '{name}'?"
        return
    for i, x in enumerate(app.teachers):
        if x.name == name:
            del app.teachers[i]
            break
    items = [
        {
            "name": x.name,
            "subjects": x.subjects,
            "available_slots": getattr(x, "available_slots", {}),
            "check_in_hours": getattr(x, "check_in_hours", {}),
            "check_out_hours": getattr(x, "check_out_hours", {})
        }
        for x in app.teachers
    ]
    json_io.write_save_json(os.path.join(consts.DATA_DIR, "teachers.json"), "teachers", items)
    app.reload_all()


def on_teacher_selected(app):
    """Select teacher and update availability grid."""
    name = app.teacher_var.get()
    t = next((x for x in app.teachers if x.name == name), None)

    teacher_subject_names = []
    if t:
        teacher_subject_names = [s['name'] for s in t.subjects]
    if not teacher_subject_names:
        teacher_subject_names = [s.name for s in app.subjects]

    app.update_combobox_values(app.teacher_cells, teacher_subject_names)

    # Load teacher's schedule from regenerated data (now includes all teachers for shared subjects)
    data = app.schedules.get('teachers', {}).get(name, {})
    
    app.data_to_grid(app.teacher_cells, data)




    

    # --- set availability ---
    def set_teacher_cells_availability(teacher_obj):
        day_index = {i + 1: d for i, d in enumerate(consts.WEEKDAYS)}
        if teacher_obj:
            avail_choices = [""] + [s['name'] for s in teacher_obj.subjects] or [""]
        else:
            avail_choices = [""] + [s.name for s in app.subjects]

        for (r, c), cb in app.teacher_cells.items():
            day = day_index.get(c)
            lesson = r
            available = True
            if teacher_obj:
                if not getattr(teacher_obj, "available_slots", None) or not teacher_obj.is_available(day, lesson):
                    available = False

            if available:
                cb.config(state="readonly")
                cb["values"] = avail_choices
                if cb.get() == "(unavailable)":
                    cb.set("")
            else:
                cb.config(state="disabled")
                cb["values"] = ["(unavailable)"]
                cb.set(consts.unavailable_slot)

            color_cb_by_content(cb)
            cb.bind("<<ComboboxSelected>>", lambda e, cb=cb: color_cb_by_content(cb))

    # apply availability
    set_teacher_cells_availability(t)

    # lock editing after load
    for cb in app.teacher_cells.values():
        try:
            cb.config(state="disabled")
        except Exception:
            pass

# import remaining handlers
from school_scheduler.ui.ui_handlers_additional import *
