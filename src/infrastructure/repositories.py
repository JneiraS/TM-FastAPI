from fastapi import Depends
from sqlalchemy.orm import Session, sessionmaker

from src.application.use_cases import UserRepository
from src.domain.models import User
from src.infrastructure.sqlalchemy_models import UserModel
from src.services.user_services import new_user_services
from src.infrastructure.persistence.db import engine


# Create a sessionmaker bound to your engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class SQLAlchemyUserRepository(UserRepository):
  def __init__(self, session):
      self.session = session

  def save(self, user: User):
      user_model = UserModel(name=user.name)
      self.session.add(user_model)
      self.session.commit()
      user.id = user_model.id

  # Dependency



  def get_by_id(self, user_id: int):
      user_model = self.session.query(UserModel).filter_by(id=user_id).first()
      if not user_model:
          return None
      return User(
          id=user_model.id,
          name=user_model.name,
          assigned_tasks=user_model.assigned_tasks)


def get_db():
      db = SessionLocal()
      try:
          yield db
      finally:
          db.close()

def get_user_service(db: Session = Depends(get_db)):
    user_repo = SQLAlchemyUserRepository(db)
    return new_user_services(user_repo)
