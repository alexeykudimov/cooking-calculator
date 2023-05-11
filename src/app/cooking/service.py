import logging
from uuid import UUID
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.misc.dependencies import get_async_session

from typing import List
from src.app.cooking.schemas import ComponentIn, RecipeOut, PopularComponentOut
from src.app.cooking.models import Recipe, Component, RecipeComponent, RecipeHistory

logger = logging.getLogger(__name__)


class CookingService:
    def __init__(self,
                 db: AsyncSession = Depends(get_async_session)):
        self.db = db

    async def save_recipe_history(self, recipe_id: UUID) -> RecipeHistory:
        recipe_history_object = RecipeHistory(recipe_id=recipe_id)
        self.db.add(recipe_history_object)
        await self.db.commit()

        return recipe_history_object
    
    async def get_recent_recipes(self) -> List[str]:
        hour_ago = datetime.utcnow() - timedelta(seconds=3600)
        stmt = select(
            RecipeHistory).where(
            RecipeHistory.created_at > hour_ago).distinct(
            RecipeHistory.recipe_id).options(selectinload(RecipeHistory.recipe))
        recent_recipes = (await self.db.execute(stmt)).scalars().all()

        if not recent_recipes:
            raise HTTPException(status_code=418, detail="System didn't recommend recipes in the last hour")
        
        return [el.recipe.name for el in recent_recipes]
    
    async def get_popular_components(self, limit: int) -> List[PopularComponentOut]:
        stmt = select(Component).where(
            Component.users_count > 0).order_by(
            Component.users_count.desc()).limit(limit)
        popular_components = (await self.db.execute(stmt)).scalars().all()

        if not popular_components:
            raise HTTPException(status_code=418, detail="No statistics yet!")
        
        return popular_components
    
    async def create_component(self, name: str) -> Component:
        component_object = Component(name=name)
        self.db.add(component_object)
        await self.db.commit()

        return component_object
    
    async def update_component_users(self, user_items_map: dict):
        for name, value in user_items_map.items():
            if not value:
                continue

            stmt = select(Component).where(Component.name == name)
            component_object = (await self.db.execute(stmt)).scalar_one_or_none()

            if not component_object:
                component_object = await self.create_component(name)

            component_object.users_count += 1
        
        await self.db.commit()

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

        # save user components for rating
        await self.update_component_users(user_items_map)

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
            await self.save_recipe_history(recipe.id)

        logger.debug(f"Result recipes => {[(r.name, r.servings) for r in result]}")
        if not result:
            raise HTTPException(status_code=418, detail="Oops! Looks like it's time to order pizza")
        
        return result


