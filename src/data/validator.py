"""
Data Validation Module for TalentScout Hiring Assistant
"""

import re
from typing import List, Dict, Any, Tuple, Optional
from pydantic import ValidationError
from src.data.models import CandidateInfo, ValidationError as CustomValidationError

class DataValidator:
    """Handles data validation for candidate information"""
    
    def __init__(self):
        self.email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        self.phone_pattern = re.compile(r'^\+?[\d\s\-\(\)]{10,15}$')
        self.name_pattern = re.compile(r'^[a-zA-Z\s\-\.\']{2,100}$')
    
    def validate_email(self, email: str) -> Tuple[bool, Optional[str]]:
        """Validate email format"""
        if not email or not email.strip():
            return False, "Email is required"
        
        email = email.strip().lower()
        if not self.email_pattern.match(email):
            return False, "Please provide a valid email address (e.g., john@example.com)"
        
        return True, None
    
    def validate_phone(self, phone: str) -> Tuple[bool, Optional[str]]:
        """Validate phone number format"""
        if not phone or not phone.strip():
            return False, "Phone number is required"
        
        # Remove all non-digit characters for length check
        phone_digits = re.sub(r'\D', '', phone)
        
        if len(phone_digits) < 10:
            return False, "Phone number must have at least 10 digits"
        
        if len(phone_digits) > 15:
            return False, "Phone number cannot exceed 15 digits"
        
        return True, None
    
    def validate_name(self, name: str) -> Tuple[bool, Optional[str]]:
        """Validate full name format"""
        if not name or not name.strip():
            return False, "Full name is required"
        
        name = name.strip()
        if len(name) < 2:
            return False, "Name must be at least 2 characters long"
        
        if len(name) > 100:
            return False, "Name cannot exceed 100 characters"
        
        if not self.name_pattern.match(name):
            return False, "Name can only contain letters, spaces, hyphens, dots, and apostrophes"
        
        # Check for at least first and last name
        name_parts = name.split()
        if len(name_parts) < 2:
            return False, "Please provide both first and last name"
        
        return True, None
    
    def validate_experience(self, experience: str) -> Tuple[bool, Optional[str], Optional[int]]:
        """Validate years of experience"""
        if not experience or not experience.strip():
            return False, "Years of experience is required", None
        
        try:
            exp_years = int(experience.strip())
            if exp_years < 0:
                return False, "Experience cannot be negative", None
            if exp_years > 50:
                return False, "Experience cannot exceed 50 years", None
            return True, None, exp_years
        except ValueError:
            return False, "Please provide a valid number for years of experience", None
    
    def validate_positions(self, positions_text: str) -> Tuple[bool, Optional[str], Optional[List[str]]]:
        """Validate desired positions"""
        if not positions_text or not positions_text.strip():
            return False, "Desired position(s) is required", None
        
        # Split by common separators
        positions = re.split(r'[,;|\n]+', positions_text.strip())
        cleaned_positions = []
        
        for pos in positions:
            pos = pos.strip()
            if pos:
                if len(pos) < 2:
                    return False, f"Position '{pos}' is too short", None
                if len(pos) > 100:
                    return False, f"Position '{pos}' is too long", None
                cleaned_positions.append(pos.title())
        
        if not cleaned_positions:
            return False, "At least one position must be specified", None
        
        return True, None, cleaned_positions
    
    def validate_location(self, location: str) -> Tuple[bool, Optional[str]]:
        """Validate location"""
        if not location or not location.strip():
            return False, "Current location is required"
        
        location = location.strip()
        if len(location) < 2:
            return False, "Location must be at least 2 characters long"
        
        if len(location) > 100:
            return False, "Location cannot exceed 100 characters"
        
        return True, None
    
    def validate_tech_stack(self, tech_stack_text: str) -> Tuple[bool, Optional[str], Optional[List[str]]]:
        """Validate tech stack"""
        if not tech_stack_text or not tech_stack_text.strip():
            return False, "Tech stack/skills is required", None
        
        # Split by common separators
        technologies = re.split(r'[,;|\n]+', tech_stack_text.strip())
        cleaned_tech = []
        
        for tech in technologies:
            tech = tech.strip()
            if tech:
                if len(tech) < 2:
                    return False, f"Technology '{tech}' is too short", None
                if len(tech) > 50:
                    return False, f"Technology '{tech}' is too long", None
                cleaned_tech.append(tech.title())
        
        if not cleaned_tech:
            return False, "At least one technology must be specified", None
        
        return True, None, cleaned_tech
    
    def validate_candidate_info(self, data: Dict[str, Any]) -> Tuple[bool, List[CustomValidationError], Optional[CandidateInfo]]:
        """Validate complete candidate information"""
        errors = []
        
        try:
            # Create CandidateInfo instance which will trigger Pydantic validation
            candidate_info = CandidateInfo(**data)
            return True, [], candidate_info
        
        except ValidationError as e:
            for error in e.errors():
                field = '.'.join(str(x) for x in error['loc'])
                message = error['msg']
                value = error.get('input', None)
                
                errors.append(CustomValidationError(
                    field=field,
                    message=message,
                    value=value
                ))
            
            return False, errors, None
        
        except Exception as e:
            errors.append(CustomValidationError(
                field="general",
                message=f"Validation error: {str(e)}",
                value=None
            ))
            return False, errors, None
    
    def extract_info_from_text(self, text: str, field_type: str) -> Optional[str]:
        """Extract specific information from natural language text"""
        text = text.strip().lower()
        
        if field_type == "email":
            # Look for email patterns in text
            email_match = re.search(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b', text)
            return email_match.group(0) if email_match else None
        
        elif field_type == "phone":
            # Look for phone patterns in text
            phone_match = re.search(r'[\+]?[\d\s\-\(\)]{10,15}', text)
            return phone_match.group(0) if phone_match else None
        
        elif field_type == "experience":
            # Look for numbers followed by year-related words
            exp_match = re.search(r'(\d+)\s*(?:years?|yrs?)', text)
            return exp_match.group(1) if exp_match else None
        
        return None
    
    def get_experience_level(self, years: int) -> str:
        """Determine experience level based on years"""
        if years <= 2:
            return "junior"
        elif years <= 7:
            return "mid"
        else:
            return "senior"
