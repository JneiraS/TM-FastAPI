from enum import Enum


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class User:
    def __init__(self, id: int, name: str, age: int, email: str, tasks=None):
        self.id = id
        self.name = name
        self.assigned_tasks = tasks or []

class Task:
    def __init__(self, id: int, assigned_to: int, priority:Priority, completed: bool):
        self.id = id
        self. assigned_to = assigned_to
        self.completed = completed
