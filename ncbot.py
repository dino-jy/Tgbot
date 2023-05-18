import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '6276398338:AAGmAh2_g8gMc-JS-Lhmif2GVhPzEARpwYQ'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

subscription_plans = {
    'free': {
        'name': 'Free',
        'price': 0,
        'features': ['Feature 1', 'Feature 2'],
    },
    'premium': {
        'name': 'Premium',
        'price': 100,  # in-bot currency
        'features': ['Feature 1', 'Feature 2', 'Feature 3', 'Feature 4'],
    },
}

# This is an example of an in-memory user database. In a production application, you should use a persistent database.
user_database = {}

async def on_start(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_database:
        user_database[user_id] = {
            'balance': 0,
            'subscription': 'free',
        }
    await message.reply("Hello! I'm a Telegram bot. Use /subscribe to see subscription plans.")

async def on_subscribe(message: types.Message):
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_markup.add('Free', 'Premium')
    
    await message.reply("Choose your subscription plan:", reply_markup=keyboard_markup)

async def on_text(message: types.Message):
    user_id = message.from_user.id
    plan = subscription_plans.get(message.text.lower())
    if plan:
        if user_database[user_id]['subscription'] == message.text.lower():
            await message.reply('You are already subscribed to this plan.')
        elif plan['price'] == 0:
            user_database[user_id]['subscription'] = 'free'
            text = f"{plan['name']} Plan\nPrice: FREE\nFeatures:\n"
            for feature in plan['features']:
                text += f"- {feature}\n"
            await message.reply(text, parse_mode=ParseMode.MARKDOWN, reply_markup=types.ReplyKeyboardRemove())
        else:
            await start_premium_payment(message)
    else:
        await message.reply('Invalid subscription plan. Please use /subscribe to see available plans.')

async def start_premium_payment(message: types.Message):
    user_id = message.from_user.id
    plan = subscription_plans['premium']
    
    keyboard_markup = InlineKeyboardMarkup()
    keyboard_markup.add(InlineKeyboardButton("Pay with in-bot currency", callback_data="pay_premium"))
    
    text = f"{plan['name']} Plan\nPrice: {plan['price']} in-bot currency\nFeatures:\n"
    for feature in plan['features']:
        text += f"- {feature}\n"
        
    await message.reply(text, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard_markup)

async def on_callback_query(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    
    if callback_query.data == "pay_premium":
        price = subscription_plans['premium']['price']
        if user_database[user_id]['balance'] >= price:
            user_database[user_id]['balance'] -= price
            user_database[user_id]['subscription'] = 'premium'
            await bot.answer_callback_query(callback_query.id, text="Payment successful! You are now subscribed to the Premium plan.")
        else:
            await bot.answer_callback_query(callback_query.id, text="Insufficient balance. Please top up your in-bot currency.")
    else:
        await bot.answer_callback_query(callback_query.id, text="Invalid action.")

def main():
    from aiogram import types
    
    dp.register_message_handler(on_start, commands=['start', 'help'])
    dp.register_message_handler(on_subscribe, commands=['subscribe'])
    dp.register_message_handler(on_text, content_types=types.ContentType.TEXT)
    dp.register_callback_query_handler(on_callback_query)
    
    executor.start_polling(dp, skip_updates=True)
# ...

CHAT_HISTORY = {}  # This is an example of an in-memory chat history. In a production application, you should use a persistent database.

# ...

async def on_text(message: types.Message):

    user_id = message.from_user.id

    plan = subscription_plans.get(message.text.lower())

    if plan:

        # ...

    elif message.text.lower() == '/chat':

        await start_chat(message)

    elif message.text.lower() == '/history':

        await show_history(message)

    else:

        await message.reply('Invalid command. Please use /subscribe, /chat, or /history.')

async def start_chat(message: types.Message):

    user_id = message.from_user.id

    if user_database[user_id]['subscription'] == 'premium':

        await message.reply("You're now in chat mode. Send any message, and I'll store it. Type /history to view your chat history or /exit to exit chat mode.")

        dp.register_message_handler(on_chat_message, content_types=types.ContentType.TEXT, state=user_id)

    else:

        await message.reply('Sorry, the chat feature is only available for Premium subscribers.')

async def on_chat_message(message: types.Message, state):

    user_id = message.from_user.id

    if message.text.lower() == '/exit':

        dp.unregister_message_handler(on_chat_message, state=user_id)

        await message.reply('You have exited chat mode.')

    elif message.text.lower() == '/history':

        await show_history(message)

    else:

        if user_id not in CHAT_HISTORY:

            CHAT_HISTORY[user_id] = []

        CHAT_HISTORY[user_id].append(message.text)

        await message.reply('Message stored in chat history.')

async def show_history(message: types.Message):

    user_id = message.from_user.id

    if user_database[user_id]['subscription'] == 'premium':

        if user_id in CHAT_HISTORY and CHAT_HISTORY[user_id]:

            chat_history = '\n'.join(CHAT_HISTORY[user_id])

            await message.reply(f"Your chat history:\n\n{chat_history}")

        else:

            await message.reply('Your chat history is empty.')

    else:

        await message.reply('Sorry, the chat history feature is only available for Premium subscribers.')

# ...
if __name__ == '__main__':
    main()
