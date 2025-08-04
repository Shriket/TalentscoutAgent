"""
Pydantic Data Models for TalentScout Hiring Assistant
"""

from datetime import datetime
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, EmailStr, Field, validator
import re
import uuid

class CandidateInfo(BaseModel):
    """Main candidate information model"""
    
    # Required fields
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr = Field(...)
    phone: str = Field(..., min_length=10, max_length=15)
    experience_years: int = Field(..., ge=0, le=50)
    desired_positions: List[str] = Field(..., min_items=1)
    location: str = Field(..., min_length=2, max_length=100)
    tech_stack: List[str] = Field(..., min_items=1)
    
    # Additional required fields
    gender: str = Field(..., pattern=r'^(Male|Female|Transgender)$')
    date_of_birth: str = Field(..., min_length=8, max_length=12)  # DD/MM/YYYY or DD-MM-YYYY
    graduation_year: int = Field(..., ge=1990, le=2030)
    cgpa_10th: float = Field(..., ge=0.0, le=10.0)
    cgpa_12th: float = Field(..., ge=0.0, le=10.0)
    cgpa_degree: float = Field(..., ge=0.0, le=10.0)
    
    # Additional questions
    work_experience_description: str = Field(default="")  # Only for experienced candidates
    why_good_candidate: str = Field(default="")  # Always asked last
    
    # Optional fields
    responses: Dict[str, str] = Field(default_factory=dict)
    sentiment_scores: List[float] = Field(default_factory=list)
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.now)
    status: str = Field(default="in_progress")
    
    @validator('phone')
    def validate_phone(cls, v):
        """Validate phone number format"""
        # Remove all non-digit characters
        phone_digits = re.sub(r'\D', '', v)
        
        # Check if it's a valid length (10-15 digits)
        if len(phone_digits) < 10 or len(phone_digits) > 15:
            raise ValueError('Phone number must be between 10-15 digits')
        
        return phone_digits
    
    @validator('full_name')
    def validate_name(cls, v):
        """Validate full name format"""
        if not re.match(r'^[a-zA-Z\s\-\.\']+$', v):
            raise ValueError('Name can only contain letters, spaces, hyphens, dots, and apostrophes')
        return v.strip().title()
    
    @validator('tech_stack')
    def validate_tech_stack(cls, v):
        """Validate tech stack entries"""
        if not v:
            raise ValueError('At least one technology must be specified')
        
        # Clean and normalize tech stack entries
        cleaned_stack = []
        for tech in v:
            if isinstance(tech, str) and tech.strip():
                cleaned_stack.append(tech.strip().title())
        
        if not cleaned_stack:
            raise ValueError('Tech stack cannot be empty')
        
        return cleaned_stack
    
    @validator('desired_positions')
    def validate_positions(cls, v):
        """Validate desired positions"""
        if not v:
            raise ValueError('At least one desired position must be specified')
        
        # Clean and normalize positions
        cleaned_positions = []
        for position in v:
            if isinstance(position, str) and position.strip():
                cleaned_positions.append(position.strip().title())
        
        if not cleaned_positions:
            raise ValueError('Desired positions cannot be empty')
        
        return cleaned_positions
    
    @validator('date_of_birth')
    def validate_date_of_birth(cls, v):
        """Validate date of birth format"""
        # Accept DD/MM/YYYY or DD-MM-YYYY format
        if not re.match(r'^\d{1,2}[/-]\d{1,2}[/-]\d{4}$', v):
            raise ValueError('Date of birth must be in DD/MM/YYYY or DD-MM-YYYY format')
        
        # Parse and validate the date
        try:
            parts = re.split(r'[/-]', v)
            day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
            
            if day < 1 or day > 31:
                raise ValueError('Day must be between 1 and 31')
            if month < 1 or month > 12:
                raise ValueError('Month must be between 1 and 12')
            if year < 1950 or year > 2010:
                raise ValueError('Birth year must be between 1950 and 2010')
                
            # Return in consistent format
            return f"{day:02d}/{month:02d}/{year}"
        except (ValueError, IndexError):
            raise ValueError('Invalid date format. Use DD/MM/YYYY or DD-MM-YYYY')
    
    @validator('cgpa_10th', 'cgpa_12th', 'cgpa_degree')
    def validate_cgpa(cls, v):
        """Validate CGPA scores"""
        if v < 0.0 or v > 10.0:
            raise ValueError('CGPA must be between 0.0 and 10.0')
        return round(v, 2)

class TechnicalQuestion(BaseModel):
    """Model for technical questions"""
    
    question: str = Field(..., min_length=10)
    tech_area: str = Field(...)
    difficulty_level: str = Field(..., pattern=r'^(junior|mid|senior)$')
    expected_answer_points: List[str] = Field(default_factory=list)
    
class CandidateResponse(BaseModel):
    """Model for candidate responses to questions"""
    
    question_id: str = Field(...)
    question: str = Field(...)
    response: str = Field(...)
    sentiment_score: Optional[float] = Field(None, ge=-1.0, le=1.0)
    timestamp: datetime = Field(default_factory=datetime.now)
    
class ConversationSession(BaseModel):
    """Model for conversation session management"""
    
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    candidate_info: Optional[CandidateInfo] = None
    current_state: str = Field(default="greeting")
    chat_history: List[Dict[str, Any]] = Field(default_factory=list)
    technical_questions: List[TechnicalQuestion] = Field(default_factory=list)
    responses: List[CandidateResponse] = Field(default_factory=list)
    started_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    completed: bool = Field(default=False)
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        """Add a message to chat history"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        self.chat_history.append(message)
        self.updated_at = datetime.now()
    
    def update_state(self, new_state: str):
        """Update conversation state"""
        self.current_state = new_state
        self.updated_at = datetime.now()
    
    def add_technical_question(self, question: TechnicalQuestion):
        """Add a technical question"""
        self.technical_questions.append(question)
        self.updated_at = datetime.now()
    
    def add_response(self, response: CandidateResponse):
        """Add a candidate response"""
        self.responses.append(response)
        self.updated_at = datetime.now()

class SentimentAnalysis(BaseModel):
    """Model for sentiment analysis results"""
    
    text: str = Field(...)
    sentiment_score: float = Field(..., ge=-1.0, le=1.0)
    sentiment_label: str = Field(...)  # positive, negative, neutral
    confidence: float = Field(..., ge=0.0, le=1.0)
    analysis_timestamp: datetime = Field(default_factory=datetime.now)
    
    @validator('sentiment_label')
    def validate_sentiment_label(cls, v):
        """Validate sentiment label"""
        valid_labels = ['positive', 'negative', 'neutral']
        if v.lower() not in valid_labels:
            raise ValueError(f'Sentiment label must be one of: {valid_labels}')
        return v.lower()

class ValidationError(BaseModel):
    """Model for validation errors"""
    
    field: str = Field(...)
    message: str = Field(...)
    value: Any = Field(None)
    
class APIResponse(BaseModel):
    """Standard API response model"""
    
    success: bool = Field(...)
    message: str = Field(...)
    data: Optional[Any] = Field(None)
    errors: List[ValidationError] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)
