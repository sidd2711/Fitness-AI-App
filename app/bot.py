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

from app.services.intent_service import (
    classify_intent
)

from app.services.onboarding_service import (
    handle_onboarding
)

from app.services.router_service import (
    execute_actions
)

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# =========================
# START COMMAND
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "Fitness Agent Activated 💪"
    )


# =========================
# MAIN MESSAGE HANDLER
# =========================

async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_message = update.message.text

    # UNIQUE TELEGRAM USER ID
    user_id = str(update.effective_user.id)
    user_name = str(update.effective_user.first_name)

    print("\n===== NEW MESSAGE =====")
    print("User:", user_message)
    print("Name:",user_name)

    try:

        # =========================
        # STEP 1 → ONBOARDING FLOW
        # =========================

        onboarding_handled = (
            await handle_onboarding(
                update=update,
                user_id=user_id,
                user_name=user_name,
                user_message=user_message
            )
        )

        # STOP NORMAL FLOW
        if onboarding_handled:
            return

        # =========================
        # STEP 2 → CLASSIFY INTENT
        # =========================

        intent_data = classify_intent(
            user_message
        )

        print("\n===== INTENT DATA =====")
        print(intent_data)

        # =========================
        # STEP 3 → EXTRACT ACTIONS
        # =========================

        if not isinstance(
            intent_data,
            dict
        ):

            intent_data = {
                "actions": []
            }

        actions = intent_data.get(
            "actions",
            []
        )

        # =========================
        # STEP 4 → EXECUTE ROUTER
        # =========================

        final_response = execute_actions(
            user_id=user_id,
            actions=actions
        )

    except Exception as e:

        print("\n===== ERROR =====")
        traceback.print_exc()
        print("=================\n")

        final_response = (
            f"Something went wrong:\n{str(e)}"
        )

    # =========================
    # STEP 5 → SEND RESPONSE
    # =========================

    await update.message.reply_text(
        final_response
    )


# =========================
# CREATE TELEGRAM APP
# =========================

app = (
    ApplicationBuilder()
    .token(BOT_TOKEN)
    .build()
)


# =========================
# COMMAND ROUTES
# =========================

app.add_handler(
    CommandHandler("start", start)
)


# =========================
# MESSAGE ROUTES
# =========================

app.add_handler(
    MessageHandler(
        filters.TEXT,
        handle_message
    )
)


print("Bot running... 🚀")


# =========================
# START BOT
# =========================

app.run_polling()