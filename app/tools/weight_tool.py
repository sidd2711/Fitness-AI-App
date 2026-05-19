from app.database import SessionLocal
from app.models import WeightLog


def log_weight(user_id, weight):

    db = SessionLocal()

    entry = WeightLog(
        user_id=user_id,
        weight=weight
    )

    db.add(entry)
    db.commit()
    db.close()

    return f"Weight logged: {weight} kg"