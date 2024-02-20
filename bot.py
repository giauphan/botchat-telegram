import telebot
import os
from dotenv import load_dotenv
from collections import defaultdict
import logging

load_dotenv()

# Configure logging
logging.basicConfig(filename='bot.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(os.getenv('api_token'))

user_stats = defaultdict(int)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")
     
@bot.message_handler(commands=['statistical'])
def send_welcome(message):
	send_statistics(message)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_stats[message.from_user.id] += 1
    bot.reply_to(message, message.text)
    log(message)

def log(message):
    logger.info(f"Message from {message.from_user.first_name}: {message.text}")

def send_statistics(message):
    user_id = message.from_user.id
    num_messages = user_stats[user_id]
    bot.reply_to(message, f"You have sent {num_messages} messages in this chat.")
	
def log(message):
    logger.info(f"Message from {message.chat.id}: {message}")

bot.infinity_polling()