"""
LLM Handler for Groq API Integration
"""

import os
from typing import Dict, List, Optional, Any
from groq import Groq
import streamlit as st
from src.config.prompts import SYSTEM_PROMPTS
from src.config.settings import AppConfig

class LLMHandler:
    """Handles all LLM interactions using Groq API"""
    
    def __init__(self, config: AppConfig):
        self.config = config
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Groq client"""
        try:
            self.client = Groq(api_key=self.config.groq_api_key)
        except Exception as e:
            st.error(f"Failed to initialize Groq client: {str(e)}")
            raise e
    
    def generate_response(
        self, 
        prompt: str, 
        context_type: str = "greeting",
        conversation_history: Optional[List[Dict]] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """Generate response using Groq LLM"""
        try:
            # Get system prompt based on context
            system_prompt = SYSTEM_PROMPTS.get(context_type, SYSTEM_PROMPTS["greeting"])
            
            # Build messages
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add conversation history if provided
            if conversation_history:
                for msg in conversation_history[-5:]:  # Last 5 messages for context
                    if msg.get("role") in ["user", "assistant"]:
                        messages.append({
                            "role": msg["role"],
                            "content": msg["content"]
                        })
            
            # Add current prompt
            messages.append({"role": "user", "content": prompt})
            
            # Make API call
            response = self.client.chat.completions.create(
                model=self.config.groq_model,
                messages=messages,
                temperature=self.config.groq_temperature,
                max_tokens=max_tokens or self.config.groq_max_tokens,
                stream=False
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            st.error(f"LLM generation failed: {str(e)}")
            return self._get_fallback_response(context_type)
    
    def generate_technical_questions(
        self, 
        tech_stack: List[str], 
        experience_level: str,
        num_questions: int = 3
    ) -> List[str]:
        """Generate technical questions based on tech stack and experience"""
        try:
            tech_stack_str = ", ".join(tech_stack)
            
            prompt = f"""
Generate {num_questions} technical interview questions for a candidate with:
- Tech Stack: {tech_stack_str}
- Experience Level: {experience_level}

Requirements:
1. Questions should be practical and scenario-based
2. Adjust difficulty for {experience_level} level
3. Focus on real-world problem-solving
4. Each question should be clear and specific
5. Avoid yes/no questions

Format: Return only the questions, numbered 1, 2, 3, etc.
"""
            
            response = self.generate_response(
                prompt=prompt,
                context_type="tech_questions",
                max_tokens=800
            )
            
            # Parse questions from response
            questions = []
            lines = response.split('\n')
            
            for line in lines:
                line = line.strip()
                if line and (line.startswith(('1.', '2.', '3.', '4.', '5.')) or 
                           line.startswith(('Q1', 'Q2', 'Q3', 'Q4', 'Q5'))):
                    # Remove numbering and clean up
                    question = line.split('.', 1)[-1].strip()
                    if question:
                        questions.append(question)
            
            # Fallback if parsing failed
            if not questions:
                questions = self._get_fallback_questions(tech_stack, experience_level)
            
            return questions[:num_questions]
            
        except Exception as e:
            st.error(f"Failed to generate technical questions: {str(e)}")
            return self._get_fallback_questions(tech_stack, experience_level)
    
    def analyze_response_quality(self, question: str, response: str) -> Dict[str, Any]:
        """Analyze the quality of a candidate's response"""
        try:
            prompt = f"""
Analyze this candidate's response to a technical interview question:

Question: {question}
Response: {response}

Provide analysis on:
1. Technical accuracy (if applicable)
2. Clarity of explanation
3. Depth of understanding
4. Communication skills

Return a brief assessment and a score from 1-10.
"""
            
            analysis = self.generate_response(
                prompt=prompt,
                context_type="tech_questions",
                max_tokens=300
            )
            
            # Extract score if possible
            score = 5  # Default score
            if "score" in analysis.lower():
                import re
                score_match = re.search(r'(\d+)/10|score.*?(\d+)', analysis.lower())
                if score_match:
                    score = int(score_match.group(1) or score_match.group(2))
            
            return {
                "analysis": analysis,
                "score": score,
                "timestamp": st.session_state.get('current_time', '')
            }
            
        except Exception as e:
            st.error(f"Failed to analyze response: {str(e)}")
            return {
                "analysis": "Unable to analyze response at this time.",
                "score": 5,
                "timestamp": ""
            }
    
    def extract_information(self, text: str, field_type: str) -> Optional[str]:
        """Extract specific information from natural language text"""
        try:
            prompt = f"""
Extract the {field_type} from this text. Return only the extracted value, nothing else.

Text: {text}
Field to extract: {field_type}

If no {field_type} is found, return "NOT_FOUND".
"""
            
            response = self.generate_response(
                prompt=prompt,
                context_type="info_collection",
                max_tokens=100
            )
            
            if response.strip().upper() == "NOT_FOUND":
                return None
            
            return response.strip()
            
        except Exception as e:
            return None
    
    def _get_fallback_response(self, context_type: str) -> str:
        """Get fallback response when LLM fails"""
        fallbacks = {
            "greeting": "Hello! I'm TalentScout's hiring assistant. I'm here to help with your application process. How can I assist you today?",
            "info_collection": "I'd be happy to help collect your information. Could you please provide the details I requested?",
            "tech_questions": "Let me ask you a technical question to better understand your skills.",
            "summary": "Thank you for your time today. We'll review your information and get back to you soon.",
            "fallback": "I apologize, but I'm having some technical difficulties. Let's continue with the interview process."
        }
        
        return fallbacks.get(context_type, fallbacks["fallback"])
    
    def _get_fallback_questions(self, tech_stack: List[str], experience_level: str) -> List[str]:
        """Get fallback technical questions when generation fails"""
        
        # Basic questions based on common technologies
        questions_map = {
            "python": [
                "How would you handle exceptions in a Python application?",
                "Explain the difference between lists and tuples in Python.",
                "How do you optimize Python code for better performance?"
            ],
            "javascript": [
                "What's the difference between let, const, and var in JavaScript?",
                "How do you handle asynchronous operations in JavaScript?",
                "Explain event bubbling and how to prevent it."
            ],
            "react": [
                "What are React hooks and why are they useful?",
                "How do you handle state management in React?",
                "Explain the component lifecycle in React."
            ],
            "java": [
                "What's the difference between abstract classes and interfaces in Java?",
                "How does garbage collection work in Java?",
                "Explain the concept of multithreading in Java."
            ]
        }
        
        # Find relevant questions
        questions = []
        for tech in tech_stack:
            tech_lower = tech.lower()
            if tech_lower in questions_map:
                questions.extend(questions_map[tech_lower])
        
        # Generic fallback questions
        if not questions:
            questions = [
                "Describe a challenging technical problem you've solved recently.",
                "How do you approach debugging when something isn't working?",
                "What's your process for learning new technologies?"
            ]
        
        return questions[:3]
    
    def check_conversation_end_intent(self, text: str) -> bool:
        """Check if user wants to end the conversation"""
        # Only trigger on very specific end phrases, not common words
        end_keywords = [
            "bye", "goodbye", "exit", "quit"
        ]
        
        text_lower = text.lower().strip()
        
        # Check for exact matches only (not partial matches)
        for keyword in end_keywords:
            if text_lower == keyword or text_lower.startswith(keyword + " ") or text_lower.endswith(" " + keyword):
                return True
        
        # Check for very specific end phrases only
        end_phrases = [
            "i'm done with the interview", "end the interview", "stop the interview",
            "i want to quit", "i want to exit", "finish the interview"
        ]
        
        for phrase in end_phrases:
            if phrase in text_lower:
                return True
        
        return False
    
    def generate_summary(self, session_data: Dict[str, Any]) -> str:
        """Generate a summary of the interview session"""
        try:
            candidate_info = session_data.get('candidate_info', {})
            
            prompt = f"""
Generate a professional summary for this candidate interview:

Candidate: {candidate_info.get('full_name', 'N/A')}
Experience: {candidate_info.get('experience_years', 'N/A')} years
Tech Stack: {', '.join(candidate_info.get('tech_stack', []))}
Position: {', '.join(candidate_info.get('desired_positions', []))}

Create a brief, professional summary highlighting:
1. Key qualifications
2. Technical skills
3. Experience level
4. Overall assessment

Keep it concise and professional.
"""
            
            return self.generate_response(
                prompt=prompt,
                context_type="summary",
                max_tokens=400
            )
            
        except Exception as e:
            return f"Interview completed for {candidate_info.get('full_name', 'candidate')}. All information has been collected successfully."
