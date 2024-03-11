import telebot
import os
from dotenv import load_dotenv
import logging
import asyncio
import sys
import re
import unicodedata
from migrations.create_table import check_connect
from Model.Chat import ChatModel as Chat
from Model.User import UserModel as User
from Model.Spending import Spending as Spending
from datetime import datetime

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
        user, created = await User.objects.get_or_create(
            username=slugify(full_name), defaults={"name": full_name}
        )
        chat = await Chat.objects.create(user_id=user, message=message.text)
        log(message)
    except Exception as e:
        logger.error(f"Error saving chat: {e}")


def get_full_name(user):
    if user.last_name:
        return f"{user.first_name} {user.last_name}"
    else:
        return user.first_name


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add("/statistical")
    bot.reply_to(message, "Howdy, how are you doing?", reply_markup=keyboard)


async def send_statistics(message):
    try:
        full_name = message.from_user.first_name + message.from_user.last_name
        user = await User.objects.filter(username=slugify(full_name)).first()
        if user:
            num_messages = await Chat.objects.filter(user_id=user).count()
            bot.reply_to(
                message, f"You have sent {num_messages} messages in this chat."
            )
        else:
            bot.reply_to(message, "You haven't sent any messages yet.")
    except Exception as e:
        logger.error(f"Error retrieving statistics: {e}")


def slugify(text):
    """
    Generate a slug from the given text.
    """
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    text = re.sub(r"[-\s]+", "_", text)
    return text


try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=["spending"])
def record_spending(message):
    bot.reply_to(message, "Hello, please record your spending today!")
    bot.register_next_step_handler(message, lambda msg: asyncio.run(save_spending(msg)))


async def save_spending(message):
    try:
        full_name = get_full_name(message.from_user)
        user, created = await User.objects.get_or_create(
            username=slugify(full_name), defaults={"name": full_name}
        )
        money_spent = float(message.text)
        print(money_spent)
        await Spending.objects.create(user_id=user, money=money_spent)
        log(message)
        bot.reply_to(message, "Your spending has been recorded successfully!")
    except Exception as e:
        logger.error(f"Error saving spending: {e}")
        bot.reply_to(
            message,
            "An error occurred while saving your spending. Please try again later.",
        )


@bot.message_handler(commands=["get_spending"])
def record_spending(message):
    bot.reply_to(message, "Hello, what day do you want to check your spending?")
    bot.register_next_step_handler(message, lambda msg: asyncio.run(Get_spending(msg)))


async def Get_spending(message):
    try:
        full_name = get_full_name(message.from_user)
        user = await User.objects.get(username=slugify(full_name))
        spending = await Spending.objects.filter(user_id=user).all()
        date_str = message.text
        date = datetime.strptime(date_str, "%d/%m/%Y")
        money = 0
        for get_spending in spending:
            get_spending_date = get_spending.created_at.strftime("%Y-%m-%d")
            print(get_spending_date, date)
            if date.strftime("%Y-%m-%d") == get_spending_date:
                money += get_spending.money
        if money != 0:
            formatMoney = "{:,.3f}".format(money) + "vnđ"
            bot.reply_to(message, f"spending date {date}: {formatMoney}")
        else:
            bot.reply_to(message, f"find not found date: {date}")
    except Exception as e:
        logger.error(f"Error saving spending: {e}")
        bot.reply_to(
            message,
            "An error occurred while saving your spending. Please try again later.",
        )


@bot.message_handler(commands=["statistical"])
def runStatistics(message):
    asyncio.run(send_statistics(message))


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    asyncio.run(save_chat(message))
    bot.reply_to(message, message.text)


def log(message):
    try:
        te = sys.version_info
        logger.info(f"Message from {message.from_user.first_name}: {message.text} {te}")
    except Exception as e:
        logger.error(f"Error logging message: {e}")


if __name__ == "__main__":
    bot.infinity_polling()
