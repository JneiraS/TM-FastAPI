from fastapi import APIRouter, Depends
from typing import Annotated

from src.domain.models import User
from src.domain.schemas import UserSchema
from src.infrastructure.repositories import get_user_service
from src.services.user_services import UserService

router = APIRouter()


@router.get("/", response_model=dict)
def read_root():
    return {"message": "Bienvenue sur l'API de gestion des utilisateurs."}


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
    return {"message": "User created successfully"}


@router.get("/user/{user_id}", response_model=UserSchema)
async def get_user(
    user_id: int,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    user = user_service.get_by_id(user_id)
    return UserSchema.from_domain(user)
