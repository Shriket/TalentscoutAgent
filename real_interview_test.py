"""
Real Interview Flow Test - Actually saves to Google Sheets
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Mock streamlit but allow Google Sheets saving
class MockStreamlit:
    class SessionState:
        def __init__(self):
            from src.data.models import ConversationSession
            self.conversation_session = ConversationSession()
            self._data = {'conversation_session': self.conversation_session}
        
        def __contains__(self, key):
            return key in self._data
        
        def __getitem__(self, key):
            return self._data[key]
        
        def __setitem__(self, key, value):
            self._data[key] = value
            
        def get(self, key, default=None):
            return self._data.get(key, default)
    
    def __init__(self):
        self.session_state = self.SessionState()
    
    def error(self, message): 
        print(f"❌ STREAMLIT ERROR: {message}")
    def warning(self, message): 
        print(f"⚠️ STREAMLIT WARNING: {message}")
    def success(self, message): 
        print(f"✅ STREAMLIT SUCCESS: {message}")
    def info(self, message): 
        print(f"ℹ️ STREAMLIT INFO: {message}")

sys.modules['streamlit'] = MockStreamlit()

from src.chatbot.conversation_manager import ConversationManager
from src.config.settings import AppConfig, ConversationState

def simulate_complete_interview():
    print("🎯 REAL INTERVIEW SIMULATION - WILL SAVE TO GOOGLE SHEETS")
    print("=" * 60)
    
    # Initialize
    config = AppConfig()
    manager = ConversationManager(config)
    
    print(f"📊 Google Sheets Available: {manager.sheets_handler is not None}")
    
    # Simulate complete interview flow
    responses = [
        "yes",  # Ready to start
        "Priya Sharma",  # Full name
        "priya.sharma@email.com",  # Email
        "9876543210",  # Phone
        "3",  # Experience years
        "Data Analyst",  # Desired position
        "Delhi, India",  # Location
        "Female",  # Gender
        "25/12/1995",  # Date of birth
        "2018",  # Graduation year
        "8.5",  # 10th CGPA
        "8.2",  # 12th CGPA
        "7.8",  # Degree CGPA
        "I worked as a Junior Data Analyst at Infosys for 2 years where I created dashboards using PowerBI and analyzed customer data using SQL queries.",  # Work experience
        "Python, SQL, PowerBI, Excel",  # Tech stack
        "INNER JOIN returns only matching records from both tables, while LEFT JOIN returns all records from the left table and matching records from the right table.",  # Tech Q1
        "I would first analyze the pattern of missing data, then use appropriate techniques like mean imputation for numerical data or mode imputation for categorical data.",  # Tech Q2
        "Key practices include choosing appropriate chart types, using clear labels, avoiding 3D effects, and ensuring color accessibility.",  # Tech Q3
        "I would use LAG function in SQL to compare current year values with previous year values and calculate the percentage growth.",  # Tech Q4
        "Primary key uniquely identifies each record in a table and cannot be null, while foreign key establishes relationships between tables.",  # Tech Q5
        "I have strong analytical skills, 3 years of hands-on experience with data analysis tools, and a proven track record of delivering insights that drive business decisions."  # Why good candidate
    ]
    
    print("🤖 Starting interview simulation...")
    print("-" * 40)
    
    response_index = 0
    conversation_count = 0
    max_conversations = 25  # Prevent infinite loop
    
    # Start conversation
    bot_response = manager.process_input("")
    
    while response_index < len(responses) and conversation_count < max_conversations:
        conversation_count += 1
        
        print(f"Q{conversation_count} bot: {bot_response}")
        
        if response_index < len(responses):
            user_input = responses[response_index]
            print(f"A{conversation_count} user: {user_input}")
            response_index += 1
            
            # Process user input
            bot_response = manager.process_input(user_input)
            
            # Check if interview completed
            session = manager.get_session()
            if session.current_state == ConversationState.COMPLETED:
                print(f"\n🎉 INTERVIEW COMPLETED!")
                print(f"✅ Final bot response: {bot_response}")
                break
                
        else:
            break
    
    # Final status
    session = manager.get_session()
    print(f"\n📊 FINAL STATUS:")
    print(f"   • Current State: {session.current_state}")
    print(f"   • Candidate Info Available: {session.candidate_info is not None}")
    print(f"   • Technical Questions: {len(session.technical_questions.get('responses', []))}")
    
    if session.candidate_info:
        print(f"   • Name: {session.candidate_info.full_name}")
        print(f"   • Email: {session.candidate_info.email}")
        print(f"   • Experience: {session.candidate_info.experience_years} years")
    
    print(f"\n🔍 CHECK GOOGLE SHEETS:")
    print(f"   URL: https://docs.google.com/spreadsheets/d/{config.google_sheet_id}")
    print(f"   Look for: 'Priya Sharma' entry with current timestamp")

if __name__ == "__main__":
    simulate_complete_interview()
