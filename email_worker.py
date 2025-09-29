import time
from database import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
YOUR_EMAIL = os.getenv("YOUR_EMAIL")
YOUR_PASSWORD = os.getenv("YOUR_PASSWORD")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(to_email, subject, body):
    """Send email via Gmail SMTP. Returns True if successful, False if failed."""
    try:
        msg = MIMEMultipart()
        msg['From'] = YOUR_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(body, 'plain'))
        
        # Gmail SMTP configuration
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Enable encryption
        server.login(YOUR_EMAIL, YOUR_PASSWORD)
        
        # Send email
        text = msg.as_string()
        server.sendmail(YOUR_EMAIL, to_email, text)
        server.quit()
        
        print(f"✅ Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {str(e)}")
        return False

while(True) :
    db=SessionLocal()
    emails = db.query(ScheduledEmail).filter(
        ScheduledEmail.status == "pending",
        ScheduledEmail.scheduled_time <= datetime.now()
    ).all()
    for entries in emails: 
        success = send_email(entries.recipient_email, entries.subject, entries.body)
        if success:
            entries.status = "sent"
            entries.sent_at = datetime.now()
        else:
            entries.status = "failed"
            entries.error_message = "SMTP send failed"
        db.commit()
    db.close()
    time.sleep(60)