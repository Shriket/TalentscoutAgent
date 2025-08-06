"""
Application Configuration Settings
"""

import os
from typing import Dict, Any
from pydantic import Field
from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    """Application configuration using Pydantic BaseSettings"""
    
    # Groq API Configuration
    groq_api_key: str = Field(..., env="GROQ_API_KEY")
    groq_model: str = "llama-3.1-8b-instant"
    groq_temperature: float = 0.7
    groq_max_tokens: int = 1000
    
    # Google Sheets Configuration
    google_sheet_id: str = Field(..., env="GOOGLE_SHEET_ID")
    google_service_account_json: str = Field(..., env="GOOGLE_SERVICE_ACCOUNT_JSON")
    
    # Application Settings
    app_env: str = Field("development", env="APP_ENV")
    debug_mode: bool = Field(True, env="DEBUG_MODE")
    session_timeout: int = Field(1800, env="SESSION_TIMEOUT")
    
    # Security
    secret_key: str = Field(..., env="SECRET_KEY")
    encryption_key: str = Field(..., env="ENCRYPTION_KEY")
    
    # Performance Settings
    max_response_time: float = 2.0
    max_concurrent_users: int = 10
    
    # UI Configuration
    app_title: str = "TalentScout Hiring Assistant"
    app_icon: str = "🤖"
    primary_color: str = "#1f77b4"
    background_color: str = "#ffffff"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Sheet configuration
SHEET_HEADERS = [
    "Timestamp", "Session_ID", "Full_Name", "Email", 
    "Phone", "Gender", "Date_of_Birth", "Experience_Years", 
    "Desired_Positions", "Location", "Graduation_Year", 
    "CGPA_10th", "CGPA_12th", "CGPA_Degree", "Tech_Stack", 
    "Work_Experience_Description", "Why_Good_Candidate", 
    "Technical_Questions", "Candidate_Responses", 
    "Sentiment_Score", "Questions_Answered"
]

# Supported tech stacks
TECH_STACKS = {
    "programming_languages": [
        "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", 
        "Go", "Rust", "PHP", "Ruby", "Swift", "Kotlin"
    ],
    "frameworks": [
        "React", "Angular", "Vue.js", "Django", "Flask", "FastAPI",
        "Spring Boot", "Express.js", "Next.js", "Laravel", "Rails"
    ],
    "databases": [
        "MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite",
        "Oracle", "SQL Server", "Cassandra", "DynamoDB"
    ],
    "cloud_platforms": [
        "AWS", "Google Cloud Platform", "Microsoft Azure", 
        "Digital Ocean", "Heroku", "Vercel"
    ],
    "devops_tools": [
        "Docker", "Kubernetes", "Jenkins", "GitLab CI", "GitHub Actions",
        "Terraform", "Ansible", "Prometheus", "Grafana"
    ]
}

# Conversation states
class ConversationState:
    GREETING = "greeting"
    INFO_COLLECTION = "info_collection"
    TECH_STACK = "tech_stack"
    TECHNICAL_QUESTIONS = "technical_questions"
    SENTIMENT_ANALYSIS = "sentiment_analysis"
    SUMMARY = "summary"
    ENDED = "ended"
