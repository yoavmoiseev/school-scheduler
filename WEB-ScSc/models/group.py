class Group:
    def __init__(self, name, subjects=None, is_united=False, sub_groups=None, room=None):
        self.name = name
        self.subjects = subjects or []  # List of subject names (used as comments)
        self.is_united = is_united      # True if this is a united (combined) group
        self.sub_groups = sub_groups or []  # List of sub-group names that form this united group
        self.room = room or ''          # Associated classroom/room name
    
    def to_dict(self):
        return {
            'name': self.name,
            'subjects': self.subjects,
            'is_united': self.is_united,
            'sub_groups': self.sub_groups,
            'room': self.room,
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            subjects=data.get('subjects', []),
            is_united=bool(data.get('is_united', False)),
            sub_groups=data.get('sub_groups', []),
            room=data.get('room', ''),
        )
