from app.feat.sendEmail import create_email_message, send_email, connect_to_smtp

if __name__ == "__main__":
    send_to = "zero99ck9@gmail.com"
    formMail = create_email_message(send_to, "test send email", "asdjakjhsdhashdsdf")
    send_email(formMail, send_to)
