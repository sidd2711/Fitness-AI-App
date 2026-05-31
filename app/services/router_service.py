from app.tools.weight_tool import log_weight

from app.tools.water_tool import log_water

from app.tools.analytics_tool import (
    get_7_day_average_weight
)

from app.tools.trend_tool import (
    get_weight_trend
)

from app.tools.summary_tool import (
    summarize_day
)

from app.tools.meal_tool import log_meal

from app.tools.goal_tool import (
    set_weight_goal,
    show_goal_progress
)


def execute_actions(user_id, actions):

    responses = []

    for action in actions:

        intent = action.get("intent")

        # =====================
        # LOG WEIGHT
        # =====================

        if intent == "log_weight":

            weight = action.get("weight")

            if weight is None:

                responses.append(
                    "Could not detect weight."
                )

            else:

                response = log_weight(
                    user_id=user_id,
                    weight=weight
                )

                responses.append(response)

        # =====================
        # LOG WATER
        # =====================

        elif intent == "log_water":

            liters = action.get("liters")

            if liters is None:

                responses.append(
                    "Could not detect water intake."
                )

            else:

                response = log_water(
                    user_id=user_id,
                    liters=liters
                )

                responses.append(response)

        # =====================
        # 7 DAY AVERAGE
        # =====================

        elif intent == "average_weight":

            response = (
                get_7_day_average_weight(
                    user_id=user_id
                )
            )

            responses.append(response)

        # =====================
        # WEIGHT TREND
        # =====================

        elif intent == "weight_trend":

            response = get_weight_trend(
                user_id=user_id
            )

            responses.append(response)

        # =====================
        # DAILY SUMMARY
        # =====================

        elif intent == "daily_summary":

            response = summarize_day(
                user_id=user_id
            )

            responses.append(response)
        elif intent == "log_meal":

            meal_text = action.get("meal_text")

            if not meal_text:

                responses.append(
                    "Could not detect meal."
                )

            else:

                response = log_meal(
                    user_id=user_id,
                    meal_text=meal_text
                )

                responses.append(response)
        elif intent == "set_goal":

            target_weight = action.get(
                "target_weight"
            )

            if target_weight is None:

                responses.append(
                    "Could not detect target weight."
                )

            else:

                response = set_weight_goal(
                    user_id=user_id,
                    target_weight=target_weight
                )

                responses.append(response)
        elif intent == "show_progress":

            response = show_goal_progress(
                user_id=user_id
            )

            responses.append(response)
        # =====================
        # UNKNOWN INTENT
        # =====================

        else:

            responses.append(
                f"Unknown intent: {intent}"
            )

    # =====================
    # FALLBACK
    # =====================

    if not responses:

        responses.append(
            (
                "I can currently help with:\n"
                "- Weight logging\n"
                "- Water tracking\n"
                "- Average weight\n"
                "- Weight trends\n"
                "- Daily summaries\n"
                "- Goal tracking"
            )
        )

    return "\n".join(responses)