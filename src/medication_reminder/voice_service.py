"""Voice call service using Twilio for medication reminders."""

from datetime import datetime
from typing import Optional, Dict, Any
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
from loguru import logger

from .config import get_settings
from .models import User, Medication, ReminderLog, ReminderStatus


class VoiceCallService:
    """Handles voice call operations for medication reminders."""

    def __init__(self):
        self.settings = get_settings()
        self.client = Client(
            self.settings.twilio_account_sid,
            self.settings.twilio_auth_token
        )
        self.from_number = self.settings.twilio_phone_number

    def create_reminder_message(
        self,
        user: User,
        medication: Medication,
        time_of_day: str
    ) -> str:
        """Create a personalized reminder message."""
        greeting = self._get_time_appropriate_greeting()

        message = (
            f"{greeting} {user.name}. "
            f"This is your medication reminder. "
            f"It's time to take your {medication.name}, {medication.dosage}. "
        )

        if medication.instructions:
            message += f"{medication.instructions}. "

        message += (
            "Press 1 if you have taken your medication, "
            "or press 2 if you need help. "
            "If you don't respond, we will try calling again shortly."
        )

        return message

    def _get_time_appropriate_greeting(self) -> str:
        """Get a greeting appropriate for the current time of day."""
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return "Good morning"
        elif 12 <= hour < 17:
            return "Good afternoon"
        elif 17 <= hour < 21:
            return "Good evening"
        else:
            return "Hello"

    def generate_twiml_response(
        self,
        message: str,
        callback_url: Optional[str] = None
    ) -> str:
        """Generate TwiML response for the voice call."""
        response = VoiceResponse()

        # Gather user input
        gather = Gather(
            num_digits=1,
            action=callback_url or "/voice/gather",
            method="POST",
            timeout=10
        )

        # Say the message with better voice
        gather.say(
            message,
            voice="Polly.Joanna",  # Amazon Polly voice (female, US English)
            language="en-US"
        )

        response.append(gather)

        # If no input, thank them and hang up
        response.say(
            "We didn't receive your response. We'll try again shortly. Take care.",
            voice="Polly.Joanna",
            language="en-US"
        )

        return str(response)

    def make_reminder_call(
        self,
        to_number: str,
        user: User,
        medication: Medication,
        reminder_log: ReminderLog,
        callback_url: Optional[str] = None
    ) -> Optional[str]:
        """
        Make a voice call to remind about medication.

        Returns:
            Call SID if successful, None otherwise.
        """
        try:
            message = self.create_reminder_message(
                user,
                medication,
                reminder_log.scheduled_time.strftime("%I:%M %p")
            )

            twiml = self.generate_twiml_response(message, callback_url)

            # Make the call
            call = self.client.calls.create(
                to=to_number,
                from_=self.from_number,
                twiml=twiml,
                status_callback=callback_url or "/voice/status",
                status_callback_event=["completed"]
            )

            logger.info(
                f"Reminder call initiated for user {user.name} "
                f"(medication: {medication.name}). Call SID: {call.sid}"
            )

            return call.sid

        except Exception as e:
            logger.error(f"Failed to make reminder call: {e}")
            return None

    def make_caregiver_notification_call(
        self,
        to_number: str,
        patient_name: str,
        medication_name: str,
        scheduled_time: datetime
    ) -> Optional[str]:
        """
        Make a voice call to notify caregiver about missed medication.

        Returns:
            Call SID if successful, None otherwise.
        """
        try:
            message = (
                f"This is an important notification from the medication reminder system. "
                f"{patient_name} has not confirmed taking their {medication_name} "
                f"scheduled for {scheduled_time.strftime('%I:%M %p')}. "
                f"Please check on them to ensure they are okay and have taken their medication. "
                f"Press any key to acknowledge this notification."
            )

            response = VoiceResponse()
            gather = Gather(num_digits=1, timeout=10)
            gather.say(message, voice="Polly.Joanna", language="en-US")
            response.append(gather)
            response.say("Thank you.", voice="Polly.Joanna", language="en-US")

            call = self.client.calls.create(
                to=to_number,
                from_=self.from_number,
                twiml=str(response)
            )

            logger.info(
                f"Caregiver notification call made to {to_number}. "
                f"Call SID: {call.sid}"
            )

            return call.sid

        except Exception as e:
            logger.error(f"Failed to make caregiver notification call: {e}")
            return None

    def get_call_status(self, call_sid: str) -> Optional[Dict[str, Any]]:
        """Get the status of a call."""
        try:
            call = self.client.calls(call_sid).fetch()
            return {
                "status": call.status,
                "duration": call.duration,
                "start_time": call.start_time,
                "end_time": call.end_time,
                "direction": call.direction,
            }
        except Exception as e:
            logger.error(f"Failed to get call status: {e}")
            return None

    def handle_gather_response(self, digit_pressed: str) -> Dict[str, Any]:
        """
        Handle the digit pressed by the user during the call.

        Returns:
            Dictionary with response status and message.
        """
        response = VoiceResponse()

        if digit_pressed == "1":
            # User confirmed taking medication
            response.say(
                "Thank you for confirming. Have a wonderful day!",
                voice="Polly.Joanna",
                language="en-US"
            )
            return {
                "status": "confirmed",
                "message": "Medication confirmed",
                "twiml": str(response)
            }

        elif digit_pressed == "2":
            # User needs help
            response.say(
                "Help is on the way. We're notifying your caregiver now. "
                "Stay on the line if this is an emergency, or hang up if you just need assistance.",
                voice="Polly.Joanna",
                language="en-US"
            )
            return {
                "status": "needs_help",
                "message": "User requested help",
                "twiml": str(response)
            }

        else:
            # Unknown input
            response.say(
                "We didn't understand your response. "
                "We'll try calling again shortly.",
                voice="Polly.Joanna",
                language="en-US"
            )
            return {
                "status": "unknown",
                "message": "Unknown input",
                "twiml": str(response)
            }
