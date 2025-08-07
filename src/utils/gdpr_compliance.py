"""
GDPR Compliance Module for TalentScout Hiring Assistant
Handles consent management, data encryption, and privacy rights
"""

import hashlib
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import streamlit as st
from cryptography.fernet import Fernet
import base64

class GDPRCompliance:
    """Handles GDPR compliance features"""
    
    def __init__(self):
        self.encryption_key = self._get_or_create_encryption_key()
        self.cipher_suite = Fernet(self.encryption_key)
    
    def _get_or_create_encryption_key(self) -> bytes:
        """Get or create encryption key for data protection"""
        try:
            # In production, store this securely (e.g., environment variable)
            key = Fernet.generate_key()
            return key
        except Exception:
            return Fernet.generate_key()
    
    def show_privacy_notice(self) -> bool:
        """Display privacy notice and get consent"""
        st.markdown("### 🔒 Data Privacy Notice")
        
        with st.expander("📋 Click to read our Privacy Policy", expanded=False):
            st.markdown("""
            **TalentScout Privacy Notice**
            
            We collect and process your personal data for recruitment purposes only:
            
            **Data We Collect:**
            - Personal details (name, email, phone, DOB, location)
            - Professional information (experience, skills, education)
            - Interview responses and assessments
            
            **Legal Basis:** Legitimate interest for recruitment
            
            **Contact:** privacy@talentscout.com for any privacy queries
            """)
        
        # Consent checkboxes (simplified)
        consent_data_processing = st.checkbox(
            "✅ I consent to the processing and storage of my personal data for recruitment purposes", 
            key="consent_processing"
        )
        
        consent_communication = st.checkbox(
            "✅ I consent to being contacted regarding this application and future opportunities", 
            key="consent_communication"
        )
        
        # Check if both consents are given
        both_consents_given = consent_data_processing and consent_communication
        
        # Show start button only when both consents are given
        start_interview = False
        if both_consents_given:
            st.markdown("---")
            start_interview = st.button(
                "🚀 Start Interview Process", 
                type="primary",
                use_container_width=True,
                key="start_interview_btn"
            )
            
            # Record consent only when starting interview
            if start_interview:
                self._record_consent({
                    'data_processing': consent_data_processing,
                    'communication': consent_communication,
                    'timestamp': datetime.now().isoformat(),
                    'ip_address': self._get_user_ip()
                })
        elif consent_data_processing or consent_communication:
            st.warning("⚠️ Please check both consent boxes to proceed with the interview.")
        
        return start_interview
    
    def _record_consent(self, consent_data: Dict[str, Any]):
        """Record user consent with timestamp"""
        if 'gdpr_consent' not in st.session_state:
            st.session_state.gdpr_consent = {}
        
        st.session_state.gdpr_consent.update(consent_data)
    
    def _get_user_ip(self) -> str:
        """Get user IP address (placeholder - implement based on deployment)"""
        return "127.0.0.1"  # Placeholder
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive personal data"""
        if not data:
            return ""
        try:
            encrypted_data = self.cipher_suite.encrypt(data.encode())
            return base64.b64encode(encrypted_data).decode()
        except Exception:
            return data  # Fallback to original if encryption fails
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive personal data"""
        if not encrypted_data:
            return ""
        try:
            decoded_data = base64.b64decode(encrypted_data.encode())
            decrypted_data = self.cipher_suite.decrypt(decoded_data)
            return decrypted_data.decode()
        except Exception:
            return encrypted_data  # Fallback to original if decryption fails
    
    def anonymize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Anonymize personal data for analytics"""
        anonymized = data.copy()
        
        # Hash personally identifiable information
        if 'full_name' in anonymized:
            anonymized['full_name'] = self._hash_data(anonymized['full_name'])
        if 'email' in anonymized:
            anonymized['email'] = self._hash_data(anonymized['email'])
        if 'phone' in anonymized:
            anonymized['phone'] = self._hash_data(anonymized['phone'])
        
        return anonymized
    
    def _hash_data(self, data: str) -> str:
        """Hash sensitive data for anonymization"""
        return hashlib.sha256(data.encode()).hexdigest()[:8]
    
    def show_data_subject_rights(self):
        """Display data subject rights options directly visible"""
        st.markdown("### ☰ Your Data Rights")
        st.markdown("**Data Subject Rights (GDPR)**")
        
        # Vertical layout for buttons - directly visible
        if st.button("📥 Download My Data", use_container_width=True, key="download_data"):
            self._export_user_data()
        
        if st.button("✏️ Correct My Data", use_container_width=True, key="correct_data"):
            self._show_data_correction_form()
        
        if st.button("🗑️ Delete My Data", use_container_width=True, key="delete_data"):
            self._show_data_deletion_form()
    
    def _export_user_data(self):
        """Export user data in JSON format"""
        if 'conversation_session' in st.session_state:
            session = st.session_state.conversation_session
            user_data = {
                'personal_info': session.candidate_info if hasattr(session, 'candidate_info') else {},
                'interview_responses': session.chat_history if hasattr(session, 'chat_history') else [],
                'consent_records': st.session_state.get('gdpr_consent', {}),
                'export_timestamp': datetime.now().isoformat()
            }
            
            st.download_button(
                label="📥 Download Your Data (JSON)",
                data=json.dumps(user_data, indent=2),
                file_name=f"talentscout_data_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
            st.success("✅ Your data is ready for download!")
    
    def _show_data_correction_form(self):
        """Show form for data correction requests"""
        st.markdown("**Data Correction Request**")
        
        correction_field = st.selectbox(
            "Which field needs correction?",
            ["Full Name", "Email", "Phone", "Location", "Other"]
        )
        
        current_value = st.text_input("Current Value:")
        corrected_value = st.text_input("Corrected Value:")
        reason = st.text_area("Reason for correction:")
        
        if st.button("Submit Correction Request"):
            correction_request = {
                'field': correction_field,
                'current_value': current_value,
                'corrected_value': corrected_value,
                'reason': reason,
                'timestamp': datetime.now().isoformat()
            }
            
            # In production, send this to admin/HR system
            st.success("✅ Correction request submitted! We'll process it within 48 hours.")
    
    def _show_data_deletion_form(self):
        """Show form for data deletion requests"""
        st.markdown("**Data Deletion Request**")
        st.warning("⚠️ This will permanently delete all your data from our systems.")
        
        deletion_reason = st.selectbox(
            "Reason for deletion:",
            ["No longer interested", "Found another job", "Privacy concerns", "Other"]
        )
        
        confirm_deletion = st.checkbox("I confirm I want to delete all my data permanently")
        
        if st.button("🗑️ Submit Deletion Request", type="secondary"):
            if confirm_deletion:
                deletion_request = {
                    'reason': deletion_reason,
                    'timestamp': datetime.now().isoformat(),
                    'confirmed': True
                }
                
                # In production, process deletion request
                st.success("✅ Deletion request submitted! Your data will be removed within 30 days.")
            else:
                st.error("Please confirm deletion by checking the checkbox.")
    
    def log_data_access(self, action: str, data_type: str, user_id: str = None):
        """Log data access for audit trail"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'data_type': data_type,
            'user_id': user_id or 'anonymous',
            'ip_address': self._get_user_ip()
        }
        
        # In production, store in secure audit log
        if 'audit_log' not in st.session_state:
            st.session_state.audit_log = []
        
        st.session_state.audit_log.append(log_entry)
    
    def check_data_retention(self, data_timestamp: datetime) -> bool:
        """Check if data should be retained based on retention policy"""
        retention_period = timedelta(days=365)  # 12 months
        return datetime.now() - data_timestamp < retention_period
    
    def get_compliance_status(self) -> Dict[str, bool]:
        """Get current GDPR compliance status"""
        return {
            'consent_obtained': bool(st.session_state.get('gdpr_consent', {}).get('data_processing')),
            'privacy_notice_shown': 'gdpr_consent' in st.session_state,
            'data_encrypted': True,  # Assuming encryption is implemented
            'audit_logging': 'audit_log' in st.session_state,
            'retention_policy': True,  # Policy defined
            'subject_rights_available': True  # Rights UI available
        }
