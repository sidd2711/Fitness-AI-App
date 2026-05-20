from app.tools.profile_tool import (
    get_user_profile,
    create_user_profile
)

# TEMPORARY IN-MEMORY STATE
user_onboarding_state = {}


async def handle_onboarding(
    update,
    user_id,
    user_message
):

    profile = get_user_profile(user_id)

    # USER ALREADY EXISTS
    if profile:

        return False

    state = user_onboarding_state.get(user_id)

    # STEP 1 → ASK HEIGHT
    if state is None:

        user_onboarding_state[user_id] = {
            "step": "height"
        }

        await update.message.reply_text(
            "Welcome 💪\n\n"
            "Let's setup your profile.\n"
            "What is your height in cm?"
        )

        return True

    # STEP 2 → SAVE HEIGHT
    elif state["step"] == "height":

        try:

            height_cm = float(user_message)

            if height_cm < 100 or height_cm > 250:

                await update.message.reply_text(
                    "Please enter realistic height in cm."
                )

                return True

            state["height_cm"] = height_cm
            state["step"] = "age"

            await update.message.reply_text(
                "Great 👍\n"
                "What is your age?"
            )

            return True

        except:

            await update.message.reply_text(
                "Please enter valid height."
            )

            return True

    # STEP 3 → SAVE AGE
    elif state["step"] == "age":

        try:

            age = int(user_message)

            if age < 10 or age > 100:

                await update.message.reply_text(
                    "Please enter valid age."
                )

                return True

            state["age"] = age
            state["step"] = "gender"

            await update.message.reply_text(
                "What is your gender?"
            )

            return True

        except:

            await update.message.reply_text(
                "Please enter valid age."
            )

            return True

    # STEP 4 → SAVE GENDER
    elif state["step"] == "gender":

        gender = user_message.lower()

        allowed_genders = [
            "male",
            "female",
            "other"
        ]

        if gender not in allowed_genders:

            await update.message.reply_text(
                "Please enter:\n"
                "- male\n"
                "- female\n"
                "- other"
            )

            return True

        create_user_profile(
            user_id=user_id,
            height_cm=state["height_cm"],
            age=state["age"],
            gender=gender
        )

        del user_onboarding_state[user_id]

        await update.message.reply_text(
            "Profile setup completed ✅\n\n"
            "You can now start logging fitness data."
        )

        return True