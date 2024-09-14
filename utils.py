import pickle
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SMTP_SERVER, SMTP_PORT, EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER

def save_pickle(data, filename):
    """Save data to a pickle file."""
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def load_pickle(filename):
    """Load data from a pickle file."""
    with open(filename, 'rb') as f:
        return pickle.load(f)

def get_file_list(folder_path):
    """Get a list of files in a directory."""
    return [os.path.join(folder_path, file) for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]

def send_email_notification(detected_criminal, video_path):
    """Send an email notification."""
    subject = "Criminal Detected"
    body = f"Attention:\n\nA criminal has been detected in the video footage.\n\nCriminal Identified: {detected_criminal}\nVideo Path: {video_path}\n\nPlease take appropriate action."

    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.close()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")
