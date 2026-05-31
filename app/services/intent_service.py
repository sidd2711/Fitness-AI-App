from app.services.router_classifier import (
    classify_route
)

from app.services.logging_extractor import (
    extract_logging_actions
)

from app.services.goal_extractor import (
    extract_goal
)

from app.services.analytics_extractor import (
    extract_analytics
)

from app.services.summary_extractor import (
    extract_summary
)

def classify_intent(user_message):

    route = classify_route(user_message)

    if route == "summary":
        return extract_summary()

    if route == "goal":
        return extract_goal(user_message)

    if route == "analytics":
        return extract_analytics(user_message)

    if route == "logging":
        return extract_logging_actions(user_message)
    if route == "progress":
        return {
            "actions": [
                {
                    "intent": "show_progress"
                }
            ]
        }

    return {
        "actions": []
    }