from app.feat.sendEmail import create_email_message, send_email, connect_to_smtp
import asyncio
from app.feat.user import getAllUser, getInfoUser
from dotenv import load_dotenv
import os
from app.feat.spending import sumMoneyLast7Weeks

load_dotenv()

def email_template(name, expense_data):
    subject = f"📊 Your Daily Expense Tracker (Week) - {name}"
    body = f"Hi {name},\n\nManaging your finances is crucial for a balanced life! Let's keep track of your expenses together. 💰\n\nExpense Tracker for {expense_data['date']}:\n\nCategory: {expense_data['category']}\nAmount: {expense_data['amount']} {expense_data['currency']}\n\n\nStay on top of your spending habits and work towards your financial goals! 💪\n\nLooking forward to seeing your progress.\n\nBest regards,\n{os.getenv('App_name')}"
    return subject, body


def sendMail():

    users = asyncio.run(getAllUser())
    for user in users:

        amount, date = asyncio.run(sumMoneyLast7Weeks(user.id))
        expense_data = {
            "date": date,
            "category": "Expense Tracker",
            "amount": amount,
            "currency": "Vnđ",
        }

        send_to = user.email
        subject, body = email_template(user.name, expense_data)
        formMail = create_email_message(send_to, subject, body)
        send_email(formMail, send_to)


def sendMailUser(username):

    user = asyncio.run(getInfoUser(username))
    amount, date = asyncio.run(sumMoneyLast7Weeks(user.id))
    expense_data = {
        "date": date,
        "category": "Expense Tracker",
        "amount": "{:,.3f}".format(amount),
        "currency": "Vnđ",
    }

    send_to = user.email
    subject, body = email_template(user.name, expense_data)
    formMail = create_email_message(send_to, subject, body)
    send_email(formMail, send_to)
