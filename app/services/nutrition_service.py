from openai import OpenAI
from dotenv import load_dotenv

import os
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def estimate_nutrition(meal_text):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        response_format={
            "type": "json_object"
        },
        messages=[
            {
                "role": "system",
                "content": (
                    "Estimate meal nutrition. "
                    "Return JSON only."
                )
            },
            {
                "role": "user",
                "content": f"""
                Meal:
                {meal_text}

                Return format:
                {{
                    "calories": 500,
                    "protein": 35
                }}
                """
            }
        ]
    )

    content = response.choices[0].message.content

    return json.loads(content)