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

from app.services.intent_service import classify_intent
from app.tools.water_tool import log_water
from app.tools.weight_tool import log_weight

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Fitness Agent Activated 💪"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # Telegram unique user id
    user_id = str(update.effective_user.id)

    try:

        # STEP 1 → Understand user intent
        intent_data = classify_intent(user_message)

        print(intent_data)

        intent = intent_data.get("intent")

        # STEP 2 → Route to correct tool

        if intent == "log_weight":

            weight = intent_data.get("weight")

            if weight is None:

                response = "I could not detect your weight."

            else:

                response = log_weight(
                    user_id=user_id,
                    weight=weight
                )

        elif intent == "log_water":

            liters = intent_data.get("liters")

            if liters is None:
                response = "I could not detect your water intake."
            else:
                response = log_water(
                    user_id=user_id,
                    liters=liters
                )

        else:

            response = (
                "I can currently help with:\n"
                "- Weight logging\n"
                "- Water tracking\n"
                "- Fitness tracking"
            )

    except Exception as e:

        import traceback

        print("\n===== ERROR =====")
        traceback.print_exc()
        print("=================\n")

        response = f"Error: {str(e)}"

    # STEP 3 → Send reply back to Telegram
    await update.message.reply_text(response)


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_message))

print("Bot running...")

app.run_polling()
