from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from dotenv import load_dotenv
import os
import traceback

from app.services.intent_service import classify_intent
from app.tools.weight_tool import log_weight
from app.tools.water_tool import log_water
from app.tools.analytics_tool import get_7_day_average_weight
from app.tools.trend_tool import get_weight_trend
from app.services.onboarding_service import handle_onboarding

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Fitness Agent Activated 💪"
    )


# MAIN MESSAGE HANDLER
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_message = update.message.text

    # Unique Telegram user id
    user_id = str(update.effective_user.id)

    # HANDLE ONBOARDING FLOW
    onboarding_handled = await handle_onboarding(
        update=update,
        user_id=user_id,
        user_message=user_message
    )

    # STOP FLOW IF ONBOARDING ACTIVE
    if onboarding_handled:
        return

    print("\n===== NEW MESSAGE =====")
    print("User:", user_message)

    try:

        # STEP 1 → Classify user intent
        intent_data = classify_intent(user_message)

        print("\n===== INTENT DATA =====")
        print(intent_data)

        # STEP 2 → Extract actions
        actions = intent_data.get("actions", [])

        responses = []

        # STEP 3 → Execute tools
        for action in actions:

            intent = action.get("intent")

            # WEIGHT LOGGING
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

            # WATER LOGGING
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
            elif intent == "average_weight":

                response = get_7_day_average_weight(
                    user_id=user_id
                )

                responses.append(response)
            elif intent == "weight_trend":

                response = get_weight_trend(
                    user_id=user_id
                )

                responses.append(response)
            # UNKNOWN INTENT
            else:

                responses.append(
                    f"Unknown intent: {intent}"
                )

        # STEP 4 → Fallback response
        if not responses:

            responses.append(
                (
                    "I can currently help with:\n"
                    "- Weight logging\n"
                    "- Water tracking\n"
                    "- Average weight\n"
                    "- Weight trends"
                )
            )

        # STEP 5 → Final response
        final_response = "\n".join(responses)

    except Exception as e:

        print("\n===== ERROR =====")
        traceback.print_exc()
        print("=================\n")

        final_response = (
            f"Something went wrong:\n{str(e)}"
        )

    # STEP 6 → Reply back to Telegram
    await update.message.reply_text(final_response)


# CREATE TELEGRAM APPLICATION
app = ApplicationBuilder().token(BOT_TOKEN).build()

# COMMAND ROUTES
app.add_handler(CommandHandler("start", start))

# MESSAGE ROUTES
app.add_handler(
    MessageHandler(filters.TEXT, handle_message)
)

print("Bot running... 🚀")

# START BOT
app.run_polling()