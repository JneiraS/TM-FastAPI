from src.domain.models import User
from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User):
        pass

    @abstractmethod
    def get_by_id(self, user_id: int):
        pass