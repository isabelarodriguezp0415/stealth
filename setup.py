from setuptools import setup, find_packages

setup(
    name="elder-medication-reminder",
    version="0.1.0",
    description="AI-powered medication reminder agent for elderly people",
    author="Your Name",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.0",
        "sqlalchemy>=2.0.23",
        "apscheduler>=3.10.4",
        "twilio>=8.11.0",
        "openai>=1.6.1",
        "langchain>=0.1.0",
        "loguru>=0.7.2",
    ],
    entry_points={
        "console_scripts": [
            "med-reminder=medication_reminder.main:main",
        ],
    },
)
