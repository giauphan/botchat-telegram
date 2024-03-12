import telebot
from dotenv import load_dotenv
import logging
import asyncio
import sys
from datetime import datetime
from Model.Chat import ChatModel as Chat
from Model.Spending import Spending
from app.feat.user import get_info_user,set_up_email,set_up_name ,get_full_name

load_dotenv()

logging.basicConfig(
    filename="log/bot.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(os.getenv("api_token"))

async def save_chat(message):
    try:
        full_name = get_full_name(message.from_user)
        user = await get_info_user(full_name)
        await Chat.objects.create(user_id=user, message=message.text)
        log(message)
    except Exception as e:
        logger.error(f"Error saving chat: {e}")

async def send_statistics(message):
    try:
        full_name = get_full_name(message.from_user)
        user = await get_info_user(full_name)
        if user:
            num_messages = await Chat.objects.filter(user_id=user).count()
            bot.reply_to(
                message, f"You have sent {num_messages} messages in this chat."
            )
        else:
            bot.reply_to(message, "You haven't sent any messages yet.")
    except Exception as e:
        logger.error(f"Error retrieving statistics: {e}")


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    full_name = get_full_name(message.from_user)
    user = asyncio.run(get_info_user(full_name))
    reply = f"Howdy {user.name}, how are you doing?"
    bot.reply_to(message, reply)

@bot.message_handler(commands=["spending"])
def record_spending(message):
    bot.reply_to(message, "Hello, please record your spending today!")
    bot.register_next_step_handler(message, lambda msg: asyncio.run(save_spending(msg)))

async def save_spending(message):
    try:
        full_name = get_full_name(message.from_user)
        user = await get_info_user(full_name)
        money_spent = float(message.text)
        await Spending.objects.create(user_id=user, money=money_spent)
        log(message)
        bot.reply_to(message, f"{user.name} spending has been recorded successfully!")
    except Exception as e:
        logger.error(f"Error saving spending: {e}")
        bot.reply_to(
            message,
            "An error occurred while saving your spending. Please try again later.",
        )

@bot.message_handler(commands=["get_spending"])
def record_spending(message):
    bot.reply_to(message, "Hello, what day do you want to check your spending?")
    bot.register_next_step_handler(message, lambda msg: asyncio.run(get_spending(msg)))

async def get_spending(message):
    try:
        full_name = get_full_name(message.from_user)
        user = await get_info_user(full_name)
        spending = await Spending.objects.filter(user_id=user).all()
        date_str = message.text
        date = datetime.strptime(date_str, "%d/%m/%Y")
        money = sum(s.money for s in spending if s.created_at.strftime("%Y-%m-%d") == date.strftime("%Y-%m-%d"))
        if money != 0:
            format_money = "{:,.3f}".format(money) + "vnđ"
            bot.reply_to(message, f"{user.name} spending date {date}: {format_money}")
        else:
            bot.reply_to(message, f"find not found date: {date}")
    except Exception as e:
        logger.error(f"Error retrieving spending: {e}")
        bot.reply_to(
            message,
            "An error occurred while retrieving your spending. Please try again later.",
        )

@bot.message_handler(commands=["set_email"])
def set_email(message):
    bot.reply_to(message, "Hello, please enter your email.")
    bot.register_next_step_handler(message, lambda msg: asyncio.run(set_user_email(msg)))

async def set_user_email(message):
    full_name = get_full_name(message.from_user)
    await set_up_email(full_name, message.text)
    bot.reply_to(message, f"{full_name} set email successfully!")

@bot.message_handler(commands=["set_name"])
def set_name(message):
    bot.reply_to(message, "Hello, please enter your name.")
    bot.register_next_step_handler(message, lambda msg: asyncio.run(set_user_name(msg)))

async def set_user_name(message):
    full_name = get_full_name(message.from_user)
    await set_up_name(full_name, message.text)
    bot.reply_to(message, f"{full_name} set name successfully!")

@bot.message_handler(commands=["show_info"])
def show_info(message):
    full_name = get_full_name(message.from_user)
    user = asyncio.run(get_info_user(full_name))
    bot.reply_to(message, f"\t Info of {user.name} \n Name: {user.name} \n Username: {user.username} \n Email: {user.email}")

@bot.message_handler(commands=["statistical"])
def run_statistics(message):
    asyncio.run(send_statistics(message))

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    asyncio.run(save_chat(message))
    bot.reply_to(message, message.text)

def log(message):
    try:
        logger.info(f"Message from {message.from_user.first_name}: {message.text} {sys.version_info}")
    except Exception as e:
        logger.error(f"Error logging message: {e}")

if __name__ == "__main__":
    bot.infinity_polling()
