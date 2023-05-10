from pydantic import BaseModel


class ComponentIn(BaseModel):
    name: str
    value: int


class RecipeOut(BaseModel):
    name: str
    servings: int
