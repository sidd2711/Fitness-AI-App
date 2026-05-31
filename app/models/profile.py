from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime
)

from datetime import datetime

from app.database import Base


class UserProfile(Base):

    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        String,
        unique=True
    )

    first_name = Column(String)

    height_cm = Column(Float)

    age = Column(Integer)

    gender = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )