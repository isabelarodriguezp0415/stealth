"""Main service for coordinating all medication reminder components."""

from typing import Optional, Dict, Any
from datetime import datetime, time
from loguru import logger

from .config import get_settings
from .database import get_db_manager
from .models import User, Medication, MedicationSchedule, Caregiver
from .scheduler import MedicationReminderScheduler
from .ai_agent import MedicationAIAgent
from .tracking import MedicationTracker
from .voice_service import VoiceCallService


class MedicationReminderService:
    """Main service that coordinates all medication reminder functionality."""

    def __init__(self):
        self.settings = get_settings()
        self.db_manager = get_db_manager()
        self.scheduler = MedicationReminderScheduler()
        self.ai_agent = MedicationAIAgent()
        self.tracker = MedicationTracker()
        self.voice_service = VoiceCallService()

    def initialize(self):
        """Initialize the service and create database tables."""
        logger.info("Initializing Medication Reminder Service...")

        # Create database tables
        self.db_manager.create_tables()
        logger.info("Database tables created")

        # Start scheduler
        self.scheduler.start()
        logger.info("Scheduler started")

        logger.info("Medication Reminder Service initialized successfully")

    def shutdown(self):
        """Shutdown the service gracefully."""
        logger.info("Shutting down Medication Reminder Service...")
        self.scheduler.stop()
        logger.info("Service shutdown complete")

    # User Management
    def create_user(
        self,
        name: str,
        phone_number: str,
        date_of_birth: Optional[datetime] = None,
        timezone: str = "America/New_York"
    ) -> User:
        """Create a new user."""
        with self.db_manager.get_session() as session:
            user = User(
                name=name,
                phone_number=phone_number,
                date_of_birth=date_of_birth,
                timezone=timezone,
                active=True
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            logger.info(f"Created user: {user.name} (ID: {user.id})")
            return user

    def get_user(self, user_id: int) -> Optional[User]:
        """Get a user by ID."""
        with self.db_manager.get_session() as session:
            return session.query(User).filter(User.id == user_id).first()

    def get_user_by_phone(self, phone_number: str) -> Optional[User]:
        """Get a user by phone number."""
        with self.db_manager.get_session() as session:
            return session.query(User).filter(
                User.phone_number == phone_number
            ).first()

    # Medication Management
    def add_medication(
        self,
        user_id: int,
        name: str,
        dosage: str,
        times: list,  # List of time strings like ["08:00", "20:00"]
        instructions: Optional[str] = None,
        purpose: Optional[str] = None,
        days_of_week: Optional[str] = None  # e.g., "0,1,2,3,4" for weekdays
    ) -> Medication:
        """Add a medication with its schedule."""
        with self.db_manager.get_session() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                raise ValueError(f"User {user_id} not found")

            # Create medication
            medication = Medication(
                user_id=user_id,
                name=name,
                dosage=dosage,
                instructions=instructions,
                purpose=purpose,
                active=True
            )
            session.add(medication)
            session.flush()

            # Create schedules
            for time_str in times:
                hour, minute = map(int, time_str.split(":"))
                schedule = MedicationSchedule(
                    medication_id=medication.id,
                    time_of_day=time(hour=hour, minute=minute),
                    days_of_week=days_of_week,
                    active=True
                )
                session.add(schedule)
                session.flush()

                # Add to scheduler
                self.scheduler.add_medication_schedule(user, medication, schedule)

            session.commit()
            session.refresh(medication)

            logger.info(
                f"Added medication {medication.name} for user {user.name} "
                f"with {len(times)} scheduled times"
            )

            return medication

    def remove_medication(self, medication_id: int):
        """Remove/deactivate a medication."""
        with self.db_manager.get_session() as session:
            medication = session.query(Medication).filter(
                Medication.id == medication_id
            ).first()

            if medication:
                medication.active = False

                # Deactivate schedules and remove from scheduler
                for schedule in medication.schedules:
                    schedule.active = False
                    self.scheduler.remove_medication_schedule(schedule.id)

                session.commit()
                logger.info(f"Removed medication {medication.name}")

    # Caregiver Management
    def add_caregiver(
        self,
        user_id: int,
        name: str,
        phone_number: str,
        relationship_type: Optional[str] = None,
        email: Optional[str] = None
    ) -> Caregiver:
        """Add a caregiver for a user."""
        with self.db_manager.get_session() as session:
            caregiver = Caregiver(
                user_id=user_id,
                name=name,
                phone_number=phone_number,
                relationship_type=relationship_type,
                email=email,
                active=True
            )
            session.add(caregiver)
            session.commit()
            session.refresh(caregiver)

            logger.info(
                f"Added caregiver {caregiver.name} for user ID {user_id}"
            )

            return caregiver

    # AI Interface
    def process_natural_language(
        self,
        user_id: int,
        message: str
    ) -> Dict[str, Any]:
        """Process a natural language message from a user."""
        return self.ai_agent.process_message(user_id, message)

    # Tracking and Reporting
    def get_adherence_report(
        self,
        user_id: int,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get adherence report for a user."""
        return self.tracker.generate_adherence_report(user_id, days)

    def get_upcoming_medications(
        self,
        user_id: int,
        hours: int = 24
    ) -> list:
        """Get upcoming medications for a user."""
        return self.tracker.get_upcoming_medications(user_id, hours)

    # Reminder Confirmation (called from webhook/callback)
    def confirm_medication_taken(
        self,
        reminder_log_id: int,
        method: str = "voice"
    ):
        """Confirm that a medication was taken."""
        self.scheduler.confirm_medication_taken(reminder_log_id, method)
