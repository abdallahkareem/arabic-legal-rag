from fastapi import APIRouter


router = APIRouter(
    prefix="/api/v1",
)

@router.get("/")
async def welcome_message():
    return "Welcome to the Arabic Legal RAG App"