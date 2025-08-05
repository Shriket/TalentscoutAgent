"""
Google Sheets Integration for TalentScout Hiring Assistant
"""

import json
import gspread
from google.oauth2.service_account import Credentials
from typing import List, Dict, Any, Optional
from datetime import datetime
import streamlit as st
from src.data.models import CandidateInfo, ConversationSession
from src.config.settings import SHEET_HEADERS
from src.utils.gdpr_compliance import GDPRCompliance

class SheetsHandler:
    """Handles Google Sheets operations for candidate data storage"""
    
    def __init__(self, sheet_id: str, service_account_json):
        self.sheet_id = sheet_id
        self.gdpr_compliance = GDPRCompliance()
        
        # Handle both string and dict formats
        if isinstance(service_account_json, str):
            self.service_account_info = json.loads(service_account_json)
        elif isinstance(service_account_json, dict):
            self.service_account_info = service_account_json
        else:
            raise ValueError("service_account_json must be a string or dict")
            
        self.client = None
        self.sheet = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Google Sheets client"""
        try:
            # Define the scope
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Handle private key format issues
            service_account_copy = self.service_account_info.copy()
            private_key = service_account_copy.get('private_key', '')
            
            # Fix common private key format issues
            if private_key and not private_key.endswith('\n'):
                service_account_copy['private_key'] = private_key + '\n'
            
            # Ensure proper line breaks in private key
            if '\\n' in private_key:
                service_account_copy['private_key'] = private_key.replace('\\n', '\n')
            
            # Create credentials
            credentials = Credentials.from_service_account_info(
                service_account_copy, 
                scopes=scopes
            )
            
            # Authorize the client
            self.client = gspread.authorize(credentials)
            
            # Open the spreadsheet
            self.sheet = self.client.open_by_key(self.sheet_id).sheet1
            
            # Initialize headers if needed
            self._ensure_headers()
            
        except ValueError as e:
            if "Could not deserialize key data" in str(e):
                print(f"❌ Cryptography error: {str(e)}")
                print("💡 Trying alternative authentication method...")
                
                # Try alternative method - save to temp file
                try:
                    import tempfile
                    import json
                    
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                        json.dump(self.service_account_info, f)
                        temp_file = f.name
                    
                    credentials = Credentials.from_service_account_file(temp_file, scopes=scopes)
                    self.client = gspread.authorize(credentials)
                    self.sheet = self.client.open_by_key(self.sheet_id).sheet1
                    self._ensure_headers()
                    
                    # Clean up temp file
                    import os
                    os.unlink(temp_file)
                    
                    print("✅ Alternative authentication successful!")
                    return
                    
                except Exception as alt_e:
                    print(f"❌ Alternative method also failed: {str(alt_e)}")
                    st.error(f"Google Sheets authentication failed. Please check your service account key format.")
                    raise e
            else:
                st.error(f"Failed to initialize Google Sheets: {str(e)}")
                raise e
        except Exception as e:
            st.error(f"Failed to initialize Google Sheets: {str(e)}")
            raise e
    
    def _ensure_headers(self):
        """Ensure the sheet has proper headers"""
        try:
            # Get the first row
            first_row = self.sheet.row_values(1)
            
            # If empty or doesn't match our headers, set them
            if not first_row or first_row != SHEET_HEADERS:
                self.sheet.clear()
                self.sheet.append_row(SHEET_HEADERS)
                
        except Exception as e:
            st.error(f"Failed to set headers: {str(e)}")
    
    def save_candidate_data(self, session: ConversationSession) -> bool:
        """Save candidate data to Google Sheets"""
        try:
            if not session.candidate_info:
                return False
            
            candidate = session.candidate_info
            
            # Handle both Pydantic model and dict formats
            if hasattr(candidate, 'full_name'):
                # Pydantic model format
                full_name = candidate.full_name
                email = candidate.email
                phone = candidate.phone
                gender = getattr(candidate, 'gender', '')
                date_of_birth = getattr(candidate, 'date_of_birth', '')
                experience_years = candidate.experience_years
                desired_positions = ', '.join(candidate.desired_positions)
                location = candidate.location
                graduation_year = getattr(candidate, 'graduation_year', '')
                cgpa_10th = getattr(candidate, 'cgpa_10th', '')
                cgpa_12th = getattr(candidate, 'cgpa_12th', '')
                cgpa_degree = getattr(candidate, 'cgpa_degree', '')
                tech_stack = ', '.join(candidate.tech_stack)
                work_experience_description = getattr(candidate, 'work_experience_description', '')
                why_good_candidate = getattr(candidate, 'why_good_candidate', '')
            else:
                # Dict format
                full_name = candidate.get('full_name', '')
                email = candidate.get('email', '')
                phone = candidate.get('phone', '')
                gender = candidate.get('gender', '')
                date_of_birth = candidate.get('date_of_birth', '')
                experience_years = candidate.get('experience_years', 0)
                desired_positions = ', '.join(candidate.get('desired_positions', []))
                location = candidate.get('location', '')
                graduation_year = candidate.get('graduation_year', '')
                cgpa_10th = candidate.get('cgpa_10th', '')
                cgpa_12th = candidate.get('cgpa_12th', '')
                cgpa_degree = candidate.get('cgpa_degree', '')
                tech_stack = ', '.join(candidate.get('tech_stack', []))
                work_experience_description = candidate.get('work_experience_description', '')
                why_good_candidate = candidate.get('why_good_candidate', '')
            
            # Encrypt sensitive personal data for GDPR compliance
            encrypted_email = self.gdpr_compliance.encrypt_sensitive_data(email)
            encrypted_phone = self.gdpr_compliance.encrypt_sensitive_data(phone)
            encrypted_dob = self.gdpr_compliance.encrypt_sensitive_data(date_of_birth)
            
            # Log data access for audit trail
            self.gdpr_compliance.log_data_access("data_save", "candidate_info", session.session_id)
            
            # Prepare row data
            row_data = [
                datetime.now().isoformat(),  # Timestamp
                session.session_id,  # Session_ID
                full_name,  # Full_Name (not encrypted - needed for HR)
                encrypted_email,  # Email (encrypted)
                encrypted_phone,  # Phone (encrypted)
                gender,  # Gender
                encrypted_dob,  # Date_of_Birth (encrypted)
                experience_years,  # Experience_Years
                desired_positions,  # Desired_Positions
                location,  # Location
                graduation_year,  # Graduation_Year
                cgpa_10th,  # CGPA_10th
                cgpa_12th,  # CGPA_12th
                cgpa_degree,  # CGPA_Degree
                tech_stack,  # Tech_Stack
                work_experience_description,  # Work_Experience_Description
                why_good_candidate,  # Why_Good_Candidate
                self._format_technical_questions(session.technical_questions),  # Technical_Questions
                self._format_responses(session.technical_questions),  # Candidate_Responses
                self._calculate_average_sentiment(session.responses),  # Sentiment_Score
                self._calculate_questions_answered(session.technical_questions)  # Questions_Answered
            ]
                
            # Append to sheet
            self.sheet.append_row(row_data)
            return True
            
        except Exception as e:
            st.error(f"Failed to save data to sheets: {str(e)}")
            return False
    
    def _format_technical_questions(self, technical_questions_data) -> str:
        """Format technical questions for storage in Q1, Q2 format"""
        if not technical_questions_data:
            return ""
        
        # Handle both dict format (from session) and list format
        if isinstance(technical_questions_data, dict):
            questions = technical_questions_data.get('questions', [])
        else:
            questions = technical_questions_data
        
        if not questions:
            return ""
        
        formatted = []
        for i, question in enumerate(questions, 1):
            if hasattr(question, 'question'):
                formatted.append(f"Q{i}: {question.question}")
            else:
                formatted.append(f"Q{i}: {str(question)}")
        
        return "\n".join(formatted)
    
    def _format_responses(self, technical_questions_data) -> str:
        """Format candidate responses for storage in A1, A2 format"""
        if not technical_questions_data:
            return ""
        
        # Handle both dict format (from session) and list format
        if isinstance(technical_questions_data, dict):
            responses = technical_questions_data.get('responses', [])
        else:
            responses = technical_questions_data
        
        if not responses:
            return ""
        
        formatted = []
        for i, response in enumerate(responses, 1):
            if hasattr(response, 'response'):
                formatted.append(f"A{i}: {response.response}")
            else:
                formatted.append(f"A{i}: {str(response)}")
        
        return "\n".join(formatted)
    
    def _calculate_average_sentiment(self, responses: List) -> float:
        """Calculate average sentiment score"""
        if not responses:
            return 0.0
        
        # For now, return a placeholder
        # In real implementation, this would analyze sentiment of responses
        return 0.5
    
    def _calculate_questions_answered(self, technical_questions_data) -> str:
        """Calculate questions answered in format like '5/5'"""
        if not technical_questions_data:
            return "0/0"
        
        # Handle both dict format (from session) and list format
        if isinstance(technical_questions_data, dict):
            total_questions = len(technical_questions_data.get('questions', []))
            answered_questions = len(technical_questions_data.get('responses', []))
        else:
            # Fallback for list format
            total_questions = len(technical_questions_data) if technical_questions_data else 0
            answered_questions = total_questions  # Assume all answered if in list format
        
        return f"{answered_questions}/{total_questions}"
    
    def get_candidate_data(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve candidate data by session ID"""
        try:
            # Get all records
            records = self.sheet.get_all_records()
            
            # Find matching session
            for record in records:
                if record.get('Session_ID') == session_id:
                    return record
            
            return None
            
        except Exception as e:
            st.error(f"Failed to retrieve data: {str(e)}")
            return None
    
    def get_all_candidates(self) -> List[Dict[str, Any]]:
        """Get all candidate records"""
        try:
            return self.sheet.get_all_records()
        except Exception as e:
            st.error(f"Failed to retrieve all candidates: {str(e)}")
            return []
    
    def update_candidate_status(self, session_id: str, new_status: str) -> bool:
        """Update candidate status"""
        try:
            # Find the row with matching session_id
            records = self.sheet.get_all_records()
            
            for i, record in enumerate(records, start=2):  # Start from row 2 (after headers)
                if record.get('Session_ID') == session_id:
                    # Update the status column (last column)
                    self.sheet.update_cell(i, len(SHEET_HEADERS), new_status)
                    return True
            
            return False
            
        except Exception as e:
            st.error(f"Failed to update status: {str(e)}")
            return False
    
    def delete_candidate_data(self, session_id: str) -> bool:
        """Delete candidate data (for GDPR compliance)"""
        try:
            # Find and delete the row with matching session_id
            records = self.sheet.get_all_records()
            
            for i, record in enumerate(records, start=2):  # Start from row 2
                if record.get('Session_ID') == session_id:
                    self.sheet.delete_rows(i)
                    return True
            
            return False
            
        except Exception as e:
            st.error(f"Failed to delete data: {str(e)}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get basic statistics from the data"""
        try:
            records = self.sheet.get_all_records()
            
            if not records:
                return {
                    "total_candidates": 0,
                    "completed_interviews": 0,
                    "average_experience": 0,
                    "top_tech_stacks": []
                }
            
            # Calculate statistics
            total = len(records)
            completed = len([r for r in records if r.get('Status') == 'completed'])
            
            # Average experience
            exp_values = []
            for record in records:
                try:
                    exp = float(record.get('Experience_Years', 0))
                    exp_values.append(exp)
                except (ValueError, TypeError):
                    continue
            
            avg_exp = sum(exp_values) / len(exp_values) if exp_values else 0
            
            # Top tech stacks
            tech_counts = {}
            for record in records:
                tech_stack = record.get('Tech_Stack', '')
                if tech_stack:
                    techs = [t.strip() for t in tech_stack.split(',')]
                    for tech in techs:
                        tech_counts[tech] = tech_counts.get(tech, 0) + 1
            
            top_techs = sorted(tech_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            
            return {
                "total_candidates": total,
                "completed_interviews": completed,
                "completion_rate": (completed / total * 100) if total > 0 else 0,
                "average_experience": round(avg_exp, 1),
                "top_tech_stacks": top_techs
            }
            
        except Exception as e:
            st.error(f"Failed to get statistics: {str(e)}")
            return {}
    
    def export_data(self, format_type: str = "csv") -> Optional[str]:
        """Export data in specified format"""
        try:
            records = self.sheet.get_all_records()
            
            if format_type.lower() == "csv":
                import csv
                import io
                
                output = io.StringIO()
                if records:
                    writer = csv.DictWriter(output, fieldnames=records[0].keys())
                    writer.writeheader()
                    writer.writerows(records)
                
                return output.getvalue()
            
            elif format_type.lower() == "json":
                import json
                return json.dumps(records, indent=2, default=str)
            
            else:
                return None
                
        except Exception as e:
            st.error(f"Failed to export data: {str(e)}")
            return None
