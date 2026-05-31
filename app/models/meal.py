from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime
)

from datetime import datetime

from app.database import Base


class MealLog(Base):

    __tablename__ = "meal_logs"

    id = Column(Integer, primary_key=True)

    user_id = Column(String)

    meal_text = Column(String)

    calories = Column(Float)

    protein = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )