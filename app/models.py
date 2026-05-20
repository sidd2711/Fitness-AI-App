from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime

Base = declarative_base()

class WeightLog(Base):
    __tablename__ = "weight_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    weight = Column(Float)
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class WaterLog(Base):
    __tablename__ = "water_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    liters = Column(Float)
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

class UserProfile(Base):

    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True)

    user_id = Column(String, unique=True)

    height_cm = Column(Float)

    age = Column(Integer)

    gender = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )