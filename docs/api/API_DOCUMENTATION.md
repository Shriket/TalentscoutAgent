# 📡 TalentScout API Documentation

## 🏗️ Architecture Overview

TalentScout follows a modular architecture with clear separation of concerns:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend UI   │    │  Business Logic │    │   Data Layer    │
│   (Streamlit)   │◄──►│   (Managers)    │◄──►│  (Handlers)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ GDPR Compliance │    │   LLM Handler   │    │ Google Sheets   │
│    Module       │    │  (Groq API)     │    │     API         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔧 Core API Classes

### ConversationManager

**Location**: `src/chatbot/conversation_manager.py`

**Purpose**: Orchestrates the entire interview conversation flow

#### Methods

##### `__init__(self, session_state)`
Initializes the conversation manager with session state.

**Parameters**:
- `session_state`: Streamlit session state object

**Returns**: ConversationManager instance

##### `process_user_input(self, user_input: str) -> str`
Main method for processing user input and generating responses.

**Parameters**:
- `user_input` (str): User's text input

**Returns**: 
- `str`: Bot's response message

**Example**:
```python
manager = ConversationManager(st.session_state)
response = manager.process_user_input("John Smith")
print(response)  # "Great! What's your email address?"
```

##### `validate_input(self, input_value: str, field_name: str) -> bool`
Validates user input for specific fields with context-aware error handling.

**Parameters**:
- `input_value` (str): The input to validate
- `field_name` (str): Name of the field being validated

**Returns**:
- `bool`: True if valid, False otherwise

**Validation Rules**:
```python
VALIDATION_RULES = {
    'full_name': {
        'min_words': 2,
        'max_length': 100,
        'pattern': r'^[a-zA-Z\s]+$'
    },
    'email': {
        'format': 'email',
        'auto_correct': True  # ; → .
    },
    'phone': {
        'min_length': 10,
        'max_length': 15,
        'pattern': r'^[\d\s\-\+\(\)]+$'
    }
}
```

##### `update_conversation_state(self, new_state: ConversationState)`
Updates the current conversation state and triggers appropriate actions.

**Parameters**:
- `new_state` (ConversationState): New state to transition to

**State Flow**:
```
GREETING → INFO_COLLECTION → TECH_STACK → TECHNICAL_QUESTIONS → SUMMARY → COMPLETE
```

---

### LLMHandler

**Location**: `src/chatbot/llm_handler.py`

**Purpose**: Manages AI model interactions and prompt engineering

#### Methods

##### `__init__(self, api_key: str, model: str = "llama-3.1-8b-instant")`
Initializes the LLM handler with API credentials.

**Parameters**:
- `api_key` (str): Groq API key
- `model` (str): Model name (default: "llama-3.1-8b-instant")

##### `generate_response(self, prompt: str, context: dict = None) -> str`
Generates AI response based on prompt and context.

**Parameters**:
- `prompt` (str): The prompt template
- `context` (dict): Additional context variables

**Returns**:
- `str`: Generated response

**Example**:
```python
handler = LLMHandler(api_key="your_key")
response = handler.generate_response(
    prompt="Generate a technical question for {role}",
    context={"role": "Data Analyst", "tech_stack": "SQL, Python"}
)
```

##### `parse_tech_stack(self, tech_input: str) -> List[str]`
Parses and validates technology stack from user input.

**Parameters**:
- `tech_input` (str): Raw tech stack input

**Returns**:
- `List[str]`: Cleaned list of technologies

**Example**:
```python
tech_list = handler.parse_tech_stack("Python, SQL, Excel, Tableau")
# Returns: ["Python", "SQL", "Excel", "Tableau"]
```

---

### GDPRCompliance

**Location**: `src/utils/gdpr_compliance.py`

**Purpose**: Handles all privacy and GDPR compliance requirements

#### Methods

##### `encrypt_data(self, data: str) -> str`
Encrypts sensitive data using AES-128 (Fernet) encryption.

**Parameters**:
- `data` (str): Plain text data to encrypt

**Returns**:
- `str`: Base64 encoded encrypted data

**Example**:
```python
gdpr = GDPRCompliance()
encrypted_email = gdpr.encrypt_data("user@example.com")
```

##### `decrypt_data(self, encrypted_data: str) -> str`
Decrypts previously encrypted data.

**Parameters**:
- `encrypted_data` (str): Base64 encoded encrypted data

**Returns**:
- `str`: Decrypted plain text

##### `log_consent(self, user_id: str, consent_type: str, granted: bool)`
Logs user consent for audit purposes.

**Parameters**:
- `user_id` (str): Unique user identifier
- `consent_type` (str): Type of consent (e.g., "data_processing")
- `granted` (bool): Whether consent was granted

**Consent Types**:
- `data_processing`: General data processing consent
- `data_storage`: Data storage consent
- `marketing`: Marketing communications consent

##### `handle_data_request(self, request_type: str, user_data: dict) -> dict`
Processes data subject rights requests.

**Parameters**:
- `request_type` (str): Type of request
- `user_data` (dict): User's data for the request

**Request Types**:
- `access`: Right to access personal data
- `rectification`: Right to correct personal data
- `erasure`: Right to delete personal data
- `portability`: Right to data portability

**Returns**:
- `dict`: Response with requested data or confirmation

---

### SheetsHandler

**Location**: `src/data/sheets_handler.py`

**Purpose**: Manages Google Sheets integration and data persistence

#### Methods

##### `__init__(self, sheet_id: str, credentials_json: str)`
Initializes Google Sheets connection.

**Parameters**:
- `sheet_id` (str): Google Sheet ID
- `credentials_json` (str): Service account JSON credentials

##### `save_candidate_data(self, candidate_info: dict) -> bool`
Saves candidate information to Google Sheets.

**Parameters**:
- `candidate_info` (dict): Complete candidate data

**Returns**:
- `bool`: True if successful, False otherwise

**Data Structure**:
```python
candidate_data = {
    'Full_Name': 'John Smith',
    'Email': 'encrypted_email_data',
    'Phone': 'encrypted_phone_data',
    'Gender': 'Male',
    'Date_of_Birth': 'encrypted_dob_data',
    'Graduation_Year': 2020,
    'CGPA_10th': 9.2,
    'CGPA_12th': 8.8,
    'CGPA_Degree': 8.5,
    'Experience_Years': 3,
    'Desired_Positions': 'Data Analyst',
    'Current_Location': 'Mumbai, Maharashtra',
    'Tech_Stack': 'Python, SQL, Tableau',
    'Technical_Questions': 'Q1: ...\nQ2: ...',
    'Candidate_Responses': 'A1: ...\nA2: ...',
    'Questions_Answered': '5/5',
    'Work_Experience_Description': 'Worked as...',
    'Why_Good_Candidate': 'I am suitable because...',
    'Sentiment_Score': 0.75,
    'Interview_Date': '2024-01-15',
    'Interview_Duration': '12 minutes',
    'Completion_Status': 'Completed'
}
```

##### `update_record(self, row_id: int, updates: dict) -> bool`
Updates specific fields in an existing record.

**Parameters**:
- `row_id` (int): Row number to update
- `updates` (dict): Fields to update

**Returns**:
- `bool`: Success status

##### `export_data(self, filters: dict = None) -> List[dict]`
Exports data with optional filtering.

**Parameters**:
- `filters` (dict): Optional filters to apply

**Returns**:
- `List[dict]`: Filtered candidate records

---

## 🎯 Data Models

### CandidateInfo (Pydantic Model)

**Location**: `src/data/models.py`

```python
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime

class CandidateInfo(BaseModel):
    # Personal Information
    full_name: str
    email: EmailStr
    phone: str
    gender: str
    date_of_birth: str
    current_location: str
    
    # Educational Background
    graduation_year: int
    cgpa_10th: float
    cgpa_12th: float
    cgpa_degree: float
    
    # Professional Information
    experience_years: int
    desired_positions: str
    tech_stack: str
    work_experience: Optional[str] = None
    why_good_candidate: Optional[str] = None
    
    # Technical Assessment
    technical_questions: Optional[str] = None
    candidate_responses: Optional[str] = None
    questions_answered: Optional[str] = "0/0"
    
    # Analytics
    sentiment_score: Optional[float] = None
    interview_date: Optional[str] = None
    interview_duration: Optional[str] = None
    completion_status: str = "In Progress"
    
    @validator('graduation_year')
    def validate_graduation_year(cls, v):
        current_year = datetime.now().year
        if not (1990 <= v <= current_year + 5):
            raise ValueError('Graduation year must be between 1990 and current year + 5')
        return v
    
    @validator('cgpa_10th', 'cgpa_12th', 'cgpa_degree')
    def validate_cgpa(cls, v):
        if not (0.0 <= v <= 10.0):
            raise ValueError('CGPA must be between 0.0 and 10.0')
        return v
    
    @validator('experience_years')
    def validate_experience(cls, v):
        if not (0 <= v <= 50):
            raise ValueError('Experience years must be between 0 and 50')
        return v
```

### ConversationState (Enum)

```python
from enum import Enum

class ConversationState(Enum):
    GREETING = "greeting"
    INFO_COLLECTION = "info_collection"
    TECH_STACK = "tech_stack"
    TECHNICAL_QUESTIONS = "technical_questions"
    SUMMARY = "summary"
    COMPLETE = "complete"
```

---

## 🔌 External API Integration

### Groq API Integration

**Base URL**: `https://api.groq.com/openai/v1/chat/completions`

**Authentication**: Bearer token in Authorization header

**Request Format**:
```python
{
    "model": "llama-3.1-8b-instant",
    "messages": [
        {
            "role": "system",
            "content": "You are a professional interviewer..."
        },
        {
            "role": "user", 
            "content": "User's response"
        }
    ],
    "temperature": 0.7,
    "max_tokens": 1000,
    "top_p": 0.9
}
```

**Response Format**:
```python
{
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "Generated response"
            },
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 150,
        "completion_tokens": 75,
        "total_tokens": 225
    }
}
```

### Google Sheets API Integration

**Base URL**: `https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}`

**Authentication**: Service Account JSON with OAuth 2.0

**Common Operations**:

#### Read Data
```python
GET /values/{range}
```

#### Write Data
```python
POST /values/{range}:append
{
    "values": [
        ["John Smith", "john@email.com", "1234567890", ...]
    ]
}
```

#### Update Data
```python
PUT /values/{range}
{
    "values": [
        ["Updated Value"]
    ]
}
```

---

## 🧪 Testing API

### Unit Testing

**Location**: `tests/`

#### Test ConversationManager
```python
import pytest
from src.chatbot.conversation_manager import ConversationManager

def test_conversation_manager_init():
    """Test conversation manager initialization"""
    manager = ConversationManager(mock_session_state)
    assert manager.current_state == ConversationState.GREETING

def test_input_validation():
    """Test input validation logic"""
    manager = ConversationManager(mock_session_state)
    
    # Valid full name
    assert manager.validate_input("John Smith", "full_name") == True
    
    # Invalid full name (single word)
    assert manager.validate_input("John", "full_name") == False
    
    # Valid email
    assert manager.validate_input("john@email.com", "email") == True
    
    # Invalid email
    assert manager.validate_input("invalid-email", "email") == False
```

#### Test GDPR Compliance
```python
def test_data_encryption():
    """Test data encryption and decryption"""
    gdpr = GDPRCompliance()
    
    original_data = "sensitive@email.com"
    encrypted = gdpr.encrypt_data(original_data)
    decrypted = gdpr.decrypt_data(encrypted)
    
    assert decrypted == original_data
    assert encrypted != original_data

def test_consent_logging():
    """Test consent logging functionality"""
    gdpr = GDPRCompliance()
    
    gdpr.log_consent("user123", "data_processing", True)
    
    # Verify log entry was created
    assert len(gdpr.audit_log) > 0
    assert gdpr.audit_log[-1]['consent_granted'] == True
```

### Integration Testing

#### End-to-End Interview Flow
```python
def test_complete_interview_flow():
    """Test complete interview from start to finish"""
    
    # Initialize test session
    test_responses = [
        "John Smith",                    # Full name
        "john.smith@email.com",         # Email
        "9876543210",                   # Phone
        "Male",                         # Gender
        "1995-05-15",                   # Date of birth
        "2020",                         # Graduation year
        "9.2",                          # 10th CGPA
        "8.8",                          # 12th CGPA
        "8.5",                          # Degree CGPA
        "3",                            # Experience years
        "Data Analyst",                 # Desired position
        "Mumbai, Maharashtra",          # Location
        "Python, SQL, Tableau",         # Tech stack
        "I have experience with...",    # Work experience
        "I am suitable because...",     # Why good candidate
        # Technical questions responses...
    ]
    
    manager = ConversationManager(mock_session_state)
    
    for response in test_responses:
        bot_response = manager.process_user_input(response)
        assert bot_response is not None
        assert len(bot_response) > 0
    
    # Verify final state
    assert manager.current_state == ConversationState.COMPLETE
    
    # Verify data was saved
    assert mock_session_state.candidate_info is not None
    assert mock_session_state.candidate_info.full_name == "John Smith"
```

---

## 📊 Performance Metrics API

### Response Time Tracking
```python
import time
from functools import wraps

def track_response_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        response_time = end_time - start_time
        log_performance_metric("response_time", response_time)
        
        return result
    return wrapper

@track_response_time
def process_user_input(self, user_input: str) -> str:
    # Method implementation
    pass
```

### Usage Analytics
```python
class AnalyticsTracker:
    def __init__(self):
        self.metrics = {
            'total_interviews': 0,
            'completed_interviews': 0,
            'average_duration': 0,
            'completion_rate': 0
        }
    
    def track_interview_start(self, session_id: str):
        self.metrics['total_interviews'] += 1
        
    def track_interview_completion(self, session_id: str, duration: float):
        self.metrics['completed_interviews'] += 1
        self.update_completion_rate()
        self.update_average_duration(duration)
    
    def get_metrics(self) -> dict:
        return self.metrics.copy()
```

---

## 🔒 Security API

### Authentication
```python
def authenticate_request(api_key: str) -> bool:
    """Validate API key for external integrations"""
    return api_key == os.getenv('API_SECRET_KEY')

def rate_limit_check(user_id: str) -> bool:
    """Check if user has exceeded rate limits"""
    # Implementation for rate limiting
    pass
```

### Data Sanitization
```python
def sanitize_input(user_input: str) -> str:
    """Sanitize user input to prevent injection attacks"""
    import re
    
    # Remove potentially harmful characters
    sanitized = re.sub(r'[<>"\']', '', user_input)
    
    # Limit length
    sanitized = sanitized[:1000]
    
    return sanitized.strip()
```

---

## 📈 Monitoring & Logging API

### Error Logging
```python
import logging
from datetime import datetime

class ErrorLogger:
    def __init__(self):
        self.logger = logging.getLogger('talentscout')
        
    def log_error(self, error: Exception, context: dict = None):
        error_data = {
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context or {}
        }
        
        self.logger.error(f"Application Error: {error_data}")
```

### Health Check API
```python
def health_check() -> dict:
    """Return application health status"""
    try:
        # Check database connectivity
        sheets_status = test_sheets_connection()
        
        # Check AI API connectivity  
        llm_status = test_groq_connection()
        
        return {
            'status': 'healthy' if sheets_status and llm_status else 'unhealthy',
            'timestamp': datetime.now().isoformat(),
            'services': {
                'google_sheets': 'up' if sheets_status else 'down',
                'groq_api': 'up' if llm_status else 'down'
            }
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }
```

---

This API documentation provides comprehensive coverage of all TalentScout components, enabling developers to understand, integrate, and extend the system effectively.
