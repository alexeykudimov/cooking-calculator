from pydantic import BaseModel


class ComponentIn(BaseModel):
    name: str
    value: int


class RecipeOut(BaseModel):
    name: str
    servings: int


class PopularComponentOut(BaseModel):
    name: str
    users_count: int

    class Config:
        orm_mode = True
