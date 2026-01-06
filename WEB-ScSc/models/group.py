class Group:
    def __init__(self, name, subjects=None):
        self.name = name
        self.subjects = subjects or []  # List of subject names
    
    def to_dict(self):
        return {
            'name': self.name,
            'subjects': self.subjects
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            subjects=data.get('subjects', [])
        )
