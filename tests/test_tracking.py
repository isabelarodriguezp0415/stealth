"""Tests for medication tracking functionality."""

import pytest
from datetime import datetime, timedelta, time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from medication_reminder.models import (
    Base, User, Medication, MedicationSchedule,
    ReminderLog, ReminderStatus
)
from medication_reminder.tracking import MedicationTracker
from medication_reminder.database import DatabaseManager


@pytest.fixture
def db_manager():
    """Create a test database manager."""
    # Use in-memory database for tests
    manager = DatabaseManager()
    manager.engine = create_engine("sqlite:///:memory:")
    manager.SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=manager.engine
    )
    Base.metadata.create_all(bind=manager.engine)
    return manager


@pytest.fixture
def tracker(db_manager, monkeypatch):
    """Create a medication tracker with test database."""
    tracker = MedicationTracker()
    monkeypatch.setattr(tracker, "db_manager", db_manager)
    return tracker


def test_adherence_rate_calculation(db_manager, tracker):
    """Test adherence rate calculation."""
    with db_manager.get_session() as session:
        # Create user
        user = User(name="Test User", phone_number="+1234567890")
        session.add(user)
        session.flush()

        # Create medication
        medication = Medication(
            user_id=user.id,
            name="Test Med",
            dosage="10mg",
            active=True
        )
        session.add(medication)
        session.flush()

        # Create schedule
        schedule = MedicationSchedule(
            medication_id=medication.id,
            time_of_day=time(hour=8, minute=0),
            active=True
        )
        session.add(schedule)
        session.flush()

        # Create reminders
        now = datetime.now()
        for i in range(10):
            status = ReminderStatus.CONFIRMED if i < 8 else ReminderStatus.MISSED
            reminder = ReminderLog(
                user_id=user.id,
                medication_id=medication.id,
                schedule_id=schedule.id,
                scheduled_time=now - timedelta(days=i),
                status=status
            )
            session.add(reminder)

        session.commit()

    # Test adherence rate
    adherence = tracker.get_user_adherence_rate(user.id, days=30)
    assert adherence["total_reminders"] == 10
    assert adherence["confirmed"] == 8
    assert adherence["missed"] == 2
    assert adherence["adherence_rate"] == 80.0


def test_missed_medications(db_manager, tracker):
    """Test getting missed medications."""
    with db_manager.get_session() as session:
        user = User(name="Test User", phone_number="+1234567890")
        session.add(user)
        session.flush()

        medication = Medication(
            user_id=user.id,
            name="Important Med",
            dosage="20mg",
            active=True
        )
        session.add(medication)
        session.flush()

        schedule = MedicationSchedule(
            medication_id=medication.id,
            time_of_day=time(hour=8, minute=0),
            active=True
        )
        session.add(schedule)
        session.flush()

        # Create a missed reminder
        reminder = ReminderLog(
            user_id=user.id,
            medication_id=medication.id,
            schedule_id=schedule.id,
            scheduled_time=datetime.now() - timedelta(hours=2),
            status=ReminderStatus.MISSED,
            attempt_count=3
        )
        session.add(reminder)
        session.commit()

    # Get missed medications
    missed = tracker.get_missed_medications(user.id, days=7)
    assert len(missed) == 1
    assert missed[0]["medication_name"] == "Important Med"
    assert missed[0]["attempt_count"] == 3
