from pydantic import BaseModel
from typing import List, Optional

from src.domain.models import User, Task, Priority


class UserSchema(BaseModel):
    id: int
    name: str
    assigned_tasks: Optional[List[int]] = []

    @classmethod
    def from_domain(cls, user: User) -> "UserSchema":
        """
        Convert a domain User model to a UserSchema.
        """
        return cls(id=user.id, name=user.name, assigned_tasks=user.assigned_tasks)


class TaskSchema(BaseModel):
    id: int
    assigned_to: int
    title: str
    priority: Priority
    completed: bool

    @classmethod
    def from_domain(cls, task: Task) -> "TaskSchema":
        """
        Convert a domain Task model to a TaskSchema.
        """
        return cls(
            id=task.id,
            title=task.title,
            priority=task.priority,
            assigned_to=task.assigned_to,
            completed=task.completed,
        )
