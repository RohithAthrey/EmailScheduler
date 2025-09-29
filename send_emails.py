import sys
import csv_reader
from datetime import datetime
import scheduler
from database import *
db = SessionLocal()
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python schedule_emails.py <csv_filename>")
        sys.exit(1)
    
    csv_filename = sys.argv[1]  # First argument after script name
    print(f"Reading contacts from: {csv_filename}")
    for contact in csv_reader.read_contacts(csv_filename): 
        personalized_message = csv_reader.personalize_email(csv_reader.EMAIL_TEMPLATE, contact)
        send_time = scheduler.calculate_send_time(datetime.now())
        scheduled_email = ScheduledEmail(
            recipient_email=contact['email'],
            subject="UMD student reaching out", 
            body=personalized_message,
            scheduled_time=send_time
        )   
        db.add(scheduled_email)
        db.commit()
        print(f"Scheduled email to {contact['email']} for {send_time}")
        db.close()

    
    