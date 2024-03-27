import telebot
from dotenv import load_dotenv
import asyncio
import os
from Model.Spending import Spending
from Model.Diary import Diary
from Model.Income import Income
from app.feat.user import getInfoUser, setUpName, setUpEmail, getFullName, UpdateMoney
from app.feat.spending import getSpendingDetail, formatMoney
from app.feat.Income import getIncomeDetail
from app.console.sendMailStatistical import sendMailUser, sendMailUserMonth
from app.feat.SaveLog import log, logger
from app.feat.Chat import statistics, saveChat
from app.feat.Diary import getDiaryDetail

load_dotenv()

bot = telebot.TeleBot(os.getenv("api_token"))


async def send_statistics(message):
    try:
        num_messages = await statistics(message)
        bot.reply_to(message, f"You have sent {num_messages} messages in this chat.")
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
    reply = f"\t You can control me by sending these commands: \n\n /start - Start bot  \n /statistical - Message statistics \n /spending  -  Give spending in day \n /expense <amount> <category> - Quick Give spending in day \n /get_spending - Get spending in day your need \n /send_spending - send email for user \n /set_email - Set email we can email for your  \n /show_info - Check info your \n /diary - notes diarys \n /get_diary - get notes diary"
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
        useraccount_balance = user.account_balance or 0
        account_balance = useraccount_balance - money_spent
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
        message.chat.id,
        "Hello, what day do you want to check your spending? Date format: day/month/year?",
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
            "Invalid expense format. Usage: day/month/year.",
        )


@bot.message_handler(commands=["expense"])
def record_quick_expense(message):
    try:
        parts = message.text.split(" ", 2)
        amount = float(parts[1])
        category = parts[2] if len(parts) > 2 else "Uncategorized"

        full_name = getFullName(message.from_user)
        user = asyncio.run(getInfoUser(full_name))

        asyncio.run(save_quick_expense(user, amount, category))
        bot.reply_to(
            message,
            f"Expense of {formatMoney(amount)} for {category} has been recorded.",
        )

    except (IndexError, ValueError):
        bot.reply_to(
            message, "Invalid expense format. Usage: /expense <amount> <category>"
        )


async def save_quick_expense(user, amount, category):
    await Spending.objects.create(user_id=user, money=amount, notes=category)
    account_balance = user.account_balance - amount
    await UpdateMoney(user.username, account_balance)


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
        useraccount_balance = user.account_balance or 0
        account_balance = useraccount_balance + money_spent
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
def record_get_income(message):
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


@bot.message_handler(commands=["diary"])
def record_diary(message):
    bot.send_message(
        message.chat.id,
        "write diary formart \n your write mood \n your write  main_events \n your write highlights \n your write challenges \n your write gratitude \n your write goals \n",
    )
    bot.register_next_step_handler(message, lambda msg: asyncio.run(save_diary(msg)))


async def save_diary(message):
    try:
        full_name = getFullName(message.from_user)
        user = await getInfoUser(full_name)
        parts = message.text.split("\n", 5)
        mood = parts[0]
        main_events = parts[1]
        highlights = parts[2]
        challenges = parts[3]
        gratitude = parts[4]
        goals = parts[5] if len(parts) > 5 else "Uncategorized"

        await Diary.objects.create(
            user_id=user,
            mood=mood,
            main_events=main_events,
            gratitude=gratitude,
            highlights=highlights,
            goals=goals,
            challenges=challenges,
        )
        bot.send_message(
            message.chat.id,
            f"{user.name} diary source has been recorded successfully!",
        )
    except Exception as e:
        logger.error(f"Error saving income: {e}")
        bot.reply_to(
            message,
            "An error write diary formart: \n your write mood \n your write  main_events \n your write highlights \n your write challenges \n your write gratitude \n your write goals \n",
        )


@bot.message_handler(commands=["get_diary"])
def record_get_diary(message):
    bot.send_message(
        message.chat.id, "plase write date your find - formart day/month/years"
    )
    bot.register_next_step_handler(message, lambda msg: asyncio.run(get_diary(msg)))


async def get_diary(message):
    try:
        full_name = getFullName(message.from_user)
        date_str = message.text
        diary = await getDiaryDetail(full_name, date_str)
        if diary:
            bot.reply_to(message, diary)
        else:
            bot.send_message(message.chat.id, f"find not found date: {date_str}")
    except Exception as e:
        logger.error(f"Error retrieving diary: {e}")
        bot.reply_to(
            message,
            "An error occurred while retrieving your diary. Please try again later.",
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
        f"\t Info of {user.name} \n Name: {user.name} \n Username: {user.username} \n Email: {user.email} \n account blade: {formatMoney(user.account_balance)}",
    )


@bot.message_handler(commands=["statistical"])
def run_statistics(message):
    asyncio.run(send_statistics(message))


@bot.message_handler(commands=["send_spending"])
def run_statistics(message):
    full_name = getFullName(message.from_user)
    sendMailUser(full_name)
    bot.send_message(message.chat.id, f"we send speding to your email  successfully!")


@bot.message_handler(commands=["send_spending_month"])
def run_statistics(message):
    full_name = getFullName(message.from_user)
    sendMailUserMonth(full_name)
    bot.send_message(message.chat.id, f"we send speding to your email  successfully!")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    asyncio.run(saveChat(message))
    bot.send_message(message.chat.id, message.text)


if __name__ == "__main__":
    bot.infinity_polling()
