from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Use FastAPI's CORS middleware

from src.infrastructure.sqlalchemy_models import Base
from src.infrastructure.persistence.db import engine
from src.interface import api
import uvicorn

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

Base.metadata.create_all(engine)
app.include_router(api.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
