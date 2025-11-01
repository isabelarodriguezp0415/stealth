"""Tests for database models."""

import pytest
from datetime import datetime, time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from medication_reminder.models import (
    Base, User, Medication, MedicationSchedule,
    Caregiver, ReminderLog, ReminderStatus
)


@pytest.fixture
def db_session():
    """Create a test database session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_create_user(db_session):
    """Test creating a user."""
    user = User(
        name="John Doe",
        phone_number="+1234567890",
        timezone="America/New_York",
        active=True
    )
    db_session.add(user)
    db_session.commit()

    assert user.id is not None
    assert user.name == "John Doe"
    assert user.active is True


def test_create_medication(db_session):
    """Test creating a medication."""
    user = User(name="Jane Doe", phone_number="+1987654321")
    db_session.add(user)
    db_session.commit()

    medication = Medication(
        user_id=user.id,
        name="Aspirin",
        dosage="100mg",
        instructions="Take with food",
        active=True
    )
    db_session.add(medication)
    db_session.commit()

    assert medication.id is not None
    assert medication.name == "Aspirin"
    assert medication.user_id == user.id


def test_create_medication_schedule(db_session):
    """Test creating a medication schedule."""
    user = User(name="Test User", phone_number="+1111111111")
    db_session.add(user)
    db_session.commit()

    medication = Medication(
        user_id=user.id,
        name="Test Med",
        dosage="10mg",
        active=True
    )
    db_session.add(medication)
    db_session.commit()

    schedule = MedicationSchedule(
        medication_id=medication.id,
        time_of_day=time(hour=8, minute=0),
        days_of_week="0,1,2,3,4",  # Weekdays
        active=True
    )
    db_session.add(schedule)
    db_session.commit()

    assert schedule.id is not None
    assert schedule.time_of_day == time(hour=8, minute=0)


def test_create_caregiver(db_session):
    """Test creating a caregiver."""
    user = User(name="Patient", phone_number="+1222222222")
    db_session.add(user)
    db_session.commit()

    caregiver = Caregiver(
        user_id=user.id,
        name="Caregiver Name",
        phone_number="+1333333333",
        relationship_type="daughter",
        active=True
    )
    db_session.add(caregiver)
    db_session.commit()

    assert caregiver.id is not None
    assert caregiver.name == "Caregiver Name"
    assert caregiver.relationship_type == "daughter"


def test_create_reminder_log(db_session):
    """Test creating a reminder log."""
    user = User(name="Test User", phone_number="+1444444444")
    db_session.add(user)
    db_session.commit()

    medication = Medication(
        user_id=user.id,
        name="Test Med",
        dosage="10mg",
        active=True
    )
    db_session.add(medication)
    db_session.commit()

    schedule = MedicationSchedule(
        medication_id=medication.id,
        time_of_day=time(hour=8, minute=0),
        active=True
    )
    db_session.add(schedule)
    db_session.commit()

    reminder = ReminderLog(
        user_id=user.id,
        medication_id=medication.id,
        schedule_id=schedule.id,
        scheduled_time=datetime.now(),
        status=ReminderStatus.PENDING
    )
    db_session.add(reminder)
    db_session.commit()

    assert reminder.id is not None
    assert reminder.status == ReminderStatus.PENDING


def test_user_relationships(db_session):
    """Test user relationships with medications and caregivers."""
    user = User(name="Test User", phone_number="+1555555555")
    db_session.add(user)
    db_session.commit()

    # Add medications
    med1 = Medication(user_id=user.id, name="Med 1", dosage="10mg", active=True)
    med2 = Medication(user_id=user.id, name="Med 2", dosage="20mg", active=True)
    db_session.add_all([med1, med2])

    # Add caregiver
    caregiver = Caregiver(
        user_id=user.id,
        name="Caregiver",
        phone_number="+1666666666",
        active=True
    )
    db_session.add(caregiver)
    db_session.commit()

    # Refresh user to load relationships
    db_session.refresh(user)

    assert len(user.medications) == 2
    assert len(user.caregivers) == 1
