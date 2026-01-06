class Teacher:
    def __init__(self, name, subjects=None, available_slots=None, check_in_hours=None, check_out_hours=None):
        self.name = name
        self.subjects = subjects or []  # List of {'name': str, 'hours': int, 'group': str}
        self.available_slots = available_slots or {}  # {day: [lesson_numbers]}
        self.check_in_hours = check_in_hours or {}  # {day: [times]}
        self.check_out_hours = check_out_hours or {}  # {day: [times]}
    
    def to_dict(self):
        return {
            'name': self.name,
            'subjects': self.subjects,
            'available_slots': self.available_slots,
            'check_in_hours': self.check_in_hours,
            'check_out_hours': self.check_out_hours
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            subjects=data.get('subjects', []),
            available_slots=data.get('available_slots', {}),
            check_in_hours=data.get('check_in_hours', {}),
            check_out_hours=data.get('check_out_hours', {})
        )
    
    def get_total_assigned_hours(self):
        return sum(s['hours'] for s in self.subjects)
    
    def get_total_available_slots(self):
        return sum(len(slots) for slots in self.available_slots.values())
