from fastapi import FastAPI
from src.infrastructure.sqlalchemy_models import Base
from src.infrastructure.persistence.db import engine

from src.interface import api

app = FastAPI()
Base.metadata.create_all(engine)
app.include_router(api.router)
