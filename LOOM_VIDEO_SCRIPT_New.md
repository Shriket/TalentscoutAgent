### **INTRODUCTION (Start Recording)**

"Hello everyone! My name is Shriket and I am going to demonstrate an intelligent Hiring Assistant chatbot Talentscout, that I have developed for automated candidate screening, So lets get started."

### **PROJECT OVERVIEW**

"first of all, let me explain what TalentScout is. It is an intelligent hiring assistant chatbot that I have designed for a fictional recruitment agency called TalentScout that specializes in technology placements. The main purpose of this chatbot is to automate the initial screening process by gathering essential candidate information, generating tech stack specific technical questions, maintaining context throughout the conversation, and ensuring complete GDPR compliance.

So as u can seee this is the url of our hiring assistant chatbot, that i have deployed on streamlit"

### **USER INTERFACE DEMONSTRATION**

"Here you can see this clean and intuitive Streamlit interface. But before we proceed, notice that the very first thing users encounter is our GDPR compliance section - Privacy & Data Protection. here we have two important consent checkboxes:

As you can see, there is a clear privacy notice, that says 'Before we begin, please review our privacy policy and provide consent for data processing.'

There are two important consent checkboxes here
1. First checkbox: 'I consent to the processing and storage of my personal data for recruitment purposes'
2. Second checkbox: 'I consent to being contacted regarding this application and future opportunities'

Users must provide explicit consent before they can proceed with the interview. This ensures complete GDPR compliance from the very beginning. Let me check both these boxes to demonstrate.

Perfect! Now that consent is provided, let me walk you through the other key components. At the top, we have the TalentScout logo and branding with a clear description of what the assistant does. 

In the top action bar, I have implemented two important buttons. First is the Start Over button which allows users to reset their conversation at any time if they have done any mistake, and second is the Help button which provides comprehensive instructions to candidates.

As you click on click on this Help button this shows the complete user guide which includes the interview process steps, tips for success, available commands, and technical support information. This helps for providing clear instructions to users.

Now let me click the Help button again to hide this and start a fresh interview to demonstrate the core functionality."

### **CHATBOT CAPABILITIES DEMONSTRATION**

"Now let me experience the chatbot from a candidate's perspective. I will go through a complete interview simulation to show you all the features.

As you can see, the chatbot starts with a warm greeting and explains its purpose clearly and provides context about what to expect during the interview.

Now I will start providing my information step by step as required by the chatbot. Let me type my full name first. I will enter 'Shriket Raut'. Perfect, it has accepted my name and is now asking for my email address.

Let me enter my email as 'shriket@example.com'. Great! Now it is asking for my phone number. I will enter a phone number '987654321'. oh its just 9 numbers, let me correct it 9876543210 Excellent, it has validated my phone number correctly.

Lets enter my year of experince which is '1'. Perfect! Next it wants to know about my desired position. I will say 'data analyst'. Great!

Now it is asking for my current location. Let me enter 'Bengaluru, India'. Excellent!

Now comes the most important part - the tech stack declaration. This is where the magic happens. Let me specify my tech stack. I will type 'I work with Python, sql, power bi and excel

Perfect! Notice how the chatbot has processed this information and understood all the different technologies that I mentioned. It has identified Python, Django, React, PostgreSQL, Docker, and AWS from my input.

Now Based on the given tech stack and years of experince, it will generate a set of 4-5 technical questions tailored to assess the candidate’s proficiency in their tech stack.
Excellent! As you can see, it has generated the exact specific technical questions, about the tech stack we have provided,____.

Let me answer one of these questions to show you the context handling capability. I will click on the first question about Python, No let me confuse it with another unexpected answer, like i dont understand the question. Thats great well played, its helping to undeerstand the question, lets give the real answer now,
 Perfect! The chatbot maintains context throughout our conversation and provides appropriate follow-up responses based on my answers, 
 Its a great error handling and fallback mechanisms, gracefully handling the unexpected inputs, Providing meaningful responses when the chatbot doesnt understand the users input without deviating from the Purpose ensuring a coherent conversational flow.

now lets say, i dont know the answer, great it handels it well, now lets give it a real answer. perfect!

 and as you complete your interview Gracefully it concludes the conversation and thanking the candidate and informing them about the next steps.

 and as the interview completes it saves all the data in this google sheet.  

### **TECHNICAL IMPLEMENTATION**

"Now let me show you the technical architecture behind this application. Let me open VS Code to show you the project structure.

As you can see, The main.py file is the entry point using Streamlit. The src folder contains all the core functionality - the chatbot folder has the conversation logic and LLM integration, the ui folder contains user interface components and styling, the data folder has data models and Google Sheets integration, and the utils folder contains GDPR compliance and security utilities.

The key technologies that I have used are Streamlit for the frontend interface, Llama 3.1 70B Versatile (via Groq API) for LLM capabilities, Google Sheets API for data storage, Cryptography library for data encryption, and Pydantic for data validation.

Let me show you the conversation manager file. Here you can see, the sophisticated prompt engineering, I have implemented. This handles context-aware responses, tech stack analysis, question generation based on specific technologies, and conversation flow management.

and this prompts.py file contains all the carefully crafted prompts that ensure the LLM stays focused on the hiring context and generates relevant technical questions based on the candidate's declared tech stack. ensuring a coherent flow. "

### **DATA PRIVACY & SECURITY**

"One of the most important aspects of this project is data privacy and GDPR compliance.

Let me show you the privacy features that I have implemented. First, we have consent management where users must explicitly consent before any data processing begins. second, the data encryption where sensitive information like email, phone number, and date of birth are encrypted using AES-128 Fernet encryption before storing into the Google Sheets.

Third, there is a complete audit logging which maintains a trail of all the data ops. And fourth, I follow the data minimization principles where we only collect job-relevant information.

Let me show you the Google Sheets integration. As you can see in our Google Sheets storage, the sensitive fields are encrypted while maintaining readability for HR teams to access the necessary information.
"

### **ADVANCED FEATURES & BONUS POINTS**

"Let me highlight some advanced features which goes beyond the basic requirements and demonstrate bonus points.

First, I have implemented real-time data validation with email format validation and auto-correction suggestions, phone number formatting and validation, and experience validation with helpful error messages.

Second, I have implemented sentiment analysis where the system tracks user sentiment throughout the conversation to gauge the sentiment score.

finally, I have implemented performance optimization with efficient LLM API usage, caching for improved response times, and streamlined data processing.


### **CODE QUALITY & BEST PRACTICES**

"Let me show you that the codebase is well-structured, modular, and follows best practices for readability and maintainability, Comprehensive error handling with try-catch blocks, detailed comments and docstrings where necessary to explain complex logic and functions for documentation, clean Git history with meaningful commit messages,a well-organized repository"


### **CONCLUSION**

"So to summarize what I have demonstrated today - I have built a fully functional hiring assistant with intelligent conversation flow, implemented advanced prompt engineering for context-aware interactions, achieved complete GDPR compliance with enterprise-grade security, created tech stack-specific question generation using sophisticated LLM integration, developed production-ready code with comprehensive documentation, and added bonus features including sentiment analysis and advanced validation.

Thank you for watching! this demo, The complete source code and documentation, are available on my GitHub.

---
