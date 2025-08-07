"""
Real Google Sheets Saving Test - Actually saves to sheets
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import real streamlit modules (not mock)
import streamlit as st
from src.chatbot.conversation_manager import ConversationManager
from src.config.settings import AppConfig, ConversationState
from src.data.models import CandidateInfo, ConversationSession
from datetime import datetime

# Mock streamlit session state for testing
class MockSessionState:
    def __init__(self):
        self.data = {}
    
    def __getitem__(self, key):
        return self.data.get(key)
    
    def __setitem__(self, key, value):
        self.data[key] = value
    
    def __contains__(self, key):
        return key in self.data
    
    def get(self, key, default=None):
        return self.data.get(key, default)

# Replace streamlit session state with mock
st.session_state = MockSessionState()

def test_real_sheets_saving():
    print("🎯 REAL GOOGLE SHEETS SAVING TEST")
    print("=" * 50)
    
    # Initialize with real config
    config = AppConfig()
    manager = ConversationManager(config)
    
    print(f"📊 Google Sheets Handler Available: {manager.sheets_handler is not None}")
    
    if not manager.sheets_handler:
        print("❌ Google Sheets handler not available!")
        return
    
    # Create a complete session manually
    session = ConversationSession()
    session.current_state = ConversationState.SUMMARY
    
    # Set up complete candidate info with all required fields
    session.candidate_info = CandidateInfo(
        full_name="Manual Test Candidate Priya Sharma",
        email="priya.test@email.com", 
        phone="9876543210",
        experience_years=4,
        desired_positions=["Data Analyst", "Business Intelligence Analyst"],
        location="Bangalore, Karnataka",
        tech_stack=["Python", "SQL", "Tableau", "PowerBI", "Excel"],
        gender="Female",
        date_of_birth="15/08/1995",
        graduation_year=2017,
        cgpa_10th=8.7,
        cgpa_12th=8.4,
        cgpa_degree=8.1
    )
    
    # Set up technical questions and responses
    session.technical_questions = {
        'current_question': 5,
        'total_questions': 5,
        'responses': [
            "INNER JOIN returns only matching records from both tables, while LEFT JOIN returns all records from the left table and matching records from the right table.",
            "I would first analyze the pattern of missing data using pandas.isnull(), then use appropriate imputation methods like mean for numerical data or mode for categorical data.",
            "Key practices include choosing appropriate chart types, using clear labels, maintaining consistent color schemes, and ensuring accessibility with colorblind-friendly palettes.",
            "I would use LAG function in SQL: SELECT year, value, (value - LAG(value) OVER (ORDER BY year)) / LAG(value) OVER (ORDER BY year) * 100 as yoy_growth FROM table_name.",
            "Primary key uniquely identifies each record in a table and cannot be null or duplicate. Foreign key references the primary key of another table to establish relationships."
        ],
        'questions': [
            "Explain the difference between INNER JOIN and LEFT JOIN in SQL.",
            "How would you handle missing values in a dataset?",
            "What are some data visualization best practices?", 
            "How would you calculate year-over-year growth in SQL?",
            "Explain the difference between primary key and foreign key."
        ]
    }
    
    # Add responses for sentiment analysis
    session.responses = []
    
    print("\n🔄 Attempting to save data to Google Sheets...")
    print("-" * 40)
    
    try:
        # Direct call to sheets handler save method
        success = manager.sheets_handler.save_candidate_data(session)
        
        if success:
            print("✅ SUCCESS: Data saved to Google Sheets!")
            print(f"\n📊 Data that was saved:")
            print(f"   • Name: {session.candidate_info.full_name}")
            print(f"   • Email: {session.candidate_info.email}")
            print(f"   • Experience: {session.candidate_info.experience_years} years")
            print(f"   • Position: {', '.join(session.candidate_info.desired_positions)}")
            print(f"   • Tech Stack: {', '.join(session.candidate_info.tech_stack)}")
            print(f"   • Technical Questions: {len(session.technical_questions['responses'])} answered")
            
            print(f"\n🔍 CHECK YOUR GOOGLE SHEET:")
            print(f"   URL: https://docs.google.com/spreadsheets/d/{config.google_sheet_id}")
            print(f"   Look for: 'Manual Test Candidate Priya Sharma' with timestamp {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            
        else:
            print("❌ FAILED: Data was not saved to Google Sheets!")
            
    except Exception as e:
        print(f"❌ ERROR: Exception occurred while saving: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_real_sheets_saving()
