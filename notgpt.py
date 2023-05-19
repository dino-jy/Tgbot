import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, filters
import logging
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Your bot token
BOT_TOKEN = '6276398338:AAGmAh2_g8gMc-JS-Lhmif2GVhPzEARpwYQ'

# Admin chat ID 
ADMIN_CHAT_ID = '6270279846'

# Database to store user balances 
database = {'user1': 100, 'user2': 200}

# Function to process payments 
def process_payment(user_id, amount):
    if user_id in database:
        balance = database[user_id]
        if balance >= amount:
            database[user_id] = balance - amount
            return f'Payment of {amount} coins successful!'
        else:
            return f'Not enough coins! You have {balance} coins.'
    else:
        return 'User not found!'

# Admin commands 
def add_coins(update, context):
    """Add coins to user"""
    if update.message.chat_id == ADMIN_CHAT_ID:
        user_id = update.message.text.split()[1]
        amount = int(update.message.text.split()[2])
        if user_id in database:
            database[user_id] += amount 
            update.message.reply_text(f'Added {amount} coins to user {user_id}.')
        else:
            database[user_id] = amount
            update.message.reply_text(f'Created user {user_id} and added {amount} coins.')

# User commands         
def pay(update, context):
    """Deduct coins from user"""
    user_id = update.message.from_user.id
    amount = int(update.message.text.split()[1])
    message = process_payment(user_id, amount)
    update.message.reply_text(message)   

# Logging 
def log(update, context):
    logger.info(update.message)

def main():
    # Create bot 
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add admin commands 
    dp.add_handler(CommandHandler('add_coins', add_coins))

    # Add user commands 
    dp.add_handler(CommandHandler('pay', pay))

    # Log all messages 
    dp.add_handler(MessageHandler(Filters.all, log))

    # Start bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
