import telebot
import os
from dotenv import load_dotenv
from collections import defaultdict
import logging

load_dotenv()

from Model.Chat import ChatModel as Chat
from Model.User import UserModel as User
# Configure logging
logging.basicConfig(filename='bot.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(os.getenv('api_token'))

user_stats = Chat.objects.all()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")
     
@bot.message_handler(commands=['statistical'])
def send_welcome(message):
	send_statistics(message)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    full_name = message.from_user.first_name + message.from_user.last_name
    user_name = message.from_user.username
    if(User.CheckUser(user_name) == False):
        user = User.objects.create( name='"'+ full_name+'"', username='"'+ message.from_user.username+'"')
    else:
         user = User.objects.filter(username=user_name).first()
    chat = Chat.objects.create(user_id=user, message=message.text)
    bot.reply_to(message, message.text)
    log(chat)
        

def log(message):
    logger.info(f"Message from {message.from_user.first_name}: {message.text}")

def send_statistics(message):
    user_name = message.from_user.username
    num_messages = user_stats[user_name]
    bot.reply_to(message, f"You have sent {num_messages} messages in this chat.")
	
def log(message):
    logger.info(f"Message from {message.chat.id}: {message}")

bot.infinity_polling()