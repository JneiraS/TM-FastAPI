from pydantic import BaseModel
from typing import List, Optional

class UserSchema(BaseModel):
    id: int
    name: str
    assigned_tasks: Optional[List[int]] = []
