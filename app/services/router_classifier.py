def classify_route(user_message):

    message = user_message.lower()

    # SUMMARY

    if (
        "summary" in message
        or "summarise" in message
        or "summarize" in message
    ):
        return "summary"

    # PROGRESS

    if (
        "progress" in message
        or "how far am i" in message
        or "remaining" in message
    ):
        return "progress"

    # GOALS

    if (
        "target weight" in message
        or "goal weight" in message
        or "my goal" in message
    ):
        return "goal"

    
    # ANALYTICS

    if (
        "average" in message
        or "trend" in message
    ):
        return "analytics"

    # EVERYTHING ELSE

    return "logging"