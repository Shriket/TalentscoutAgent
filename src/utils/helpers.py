"""
Helper utilities for TalentScout Hiring Assistant
"""

import re
import json
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import streamlit as st

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent injection attacks"""
    if not text:
        return ""
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', text)
    
    # Limit length
    sanitized = sanitized[:1000]
    
    return sanitized.strip()

def validate_email_format(email: str) -> bool:
    """Validate email format using regex"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone_format(phone: str) -> bool:
    """Validate phone number format"""
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    # Check if it's between 10-15 digits
    return 10 <= len(digits) <= 15

def format_phone_number(phone: str) -> str:
    """Format phone number for display"""
    digits = re.sub(r'\D', '', phone)
    
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return phone

def extract_tech_stack_from_text(text: str) -> List[str]:
    """Extract technology names from text"""
    # Common technology keywords
    tech_keywords = [
        # Programming Languages
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust',
        'php', 'ruby', 'swift', 'kotlin', 'scala', 'r', 'matlab',
        
        # Web Technologies
        'html', 'css', 'react', 'angular', 'vue', 'nodejs', 'express',
        'django', 'flask', 'fastapi', 'spring', 'laravel', 'rails',
        
        # Databases
        'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle',
        'sql server', 'cassandra', 'dynamodb', 'elasticsearch',
        
        # Cloud & DevOps
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins',
        'terraform', 'ansible', 'git', 'github', 'gitlab',
        
        # Data & ML
        'pandas', 'numpy', 'tensorflow', 'pytorch', 'scikit-learn',
        'spark', 'hadoop', 'kafka', 'airflow'
    ]
    
    text_lower = text.lower()
    found_tech = []
    
    for tech in tech_keywords:
        if tech in text_lower:
            found_tech.append(tech.title())
    
    # Remove duplicates and return
    return list(set(found_tech))

def calculate_experience_level(years: int) -> str:
    """Calculate experience level based on years"""
    if years <= 2:
        return "junior"
    elif years <= 7:
        return "mid"
    else:
        return "senior"

def generate_session_id() -> str:
    """Generate unique session ID"""
    timestamp = datetime.now().isoformat()
    random_data = f"{timestamp}_{hash(timestamp)}"
    return hashlib.md5(random_data.encode()).hexdigest()[:12]

def format_duration(start_time: datetime, end_time: Optional[datetime] = None) -> str:
    """Format duration between two timestamps"""
    if end_time is None:
        end_time = datetime.now()
    
    duration = end_time - start_time
    
    # Convert to total seconds
    total_seconds = int(duration.total_seconds())
    
    if total_seconds < 60:
        return f"{total_seconds} seconds"
    elif total_seconds < 3600:
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}m {seconds}s"
    else:
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours}h {minutes}m"

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    
    return text[:max_length-3] + "..."

def clean_text_for_storage(text: str) -> str:
    """Clean text for database storage"""
    if not text:
        return ""
    
    # Remove extra whitespace
    cleaned = re.sub(r'\s+', ' ', text.strip())
    
    # Remove special characters that might cause issues
    cleaned = re.sub(r'[^\w\s\-\.\,\!\?\:\;]', '', cleaned)
    
    return cleaned

def parse_list_from_text(text: str, separators: List[str] = None) -> List[str]:
    """Parse a list from comma/semicolon separated text"""
    if separators is None:
        separators = [',', ';', '|', '\n']
    
    # Create regex pattern for splitting
    pattern = '|'.join(re.escape(sep) for sep in separators)
    
    # Split and clean
    items = re.split(pattern, text)
    cleaned_items = []
    
    for item in items:
        item = item.strip()
        if item:
            cleaned_items.append(item)
    
    return cleaned_items

def is_valid_name(name: str) -> bool:
    """Validate if name contains valid characters"""
    if not name or len(name.strip()) < 2:
        return False
    
    # Allow letters, spaces, hyphens, dots, apostrophes
    pattern = r'^[a-zA-Z\s\-\.\']+$'
    return bool(re.match(pattern, name.strip()))

def normalize_tech_name(tech: str) -> str:
    """Normalize technology name for consistency"""
    tech_mapping = {
        'js': 'JavaScript',
        'ts': 'TypeScript',
        'py': 'Python',
        'node': 'Node.js',
        'react.js': 'React',
        'vue.js': 'Vue.js',
        'angular.js': 'Angular',
        'postgresql': 'PostgreSQL',
        'mysql': 'MySQL',
        'mongodb': 'MongoDB',
        'aws': 'AWS',
        'gcp': 'Google Cloud Platform',
        'azure': 'Microsoft Azure'
    }
    
    tech_lower = tech.lower().strip()
    return tech_mapping.get(tech_lower, tech.title())

def calculate_sentiment_trend(scores: List[float]) -> str:
    """Calculate sentiment trend from list of scores"""
    if len(scores) < 2:
        return "stable"
    
    # Compare first half with second half
    mid_point = len(scores) // 2
    first_half = scores[:mid_point] if mid_point > 0 else [scores[0]]
    second_half = scores[mid_point:]
    
    first_avg = sum(first_half) / len(first_half)
    second_avg = sum(second_half) / len(second_half)
    
    difference = second_avg - first_avg
    
    if difference > 0.2:
        return "improving"
    elif difference < -0.2:
        return "declining"
    else:
        return "stable"

def get_time_greeting() -> str:
    """Get appropriate greeting based on time of day"""
    current_hour = datetime.now().hour
    
    if 5 <= current_hour < 12:
        return "Good morning"
    elif 12 <= current_hour < 17:
        return "Good afternoon"
    elif 17 <= current_hour < 22:
        return "Good evening"
    else:
        return "Hello"

def mask_sensitive_data(text: str, data_type: str) -> str:
    """Mask sensitive data for logging"""
    if data_type == "email":
        if '@' in text:
            parts = text.split('@')
            if len(parts) == 2:
                username = parts[0]
                domain = parts[1]
                masked_username = username[:2] + '*' * (len(username) - 2)
                return f"{masked_username}@{domain}"
    
    elif data_type == "phone":
        digits = re.sub(r'\D', '', text)
        if len(digits) >= 10:
            return digits[:3] + '*' * (len(digits) - 6) + digits[-3:]
    
    elif data_type == "name":
        words = text.split()
        if len(words) >= 2:
            return f"{words[0]} {words[1][0]}***"
    
    return text

def validate_session_timeout(start_time: datetime, timeout_minutes: int = 30) -> bool:
    """Check if session has timed out"""
    if not start_time:
        return False
    
    elapsed = datetime.now() - start_time
    return elapsed.total_seconds() > (timeout_minutes * 60)

def create_backup_data(session_data: Dict[str, Any]) -> str:
    """Create backup of session data"""
    backup = {
        'timestamp': datetime.now().isoformat(),
        'session_data': session_data,
        'version': '1.0'
    }
    
    return json.dumps(backup, indent=2, default=str)

def restore_from_backup(backup_string: str) -> Optional[Dict[str, Any]]:
    """Restore session data from backup"""
    try:
        backup = json.loads(backup_string)
        return backup.get('session_data')
    except (json.JSONDecodeError, KeyError):
        return None

def log_interaction(interaction_type: str, data: Dict[str, Any]):
    """Log interaction for analytics (privacy-safe)"""
    # Only log non-sensitive analytics data
    safe_data = {
        'type': interaction_type,
        'timestamp': datetime.now().isoformat(),
        'session_id': data.get('session_id', 'unknown')[:8],  # Truncated
        'stage': data.get('current_stage', 'unknown'),
        'success': data.get('success', True)
    }
    
    # Store in session state for potential export
    if 'interaction_log' not in st.session_state:
        st.session_state.interaction_log = []
    
    st.session_state.interaction_log.append(safe_data)

def get_performance_metrics() -> Dict[str, Any]:
    """Get performance metrics for monitoring"""
    if 'interaction_log' not in st.session_state:
        return {}
    
    log = st.session_state.interaction_log
    
    if not log:
        return {}
    
    # Calculate metrics
    total_interactions = len(log)
    successful_interactions = len([i for i in log if i.get('success', True)])
    success_rate = (successful_interactions / total_interactions) * 100 if total_interactions > 0 else 0
    
    # Get stage distribution
    stages = [i.get('stage', 'unknown') for i in log]
    stage_counts = {stage: stages.count(stage) for stage in set(stages)}
    
    return {
        'total_interactions': total_interactions,
        'success_rate': round(success_rate, 2),
        'stage_distribution': stage_counts,
        'session_duration': format_duration(
            datetime.fromisoformat(log[0]['timestamp']),
            datetime.fromisoformat(log[-1]['timestamp'])
        ) if len(log) > 1 else "0 seconds"
    }
