from app.database import SessionLocal
from app.models import WeightLog

from datetime import datetime, timedelta
from sqlalchemy import func


def get_7_day_average_weight(user_id):

    db = SessionLocal()

    seven_days_ago = datetime.utcnow() - timedelta(days=7)

    average_weight = db.query(
        func.avg(WeightLog.weight)
    ).filter(
        WeightLog.user_id == user_id,
        WeightLog.created_at >= seven_days_ago
    ).scalar()

    db.close()

    if average_weight is None:

        return "No weight data found for last 7 days."

    return (
        f"Your 7-day average weight is "
        f"{round(average_weight, 2)} kg"
    )