from enum import Enum


class Priority(Enum):
    HIGH = 3

    LOW = 1
    MEDIUM = 2
class User:
    def __init__(self, id: int, name: str, assigned_tasks=None):
        self.id = id
        self.name = name
        self.assigned_tasks = assigned_tasks or []

class Task:
    def __init__(self, id: int, assigned_to: int, priority:Priority, completed: bool, title: str) -> None:
        self.id = id
        self.title = title
        self.priority = priority
        self. assigned_to = assigned_to
        self.completed = completed


