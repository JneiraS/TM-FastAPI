from fastapi import FastAPI

from src.domain.models import User
from src.domain.schemas import UserSchema
from src.infrastructure.persistence.db import engine
from src.infrastructure.sqlalchemy_models import Base
from src.services.user_services import new_user_services
from src.infrastructure.repositories import SQLAlchemyUserRepository
from sqlalchemy.orm import Session, sessionmaker

app = FastAPI()

# Create a sessionmaker bound to your engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(engine)

# Create a session using the sessionmaker
session = SessionLocal()

# À instancier avec un vrai Session SQLAlchemy
user_repo = SQLAlchemyUserRepository(session)
user_services = new_user_services(user_repo)


@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API FastAPI"}

@app.post("/user/")
async def create_user(user_data: UserSchema):  # Use the Pydantic model here
    # Convert Pydantic model to domain model
    user = User(id=user_data.id, name=user_data.name, assigned_tasks=user_data.assigned_tasks)
    user_services.save(user)
    return {"message": "User created successfully"}
