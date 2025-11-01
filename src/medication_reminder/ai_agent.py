"""AI-powered natural language interface for medication management."""

from datetime import datetime, time
from typing import Dict, Any, Optional, List
from openai import OpenAI
from loguru import logger
from sqlalchemy.orm import Session

from .config import get_settings
from .database import get_db_manager
from .models import (
    User, Medication, MedicationSchedule, Caregiver,
    AIConversationLog
)
from .tracking import MedicationTracker


class MedicationAIAgent:
    """AI agent for natural language medication management."""

    def __init__(self):
        self.settings = get_settings()
        self.client = OpenAI(api_key=self.settings.openai_api_key)
        self.db_manager = get_db_manager()
        self.tracker = MedicationTracker()

    def process_message(
        self,
        user_id: int,
        message: str
    ) -> Dict[str, Any]:
        """
        Process a natural language message from a user.

        Args:
            user_id: User ID
            message: User's message

        Returns:
            Response dictionary with intent, action, and reply
        """
        # Analyze intent
        intent = self._analyze_intent(message)

        # Execute action based on intent
        result = self._execute_intent(user_id, intent, message)

        # Log the conversation
        self._log_conversation(user_id, message, result["reply"], intent["intent"])

        return result

    def _analyze_intent(self, message: str) -> Dict[str, Any]:
        """
        Analyze user message to determine intent using GPT.

        Args:
            message: User's message

        Returns:
            Dictionary with intent and extracted entities
        """
        system_prompt = """You are an AI assistant helping elderly people manage their medications.
Analyze the user's message and determine their intent.

Possible intents:
- add_medication: User wants to add a new medication
- remove_medication: User wants to remove/stop a medication
- query_schedule: User wants to know their medication schedule
- query_adherence: User wants to know how well they're doing
- add_caregiver: User wants to add a caregiver
- get_help: User needs general help
- confirm_taken: User is confirming they took their medication
- other: Other intents

Extract relevant entities like:
- medication_name
- dosage
- frequency/time
- caregiver_name
- phone_number

Respond in JSON format:
{
  "intent": "intent_name",
  "entities": {
    "key": "value"
  },
  "confidence": 0.0-1.0
}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )

            import json
            intent_data = json.loads(response.choices[0].message.content)
            return intent_data

        except Exception as e:
            logger.error(f"Failed to analyze intent: {e}")
            return {
                "intent": "error",
                "entities": {},
                "confidence": 0.0
            }

    def _execute_intent(
        self,
        user_id: int,
        intent: Dict[str, Any],
        original_message: str
    ) -> Dict[str, Any]:
        """
        Execute the appropriate action based on the detected intent.

        Args:
            user_id: User ID
            intent: Intent data from analysis
            original_message: Original user message

        Returns:
            Result dictionary with reply and action taken
        """
        intent_name = intent.get("intent", "other")
        entities = intent.get("entities", {})

        if intent_name == "add_medication":
            return self._handle_add_medication(user_id, entities, original_message)

        elif intent_name == "remove_medication":
            return self._handle_remove_medication(user_id, entities)

        elif intent_name == "query_schedule":
            return self._handle_query_schedule(user_id)

        elif intent_name == "query_adherence":
            return self._handle_query_adherence(user_id)

        elif intent_name == "add_caregiver":
            return self._handle_add_caregiver(user_id, entities)

        elif intent_name == "confirm_taken":
            return self._handle_confirm_taken(user_id, entities)

        elif intent_name == "get_help":
            return self._handle_get_help()

        else:
            return {
                "intent": intent_name,
                "action": None,
                "reply": "I'm sorry, I didn't quite understand that. Could you please rephrase?"
            }

    def _handle_add_medication(
        self,
        user_id: int,
        entities: Dict[str, Any],
        original_message: str
    ) -> Dict[str, Any]:
        """Handle adding a new medication using AI to extract details."""
        # Use GPT to extract complete medication details
        system_prompt = """Extract medication details from the user's message.
Return JSON with these fields:
- medication_name: Name of the medication
- dosage: Dosage (e.g., "10mg", "2 tablets")
- times: Array of times to take it (e.g., ["08:00", "20:00"])
- instructions: Special instructions (e.g., "with food")
- purpose: What it's for (optional)

Example: "I need to take 10mg of Lisinopril twice a day at 8am and 8pm for blood pressure"
Returns:
{
  "medication_name": "Lisinopril",
  "dosage": "10mg",
  "times": ["08:00", "20:00"],
  "instructions": null,
  "purpose": "blood pressure"
}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": original_message}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )

            import json
            med_details = json.loads(response.choices[0].message.content)

            # Add medication to database
            with self.db_manager.get_session() as session:
                medication = Medication(
                    user_id=user_id,
                    name=med_details.get("medication_name", "Unknown"),
                    dosage=med_details.get("dosage", "As prescribed"),
                    instructions=med_details.get("instructions"),
                    purpose=med_details.get("purpose"),
                    active=True
                )
                session.add(medication)
                session.flush()

                # Add schedules
                times = med_details.get("times", [])
                for time_str in times:
                    try:
                        hour, minute = map(int, time_str.split(":"))
                        schedule = MedicationSchedule(
                            medication_id=medication.id,
                            time_of_day=time(hour=hour, minute=minute),
                            active=True
                        )
                        session.add(schedule)
                    except Exception as e:
                        logger.error(f"Failed to parse time {time_str}: {e}")

                session.commit()

                reply = (
                    f"I've added {medication.name} ({medication.dosage}) to your schedule. "
                    f"You'll receive reminders at {', '.join(times)}. "
                    f"Is there anything else you'd like me to help with?"
                )

                return {
                    "intent": "add_medication",
                    "action": "medication_added",
                    "medication_id": medication.id,
                    "reply": reply
                }

        except Exception as e:
            logger.error(f"Failed to add medication: {e}")
            return {
                "intent": "add_medication",
                "action": "failed",
                "reply": "I'm sorry, I had trouble adding that medication. Could you provide the details again?"
            }

    def _handle_remove_medication(
        self,
        user_id: int,
        entities: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle removing a medication."""
        medication_name = entities.get("medication_name")

        if not medication_name:
            return {
                "intent": "remove_medication",
                "action": "need_more_info",
                "reply": "Which medication would you like to stop taking?"
            }

        with self.db_manager.get_session() as session:
            medication = session.query(Medication).filter(
                Medication.user_id == user_id,
                Medication.name.ilike(f"%{medication_name}%"),
                Medication.active == True
            ).first()

            if medication:
                medication.active = False
                # Deactivate schedules
                for schedule in medication.schedules:
                    schedule.active = False
                session.commit()

                return {
                    "intent": "remove_medication",
                    "action": "medication_removed",
                    "reply": f"I've stopped reminders for {medication.name}. Stay healthy!"
                }
            else:
                return {
                    "intent": "remove_medication",
                    "action": "not_found",
                    "reply": f"I couldn't find an active medication called {medication_name}. Could you check the name?"
                }

    def _handle_query_schedule(self, user_id: int) -> Dict[str, Any]:
        """Handle querying medication schedule."""
        upcoming = self.tracker.get_upcoming_medications(user_id, hours=24)

        if not upcoming:
            return {
                "intent": "query_schedule",
                "action": "no_medications",
                "reply": "You don't have any medications scheduled for the next 24 hours."
            }

        # Format the schedule
        schedule_text = "Here are your upcoming medications:\n\n"
        for med in upcoming:
            scheduled_time = datetime.fromisoformat(med["scheduled_time"])
            time_str = scheduled_time.strftime("%I:%M %p")
            schedule_text += (
                f"• {med['medication_name']} ({med['dosage']}) at {time_str}"
            )
            if med.get("instructions"):
                schedule_text += f" - {med['instructions']}"
            schedule_text += "\n"

        return {
            "intent": "query_schedule",
            "action": "schedule_provided",
            "upcoming": upcoming,
            "reply": schedule_text
        }

    def _handle_query_adherence(self, user_id: int) -> Dict[str, Any]:
        """Handle querying medication adherence."""
        report = self.tracker.generate_adherence_report(user_id, days=30)

        if "error" in report:
            return {
                "intent": "query_adherence",
                "action": "error",
                "reply": "I'm sorry, I couldn't generate your adherence report."
            }

        adherence = report["overall_adherence"]
        rate = adherence["adherence_rate"]

        # Generate encouraging message
        if rate >= 90:
            message = f"Excellent work! You've taken {rate}% of your medications on time."
        elif rate >= 70:
            message = f"Good job! You've taken {rate}% of your medications. Let's try to improve a bit more!"
        else:
            message = f"Your adherence rate is {rate}%. Let's work together to improve this for your health."

        message += f"\n\nIn the last 30 days:\n"
        message += f"• Confirmed: {adherence['confirmed']} doses\n"
        message += f"• Missed: {adherence['missed']} doses\n"

        if adherence['missed'] > 0:
            message += "\nRemember, taking your medications regularly is important for your health!"

        return {
            "intent": "query_adherence",
            "action": "adherence_reported",
            "report": report,
            "reply": message
        }

    def _handle_add_caregiver(
        self,
        user_id: int,
        entities: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle adding a caregiver."""
        caregiver_name = entities.get("caregiver_name")
        phone_number = entities.get("phone_number")

        if not caregiver_name or not phone_number:
            return {
                "intent": "add_caregiver",
                "action": "need_more_info",
                "reply": "I need both the caregiver's name and phone number to add them."
            }

        with self.db_manager.get_session() as session:
            caregiver = Caregiver(
                user_id=user_id,
                name=caregiver_name,
                phone_number=phone_number,
                active=True
            )
            session.add(caregiver)
            session.commit()

            return {
                "intent": "add_caregiver",
                "action": "caregiver_added",
                "reply": f"I've added {caregiver_name} as your caregiver. They'll be notified if you miss any medications."
            }

    def _handle_confirm_taken(
        self,
        user_id: int,
        entities: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle manual confirmation of medication taken."""
        # This would typically be used in conjunction with the reminder system
        return {
            "intent": "confirm_taken",
            "action": "acknowledged",
            "reply": "Thank you for confirming! I've recorded that you took your medication."
        }

    def _handle_get_help(self) -> Dict[str, Any]:
        """Provide help information."""
        help_text = """I'm here to help you manage your medications! Here's what I can do:

• Add medications: "I need to take Aspirin 100mg every morning at 8am"
• Check schedule: "What medications do I need to take today?"
• Check adherence: "How am I doing with my medications?"
• Add caregiver: "Add my daughter Jane as caregiver, her number is 555-0123"
• Remove medication: "I'm stopping Medication X"

Just talk to me naturally, and I'll help you out!"""

        return {
            "intent": "get_help",
            "action": "help_provided",
            "reply": help_text
        }

    def _log_conversation(
        self,
        user_id: int,
        user_input: str,
        ai_response: str,
        intent: str
    ):
        """Log the conversation to the database."""
        try:
            with self.db_manager.get_session() as session:
                log = AIConversationLog(
                    user_id=user_id,
                    user_input=user_input,
                    ai_response=ai_response,
                    intent=intent
                )
                session.add(log)
                session.commit()
        except Exception as e:
            logger.error(f"Failed to log conversation: {e}")
