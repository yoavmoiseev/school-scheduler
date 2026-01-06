import tkinter as tk
from tkinter import ttk

import school_scheduler.data.consts as consts
from .popups import add_teacher_popup, add_group_popup, add_subject_popup
from .buttons_functions import *
from .translations import *
from .build_config_tab import build_config_tab



def build_ui(app):
    """Construct UI and attach widgets to the passed app instance."""

    # ===== Top buttons =====
    top_frame = tk.Frame(app.root)
    top_frame.pack(fill=tk.X, padx=8, pady=6)
    btn_frame = tk.Frame(top_frame)
    btn_frame.pack(side=tk.LEFT)

    group1 = tk.Frame(btn_frame)
    group1.pack(side=tk.LEFT)
    tk.Button(group1, text=GUI_TEXT[0], command=lambda: add_teacher_popup(app.root, app.reload_all)).pack(side=tk.LEFT, padx=6)
    tk.Button(group1, text=GUI_TEXT[1], command=lambda: add_group_popup(app.root, app.reload_all)).pack(side=tk.LEFT, padx=6)
    tk.Button(group1, text=GUI_TEXT[2], command=lambda: add_subject_popup(app.root, app.reload_all)).pack(side=tk.LEFT, padx=6)

    group2 = tk.Frame(btn_frame)
    group2.pack(side=tk.LEFT, padx=100)  # some space between groups
    tk.Button(group2, text=GUI_TEXT[121], command=load_snapshot).pack(side=tk.LEFT, padx=6) # Load
    tk.Button(group2, text=GUI_TEXT[122], command=save_as_snapshot).pack(side=tk.LEFT, padx=6) # Save As

    tk.Button(group2, text=GUI_TEXT[4], command=lambda: rebuild_all_schedule(app)).pack(side=tk.LEFT, padx=50)
    
    # Excel import/export buttons
    group3 = tk.Frame(btn_frame)
    group3.pack(side=tk.LEFT, padx=50)
    tk.Button(group3, text=GUI_TEXT[147], command=lambda: export_to_excel(app)).pack(side=tk.LEFT, padx=6)  # Export to Excel
    tk.Button(group3, text=GUI_TEXT[148], command=lambda: load_from_excel(app)).pack(side=tk.LEFT, padx=6)  # Load from Excel
    
    # Clear buttons
    group4 = tk.Frame(btn_frame)
    group4.pack(side=tk.LEFT, padx=50)
    tk.Button(group4, text=GUI_TEXT[141], command=lambda: clear_schedulers(app)).pack(side=tk.LEFT, padx=6)  # Clear Schedulers
    tk.Button(group4, text=GUI_TEXT[142], command=lambda: clear_all_data(app)).pack(side=tk.LEFT, padx=6)  # Clear All Data


    # ===== Tabs =====
    app.notebook = ttk.Notebook(app.root)

    tab_teachers = tk.Frame(app.notebook)
    tab_groups = tk.Frame(app.notebook)
    tab_subjects = tk.Frame(app.notebook)

    tab_empty_schedule = tk.Frame(app.notebook)
    tab_group_schedule = tk.Frame(app.notebook)
    tab_teacher_schedule = tk.Frame(app.notebook)
    tab_schedule = tk.Frame(app.notebook)
    
    tab_empty_general = tk.Frame(app.notebook)
    tab_general = tk.Frame(app.notebook)

    app.notebook.add(tab_teachers, text=GUI_TEXT[5])  # Teachers
    app.notebook.add(tab_groups, text=GUI_TEXT[6])    # Groups
    app.notebook.add(tab_subjects, text=GUI_TEXT[7])  # Subjects

    app.notebook.add(tab_empty_schedule, text= "                               \
                      ",state = 'disabled') # Add emty space before 3 Schedulers Tabs

    app.notebook.add(tab_schedule, text=GUI_TEXT[8])  # Day view
    app.notebook.add(tab_group_schedule, text=GUI_TEXT[9])  # Group Scheduler
    app.notebook.add(tab_teacher_schedule, text=GUI_TEXT[10])  # Teacher Scheduler

    # Add emty space before Config Tab
    app.notebook.add(tab_empty_general, text= "                               \
                      ",state = 'disabled') # Add emty space before Config Tab
    
    app.notebook.add(tab_general, text=GUI_TEXT[102]) # General Configuration

    # ===== General Configuration tab =====
    build_config_tab(app, tab_general)
    app.notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))



    # ===== Teachers Tree =====
    app.teachers_tree = ttk.Treeview(tab_teachers, columns=("Name", "Subjects", "TotalHours"), show="headings")
    
    app.teachers_tree.heading("Name", text=GUI_TEXT[15])       # Name
    app.teachers_tree.column("Name", stretch=False, anchor='w')
    
    app.teachers_tree.heading("Subjects", text=GUI_TEXT[16])   # Subjects (name : hours : group;)
    app.teachers_tree.column("Subjects", stretch=True, anchor='w')

    app.teachers_tree.heading("TotalHours", text=GUI_TEXT[158]) # Assigned/Available
    app.teachers_tree.column("TotalHours", stretch=False, anchor='e')
    
    app.teachers_tree.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

    tch_btn_frame = tk.Frame(tab_teachers)
    tch_btn_frame.pack(fill=tk.X, padx=6, pady=(0, 6))
    tk.Button(tch_btn_frame, text=GUI_TEXT[18], command=lambda: app.edit_selected_teacher()).pack(side=tk.LEFT, padx=6)  # Edit Selected
    tk.Button(tch_btn_frame, text=GUI_TEXT[19], command=lambda: app.delete_selected_teacher()).pack(side=tk.LEFT, padx=6)  # Delete Selected
    tk.Button(tch_btn_frame, text=GUI_TEXT[127], command=lambda: app.move_teacher_up()).pack(side=tk.LEFT, padx=6)  # Move Up
    tk.Button(tch_btn_frame, text=GUI_TEXT[128], command=lambda: app.move_teacher_down()).pack(side=tk.LEFT, padx=6)  # Move Down

    # ===== Groups Tree =====
    app.groups_tree = ttk.Treeview(tab_groups, columns=("Name", "Comment", "TotalHours"), show="headings")
    app.groups_tree.heading("Name", text=GUI_TEXT[20])
    app.groups_tree.heading("Comment", text=GUI_TEXT[196])  # "Comment"
    app.groups_tree.heading("TotalHours", text=GUI_TEXT[160])  # "Total Hours Per Group"
    app.groups_tree.column("Name", width=150)
    app.groups_tree.column("Comment", width=200)
    app.groups_tree.column("TotalHours", width=150)
    app.groups_tree.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

    grp_btn_frame = tk.Frame(tab_groups)
    grp_btn_frame.pack(fill=tk.X, padx=6, pady=(0, 6))
    tk.Button(grp_btn_frame, text=GUI_TEXT[24], command=lambda: app.edit_selected_group()).pack(side=tk.LEFT, padx=6)  # Edit Selected
    tk.Button(grp_btn_frame, text=GUI_TEXT[25], command=lambda: app.delete_selected_group()).pack(side=tk.LEFT, padx=6)  # Delete Selected
    tk.Button(grp_btn_frame, text=GUI_TEXT[127], command=lambda: app.move_group_up()).pack(side=tk.LEFT, padx=6)  # Move Up
    tk.Button(grp_btn_frame, text=GUI_TEXT[128], command=lambda: app.move_group_down()).pack(side=tk.LEFT, padx=6)  # Move Down

    # ===== Subjects Tree =====
    app.subjects_tree = ttk.Treeview(tab_subjects, columns=("Name", "Hours", "Group"), show="headings")
    app.subjects_tree.heading("Name", text=GUI_TEXT[29])   # Name
    app.subjects_tree.heading("Hours", text=GUI_TEXT[30])  # Hours/week
    app.subjects_tree.heading("Group", text=GUI_TEXT[31])  # Group
    app.subjects_tree.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

    sub_btn_frame = tk.Frame(tab_subjects)
    sub_btn_frame.pack(fill=tk.X, padx=6, pady=(0, 6))
    tk.Button(sub_btn_frame, text=GUI_TEXT[32], command=lambda: app.edit_selected_subject()).pack(side=tk.LEFT, padx=6)  # Edit Selected
    tk.Button(sub_btn_frame, text=GUI_TEXT[33], command=lambda: app.delete_selected_subject()).pack(side=tk.LEFT, padx=6)  # Delete Selected
    tk.Button(sub_btn_frame, text=GUI_TEXT[127], command=lambda: app.move_subject_up()).pack(side=tk.LEFT, padx=6)  # Move Up
    tk.Button(sub_btn_frame, text=GUI_TEXT[128], command=lambda: app.move_subject_down()).pack(side=tk.LEFT, padx=6)  # Move Down

    # ===== Day View =====
    dv_ctrl = tk.Frame(tab_schedule)
    dv_ctrl.pack(fill=tk.X, padx=6, pady=4)
    tk.Label(dv_ctrl, text=GUI_TEXT[34]).pack(side=tk.LEFT)  # Select day

    day_cb = ttk.Combobox(dv_ctrl, textvariable=app.day_var, values=consts.WEEKDAYS, state="readonly", width=20)
    day_cb.pack(side=tk.LEFT, padx=6)
    day_cb.bind("<<ComboboxSelected>>", lambda e=None: app.on_day_selected())

    app.table_frame = tk.Frame(tab_schedule, bd=2, relief="groove")
    app.table_frame.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

    day_view_buttons = tk.Frame(tab_schedule)
    day_view_buttons.pack(fill=tk.X, padx=6, pady=4)
    tk.Button(day_view_buttons, text=GUI_TEXT[35], command=lambda: print_to_pdf(tab_schedule, name=app.day_var.get())).pack(side=tk.LEFT, padx=120)  # Print to PDF

    # ===== Group Scheduler =====
    grp_ctrl = tk.Frame(tab_group_schedule)
    grp_ctrl.pack(fill=tk.X, padx=6, pady=6)
    tk.Label(grp_ctrl, text=GUI_TEXT[36]).pack(side=tk.LEFT)  # Select group

    app.group_cb = ttk.Combobox(grp_ctrl, textvariable=app.group_var, state="readonly", width=40)
    app.group_cb.pack(side=tk.LEFT, padx=6)
    app.group_cb.bind("<<ComboboxSelected>>", lambda e=None: app.on_group_selected())

    app.grp_table = tk.Frame(tab_group_schedule, bd=2, relief="groove")
    app.grp_table.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

    tk.Label(app.grp_table, text="", borderwidth=1, relief="solid", width=8, height=2, bg="#ddd").grid(row=0, column=0, sticky="nsew")
    for c, day in enumerate(consts.WEEKDAYS, start=1):
        tk.Label(app.grp_table, text=day, borderwidth=1, relief="solid", width=18, height=2, bg="#ddd").grid(row=0, column=c, sticky="nsew")

    app.group_cells = {}
    for r, lesson in enumerate(consts.LESSONS, start=1):
        app.create_lessons_lable(app.grp_table, lesson, r)
        for c, day in enumerate(consts.WEEKDAYS, start=1):
            cb = ttk.Combobox(app.grp_table, values=[""], state="readonly", width=18, justify="center")
            cb.grid(row=r, column=c, sticky="nsew", padx=1, pady=1)
            app.group_cells[(r, c)] = cb

    for c in range(len(consts.WEEKDAYS) + 1):
        app.grp_table.grid_columnconfigure(c, weight=1)
    for r in range(len(consts.LESSONS) + 1):
        app.grp_table.grid_rowconfigure(r, weight=1)

    grp_buttons = tk.Frame(tab_group_schedule)
    grp_buttons.pack(fill=tk.X, padx=6, pady=4)
    tk.Button(grp_buttons, text=GUI_TEXT[37], command=lambda: app.clear_cells(app.group_cells)).pack(side=tk.LEFT, padx=4)  # Clear
    tk.Button(grp_buttons, text=GUI_TEXT[38], command=lambda: app.autofill_group(app.group_var.get(), \
        app.group_cells, app.subjects, app.teachers, _attempt=consts.max_autofill_retries))\
            .pack(side=tk.LEFT, padx=4)  # Auto-fill for group
    tk.Button(grp_buttons, text=GUI_TEXT[39], command=lambda: app.save_group_schedule(app.group_var.get(),app.group_cells)).pack(side=tk.LEFT, padx=4)  # Save Group Schedule
    tk.Button(grp_buttons, text=GUI_TEXT[40], command=lambda: print_to_pdf(tab_group_schedule, name=app.group_var.get())).pack(side=tk.LEFT, padx=80)  # Print to PDF

    # ===== Teacher Scheduler =====
    tch_ctrl = tk.Frame(tab_teacher_schedule)
    tch_ctrl.pack(fill=tk.X, padx=6, pady=6)
    tk.Label(tch_ctrl, text=GUI_TEXT[41]).pack(side=tk.LEFT)  # Select teacher

    app.teacher_cb = ttk.Combobox(tch_ctrl, textvariable=app.teacher_var, state="readonly", width=40)
    app.teacher_cb.pack(side=tk.LEFT, padx=6)
    app.teacher_cb.bind("<<ComboboxSelected>>", lambda e=None: app.on_teacher_selected())

    app.tch_table = tk.Frame(tab_teacher_schedule, bd=2, relief="groove")
    app.tch_table.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

    tk.Label(app.tch_table, text="", borderwidth=1, relief="solid", width=8, height=2, bg="#ddd").grid(row=0, column=0, sticky="nsew")
    for c, day in enumerate(consts.WEEKDAYS, start=1):
        tk.Label(app.tch_table, text=day, borderwidth=1, relief="solid", width=18, height=2, bg="#ddd").grid(row=0, column=c, sticky="nsew")

    app.teacher_cells = {}
    for r, lesson in enumerate(consts.LESSONS, start=1):
        app.create_lessons_lable(app.tch_table, lesson, r)
        for c, day in enumerate(consts.WEEKDAYS, start=1):
            cb = ttk.Combobox(app.tch_table, values=[""], state="readonly", width=18, justify="center")
            cb.grid(row=r, column=c, sticky="nsew", padx=1, pady=1)
            app.teacher_cells[(r, c)] = cb

    for c in range(len(consts.WEEKDAYS) + 1):
        app.tch_table.grid_columnconfigure(c, weight=1)
    for r in range(len(consts.LESSONS) + 1):
        app.tch_table.grid_rowconfigure(r, weight=1)

    tch_buttons = tk.Frame(tab_teacher_schedule)
    tch_buttons.pack(fill=tk.X, padx=6, pady=4)
    tk.Button(tch_buttons, text=GUI_TEXT[42], command=lambda: print_to_pdf(tab_teacher_schedule, app.teacher_var.get())).pack(side=tk.LEFT, padx=120)  # Print to PDF
