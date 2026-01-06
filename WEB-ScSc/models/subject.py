class Subject:
    def __init__(self, name, group, hours_per_week, teacher=None):
        self.name = name
        self.group = group
        self.hours_per_week = hours_per_week
        self.teacher = teacher
    
    def to_dict(self):
        return {
            'name': self.name,
            'group': self.group,
            'hours_per_week': self.hours_per_week,
            'teacher': self.teacher
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            group=data['group'],
            hours_per_week=data['hours_per_week'],
            teacher=data.get('teacher')
        )
