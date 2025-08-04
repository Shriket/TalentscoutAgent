"""
Constants for TalentScout Hiring Assistant
"""

# Application constants
APP_NAME = "TalentScout Hiring Assistant"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "AI-powered candidate screening and technical assessment"

# API Configuration
GROQ_MODEL_NAME = "llama-3.1-70b-versatile"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 1000
MAX_RESPONSE_TIME = 2.0  # seconds

# Conversation limits
MAX_CHAT_HISTORY = 50
MAX_MESSAGE_LENGTH = 1000
MAX_TECHNICAL_QUESTIONS = 5
MIN_TECHNICAL_QUESTIONS = 3

# Validation constants
MIN_NAME_LENGTH = 2
MAX_NAME_LENGTH = 100
MIN_PHONE_DIGITS = 10
MAX_PHONE_DIGITS = 15
MIN_EXPERIENCE_YEARS = 0
MAX_EXPERIENCE_YEARS = 50

# Sentiment analysis
SENTIMENT_THRESHOLD = 0.1
CONFIDENCE_THRESHOLD = 0.5

# Session management
SESSION_TIMEOUT_MINUTES = 30
MAX_CONCURRENT_SESSIONS = 10

# File paths
LOG_FILE_PATH = "logs/talentscout.log"
BACKUP_DIRECTORY = "backups/"
EXPORT_DIRECTORY = "exports/"

# UI constants
CHAT_CONTAINER_HEIGHT = 500
PROGRESS_BAR_HEIGHT = 10
MESSAGE_BUBBLE_PADDING = "1rem"

# Colors (matching CSS)
PRIMARY_COLOR = "#1f77b4"
SECONDARY_COLOR = "#2e86c1"
SUCCESS_COLOR = "#4caf50"
WARNING_COLOR = "#ff9800"
ERROR_COLOR = "#f44336"
NEUTRAL_COLOR = "#666666"

# Emoji mappings
SENTIMENT_EMOJIS = {
    "positive": "😊",
    "negative": "😟",
    "neutral": "😐"
}

TREND_EMOJIS = {
    "improving": "📈",
    "declining": "📉",
    "stable": "➡️"
}

STAGE_EMOJIS = {
    "greeting": "👋",
    "info_collection": "📝",
    "tech_stack": "💻",
    "technical_questions": "❓",
    "summary": "📊",
    "ended": "✅"
}

# Error messages
ERROR_MESSAGES = {
    "groq_api_error": "Unable to connect to AI service. Please try again.",
    "sheets_api_error": "Unable to save data. Your progress is still maintained locally.",
    "validation_error": "Please check your input and try again.",
    "session_timeout": "Your session has expired. Please start a new interview.",
    "general_error": "An unexpected error occurred. Please try again."
}

# Success messages
SUCCESS_MESSAGES = {
    "data_saved": "Your information has been saved successfully!",
    "interview_completed": "Interview completed successfully!",
    "validation_passed": "Information validated successfully.",
    "session_started": "Interview session started successfully."
}

# Help text
HELP_TEXT = {
    "general": """
    Welcome to TalentScout Hiring Assistant! Here's how to get the most out of your interview:
    
    • Be honest and specific about your experience
    • Provide complete information when asked
    • Take your time with technical questions
    • Ask for clarification if needed
    """,
    
    "commands": """
    Available commands:
    • "help" - Show this help message
    • "bye" or "quit" - End the interview
    • "start over" - Restart the interview
    • "export" - Download conversation history
    """,
    
    "technical_questions": """
    Tips for technical questions:
    • Explain your thought process
    • Use specific examples from your experience
    • It's okay to say "I don't know" if unsure
    • Ask for clarification if the question is unclear
    """
}

# Regular expressions
REGEX_PATTERNS = {
    "email": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    "phone": r'^\+?[\d\s\-\(\)]{10,15}$',
    "name": r'^[a-zA-Z\s\-\.\']{2,100}$',
    "experience": r'(\d+)\s*(?:years?|yrs?)',
    "tech_stack": r'[a-zA-Z0-9\+\#\.\-\s]+',
}

# Default responses
DEFAULT_RESPONSES = {
    "greeting": "Hello! I'm TalentScout's hiring assistant. I'm here to help with your application process.",
    "fallback": "I apologize, but I didn't understand that. Could you please rephrase?",
    "error": "I'm experiencing some technical difficulties. Let's continue with the interview.",
    "goodbye": "Thank you for your time! We'll be in touch soon."
}

# Question categories
QUESTION_CATEGORIES = {
    "programming": ["algorithms", "data_structures", "coding_practices", "debugging"],
    "web_development": ["frontend", "backend", "apis", "databases"],
    "devops": ["deployment", "monitoring", "automation", "infrastructure"],
    "data_science": ["analysis", "modeling", "visualization", "statistics"],
    "mobile": ["ios", "android", "cross_platform", "ui_ux"]
}

# Experience level mappings
EXPERIENCE_LEVELS = {
    "junior": {"min": 0, "max": 2, "description": "Entry level with basic skills"},
    "mid": {"min": 3, "max": 7, "description": "Experienced with proven track record"},
    "senior": {"min": 8, "max": 50, "description": "Expert level with leadership experience"}
}

# Tech stack categories
TECH_CATEGORIES = {
    "programming_languages": [
        "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", 
        "Go", "Rust", "PHP", "Ruby", "Swift", "Kotlin", "Scala"
    ],
    "web_frameworks": [
        "React", "Angular", "Vue.js", "Django", "Flask", "FastAPI",
        "Spring Boot", "Express.js", "Next.js", "Laravel", "Rails"
    ],
    "databases": [
        "MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite",
        "Oracle", "SQL Server", "Cassandra", "DynamoDB"
    ],
    "cloud_platforms": [
        "AWS", "Google Cloud Platform", "Microsoft Azure", 
        "Digital Ocean", "Heroku", "Vercel", "Netlify"
    ],
    "devops_tools": [
        "Docker", "Kubernetes", "Jenkins", "GitLab CI", "GitHub Actions",
        "Terraform", "Ansible", "Prometheus", "Grafana", "Git"
    ],
    "data_tools": [
        "Pandas", "NumPy", "TensorFlow", "PyTorch", "Scikit-learn",
        "Apache Spark", "Hadoop", "Kafka", "Airflow", "Tableau"
    ]
}

# Multilingual support
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi", 
    "es": "Spanish"
}

# Performance metrics
PERFORMANCE_TARGETS = {
    "response_time": 2.0,  # seconds
    "completion_rate": 90,  # percentage
    "user_satisfaction": 4.5,  # out of 5
    "error_rate": 5  # percentage
}

# Export formats
EXPORT_FORMATS = {
    "txt": "Plain Text",
    "json": "JSON Format",
    "csv": "CSV Format"
}

# Logging levels
LOG_LEVELS = {
    "DEBUG": 10,
    "INFO": 20,
    "WARNING": 30,
    "ERROR": 40,
    "CRITICAL": 50
}
