from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime
)

from datetime import datetime

from app.database import Base


class WaterLog(Base):

    __tablename__ = "water_logs"

    id = Column(Integer, primary_key=True)

    user_id = Column(String)

    liters = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )