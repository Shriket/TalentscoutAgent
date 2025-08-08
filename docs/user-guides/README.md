# 🤖 TalentScout Hiring Assistant

<div align="center">

![TalentScout Logo](https://img.shields.io/badge/TalentScout-AI%20Hiring%20Assistant-blue?style=for-the-badge&logo=robot)
![Python](https://img.shields.io/badge/Python-3.9+-green?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?style=for-the-badge&logo=streamlit)
![GDPR](https://img.shields.io/badge/GDPR-Compliant-success?style=for-the-badge&logo=shield)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**An Enterprise-Grade AI-Powered Hiring Assistant for Intelligent Candidate Screening**

<div align="center">

### 🌐 **Live Demo & Resources**

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Try_Now-success?style=for-the-badge&logo=streamlit)](https://talentscouts-hiring-assistant.streamlit.app)
[![Demo Video](https://img.shields.io/badge/🎬_Demo_Video-Watch_Now-red?style=for-the-badge&logo=youtube)](https://youtu.be/lrc5D28AdkU)

**Experience the AI-powered hiring process in action!**

</div>

</div>

---

## 📋 Table of Contents

- [🌟 Project Overview](#-project-overview)
- [✨ Key Features & Capabilities](#-key-features--capabilities)
- [🚀 Quick Start](#-quick-start)
- [📖 Installation Instructions](#-installation-instructions)
- [🎯 Usage Guide](#-usage-guide)
- [🏗️ Technical Details](#️-technical-details)
- [🧠 Prompt Design](#-prompt-design)
- [🚧 Challenges & Solutions](#-challenges--solutions)
- [📊 Performance Metrics](#-performance-metrics)
- [🔒 GDPR Compliance](#-gdpr-compliance)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🌟 Project Overview

**TalentScout Hiring Assistant** is a cutting-edge AI-powered recruitment platform that revolutionizes the candidate screening process. Built with enterprise-grade security and GDPR compliance, it provides intelligent, contextual interviews that assess both technical skills and cultural fit.

### 🎯 **Mission Statement**
*"To democratize intelligent hiring by providing AI-powered candidate assessment that is fair, comprehensive, and privacy-compliant."*

### 🏆 **What Makes TalentScout Special?**

- **🤖 AI-Driven Intelligence**: Advanced LLM integration for natural, human-like conversations
- **⚡ Real-Time Processing**: Sub-2-second response times for seamless candidate experience
- **🔒 Enterprise Security**: GDPR-compliant with end-to-end encryption of sensitive data
- **📊 Comprehensive Assessment**: Collects 21+ data points with behavioral sentiment analysis
- **🌍 Global Ready**: Multi-language framework ready (currently English, with Hindi/Spanish support planned)
- **📈 Scalable Architecture**: Handles concurrent users with cloud-ready deployment

### 🎪 **Core Capabilities**

1. **Intelligent Conversation Management**: Context-aware dialogue that adapts to candidate responses
2. **Role-Specific Technical Assessment**: Customized questions based on job position and experience level
3. **Real-Time Data Validation**: Smart input validation with helpful error correction
4. **Automated Data Export**: Seamless integration with Google Sheets for HR workflow
5. **Behavioral Analysis**: Sentiment scoring and communication style assessment
6. **Privacy-First Design**: Complete GDPR compliance with data subject rights implementation

---

## ✨ Key Features & Capabilities

<div align="center">

| 🎯 **Core Features** | 🔧 **Technical Features** | 🛡️ **Security & Compliance** |
|:-------------------:|:------------------------:|:----------------------------:|
| Intelligent Conversation Flow | Streamlit Web Interface | GDPR Compliant Data Handling |
| Role-Specific Technical Questions | Google Sheets Integration | AES-128 (Fernet) Data Encryption |
| Real-Time Sentiment Analysis | Streamlit Web Architecture | Audit Logging & Monitoring |
| Multi-Language Framework | Automated Testing Suite | Data Subject Rights Portal |
| Behavioral Assessment | Cloud-Ready Deployment | Privacy Policy Management |
| Comprehensive Reporting | Data Export Features | Consent Management System |

</div>

### 🚀 **Advanced Features**

#### **🧠 Intelligent Assessment Engine**
- **Adaptive Questioning**: Dynamic question generation based on candidate responses and experience level
- **Context-Aware Validation**: Smart answer validation with empathetic follow-ups for incomplete responses
- **Role-Based Customization**: Tailored questions for different job positions (Data Analyst, Software Developer, etc.)
- **Experience-Level Adaptation**: Questions automatically adjust complexity based on years of experience

#### **📊 Comprehensive Data Collection**
- **Personal Information**: Full name, contact details, demographics, location
- **Educational Background**: Graduation year, CGPA scores (10th/12th/Degree)
- **Professional Profile**: Years of experience, desired positions, current location, work history
- **Technical Assessment**: 5-6 role-specific technical questions with detailed evaluation
- **Behavioral Analysis**: Sentiment scoring, communication style, and cultural fit assessment

#### **🔒 Enterprise-Grade Security**
- **Data Encryption**: Sensitive fields (email, phone, DOB) encrypted using AES-128 (Fernet) before storage
- **Access Control**: Service account authentication with role-based permissions
- **Audit Trail**: Complete logging of all data operations and user consent
- **Privacy Rights**: Self-service portal for data access, correction, and deletion requests

---

## 🚀 Quick Start

### **⚡ 5-Minute Setup**

```bash
# 1. Clone the repository
git clone https://github.com/shriket/talentscout-hiring-assistant.git
cd talentscout-hiring-assistant

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your API keys (see Installation section)

# 4. Run the application
streamlit run main.py
```

🎉 **That's it!** Your TalentScout instance is now running at `http://localhost:8501`

---

## 📖 Installation Instructions

### **📋 Prerequisites**

- **Python**: 3.9 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: Minimum 4GB RAM recommended
- **Storage**: 500MB free space
- **Internet**: Stable connection for API calls

### **🔧 Detailed Installation Steps**

#### **Step 1: Environment Setup**

```bash
# Create virtual environment (highly recommended)
python -m venv talentscout-env

# Activate virtual environment
# Windows:
talentscout-env\Scripts\activate
# macOS/Linux:
source talentscout-env/bin/activate
```

#### **Step 2: Install Dependencies**

```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
python -c "import streamlit; print('✅ Streamlit version:', streamlit.__version__)"
python -c "import groq; print('✅ Groq client installed successfully')"
```

#### **Step 3: API Keys Configuration**

Create a `.env` file in the project root directory:

```env
# AI Configuration
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant

# Google Sheets Integration
GOOGLE_SHEET_ID=your_google_sheet_id_here
GOOGLE_SERVICE_ACCOUNT_JSON='{"type": "service_account", "project_id": "your-project", ...}'

# Security Keys (generate strong keys)
SECRET_KEY=your-secret-key-minimum-32-characters-long
ENCRYPTION_KEY=your-fernet-encryption-key-32-bytes

# Application Settings
APP_ENV=development
DEBUG_MODE=True
LOG_LEVEL=INFO
```

#### **Step 4: Google Sheets Setup**

1. **Create Google Cloud Project**:
   - Visit [Google Cloud Console](https://console.cloud.google.com/)
   - Create new project: "TalentScout-Hiring"
   - Enable Google Sheets API

2. **Create Service Account**:
   - Navigate to IAM & Admin > Service Accounts
   - Create service account: "talentscout-sheets-service"
   - Download JSON key file
   - Copy JSON content to `GOOGLE_SERVICE_ACCOUNT_JSON` in `.env`

3. **Setup Google Sheet**:
   - Create new Google Sheet: "TalentScout Candidate Data"
   - Share sheet with service account email (Editor permissions)
   - Copy Sheet ID from URL and add to `.env`

#### **Step 5: Launch Application**

```bash
# Test configuration
python -c "from src.config.settings import Settings; print('✅ Configuration loaded successfully')"

# Run application
streamlit run main.py

# Application will be available at: http://localhost:8501
```

---

## 🎯 Usage Guide

### **👤 For HR Professionals**

#### **🎬 Conducting an Interview**

1. **Launch Application**: Open browser to `http://localhost:8501`
2. **Privacy Consent**: Candidate reviews and accepts privacy policy
3. **Personal Information**: System collects basic candidate details
4. **Educational Background**: Graduation year and academic performance
5. **Professional Profile**: Experience, skills, and career goals
6. **Technical Assessment**: Role-specific technical questions (5-6 questions)
7. **Behavioral Questions**: Work experience and motivation assessment
8. **Interview Summary**: Complete profile generation and data export

#### **📊 Interview Process Flow**

```
Candidate Arrives → Privacy Consent → Personal Information → 
Educational Background → Professional Experience → Technical Skills → 
Technical Assessment → Behavioral Questions → Interview Summary → 
Data Export to Google Sheets
```

#### **📈 Accessing Results**

- **Google Sheets**: Real-time data export with 21+ candidate fields
- **Sentiment Analysis**: Behavioral assessment scores and communication style
- **Technical Evaluation**: Detailed responses to role-specific questions
- **Compliance Reports**: GDPR audit trails and consent management records

### **👨‍💻 For Developers**

#### **🔧 Development Workflow**

```bash
# Run comprehensive tests
python test_real_sheets_save.py

# Run automated interview simulation
python final_test.py

# Check code quality
flake8 src/
black src/

# Generate documentation
sphinx-build -b html docs/ docs/_build/
```

#### **🧪 Testing the System**

```bash
# Test Google Sheets integration
python test_sheets_connection.py

# Run end-to-end interview simulation
python final_test.py

# Expected output format:
# Q1 bot: What's your full name?
# A1 user: John Smith
# Q2 bot: What's your email address?
# A2 user: john.smith@email.com
# ... (complete interview flow)
```

---

## 🏗️ Technical Details

### **🎯 System Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend UI   │    │  Business Logic │    │   Data Layer    │
│   (Streamlit)   │◄──►│   (Managers)    │◄──►│  (Handlers)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ GDPR Compliance │    │   LLM Handler   │    │ Google Sheets   │
│    Module       │    │  (Groq API)     │    │     API         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **📚 Libraries and Dependencies**

#### **Core Framework**
- **Streamlit** (1.28+): Web application framework for rapid UI development
- **Python** (3.9+): Primary programming language with modern features

#### **AI and Machine Learning**
- **Groq API**: High-performance LLM inference with Llama-3.1-8b-instant model
- **TextBlob**: Natural language processing for sentiment analysis
- **Google Translate API**: Multi-language support and translation

#### **Data Management**
- **Pydantic** (2.0+): Data validation and serialization with type hints
- **Google Sheets API**: Cloud-based data storage and real-time synchronization
- **Pandas**: Data manipulation and analysis

#### **Security and Compliance**
- **Cryptography**: AES-128 (Fernet) encryption for sensitive data protection
- **Python-dotenv**: Secure environment variable management
- **Logging**: Comprehensive audit trail and error tracking

#### **Testing and Quality**
- **Pytest**: Comprehensive testing framework
- **Black**: Code formatting and style consistency
- **Flake8**: Code linting and quality checks

### **🔧 Architectural Decisions**

#### **1. Modular Design Pattern**
```python
src/
├── chatbot/           # Conversation logic and AI integration
├── data/              # Data models and validation
├── ui/                # User interface components
├── utils/             # Utility functions and GDPR compliance
└── config/            # Settings and prompt templates
```

#### **2. State Management**
- **Streamlit Session State**: Maintains conversation context across interactions
- **Pydantic Models**: Ensures data integrity and type safety
- **Enum-based States**: Clear conversation flow management

#### **3. API Integration Strategy**
- **Groq API**: Chosen for high-performance LLM inference with low latency
- **Google Sheets API**: Selected for real-time collaboration and accessibility
- **Service Account Authentication**: Secure, scalable access control

#### **4. Performance Optimization**
- **Async Processing**: Non-blocking operations for better user experience
- **Caching Strategy**: Efficient prompt and response caching
- **Error Handling**: Graceful degradation and retry mechanisms

### **📊 Data Models**

#### **Candidate Information Schema**
```python
class CandidateInfo(BaseModel):
    # Personal Information (21+ fields)
    full_name: str
    email: EmailStr
    phone: str
    gender: str
    date_of_birth: str
    current_location: str
    
    # Educational Background
    graduation_year: int
    cgpa_10th: float
    cgpa_12th: float
    cgpa_degree: float
    
    # Professional Profile
    experience_years: int
    desired_positions: str
    tech_stack: str
    work_experience: Optional[str]
    why_good_candidate: Optional[str]
    
    # Technical Assessment
    technical_questions: Optional[str]
    candidate_responses: Optional[str]
    questions_answered: str = "0/0"
    
    # Analytics and Metadata
    sentiment_score: Optional[float]
    interview_date: Optional[str]
    interview_duration: Optional[str]
    completion_status: str = "In Progress"
```

---

## 🧠 Prompt Design

### **🎯 Prompt Engineering Strategy**

Our AI system uses carefully crafted prompts to ensure natural, contextual conversations while maintaining professional assessment standards. The prompt design follows a multi-layered approach:

#### **🏗️ Prompt Architecture**

```python
# Base System Prompt Template
SYSTEM_PROMPT = """
You are a professional, friendly HR interviewer conducting a candidate screening interview.

Your role:
- Conduct a structured interview to collect candidate information
- Ask clear, professional questions
- Validate responses and provide helpful feedback
- Maintain a supportive and encouraging tone
- Guide candidates through the process step-by-step

Conversation Guidelines:
- Be concise and clear in your questions
- Show empathy for nervous candidates
- Provide context for why information is needed
- Offer help if candidates seem confused
- Maintain professional boundaries
"""
```

#### **🎨 Prompt Design Principles**

1. **Context Awareness**: Prompts adapt based on candidate responses and conversation history
2. **Progressive Difficulty**: Technical questions scale with declared experience level
3. **Role Specificity**: Customized content for different job positions and tech stacks
4. **Empathetic Communication**: Supportive tone for nervous or uncertain candidates
5. **Cultural Sensitivity**: Inclusive language that works across different backgrounds

#### **📝 Information Gathering Prompts**

```python
# Personal Information Collection
INFO_PROMPTS = {
    'greeting': """
    Hello! 👋 Welcome to the TalentScout interview process. 
    I'm here to learn about your background and skills. 
    The entire process takes about 5-10 minutes. 
    Are you ready to get started?
    """,
    
    'full_name': """
    Great! Let's start with your full name. 
    Please provide your first and last name.
    """,
    
    'email': """
    What's your email address? 
    This will be used for follow-up communications.
    """,
    
    'experience_validation': """
    I notice you mentioned {years} years of experience. 
    Could you briefly describe your work experience? 
    This helps me ask more relevant technical questions.
    """
}
```

#### **🔧 Technical Question Generation**

```python
# Role-Specific Question Templates
TECHNICAL_PROMPTS = {
    'data_analyst': {
        'junior': [
            "Explain the difference between a primary key and a foreign key in databases.",
            "How would you handle missing values in a dataset?",
            "What's the difference between INNER JOIN and LEFT JOIN in SQL?"
        ],
        'mid': [
            "Describe your approach to data cleaning and preprocessing.",
            "How would you optimize a slow-running SQL query?",
            "Explain the concept of data normalization and when to use it."
        ],
        'senior': [
            "Design a data pipeline for real-time analytics processing.",
            "How would you implement data quality monitoring in production?",
            "Describe your approach to A/B testing analysis and statistical significance."
        ]
    }
}
```

#### **🤖 Dynamic Question Generation**

```python
# AI-Powered Question Customization
QUESTION_GENERATION_PROMPT = """
Generate a technical interview question for a {role} position.

Candidate Profile:
- Role: {desired_position}
- Experience Level: {experience_level}
- Tech Stack: {tech_stack}
- Years of Experience: {experience_years}

Requirements:
1. Question should match their declared skill level
2. Must be relevant to their tech stack: {tech_stack}
3. Should be answerable in 2-3 minutes
4. Include practical, scenario-based elements
5. Progressive difficulty based on experience

Format: Provide one clear, specific question that tests both knowledge and practical application.
"""
```

---

## 🚧 Challenges & Solutions

### **🎯 Development Journey**

Building TalentScout presented unique challenges that required innovative solutions:

#### **Challenge 1: Natural Conversation Flow**

**🔴 Problem**: Creating human-like, contextual conversations while maintaining structured data collection and professional assessment standards.

**💡 Solution Approach**:
- **State-Based Architecture**: Implemented finite state machine for conversation flow
- **Context Preservation**: Maintained conversation history and candidate profile throughout session
- **Adaptive Responses**: Dynamic prompt generation based on user responses and experience level
- **Empathetic Error Handling**: Supportive feedback for incomplete or unclear responses

**🛠️ Technical Implementation**:
```python
class ConversationManager:
    def __init__(self, session_state):
        self.state = ConversationState.GREETING
        self.context = {}
        self.conversation_history = []
    
    def process_user_input(self, user_input: str) -> str:
        # Context-aware response generation
        if self.is_clarification_request(user_input):
            return self.provide_clarification()
        elif self.is_incomplete_answer(user_input):
            return self.request_more_details()
        else:
            return self.process_valid_input(user_input)
```

**📈 Impact**: Provides smooth interview experience with natural conversation flow and comprehensive candidate assessment

#### **Challenge 2: GDPR Compliance Implementation**

**🔴 Problem**: Implementing comprehensive GDPR compliance while maintaining seamless user experience and system performance.

**💡 Solution Approach**:
- **Privacy by Design**: Built compliance into core architecture from day one
- **Granular Consent Management**: Explicit consent for each data processing activity
- **Data Minimization**: Collect only job-relevant information
- **Encryption at Rest**: AES-128 (Fernet) encryption for all sensitive personal data
- **Audit Trail**: Complete logging of all data operations and user consent

**🛠️ Technical Implementation**:
```python
class GDPRCompliance:
    def __init__(self):
        self.cipher_suite = Fernet(os.getenv('ENCRYPTION_KEY'))
        self.audit_log = []
    
    def encrypt_sensitive_data(self, data: str) -> str:
        return self.cipher_suite.encrypt(data.encode()).decode()
    
    def log_consent(self, user_id: str, consent_type: str, granted: bool):
        self.audit_log.append({
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'consent_type': consent_type,
            'granted': granted,
            'ip_address': self.get_user_ip()
        })
```

**📈 Impact**: Implements comprehensive GDPR compliance with enterprise-grade security and transparent data handling

#### **Challenge 3: Real-Time Data Validation**

**🔴 Problem**: Validating diverse user inputs while providing helpful, non-frustrating feedback that guides users toward correct responses.

**💡 Solution Approach**:
- **Intelligent Validation**: Context-aware validation rules with smart error messages
- **Progressive Validation**: Guide users step-by-step rather than rejecting outright
- **Auto-Correction**: Automatic fixing of common mistakes (e.g., email semicolon → dot)
- **Helpful Suggestions**: Provide examples and format guidance

**🛠️ Technical Implementation**:
```python
def validate_email(self, email: str) -> tuple[bool, str]:
    # Auto-correct common mistakes
    corrected_email = email.replace(';', '.')
    
    if not self.is_valid_email_format(corrected_email):
        return False, "Please provide a valid email address (e.g., john@company.com)"
    
    return True, corrected_email
```

**📈 Impact**: Ensures accurate data collection with user-friendly validation and clear error messaging

---

## 📊 Performance Metrics

### **🎯 Development Targets**

| Feature | Target | Implementation | Status |
|---------|--------|----------------|--------|
| **Response Time** | <3s | Optimized LLM calls | ✅ Achieved |
| **Data Validation** | Real-time | Input validation system | ✅ Implemented |
| **GDPR Compliance** | Full compliance | Encryption + consent forms | ✅ Implemented |
| **User Experience** | Intuitive flow | Streamlit interface | ✅ Achieved |
| **Data Security** | Encrypted storage | AES-128 Fernet encryption | ✅ Implemented |
| **Error Handling** | Graceful failures | Try-catch + user feedback | ✅ Implemented |

---

## 🔒 GDPR Compliance

### **🛡️ Compliance Overview**

**TalentScout** implements comprehensive GDPR compliance measures through technical and organizational controls:

#### **📋 GDPR Compliance Implementation**

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Lawful Basis | ✅ | Legitimate interest + Consent |
| Transparency | ✅ | Clear privacy notices |
| Consent Management | ✅ | Granular consent system |
| Data Subject Rights | ✅ | Self-service portal |
| Data Security | ✅ | AES-128 (Fernet) encryption |
| Data Minimization | ✅ | Job-relevant data only |
| Audit Logging | ✅ | Complete activity logs |
| Data Retention | ✅ | 12-month policy |

### **👤 Data Subject Rights**

- **Right to Access**: One-click data export in JSON format (✅ Implemented)
- **Right to Rectification**: Self-service data correction request form (✅ Implemented)
- **Right to Erasure**: Secure data deletion request process (✅ Implemented)
- **Right to Portability**: JSON structured data export (✅ Implemented)

*Note: Data correction and deletion requests are processed manually by administrators for security compliance.*

---

## 🤝 Contributing

We welcome contributions to TalentScout! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### **🔧 Development Setup**
```bash
# Fork and clone the repository
git clone https://github.com/shriket/talentscout-hiring-assistant.git

# Install development dependencies
pip install -r requirements.txt

# Run tests
python test_real_sheets_save.py

# Submit pull request
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ by the TalentScout Team**

[🌟 Star this repo](https://github.com/shriket/talentscout-hiring-assistant) • [🐛 Report Bug](https://github.com/shriket/talentscout-hiring-assistant/issues) • [💡 Request Feature](https://github.com/shriket/talentscout-hiring-assistant/issues)

</div>
