import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

def sendEmail(msg,send_to:str):
    try:
        sender_email= os.getenv('sender_email')
        server = smtplib.SMTP(os.getenv('smtp_server'), os.getenv('port'))
        server.starttls() # Secure the connection
        server.login(sender_email, os.getenv('password'))
        text = msg.as_string()
        server.sendmail(sender_email, send_to, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
