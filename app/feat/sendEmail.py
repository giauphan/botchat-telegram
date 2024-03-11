import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

def connect_to_smtp():
    sender_email = os.getenv('SENDER_EMAIL')
    smtp_server = os.getenv('SMTP_SERVER')
    port = os.getenv('SMTP_PORT')
    password = os.getenv('SMTP_PASSWORD')

    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(sender_email, password)
    return server


def send_email(msg, send_to):
    server = connect_to_smtp()
    try:
        sender_email = os.getenv('SENDER_EMAIL')
        text = msg.as_string()
        server.sendmail(sender_email, send_to, text)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()

def create_email_message(send_to, subject, body):
    msg = MIMEMultipart()
    msg['From'] = os.getenv('SENDER_EMAIL')
    msg['To'] = send_to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    return msg