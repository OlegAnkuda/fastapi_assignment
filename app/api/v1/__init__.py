from fastapi import APIRouter
from app.api.v1 import books


v1_router = APIRouter(prefix="/v1")

v1_router.include_router(books.router)