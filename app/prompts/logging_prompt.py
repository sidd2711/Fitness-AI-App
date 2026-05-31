LOGGING_PROMPT = """
Extract fitness logging actions.

Return JSON only.

Supported intents:
- log_weight
- log_water
- log_meal

Schema:

{
  "actions": [
    {
      "intent": "<intent_name>"
    }
  ]
}

Examples:

weight 101
{
  "actions":[
    {
      "intent":"log_weight",
      "weight":101
    }
  ]
}

water 3L
{
  "actions":[
    {
      "intent":"log_water",
      "liters":3
    }
  ]
}

weight 101 and water 3L
{
  "actions":[
    {
      "intent":"log_weight",
      "weight":101
    },
    {
      "intent":"log_water",
      "liters":3
    }
  ]
}

4 eggs and whey protein
{
  "actions":[
    {
      "intent":"log_meal",
      "meal_text":"4 eggs and whey protein"
    }
  ]
}

Rules:
- Use intent, never type.
- Use weight for log_weight.
- Use liters for log_water.
- Use meal_text for log_meal.
- Return only valid JSON.
"""