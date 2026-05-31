from datetime import datetime

from app.database import SessionLocal

from app.models import (
    WeightLog,
    WaterLog,
    UserProfile,
    MealLog
)

from app.utils.bmi import calculate_bmi


def summarize_day(user_id):

    db = SessionLocal()

    today = datetime.utcnow().date()

    # DEFAULT VALUES
    today_water = 0
    today_calories = 0
    today_protein = 0

    # =====================
    # FETCH LATEST WEIGHT
    # =====================

    latest_weight = db.query(WeightLog).filter(
        WeightLog.user_id == user_id
    ).order_by(
        WeightLog.created_at.desc()
    ).first()

    # =====================
    # FETCH TODAY WATER
    # =====================

    water_logs = db.query(WaterLog).filter(
        WaterLog.user_id == user_id
    ).all()

    for log in water_logs:

        if log.created_at.date() == today:

            today_water += log.liters

    # =====================
    # FETCH TODAY MEALS
    # =====================

    meal_logs = db.query(MealLog).filter(
        MealLog.user_id == user_id
    ).all()

    for meal in meal_logs:

        if meal.created_at.date() == today:

            today_calories += meal.calories
            today_protein += meal.protein

    # =====================
    # FETCH PROFILE
    # =====================

    profile = db.query(UserProfile).filter(
        UserProfile.user_id == user_id
    ).first()

    db.close()

    # =====================
    # BUILD SUMMARY
    # =====================

    summary_lines = []

    summary_lines.append(
        "📊 Daily Summary\n"
    )

    # WEIGHT

    if latest_weight:

        summary_lines.append(
            f"Weight: {latest_weight.weight} kg"
        )

    else:

        summary_lines.append(
            "Weight: No data"
        )

    # BMI

    if latest_weight and profile:

        bmi = calculate_bmi(
            latest_weight.weight,
            profile.height_cm
        )

        summary_lines.append(
            f"BMI: {bmi}"
        )

    # WATER

    summary_lines.append(
        f"Water Intake: {round(today_water, 2)}L 💧"
    )

    # MEALS

    if today_calories > 0:

        summary_lines.append(
            f"Calories: {today_calories} kcal 🍽️"
        )

        summary_lines.append(
            f"Protein: {today_protein}g 💪"
        )

    else:

        summary_lines.append(
            "Meals: No meal data today"
        )

    # =====================
    # INSIGHTS
    # =====================

    if today_water < 2:

        summary_lines.append(
            "\nHydration is low today."
        )

    else:

        summary_lines.append(
            "\nHydration looks decent today."
        )

    if today_calories > 0:

        if today_protein < 80:

            summary_lines.append(
                "Protein intake is a bit low today."
            )

        else:

            summary_lines.append(
                "Protein intake looks good today."
            )

    return "\n".join(summary_lines)