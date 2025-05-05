from src.application.use_cases import UserRepository


def new_user_services(user_repository: UserRepository):
    return UserService(user_repository)

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def save(self, user):
            self.user_repository.save(user)

    def get_all(self):
        return self.user_repository.get_all()

    def get_by_id(self, user_id: int):
        return self.user_repository.get_by_id(user_id)
    def get_by_name(self, name: str):
        return self.user_repository.get_by_name(name)

    def update(self, user):
        self.user_repository.update(user)

    def delete(self, user_id: int):
        self.user_repository.delete(user_id)

