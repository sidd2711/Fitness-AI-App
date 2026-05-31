from openai import OpenAI
from dotenv import load_dotenv

from app.prompts.logging_prompt import LOGGING_PROMPT

import json
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def extract_logging_actions(user_message):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",

        response_format={
            "type": "json_object"
        },

        messages=[
            {
                "role": "system",
                "content": LOGGING_PROMPT
            },
            {
                "role": "user",
                "content": f"""
                Return JSON only.

                Message:
                {user_message}
                """
            }
        ]
    )

    content = response.choices[0].message.content

    if not content:
        raise Exception(
            "Empty response from model"
        )

    result = json.loads(content)

    for action in result.get("actions", []):

        if "type" in action:

            action["intent"] = action.pop("type")

        if (
            action.get("intent") == "log_weight"
            and "value" in action
        ):
            action["weight"] = action.pop("value")

        if (
            action.get("intent") == "log_water"
            and "value" in action
        ):
            action["liters"] = action.pop("value")

    print("LOGGING EXTRACTOR:")
    print(result)

    return result