from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime
)

from datetime import datetime

from app.database import Base


class Goal(Base):

    __tablename__ = "goals"

    id = Column(Integer, primary_key=True)

    user_id = Column(String)

    target_weight = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )