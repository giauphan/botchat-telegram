import telebot
from dotenv import load_dotenv
import logging
import asyncio
import os
import sys
from Model.Chat import ChatModel as Chat
from Model.Spending import Spending
from Model.Income import Income
from app.feat.user import getInfoUser, setUpName, setUpEmail, getFullName, UpdateMoney
from app.feat.spending import getSpendingDetail, formatMoney
from app.feat.Income import getIncomeDetail
from app.console.sendMailStatistical import sendMailUser

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
        full_name = getFullName(message.from_user)
        user = await getInfoUser(full_name)
        await Chat.objects.create(user_id=user, message=message.text)
        log(message)
    except Exception as e:
        logger.error(f"Error saving chat: {e}")


async def send_statistics(message):
    try:
        full_name = getFullName(message.from_user)
        user = await getInfoUser(full_name)
        if user:
            num_messages = await Chat.objects.filter(user_id=user).count()
            bot.reply_to(
                message, f"You have sent {num_messages} messages in this chat."
            )
        else:
            bot.send_message(message.chat.id, "You haven't sent any messages yet.")
    except Exception as e:
        logger.error(f"Error retrieving statistics: {e}")


@bot.message_handler(commands=["start"])
def send_welcome(message):
    full_name = getFullName(message.from_user)
    user = asyncio.run(getInfoUser(full_name))
    reply = f"Howdy {user.name}, how are you doing?"
    bot.send_message(message.chat.id, reply)


@bot.message_handler(commands=["help"])
def send_welcome(message):
    reply = f"\t You can control me by sending these commands: \n\n /start - Start bot  \n /statistical - Message statistics \n /spending  -  Give spending in day \n /get_spending - Get spending in day your need \n /send_spending - send email for user \n /set_email - Set email we can email for your  \n /show_info - Check info your"
    bot.send_message(message.chat.id, reply)


@bot.message_handler(commands=["spending"])
def record_spending(message):
    bot.send_message(message.chat.id, "Hello, please record your spending today!")
    bot.register_next_step_handler(message, lambda msg: asyncio.run(save_spending(msg)))


async def save_spending(message):
    try:
        full_name = getFullName(message.from_user)
        user = await getInfoUser(full_name)
        money_spent = float(message.text)
        bot.send_message(
            message.chat.id,
            f"{user.name} spending has been recorded successfully. Now, please enter any notes you have",
        )
        bot.register_next_step_handler(
            message, lambda msg: asyncio.run(save_notes(msg, money_spent, user))
        )
    except Exception as e:
        logger.error(f"Error saving spending: {e}")
        bot.reply_to(
            message,
            "An error occurred while saving your spending. Please try again later.",
        )


async def save_notes(message, money_spent, user):
    try:
        notes = message.text
        await Spending.objects.create(user_id=user, money=money_spent, notes=notes)
        account_balance = user.account_balance - money_spent
        await user.update(account_balance=account_balance)
        log(message)
        bot.send_message(
            message.chat.id,
            f"{user.name} spending notes has been recorded successfully!",
        )
    except Exception as e:
        logger.error(f"Error saving spending: {e}")
        bot.reply_to(
            message,
            "An error occurred while saving your spending. Please try again later.",
        )


@bot.message_handler(commands=["get_spending"])
def record_spending(message):
    bot.send_message(
        message.chat.id, "Hello, what day do you want to check your spending?"
    )
    bot.register_next_step_handler(message, lambda msg: asyncio.run(get_spending(msg)))


async def get_spending(message):
    try:
        full_name = getFullName(message.from_user)
        date_str = message.text
        spending = await getSpendingDetail(full_name, date_str)
        if spending:
            bot.reply_to(message, spending)
        else:
            bot.send_message(message.chat.id, f"find not found date: {date_str}")
    except Exception as e:
        logger.error(f"Error retrieving spending: {e}")
        bot.reply_to(
            message,
            "An error occurred while retrieving your spending. Please try again later.",
        )


@bot.message_handler(commands=["income"])
def record_income(message):
    bot.send_message(message.chat.id, "Hello, please record your income today!")
    bot.register_next_step_handler(message, lambda msg: asyncio.run(save_income(msg)))


async def save_income(message):
    try:
        full_name = getFullName(message.from_user)
        user = await getInfoUser(full_name)
        money_spent = float(message.text)
        bot.send_message(
            message.chat.id,
            f"{user.name} income has been recorded successfully. Now, please enter any notes you have",
        )
        bot.register_next_step_handler(
            message, lambda msg: asyncio.run(save_sources(msg, money_spent, user))
        )
    except Exception as e:
        logger.error(f"Error saving income: {e}")
        bot.reply_to(
            message,
            "An error occurred while saving your income. Please try again later.",
        )


async def save_sources(message, money_spent, user):
    try:
        source = message.text
        await Income.objects.create(user_id=user, amount=money_spent, source=source)
        account_balance = user.account_balance + money_spent
        await UpdateMoney(user.username, account_balance)
        log(message)
        bot.send_message(
            message.chat.id,
            f"{user.name} income source has been recorded successfully!",
        )
    except Exception as e:
        logger.error(f"Error saving income: {e}")
        bot.reply_to(
            message,
            "An error occurred while saving your income. Please try again later.",
        )


@bot.message_handler(commands=["get_income"])
def record_income(message):
    bot.send_message(
        message.chat.id, "Hello, what day do you want to check your income?"
    )
    bot.register_next_step_handler(message, lambda msg: asyncio.run(get_income(msg)))


async def get_income(message):
    try:
        full_name = getFullName(message.from_user)
        date_str = message.text
        income = await getIncomeDetail(full_name, date_str)
        if income:
            bot.reply_to(message, income)
        else:
            bot.send_message(message.chat.id, f"find not found date: {date_str}")
    except Exception as e:
        logger.error(f"Error retrieving income: {e}")
        bot.reply_to(
            message,
            "An error occurred while retrieving your income. Please try again later.",
        )


@bot.message_handler(commands=["set_email"])
def set_email(message):
    bot.send_message(message.chat.id, "Hello, please enter your email.")
    bot.register_next_step_handler(
        message, lambda msg: asyncio.run(set_user_email(msg))
    )


async def set_user_email(message):
    full_name = getFullName(message.from_user)
    await setUpEmail(full_name, message.text)
    bot.send_message(message.chat.id, f"{full_name} set email successfully!")


@bot.message_handler(commands=["set_name"])
def set_name(message):
    bot.send_message(message.chat.id, "Hello, please enter your name.")
    bot.register_next_step_handler(message, lambda msg: asyncio.run(set_user_name(msg)))


async def set_user_name(message):
    full_name = getFullName(message.from_user)
    await setUpName(full_name, message.text)
    bot.send_message(message.chat.id, f"{full_name} set name successfully!")


@bot.message_handler(commands=["show_info"])
def show_info(message):
    full_name = getFullName(message.from_user)
    user = asyncio.run(getInfoUser(full_name))
    bot.reply_to(
        message,
        f"\t Info of {user.name} \n Name: {user.name} \n Username: {user.username} \n Email: {user.email} \n account blade: {formatMoney(user.account_balance or 0)}",
    )


@bot.message_handler(commands=["statistical"])
def run_statistics(message):
    asyncio.run(send_statistics(message))


@bot.message_handler(commands=["send_spending"])
def run_statistics(message):
    full_name = getFullName(message.from_user)
    sendMailUser(full_name)
    bot.send_message(message.chat.id, f"we send speding to your email  successfully!")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    asyncio.run(save_chat(message))
    bot.send_message(message.chat.id, message.text)


def log(message):
    try:
        logger.info(
            f"Message from {message.from_user.first_name}: {message.text} {sys.version_info}"
        )
    except Exception as e:
        logger.error(f"Error logging message: {e}")


if __name__ == "__main__":
    bot.infinity_polling()
