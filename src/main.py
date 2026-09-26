from fastapi import FastAPI , APIRouter
from pydantic import BaseModel
from src.routes import health , base

app = FastAPI(
  title="Arabic Legal RAG",
)

app.include_router(base.router)
app.include_router(health.router)