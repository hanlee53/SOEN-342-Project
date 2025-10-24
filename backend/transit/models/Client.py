class Client:
    """
    Stores the record of a traveller in memory.
    "name, age, and id"
    """
    def __init__(self, client_id: str, name: str, age: int):
        self.client_id = client_id # "id" (e.g., state-id or passport number)
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.name} (ID: {self.client_id})"

