### **INTRODUCTION (Start Recording)**

"Hello everyone! My name is Shriket and and in this video I'm going to demonstrate an intelligent Hiring Assistant chatbot Talentscout, that I have developed for automated candidate screening, So lets get started."

### **PROJECT OVERVIEW**

"first of all, let me explain what TalentScout is. It is an intelligent hiring assistant chatbot that I have designed for a fictional recruitment agency called TalentScout that specializes in technology placements. The main purpose of this chatbot is to automate the initial screening process by gathering essential candidate information, generating tech stack specific technical questions, maintaining context throughout the conversation, and ensuring complete GDPR compliance.

So let me run the main.py file using Streamlit. So that we can see the chatbot. 


### **USER INTERFACE DEMONSTRATION**

" now we can see this clean and intuitive Streamlit interface. before proceeding, the very first thing user will encounter is, this GDPR compliance section.
As you can see, there is a clear privacy notice, that says 'Before we begin, please review our privacy policy and provide consent for data processing.'

so Here we have these 2 important checkboxes for consent,
1. First one: is about processing and storage of users personal data for recruitment purposes'
2. Second one: is about being contacted regarding the application and future opportunities'
User must provide explicit consent before they can proceed with the interview. This ensures complete GDPR compliance from the very beginning. Let me check both these boxes

Perfect! Now the consent is provided, lets start the interview process. let me walk you through the other key components. At the top, we have the TalentScout logo and branding with a clear description of what the assistant does. 
In the top action bar, I have implemented two important buttons. First is the Start Over button which allows users to reset their conversation at any time if they have done any mistake in the interview process, if they click the startover button the existing responce will not get submitted, and can start with a new session, and second is the Help button which provides comprehensive instructions to candidates.

As you click on the Help button it shows the complete user guide, and steps of the interview process , tips for success, available commands, and  support information. This helps for providing clear instructions to users.

I will click the Help button again to hide this"

### **CHATBOT CAPABILITIES DEMONSTRATION**

"Now let me experience the chatbot from a candidate's perspective. I will go through a complete interview simulation to demonstrate all the core functionalities.

As you can see, the chatbot starts with a warm greeting message explaining its purpose clearly, and also provides the context about, what to expect during the interview.

Now I will start providing my information step by step as required by the chatbot.
i will say ok, so its asking, should we start or not, i will say no lets see what is says, very good, ok its enough lets say yes and start the interview.


Let me type my full name first. I will enter 'Shriket Raut'. Perfect, it has accepted my name and is now asking for my mail.

ok here it is shriket@example.com. oh! Now it is asking for my phone number. I will enter a random phone number '987654321'. oh its just 9 numbers, let me correct it 9876543210 Excellent, it has validated my phone number correctly, it means it doesnt takes wrong numbers

Lets enter my year of experince which is '1'. Perfect! Next it wants to know about my desired position. I will say 'data analyst'.

Now it is asking for my current location. Let me enter 'Bengaluru, India'.

ok Now comes the most important part - the tech stack declaration. This is where the magic happens. Let me specify my tech stack. I will say ' sql, power bi, Python and excel
Thats great the chatbot has processed it well and understood all the different technologies that I mentioned.

lets answer all these questions one by one.
_________________

Now Based on the given tech stack , it will generate a set of technical questions tailored to assess the candidate’s proficiency in their tech stack.
As you can see, it has generated the exact specific technical questions, about the tech stack we have provided,____.

Let me answer one of these questions to show you the context handling capability. I will click on the first question about Python, No let me confuse it with another unexpected answer, like i dont understand the question. Thats great well played, its helping to undeerstand the question, lets give the real answer now,
 Perfect! The chatbot maintains context throughout our conversation and provides appropriate follow-up responses based on my answers, 
 Its a great error handling and fallback mechanisms, gracefully handling the unexpected inputs, Providing meaningful responses when the chatbot doesnt understand the users input without deviating from the Purpose ensuring a coherent conversational flow.

now lets say, i dont know the answer, great it handels it well, now lets give it a real answer. perfect!



 and as you complete your interview, Gracefully it concludes the conversation and thanking the candidate and informing them about the next steps.

and as the interview completes it saves all the data in this google sheet,
lets see the google sheet, so as you can see,
 the info we have given to the bot has successfully appended into the sheeet with the timestamp, sentiment score and count of total questions answered.
so our bot provides all the information it gathered, in all this 21 columns 

### **TECHNICAL IMPLEMENTATION**

"Now let me show you the technical architecture behind this application. Let me open VS Code to show you the project structure.

As you can see, The main.py file is our entry point using Streamlit. 

The src folder contains all the core functionality 
- the chatbot folder has the conversation logic and LLM integration,
Let me show you the conversation manager file. Here you can see, the sophisticated prompt engineering, I have implemented. This handles context-aware responses, tech stack analysis, question generation based on specific technologies, and conversation flow management.
- the config folder has the Application configuration and settings also all the carefully crafted prompts llm
- the ui folder contains user interface components and styling, 
- the data folder has data models and Google Sheets integration, 
- the utils folder contains GDPR compliance and security utilities.  
encrypting sensitive information using AES-128 Fernet encryption before storing it into the Google Sheets.and I have followed the data minimization principles where we only collect job-relevant information.

The key technologies that I have used are Streamlit for the frontend , Llama 3.1 70B Versatile (via Groq API) for LLM capabilities, Google Sheets API for data storage, Cryptography library for data encryption, and Pydantic for data validation.

the docs folder contains - some Comprehensive Documentations such as.
user-guides folder has README and requirements documentation
Technical contains architecture documentation
api folder has- API and integration documentation
deployment has - Deployment and contributing guides
and compliance has - Privacy policy and GDPR compliance docs


### **CONCLUSION**

"So to summarize what I have demonstrated today - I have built a fully functional hiring assistant with intelligent conversation flow, implementing prompt engineering for context-aware interactions, achieved complete GDPR compliance with enterprise-grade security, created tech stack-specific question generation using sophisticated LLM integration, developed production-ready code with comprehensive documentation, and added bonus features including caching for improved response times, sentiment analysis and advanced validation.

Thank you for watching! this video, The complete source code and documentation, are available on my GitHub.

____________________________________________________________________________
_____________________________________________________________________________________
