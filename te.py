from app.feat.sendEmail import create_email_message, send_email, connect_to_smtp
import asyncio
from app.feat.user import getAllUser
from dotenv import load_dotenv
import os

load_dotenv()

def email_template(name, expense_data):
    subject = f"📊 Your Daily Expense Tracker - {name}"
    body = f"Hi {name},\n\nManaging your finances is crucial for a balanced life! Let's keep track of your expenses together. 💰\n\nExpense Tracker for {expense_data['date']}:\n\nCategory: {expense_data['category']}\nDescription: {expense_data['description']}\nAmount: {expense_data['amount']} {expense_data['currency']}\n\nNotes: {expense_data['notes']}\n\nStay on top of your spending habits and work towards your financial goals! 💪\n\nLooking forward to seeing your progress.\n\nBest regards,\n{os.getenv('App_name')}"
    return subject, body

if __name__ == "__main__":
    users = asyncio.run(getAllUser())
    for user in users:
        # Example expense data, replace with actual expense data
        expense_data = {
            'date': '2024-03-12',
            'category': 'Groceries',
            'description': 'Purchased groceries for the week',
            'amount': 50.00,
            'currency': 'Vnđ',
            'notes': 'Bought fruits, vegetables, and other essentials'
        }
        
        send_to = user.email
        subject, body = email_template(user.name, expense_data)
        formMail = create_email_message(send_to, subject, body)
        send_email(formMail, send_to)
