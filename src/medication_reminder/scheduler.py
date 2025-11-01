"""Medication reminder scheduler using APScheduler."""

from datetime import datetime, timedelta
from typing import List, Optional
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger
from sqlalchemy.orm import Session

from .config import get_settings
from .database import get_db_manager
from .models import (
    User, Medication, MedicationSchedule, ReminderLog,
    ReminderStatus, Caregiver
)
from .voice_service import VoiceCallService


class MedicationReminderScheduler:
    """Manages scheduling and sending of medication reminders."""

    def __init__(self):
        self.settings = get_settings()
        self.db_manager = get_db_manager()
        self.voice_service = VoiceCallService()
        self.scheduler = BackgroundScheduler(
            timezone=pytz.timezone(self.settings.timezone)
        )

    def start(self):
        """Start the scheduler."""
        self.scheduler.start()
        logger.info("Medication reminder scheduler started")
        self._schedule_all_active_medications()

    def stop(self):
        """Stop the scheduler."""
        self.scheduler.shutdown()
        logger.info("Medication reminder scheduler stopped")

    def _schedule_all_active_medications(self):
        """Schedule reminders for all active medications."""
        with self.db_manager.get_session() as session:
            # Get all active users
            users = session.query(User).filter(User.active == True).all()

            for user in users:
                # Get all active medications for this user
                medications = session.query(Medication).filter(
                    Medication.user_id == user.id,
                    Medication.active == True
                ).all()

                for medication in medications:
                    # Get all active schedules for this medication
                    schedules = session.query(MedicationSchedule).filter(
                        MedicationSchedule.medication_id == medication.id,
                        MedicationSchedule.active == True
                    ).all()

                    for schedule in schedules:
                        self._schedule_medication_reminder(
                            user, medication, schedule
                        )

        logger.info("All active medications scheduled")

    def _schedule_medication_reminder(
        self,
        user: User,
        medication: Medication,
        schedule: MedicationSchedule
    ):
        """Schedule a single medication reminder."""
        # Parse time of day
        hour = schedule.time_of_day.hour
        minute = schedule.time_of_day.minute

        # Parse days of week (if specified)
        if schedule.days_of_week:
            days_of_week = schedule.days_of_week
        else:
            # Daily - all days
            days_of_week = "0,1,2,3,4,5,6"

        # Create cron trigger
        trigger = CronTrigger(
            hour=hour,
            minute=minute,
            day_of_week=days_of_week,
            timezone=pytz.timezone(user.timezone or self.settings.timezone)
        )

        # Create job ID
        job_id = f"medication_{medication.id}_schedule_{schedule.id}"

        # Check if job already exists
        if self.scheduler.get_job(job_id):
            logger.debug(f"Job {job_id} already exists, removing old job")
            self.scheduler.remove_job(job_id)

        # Schedule the job
        self.scheduler.add_job(
            func=self._send_medication_reminder,
            trigger=trigger,
            args=[user.id, medication.id, schedule.id],
            id=job_id,
            name=f"Reminder for {user.name} - {medication.name}",
            replace_existing=True
        )

        logger.info(
            f"Scheduled reminder for {user.name} - {medication.name} "
            f"at {hour:02d}:{minute:02d} (days: {days_of_week})"
        )

    def _send_medication_reminder(
        self,
        user_id: int,
        medication_id: int,
        schedule_id: int
    ):
        """Send a medication reminder via voice call."""
        with self.db_manager.get_session() as session:
            # Get user, medication, and schedule
            user = session.query(User).filter(User.id == user_id).first()
            medication = session.query(Medication).filter(
                Medication.id == medication_id
            ).first()
            schedule = session.query(MedicationSchedule).filter(
                MedicationSchedule.id == schedule_id
            ).first()

            if not user or not medication or not schedule:
                logger.error(
                    f"Failed to send reminder: User, medication, or schedule not found "
                    f"(user_id={user_id}, medication_id={medication_id}, schedule_id={schedule_id})"
                )
                return

            # Check if user is active
            if not user.active:
                logger.info(f"User {user.name} is inactive, skipping reminder")
                return

            # Create reminder log
            reminder_log = ReminderLog(
                user_id=user.id,
                medication_id=medication.id,
                schedule_id=schedule.id,
                scheduled_time=datetime.now(),
                status=ReminderStatus.PENDING,
                attempt_count=1
            )
            session.add(reminder_log)
            session.flush()  # Get the ID

            # Make the voice call
            call_sid = self.voice_service.make_reminder_call(
                to_number=user.phone_number,
                user=user,
                medication=medication,
                reminder_log=reminder_log
            )

            if call_sid:
                # Update reminder log
                reminder_log.call_sid = call_sid
                reminder_log.sent_time = datetime.now()
                reminder_log.status = ReminderStatus.SENT

                # Schedule follow-up check
                self._schedule_reminder_followup(reminder_log.id)

                logger.info(
                    f"Medication reminder sent to {user.name} "
                    f"for {medication.name}"
                )
            else:
                reminder_log.status = ReminderStatus.MISSED
                logger.error(
                    f"Failed to send medication reminder to {user.name}"
                )

            session.commit()

    def _schedule_reminder_followup(self, reminder_log_id: int):
        """
        Schedule a follow-up check to see if the reminder was confirmed.
        If not confirmed, retry or notify caregiver.
        """
        delay_minutes = self.settings.caregiver_notification_delay_minutes

        # Schedule follow-up
        run_date = datetime.now() + timedelta(minutes=delay_minutes)

        self.scheduler.add_job(
            func=self._check_reminder_confirmation,
            trigger='date',
            run_date=run_date,
            args=[reminder_log_id],
            id=f"followup_{reminder_log_id}",
            name=f"Follow-up check for reminder {reminder_log_id}"
        )

        logger.debug(
            f"Scheduled follow-up check for reminder {reminder_log_id} "
            f"in {delay_minutes} minutes"
        )

    def _check_reminder_confirmation(self, reminder_log_id: int):
        """
        Check if a reminder was confirmed.
        If not, retry (up to max attempts) or notify caregiver.
        """
        with self.db_manager.get_session() as session:
            reminder_log = session.query(ReminderLog).filter(
                ReminderLog.id == reminder_log_id
            ).first()

            if not reminder_log:
                logger.error(f"Reminder log {reminder_log_id} not found")
                return

            # If already confirmed, nothing to do
            if reminder_log.status == ReminderStatus.CONFIRMED:
                logger.info(
                    f"Reminder {reminder_log_id} already confirmed, "
                    f"no action needed"
                )
                return

            # Get user and medication
            user = session.query(User).filter(
                User.id == reminder_log.user_id
            ).first()
            medication = session.query(Medication).filter(
                Medication.id == reminder_log.medication_id
            ).first()

            if not user or not medication:
                logger.error("User or medication not found for reminder follow-up")
                return

            # Check if we should retry
            max_attempts = self.settings.max_reminder_attempts

            if reminder_log.attempt_count < max_attempts:
                # Retry the reminder
                reminder_log.attempt_count += 1

                call_sid = self.voice_service.make_reminder_call(
                    to_number=user.phone_number,
                    user=user,
                    medication=medication,
                    reminder_log=reminder_log
                )

                if call_sid:
                    reminder_log.call_sid = call_sid
                    reminder_log.sent_time = datetime.now()
                    reminder_log.status = ReminderStatus.SENT

                    # Schedule another follow-up
                    self._schedule_reminder_followup(reminder_log.id)

                    logger.info(
                        f"Retry {reminder_log.attempt_count}/{max_attempts} "
                        f"for reminder {reminder_log_id}"
                    )
                else:
                    logger.error(f"Failed to retry reminder {reminder_log_id}")

            else:
                # Max attempts reached, notify caregiver
                reminder_log.status = ReminderStatus.MISSED
                self._notify_caregivers(session, user, medication, reminder_log)

            session.commit()

    def _notify_caregivers(
        self,
        session: Session,
        user: User,
        medication: Medication,
        reminder_log: ReminderLog
    ):
        """Notify all active caregivers about a missed medication."""
        caregivers = session.query(Caregiver).filter(
            Caregiver.user_id == user.id,
            Caregiver.active == True
        ).all()

        if not caregivers:
            logger.warning(
                f"No active caregivers found for user {user.name}. "
                f"Medication {medication.name} was missed."
            )
            return

        for caregiver in caregivers:
            call_sid = self.voice_service.make_caregiver_notification_call(
                to_number=caregiver.phone_number,
                patient_name=user.name,
                medication_name=medication.name,
                scheduled_time=reminder_log.scheduled_time
            )

            if call_sid:
                logger.info(
                    f"Caregiver {caregiver.name} notified about "
                    f"missed medication for {user.name}"
                )

        # Update reminder log
        reminder_log.caregiver_notified = True
        reminder_log.caregiver_notified_at = datetime.now()
        reminder_log.status = ReminderStatus.CAREGIVER_NOTIFIED

    def add_medication_schedule(
        self,
        user: User,
        medication: Medication,
        schedule: MedicationSchedule
    ):
        """Add a new medication schedule to the scheduler."""
        self._schedule_medication_reminder(user, medication, schedule)

    def remove_medication_schedule(self, schedule_id: int):
        """Remove a medication schedule from the scheduler."""
        with self.db_manager.get_session() as session:
            schedule = session.query(MedicationSchedule).filter(
                MedicationSchedule.id == schedule_id
            ).first()

            if schedule:
                job_id = f"medication_{schedule.medication_id}_schedule_{schedule.id}"
                if self.scheduler.get_job(job_id):
                    self.scheduler.remove_job(job_id)
                    logger.info(f"Removed schedule {schedule_id} from scheduler")

    def confirm_medication_taken(self, reminder_log_id: int, method: str = "voice"):
        """Mark a medication reminder as confirmed."""
        with self.db_manager.get_session() as session:
            reminder_log = session.query(ReminderLog).filter(
                ReminderLog.id == reminder_log_id
            ).first()

            if reminder_log:
                reminder_log.status = ReminderStatus.CONFIRMED
                reminder_log.confirmation_received_at = datetime.now()
                reminder_log.confirmation_method = method
                session.commit()

                logger.info(
                    f"Medication confirmed for reminder {reminder_log_id} "
                    f"via {method}"
                )

                # Cancel any pending follow-up
                followup_job_id = f"followup_{reminder_log_id}"
                if self.scheduler.get_job(followup_job_id):
                    self.scheduler.remove_job(followup_job_id)
