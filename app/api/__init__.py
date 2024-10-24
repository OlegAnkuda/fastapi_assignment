from fastapi import APIRouter
from app.api.v1 import v1_router


router = APIRouter(prefix="/api")

router.include_router(v1_router)