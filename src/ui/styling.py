"""
CSS Styling for TalentScout Hiring Assistant
"""

import streamlit as st
import os

# Public URL to assistant logo image
LOGO_URL = "https://i.postimg.cc/W3JnprTS/logo.png"

def apply_custom_css():
    """Apply custom CSS styling to the Streamlit app"""
    
    css = """
    <style>
    /* Dark theme - Main app styling */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    .main {
        padding-top: 2rem;
        background-color: #0e1117;
    }
    
    /* Progress Action Bar - EXACTLY like mockup */
    .progress-action-bar {
        background: #060048;
        padding: 0.3rem 1rem 1rem 1rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        position: relative;
    }
    
    .progress-section {
        display: none !important;
        flex: 1;
        margin-right: 2rem;
        background: transparent !important;
    }
    
    /* Override Streamlit column background inside progress bar */
    .progress-action-bar div[data-testid="column"] {
        background: transparent !important;
    }
    
    .progress-section h4 {
        color: white;
        margin: 0 0 0.5rem 0;
        font-size: 1rem;
        font-weight: 600;
    }
    
    .progress-bar-inline {
        background: rgba(255,255,255,0.2);
        height: 8px;
        border-radius: 4px;
        overflow: hidden;
        width: 100%;
    }
    
    .progress-fill-inline {
        background: #4fc3f7;
        height: 100%;
        border-radius: 4px;
        transition: width 0.3s ease;
    }
    
    .button-section {
        display: flex;
        gap: 0.5rem;
    }
    
    /* Style buttons inside progress bar */
    .progress-action-bar .stButton>button {
        background: #0e1117 !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
        height: 40px !important;
        min-width: 100px !important;
    }
    
    .progress-action-bar .stButton>button:hover {
        background: #060048 !important;
    }
    
    /* More specific targeting for buttons */
    .progress-action-bar div[data-testid="column"] .stButton>button {
        background: #0e1117 !important;
        color: white !important;
        border: 1px solid #333 !important;
    }
    
    .progress-action-bar div[data-testid="column"] .stButton>button:hover {
        background: #262626 !important;
    }
    
    /* Ultra specific targeting - highest priority */
    div.progress-action-bar div[data-testid="column"] button[kind="primary"],
    div.progress-action-bar div[data-testid="column"] button[kind="secondary"],
    div.progress-action-bar div[data-testid="column"] button {
        background-color: #0e1117 !important;
        background: #0e1117 !important;
        color: white !important;
        border: 1px solid #333 !important;
    }
    
    div.progress-action-bar div[data-testid="column"] button:hover {
        background-color: #262626 !important;
        background: #262626 !important;
    }
    
    /* Target exact button classes from DOM */
    .progress-action-bar button[data-testid="baseButton-secondary"],
    .progress-action-bar button.st-emotion-cache-1i0chw4,
    .progress-action-bar button.ef3psqc13 {
        background-color: #0e1117 !important;
        background: #0e1117 !important;
        color: white !important;
        border: 1px solid #333 !important;
    }
    
    .progress-action-bar button[data-testid="baseButton-secondary"]:hover,
    .progress-action-bar button.st-emotion-cache-1i0chw4:hover,
    .progress-action-bar button.ef3psqc13:hover {
        background-color: #262626 !important;
        background: #262626 !important;
    }
    
    /* Global override for Streamlit buttons */
    button[data-testid="baseButton-primary"],
    button[data-testid="baseButton-secondary"] {
        background-color: #0e1117 !important;
        background: #0e1117 !important;
        background-image: none !important;
        color: #ffffff !important;
        border: 1px solid #333 !important;
    }
    
    button[data-testid="baseButton-primary"]:hover,
    button[data-testid="baseButton-secondary"]:hover {
        background-color: #262626 !important;
        background: #262626 !important;
        background-image: none !important;
        color: #ffffff !important;
    }
    
    /* SUPER AGGRESSIVE - Override everything */
    .progress-action-bar * button {
        background-color: #0e1117 !important;
        background: #0e1117 !important;
        background-image: none !important;
    }
    
    .progress-action-bar * button:hover {
        background-color: #262626 !important;
        background: #262626 !important;
        background-image: none !important;
    }

    /* Small inline progress bar */
    .progress-inline-small {
        display: none !important;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-top: 24px;   /* pushes label + bar down */

    }

    .progress-label {
        font-size: 1rem;
        font-weight: 600;
        color: #ffffff;
    }

    .progress-bar-inline-small {
        background: #3e3e59;
        height: 8px;
        width: 160px;
        border-radius: 4px;
        overflow: hidden;
    }

    .progress-fill-inline-small {
        background: #4fc3f7;
        height: 100%;
        border-radius: 4px;
        transition: width 0.3s ease;
    }

    /* Header styling - Dark theme */
    .main-header {
        background: #040032;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(255, 255, 255, 0.1);
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.2rem;
        font-weight: 600;
    }
    
    .main-header p {
        color: #e8f4f8;
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    
    /* Chat container styling - Dark theme */
    .chat-container {
        background: #1e1e1e;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(255, 255, 255, 0.1);
        margin-bottom: 1rem;
        max-height: 500px;
        overflow-y: auto;
        border: 1px solid #333;
    }
    
    /* Message bubble styling - Dark theme */
    .user-message {
        background: #2d3748;
        color: #ffffff;
        padding: 1rem;
        border-radius: 15px 15px 5px 15px;
        margin: 0.5rem 0;
        margin-left: 2rem;
        border-left: 4px solid #1f77b4;
    }
    
    .assistant-message {
        background: #1a202c;
        color: #ffffff;
        padding: 1rem;
        border-radius: 15px 15px 15px 5px;
        margin: 0.5rem 0;
        margin-right: 2rem;
        border-left: 4px solid #2e86c1;
        line-height: 1.6;
        word-wrap: break-word;
    }
    
    .message-header {
        margin-bottom: 0.5rem;
    }
    
    .message-content {
        line-height: 1.6;
        white-space: normal;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    /* Progress bar styling - Dark theme */
    .progress-container {
        background: #1e1e1e;
        color: #ffffff;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(255, 255, 255, 0.1);
        border: 1px solid #333;
    }
    
    .progress-bar {
        background: #333;
        border-radius: 10px;
        height: 10px;
        overflow: hidden;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #1f77b4, #2e86c1);
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    /* Input styling - Dark theme */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #444;
        background-color: #2d3748;
        color: #ffffff;
        padding: 0.75rem 1rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #1f77b4;
        box-shadow: 0 0 0 2px rgba(31, 119, 180, 0.2);
        background-color: #2d3748;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #040032;
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(255, 255, 255, 0.1);
    }
    
    .stButton > button:hover {
        background-color: #060048;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(255, 255, 255, 0.2);
    }
    
    /* Form submit button - Dark theme */
    .stForm > div > div > button {
        background-color: #040032 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stForm > div > div > button:hover {
        background-color: #060048 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Sidebar styling - Dark theme */
    .css-1d391kg {
        background: #1a1a1a;
        color: #ffffff;
    }
    
    /* Info cards - Dark theme */
    .info-card {
        background: #1e1e1e;
        color: #ffffff;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(255, 255, 255, 0.1);
        border-left: 4px solid #1f77b4;
        border: 1px solid #333;
    }
    
    .info-card h4 {
        color: #4fc3f7;
        margin: 0 0 0.5rem 0;
    }
    
    .info-card p {
        margin: 0;
        color: #cccccc;
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.875rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    .status-active {
        background: #2e7d32;
        color: #ffffff;
    }
    
    .status-pending {
        background: #f57c00;
        color: #ffffff;
    }
    
    .status-completed {
        background: #1976d2;
        color: #ffffff;
    }
    
    /* Sentiment display - Dark theme */
    .sentiment-display {
        background: #1e1e1e;
        color: #ffffff;
        border-radius: 8px;
        padding: 0.75rem;
        margin: 0.5rem 0;
        border-left: 4px solid #4caf50;
        font-size: 0.9rem;
        border: 1px solid #333;
    }
    
    /* Loading animation */
    .loading-dots {
        display: inline-block;
    }
    
    .loading-dots::after {
        content: '...';
        animation: dots 1.5s steps(4, end) infinite;
    }
    
    @keyframes dots {
        0%, 20% { content: '.'; }
        40% { content: '..'; }
        60% { content: '...'; }
        80%, 100% { content: ''; }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.8rem;
        }
        
        .user-message, .assistant-message {
            margin-left: 0.5rem;
            margin-right: 0.5rem;
        }
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    .chat-container::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 10px;
    }
    
    .chat-container::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8;
    }
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)

def create_message_bubble(message: str, is_user: bool = False) -> str:
    """Create HTML for message bubble with natural chat formatting"""
    css_class = "user-message" if is_user else "assistant-message"
    if is_user:
        icon_html = "👤"
    else:
        icon_html = f'<img src="{LOGO_URL}" width="20" style="vertical-align:middle;">'
    
    # Format message content to preserve line breaks and structure
    formatted_message = message.replace('\n', '<br>')
    
    return f"""
    <div class="{css_class}">
        <div class="message-header">
            <strong>{icon_html} {'You' if is_user else 'TalentScout Assistant'}:</strong>
        </div>
        <div class="message-content">
            {formatted_message}
        </div>
    </div>
    """

def create_progress_bar(percentage: int, label: str = "") -> str:
    """Create HTML for progress bar"""
    return f"""
    <div class="progress-container">
        <h4>Interview Progress {f'- {label}' if label else ''}</h4>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {percentage}%"></div>
        </div>
        <p style="margin-top: 0.5rem; color: #666;">{percentage}% Complete</p>
    </div>
    """

def create_info_card(title: str, content: str, icon: str = "ℹ️") -> str:
    """Create HTML for info card"""
    return f"""
    <div class="info-card">
        <h4>{icon} {title}</h4>
        <p>{content}</p>
    </div>
    """

def create_status_indicator(status: str, text: str) -> str:
    """Create HTML for status indicator"""
    return f'<span class="status-indicator status-{status}">{text}</span>'

def create_sentiment_display(sentiment_data: dict) -> str:
    """Create HTML for sentiment display"""
    sentiment = sentiment_data.get('overall_sentiment', 'neutral')
    score = sentiment_data.get('sentiment_score', 0.0)
    
    emoji_map = {
        'positive': '😊',
        'negative': '😟',
        'neutral': '😐'
    }
    
    color_map = {
        'positive': '#4caf50',
        'negative': '#f44336',
        'neutral': '#ff9800'
    }
    
    emoji = emoji_map.get(sentiment, '😐')
    color = color_map.get(sentiment, '#ff9800')
    
    return f"""
    <div class="sentiment-display" style="border-left-color: {color};">
        <strong>{emoji} Sentiment Analysis</strong><br>
        Overall: {sentiment.title()} (Score: {score:.2f})
    </div>
    """
