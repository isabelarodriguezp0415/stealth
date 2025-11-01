"""Command-line interface for managing the medication reminder system."""

import sys
from datetime import datetime
from loguru import logger

from .service import MedicationReminderService


def print_header():
    """Print CLI header."""
    print("\n" + "=" * 70)
    print("Elder Medication Reminder Agent - Management CLI")
    print("=" * 70 + "\n")


def print_menu():
    """Print main menu."""
    print("\nWhat would you like to do?")
    print("1. Add a new user")
    print("2. Add medication for a user")
    print("3. Add caregiver for a user")
    print("4. Talk to AI assistant")
    print("5. View adherence report")
    print("6. View upcoming medications")
    print("7. List all users")
    print("8. Exit")
    print()


def add_user_interactive(service: MedicationReminderService):
    """Interactively add a new user."""
    print("\n--- Add New User ---")
    name = input("Enter user name: ").strip()
    phone = input("Enter phone number (e.g., +1234567890): ").strip()
    timezone = input("Enter timezone (default: America/New_York): ").strip() or "America/New_York"

    try:
        user = service.create_user(name, phone, timezone=timezone)
        print(f"\n✓ User created successfully! User ID: {user.id}")
        return user
    except Exception as e:
        print(f"\n✗ Error creating user: {e}")
        return None


def add_medication_interactive(service: MedicationReminderService):
    """Interactively add a medication."""
    print("\n--- Add Medication ---")

    user_id = input("Enter user ID: ").strip()
    try:
        user_id = int(user_id)
    except ValueError:
        print("Invalid user ID")
        return

    user = service.get_user(user_id)
    if not user:
        print(f"User {user_id} not found")
        return

    print(f"Adding medication for: {user.name}")

    name = input("Medication name: ").strip()
    dosage = input("Dosage (e.g., 10mg, 2 tablets): ").strip()
    instructions = input("Instructions (optional): ").strip() or None
    purpose = input("Purpose (optional): ").strip() or None

    print("\nWhen should this medication be taken?")
    times_input = input("Enter times separated by commas (e.g., 08:00,20:00): ").strip()
    times = [t.strip() for t in times_input.split(",")]

    days_input = input("Days of week (0=Mon, 6=Sun, comma-separated, or leave blank for daily): ").strip()
    days_of_week = days_input if days_input else None

    try:
        medication = service.add_medication(
            user_id=user_id,
            name=name,
            dosage=dosage,
            times=times,
            instructions=instructions,
            purpose=purpose,
            days_of_week=days_of_week
        )
        print(f"\n✓ Medication added successfully! Medication ID: {medication.id}")
        print(f"Reminders scheduled for: {', '.join(times)}")
    except Exception as e:
        print(f"\n✗ Error adding medication: {e}")


def add_caregiver_interactive(service: MedicationReminderService):
    """Interactively add a caregiver."""
    print("\n--- Add Caregiver ---")

    user_id = input("Enter user ID: ").strip()
    try:
        user_id = int(user_id)
    except ValueError:
        print("Invalid user ID")
        return

    user = service.get_user(user_id)
    if not user:
        print(f"User {user_id} not found")
        return

    print(f"Adding caregiver for: {user.name}")

    name = input("Caregiver name: ").strip()
    phone = input("Phone number: ").strip()
    relationship = input("Relationship (e.g., daughter, son, nurse): ").strip() or None
    email = input("Email (optional): ").strip() or None

    try:
        caregiver = service.add_caregiver(
            user_id=user_id,
            name=name,
            phone_number=phone,
            relationship_type=relationship,
            email=email
        )
        print(f"\n✓ Caregiver added successfully! Caregiver ID: {caregiver.id}")
    except Exception as e:
        print(f"\n✗ Error adding caregiver: {e}")


def ai_chat_interactive(service: MedicationReminderService):
    """Interactive AI chat session."""
    print("\n--- AI Assistant ---")

    user_id = input("Enter user ID: ").strip()
    try:
        user_id = int(user_id)
    except ValueError:
        print("Invalid user ID")
        return

    user = service.get_user(user_id)
    if not user:
        print(f"User {user_id} not found")
        return

    print(f"\nChatting as: {user.name}")
    print("Type 'exit' to quit the chat\n")

    while True:
        message = input("You: ").strip()

        if message.lower() in ['exit', 'quit', 'bye']:
            print("Goodbye!")
            break

        if not message:
            continue

        try:
            result = service.process_natural_language(user_id, message)
            print(f"\nAI: {result['reply']}\n")
        except Exception as e:
            print(f"\n✗ Error: {e}\n")


def view_adherence_report(service: MedicationReminderService):
    """View adherence report for a user."""
    print("\n--- Adherence Report ---")

    user_id = input("Enter user ID: ").strip()
    try:
        user_id = int(user_id)
    except ValueError:
        print("Invalid user ID")
        return

    days = input("Number of days to look back (default: 30): ").strip()
    days = int(days) if days else 30

    try:
        report = service.get_adherence_report(user_id, days)

        if "error" in report:
            print(f"\n✗ {report['error']}")
            return

        print(f"\n--- Report for {report['user']['name']} ---")
        print(f"Period: Last {days} days")
        print(f"\nOverall Adherence: {report['overall_adherence']['adherence_rate']}%")
        print(f"Total Reminders: {report['overall_adherence']['total_reminders']}")
        print(f"Confirmed: {report['overall_adherence']['confirmed']}")
        print(f"Missed: {report['overall_adherence']['missed']}")

        if report['medication_adherence']:
            print("\nBy Medication:")
            for med in report['medication_adherence']:
                print(f"  • {med['medication_name']}: {med['adherence_rate']}%")

    except Exception as e:
        print(f"\n✗ Error: {e}")


def view_upcoming_medications(service: MedicationReminderService):
    """View upcoming medications for a user."""
    print("\n--- Upcoming Medications ---")

    user_id = input("Enter user ID: ").strip()
    try:
        user_id = int(user_id)
    except ValueError:
        print("Invalid user ID")
        return

    try:
        upcoming = service.get_upcoming_medications(user_id, hours=24)

        if not upcoming:
            print("\nNo upcoming medications in the next 24 hours.")
            return

        print("\nNext 24 hours:")
        for med in upcoming:
            scheduled = datetime.fromisoformat(med['scheduled_time'])
            print(f"  • {scheduled.strftime('%I:%M %p')} - {med['medication_name']} ({med['dosage']})")
            if med.get('instructions'):
                print(f"    Instructions: {med['instructions']}")

    except Exception as e:
        print(f"\n✗ Error: {e}")


def list_users(service: MedicationReminderService):
    """List all users."""
    print("\n--- All Users ---")

    from .database import get_db_manager
    from .models import User

    try:
        db_manager = get_db_manager()
        with db_manager.get_session() as session:
            users = session.query(User).filter(User.active == True).all()

            if not users:
                print("\nNo users found.")
                return

            for user in users:
                print(f"\nID: {user.id}")
                print(f"Name: {user.name}")
                print(f"Phone: {user.phone_number}")
                print(f"Timezone: {user.timezone}")

    except Exception as e:
        print(f"\n✗ Error: {e}")


def interactive_cli():
    """Run the interactive CLI."""
    print_header()

    # Suppress loguru output for cleaner CLI
    logger.remove()
    logger.add(sys.stderr, level="ERROR")

    # Initialize service
    service = MedicationReminderService()

    try:
        service.initialize()

        while True:
            print_menu()
            choice = input("Enter your choice (1-8): ").strip()

            if choice == "1":
                add_user_interactive(service)
            elif choice == "2":
                add_medication_interactive(service)
            elif choice == "3":
                add_caregiver_interactive(service)
            elif choice == "4":
                ai_chat_interactive(service)
            elif choice == "5":
                view_adherence_report(service)
            elif choice == "6":
                view_upcoming_medications(service)
            elif choice == "7":
                list_users(service)
            elif choice == "8":
                print("\nGoodbye!")
                break
            else:
                print("\n✗ Invalid choice. Please try again.")

    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    finally:
        service.shutdown()


if __name__ == "__main__":
    interactive_cli()
