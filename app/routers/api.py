from fastapi import APIRouter
from app.api.auth2 import auth
from app.api.super_engineer.super_api import router as super_engineer_router
from app.api.engineer.engineer_api import router as engineer_router

router = APIRouter()
router.include_router(auth.router, tags=["authentication"], prefix="/users")
router.include_router(engineer_router, tags=["Engineer"], prefix="/engineer")
router.include_router(super_engineer_router, tags=["Super_Engineer"], prefix="/super_engineer")

