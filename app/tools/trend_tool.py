from app.database import SessionLocal
from app.models import WeightLog

from datetime import datetime, timedelta


def get_weight_trend(user_id):

    db = SessionLocal()

    seven_days_ago = datetime.utcnow() - timedelta(days=7)

    weights = db.query(WeightLog).filter(
        WeightLog.user_id == user_id,
        WeightLog.created_at >= seven_days_ago
    ).order_by(
        WeightLog.created_at.asc()
    ).all()

    db.close()

    if len(weights) < 2:

        return (
            "Not enough weight data "
            "to calculate trend."
        )

    first_weight = weights[0].weight
    latest_weight = weights[-1].weight

    difference = round(
        latest_weight - first_weight,
        2
    )

    if difference < 0:

        return (
            f"You lost {abs(difference)} kg "
            f"in the last 7 days 📉"
        )

    elif difference > 0:

        return (
            f"You gained {difference} kg "
            f"in the last 7 days 📈"
        )

    else:

        return (
            "Your weight remained stable "
            "in the last 7 days."
        )