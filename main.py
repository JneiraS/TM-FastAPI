from fastapi import FastAPI
from src.infrastructure.sqlalchemy_models import Base
from src.infrastructure.persistence.db import engine
from src.interface import api
import uvicorn

app = FastAPI()

Base.metadata.create_all(engine)
app.include_router(api.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
