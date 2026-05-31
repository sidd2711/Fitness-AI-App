def extract_analytics(user_message):

    message = user_message.lower()

    if (
        "average" in message
        or "avg" in message
    ):

        return {
            "actions": [
                {
                    "intent": "average_weight"
                }
            ]
        }

    if "trend" in message:

        return {
            "actions": [
                {
                    "intent": "weight_trend"
                }
            ]
        }

    return {"actions": []}