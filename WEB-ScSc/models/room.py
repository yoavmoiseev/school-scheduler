class Room:
    def __init__(self, name, description=None):
        self.name = name
        self.description = description or ''

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            description=data.get('description', ''),
        )
