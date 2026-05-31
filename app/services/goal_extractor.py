import re


def extract_goal(user_message):

    match = re.search(
        r"(\d+(\.\d+)?)",
        user_message
    )

    if not match:

        return None

    return {
        "actions": [
            {
                "intent": "set_goal",
                "target_weight":
                    float(match.group(1))
            }
        ]
    }