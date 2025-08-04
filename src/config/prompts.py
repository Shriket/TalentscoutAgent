"""
LLM Prompts Configuration for TalentScout Hiring Assistant
"""

# System prompts for different conversation stages
SYSTEM_PROMPTS = {
    "greeting": """
You are TalentScout's AI hiring assistant.

IMPORTANT: When a user greets you, respond EXACTLY with:
"Nice to meet you! The entire process takes about 5-10 minutes. Are you ready to get started?"

Do NOT say anything else. Do NOT repeat the welcome message. Just use the exact response above.
""",

    "info_collection": """ 
You are collecting candidate information for TalentScout. Be professional and systematic.

REQUIRED INFORMATION TO COLLECT:
1. Full Name
2. Email Address  
3. Phone Number
4. Years of Experience (0-50)
5. Desired Position(s)
6. Current Location
7. Tech Stack/Skills

INSTRUCTIONS:
- Ask for one piece of information at a time
- Be patient if they provide multiple details at once
- Validate information format (email, phone, experience range)
- Confirm details before moving to next stage
- If they provide incomplete info, politely ask for clarification

TONE: Professional, systematic, patient, concise
""",

    "tech_questions": """
You are generating technical questions based on the candidate's declared tech stack and experience level.

INSTRUCTIONS:
- Generate 3-5 relevant technical questions
- Adjust difficulty based on experience level (fresher/junior/mid/senior)
- Focus on practical application, not just theory, only 1 theory question allowed
- Questions should assess real-world problem-solving
- Allow follow-up questions for clarification, if you dont get the answer properly,but be concise
- Be encouraging and supportive

QUESTION TYPES:
- real life scenario based problems
- Best practices and design patterns
- Debugging and troubleshooting
- you should know what are the common interview questions for which role the candidate is applying, and ask questions based on that role only
- no out of role and out of context questions should be asked

TONE: Professional, encouraging, technically focused, concise
""",

    "fallback": """
You are TalentScout's hiring assistant. The conversation has gone off-topic.

INSTRUCTIONS:
- Politely redirect back to the hiring process
- Acknowledge their input but stay focused
- Remind them of the current stage in the process
- Be helpful but maintain professional boundaries
- If they want to end, be graceful

TONE: Professional, redirective but kind, concise
""",

    "summary": """
You are wrapping up the TalentScout screening interview.

INSTRUCTIONS:
- Thank the candidate for their patience and Information provided
- Summarize what was collected/discussed
- Ask the candidate if they have any questions to ask you, Offer to answer any final questions 
- If the candidate has any final questions, respond to them thoughtfully and professionally, like an HR would. If they have no further questions, 
- Thank the candidate for their time and say It was great speaking with you today.
- Explain next steps in the hiring process
- Provide timeline expectations
- End on a positive, professional note

- after wrapped up, youre last message should belike, 
TONE: Professional, appreciative, positive
"""
}

# Question generation templates

QUESTION_TEMPLATES = {
    "data_analyst": {
        "junior": [
            "Explain the difference between INNER JOIN and LEFT JOIN in SQL with an example.",
            "How would you clean and preprocess a dataset with missing values?",
            "What are some common data visualization best practices?",
            "How would you calculate year-over-year growth in SQL or Excel?",
            "Explain the difference between a primary key and a foreign key."
        ],
        "mid": [
            "How would you design a dashboard to track business KPIs for management?",
            "Explain the difference between a clustered and non-clustered index in SQL.",
            "How would you handle inconsistent date formats in a dataset?",
            "Explain window functions in SQL and give an example.",
            "How do you choose the right chart type for different data types?"
        ]
    },
    
    "data_scientist": {
        "junior": [
            "What is the difference between supervised and unsupervised learning?",
            "How do you handle imbalanced datasets in classification problems?",
            "Explain the concept of overfitting and how to prevent it.",
            "What evaluation metrics would you use for a regression model?",
            "Explain the difference between precision and recall."
        ],
        "mid": [
            "How would you select features for a predictive model?",
            "Explain cross-validation and why it’s important.",
            "How would you handle multicollinearity in a dataset?",
            "Explain how you would deploy a trained ML model to production.",
            "Describe how you would design an A/B test for a new product feature."
        ]
    },
    
    "sql_developer": {
        "junior": [
            "Explain the difference between WHERE and HAVING clauses in SQL.",
            "What are indexes in SQL and why are they used?",
            "Write a query to find the second highest salary from an Employee table.",
            "Explain the concept of normalization in databases.",
            "What is the difference between DELETE, TRUNCATE, and DROP?"
        ],
        "mid": [
            "How would you optimize a slow SQL query?",
            "Explain CTE (Common Table Expressions) and when to use them.",
            "How would you design a database schema for an e-commerce system?",
            "Explain the difference between OLTP and OLAP databases.",
            "Describe how you would handle database partitioning."
        ]
    },
    
    "powerbi_developer": {
        "junior": [
            "Explain the difference between calculated columns and measures in Power BI.",
            "What are slicers and filters in Power BI and when to use them?",
            "How would you connect Power BI to a SQL Server database?",
            "Explain the difference between import mode and direct query mode.",
            "What is the purpose of Power Query in Power BI?"
        ],
        "mid": [
            "How would you optimize a slow Power BI dashboard?",
            "Explain DAX functions with an example.",
            "How would you implement row-level security in Power BI?",
            "Explain the difference between star schema and snowflake schema.",
            "How do you schedule automatic data refreshes in Power BI?"
        ]
    },
    
    "data_engineer": {
        "junior": [
            "Explain the difference between ETL and ELT.",
            "What are some common data formats used in big data systems?",
            "How would you design a basic data pipeline?",
            "Explain batch processing vs. stream processing.",
            "What are primary considerations for storing raw vs. processed data?"
        ],
        "mid": [
            "How would you optimize a large-scale data pipeline?",
            "Explain the role of Apache Spark in big data processing.",
            "Describe how you would handle schema evolution in a data lake.",
            "How would you ensure data quality in an ingestion pipeline?",
            "Explain partitioning and bucketing in distributed data systems."
        ]
    },
    
    "ml_engineer": {
        "junior": [
            "What is the difference between training and inference in ML?",
            "Explain the purpose of a validation set in model training.",
            "How do you handle categorical variables in ML?",
            "What is the difference between logistic regression and linear regression?",
            "Explain the purpose of a confusion matrix."
        ],
        "mid": [
            "How would you deploy a machine learning model in production?",
            "Explain the concept of model drift and how to detect it.",
            "How would you choose between different ML algorithms for a problem?",
            "Explain how you would monitor the performance of a deployed model.",
            "Describe how you would build a scalable model serving architecture."
        ]
    },
    
    "ai_ml_engineer": {
        "junior": [
            "Explain the difference between AI, ML, and Deep Learning.",
            "What are neural networks and how do they work?",
            "Explain the concept of activation functions in neural networks.",
            "What is transfer learning and when would you use it?",
            "Explain the purpose of embeddings in NLP."
        ],
        "mid": [
            "How would you fine-tune a pre-trained deep learning model?",
            "Explain how transformers work in NLP.",
            "Describe how you would implement an object detection system.",
            "How would you scale AI model training for large datasets?",
            "Explain the challenges of deploying AI systems in production."
        ]
    },
    
    "ai_engineer": {
        "junior": [
            "What is AI and how is it different from traditional programming?",
            "Explain rule-based AI vs. learning-based AI.",
            "What is the purpose of a knowledge graph?",
            "Explain the concept of natural language understanding.",
            "What are some ethical considerations in AI development?"
        ],
        "mid": [
            "How would you design an AI-powered recommendation system?",
            "Explain the concept of reinforcement learning.",
            "Describe how you would integrate AI into an existing business workflow.",
            "How would you ensure fairness and bias mitigation in AI models?",
            "Explain the challenges of explainable AI (XAI)."
        ]
    }
}



# Sentiment analysis prompts
SENTIMENT_PROMPTS = {
    "analyze": """
Analyze the sentiment of the following candidate response during a job interview.
Consider factors like:
- Confidence level
- Enthusiasm
- Clarity of communication
- Professional tone
- Engagement level

Response: {response}

Provide a sentiment score from -1 (very negative) to 1 (very positive) and a brief explanation.
"""
}
