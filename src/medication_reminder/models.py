"""Database models for the medication reminder system."""

from datetime import datetime, time
from enum import Enum
from typing import Optional, List
from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, ForeignKey,
    Time, Text, Enum as SQLEnum
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class ReminderStatus(str, Enum):
    """Status of a medication reminder."""
    PENDING = "pending"
    SENT = "sent"
    CONFIRMED = "confirmed"
    MISSED = "missed"
    CAREGIVER_NOTIFIED = "caregiver_notified"


class User(Base):
    """Represents an elderly person using the medication reminder system."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False, unique=True)
    date_of_birth = Column(DateTime, nullable=True)
    timezone = Column(String(50), default="America/New_York")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = Column(Boolean, default=True)

    # Relationships
    medications = relationship("Medication", back_populates="user", cascade="all, delete-orphan")
    caregivers = relationship("Caregiver", back_populates="user", cascade="all, delete-orphan")
    reminders = relationship("ReminderLog", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', phone='{self.phone_number}')>"


class Caregiver(Base):
    """Represents a caregiver who should be notified if medications are missed."""

    __tablename__ = "caregivers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False)
    email = Column(String(100), nullable=True)
    relationship_type = Column(String(50), nullable=True)  # e.g., "daughter", "son", "nurse"
    created_at = Column(DateTime, default=datetime.utcnow)
    active = Column(Boolean, default=True)

    # Relationships
    user = relationship("User", back_populates="caregivers")

    def __repr__(self):
        return f"<Caregiver(id={self.id}, name='{self.name}', relationship='{self.relationship_type}')>"


class Medication(Base):
    """Represents a medication that needs to be taken."""

    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(200), nullable=False)
    dosage = Column(String(100), nullable=False)  # e.g., "10mg", "2 tablets"
    instructions = Column(Text, nullable=True)  # e.g., "Take with food"
    purpose = Column(Text, nullable=True)  # What the medication is for
    prescribing_doctor = Column(String(100), nullable=True)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="medications")
    schedules = relationship("MedicationSchedule", back_populates="medication", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Medication(id={self.id}, name='{self.name}', dosage='{self.dosage}')>"


class MedicationSchedule(Base):
    """Represents the schedule for when a medication should be taken."""

    __tablename__ = "medication_schedules"

    id = Column(Integer, primary_key=True, index=True)
    medication_id = Column(Integer, ForeignKey("medications.id"), nullable=False)
    time_of_day = Column(Time, nullable=False)  # e.g., 08:00, 14:00, 20:00
    days_of_week = Column(String(50), nullable=True)  # e.g., "1,2,3,4,5" (Mon-Fri) or None for daily
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    medication = relationship("Medication", back_populates="schedules")

    def __repr__(self):
        return f"<MedicationSchedule(id={self.id}, medication_id={self.medication_id}, time={self.time_of_day})>"


class ReminderLog(Base):
    """Log of all medication reminders sent."""

    __tablename__ = "reminder_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    medication_id = Column(Integer, ForeignKey("medications.id"), nullable=False)
    schedule_id = Column(Integer, ForeignKey("medication_schedules.id"), nullable=False)

    scheduled_time = Column(DateTime, nullable=False)
    sent_time = Column(DateTime, nullable=True)
    status = Column(SQLEnum(ReminderStatus), default=ReminderStatus.PENDING)

    # Tracking
    confirmation_received_at = Column(DateTime, nullable=True)
    confirmation_method = Column(String(50), nullable=True)  # e.g., "voice", "keypress"
    attempt_count = Column(Integer, default=0)

    # Call details
    call_sid = Column(String(100), nullable=True)  # Twilio call SID
    call_duration = Column(Integer, nullable=True)  # Duration in seconds

    # Caregiver notification
    caregiver_notified = Column(Boolean, default=False)
    caregiver_notified_at = Column(DateTime, nullable=True)

    notes = Column(Text, nullable=True)

    # Relationships
    user = relationship("User", back_populates="reminders")
    medication = relationship("Medication")
    schedule = relationship("MedicationSchedule")

    def __repr__(self):
        return f"<ReminderLog(id={self.id}, user_id={self.user_id}, status='{self.status}')>"


class AIConversationLog(Base):
    """Log of AI-powered conversations with users."""

    __tablename__ = "ai_conversation_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_input = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    intent = Column(String(100), nullable=True)  # e.g., "add_medication", "query_schedule"
    action_taken = Column(Text, nullable=True)

    def __repr__(self):
        return f"<AIConversationLog(id={self.id}, user_id={self.user_id}, intent='{self.intent}')>"
