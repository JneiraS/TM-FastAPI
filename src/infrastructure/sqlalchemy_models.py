from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class UserModel(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  assigned_tasks = relationship("TaskModel", back_populates="user")

class TaskModel(Base):
  __tablename__ = 'tasks'
  id = Column(Integer, primary_key=True)
  assigned_to = Column(Integer, ForeignKey('users.id'))
  title = Column(String, nullable=False)
  priority = Column(String, nullable=False)
  completed = Column(Integer, nullable=False)
  user = relationship("UserModel", back_populates="assigned_tasks")