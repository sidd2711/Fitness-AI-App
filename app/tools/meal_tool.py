from app.database import SessionLocal

from app.models import MealLog

from app.services.nutrition_service import (
    estimate_nutrition
)


def log_meal(user_id, meal_text):

    nutrition = estimate_nutrition(meal_text)

    calories = nutrition.get("calories", 0)

    protein = nutrition.get("protein", 0)

    db = SessionLocal()

    entry = MealLog(
        user_id=user_id,
        meal_text=meal_text,
        calories=calories,
        protein=protein
    )

    db.add(entry)

    db.commit()

    db.close()

    return (
        "Meal logged 🍽️\n\n"
        f"Calories: {calories} kcal\n"
        f"Protein: {protein}g"
    )