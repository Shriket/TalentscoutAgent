"""
UI Components for TalentScout Hiring Assistant
"""

import streamlit as st
from typing import List, Dict, Any, Optional
from datetime import datetime
import time

from src.ui.styling import (
    apply_custom_css, create_message_bubble, create_progress_bar,
    create_info_card, create_status_indicator, create_sentiment_display
)
from src.chatbot.conversation_manager import ConversationManager

def setup_page_config():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="TalentScout Hiring Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Force dark theme for better text visibility
    st.markdown("""
    <style>
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        
        /* Override Streamlit's default styles for dark theme */
        .main .block-container {
            background-color: #0e1117;
            color: #fafafa;
        }
        
        /* Sidebar dark theme */
        .css-1d391kg, .css-1lcbmhc {
            background-color: #1a1a1a;
            color: #ffffff;
        }
        
        /* Text elements */
        .stMarkdown, .stText, p, div, span {
            color: #fafafa !important;
        }
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            color: #ffffff !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Apply custom CSS
    apply_custom_css()

def render_header():
    """Render the main header"""
    st.markdown("""
    <div class="main-header">
        <h1>🤖 TalentScout Hiring Assistant</h1>
        <p>AI-powered candidate screening and technical assessment</p>
    </div>
    """, unsafe_allow_html=True)

def render_chat_interface(conversation_manager: ConversationManager):
    """Render the main chat interface"""
    
    # Create columns for layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        render_chat_area(conversation_manager)
    
    with col2:
        render_sidebar_info(conversation_manager)

def render_chat_area(conversation_manager: ConversationManager):
    """Render the main chat area"""
    
    # Get current session
    session = conversation_manager.get_session()
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Show welcome message if no chat history
        if not session.chat_history:
            welcome_msg = """
            👋 Hello! Welcome to TalentScout!
            
            I'm your AI hiring assistant, and I'm here to help you through our application process.
            
            Here's what we'll do together:
            1. ✅ Collect your basic information (name, email, experience)
            2. 🛠️ Learn about your technical skills and preferred tech stack
            3. 🧠 Ask you some technical questions based on your expertise
            4. 📊 Provide feedback and next steps
            """
            st.markdown(create_message_bubble(welcome_msg, is_user=False), unsafe_allow_html=True)
        else:
            # Display chat history
            for message in session.chat_history:
                is_user = message["role"] == "user"
                content = message["content"]
                st.markdown(create_message_bubble(content, is_user), unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Input area
    render_input_area(conversation_manager)

def render_input_area(conversation_manager: ConversationManager):
    """Render the input area for user messages"""
    
    session = conversation_manager.get_session()
    
    # Check if conversation is ended
    if session.current_state == "ended":
        st.info("Interview completed! Thank you for your time.")
        if st.button("Start New Interview", key="new_interview"):
            conversation_manager.reset_conversation()
            st.rerun()
        return
    
    # Input form
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_input = st.text_input(
                "Your message:",
                placeholder="Type your response here...",
                key="user_input",
                label_visibility="collapsed"
            )
        
        with col2:
            submit_button = st.form_submit_button("Send", use_container_width=True)
        
        # Process input when submitted
        if submit_button and user_input.strip():
            process_user_input(conversation_manager, user_input.strip())

def process_user_input(conversation_manager: ConversationManager, user_input: str):
    """Process user input and update chat"""
    
    # Show typing indicator
    with st.spinner("TalentScout is typing..."):
        start_time = time.time()
        
        # Process the input
        response = conversation_manager.process_user_input(user_input)
        
        # Ensure minimum response time for better UX
        elapsed_time = time.time() - start_time
        if elapsed_time < 1.0:
            time.sleep(1.0 - elapsed_time)
    
    # Rerun to update the interface
    st.rerun()

def render_sidebar_info(conversation_manager: ConversationManager):
    """Render sidebar with progress and information"""
    
    session = conversation_manager.get_session()
    
    # Progress section (GREEN BOX - KEEP)
    st.markdown("### Interview Progress")
    progress = conversation_manager.get_progress_percentage()
    stage_description = conversation_manager.get_current_stage_description()
    
    st.markdown(create_progress_bar(progress, stage_description), unsafe_allow_html=True)
    
    # Control buttons (GREEN BOX - KEEP)
    render_control_buttons(conversation_manager)

def render_candidate_summary(candidate_info):
    """Render candidate information summary"""
    
    st.markdown("### Candidate Information")
    
    info_items = []
    
    # Handle both dict and Pydantic model formats
    def get_field(field_name):
        if isinstance(candidate_info, dict):
            return candidate_info.get(field_name)
        else:
            return getattr(candidate_info, field_name, None)
    
    if get_field('full_name'):
        info_items.append(f"**Name:** {get_field('full_name')}")
    
    if get_field('email'):
        info_items.append(f"**Email:** {get_field('email')}")
    
    experience_years = get_field('experience_years')
    if experience_years and experience_years > 0:
        info_items.append(f"**Experience:** {experience_years} years")
    
    desired_positions = get_field('desired_positions')
    if desired_positions:
        positions = ", ".join(desired_positions)
        info_items.append(f"**Position:** {positions}")
    
    if get_field('location'):
        info_items.append(f"**Location:** {get_field('location')}")
    
    tech_stack = get_field('tech_stack')
    if tech_stack:
        tech_stack_str = ", ".join(tech_stack[:3])  # Show first 3
        if len(tech_stack) > 3:
            tech_stack_str += f" (+{len(tech_stack) - 3} more)"
        info_items.append(f"**Tech Stack:** {tech_stack_str}")
    
    if info_items:
        info_content = "<br>".join(info_items)
        st.markdown(create_info_card(
            "Profile Summary",
            info_content,
            "👤"
        ), unsafe_allow_html=True)

def render_sentiment_summary():
    """Render sentiment analysis summary"""
    
    st.markdown("### Sentiment Analysis")
    
    sentiment_history = st.session_state.sentiment_history
    
    if sentiment_history:
        # Get latest sentiment
        latest = sentiment_history[-1]
        
        # Calculate average sentiment
        scores = [item['score'] for item in sentiment_history]
        avg_score = sum(scores) / len(scores)
        
        # Determine overall sentiment
        if avg_score > 0.1:
            overall_sentiment = "positive"
        elif avg_score < -0.1:
            overall_sentiment = "negative"
        else:
            overall_sentiment = "neutral"
        
        sentiment_data = {
            'overall_sentiment': overall_sentiment,
            'sentiment_score': avg_score
        }
        
        st.markdown(create_sentiment_display(sentiment_data), unsafe_allow_html=True)
        
        # Show trend
        if len(sentiment_history) >= 2:
            trend = "improving" if scores[-1] > scores[0] else "stable" if scores[-1] == scores[0] else "declining"
            trend_emoji = {"improving": "📈", "stable": "➡️", "declining": "📉"}
            
            st.markdown(create_info_card(
                "Sentiment Trend",
                f"{trend_emoji.get(trend, '➡️')} {trend.title()}",
                "📊"
            ), unsafe_allow_html=True)

def render_session_info(session):
    """Render session information"""
    
    st.markdown("### Session Info")
    
    # Session duration
    if session.started_at:
        duration = datetime.now() - session.started_at
        duration_str = str(duration).split('.')[0]  # Remove microseconds
        
        st.markdown(create_info_card(
            "Duration",
            duration_str,
            "⏱️"
        ), unsafe_allow_html=True)
    
    # Message count
    message_count = len(session.chat_history)
    st.markdown(create_info_card(
        "Messages",
        f"{message_count} exchanged",
        "💬"
    ), unsafe_allow_html=True)
    
    # Questions answered
    if session.responses:
        answered = len(session.responses)
        total = len(session.technical_questions)
        st.markdown(create_info_card(
            "Technical Questions",
            f"{answered}/{total} answered",
            "❓"
        ), unsafe_allow_html=True)

def render_control_buttons(conversation_manager: ConversationManager):
    """Render control buttons"""
    
    st.markdown("### Actions")
    
    # Reset conversation button (GREEN BOX - KEEP)
    if st.button("🔄 Start Over", use_container_width=True):
        if st.session_state.get('confirm_reset', False):
            conversation_manager.reset_conversation()
            st.session_state.confirm_reset = False
            st.rerun()
        else:
            st.session_state.confirm_reset = True
            st.warning("Click again to confirm reset")
    
    # Help button (GREEN BOX - KEEP)
    if st.button("❓ Help", use_container_width=True):
        show_help_dialog()

def export_conversation(conversation_manager: ConversationManager):
    """Export conversation to downloadable format"""
    
    session = conversation_manager.get_session()
    
    # Create export content
    export_content = f"""
TalentScout Hiring Assistant - Conversation Export
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Session ID: {session.session_id}

=== CANDIDATE INFORMATION ===
"""
    
    if session.candidate_info:
        candidate = session.candidate_info
        export_content += f"""
Name: {candidate.full_name}
Email: {candidate.email}
Phone: {candidate.phone}
Experience: {candidate.experience_years} years
Position(s): {', '.join(candidate.desired_positions)}
Location: {candidate.location}
Tech Stack: {', '.join(candidate.tech_stack)}
"""
    
    export_content += "\n=== CONVERSATION HISTORY ===\n"
    
    for message in session.chat_history:
        role = "User" if message["role"] == "user" else "Assistant"
        timestamp = message.get("timestamp", "")
        content = message["content"]
        export_content += f"\n[{timestamp}] {role}: {content}\n"
    
    if session.responses:
        export_content += "\n=== TECHNICAL QUESTIONS & RESPONSES ===\n"
        for i, response in enumerate(session.responses, 1):
            export_content += f"\nQ{i}: {response.question}"
            export_content += f"\nA{i}: {response.response}"
            if response.sentiment_score is not None:
                export_content += f"\nSentiment: {response.sentiment_score:.2f}\n"
    
    # Create download button
    st.download_button(
        label="Download Conversation",
        data=export_content,
        file_name=f"talentscout_interview_{session.session_id[:8]}.txt",
        mime="text/plain"
    )

def show_help_dialog():
    """Show help information"""
    
    with st.expander("🆘 Help & Instructions", expanded=True):
        st.markdown("""
        ### How to Use TalentScout Hiring Assistant
        
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

def render_typing_indicator():
    """Render typing indicator animation"""
    return """
    <div style="padding: 1rem; color: #666;">
        <span class="loading-dots">TalentScout is typing</span>
    </div>
    """

def show_error_message(error: str):
    """Show error message with styling"""
    st.error(f"❌ {error}")

def show_success_message(message: str):
    """Show success message with styling"""
    st.success(f"✅ {message}")

def show_info_message(message: str):
    """Show info message with styling"""
    st.info(f"ℹ️ {message}")

def show_warning_message(message: str):
    """Show warning message with styling"""
    st.warning(f"⚠️ {message}")

def create_quick_response_buttons(options: List[str]) -> Optional[str]:
    """Create quick response buttons"""
    
    st.markdown("**Quick responses:**")
    
    cols = st.columns(len(options))
    
    for i, option in enumerate(options):
        with cols[i]:
            if st.button(option, key=f"quick_{i}"):
                return option
    
    return None

def render_loading_screen():
    """Render loading screen while initializing"""
    
    st.markdown("""
    <div style="text-align: center; padding: 3rem;">
        <h2>🤖 Initializing TalentScout Assistant...</h2>
        <p>Setting up your interview session</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bar animation
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress_bar.progress(i + 1)
    
    st.success("✅ Ready to start your interview!")
    time.sleep(1)
