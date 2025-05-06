from pydantic import BaseModel
from typing import List, Optional

from src.domain.models import User


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
