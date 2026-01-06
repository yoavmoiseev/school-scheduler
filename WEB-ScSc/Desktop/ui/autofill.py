import random
from tkinter import messagebox
from school_scheduler.helpers import data_utils
from school_scheduler.helpers.ui_helpers import color_cb_by_content
import school_scheduler.data.consts as consts
from school_scheduler.ui.teacher_busy_map import *  # normalize_day, build_teacher_busy_map etc.
from .translations import *

MAX_ATTEMPTS = consts.max_autofill_retries  # Maximum number of autofill retry attempts

def autofill_group(app, group_name, cells_map, subjects_list, teachers_list,
                   max_sequence_lessons=consts.max_sequence_lessons,
                   max_per_day=consts.max_per_day, direction=autofill_direction, _attempt=1, ):
    """
    Autofill schedule for a group with retries.

    - Completely clears and recreates the group's schedule if not all lessons could be placed.
    - direction: "Left_to_Right" or "Right_to_Left"
    - max_sequence_lessons: maximum number of consecutive lessons of the same subject
    - max_per_day: maximum lessons of the same subject per day
    - Retries up to MAX_ATTEMPTS if not all hours can be scheduled
    """

    # Print only on first attempt for clarity in logs
    if _attempt == 1:
        print(f"\n=== Starting autofill for group '{group_name}' ===")

    # Error check: group must be selected
    if not group_name:
        messagebox.showerror(GUI_TEXT[43], [GUI_TEXT[43]])  # Group must be selected
        return

    # Filter subjects relevant to the selected group
    group_subjects = [s for s in subjects_list if getattr(s, 'group', '') == group_name]
    if not group_subjects:
        messagebox.showinfo(GUI_TEXT[44], [f"{GUI_TEXT[44]} '{group_name}'"])
        return

    # --- Compute target hours per subject ---
    target = {}
    for subj in group_subjects:
        name = subj.name

        # Calculate teacher-related totals and count how many distinct teachers can teach this subject
        teacher_hours_total = 0
        teacher_count = 0
        seen_teacher_names = set()
        for t in teachers_list:
            for se in getattr(t, "subjects", []):
                if not isinstance(se, dict):
                    continue
                se_name = se.get("name")
                se_group = se.get("group", "") or ""
                try:
                    se_hours = int(se.get("hours", 0))
                except Exception:
                    se_hours = 0
                if se_name == name and (se_group == group_name or se_group == ""):
                    if t.name not in seen_teacher_names:
                        seen_teacher_names.add(t.name)
                        teacher_count += 1
                    teacher_hours_total += max(0, se_hours)

        # If subject is assigned to >1 teacher, prefer subject.hours_per_week as total (if provided),
        # otherwise fall back to teacher_hours_total. This implements "5 hours total for the subject"
        if teacher_count > 1:
            subj_defined_hours = int(getattr(subj, "hours_per_week", 0) or 0)
            if subj_defined_hours > 0:
                total = subj_defined_hours
            else:
                # fallback (unlikely) to summed teacher hours
                total = teacher_hours_total
        else:
            # original behavior: sum teacher hours; fallback to subj.hours_per_week if none declared
            total = teacher_hours_total
            if total <= 0:
                total = int(getattr(subj, "hours_per_week", 0) or 0)

        target[name] = max(0, total)

    # --- Determine already assigned hours ---
    assigned = count_subject_assignments(app.grid_to_data(cells_map))
    remaining = {name: max(0, target.get(name, 0) - assigned.get(name, 0)) for name in target}

    # Load existing schedules to check teacher availability
    existing_schedule = data_utils.load_schedules()
    teacher_busy = build_teacher_busy_map(existing_schedule, teachers_list)

    teacher_avail = {}  # Available slots per teacher
    subj_teachers = {name: [] for name in target.keys()}  # teachers per subject

    # --- Build teacher availability maps ---
    for t in teachers_list:
        subj_hours = {}
        for se in getattr(t, "subjects", []):
            if not isinstance(se, dict):
                continue
            nm = se.get("name")
            grp = se.get("group", "") or ""
            try:
                hrs = int(se.get("hours", 0))
            except Exception:
                hrs = 0
            if nm in subj_teachers and (grp == group_name or grp == "") and hrs > 0:
                subj_hours[nm] = subj_hours.get(nm, 0) + max(0, hrs)
        if not subj_hours:
            continue

        slots = set()
        if getattr(t, "available_slots", None):
            for day, intervals in (t.available_slots or {}).items():
                for s_int in intervals:
                    try:
                        start, end = s_int[0], s_int[1]
                        for l in range(start, end + 1):
                            if (day, l) not in teacher_busy.get(t.name, set()):
                                slots.add((day, l))
                    except Exception:
                        continue
        if not slots:
            continue
        teacher_avail[t.name] = {"slots": slots, "teacher_obj": t, "subj_hours": subj_hours}
        for nm in subj_hours:
            subj_teachers[nm].append(t.name)

    # --- Count subject instances per day ---
    day_index = {i + 1: d for i, d in enumerate(consts.WEEKDAYS)}
    day_counts = {}
    for (r, c), cb in cells_map.items():
        val = (cb.get() or "").strip()
        if not val:
            continue
        day = normalize_day(c, day_index)
        if not day:
            continue
        day_counts[(day, val)] = day_counts.get((day, val), 0) + 1

    # --- Function to check available teachers for a subject ---
    def teachers_available_for(subject_name, day, lesson, require_hours=True):
        """
        Returns:
         - For single-teacher subjects: list of available teacher names (like before)
         - For multi-teacher subjects: list of ALL assigned teachers if ALL of them are free in this slot
           and (if require_hours) the sum of their subj_hours for this subject > 0.
           Otherwise returns [].
        """
        assigned = subj_teachers.get(subject_name, [])
        if not assigned:
            return []

        # Single teacher or effectively single -> keep old behavior
        if len(assigned) == 1:
            out = []
            tn = assigned[0]
            info = teacher_avail.get(tn)
            if not info:
                return []
            if (day, lesson) not in info["slots"]:
                return []
            if require_hours and info["subj_hours"].get(subject_name, 0) <= 0:
                return []
            out.append(tn)
            return out

        # Multi-teacher subject: require that ALL assigned teachers are free at (day,lesson)
        total_hours_across_teachers = 0
        for tn in assigned:
            info = teacher_avail.get(tn)
            if not info:
                return []  # a required teacher has no availability map -> cannot place
            if (day, lesson) not in info["slots"]:
                return []  # this teacher not free in that slot -> slot invalid
            total_hours_across_teachers += info["subj_hours"].get(subject_name, 0)

        if require_hours and total_hours_across_teachers <= 0:
            return []

        # return the full assigned list (they are all available in this slot)
        return list(assigned)

    empties = [(r, c) for (r, c), cb in cells_map.items() if not cb.get().strip()]
    if not empties:
        return

    rows = sorted(set(r for r, _ in empties))
    cols = sorted(set(c for _, c in empties))
    if direction == "Right_to_Left":
        cols = list(reversed(cols))

    ordered = []
    for r in rows:
        for c in cols:
            if (r, c) in empties:
                ordered.append((r, c))

    # --- Helper functions for placement checks ---
    def contiguous_length_if_placed(subject, row, col):
        length = 1
        r_up = row - 1
        while True:
            cb = cells_map.get((r_up, col))
            if not cb:
                break
            val = (cb.get() or "").strip()
            if val != subject:
                break
            length += 1
            r_up -= 1
        r_down = row + 1
        while True:
            cb = cells_map.get((r_down, col))
            if not cb:
                break
            val = (cb.get() or "").strip()
            if val != subject:
                break
            length += 1
            r_down += 1
        return length

    def can_place_single(subject, row, col, day):
        if cells_map[(row, col)].get().strip():
            return False
        if day_counts.get((day, subject), 0) + 1 > max_per_day:
            return False
        if contiguous_length_if_placed(subject, row, col) > max_sequence_lessons:
            return False
        if not teachers_available_for(subject, day, int(row), True):
            return False
        return True

    def can_place_pair(subject, row, col, day):
        pair_row = row + 1
        if (pair_row, col) not in cells_map:
            return False
        if cells_map[(row, col)].get().strip() or cells_map[(pair_row, col)].get().strip():
            return False
        if day_counts.get((day, subject), 0) + 2 > max_per_day:
            return False
        if contiguous_length_if_placed(subject, row, col) > max_sequence_lessons:
            return False
        if contiguous_length_if_placed(subject, pair_row, col) > max_sequence_lessons:
            return False
        if not teachers_available_for(subject, day, int(row), True):
            return False
        if not teachers_available_for(subject, day, int(pair_row), True):
            return False
        return True

    def place_choice_in(subject, row, col):
        # Get available teachers for this subject+slot
        avail_teachers = teachers_available_for(subject, normalize_day(col, day_index), int(row), True)
        if not avail_teachers:
            return False

        # If single teacher — keep existing behavior (choose among available teachers heuristically)
        if len(avail_teachers) == 1:
            avail_teachers.sort(key=lambda tn: teacher_avail[tn]["subj_hours"].get(subject, 0), reverse=True)
            chosen_teacher = random.choice(avail_teachers[:max(1, min(3, len(avail_teachers)))])
            try:
                teacher_avail[chosen_teacher]["slots"].remove((normalize_day(col, day_index), int(row)))
            except Exception:
                pass
            teacher_avail[chosen_teacher]["subj_hours"][subject] = max(
                0, teacher_avail[chosen_teacher]["subj_hours"].get(subject, 0) - 1
            )

        else:
            # Multi-teacher subject: avail_teachers contains ALL assigned teachers and all are free in this slot.
            # We must reserve the slot for ALL these teachers (remove it from each teacher's slots).
            # For decrementing subj_hours, pick the teacher with the most remaining subj_hours for this subject.
            # (We decrement only one teacher's subj_hours because total subject-hours are tracked by `remaining`.)
            avail_teachers.sort(key=lambda tn: teacher_avail[tn]["subj_hours"].get(subject, 0), reverse=True)
            chosen_teacher = avail_teachers[0]  # primary to decrement

            # remove slot from all teachers so that slot is no longer available for them
            for tn in avail_teachers:
                try:
                    teacher_avail[tn]["slots"].remove((normalize_day(col, day_index), int(row)))
                except Exception:
                    pass

            # decrement subj_hours only on chosen_teacher (keeps bookkeeping simple)
            teacher_avail[chosen_teacher]["subj_hours"][subject] = max(
                0, teacher_avail[chosen_teacher]["subj_hours"].get(subject, 0) - 1
            )

        # Place subject text into cell as before
        cells_map[(row, col)].set(subject)
        remaining[subject] = max(0, remaining.get(subject, 0) - 1)
        day = normalize_day(col, day_index)
        day_counts[(day, subject)] = day_counts.get((day, subject), 0) + 1
        color_cb_by_content(cells_map[(row, col)])
        return True

    # === Main autofill loop ===
    for (r, c) in ordered:
        if cells_map[(r, c)].get().strip():
            continue
        day = normalize_day(c, day_index)
        if not day:
            continue
        lesson = int(r)

        above_cb = cells_map.get((r - 1, c))
        above_val = (above_cb.get() or "").strip() if above_cb else ""
        if above_val:
            subj = above_val
            if remaining.get(subj, 0) > 0 and day_counts.get((day, subj), 0) < max_per_day:
                if can_place_single(subj, r, c, day):
                    place_choice_in(subj, r, c)
                    continue

        candidates = [name for name, rem in remaining.items()
                      if rem > 0 and day_counts.get((day, name), 0) < max_per_day
                      and teachers_available_for(name, day, lesson, True)]
        if not candidates:
            continue

        candidates.sort(key=lambda n: remaining.get(n, 0), reverse=True)
        choice = random.choice(candidates) if len(candidates) > 1 else candidates[0]

        if max_sequence_lessons >= 2 and can_place_pair(choice, r, c, day):
            placed1 = place_choice_in(choice, r, c)
            if placed1:
                place_choice_in(choice, r + 1, c)
            continue

        if can_place_single(choice, r, c, day):
            place_choice_in(choice, r, c)
            continue

    # --- Check for incomplete subjects ---
    not_full = []
    for subj_name, total_needed in target.items():
        total_inserted = total_needed - remaining.get(subj_name, 0)
        if total_inserted < total_needed:
            diff = total_needed - total_inserted
            print(f"[Warning] '{subj_name}': inserted {total_inserted} of {total_needed} (missing {diff})")
            not_full.append(subj_name)

    # --- Autofill retry logic ---
    if not_full and _attempt < MAX_ATTEMPTS:
        print(f"⚠️  Attempt {_attempt} failed. Clearing group and retrying ({_attempt + 1}/{MAX_ATTEMPTS})...")
        for (r, c), cb in cells_map.items():
            if cb.get().strip():
                cb.set("")  # clear all slots for this group
        autofill_group(app, group_name, cells_map, subjects_list, teachers_list,
                       max_sequence_lessons, max_per_day, direction, _attempt=_attempt + 1)
        return

    if not_full and _attempt >= MAX_ATTEMPTS:
        messagebox.showerror(GUI_TEXT[46], [f"{GUI_TEXT[46]}: {', '.join(not_full)}"])
    elif not not_full:
        print(f"✅ Group '{group_name}' successfully filled in {_attempt} attempts.\n")
        # optional info message
        # messagebox.showinfo(GUI_TEXT[47], [GUI_TEXT[47]])

    # --- Final update of colors ---
    for cb in cells_map.values():
        color_cb_by_content(cb)
