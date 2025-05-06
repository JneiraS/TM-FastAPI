from sqlalchemy.orm import Session
from typing import List, Optional

from src.domain.models import Task
from src.infrastructure.sqlalchemy_models import TaskModel


class TaskMapper:
    """
    Classe responsable de la conversion entre les objets de domaine Task
    et les modèles d'infrastructure TaskModel.
    """

    @staticmethod
    def to_domain(task_model) -> Optional[Task]:
        """
        Convertit un modèle de base de données en objet du domaine.
        """
        if not task_model:
            return None
        return Task(
            id=task_model.id,
            title=task_model.title,
            priority=task_model.priority,
            assigned_to=task_model.assigned_to,
            completed=task_model.completed,
        )

    @staticmethod
    def to_infrastructure(task: Task) -> TaskModel:
        """
        Convertit un objet du domaine en modèle de base de données.
        """
        return TaskModel(
            id=task.id,
            title=task.title,
            priority=task.priority,
            assigned_to=task.assigned_to,
            completed=task.completed,
        )


class SQLAlchemyTaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, task: Task) -> None:
        """
        Enregistre une nouvelle tâche dans la base de données.
        """
        # Validate task data
        if not task.title or len(task.title.strip()) == 0:
            raise ValueError("Task title ne peut pas être vide.")

        # Either let the database assign an ID automatically by setting it to None
        task_to_save = Task(
            id=None if task.id == 0 else task.id,
            title=task.title,
            priority=task.priority,
            assigned_to=task.assigned_to,
            completed=task.completed,
        )

        # Convert domain object to database model
        task_model = TaskMapper.to_infrastructure(task_to_save)

        # Save to database
        self.session.add(task_model)
        self.session.commit()
        self.session.refresh(task_model)

    def get_all(self) -> List[Task]:
        task_models = self.session.query(TaskModel).all()
        return [TaskMapper.to_domain(task_model) for task_model in task_models]

    def get_by_id(self, task_id: int) -> Optional[Task]:
        task_model = self.session.query(TaskModel).filter_by(id=task_id).first()
        return TaskMapper.to_domain(task_model)

    def update(self, task: Task):
        task_model = TaskMapper.to_infrastructure(task)
        self.session.merge(task_model)
        self.session.commit()
        return TaskMapper.to_domain(task_model)

    def delete(self, task_id: int):
        task_model = self.session.query(TaskModel).filter_by(id=task_id).first()
        if task_model:
            self.session.delete(task_model)
            self.session.commit()
