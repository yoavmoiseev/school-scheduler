import random
import os
from datetime import datetime


class AutofillService:
    def __init__(self, excel_service, conflict_checker, color_service):
        self.excel = excel_service
        self.checker = conflict_checker
        self.color_service = color_service
    
    def autofill_group(self, group_name, max_retries=100):
        """
        Autofill schedule for a group.
        Returns: (success: bool, schedule: dict, errors: list)
        """
        config = self.excel.get_config()
        teachers = self.excel.get_teachers()
        subjects = self.excel.get_subjects()
        
        weekdays = config.get('WEEKDAYS', 'Monday,Tuesday,Wednesday,Thursday,Friday').split(',')
        weekdays = [day.strip() for day in weekdays]  # Remove whitespace
        lessons_count = int(config.get('lessons', 8))
        lessons = list(range(1, lessons_count + 1))
        
        max_sequence = int(config.get('max_sequence_lessons', 2))
        max_per_day = int(config.get('max_per_day', 3))
        autofill_direction = config.get('autofill_direction', 'forward')

        # (diagnostic log removed)

        # helper to append detailed debug lines
        def _log_detail(msg):
            try:
                with open(os.path.join('uploads', 'autofill_debug.log'), 'a', encoding='utf-8') as lf:
                    lf.write(f"{datetime.now().isoformat()} | autofill_detail | group={group_name} | {msg}\n")
            except Exception:
                pass

        # Log start of autofill for this group
        try:
            os.makedirs('uploads', exist_ok=True)
            with open(os.path.join('uploads', 'autofill_debug.log'), 'a', encoding='utf-8') as lf:
                lf.write(f"{datetime.now().isoformat()} | autofill_start | group={group_name}\n")
        except Exception:
            pass
        
        # Prepare containers
        errors = []
        incomplete = []
        # Filter subjects for this group
        group_subjects = [s for s in subjects if s['group'] == group_name]

        # Initialize schedule
        schedule = {}
        for day in weekdays:
            schedule[day] = {}

        if not group_subjects:
            errors.append(f"No subjects found for group '{group_name}'")
            return False, schedule, errors
        
        # Build teacher busy map from existing schedules (excluding current group)
        existing_schedules = self.excel.get_group_schedules()
        if group_name in existing_schedules:
            del existing_schedules[group_name]  # Don't count current group
        
        busy_map = self.checker.build_busy_map(existing_schedules, teachers)
        
        errors = []
        
        # For each subject, try to place lessons
        for subject in group_subjects:
            subj_name = subject['name']

            # Build list of assigned teachers for this subject (matching group or empty group)
            assigned_teachers = []
            teacher_name_map = {t['name']: t for t in teachers}
            subj_teacher_hours = {}
            for t in teachers:
                for ts in t.get('subjects', []):
                    if ts.get('name') == subj_name and (ts.get('group', '') == group_name or ts.get('group', '') == ''):
                        assigned_teachers.append(t['name'])
                        try:
                            subj_teacher_hours[t['name']] = subj_teacher_hours.get(t['name'], 0) + int(ts.get('hours', 0) or 0)
                        except Exception:
                            subj_teacher_hours[t['name']] = subj_teacher_hours.get(t['name'], 0)

            if not assigned_teachers:
                errors.append(f"No teacher found for subject '{subj_name}' in group '{group_name}'")
                continue

            # Determine required lessons for this subject
            required = int(subject.get('hours_per_week', 0) or 0)
            if len(assigned_teachers) > 1:
                # if multiple teachers assigned, prefer subject hours if defined, otherwise sum teacher hours
                if required <= 0:
                    total_teacher_hours = sum(subj_teacher_hours.get(n, 0) for n in assigned_teachers)
                    required = total_teacher_hours

            placed = 0
            retries = 0

            # Create list of all possible slots
            possible_slots = []
            for day in weekdays:
                for lesson in lessons:
                    possible_slots.append((day, lesson))

            # Shuffle or reverse based on direction
            if autofill_direction == 'random':
                random.shuffle(possible_slots)
            elif autofill_direction == 'backward':
                possible_slots.reverse()

            # Local mutable subj hours map for bookkeeping
            subj_hours_remaining = dict(subj_teacher_hours)

            # Try to place lessons
            while placed < required and retries < max_retries:
                placed_this_round = False

                for day, lesson in possible_slots:
                    if placed >= required:
                        break

                    # Skip if slot already filled
                    if lesson in schedule.get(day, {}):
                        _log_detail(f"skip_filled | day={day} | lesson={lesson} | subject={subj_name}")
                        continue

                    # Check constraints
                    if not self._check_constraints(schedule, day, lesson, subj_name, max_sequence, max_per_day):
                        _log_detail(f"skip_constraints | day={day} | lesson={lesson} | subject={subj_name}")
                        continue

                    # Multi-teacher: require ALL assigned teachers be available and not busy
                    multi_ok = True
                    for tn in assigned_teachers:
                        t_obj = teacher_name_map.get(tn)
                        if not t_obj or not self._is_teacher_available(t_obj, day, lesson):
                            multi_ok = False
                            _log_detail(f"skip_not_available_multi | day={day} | lesson={lesson} | teacher={tn} | subject={subj_name}")
                            break
                        if self.checker.is_busy(busy_map, tn, day, lesson):
                            multi_ok = False
                            _log_detail(f"skip_busy_multi | day={day} | lesson={lesson} | teacher={tn} | subject={subj_name}")
                            break

                    if not multi_ok:
                        continue

                    # Single-teacher case: if only one assigned, ensure availability and not busy
                    if len(assigned_teachers) == 1:
                        tn = assigned_teachers[0]
                        t_obj = teacher_name_map.get(tn)
                        if not t_obj or not self._is_teacher_available(t_obj, day, lesson):
                            _log_detail(f"skip_not_available | day={day} | lesson={lesson} | subject={subj_name}")
                            continue
                        if self.checker.is_busy(busy_map, tn, day, lesson):
                            _log_detail(f"skip_busy | day={day} | lesson={lesson} | teacher={tn} | subject={subj_name}")
                            continue

                    # Place lesson: set teacher field to semicolon-separated list
                    teacher_field = ';'.join(assigned_teachers)
                    color_bg, color_fg = self.color_service.get_color(subj_name)
                    schedule[day][lesson] = {
                        'subject': subj_name,
                        'teacher': teacher_field,
                        'group': group_name,
                        'color_bg': color_bg,
                        'color_fg': color_fg
                    }

                    _log_detail(f"placed | day={day} | lesson={lesson} | subject={subj_name} | teachers={teacher_field}")

                    # Update busy map for all assigned teachers
                    for tn in assigned_teachers:
                        self.checker.mark_busy(busy_map, tn, day, lesson)

                    # Decrement subj_hours from the teacher with most remaining hours (if tracked)
                    if subj_hours_remaining:
                        primary = max(subj_hours_remaining.items(), key=lambda x: x[1])[0]
                        subj_hours_remaining[primary] = max(0, subj_hours_remaining.get(primary, 0) - 1)

                    placed += 1
                    placed_this_round = True

                if not placed_this_round:
                    retries += 1
                else:
                    retries = 0

            if placed < required:
                errors.append(f"Could not place all hours for {subj_name} (placed {placed}/{required})")
                incomplete.append({
                    'subject': subj_name,
                    'placed': placed,
                    'required': required,
                    'teachers': assigned_teachers
                })
        
        success = len(errors) == 0
        # Log end of autofill with results summary
        try:
            with open(os.path.join('uploads', 'autofill_debug.log'), 'a', encoding='utf-8') as lf:
                lf.write(f"{datetime.now().isoformat()} | autofill_end | group={group_name} | success={success} | placed_total={sum([len(v) for v in schedule.values()])} | errors={len(errors)} | incomplete={len(incomplete)}\n")
        except Exception:
            pass

        return success, schedule, {
            'errors': errors,
            'incomplete': incomplete
        }
    
    def _find_teacher(self, subject, teachers):
        """Find a teacher who teaches this subject for this group"""
        subject_name = subject['name']
        group_name = subject['group']
        
        for teacher in teachers:
            for teacher_subject in teacher.get('subjects', []):
                if (teacher_subject['name'] == subject_name and 
                    teacher_subject['group'] == group_name):
                    return teacher
        
        # If no exact match, try to find teacher with same subject (any group)
        for teacher in teachers:
            for teacher_subject in teacher.get('subjects', []):
                if teacher_subject['name'] == subject_name:
                    return teacher
        
        return None
    
    def _is_teacher_available(self, teacher, day, lesson):
        """Check if teacher is available at this day/lesson"""
        available_slots = teacher.get('available_slots', {})
        
        if not available_slots:
            return True  # If no availability specified, assume always available
        
        if day not in available_slots:
            return False
        
        return lesson in available_slots[day]
    
    def _check_constraints(self, schedule, day, lesson, subject_name, max_sequence, max_per_day):
        """Check max_sequence_lessons and max_per_day constraints"""
        # Check sequence constraint: count contiguous same-subject lessons
        # including both before and after the candidate lesson. The total
        # block length (including the candidate) must not exceed max_sequence.
        before_count = 0
        i = lesson - 1
        while i >= 1:
            if i in schedule.get(day, {}) and schedule[day][i]['subject'] == subject_name:
                before_count += 1
                i -= 1
            else:
                break

        after_count = 0
        i = lesson + 1
        # Determine number of lessons per day to avoid infinite loops
        # (lessons are sparse in schedule keys, but we stop if no entry or different subject)
        while True:
            if i in schedule.get(day, {}) and schedule[day][i]['subject'] == subject_name:
                after_count += 1
                i += 1
            else:
                break

        total_block = 1 + before_count + after_count
        if total_block > max_sequence:
            return False
        
        # Check daily limit
        day_count = 0
        if day in schedule:
            for lesson_data in schedule[day].values():
                if lesson_data['subject'] == subject_name:
                    day_count += 1
        
        if day_count >= max_per_day:
            return False
        
        return True
