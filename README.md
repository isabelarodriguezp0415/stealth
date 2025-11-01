# Elder Medication Reminder Agent

An AI-powered medication reminder system designed to help elderly people manage their medications through automated voice call reminders, intelligent scheduling, and caregiver notifications.

## Features

### Core Functionality
- **Voice Call Reminders**: Automated voice calls to remind users to take medications at scheduled times
- **AI-Powered Interface**: Natural language processing for easy medication management
- **Smart Scheduling**: Flexible scheduling with support for daily, specific days, and multiple times per day
- **Medication Tracking**: Comprehensive adherence tracking and reporting
- **Caregiver Notifications**: Automatic alerts to caregivers when medications are missed
- **Multi-Attempt System**: Retries reminders up to a configurable number of times before escalating

### Key Features

#### 1. Voice Call Reminders
- Personalized voice messages using Amazon Polly
- Interactive voice response (IVR) for confirmation
- Time-appropriate greetings (Good morning, afternoon, evening)
- Clear medication instructions and dosage information

#### 2. Medication Management
- Add/remove medications with flexible schedules
- Support for multiple medications per user
- Dosage tracking and special instructions
- Medication purpose and prescribing doctor information

#### 3. Intelligent Scheduling
- Daily or specific days of the week
- Multiple times per day
- Timezone support for different locations
- Automatic rescheduling

#### 4. Tracking & Reporting
- Medication adherence rates
- Missed medication alerts
- Upcoming medication schedules
- Historical tracking and analytics

#### 5. Caregiver Support
- Multiple caregivers per user
- Automatic notifications for missed medications
- Configurable notification delays
- Voice call notifications to caregivers

#### 6. AI Natural Language Interface
- Add medications using natural language: "I need to take Aspirin 100mg every morning at 8am"
- Query schedules: "What medications do I need to take today?"
- Check adherence: "How am I doing with my medications?"
- Manage caregivers conversationally

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Elder Medication Reminder                 │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐      ┌───────────┐  │
│  │  AI Agent    │◄────►│  Scheduler   │◄────►│  Voice    │  │
│  │ (OpenAI GPT) │      │ (APScheduler)│      │  Service  │  │
│  └──────────────┘      └──────────────┘      │  (Twilio) │  │
│         │                      │              └───────────┘  │
│         │                      │                     │       │
│         ▼                      ▼                     ▼       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Database (SQLite/PostgreSQL)            │   │
│  │  - Users  - Medications  - Schedules  - Reminders   │   │
│  │  - Caregivers  - Tracking Logs                      │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Installation

### Prerequisites

- Python 3.9 or higher
- Twilio account (for voice calls)
- OpenAI API key (for AI features)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd stealth
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your credentials:
   ```env
   # Twilio Configuration
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_PHONE_NUMBER=+1234567890

   # OpenAI Configuration
   OPENAI_API_KEY=your_openai_api_key

   # Database Configuration
   DATABASE_URL=sqlite:///./medication_reminders.db

   # Application Settings
   TIMEZONE=America/New_York
   CAREGIVER_NOTIFICATION_DELAY_MINUTES=15
   MAX_REMINDER_ATTEMPTS=3
   ```

5. **Install the package**
   ```bash
   pip install -e .
   ```

## Usage

### Running the Service

#### As a Background Service
```bash
python -m medication_reminder.main
```

This starts the scheduler and keeps it running. The service will:
- Initialize the database
- Start the medication reminder scheduler
- Listen for scheduled reminder times
- Send voice call reminders automatically

#### Interactive CLI
```bash
python -m medication_reminder.cli
```

This provides an interactive command-line interface for:
- Adding users
- Managing medications
- Adding caregivers
- Chatting with the AI assistant
- Viewing reports

### Python API

```python
from medication_reminder.service import MedicationReminderService

# Initialize the service
service = MedicationReminderService()
service.initialize()

# Create a user
user = service.create_user(
    name="John Doe",
    phone_number="+1234567890",
    timezone="America/New_York"
)

# Add a medication with schedule
medication = service.add_medication(
    user_id=user.id,
    name="Aspirin",
    dosage="100mg",
    times=["08:00", "20:00"],  # 8 AM and 8 PM
    instructions="Take with food",
    purpose="Blood pressure"
)

# Add a caregiver
caregiver = service.add_caregiver(
    user_id=user.id,
    name="Jane Doe",
    phone_number="+1987654321",
    relationship_type="daughter"
)

# Use the AI assistant
result = service.process_natural_language(
    user_id=user.id,
    message="What medications do I need to take today?"
)
print(result['reply'])

# Get adherence report
report = service.get_adherence_report(user_id=user.id, days=30)
print(f"Adherence rate: {report['overall_adherence']['adherence_rate']}%")
```

### Natural Language Examples

The AI agent understands natural language commands:

```python
# Adding medications
"I need to take Lisinopril 10mg twice a day at 8am and 8pm for blood pressure"
"Add Metformin 500mg three times daily with meals"

# Querying schedule
"What medications do I take today?"
"When is my next medication?"
"Show me my medication schedule"

# Checking adherence
"How am I doing with my medications?"
"Did I miss any medications this week?"

# Managing caregivers
"Add my daughter Sarah as a caregiver, her number is 555-0123"
```

## How It Works

### Reminder Flow

1. **Scheduling**: Medications are scheduled based on user-defined times and days
2. **Reminder Trigger**: At the scheduled time, a voice call is initiated
3. **Voice Call**: User receives a personalized voice call with medication details
4. **Confirmation**: User can confirm by pressing 1, request help with 2
5. **Follow-up**: If not confirmed, system retries based on MAX_REMINDER_ATTEMPTS
6. **Caregiver Alert**: After max attempts, caregivers are notified via voice call

### Voice Call Interaction

When a user receives a reminder call:

```
"Good morning, John. This is your medication reminder.
It's time to take your Aspirin, 100mg. Take with food.
Press 1 if you have taken your medication, or press 2 if you need help."
```

Responses:
- **Press 1**: Confirms medication taken, reminder marked as complete
- **Press 2**: Triggers immediate caregiver notification for assistance
- **No response**: System retries after configured delay

### Caregiver Notification

When medications are missed:

```
"This is an important notification from the medication reminder system.
John Doe has not confirmed taking their Aspirin scheduled for 8:00 AM.
Please check on them to ensure they are okay and have taken their medication."
```

## Database Schema

### Users
- Personal information (name, phone, timezone)
- Medication history
- Associated caregivers

### Medications
- Medication details (name, dosage, instructions)
- Purpose and prescribing doctor
- Active/inactive status

### Medication Schedules
- Time of day for each dose
- Days of week (or daily)
- Active/inactive status

### Reminder Logs
- Scheduled and actual call times
- Confirmation status
- Attempt counts
- Call details (SID, duration)

### Caregivers
- Contact information
- Relationship to user
- Notification preferences

## Testing

Run the test suite:

```bash
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ --cov=medication_reminder --cov-report=html
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TWILIO_ACCOUNT_SID` | Twilio account SID | Required |
| `TWILIO_AUTH_TOKEN` | Twilio auth token | Required |
| `TWILIO_PHONE_NUMBER` | Twilio phone number | Required |
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `DATABASE_URL` | Database connection URL | `sqlite:///./medication_reminders.db` |
| `TIMEZONE` | Default timezone | `America/New_York` |
| `CAREGIVER_NOTIFICATION_DELAY_MINUTES` | Delay before notifying caregiver | `15` |
| `MAX_REMINDER_ATTEMPTS` | Max retry attempts | `3` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Production Deployment

### Using systemd (Linux)

Create `/etc/systemd/system/medication-reminder.service`:

```ini
[Unit]
Description=Elder Medication Reminder Service
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/stealth
Environment="PATH=/path/to/stealth/venv/bin"
ExecStart=/path/to/stealth/venv/bin/python -m medication_reminder.main
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable medication-reminder
sudo systemctl start medication-reminder
sudo systemctl status medication-reminder
```

### Using Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install -e .

CMD ["python", "-m", "medication_reminder.main"]
```

Build and run:
```bash
docker build -t medication-reminder .
docker run -d --name medication-reminder \
  --env-file .env \
  -v $(pwd)/medication_reminders.db:/app/medication_reminders.db \
  medication-reminder
```

## Security Considerations

- Store API keys securely (use environment variables, not hardcoded)
- Use HTTPS for any web interfaces
- Implement proper authentication for API access
- Regularly backup the database
- Follow HIPAA guidelines if handling protected health information
- Encrypt sensitive data at rest and in transit

## Troubleshooting

### Voice calls not working
- Verify Twilio credentials are correct
- Check Twilio account balance
- Ensure phone numbers are in E.164 format (+1234567890)
- Check Twilio console for error logs

### Scheduler not running
- Check logs in `logs/` directory
- Verify timezone settings
- Ensure database is accessible
- Check for any Python errors in the logs

### AI not responding
- Verify OpenAI API key is valid
- Check OpenAI account status and credits
- Review API rate limits
- Check logs for specific errors

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or feature requests, please open an issue on GitHub.

## Acknowledgments

- Twilio for voice communication services
- OpenAI for AI capabilities
- APScheduler for reliable scheduling
- SQLAlchemy for database management

---

**Made with care for helping elderly people maintain their health through medication adherence.**
