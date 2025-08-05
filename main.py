"""
TalentScout Hiring Assistant - Main Entry Point
A Streamlit-based AI chatbot for automated candidate screening
"""

import streamlit as st
import os

# Load environment variables (only in local development)
try:
    from dotenv import load_dotenv
    # Ensure .env values override existing environment vars (e.g., Streamlit Cloud defaults)
    load_dotenv(override=True)
except ImportError:
    # Running on Streamlit Cloud - use st.secrets instead
    pass

# Import custom modules
from src.ui.components import setup_page_config, render_header, render_chat_interface, render_progress_actions_bar
from src.chatbot.conversation_manager import ConversationManager
from src.config.settings import AppConfig
from src.utils.gdpr_compliance import GDPRCompliance

def main():
    """Main application entry point"""
    
    # Initialize GDPR compliance
    gdpr_compliance = GDPRCompliance()
    
    # Configure Streamlit page
    setup_page_config()
    
    # Initialize app configuration
    config = AppConfig()
    
    # Initialize conversation manager
    if 'conversation_manager' not in st.session_state:
        st.session_state.conversation_manager = ConversationManager(config)
    
    # Render header
    render_header()

    # Progress + actions top bar
    render_progress_actions_bar(st.session_state.conversation_manager)
    
    # Show help if toggled
    if st.session_state.get('show_help', False):
        st.info("""
🆘 **Help & Instructions**

**How to Use TalentScout Hiring Assistant**

**Interview Process:**
1. **Introduction** - We'll start with a welcome and overview
2. **Basic Information** - Provide your contact details and experience
3. **Technical Skills** - Tell us about your tech stack and expertise
4. **Technical Questions** - Answer 3-5 questions based on your skills
5. **Summary** - Review and completion

**Tips for Success:**
- Be honest and specific about your experience
- Provide complete information when asked
- Take your time with technical questions
- Ask for clarification if needed

**Commands:**
- Type "help" anytime for assistance
- Say "bye" or "quit" to end early
- Use "start over" to restart the interview

**Technical Support:**
If you experience any issues, please contact our support team.
        """)
    
    # GDPR Compliance Check
    if 'gdpr_consent_given' not in st.session_state:
        st.markdown("### 🔒 Privacy & Data Protection")
        st.info("Before we begin, please review our privacy policy and provide consent for data processing.")
        
        consent_given = gdpr_compliance.show_privacy_notice()
        
        if consent_given:
            st.session_state.gdpr_consent_given = True
            gdpr_compliance.log_data_access("consent_obtained", "user_consent")
            st.success("✅ Thank you for providing consent. You can now proceed with the interview.")
            st.rerun()
        else:
            st.stop()
    
    # GDPR compliance achieved through consent form and privacy policy only
    # No additional data management features needed for assignment requirements
    
    # Render main chat interface
    render_chat_interface(st.session_state.conversation_manager)

if __name__ == "__main__":
    main()
