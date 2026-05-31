from app.database import SessionLocal

from app.models import (
    Goal,
    WeightLog
)


def set_weight_goal(
    user_id,
    target_weight
):

    db = SessionLocal()

    goal = Goal(
        user_id=user_id,
        target_weight=target_weight
    )

    db.add(goal)

    db.commit()

    db.close()

    return (
        "Goal saved 🎯\n"
        f"Target weight: "
        f"{target_weight} kg"
    )


def show_goal_progress(user_id):

    db = SessionLocal()

    # =====================
    # FETCH LATEST GOAL
    # =====================

    goal = db.query(Goal).filter(
        Goal.user_id == user_id
    ).order_by(
        Goal.created_at.desc()
    ).first()

    # =====================
    # FETCH LATEST WEIGHT
    # =====================

    latest_weight = db.query(
        WeightLog
    ).filter(
        WeightLog.user_id == user_id
    ).order_by(
        WeightLog.created_at.desc()
    ).first()

    db.close()

    # =====================
    # VALIDATIONS
    # =====================

    if not goal:

        return (
            "No goal found.\n"
            "Set one using:\n"
            "'My target weight is 90 kg'"
        )

    if not latest_weight:

        return (
            "Please log weight first."
        )

    # =====================
    # CALCULATE REMAINING
    # =====================

    remaining = round(
        latest_weight.weight
        - goal.target_weight,
        2
    )

    # =====================
    # BUILD RESPONSE
    # =====================

    return (
        "🎯 Goal Progress\n\n"
        f"Current Weight: "
        f"{latest_weight.weight} kg\n"
        f"Target Weight: "
        f"{goal.target_weight} kg\n\n"
        f"Remaining: "
        f"{remaining} kg"
    )