import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor

API_TOKEN = '6276398338:AAGmAh2_g8gMc-JS-Lhmif2GVhPzEARpwYQ'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

subscription_plans = {
    'free': {
        'name': 'Free',
        'price': '0',
        'features': ['Feature 1', 'Feature 2'],
    },
    'premium': {
        'name': 'Premium',
        'price': '10',
        'features': ['Feature 1', 'Feature 2', 'Feature 3', 'Feature 4'],
    },
}

async def on_start(message: types.Message):
    await message.reply("Hello! I'm a Telegram bot. Use /subscribe to see subscription plans.")

async def on_subscribe(message: types.Message):
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_markup.add('Free', 'Premium')
    
    await message.reply("Choose your subscription plan:", reply_markup=keyboard_markup)

async def on_text(message: types.Message):
    plan = subscription_plans.get(message.text.lower())
    if plan:
        text = f"{plan['name']} Plan\nPrice: ${plan['price']}\nFeatures:\n"
        for feature in plan['features']:
            text += f"- {feature}\n"
        await message.reply(text, parse_mode=ParseMode.MARKDOWN, reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.reply('Invalid subscription plan. Please use /subscribe to see available plans.')

def main():
    from aiogram import types
    
    dp.register_message_handler(on_start, commands=['start', 'help'])
    dp.register_message_handler(on_subscribe, commands=['subscribe'])
    dp.register_message_handler(on_text, content_types=types.ContentType.TEXT)
    
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()
