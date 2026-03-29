class User:
    def __init__(self, name: str, age: int, user_id: int | None = None):
        self.id = user_id
        self.name = name
        self.age = age
