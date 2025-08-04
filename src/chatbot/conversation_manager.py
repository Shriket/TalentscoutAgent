"""
Conversation Manager for TalentScout Hiring Assistant
"""

import streamlit as st
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import uuid

from src.data.models import ConversationSession, CandidateInfo, TechnicalQuestion, CandidateResponse
from src.data.validator import DataValidator
from src.data.sheets_handler import SheetsHandler
from src.chatbot.llm_handler import LLMHandler
from src.chatbot.sentiment_analyzer import SentimentAnalyzer
from src.config.prompts import QUESTION_TEMPLATES
from src.config.settings import ConversationState, AppConfig

# Ensure ConversationState is available globally in this module
# This prevents UnboundLocalError in long methods
from src.config.settings import ConversationState as CS

class ConversationManager:
    """Manages the entire conversation flow and state"""
    
    def __init__(self, config: AppConfig):
        self.config = config
        self.llm_handler = LLMHandler(config)
        self.sentiment_analyzer = SentimentAnalyzer()
        self.data_validator = DataValidator()
        
        # Initialize sheets handler if credentials are available
        self.sheets_handler = None
        try:
            # Only initialize if we have valid credentials
            if (hasattr(config, 'google_sheet_id') and 
                hasattr(config, 'google_service_account_json') and
                config.google_sheet_id and 
                config.google_service_account_json):
                
                print(f"🔍 Attempting Google Sheets initialization...")
                print(f"Sheet ID: {config.google_sheet_id}")
                print(f"Service Account JSON type: {type(config.google_service_account_json)}")
                
                # Parse JSON string if needed
                service_account_data = config.google_service_account_json
                if isinstance(service_account_data, str):
                    import json
                    service_account_data = json.loads(service_account_data)
                
                print(f"Parsed JSON type: {type(service_account_data)}")
                print(f"Has client_email: {'client_email' in service_account_data}")
                print(f"Has token_uri: {'token_uri' in service_account_data}")
                
                self.sheets_handler = SheetsHandler(
                    sheet_id=config.google_sheet_id,
                    service_account_json=service_account_data
                )
                print("✅ Google Sheets integration enabled successfully!")
            else:
                print("⚠️ Google Sheets integration disabled - missing credentials")
        except Exception as e:
            print(f"❌ Google Sheets integration failed: {str(e)}")
            import traceback
            traceback.print_exc()
        
        # Initialize session if not exists
        if 'conversation_session' not in st.session_state:
            st.session_state.conversation_session = ConversationSession()
    
    def get_session(self) -> ConversationSession:
        """Get current conversation session"""
        return st.session_state.conversation_session
    
    def process_user_input(self, user_input: str) -> str:
        """Process user input and generate appropriate response"""
        session = self.get_session()
        
        # Add user message to history
        session.add_message("user", user_input)
        
        # Check if user wants to end conversation
        if self.llm_handler.check_conversation_end_intent(user_input):
            return self._handle_conversation_end()
        
        # Process based on current state
        response = ""
        current_state = session.current_state
        
        if current_state == ConversationState.GREETING:
            response = self._handle_greeting(user_input)
        elif current_state == ConversationState.INFO_COLLECTION:
            response = self._handle_info_collection(user_input)
        elif current_state == ConversationState.TECH_STACK:
            response = self._handle_tech_stack(user_input)
        elif current_state == ConversationState.TECHNICAL_QUESTIONS:
            response = self._handle_technical_questions(user_input)
        elif current_state == ConversationState.SUMMARY:
            response = self._handle_summary(user_input)
        else:
            response = self._handle_fallback(user_input)
        
        # Add assistant response to history
        session.add_message("assistant", response)
        
        # Analyze sentiment of user input
        self._analyze_user_sentiment(user_input)
        
        return response
    
    def _handle_greeting(self, user_input: str) -> str:
        """Handle greeting phase with intelligent question understanding"""
        session = self.get_session()
        
        # Check if this is the first interaction
        if len(session.chat_history) <= 2:  # Only user input and this response
            # Return exact greeting message as specified in prompts
            return "Nice to meet you! The entire process takes about 5-10 minutes. Are you ready to get started?"
        
        user_lower = user_input.lower().strip()
        
        # Handle specific questions about the bot/company
        if any(word in user_lower for word in ['name', 'who are you', 'what are you', 'introduce']):
            return "I'm TalentScout Assistant! 🤖 I'm an AI hiring assistant designed to help you through our application process. I'll collect your information, assess your technical skills, and ask relevant questions based on your expertise.\n\nAre you ready to start the application process?"
        
        elif any(word in user_lower for word in ['what do you do', 'what is this', 'purpose', 'help']):
            return "I help candidates like you apply for positions at TalentScout! 🎯\n\nHere's what I do:\n• Collect your basic information\n• Understand your technical skills\n• Ask relevant questions based on your expertise\n• Provide feedback and next steps\n\nWould you like to begin the application process?"
        
        elif any(word in user_lower for word in ['company', 'talentscout', 'about company']):
            return "TalentScout is a hiring platform that connects talented professionals with great opportunities! 🌟\n\nI'm here to help you through our streamlined application process. Ready to get started?"
        
        elif any(word in user_lower for word in ['time', 'how long', 'duration']):
            return "The entire process takes about 5-10 minutes! ⏰\n\nIt's quick and straightforward - just some basic info and a few technical questions. Are you ready to begin?"
        
        # Check if user is ready to proceed
        positive_indicators = ["yes", "y", "sure", "okay", "ok", "ready", "proceed", "start", "let's go", "begin", "go", "continue", "yeah", "yep", "yup", "haan", "ha"]
        negative_indicators = ["no", "n", "not ready", "later", "wait", "nahi", "nah"]
        
        if any(indicator in user_lower for indicator in positive_indicators):
            session.update_state(ConversationState.INFO_COLLECTION)
            response = "🎉 Excellent! Let's begin with some basic information.\n\n📝 **Step 1: Personal Information**\n\nCould you please tell me your **full name**?"
            return response
        elif any(indicator in user_lower for indicator in negative_indicators):
            response = "No problem! Take your time. When you're ready to start the application process, just let me know by saying 'yes' or 'ready'."
            return response
        else:
            # Handle other inputs during greeting
            response = "I understand you might have questions! I'm here to help you apply for positions at TalentScout.\n\nWould you like to **start the application process** now? Just say 'yes' when you're ready!"
            return response
    
    def _handle_info_collection(self, user_input: str) -> str:
        """Handle information collection phase with intelligent question handling"""
        session = self.get_session()
        user_lower = user_input.lower().strip()
        
        # Handle general questions even during info collection
        if any(word in user_lower for word in ['name', 'who are you', 'what are you', 'introduce']):
            return "I'm TalentScout Assistant! 🤖 I'm an AI hiring assistant designed to help you through our application process.\n\nLet's continue with collecting your information. Could you please tell me your **full name**?"
        
        elif any(word in user_lower for word in ['what do you do', 'what is this', 'purpose', 'help']):
            return "I help candidates like you apply for positions at TalentScout! 🎯\n\nRight now I'm collecting your basic information to get started. Could you please provide your **full name**?"
        
        elif any(word in user_lower for word in ['company', 'talentscout', 'about company']):
            return "TalentScout is a hiring platform that connects talented professionals with great opportunities! 🌟\n\nLet's continue with your application. Please tell me your **full name**."
        
        elif any(word in user_lower for word in ['time', 'how long', 'duration']):
            return "The entire process takes about 5-10 minutes! ⏰ We're just getting started.\n\nCould you please tell me your **full name** to continue?"
        
        # Initialize candidate info if not exists
        if not hasattr(session, 'candidate_info') or not session.candidate_info:
            session.candidate_info = {
                'full_name': '',
                'email': '',
                'phone': '',
                'experience_years': None,
                'desired_positions': [],
                'location': '',
                'gender': '',
                'date_of_birth': '',
                'graduation_year': None,
                'cgpa_10th': None,
                'cgpa_12th': None,
                'cgpa_degree': None,
                'work_experience_description': '',
                'why_good_candidate': '',
                'current_field': 'full_name'
            }
        
        candidate_info = session.candidate_info
        current_field = candidate_info.get('current_field', 'full_name')
        
        # Process based on current field being collected
        if current_field == 'full_name':
            name_parts = user_input.strip().split()
            if len(name_parts) >= 2 and all(part.isalpha() for part in name_parts):
                candidate_info['full_name'] = user_input.strip()
                candidate_info['current_field'] = 'email'
                return f"Nice to meet you, {user_input.strip()}! 📧\n\nNow, could you please provide your **email address**?"
            elif len(name_parts) == 1:
                return "Please provide your **full name** (both first and last name). For example: 'John Smith' or 'Priya Sharma'."
            else:
                return "Please provide a valid **full name** using only letters. For example: 'John Smith' or 'Priya Sharma'."
                
        elif current_field == 'email':
            email = user_input.strip()
            # Proper email validation
            if (' ' in email or '\t' in email or 
                not '@' in email or not '.' in email or 
                email.count('@') != 1 or 
                len(email.split('@')[0]) < 2 or 
                len(email.split('@')[1].split('.')[0]) < 2 or 
                len(email.split('.')[-1]) < 2 or 
                email.startswith('@') or email.endswith('@') or 
                email.startswith('.') or email.endswith('.') or 
                '..' in email or '@@' in email):
                return "That doesn't look like a valid email address. Please provide a valid **email address** (e.g., john@example.com). No spaces allowed."
            else:
                candidate_info['email'] = email
                candidate_info['current_field'] = 'phone'
                return "Great! 📱\n\nNext, please provide your **phone number**:"
                
        elif current_field == 'phone':
            # Intelligent phone validation
            phone_digits = ''.join(filter(str.isdigit, user_input))
            if len(phone_digits) < 10:
                return "Please provide a valid **phone number** with at least 10 digits:"
            elif len(phone_digits) > 15:
                return "That phone number seems too long. Please provide a valid **phone number**:"
            elif phone_digits == '0' * len(phone_digits):  # All zeros
                return "That doesn't look like a real phone number. Please provide your actual **phone number**:"
            elif phone_digits == '1' * len(phone_digits):  # All ones
                return "That doesn't look like a real phone number. Please provide your actual **phone number**:"
            elif len(set(phone_digits)) == 1:  # All same digits
                return "That doesn't look like a real phone number. Please provide your actual **phone number**:"
            elif phone_digits.startswith('0000') or phone_digits.startswith('1111'):
                return "That doesn't look like a real phone number. Please provide your actual **phone number**:"
            else:
                candidate_info['phone'] = phone_digits
                candidate_info['current_field'] = 'experience_years'
                return "Perfect! 💼\n\nHow many **years of professional experience** do you have? (Please enter a number):"
                
        elif current_field == 'experience_years':
            try:
                years = int(''.join(filter(str.isdigit, user_input)))
                if 0 <= years <= 50:
                    candidate_info['experience_years'] = years
                    candidate_info['current_field'] = 'desired_positions'
                    return f"Excellent! {years} years of experience. 🎯\n\nWhat **position(s)** are you interested in? (e.g., Software Developer, Data Scientist, etc.):"
                else:
                    return "Please enter a realistic number of years (0-50):"
            except:
                return "Please enter the number of years as a **number** (e.g., 5, 10, etc.):"
                
        elif current_field == 'desired_positions':
            if user_input.strip() and len(user_input.strip()) > 2:
                # Check if it's a meaningful position (not just abbreviations like 'ds')
                if len(user_input.strip()) < 3:
                    return "Please provide the **full position name**. For example: 'Data Scientist', 'Software Developer', 'Product Manager', etc."
                positions = [pos.strip() for pos in user_input.split(',') if pos.strip()]
                candidate_info['desired_positions'] = positions
                candidate_info['current_field'] = 'location'
                return f"Great! Interested in: {', '.join(positions)} 🌍\n\nWhat's your current **location** (city, country)? Please provide both city and country."
            else:
                return "Please tell me what **positions** you're interested in. For example: 'Data Scientist', 'Software Developer', 'Product Manager', etc."
                
        elif current_field == 'location':
            location_parts = user_input.strip().split()
            if len(location_parts) >= 2 and len(user_input.strip()) > 5:
                candidate_info['location'] = user_input.strip()
                candidate_info['current_field'] = 'gender'
                return f"Great! Location: {user_input.strip()} 👤\n\nNext, please select your **gender**:\n\n• Male\n• Female\n• Transgender\n\nPlease type one of the above options:"
            elif len(location_parts) == 1:
                return "Please provide both **city and country** for your location. For example: 'Mumbai, India' or 'New York, USA'."
            else:
                return "Please provide a valid **location** with city and country. For example: 'Mumbai, India' or 'London, UK'."
                
        elif current_field == 'gender':
            gender = user_input.strip().title()
            if gender in ['Male', 'Female', 'Transgender']:
                candidate_info['gender'] = gender
                candidate_info['current_field'] = 'date_of_birth'
                return f"Thank you! 📅\n\nPlease provide your **date of birth** in DD/MM/YYYY format:\n\n*Example: 15/08/1995*"
            else:
                return "Please select one of the following options:\n\n• Male\n• Female\n• Transgender\n\nPlease type exactly as shown above:"
                
        elif current_field == 'date_of_birth':
            import re
            if re.match(r'^\d{1,2}[/-]\d{1,2}[/-]\d{4}$', user_input.strip()):
                try:
                    parts = re.split(r'[/-]', user_input.strip())
                    day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
                    
                    if day < 1 or day > 31 or month < 1 or month > 12 or year < 1950 or year > 2010:
                        return "Please provide a valid date. Day (1-31), Month (1-12), Year (1950-2010):\n\n*Example: 15/08/1995*"
                    
                    candidate_info['date_of_birth'] = f"{day:02d}/{month:02d}/{year}"
                    candidate_info['current_field'] = 'graduation_year'
                    return f"Perfect! 🎓\n\nWhat year did you **graduate** from your degree program?\n\n*Example: 2020*"
                except:
                    return "Please provide your date of birth in DD/MM/YYYY format:\n\n*Example: 15/08/1995*"
            else:
                return "Please provide your date of birth in DD/MM/YYYY format:\n\n*Example: 15/08/1995*"
                
        elif current_field == 'graduation_year':
            try:
                year = int(user_input.strip())
                if 1990 <= year <= 2030:
                    candidate_info['graduation_year'] = year
                    candidate_info['current_field'] = 'cgpa_10th'
                    return f"Great! Graduated in {year} 📊\n\nPlease provide your **10th standard CGPA/Percentage** (0.0 to 10.0):\n\n*Example: 8.5*"
                else:
                    return "Please enter a valid graduation year (1990-2030):\n\n*Example: 2020*"
            except:
                return "Please enter the graduation year as a number:\n\n*Example: 2020*"
                
        elif current_field == 'cgpa_10th':
            try:
                cgpa = float(user_input.strip())
                if 0.0 <= cgpa <= 10.0:
                    candidate_info['cgpa_10th'] = round(cgpa, 2)
                    candidate_info['current_field'] = 'cgpa_12th'
                    return f"Excellent! 📊\n\nNow, please provide your **12th standard CGPA/Percentage** (0.0 to 10.0):\n\n*Example: 8.7*"
                else:
                    return "Please enter a CGPA between 0.0 and 10.0:\n\n*Example: 8.5*"
            except:
                return "Please enter your 10th CGPA as a number:\n\n*Example: 8.5*"
                
        elif current_field == 'cgpa_12th':
            try:
                cgpa = float(user_input.strip())
                if 0.0 <= cgpa <= 10.0:
                    candidate_info['cgpa_12th'] = round(cgpa, 2)
                    candidate_info['current_field'] = 'cgpa_degree'
                    return f"Great! 📊\n\nFinally, please provide your **degree CGPA** (0.0 to 10.0):\n\n*Example: 8.9*"
                else:
                    return "Please enter a CGPA between 0.0 and 10.0:\n\n*Example: 8.7*"
            except:
                return "Please enter your 12th CGPA as a number:\n\n*Example: 8.7*"
                
        elif current_field == 'cgpa_degree':
            try:
                cgpa = float(user_input.strip())
                if 0.0 <= cgpa <= 10.0:
                    candidate_info['cgpa_degree'] = round(cgpa, 2)
                    
                    # Check if candidate has experience to ask work experience question
                    if candidate_info.get('experience_years', 0) > 0:
                        candidate_info['current_field'] = 'work_experience_description'
                        return f"Excellent! 💼\n\nSince you have {candidate_info['experience_years']} years of experience, please **describe your work experience** in detail:\n\n• What was your **Position Title**?\n• What was the **Organization Name**?\n• How long did you work there?\n• What were your main responsibilities?\n\nPlease provide a detailed description:"
                    else:
                        # Skip work experience for freshers, go to final question
                        candidate_info['current_field'] = 'why_good_candidate'
                        return f"Perfect! 🎆\n\nFinally, please **describe why you are a good candidate** for this position:\n\n• What makes you unique?\n• What skills and qualities do you bring?\n• Why should we consider you?\n\nPlease provide a detailed response:"
                else:
                    return "Please enter a CGPA between 0.0 and 10.0:\n\n*Example: 8.9*"
            except:
                return "Please enter your degree CGPA as a number:\n\n*Example: 8.9*"
                
        elif current_field == 'work_experience_description':
            user_response = user_input.strip().lower()
            
            # Check for meaningful work experience content
            work_indicators = ['worked', 'work', 'job', 'position', 'role', 'company', 'organization', 'responsibilities', 'experience', 'analyst', 'developer', 'engineer', 'manager', 'years', 'months']
            has_work_content = any(indicator in user_response for indicator in work_indicators)
            
            # Check if it's just repeating the question or giving irrelevant answer
            invalid_responses = ['data analyst, business analyst', 'data analyst', 'business analyst', '5', 'yes', 'no']
            is_invalid = user_response in invalid_responses or len(user_input.strip()) < 15
            
            if has_work_content and not is_invalid and len(user_input.strip()) > 20:
                candidate_info['work_experience_description'] = user_input.strip()
                candidate_info['current_field'] = 'why_good_candidate'
                return f"Thank you for sharing your experience! 🎆\n\nFinally, please **describe why you are a good candidate** for this position:\n\n• What makes you unique?\n• What skills and qualities do you bring?\n• Why should we consider you?\n\nPlease provide a detailed response:"
            else:
                return "Please provide a detailed description of your work experience (at least a few sentences):\n\n• Position Title\n• Organization Name\n• Duration\n• Main responsibilities"
                
        elif current_field == 'why_good_candidate':
            user_response = user_input.strip().lower()
            
            # Check for meaningful candidate qualities content
            candidate_indicators = ['skills', 'experience', 'good', 'strong', 'qualified', 'ability', 'knowledge', 'expertise', 'passion', 'dedicated', 'motivated', 'team', 'leadership', 'problem', 'solve', 'analytical', 'technical']
            has_candidate_content = any(indicator in user_response for indicator in candidate_indicators)
            
            # Check if it's just repeating positions or giving irrelevant answer
            invalid_responses = ['data analyst, business analyst', 'data analyst', 'business analyst', '5', 'yes', 'no']
            is_invalid = user_response in invalid_responses or len(user_input.strip()) < 15
            
            if has_candidate_content and not is_invalid and len(user_input.strip()) > 20:
                candidate_info['why_good_candidate'] = user_input.strip()
                # Update session with the candidate info
                session.candidate_info = candidate_info
                # All info collected, move to tech stack
                session.update_state(CS.TECH_STACK)
                
                # Simple, clean confirmation
                return f"""🎉 Perfect!

Now, let's talk about your technical expertise! Please tell me about your **tech stack** - what programming languages, frameworks, databases, and tools do you work with?

*Example: Python, JavaScript, React, Node.js, PostgreSQL, Docker*"""
            else:
                return "Please provide a detailed response about why you are a good candidate (at least a few sentences):\n\n• What makes you unique?\n• What skills do you bring?\n• Why should we consider you?"
                

    
        import re  # at top already? ensure near other imports; but easier: no replacement
        session = self.get_session()
        
        if user_input.strip():
            # Simple tech stack extraction with stopwords removal
            stop_words = {"i", "im", "i'm", "am", "good", "in", "and", "with", "the", "a", "an", "of"}
            tech_stack = [tok.strip().lower() for tok in user_input.replace('/', ' ').replace(',', ' ').split() if tok and tok not in stop_words]
            
            # --- Role-specific question selection will be handled later using QUESTION_TEMPLATES ---
            role_map = {
                'software developer': ['python', 'javascript', 'java'],
                'data scientist': ['python', 'r', 'sql'],
                'data engineer': ['python', 'java', 'scala']
            }
            desired_positions = session.candidate_info.get('desired_positions', [])
            role = desired_positions[0].lower() if desired_positions else 'software developer'
            mapped_tech_stack = role_map.get(role, ['python', 'javascript', 'java'])
            
            # Choose questions accordingly
            questions = []
            for tech in mapped_tech_stack[:3]:  # Max 3 questions
                if tech in tech_stack:
                    questions.append(self._generate_simple_questions([tech], 'mid')[0])
                session.technical_questions = {
                    'current_question': 1,
                    'total_questions': 3,
                    'responses': [],
                    'questions': []
                }
                
                # Generate simple technical questions based on experience level
                experience_years = session.candidate_info.get('experience_years', 0) if session.candidate_info else 0
                
                if experience_years <= 2:
                    level = "junior"
                elif experience_years <= 5:
                    level = "mid"
                else:
                    level = "senior"
                
                # Generate questions
                questions = []
                for tech in tech_stack[:3]:  # Max 3 questions
                    tech_lower = tech.lower()
                    if tech_lower == 'python':
                        if level == 'junior':
                            questions.append("What is the difference between a list and a tuple in Python?")
                        elif level == 'mid':
                            questions.append("Explain how Python's garbage collection works.")
                        else:
                            questions.append("How would you optimize a Python application for better performance?")
                    elif tech_lower == 'javascript':
                        if level == 'junior':
                            questions.append("What is the difference between let, const, and var in JavaScript?")
                        elif level == 'mid':
                            questions.append("Explain how closures work in JavaScript with an example.")
                        else:
                            questions.append("How would you handle memory leaks in a JavaScript application?")
                    elif tech_lower == 'react':
                        if level == 'junior':
                            questions.append("What is the difference between functional and class components in React?")
                        elif level == 'mid':
                            questions.append("Explain the React component lifecycle methods.")
                        else:
                            questions.append("How would you optimize a React application for better performance?")
                    elif tech_lower == 'sql':
                        if level == 'junior':
                            questions.append("What is the difference between INNER JOIN and LEFT JOIN in SQL?")
                        elif level == 'mid':
                            questions.append("How would you optimize a slow SQL query?")
                        else:
                            questions.append("How would you design a database schema for a large-scale application?")
                    else:
                        # Generic questions with variety
                        if level == 'junior':
                            generic_junior = [
                                f"What are the basic concepts you should know when working with {tech}?",
                                f"Can you explain what {tech} is used for and why it's important?",
                                f"What challenges have you faced while learning {tech}?"
                            ]
                            questions.append(generic_junior[len(questions) % len(generic_junior)])
                        elif level == 'mid':
                            generic_mid = [
                                f"Describe a challenging project you've worked on using {tech}.",
                                f"What are some best practices you follow when working with {tech}?",
                                f"How do you troubleshoot issues when working with {tech}?"
                            ]
                            questions.append(generic_mid[len(questions) % len(generic_mid)])
                        else:
                            generic_senior = [
                                f"How would you architect a scalable system using {tech}?",
                                f"What are the performance considerations when using {tech} in production?",
                                f"How would you mentor a junior developer learning {tech}?"
                            ]
                            questions.append(generic_senior[len(questions) % len(generic_senior)])
                
                # Ensure we have at least 3 questions with variety
                fallback_questions = [
                    "Describe your approach to debugging code when you encounter an error.",
                    "How do you ensure code quality and maintainability in your projects?",
                    "How do you stay updated with the latest technologies and best practices?",
                    "Tell me about a challenging project you've worked on and how you solved it.",
                    "What's your experience with version control systems like Git?",
                    "How do you handle tight deadlines and pressure in development projects?",
                    "What's your preferred development environment and why?",
                    "How do you approach learning a new technology or framework?"
                ]
                
                for fallback in fallback_questions:
                    if len(questions) >= 3:
                        break
                    if fallback not in questions:
                        questions.append(fallback)
                
                session.technical_questions['questions'] = questions[:3]
                
                # Move to technical questions phase
                from src.config.settings import ConversationState
                session.current_state = ConversationState.TECHNICAL_QUESTIONS
                
                tech_list = ', '.join(tech_stack[:5])  # Show first 5 technologies
                response = f"""🛠️ **Great! I see you work with:** {tech_list}

🧠 **Technical Assessment**

Based on your {experience_years} years of experience and your tech stack, I have {len(questions)} questions for you. These will help us understand your technical expertise better.

**Question 1 of {len(questions)}:**
{questions[0]}

*Please provide your answer, and I'll move to the next question.*"""
                
                return response
            else:
                return "I didn't catch any technologies in your response. Could you please list some technologies you work with? (e.g., Python, JavaScript, React, etc.)"
        else:
            return "Please tell me about your **tech stack** - what programming languages, frameworks, databases, and tools do you work with?"
    
    def _generate_simple_questions(self, tech_stack: list, level: str) -> list:
        """Generate simple technical questions based on tech stack and level"""
        questions = []
        
        # Common questions based on technologies
        question_templates = {
            'python': {
                'junior': "What is the difference between a list and a tuple in Python?",
                'mid': "Explain how Python's garbage collection works.",
                'senior': "How would you optimize a Python application for better performance?"
            },
            'javascript': {
                'junior': "What is the difference between let, const, and var in JavaScript?",
                'mid': "Explain how closures work in JavaScript with an example.",
                'senior': "How would you handle memory leaks in a JavaScript application?"
            },
            'react': {
                'junior': "What is the difference between functional and class components in React?",
                'mid': "Explain the React component lifecycle methods.",
                'senior': "How would you optimize a React application for better performance?"
            },
            'java': {
                'junior': "What is the difference between abstract classes and interfaces in Java?",
                'mid': "Explain how garbage collection works in Java.",
                'senior': "How would you design a scalable Java application architecture?"
            }
        }
        
        # Generate questions based on tech stack
        for tech in tech_stack[:3]:  # Max 3 questions
            tech_lower = tech.lower()
            if tech_lower in question_templates:
                questions.append(question_templates[tech_lower][level])
            else:
                # Generic questions
                if level == 'junior':
                    questions.append(f"What are the basic concepts you should know when working with {tech}?")
                elif level == 'mid':
                    questions.append(f"Describe a challenging project you've worked on using {tech}.")
                else:
                    questions.append(f"How would you architect a large-scale system using {tech}?")
        
        # Ensure we have at least 3 questions (prevent infinite loop)
        fallback_questions = [
            "Describe your approach to debugging code when you encounter an error.",
            "How do you ensure code quality and maintainability in your projects?",
            "How do you stay updated with the latest technologies and best practices?",
            "Tell me about a challenging project you've worked on.",
            "What's your experience with version control systems like Git?"
        ]
        
        fallback_index = 0
        while len(questions) < 3 and fallback_index < len(fallback_questions):
            if fallback_questions[fallback_index] not in questions:
                questions.append(fallback_questions[fallback_index])
            fallback_index += 1
        
        return questions[:3]  # Return exactly 3 questions
    
    # --------------------------------------------------
    # TECH STACK HANDLER
    # --------------------------------------------------
    def _handle_tech_stack(self, user_input: str) -> str:
        """Parse candidate tech stack input, determine role & level and generate questions"""
        session = self.get_session()

        # Basic stop words to discard common filler terms
        stop_words = {
            "i", "am", "i'm", "im", "good", "in", "with", "at", "and", "&", "/", "working",
            "have", "experience", "on", "of", "the", "using"
        }

        # Normalise & split tech stack string
        tokens = [t.strip().lower().rstrip(",.") for t in user_input.split() if t.strip()]
        tech_tokens = [t for t in tokens if t not in stop_words and len(t) > 1]

        # Deduplicate while preserving order
        seen = set()
        tech_stack = []
        for t in tech_tokens:
            if t not in seen:
                tech_stack.append(t)
                seen.add(t)

        # Persist raw stack for future reference
        session.candidate_info["tech_stack"] = tech_stack

        # Determine candidate role (take first desired position if any)
        desired_roles = session.candidate_info.get("desired_positions", []) if session.candidate_info else []
        candidate_role_raw = desired_roles[0] if desired_roles else "general"
        role_key = (
            candidate_role_raw.lower()
            .replace(" ", "_")
            .replace("-", "_")
        )  # map "Data Analyst" -> "data_analyst"

        # Determine level from experience
        exp_years = session.candidate_info.get("experience_years") or 0
        if exp_years <= 1:
            level = "junior"
        elif exp_years <= 4:
            level = "mid"
        else:
            level = "senior"

        # Try to fetch questions from QUESTION_TEMPLATES
        questions: list[str] = []
        template_for_role = QUESTION_TEMPLATES.get(role_key, {})
        if template_for_role:
            if level in template_for_role:
                questions = template_for_role[level][:]
            else:
                # pick any available list (junior/mid) if specific level missing
                questions = next(iter(template_for_role.values()))

        # If role template missing or less than 5 questions, fallback based on tech stack
        if len(questions) < 5:
            # Use helper to generate simple questions based on tech stack
            extra_qs = self._generate_simple_questions(tech_stack, level)
            questions.extend(q for q in extra_qs if q not in questions)

        # Ensure we have 5 questions maximum
        questions = questions[:5]

        # Save questions in session
        session.technical_questions = {
            "questions": questions,
            "responses": []
        }

        # Transition to technical questions state
        session.update_state(ConversationState.TECHNICAL_QUESTIONS)

        first_q = questions[0] if questions else "Could you tell me about a project that demonstrates your technical skills?"
        return (
            "✅ Great, thank you for sharing your technical skills! Let's dive into some questions.\n\n" +
            f"**Question 1 of {len(questions)}:**\n{first_q}\n\n*Please answer in as much detail as you can.*"
        )

    def _handle_technical_questions(self, user_input: str) -> str:
        """Handle technical questions phase with intelligent validation and empathy"""
        session = self.get_session()
        candidate_name = session.candidate_info.get('full_name', 'there').split()[0] if session.candidate_info else 'there'
        
        # Validate the answer quality
        answer = user_input.strip().lower()
        
        # Check for clarification requests
        clarification_requests = ['clarify', 'explain', 'what do you mean', 'i dont understand', "i don't understand", 'can you explain', 'what is this', 'help me understand']
        
        if any(request in answer for request in clarification_requests):
            # Get current question to provide clarification
            current_question_num = len(session.technical_questions['responses'])
            if current_question_num < len(session.technical_questions['questions']):
                current_question = session.technical_questions['questions'][current_question_num - 1] if current_question_num > 0 else "the question"
                return f"""Of course, {candidate_name}! Let me clarify the question for you. 😊

**Question Explanation:**
{current_question}

This question is asking you to explain your understanding or experience with this topic. You can:
- Share what you know about it
- Explain how you would approach it
- Give an example if you have one
- Say "I'm not familiar with this" if you don't know

Please try answering now! 🙏"""
        
        # Check for irrelevant tech stack answers (when user just lists technologies)
        tech_stack_pattern = ['python', 'sql', 'powerbi', 'excel', 'tableau', 'javascript', 'react', 'java']
        is_just_tech_list = (len(answer.split()) <= 6 and 
                            sum(1 for tech in tech_stack_pattern if tech in answer) >= 2 and
                            not any(word in answer for word in ['join', 'query', 'function', 'method', 'because', 'would', 'can', 'use', 'create', 'analyze']))
        
        if is_just_tech_list:
            return f"""I see you've listed some technologies, {candidate_name}! 😊

However, I need you to actually answer the technical question I asked. Please explain your understanding or approach to the specific question.

If you're not familiar with the topic, you can say:
- "I haven't worked with this directly, but I think..."
- "I'm not experienced with this, but my understanding is..."
- "I don't know this specific topic"

Please try answering the actual question now! 🙏"""
        
        # Check for very short or nonsensical answers
        nonsense_answers = ['hh', 'h', '.', '..', 'idk', 'dk', 'no', 'nah', 'nothing', 'aisehi', 'aise hi', 'kuch nahi', 'pata nahi', 'nhi', 'na', 'nope', 'dunno', 'xyz', 'abc', 'test', 'testing']

        if len(answer) <= 3 or answer in nonsense_answers or len(answer.split()) <= 1:
            return f"""I understand, {candidate_name}! 😊

Could you please provide a more detailed answer? Even if you're not completely sure, sharing your thoughts would be helpful.

If you're not familiar with this topic, you can say:
- "I haven't worked with this directly, but I think..."
- "I'm not very experienced with this, but my understanding is..."
- "I would approach this by..."
- "I don't know this specific topic, but I know..."

Please try answering again with a bit more detail! 🙏"""
        
        # Check for "I don't know" type responses
        dont_know_indicators = ['dont know', "don't know", 'not sure', 'no idea', 'never used', 'not familiar', 
                               'dont understand', "don't understand", 'confused', 'not experienced']
        
        if any(indicator in answer for indicator in dont_know_indicators):
            # Empathetic response and offer to adjust
            current_question_num = len(session.technical_questions['responses'])
            
            # Check if user mentioned specific technologies they DO know
            user_knows = []
            known_techs = ['python', 'sql', 'excel', 'powerbi', 'javascript', 'react', 'java', 'html', 'css']
            for tech in known_techs:
                if tech in answer:
                    user_knows.append(tech)
            
            if user_knows:
                # User mentioned technologies they know - adjust questions
                session.technical_questions['responses'].append(user_input)
                
                # Generate a question based on what they know
                known_tech = user_knows[0]
                if known_tech == 'python':
                    adjusted_question = "Great! Since you know Python, can you tell me about a simple Python project you've worked on or would like to work on?"
                elif known_tech == 'sql':
                    adjusted_question = "Perfect! Since you're familiar with SQL, can you explain what a JOIN operation does in simple terms?"
                elif known_tech == 'excel':
                    adjusted_question = "Excellent! Since you know Excel, can you describe how you've used formulas or functions in your work?"
                elif known_tech == 'powerbi':
                    adjusted_question = "Great! Since you work with PowerBI, can you tell me about a dashboard or report you've created?"
                else:
                    adjusted_question = f"That's perfectly fine, {candidate_name}! Since you mentioned {known_tech}, can you tell me about your experience with it?"
                
                total_questions = len(session.technical_questions['questions'])
                return f"""No worries at all, {candidate_name}! 😊

Everyone has different strengths and that's completely normal. I appreciate your honesty!

Let me ask you something more aligned with your experience:

**Adjusted Question {current_question_num + 1} of {total_questions}:**
{adjusted_question}

*Please share your thoughts - even basic experience is valuable!*"""
            else:
                # Generic empathetic response
                session.technical_questions['responses'].append(user_input)
                current_question_num = len(session.technical_questions['responses'])
                total_questions = len(session.technical_questions['questions'])
                
                if current_question_num < total_questions:
                    next_question = session.technical_questions['questions'][current_question_num]
                    return f"""That's absolutely fine, {candidate_name}! 😊

No one knows everything, and honesty is really appreciated in interviews. Let's try a different question:

**Question {current_question_num + 1} of {total_questions}:**
{next_question}

*Take your time and share whatever you know!*"""
        
        # Answer seems reasonable - store it and continue
        session.technical_questions['responses'].append(user_input)
        current_question_num = len(session.technical_questions['responses'])
        total_questions = len(session.technical_questions['questions'])
        
        if current_question_num < total_questions:
            # Ask next question
            next_question = session.technical_questions['questions'][current_question_num]
            return f"""✅ Thank you for that detailed response, {candidate_name}!

**Question {current_question_num + 1} of {total_questions}:**
{next_question}

*Please share your thoughts and experience.*"""
        else:
            # All questions completed, move to summary
            from src.config.settings import ConversationState
            session.current_state = ConversationState.SUMMARY
            
            # CRITICAL FIX: Save data to Google Sheets when interview completes
            if self.sheets_handler:
                try:
                    print(f"🔄 Attempting to save candidate data to Google Sheets...")
                    print(f"Session ID: {session.session_id}")
                    print(f"Candidate Info: {session.candidate_info is not None}")
                    print(f"Candidate Info Type: {type(session.candidate_info)}")
                    
                    # Convert dict to Pydantic model if needed
                    if isinstance(session.candidate_info, dict):
                        print(f"🔄 Converting dict to Pydantic model...")
                        from src.data.models import CandidateInfo
                        
                        # Create a copy with validated/cleaned data
                        cleaned_info = session.candidate_info.copy()
                        
                        # Fix common validation issues
                        if 'email' in cleaned_info:
                            # Fix semicolon in email
                            cleaned_info['email'] = cleaned_info['email'].replace(';', '.')
                            print(f"🔧 Fixed email: {cleaned_info['email']}")
                        
                        try:
                            # Convert to Pydantic model
                            pydantic_candidate_info = CandidateInfo(**cleaned_info)
                            session.candidate_info = pydantic_candidate_info
                            print(f"✅ Successfully converted to Pydantic model")
                        except Exception as validation_error:
                            print(f"⚠️ Pydantic validation failed: {str(validation_error)}")
                            # Continue with dict format - sheets handler will handle it
                    
                    success = self.sheets_handler.save_candidate_data(session)
                    if success:
                        print(f"✅ Data saved successfully to Google Sheets!")
                        st.success("✅ Your information has been saved to Google Sheets successfully!")
                    else:
                        print(f"❌ Failed to save data to Google Sheets")
                        st.error("❌ Failed to save data to Google Sheets")
                        
                except Exception as e:
                    print(f"❌ Exception while saving to Google Sheets: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    st.error(f"❌ Failed to save data: {str(e)}")
            else:
                print(f"⚠️ No Google Sheets handler available - data not saved to sheets")
                st.warning("⚠️ Google Sheets integration not available - data saved locally only")
            
            # Mark session as completed
            session.completed = True
            session.current_state = ConversationState.ENDED
            
            candidate_info = session.candidate_info
            
            # Handle both dict and Pydantic model formats
            if hasattr(candidate_info, 'tech_stack'):
                # Pydantic model format
                tech_stack = ', '.join(candidate_info.tech_stack[:5])
                full_name = candidate_info.full_name
                experience_years = candidate_info.experience_years
                desired_positions = ', '.join(candidate_info.desired_positions)
                email = candidate_info.email
            else:
                # Dict format
                tech_stack = ', '.join(candidate_info['tech_stack'][:5])
                full_name = candidate_info['full_name']
                experience_years = candidate_info['experience_years']
                desired_positions = ', '.join(candidate_info['desired_positions'])
                email = candidate_info['email']
            
            return f"""🎉 **Excellent work, {candidate_name}! You've completed the technical assessment!**

📋 **Interview Summary:**
• **Name:** {full_name}
• **Experience:** {experience_years} years
• **Position Interest:** {desired_positions}
• **Tech Stack:** {tech_stack}
• **Questions Answered:** {total_questions}

🎯 **Next Steps:**
1. Our technical team will review your responses
2. You'll receive feedback within 2-3 business days
3. If selected, we'll schedule a technical interview

📧 We'll contact you at **{email}** with updates.

**Thank you for your time and interest in TalentScout!** 🚀

*You can type 'restart' to begin a new application or 'exit' to end this session.*"""
    
    def _handle_summary(self, user_input: str) -> str:
        """Handle summary phase"""
        session = self.get_session()
        
        # Save data to sheets if available
        if self.sheets_handler:
            try:
                print(f"🔄 Attempting to save candidate data to Google Sheets...")
                print(f"Session ID: {session.session_id}")
                print(f"Candidate Info: {session.candidate_info is not None}")
                
                success = self.sheets_handler.save_candidate_data(session)
                if success:
                    print(f"✅ Data saved successfully to Google Sheets!")
                    st.success("✅ Your information has been saved to Google Sheets successfully!")
                else:
                    print(f"❌ Failed to save data to Google Sheets")
                    st.error("❌ Failed to save data to Google Sheets")
            except Exception as e:
                print(f"❌ Exception while saving to Google Sheets: {str(e)}")
                import traceback
                traceback.print_exc()
                st.error(f"❌ Failed to save data: {str(e)}")
        else:
            print(f"⚠️ No Google Sheets handler available - data not saved to sheets")
            st.warning("⚠️ Google Sheets integration not available - data saved locally only")
        
        # Mark session as completed
        session.completed = True
        session.update_state(ConversationState.ENDED)
        
        return "Thank you for completing the interview! Your information has been recorded and our team will review it shortly. You should hear back from us within 2-3 business days. Have a great day!"
    
    def _handle_conversation_end(self) -> str:
        """Handle conversation end request"""
        session = self.get_session()
        session.update_state(ConversationState.ENDED)
        
        return "Thank you for your time today. If you'd like to continue the interview process later, please feel free to start a new session. Have a great day!"
    
    def _handle_fallback(self, user_input: str) -> str:
        """Handle fallback cases"""
        return self.llm_handler.generate_response(
            prompt=user_input,
            context_type="fallback",
            conversation_history=self.get_session().chat_history
        )
    
    def _extract_candidate_info(self, text: str) -> Dict[str, Any]:
        """Extract candidate information from text"""
        extracted = {}
        
        # Try to extract email
        email = self.data_validator.extract_info_from_text(text, "email")
        if email:
            extracted["email"] = email
        
        # Try to extract phone
        phone = self.data_validator.extract_info_from_text(text, "phone")
        if phone:
            extracted["phone"] = phone
        
        # Try to extract experience
        experience = self.data_validator.extract_info_from_text(text, "experience")
        if experience:
            extracted["experience_years"] = experience
        
        # For other fields, use simple text processing
        text_lower = text.lower()
        
        # Check for name patterns
        if any(word in text_lower for word in ["name is", "i'm", "i am", "call me"]):
            # Extract potential name
            words = text.split()
            for i, word in enumerate(words):
                if word.lower() in ["name", "i'm", "am", "call"]:
                    if i + 1 < len(words):
                        potential_name = " ".join(words[i+1:i+3])  # Take next 1-2 words
                        if len(potential_name.strip()) > 1:
                            extracted["full_name"] = potential_name.strip()
                        break
        
        return extracted
    
    def _validate_and_update_candidate_info(self, extracted_info: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and update candidate information"""
        session = self.get_session()
        candidate = session.candidate_info
        
        # Track what's missing
        missing_fields = []
        
        # Update extracted information
        for field, value in extracted_info.items():
            if field == "full_name" and not candidate.full_name:
                is_valid, error = self.data_validator.validate_name(value)
                if is_valid:
                    candidate.full_name = value.strip().title()
                else:
                    return {"complete": False, "response": f"Name validation error: {error}"}
            
            elif field == "email" and not candidate.email:
                is_valid, error = self.data_validator.validate_email(value)
                if is_valid:
                    candidate.email = value.strip().lower()
                else:
                    return {"complete": False, "response": f"Email validation error: {error}"}
            
            elif field == "phone" and not candidate.phone:
                is_valid, error = self.data_validator.validate_phone(value)
                if is_valid:
                    candidate.phone = value.strip()
                else:
                    return {"complete": False, "response": f"Phone validation error: {error}"}
            
            elif field == "experience_years" and candidate.experience_years == 0:
                is_valid, error, exp_value = self.data_validator.validate_experience(value)
                if is_valid:
                    candidate.experience_years = exp_value
                else:
                    return {"complete": False, "response": f"Experience validation error: {error}"}
        
        # Check what's still missing
        if not candidate.full_name:
            missing_fields.append("full name")
        if not candidate.email:
            missing_fields.append("email address")
        if not candidate.phone:
            missing_fields.append("phone number")
        if candidate.experience_years == 0:
            missing_fields.append("years of experience")
        if not candidate.desired_positions:
            missing_fields.append("desired position(s)")
        if not candidate.location:
            missing_fields.append("current location")
        
        # If information is complete
        if not missing_fields:
            return {"complete": True, "response": ""}
        
        # Ask for next missing field
        next_field = missing_fields[0]
        prompts = {
            "full name": "Could you please tell me your full name?",
            "email address": "What's your email address?",
            "phone number": "Could you provide your phone number?",
            "years of experience": "How many years of professional experience do you have?",
            "desired position(s)": "What position(s) are you interested in?",
            "current location": "Where are you currently located?"
        }
        
        return {
            "complete": False, 
            "response": prompts.get(next_field, f"Could you please provide your {next_field}?")
        }
    
    def _analyze_user_sentiment(self, text: str):
        """Analyze and store user sentiment"""
        try:
            sentiment_analysis = self.sentiment_analyzer.analyze_sentiment(text)
            
            # Store in session state for display
            if 'sentiment_history' not in st.session_state:
                st.session_state.sentiment_history = []
            
            st.session_state.sentiment_history.append({
                "text": text,
                "sentiment": sentiment_analysis.sentiment_label,
                "score": sentiment_analysis.sentiment_score,
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            st.error(f"Sentiment analysis failed: {str(e)}")
    
    def _generate_interview_summary(self) -> str:
        """Generate interview summary"""
        session = self.get_session()
        
        # Analyze overall conversation sentiment
        sentiment_data = self.sentiment_analyzer.analyze_conversation_sentiment(session.chat_history)
        
        # Generate summary using LLM
        session_data = {
            "candidate_info": session.candidate_info.dict() if session.candidate_info else {},
            "responses": [r.dict() for r in session.responses],
            "sentiment_data": sentiment_data
        }
        
        summary = self.llm_handler.generate_summary(session_data)
        
        # Add sentiment insights
        sentiment_insights = self.sentiment_analyzer.get_sentiment_insights(sentiment_data)
        
        full_summary = f"{summary}\n\n**Interview Analysis:**\n"
        full_summary += f"- Overall Sentiment: {sentiment_data.get('overall_sentiment', 'neutral').title()}\n"
        full_summary += f"- Engagement Level: {sentiment_insights.get('engagement', 'Standard')}\n"
        full_summary += f"- Communication: {sentiment_insights.get('communication', 'Professional')}\n"
        
        return full_summary
    
    def get_progress_percentage(self) -> int:
        """Get conversation progress percentage"""
        session = self.get_session()
        state = session.current_state
        
        progress_map = {
            ConversationState.GREETING: 10,
            ConversationState.INFO_COLLECTION: 30,
            ConversationState.TECH_STACK: 50,
            ConversationState.TECHNICAL_QUESTIONS: 80,
            ConversationState.SUMMARY: 95,
            ConversationState.ENDED: 100
        }
        
        return progress_map.get(state, 0)
    
    def get_current_stage_description(self) -> str:
        """Get description of current conversation stage"""
        session = self.get_session()
        state = session.current_state
        
        descriptions = {
            ConversationState.GREETING: "Welcome & Introduction",
            ConversationState.INFO_COLLECTION: "Collecting Basic Information",
            ConversationState.TECH_STACK: "Technical Skills Assessment",
            ConversationState.TECHNICAL_QUESTIONS: "Technical Interview Questions",
            ConversationState.SUMMARY: "Interview Summary",
            ConversationState.ENDED: "Interview Completed"
        }
        
        return descriptions.get(state, "In Progress")
    
    def reset_conversation(self):
        """Reset conversation to start fresh"""
        st.session_state.conversation_session = ConversationSession()
        if 'sentiment_history' in st.session_state:
            del st.session_state.sentiment_history
