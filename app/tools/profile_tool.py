from app.database import SessionLocal
from app.models import UserProfile


def get_user_profile(user_id):

    db = SessionLocal()

    profile = db.query(UserProfile).filter(
        UserProfile.user_id == user_id
    ).first()

    db.close()

    return profile


def create_user_profile(
    user_id,
    height_cm,
    age,
    gender
):

    db = SessionLocal()

    profile = UserProfile(
        user_id=user_id,
        height_cm=height_cm,
        age=age,
        gender=gender
    )

    db.add(profile)

    db.commit()

    db.close()

    return (
        "Profile setup completed ✅"
    )