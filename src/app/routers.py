from fastapi import APIRouter

from src.app.cooking.endpoints import router as cooking_router

api_router = APIRouter()

api_router.include_router(cooking_router, prefix='', tags=['Cooking'])
