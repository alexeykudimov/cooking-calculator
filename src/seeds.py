import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.misc.database import async_session_maker

from src.app.cooking.models import Recipe, Component, RecipeComponent

data = [
    {
        "name": "Салат «Русский»",
        "components": [{"item": "мясо", "q": 250}, {"item": "огурец", "q": 2}]
    },
    {
        "name": "Салат «Ленинградский»",
        "components": [{"item": "мясо", "q": 500}, {"item": "картофель", "q": 3}]
    },
    {
        "name": "Салат с рыбой и овощами",
        "components": [{"item": "рыба", "q": 500}, {"item": "картофель", "q": 10}, {"item": "яйцо", "q": 3}]
    }
]

async def seeds(session: AsyncSession):
    components_set = set()

    for recipe in data:
        recipe_object = Recipe(name=recipe['name'])
        session.add(recipe_object)

        await session.commit()

        for component in recipe['components']:
            if component['item'] in components_set:
                stmt = select(Component).where(Component.name == component['item'])
                component_object = (await session.execute(stmt)).scalar_one_or_none()
            else:
                components_set.add(component['item'])
                component_object = Component(name=component['item'])
                session.add(component_object)
                
                await session.commit()

            recipe_component_object = RecipeComponent(
                recipe_id=recipe_object.id, component_id=component_object.id, value=component['q'])
            
            session.add(recipe_component_object)

    await session.commit()
                

if __name__ == '__main__':
    session: AsyncSession = async_session_maker()
    asyncio.run(seeds(session))



