import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(msg, send_to):
    try:
        sender_email = os.getenv('SENDER_EMAIL')
        smtp_server = os.getenv('SMTP_SERVER')
        port = os.getenv('SMTP_PORT')
        password = os.getenv('SMTP_PASSWORD')

        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls() 
            server.login(sender_email, password)
            text = msg.as_string()
            server.sendmail(sender_email, send_to, text)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

def create_email_message(send_to, sender_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = send_to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    return msg
