import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
)

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Replace with your bot token
TOKEN = "6276398338:AAGmAh2_g8gMc-JS-Lhmif2GVhPzEARpwYQ"

# Subscription plans
SUBSCRIPTION_PLANS = {
    "basic": {"price": 10, "duration": "1 month"},
    "premium": {"price": 20, "duration": "1 month"},
}

# In-memory user data storage (replace with a database for a production bot)
user_data = {}


def start(update: Update, context: CallbackContext):
    """Send a message with a subscription plan when the command /start is issued."""
    keyboard = [
        [
            InlineKeyboardButton(
                f"Basic Plan (${SUBSCRIPTION_PLANS['basic']['price']}/month)",
                callback_data="basic",
            ),
            InlineKeyboardButton(
                f"Premium Plan (${SUBSCRIPTION_PLANS['premium']['price']}/month)",
                callback_data="premium",
            ),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Choose a subscription plan:", reply_markup=reply_markup)


def plan_callback(update: Update, context: CallbackContext):
    """Handle the user's plan choice."""
    query = update.callback_query
    query.answer()

    plan = query.data

    if plan == "basic" or plan == "premium":
        user_data[query.from_user.id] = {"plan": plan}
        query.edit_message_text(
            text=f"Selected plan: {plan.capitalize()}.\n\nPlease send the payment of ${SUBSCRIPTION_PLANS[plan]['price']} to the following address: `your_payment_address_here`.",
            parse_mode=ParseMode.MARKDOWN,
        )


def message_handler(update: Update, context: CallbackContext):
    """Handle user messages."""
    if update.message.chat_id == YOUR_TELEGRAM_ID:
        # Handle admin messages (broadcast, etc.)
        pass
    else:
        # Handle user messages
        pass


def broadcast(update: Update, context: CallbackContext):
    """Broadcast a message to all users."""
    if update.message.chat_id == YOUR_TELEGRAM_ID:
        message = update.message.text[10:]

        for user_id in user_data:
            context.bot.send_message(chat_id=user_id, text=message)


def main():
    """Start the bot."""
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(plan_callback))
    dp.add_handler(CommandHandler("broadcast", broadcast))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
