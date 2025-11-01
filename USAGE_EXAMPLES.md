# Usage Examples

This document provides detailed examples of how to use the Elder Medication Reminder Agent.

## Table of Contents

1. [Basic Setup](#basic-setup)
2. [Managing Users](#managing-users)
3. [Managing Medications](#managing-medications)
4. [Managing Caregivers](#managing-caregivers)
5. [Using the AI Interface](#using-the-ai-interface)
6. [Tracking and Reports](#tracking-and-reports)
7. [Advanced Scenarios](#advanced-scenarios)

## Basic Setup

### First Time Setup

```python
from medication_reminder.service import MedicationReminderService

# Initialize service
service = MedicationReminderService()
service.initialize()

print("Service initialized and ready!")
```

## Managing Users

### Create a New User

```python
# Create a user
user = service.create_user(
    name="Mary Johnson",
    phone_number="+15551234567",
    timezone="America/Los_Angeles"
)

print(f"Created user: {user.name} (ID: {user.id})")
```

### Get User by Phone Number

```python
user = service.get_user_by_phone("+15551234567")
if user:
    print(f"Found user: {user.name}")
else:
    print("User not found")
```

## Managing Medications

### Add a Simple Daily Medication

```python
# Add medication taken once daily
medication = service.add_medication(
    user_id=user.id,
    name="Aspirin",
    dosage="81mg",
    times=["08:00"],  # 8:00 AM
    instructions="Take with breakfast",
    purpose="Heart health"
)

print(f"Added {medication.name} - will remind at 8:00 AM daily")
```

### Add Medication Taken Multiple Times Per Day

```python
# Add medication taken three times daily
medication = service.add_medication(
    user_id=user.id,
    name="Metformin",
    dosage="500mg",
    times=["08:00", "14:00", "20:00"],  # 8 AM, 2 PM, 8 PM
    instructions="Take with food",
    purpose="Blood sugar control"
)

print(f"Added {medication.name} - 3 reminders per day")
```

### Add Medication for Specific Days

```python
# Add medication only on weekdays (Monday=0 to Friday=4)
medication = service.add_medication(
    user_id=user.id,
    name="Vitamin D",
    dosage="2000 IU",
    times=["09:00"],
    days_of_week="0,1,2,3,4",  # Monday through Friday
    purpose="Vitamin supplement"
)

print(f"Added {medication.name} - weekdays only")
```

### Remove a Medication

```python
# Deactivate a medication
service.remove_medication(medication_id=5)
print("Medication removed and reminders stopped")
```

## Managing Caregivers

### Add a Caregiver

```python
# Add primary caregiver
caregiver = service.add_caregiver(
    user_id=user.id,
    name="Sarah Johnson",
    phone_number="+15559876543",
    relationship_type="daughter",
    email="sarah@example.com"
)

print(f"Added caregiver: {caregiver.name}")
```

### Add Multiple Caregivers

```python
# Add multiple caregivers
caregivers = [
    {
        "name": "Dr. Smith",
        "phone_number": "+15551112222",
        "relationship_type": "doctor",
        "email": "dr.smith@clinic.com"
    },
    {
        "name": "Home Nurse",
        "phone_number": "+15553334444",
        "relationship_type": "nurse"
    }
]

for caregiver_info in caregivers:
    caregiver = service.add_caregiver(
        user_id=user.id,
        **caregiver_info
    )
    print(f"Added {caregiver.name}")
```

## Using the AI Interface

### Natural Language Medication Addition

```python
# User speaks naturally
result = service.process_natural_language(
    user_id=user.id,
    message="I need to take Lisinopril 10mg every morning at 8am for blood pressure"
)

print(result['reply'])
# Output: "I've added Lisinopril (10mg) to your schedule.
#          You'll receive reminders at 08:00. Is there anything else?"
```

### Query Today's Schedule

```python
result = service.process_natural_language(
    user_id=user.id,
    message="What medications do I need to take today?"
)

print(result['reply'])
# Output: "Here are your upcoming medications:
#          • Aspirin (81mg) at 08:00 AM - Take with breakfast
#          • Metformin (500mg) at 08:00 AM - Take with food
#          ..."
```

### Check Adherence

```python
result = service.process_natural_language(
    user_id=user.id,
    message="How am I doing with my medications?"
)

print(result['reply'])
# Output: "Excellent work! You've taken 95% of your medications on time.
#          In the last 30 days:
#          • Confirmed: 57 doses
#          • Missed: 3 doses"
```

### Add Caregiver via AI

```python
result = service.process_natural_language(
    user_id=user.id,
    message="Add my son Robert as caregiver, phone number +15556667777"
)

print(result['reply'])
# Output: "I've added Robert as your caregiver.
#          They'll be notified if you miss any medications."
```

## Tracking and Reports

### Get Adherence Report

```python
# Get 30-day adherence report
report = service.get_adherence_report(user_id=user.id, days=30)

print(f"Overall adherence: {report['overall_adherence']['adherence_rate']}%")
print(f"Total reminders: {report['overall_adherence']['total_reminders']}")
print(f"Confirmed: {report['overall_adherence']['confirmed']}")
print(f"Missed: {report['overall_adherence']['missed']}")

print("\nBy Medication:")
for med in report['medication_adherence']:
    print(f"  {med['medication_name']}: {med['adherence_rate']}%")
```

### Get Upcoming Medications

```python
# Get medications for next 24 hours
upcoming = service.get_upcoming_medications(user_id=user.id, hours=24)

print("Upcoming medications:")
for med in upcoming:
    print(f"  {med['scheduled_time']} - {med['medication_name']} ({med['dosage']})")
```

## Advanced Scenarios

### Complete Setup for New Patient

```python
from medication_reminder.service import MedicationReminderService
from datetime import datetime

# Initialize
service = MedicationReminderService()
service.initialize()

# 1. Create user
user = service.create_user(
    name="Robert Williams",
    phone_number="+15557778888",
    date_of_birth=datetime(1945, 6, 15),
    timezone="America/Chicago"
)

# 2. Add multiple medications
medications = [
    {
        "name": "Lisinopril",
        "dosage": "10mg",
        "times": ["08:00"],
        "instructions": "Take in the morning",
        "purpose": "Blood pressure"
    },
    {
        "name": "Metformin",
        "dosage": "500mg",
        "times": ["08:00", "20:00"],
        "instructions": "Take with food",
        "purpose": "Diabetes"
    },
    {
        "name": "Atorvastatin",
        "dosage": "20mg",
        "times": ["21:00"],
        "instructions": "Take at bedtime",
        "purpose": "Cholesterol"
    }
]

for med_info in medications:
    medication = service.add_medication(user_id=user.id, **med_info)
    print(f"✓ Added {medication.name}")

# 3. Add caregivers
caregivers = [
    {
        "name": "Emily Williams",
        "phone_number": "+15552223333",
        "relationship_type": "daughter"
    },
    {
        "name": "Nurse Betty",
        "phone_number": "+15554445555",
        "relationship_type": "home_health_aide"
    }
]

for caregiver_info in caregivers:
    caregiver = service.add_caregiver(user_id=user.id, **caregiver_info)
    print(f"✓ Added caregiver {caregiver.name}")

print("\n✓ Setup complete!")
print(f"User {user.name} has {len(medications)} medications scheduled")
print(f"and {len(caregivers)} caregivers assigned")
```

### Interactive Voice Response Handling

```python
# This would typically be in a web server handling Twilio callbacks

from medication_reminder.voice_service import VoiceCallService

voice_service = VoiceCallService()

# When user presses a digit during call
digit_pressed = "1"  # User confirmed
response = voice_service.handle_gather_response(digit_pressed)

if response['status'] == 'confirmed':
    # Mark medication as taken
    service.confirm_medication_taken(reminder_log_id=123, method="voice")
    print("Medication confirmed!")

elif response['status'] == 'needs_help':
    # Notify caregivers immediately
    print("User needs help! Notifying caregivers...")
```

### Batch Operations

```python
# Add medications from a prescription list
prescriptions = [
    ("Aspirin", "81mg", ["08:00"], "Blood thinner"),
    ("Metoprolol", "25mg", ["08:00", "20:00"], "Heart rate"),
    ("Furosemide", "40mg", ["08:00"], "Diuretic"),
    ("Potassium", "20mEq", ["08:00"], "Supplement"),
]

for name, dosage, times, purpose in prescriptions:
    medication = service.add_medication(
        user_id=user.id,
        name=name,
        dosage=dosage,
        times=times,
        purpose=purpose
    )
    print(f"✓ {name} added")

print(f"\n✓ Added {len(prescriptions)} medications")
```

### Generating Reports for Multiple Users

```python
from medication_reminder.database import get_db_manager
from medication_reminder.models import User

db_manager = get_db_manager()

with db_manager.get_session() as session:
    users = session.query(User).filter(User.active == True).all()

print(f"Generating reports for {len(users)} users...\n")

for user in users:
    report = service.get_adherence_report(user.id, days=7)
    adherence = report['overall_adherence']['adherence_rate']

    print(f"{user.name}:")
    print(f"  Adherence: {adherence}%")

    if adherence < 80:
        print(f"  ⚠ WARNING: Low adherence!")

    print()
```

## Tips and Best Practices

### 1. Phone Number Format
Always use E.164 format for phone numbers:
```python
# Good
phone = "+15551234567"

# Bad
phone = "555-123-4567"
phone = "(555) 123-4567"
```

### 2. Timezone Management
Always specify timezones for accurate scheduling:
```python
user = service.create_user(
    name="User Name",
    phone_number="+15551234567",
    timezone="America/New_York"  # or America/Chicago, America/Los_Angeles, etc.
)
```

### 3. Testing Before Production
Test with your own phone number first:
```python
# Create test user with your number
test_user = service.create_user(
    name="Test User",
    phone_number="+1YOUR_NUMBER",
    timezone="YOUR_TIMEZONE"
)

# Add a test medication with immediate reminder
from datetime import datetime, timedelta
now = datetime.now()
next_minute = (now + timedelta(minutes=1)).strftime("%H:%M")

service.add_medication(
    user_id=test_user.id,
    name="Test Medication",
    dosage="1 tablet",
    times=[next_minute]
)

print(f"Test call will come in ~1 minute to {test_user.phone_number}")
```

### 4. Monitoring Adherence
Regular monitoring helps identify issues:
```python
# Check daily
report = service.get_adherence_report(user_id=user.id, days=7)

if report['overall_adherence']['adherence_rate'] < 70:
    print("⚠ Alert: User may need additional support")
    # Consider increasing caregiver involvement
```

### 5. Graceful Shutdown
Always shutdown the service properly:
```python
try:
    service.initialize()
    # ... do work ...
finally:
    service.shutdown()
```
