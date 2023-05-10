import logging

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.misc.dependencies import get_async_session

from typing import List
from src.app.cooking.schemas import ComponentIn, RecipeOut
from src.app.cooking.models import Recipe, Component, RecipeComponent

logger = logging.getLogger(__name__)


class CookingService:
    def __init__(self,
                 db: AsyncSession = Depends(get_async_session)):
        self.db = db

    async def calculate_recipes(self, payload: List[ComponentIn]) -> List[RecipeOut]:
        result = []
        logger.debug(f"User input => {[(c.name, c.value) for c in payload]}")
        
        # form products from the user's refrigerator (case insensitive)
        user_items_map = {}
        for user_item in payload:
            item_name = user_item.name.lower()
            if item_name in user_items_map:
                user_items_map[item_name] += user_item.value
            else:
                user_items_map[item_name] = user_item.value

        stmt = select(Recipe)
        recipes = (await self.db.execute(stmt)).scalars().all()

        for recipe in recipes:
            stmt = select(RecipeComponent).where(
                RecipeComponent.recipe_id == recipe.id).options(selectinload(RecipeComponent.component))
            recipe_components = (await self.db.execute(stmt)).scalars().all()
            
            # form products needed for this recipe (case insensitive)
            recipe_items_map = {el.component.name.lower(): el.value for el in recipe_components}

            # intersect user products with needed for this recipe
            intersection = set(user_items_map.keys()) & set(recipe_items_map.keys())
            if len(intersection) != len(recipe_items_map.keys()):
                continue
            
            # calculate number of servings this recipe if user have all needed components
            servings = min([user_items_map[key] // value for key, value in recipe_items_map.items()])

            if not servings:
                continue

            result.append(RecipeOut(name=recipe.name, servings=servings))

        logger.debug(f"Result recipes => {[(r.name, r.servings) for r in result]}")
        if not result:
            raise HTTPException(status_code=418, detail="Oops! Looks like it's time to order pizza")
        
        return result


