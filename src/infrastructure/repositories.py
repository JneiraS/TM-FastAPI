from src.application.use_cases import UserRepository
from src.domain.models import User
from src.infrastructure.sqlalchemy_models import UserModel

class SQLAlchemyUserRepository(UserRepository):
  def __init__(self, session):
      self.session = session

  def save(self, user: User):
      user_model = UserModel(name=user.name)
      self.session.add(user_model)
      self.session.commit()
      user.id = user_model.id

  def get_by_id(self, user_id: int):
      user_model = self.session.query(UserModel).filter_by(id=user_id).first()
      if not user_model:
          return None
      return User(
          id=user_model.id,
          name=user_model.name,
          assigned_tasks=user_model.assigned_tasks)
