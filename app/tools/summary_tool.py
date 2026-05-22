from app.database import SessionLocal

from app.models import (
    WeightLog,
    WaterLog,
    UserProfile,
    MealLog
)

from app.utils.bmi import calculate_bmi

from datetime import datetime


def summarize_day(user_id):

    db = SessionLocal()

    today = datetime.utcnow().date()

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

    today_water = 0

    for log in water_logs:

        if log.created_at.date() == today:

            today_water += log.liters

        # =====================
        # FETCH TODAY MEALS
        # =====================

        meal_logs = db.query(MealLog).filter(
            MealLog.user_id == user_id
        ).all()

        today_calories = 0
        today_protein = 0

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

    # CALORIES
    summary_lines.append(
        f"Calories: {round(today_calories)} kcal 🍽️"
    )

    # PROTEIN
    summary_lines.append(
        f"Protein: {round(today_protein)}g 💪"
    )

    # SIMPLE INSIGHTS
    if today_water < 2:

        summary_lines.append(
            "\nHydration is low today."
        )

    else:

        summary_lines.append(
            "\nHydration looks decent today."
        )

    # PROTEIN INSIGHT
    if today_protein < 80:

        summary_lines.append(
            "Protein intake is a bit low today."
        )

    else:

        summary_lines.append(
            "Protein intake looks good today."
        )
        
    return "\n".join(summary_lines)