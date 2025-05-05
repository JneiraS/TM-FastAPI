from fastapi import FastAPI

from src.domain.models import User
from src.services.user_services import new_user_services
from src.infrastructure.repositories import SQLAlchemyUserRepository
from sqlalchemy.orm import Session

app = FastAPI()
session = Session()

# À instancier avec un vrai Session SQLAlchemy
user_repo = SQLAlchemyUserRepository(session)
user_services = new_user_services(user_repo)

@app.post("/user/")
async def create_user(user: User):
    user_services.save(user)
    return {"message": "User created successfully"}

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API FastAPI"}
