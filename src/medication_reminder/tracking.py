"""Medication tracking and reporting functionality."""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session

from .database import get_db_manager
from .models import (
    User, Medication, MedicationSchedule, ReminderLog,
    ReminderStatus, Caregiver
)


class MedicationTracker:
    """Tracks medication adherence and generates reports."""

    def __init__(self):
        self.db_manager = get_db_manager()

    def get_user_adherence_rate(
        self,
        user_id: int,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Calculate medication adherence rate for a user over a period.

        Args:
            user_id: User ID
            days: Number of days to look back

        Returns:
            Dictionary with adherence statistics
        """
        with self.db_manager.get_session() as session:
            start_date = datetime.now() - timedelta(days=days)

            # Get all reminders for this user in the period
            reminders = session.query(ReminderLog).filter(
                ReminderLog.user_id == user_id,
                ReminderLog.scheduled_time >= start_date
            ).all()

            total_reminders = len(reminders)
            if total_reminders == 0:
                return {
                    "user_id": user_id,
                    "period_days": days,
                    "total_reminders": 0,
                    "adherence_rate": 0.0,
                    "confirmed": 0,
                    "missed": 0,
                    "pending": 0
                }

            # Count by status
            confirmed = sum(
                1 for r in reminders
                if r.status == ReminderStatus.CONFIRMED
            )
            missed = sum(
                1 for r in reminders
                if r.status in [ReminderStatus.MISSED, ReminderStatus.CAREGIVER_NOTIFIED]
            )
            pending = sum(
                1 for r in reminders
                if r.status in [ReminderStatus.PENDING, ReminderStatus.SENT]
            )

            adherence_rate = (confirmed / total_reminders) * 100

            return {
                "user_id": user_id,
                "period_days": days,
                "total_reminders": total_reminders,
                "adherence_rate": round(adherence_rate, 2),
                "confirmed": confirmed,
                "missed": missed,
                "pending": pending
            }

    def get_medication_adherence_rate(
        self,
        medication_id: int,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Calculate adherence rate for a specific medication.

        Args:
            medication_id: Medication ID
            days: Number of days to look back

        Returns:
            Dictionary with adherence statistics
        """
        with self.db_manager.get_session() as session:
            start_date = datetime.now() - timedelta(days=days)

            medication = session.query(Medication).filter(
                Medication.id == medication_id
            ).first()

            if not medication:
                return {"error": "Medication not found"}

            # Get all reminders for this medication in the period
            reminders = session.query(ReminderLog).filter(
                ReminderLog.medication_id == medication_id,
                ReminderLog.scheduled_time >= start_date
            ).all()

            total_reminders = len(reminders)
            if total_reminders == 0:
                return {
                    "medication_id": medication_id,
                    "medication_name": medication.name,
                    "period_days": days,
                    "total_reminders": 0,
                    "adherence_rate": 0.0
                }

            confirmed = sum(
                1 for r in reminders
                if r.status == ReminderStatus.CONFIRMED
            )

            adherence_rate = (confirmed / total_reminders) * 100

            return {
                "medication_id": medication_id,
                "medication_name": medication.name,
                "period_days": days,
                "total_reminders": total_reminders,
                "adherence_rate": round(adherence_rate, 2),
                "confirmed": confirmed,
                "missed": total_reminders - confirmed
            }

    def get_missed_medications(
        self,
        user_id: int,
        days: int = 7
    ) -> List[Dict[str, Any]]:
        """
        Get all missed medications for a user in a period.

        Args:
            user_id: User ID
            days: Number of days to look back

        Returns:
            List of missed medication events
        """
        with self.db_manager.get_session() as session:
            start_date = datetime.now() - timedelta(days=days)

            missed_reminders = session.query(ReminderLog).filter(
                ReminderLog.user_id == user_id,
                ReminderLog.scheduled_time >= start_date,
                ReminderLog.status.in_([
                    ReminderStatus.MISSED,
                    ReminderStatus.CAREGIVER_NOTIFIED
                ])
            ).order_by(ReminderLog.scheduled_time.desc()).all()

            result = []
            for reminder in missed_reminders:
                medication = session.query(Medication).filter(
                    Medication.id == reminder.medication_id
                ).first()

                result.append({
                    "reminder_id": reminder.id,
                    "medication_name": medication.name if medication else "Unknown",
                    "dosage": medication.dosage if medication else "Unknown",
                    "scheduled_time": reminder.scheduled_time.isoformat(),
                    "attempt_count": reminder.attempt_count,
                    "caregiver_notified": reminder.caregiver_notified
                })

            return result

    def get_upcoming_medications(
        self,
        user_id: int,
        hours: int = 24
    ) -> List[Dict[str, Any]]:
        """
        Get upcoming scheduled medications for a user.

        Args:
            user_id: User ID
            hours: Number of hours to look ahead

        Returns:
            List of upcoming medications
        """
        with self.db_manager.get_session() as session:
            user = session.query(User).filter(User.id == user_id).first()

            if not user:
                return []

            # Get all active medications
            medications = session.query(Medication).filter(
                Medication.user_id == user_id,
                Medication.active == True
            ).all()

            upcoming = []
            now = datetime.now()
            end_time = now + timedelta(hours=hours)

            for medication in medications:
                schedules = session.query(MedicationSchedule).filter(
                    MedicationSchedule.medication_id == medication.id,
                    MedicationSchedule.active == True
                ).all()

                for schedule in schedules:
                    # Calculate next occurrence
                    next_time = self._calculate_next_occurrence(
                        schedule.time_of_day,
                        schedule.days_of_week
                    )

                    if next_time and now <= next_time <= end_time:
                        upcoming.append({
                            "medication_id": medication.id,
                            "medication_name": medication.name,
                            "dosage": medication.dosage,
                            "scheduled_time": next_time.isoformat(),
                            "instructions": medication.instructions
                        })

            # Sort by scheduled time
            upcoming.sort(key=lambda x: x["scheduled_time"])

            return upcoming

    def _calculate_next_occurrence(
        self,
        time_of_day: datetime.time,
        days_of_week: Optional[str]
    ) -> Optional[datetime]:
        """
        Calculate the next occurrence of a scheduled time.

        Args:
            time_of_day: Time of day for the medication
            days_of_week: Comma-separated days (0=Monday, 6=Sunday) or None for daily

        Returns:
            Next occurrence datetime or None
        """
        now = datetime.now()
        today = now.date()

        # Create datetime for today at the scheduled time
        next_occurrence = datetime.combine(today, time_of_day)

        # If the time has already passed today, start from tomorrow
        if next_occurrence <= now:
            next_occurrence += timedelta(days=1)

        # If specific days of week are set, find the next matching day
        if days_of_week:
            allowed_days = set(int(d) for d in days_of_week.split(','))

            # Search up to 7 days ahead
            for _ in range(7):
                if next_occurrence.weekday() in allowed_days:
                    return next_occurrence
                next_occurrence += timedelta(days=1)

            return None  # No matching day found

        return next_occurrence

    def generate_adherence_report(
        self,
        user_id: int,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive adherence report for a user.

        Args:
            user_id: User ID
            days: Number of days to include in the report

        Returns:
            Comprehensive adherence report
        """
        with self.db_manager.get_session() as session:
            user = session.query(User).filter(User.id == user_id).first()

            if not user:
                return {"error": "User not found"}

            # Get overall adherence
            overall_adherence = self.get_user_adherence_rate(user_id, days)

            # Get adherence by medication
            medications = session.query(Medication).filter(
                Medication.user_id == user_id
            ).all()

            medication_adherence = []
            for med in medications:
                med_adherence = self.get_medication_adherence_rate(med.id, days)
                medication_adherence.append(med_adherence)

            # Get missed medications
            missed = self.get_missed_medications(user_id, days)

            # Get upcoming medications
            upcoming = self.get_upcoming_medications(user_id, 24)

            return {
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "phone": user.phone_number
                },
                "report_period_days": days,
                "generated_at": datetime.now().isoformat(),
                "overall_adherence": overall_adherence,
                "medication_adherence": medication_adherence,
                "missed_medications": missed,
                "upcoming_medications": upcoming
            }
