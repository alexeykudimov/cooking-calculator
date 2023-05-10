from httpx import AsyncClient

all_recipes = [
    {"name": "мясо", "value": 2000},
    {"name": "картофель", "value": 50},
    {"name": "огурец", "value": 5},
    {"name": "рыба", "value": 1520},
    {"name": "яйцо", "value": 50}]

all_recipes_but_enough_for_one = [
    {"name": "мясо", "value": 2000},
    {"name": "картофель", "value": 50},
    {"name": "огурец", "value": 1},
    {"name": "рыба", "value": 2000},
    {"name": "яйцо", "value": 1}]

no_recipes = [
    {"name": "мясо", "value": 1},
    {"name": "рыба", "value": 1},
    {"name": "ананас", "value": 1}]

with_repeat_and_uppercase = [
    {"name": "МясО", "value": 250},
    {"name": "мЯсО", "value": 500},
    {"name": "огурец", "value": 10}]

async def test_all_recipes(ac: AsyncClient):
    response = await ac.post("v1/recipes", json=all_recipes)

    assert response.status_code == 200
    assert len(response.json()) == 3

async def test_all_recipes_but_enough_for_one(ac: AsyncClient):
    response = await ac.post("v1/recipes", json=all_recipes_but_enough_for_one)

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['name'] == 'Салат «Ленинградский»'
    assert response.json()[0]['servings'] == 4

async def test_no_recipes(ac: AsyncClient):
    response = await ac.post("v1/recipes", json=no_recipes)

    assert response.status_code == 418

async def test_with_repeat_and_uppercase(ac: AsyncClient):
    response = await ac.post("v1/recipes", json=with_repeat_and_uppercase)

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['name'] == 'Салат «Русский»'
    assert response.json()[0]['servings'] == 3
