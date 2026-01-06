import re


class ConflictChecker:
    def __init__(self):
        pass

    def build_busy_map(self, group_schedules, teachers):
        """
        Build a map of teacher busy times from existing schedules
        Returns: {teacher_name: {day: {lesson: True/False}}}
        """
        busy_map = {}

        # Initialize busy map for all teachers
        for teacher in teachers:
            teacher_name = teacher['name']
            busy_map[teacher_name] = {}

        # Mark busy times from existing schedules
        for group_name, group_schedule in group_schedules.items():
            for day, lessons in group_schedule.items():
                for lesson_num, lesson_data in lessons.items():
                    teacher_field = lesson_data.get('teacher', '') or ''
                    # teacher_field may contain multiple teacher names separated by ';' or ','
                    if not teacher_field:
                        continue
                    if isinstance(teacher_field, str):
                        parts = [p.strip() for p in re.split(r'[;,]', teacher_field) if p.strip()]
                    elif isinstance(teacher_field, (list, tuple)):
                        parts = list(teacher_field)
                    else:
                        parts = [str(teacher_field)]

                    for teacher in parts:
                        if teacher:
                            if teacher not in busy_map:
                                busy_map[teacher] = {}
                            if day not in busy_map[teacher]:
                                busy_map[teacher][day] = {}
                            busy_map[teacher][day][lesson_num] = True

        return busy_map

    def is_busy(self, busy_map, teacher_name, day, lesson):
        """Check if a teacher is busy at a specific time"""
        if teacher_name not in busy_map:
            return False
        if day not in busy_map[teacher_name]:
            return False
        return busy_map[teacher_name].get(day, {}).get(lesson, False)

    def mark_busy(self, busy_map, teacher_name, day, lesson):
        """Mark a teacher as busy at a specific time"""
        if teacher_name not in busy_map:
            busy_map[teacher_name] = {}
        if day not in busy_map[teacher_name]:
            busy_map[teacher_name][day] = {}
        busy_map[teacher_name][day][lesson] = True

    def check_teacher_conflict(self, teacher_name, day, lesson, group_schedules):
        """Check if adding a lesson would create a conflict"""
        for group_name, group_schedule in group_schedules.items():
            if day in group_schedule and lesson in group_schedule[day]:
                existing_lesson = group_schedule[day][lesson]
                tfield = existing_lesson.get('teacher', '') or ''
                if isinstance(tfield, str):
                    parts = [p.strip() for p in re.split(r'[;,]', tfield) if p.strip()]
                elif isinstance(tfield, (list, tuple)):
                    parts = list(tfield)
                else:
                    parts = [str(tfield)]
                if teacher_name in parts:
                    return True  # Conflict found
        return False
