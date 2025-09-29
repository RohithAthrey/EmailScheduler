from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ScheduledEmail(Base):
    __tablename__ = "scheduled_emails"
    
    id = Column(Integer, primary_key=True, index=True)
    recipient_email = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    body = Column(Text, nullable=False) 
    scheduled_time = Column(DateTime, nullable=False)
    status = Column(String(50), default="pending", nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    sent_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)

Base.metadata.create_all(bind=engine)
def test_connection():
    try:
        db = SessionLocal()
        test_email = ScheduledEmail(
            recipient_email="test@example.com",
            subject="Test",
            body="Test message",
            scheduled_time=datetime.now()
        )
        db.add(test_email)
        db.commit()
        print("Database connection successful!")
        return True
    except Exception as e:
        print(f"Database error: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    test_connection()