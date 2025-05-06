from fastapi import APIRouter, Depends
from typing import Annotated

from src.domain.models import User, Task, Priority
from src.domain.schemas import UserSchema, TaskSchema
from src.infrastructure.repositories import get_user_service
from src.services.task_services import TaskService, get_task_service
from src.services.user_services import UserService

router = APIRouter()


@router.get("/", response_model=dict)
def read_root():
    return {"message": "Bienvenue sur l'API de gestion des utilisateurs."}


# -----USERS-----


@router.post("/user/", response_model=dict)
async def create_user(
    user_data: UserSchema,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    # Convertir le modèle Pydantic en modèle de domaine
    user = User(
        id=user_data.id, name=user_data.name, assigned_tasks=user_data.assigned_tasks
    )
    user_service.save(user)
    return {"message": "User créé avec succès."}


@router.get("/user/{user_id}", response_model=UserSchema)
async def get_user(
    user_id: int,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    user = user_service.get_by_id(user_id)
    return UserSchema.from_domain(user)


@router.put("/user/{user_id}", response_model=dict)
async def update_user(
    user_id: int,
    user_data: UserSchema,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    # Verifier si l'utilisateur existe
    existing_user = user_service.get_by_id(user_id)
    if not existing_user:
        return {"message": "Aucun User trouvé", "success": False}, 404

    # Update user with new data
    updated_user = User(
        id=user_id, name=user_data.name, assigned_tasks=user_data.assigned_tasks
    )

    # Enregistrez l'utilisateur mis à jour
    user_service.update(updated_user)

    return {"message": "User mis à jour avec succès.", "success": True}


# -----TASKS-----


@router.post("/task/", response_model=dict)
async def create_task(
    task_data: TaskSchema,
    task_service: Annotated[TaskService, Depends(get_task_service)],
):
    # Convertir En Enum
    priority = Priority(task_data.priority)

    # Convertir le modèle Pydantic en modèle de domaine
    task = Task(
        id=task_data.id,
        title=task_data.title,
        priority=priority.value,
        assigned_to=task_data.assigned_to,
        completed=task_data.completed,
    )
    task_service.save(task)
    return {"message": "Task créé avec succès."}


@router.get("/task/", response_model=list[TaskSchema])
async def get_all_task(
    task_service: Annotated[TaskService, Depends(get_task_service)],
):
    tasks = task_service.get_all()
    # Convert the priority value back to an enum value
    for task in tasks:
        task.priority = int(task.priority)
    return tasks
