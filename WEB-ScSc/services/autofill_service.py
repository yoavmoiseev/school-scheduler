import random
import os
from datetime import datetime


class AutofillService:
    def __init__(self, excel_service, conflict_checker, color_service):
        self.excel = excel_service
        self.checker = conflict_checker
        self.color_service = color_service
    
    def autofill_group(self, group_name, max_retries=100, preserve_existing=True, subject_order=None):
        """
        Autofill schedule for a group.
        Args:
            group_name: Name of the group to autofill
            max_retries: Maximum number of retry attempts
            preserve_existing: If True, keep existing lessons and only fill empty slots.
                             If False, start from scratch (used by Rebuild All)
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

        # Sort subjects by priority order.
        # If a subject_order list is provided (from Rebuild All priorities UI), respect it.
        # Otherwise auto-sort: multi-teacher subjects first (most constrained), then by hours desc.
        if subject_order:
            _order_index = {name: i for i, name in enumerate(subject_order)}
            group_subjects.sort(key=lambda s: _order_index.get(s.get('name', ''), len(subject_order)))
        else:
            # Build a quick teacher-count map for this group's subjects
            _subj_teacher_count = {}
            for s in group_subjects:
                sn = s.get('name', '')
                cnt = sum(
                    1 for t in teachers
                    for ts in t.get('subjects', [])
                    if ts.get('name') == sn and (ts.get('group', '') == group_name or ts.get('group', '') == '')
                )
                _subj_teacher_count[sn] = cnt

            # MRV-эвристика: считаем минимальное число доступных слотов у преподавателя предмета.
            # Предмет с наиболее ограниченным преподавателем ставится в расписание первым.
            def _count_slots(teacher):
                avail = teacher.get('available_slots', {})
                if not avail:
                    return 999  # без ограничений = максимально гибкий
                return sum(len(v) for v in avail.values() if v)

            _subj_min_slots = {}
            for s in group_subjects:
                sn = s.get('name', '')
                t_list = [
                    t for t in teachers
                    for ts in t.get('subjects', [])
                    if ts.get('name') == sn and (ts.get('group', '') == group_name or ts.get('group', '') == '')
                ]
                _subj_min_slots[sn] = min((_count_slots(t) for t in t_list), default=999)

            # Сортировка: сначала самый ограниченный по слотам,
            # затем предметы с несколькими преподавателями, затем по часам
            group_subjects.sort(key=lambda s: (
                _subj_min_slots.get(s.get('name', ''), 999),
                0 if _subj_teacher_count.get(s.get('name', ''), 0) > 1 else 1,
                -int(s.get('hours_per_week', 0) or 0)
            ))

        # Initialize schedule
        schedule = {}
        for day in weekdays:
            schedule[day] = {}

        if not group_subjects:
            errors.append(f"No subjects found for group '{group_name}'")
            return False, schedule, errors
        
        # Build teacher busy map from existing schedules (excluding current group)
        existing_schedules = self.excel.get_group_schedules()
        
        # Load existing schedule for this group to preserve manual selections (if preserve_existing=True)
        if preserve_existing and group_name in existing_schedules:
            current_schedule = existing_schedules[group_name]
            # Copy existing lessons into schedule
            for day in current_schedule:
                if day not in schedule:
                    schedule[day] = {}
                for lesson_num, lesson_data in current_schedule[day].items():
                    schedule[day][lesson_num] = lesson_data
            # Remove from existing_schedules to avoid double-counting in busy_map
            del existing_schedules[group_name]
        elif group_name in existing_schedules:
            # If not preserving, just remove current group from existing_schedules
            del existing_schedules[group_name]
        
        busy_map = self.checker.build_busy_map(existing_schedules, teachers)
        
        # Mark teachers from preserved lessons as busy (only if we preserved lessons)
        if preserve_existing:
            for day in schedule:
                for lesson_num, lesson_data in schedule[day].items():
                    teacher_str = lesson_data.get('teacher', '')
                    if teacher_str:
                        # Handle multiple teachers (semicolon-separated)
                        teacher_names = [t.strip() for t in teacher_str.split(';')]
                        for teacher_name in teacher_names:
                            self.checker.mark_busy(busy_map, teacher_name, day, lesson_num)

        
        errors = []
        
        # For each subject, try to place lessons
        for subject in group_subjects:
            subj_name = subject['name']

            # Build list of assigned teachers for this subject (matching group or empty group)
            assigned_teachers = []
            teacher_name_map = {t['name']: t for t in teachers}
            subj_teacher_hours = {}
            teachers_without_slots = {}  # Track teachers without available slots
            
            for t in teachers:
                for ts in t.get('subjects', []):
                    if ts.get('name') == subj_name and (ts.get('group', '') == group_name or ts.get('group', '') == ''):
                        # Check if teacher has available time slots
                        available_slots = t.get('available_slots', {})
                        has_slots = available_slots and any(slots for slots in available_slots.values() if slots)
                        
                        if not has_slots:
                            # Teacher has no available time slots - track but don't add to assigned
                            if t['name'] not in teachers_without_slots:
                                teachers_without_slots[t['name']] = []
                            teachers_without_slots[t['name']].append(f"{subj_name} ({group_name})")
                            continue
                        
                        assigned_teachers.append(t['name'])
                        try:
                            subj_teacher_hours[t['name']] = subj_teacher_hours.get(t['name'], 0) + int(ts.get('hours', 0) or 0)
                        except Exception:
                            subj_teacher_hours[t['name']] = subj_teacher_hours.get(t['name'], 0)
            
            # Report teachers without slots
            for teacher_name, subjects_list in teachers_without_slots.items():
                subjects_str = ', '.join(subjects_list)
                errors.append("Teacher '{TEACHER}' has no available time slots but is assigned to: {SUBJECTS}".replace('{TEACHER}', teacher_name).replace('{SUBJECTS}', subjects_str))

            if not assigned_teachers:
                errors.append("No teacher found for subject 'SUBJECT_NAME' in group 'GROUP_NAME'".replace('SUBJECT_NAME', subj_name).replace('GROUP_NAME', group_name))
                continue

            # Determine required lessons for this subject
            required = int(subject.get('hours_per_week', 0) or 0)
            if len(assigned_teachers) > 1:
                # if multiple teachers assigned, prefer subject hours if defined, otherwise sum teacher hours
                if required <= 0:
                    total_teacher_hours = sum(subj_teacher_hours.get(n, 0) for n in assigned_teachers)
                    required = total_teacher_hours

            # Count how many lessons of this subject are already placed (if preserve_existing)
            placed = 0
            if preserve_existing:
                for day in schedule:
                    for lesson_data in schedule[day].values():
                        if lesson_data.get('subject') == subj_name:
                            placed += 1
            
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
                    random.shuffle(possible_slots)  # вариируем порядок при следующей попытке
                else:
                    retries = 0

            # Swap-based backtracking: если greedy-цикл не разместил все уроки,
            # пробуем освободить занятые слоты, переставив блокирующий урок в другое место.
            while placed < required:
                swapped = self._try_swap_placement(
                    schedule, busy_map, teacher_name_map, weekdays, lessons,
                    subj_name, assigned_teachers, group_name,
                    max_sequence, max_per_day
                )
                if not swapped:
                    break
                placed += 1
                _log_detail(f"swap_placed | subject={subj_name} | placed={placed}/{required}")

            if placed < required:
                errors.append("Could not place all hours for {SUBJ} (placed {NUM_PLACED}/{NUM_REQUIRED})".replace('{SUBJ}', subj_name).replace('{NUM_PLACED}', str(placed)).replace('{NUM_REQUIRED}', str(required)))
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
    
    def _try_swap_placement(self, schedule, busy_map, teacher_name_map, weekdays, lessons,
                             subj_name, assigned_teachers, group_name,
                             max_sequence, max_per_day):
        """
        Пытается разместить один урок subj_name, переставив блокирующий урок на другой слот.
        Возвращает True если перестановка выполнена (schedule и busy_map изменены in-place).
        """
        for day in weekdays:
            for lesson_num in lessons:
                # Нас интересуют только занятые слоты (пустые уже проверены greedy-циклом)
                if lesson_num not in schedule.get(day, {}):
                    continue

                blocking_data = schedule[day][lesson_num]
                blocking_teacher_str = blocking_data.get('teacher') or ''
                blocking_teachers = [t.strip() for t in blocking_teacher_str.split(';') if t.strip()]
                blocking_subj = blocking_data.get('subject', '')

                # Не трогаем уроки того же предмета
                if blocking_subj == subj_name:
                    continue

                # Все наши учителя должны быть доступны в этом слоте
                teachers_ok = True
                for tn in assigned_teachers:
                    t_obj = teacher_name_map.get(tn)
                    if not t_obj or not self._is_teacher_available(t_obj, day, lesson_num):
                        teachers_ok = False
                        break
                if not teachers_ok:
                    continue

                # Наши учителя не должны быть заняты в этом слоте другими группами
                # (блокирующий урок здесь — не считается: мы его уберём)
                teachers_free = True
                for tn in assigned_teachers:
                    if tn in blocking_teachers:
                        # Тот же преподаватель — swap невозможен
                        teachers_free = False
                        break
                    if self.checker.is_busy(busy_map, tn, day, lesson_num):
                        teachers_free = False
                        break
                if not teachers_free:
                    continue

                # Проверяем ограничения для нашего предмета в этом слоте
                # (временно убираем блокирующий урок для чистой проверки)
                temp_removed = schedule[day].pop(lesson_num)
                constraints_ok = self._check_constraints(
                    schedule, day, lesson_num, subj_name, max_sequence, max_per_day
                )
                schedule[day][lesson_num] = temp_removed
                if not constraints_ok:
                    continue

                # Ищем альтернативный пустой слот для блокирующего урока
                for alt_day in weekdays:
                    for alt_lesson in lessons:
                        if alt_lesson in schedule.get(alt_day, {}):
                            continue
                        if alt_day == day and alt_lesson == lesson_num:
                            continue

                        # Учителя блокирующего урока должны быть доступны
                        bt_avail = True
                        for btn in blocking_teachers:
                            bt_obj = teacher_name_map.get(btn)
                            if not bt_obj or not self._is_teacher_available(bt_obj, alt_day, alt_lesson):
                                bt_avail = False
                                break
                        if not bt_avail:
                            continue

                        # Учителя блокирующего урока не должны быть заняты
                        bt_free = True
                        for btn in blocking_teachers:
                            if self.checker.is_busy(busy_map, btn, alt_day, alt_lesson):
                                bt_free = False
                                break
                        if not bt_free:
                            continue

                        # Ограничения для блокирующего предмета в alt-слоте
                        temp_blocking = schedule[day].pop(lesson_num)
                        alt_ok = self._check_constraints(
                            schedule, alt_day, alt_lesson, blocking_subj, max_sequence, max_per_day
                        )
                        if not alt_ok:
                            schedule[day][lesson_num] = temp_blocking
                            continue

                        # ✅ SWAP возможен — выполняем
                        # 1. Снимаем занятость учителей блокирующего урока в исходном слоте
                        for btn in blocking_teachers:
                            if btn in busy_map and day in busy_map[btn]:
                                busy_map[btn][day].pop(lesson_num, None)

                        # 2. Перемещаем блокирующий урок в alt-слот
                        schedule[alt_day][alt_lesson] = temp_blocking
                        for btn in blocking_teachers:
                            self.checker.mark_busy(busy_map, btn, alt_day, alt_lesson)

                        # 3. Размещаем наш предмет в освобождённый слот
                        color_bg, color_fg = self.color_service.get_color(subj_name)
                        schedule[day][lesson_num] = {
                            'subject': subj_name,
                            'teacher': ';'.join(assigned_teachers),
                            'group': group_name,
                            'color_bg': color_bg,
                            'color_fg': color_fg
                        }
                        for tn in assigned_teachers:
                            self.checker.mark_busy(busy_map, tn, day, lesson_num)

                        return True

        return False

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
