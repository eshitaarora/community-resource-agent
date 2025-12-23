from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class SocialService(Base):
    """Represents a social service (shelter, food bank, clinic, etc.)"""
    __tablename__ = "social_services"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(Text)
    category = Column(String(50), index=True)  # shelter, food, health, employment, etc
    address = Column(String(500))
    latitude = Column(Float)
    longitude = Column(Float)
    phone = Column(String(20))
    website = Column(String(500))
    operating_hours = Column(JSON)  # {"monday": "9AM-5PM", ...}
    eligibility_criteria = Column(JSON)  # Income limits, age, residency, etc
    services_provided = Column(JSON)  # List of services
    is_active = Column(Boolean, default=True)
    last_verified = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserProfile(Base):
    """Tracks user journeys and needs"""
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), unique=True, index=True)
    phone_number = Column(String(20), nullable=True)
    primary_language = Column(String(10), default="en")
    location = Column(String(500))
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    needs = Column(JSON)  # ["shelter", "food", "health", ...]
    eligibility_info = Column(JSON)  # Income level, family size, etc
    accessibility_needs = Column(JSON)  # Mobility, language, sensory
    created_at = Column(DateTime, default=datetime.utcnow)
    last_interaction = Column(DateTime, default=datetime.utcnow)


class ChatMessage(Base):
    """Stores conversation history for context"""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), index=True)
    message = Column(Text)
    response = Column(Text)
    agent_tools_used = Column(JSON)  # Which tools the agent called
    timestamp = Column(DateTime, default=datetime.utcnow)
    helpful = Column(Boolean, nullable=True)  # User feedback


class ServiceAccess(Base):
    """Tracks successful service access for impact metrics"""
    __tablename__ = "service_access"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), index=True)
    service_id = Column(Integer, index=True)
    service_name = Column(String(255))
    access_date = Column(DateTime, default=datetime.utcnow)
    contact_method = Column(String(50))  # phone, in-person, referral
    outcome = Column(String(50))  # completed, pending, no-show
    notes = Column(Text)


def get_db():
    """Dependency for FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
