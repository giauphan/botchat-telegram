import telebot
import os
from dotenv import load_dotenv
import logging
import asyncio ,sys,re, unicodedata
load_dotenv()

from Model.Chat import ChatModel as Chat
from Model.User import UserModel as User

# Configure logging
logging.basicConfig(filename='bot.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(os.getenv('api_token'))

async def save_chat(message):
    # try:
        full_name = message.from_user.first_name + message.from_user.last_name
        user, created = await User.objects.get_or_create(username=slugify(full_name), defaults={'name': full_name})
        chat = await Chat.objects.create(user_id=user, message=message.text)
        log(message)
    # except Exception as e:
    #     logger.error(f"Error saving chat: {e}")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

async def send_statistics(message):
    try:
        full_name = message.from_user.first_name + message.from_user.last_name
        user = await User.objects.filter(username=slugify(full_name)).first()
        if user:
            num_messages = await Chat.objects.filter(user_id=user).count()
            bot.reply_to(message, f"You have sent {num_messages} messages in this chat.")
        else:
            bot.reply_to(message, "You haven't sent any messages yet.")
    except Exception as e:
        logger.error(f"Error retrieving statistics: {e}")

def slugify(text):
    """
    Generate a slug from the given text.
    """
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    text = re.sub(r'[-\s]+', '_', text)
    return text

if sys.version_info < (3,  10):
    loop = asyncio.get_event_loop()
else:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

@bot.message_handler(commands=['statistical'])
def runStatistics(message):
    loop.run_until_complete(send_statistics(message))

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    loop.run_until_complete(save_chat(message))
    bot.reply_to(message, message.text)


def log(message):
    try:
        logger.info(f"Message from {message.from_user.first_name}: {message.text}")
    except Exception as e:
        logger.error(f"Error logging message: {e}")

bot.infinity_polling()
