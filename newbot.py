import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor

API_TOKEN = '6276398338:AAGmAh2_g8gMc-JS-Lhmif2GVhPzEARpwYQ'

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# User data and chat history dictionaries (Replace with a persistent database)
user_data = {}
chat_history = {}

# Subscription plans (Modify as needed)
subscription_plans = {
    'premium': 'Premium Plan - All features'
}

# Start command
@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    text = ("*🚀 Welcome to the Premium Subscription Chat Bot!*\n\n"
            "📚 Use /subscription to view available subscription plans.\n"
            "💬 Use /chat to chat with other users.")
    await message.reply(text, parse_mode=ParseMode.MARKDOWN)

# Help command
@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    text = ("*📖 List of available commands:*\n\n"
            "/start - Show the welcome message\n"
            "/help - Show this help message\n"
            "/subscription - Show available subscription plans\n"
            "/chat - Chat with other users")
    await message.reply(text, parse_mode=ParseMode.MARKDOWN)

# Subscription command
@dp.message_handler(commands=['subscription'])
async def subscription(message: types.Message):
    text = "*💎 Available subscription plans:*\n\n"

    for plan, features in subscription_plans.items():
        text += f"*{plan.capitalize()}*:\n{features}\n\n"
    text += "To upgrade to Premium, type `/upgrade` and follow the instructions."

    await message.reply(text, parse_mode=ParseMode.MARKDOWN)

# Upgrade command
@dp.message_handler(commands=['upgrade'])
async def upgrade(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {'subscription': 'premium'}
    text = "Congratulations! 🎉 Your premium subscription has been activated. Use /chat to start chatting with other users."
    await message.reply(text, parse_mode=ParseMode.MARKDOWN)

# Chat feature
@dp.message_handler(lambda message: message.text.startswith('/chat'))
async def chat_command(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_data or user_data[user_id]['subscription'] != 'premium':
        await message.reply("You need to have a premium subscription to use the chat feature. Use /subscription to view the available plan.")
    else:
        await message.reply("Enter your message to start chatting:")

# Handle chat messages
@dp.message_handler(lambda message: message.from_user.id in user_data and user_data[message.from_user.id]['subscription'] == 'premium')
async def chat(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    chat_text = message.text

    if chat_id not in chat_history:
        chat_history[chat_id] = []

    chat_history[chat_id].append((user_id, chat_text))

    response = f"{message.from_user.first_name}: {chat_text}"
    for user, _ in chat_history[chat_id]:
        if user != user_id:
            await bot.send_message(user, response)

# Run the bot
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
