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
                "content": "Return JSON only."
            },
            {
                "role": "user",
                "content": f"""
                Examples:

                "Weight is 102"
                {{"intent":"log_weight","weight":102}}

                "Drank 3L water"
                {{"intent":"log_water","liters":3}}

                Message:
                {user_message}
                """
            }
        ]
    )

    content = response.choices[0].message.content

    return json.loads(content)