import logging
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from src.app.cooking.service import CookingService
from src.app.cooking.schemas import ComponentIn, RecipeOut, PopularComponentOut

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
        "/recipes", 
        status_code=200,
        response_model=List[RecipeOut])
async def calculate_recipes(
        payload: List[ComponentIn],
        cooking_service: CookingService = Depends()):
    '''
    Calculate the number of servings of recipes that the user will have enough.
    Case insensitive and protected for duplicates.
    '''
    return await cooking_service.calculate_recipes(payload)


@router.get(
        "/recipes/recent", 
        status_code=200,
        response_model=List[str])
async def get_recent_recipes(
        cooking_service: CookingService = Depends()):
    '''
    Get recommended by system recipes for the last hour
    '''
    return await cooking_service.get_recent_recipes()


@router.get(
        "/components/popular", 
        status_code=200,
        response_model=List[PopularComponentOut])
async def get_popular_components(
        limit: int = 10,
        cooking_service: CookingService = Depends()):
    '''
    Get popular components by users count (default limit = 10).
    '''
    return await cooking_service.get_popular_components(limit)
