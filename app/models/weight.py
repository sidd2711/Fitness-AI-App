from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime
)

from datetime import datetime

from app.database import Base


class WeightLog(Base):

    __tablename__ = "weight_logs"

    id = Column(Integer, primary_key=True)

    user_id = Column(String)

    weight = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )