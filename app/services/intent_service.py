from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def classify_intent(user_message):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",

        response_format={
            "type": "json_object"
        },

        messages=[
            {
                "role": "system",
                "content": """
                You are an intent extraction engine.

                Allowed intents:
                - log_weight
                - log_water
                - average_weight
                - weight_trend

                Rules:
                - Extract ALL actions.
                - Return ONLY valid JSON.
                - Do not invent actions.
                """
            },
            {
                "role": "user",
                "content": f"""
                Message:
                Weight is 102 and drank 3L water

                Response:
                {{
                    "actions": [
                        {{
                            "intent": "log_weight",
                            "weight": 102
                        }},
                        {{
                            "intent": "log_water",
                            "liters": 3
                        }}
                    ]
                }}

                Message:
                Show my 7 day average weight

                Response:
                {{
                    "actions": [
                        {{
                            "intent": "average_weight"
                        }}
                    ]
                }}

                Message:
                How is my weight trend?

                Response:
                {{
                    "actions": [
                        {{
                            "intent": "weight_trend"
                        }}
                    ]
                }}

                Now analyze this message:

                {user_message}
                """
            }
        ]
    )

    content = response.choices[0].message.content

    print("\n===== RAW LLM RESPONSE =====")
    print(content)

    return json.loads(content)