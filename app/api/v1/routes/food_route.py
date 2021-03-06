from fastapi import APIRouter, Security
from starlette.responses import JSONResponse

from app.api.v1.validations.food_validators import FoodFilterSchema, FoodSchema
from app.core.logger import logger
from app.models.category import FoodCategory
from app.models.food import Food
from app.models.user import User
from app.utils.autentication import authenticate_admin_user
from app.utils.settings import SETTINGS

food_route = APIRouter()


@food_route.get("/")
async def get_all_foods(page: int = 1,
                  food_category_id: str = None,
                  name: str = None,
                  min_price: float = None,
                  max_price: float = None):
    """List food for filter"""
    try:
        filters = FoodFilterSchema(food_category_id=food_category_id,
                                   name=name,
                                   min_price=min_price,
                                   max_price=max_price)

        food_query = Food.get_by_filters(page=page, filters=filters)
        return {
            "info": {
                "page": page,
                "next_page": page + 1 if SETTINGS.ITEMS_PER_PAGE * page < food_query.count() else None,
                "total": food_query.count(),
                "items_per_page": SETTINGS.ITEMS_PER_PAGE
            },
            "data": [food_categories.serialize() for food_categories in food_query]
        }
    except (Exception) as err:
        logger.error(f"Error in get food categories - Error: {err}")
        return JSONResponse(status_code=400, content={"message": "Error in get food categories"})


@food_route.get("/{food_id}")
async def get_food_by_id(food_id: str):
    """Get food for id"""
    try:
        food = Food.get_by_id(food_id)

        if not food:
            return JSONResponse(status_code=404, content={"message": "Food do not exist!"})

        return food.serialize()

    except (Exception) as err:
        logger.error(f"Error in get food - Error: {err}")
        return JSONResponse(status_code=400, content={"message": "Error in get food"})


@food_route.post("/")
async def save_food(food: FoodSchema, current_user: User = Security(authenticate_admin_user)):
    """Save new food"""
    try:
        food = food.dict()
        food['food_categories'] = []
        for food_category_id in food.get('food_categories_id'):
            food['food_categories'].append(FoodCategory.get_by_id(food_category_id))

        del food['food_categories_id']

        return Food(**food).save().serialize()

    except (Exception) as err:
        logger.error(f"Error in save food - Error: {err}")
        return JSONResponse(status_code=400, content={"message": "Error in save food"})


@food_route.delete("/{food_id}")
async def delete_food(food_id: str, current_user: User = Security(authenticate_admin_user)):
    """Delete food"""
    try:
        food = Food.get_by_id(id=food_id)
        if not food:
            return JSONResponse(status_code=400, content={"message": "Food do not exists"})

        food.delete()
        return {"message": "Food deleted!"}

    except (Exception) as err:
        logger.error(f"Error in delete food - Error: {err}")
        return JSONResponse(status_code=400, content={"message": "Error in delete food"})
