import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(subject, message):
    sender_email = "your_sender_email@gmail.com"  # Replace with your actual sender email
    receiver_email = "your_receiver_email@gmail.com"  # Replace with your actual receiver email
    password = os.getenv('EMAIL_PASSWORD')  # Retrieve password from environment variable

    print("Preparing the email...")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    print("Connecting to the email server...")
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        print("Starting secure session...")
        server.login(sender_email, password)
        print("Logged in successfully, sending email...")
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()
        print("Server connection closed.")

if __name__ == "__main__":
    send_email( "Hello, this is a test email from your anomaly detection system.")
