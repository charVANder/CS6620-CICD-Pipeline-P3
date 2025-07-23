'''
Changed the file so that it works w/ DynamoDB stuff
NOTE: I later realized that I didn't really need this anymore (TT_TT) but I'm leaving it here anyway, lol.
Dictionaries are good enough for a Flask CRUD API with AWS backends.
'''
class Pokemon:
    def __init__(self, id: int, name: str, level: int, pkmn_type="Normal", hp=None, max_hp=None):
        self.id = id
        self.name = name.strip()
        self.level = level
        self.type = pkmn_type
        self.hp = hp if hp is not None else 50 + (level * 2)
        self.max_hp = max_hp if max_hp is not None else 50 + (level * 2)

    def to_dict(self):
        """Convert to dict for DynamoDB storage or JSON response."""
        return {
            "id": self.id,
            "name": self.name,
            "level": self.level,
            "type": self.type,
            "hp": self.hp,
            "max_hp": self.max_hp
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=int(data["id"]),
            name=data["name"],
            level=int(data["level"]),
            pkmn_type=data.get("type", "Normal"),
            hp=data.get("hp"),
            max_hp=data.get("max_hp")
        )

    def validate(self):
        if not self.name or not isinstance(self.name, str):
            return False, "The name is invalid"
        if not isinstance(self.level, int) or not (1 <= self.level <= 100):
            return False, "Level must be an integer b/w 1 and 100"
        if self.hp is None or self.hp < 0:
            return False, "HP must be a positive number"
        if self.max_hp is None or self.max_hp < 0:
            return False, "Max HP must be a positive number"
        return True, ""