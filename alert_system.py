import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(subject, message):
    sender_email = "user_email"
    receiver_email = "user_email"
    password = os.getenv('EMAIL_PASSWORD')  # Retrieve password from environment variable

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)  # Correct server for Gmail
    server.starttls()
    try:
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
    finally:
        server.quit()

if __name__ == "__main__":
    send_email("Test Subject", "Hello, this is a test email from your anomaly detection system.")
