from app.database import SessionLocal
from app.models import WaterLog

def log_water(user_id, liters):

    db = SessionLocal()

    entry = WaterLog(
        user_id=user_id,
        liters=liters
    )

    db.add(entry)
    db.commit()
    db.close()

    return f"Water logged: {liters} liters"