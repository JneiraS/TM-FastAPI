from src.application.use_cases import UserRepository


def new_user_services(user_repository: UserRepository):
    return UserService(user_repository)

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def save(self, user):
            self.user_repository.save(user)


