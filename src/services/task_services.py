from src.infrastructure.persistence.db import get_db
from src.infrastructure.task_repository import SQLAlchemyTaskRepository
from fastapi import Depends
from sqlalchemy.orm import Session


def new_task_services(task_repository: SQLAlchemyTaskRepository):
    return TaskService(task_repository)


class TaskService:
    def __init__(self, task_repository: SQLAlchemyTaskRepository):
        self.task_repository = task_repository

    def save(self, task):
        self.task_repository.save(task)

    def get_all(self):
        return self.task_repository.get_all()

    def get_by_id(self, task_id: int):
        return self.task_repository.get_by_id(task_id)

    def update(self, task):
        self.task_repository.update(task)

    def delete(self, task_id: int):
        self.task_repository.delete(task_id)


def get_task_service(db: Session = Depends(get_db)):
    task_repo = SQLAlchemyTaskRepository(db)
    return new_task_services(task_repo)
