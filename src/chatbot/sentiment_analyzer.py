"""
Sentiment Analysis Module for TalentScout Hiring Assistant
"""

from typing import Dict, Any, Optional
import streamlit as st
from textblob import TextBlob
from src.data.models import SentimentAnalysis

class SentimentAnalyzer:
    """Handles sentiment analysis of candidate responses"""
    
    def __init__(self):
        self.confidence_threshold = 0.1  # Minimum confidence for sentiment classification
    
    def analyze_sentiment(self, text: str) -> SentimentAnalysis:
        """Analyze sentiment of given text"""
        try:
            # Use TextBlob for sentiment analysis
            blob = TextBlob(text)
            
            # Get polarity (-1 to 1) and subjectivity (0 to 1)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Determine sentiment label
            if polarity > self.confidence_threshold:
                sentiment_label = "positive"
            elif polarity < -self.confidence_threshold:
                sentiment_label = "negative"
            else:
                sentiment_label = "neutral"
            
            # Calculate confidence based on absolute polarity
            confidence = min(abs(polarity) + 0.5, 1.0)
            
            return SentimentAnalysis(
                text=text,
                sentiment_score=polarity,
                sentiment_label=sentiment_label,
                confidence=confidence
            )
            
        except Exception as e:
            st.error(f"Sentiment analysis failed: {str(e)}")
            return self._get_fallback_sentiment(text)
    
    def analyze_conversation_sentiment(self, messages: list) -> Dict[str, Any]:
        """Analyze overall conversation sentiment"""
        try:
            user_messages = [msg for msg in messages if msg.get("role") == "user"]
            
            if not user_messages:
                return {
                    "overall_sentiment": "neutral",
                    "sentiment_score": 0.0,
                    "confidence": 0.0,
                    "message_count": 0,
                    "sentiment_trend": "stable"
                }
            
            # Analyze each user message
            sentiments = []
            scores = []
            
            for msg in user_messages:
                content = msg.get("content", "")
                if content.strip():
                    analysis = self.analyze_sentiment(content)
                    sentiments.append(analysis.sentiment_label)
                    scores.append(analysis.sentiment_score)
            
            if not scores:
                return self._get_neutral_analysis()
            
            # Calculate overall metrics
            avg_score = sum(scores) / len(scores)
            
            # Determine overall sentiment
            if avg_score > 0.1:
                overall_sentiment = "positive"
            elif avg_score < -0.1:
                overall_sentiment = "negative"
            else:
                overall_sentiment = "neutral"
            
            # Calculate sentiment trend
            sentiment_trend = self._calculate_trend(scores)
            
            # Calculate confidence
            confidence = min(abs(avg_score) + 0.3, 1.0)
            
            return {
                "overall_sentiment": overall_sentiment,
                "sentiment_score": avg_score,
                "confidence": confidence,
                "message_count": len(scores),
                "sentiment_trend": sentiment_trend,
                "individual_scores": scores
            }
            
        except Exception as e:
            st.error(f"Conversation sentiment analysis failed: {str(e)}")
            return self._get_neutral_analysis()
    
    def _calculate_trend(self, scores: list) -> str:
        """Calculate sentiment trend over the conversation"""
        if len(scores) < 2:
            return "stable"
        
        # Compare first half with second half
        mid_point = len(scores) // 2
        first_half_avg = sum(scores[:mid_point]) / mid_point if mid_point > 0 else 0
        second_half_avg = sum(scores[mid_point:]) / (len(scores) - mid_point)
        
        difference = second_half_avg - first_half_avg
        
        if difference > 0.2:
            return "improving"
        elif difference < -0.2:
            return "declining"
        else:
            return "stable"
    
    def get_sentiment_insights(self, sentiment_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate insights based on sentiment analysis"""
        try:
            overall_sentiment = sentiment_data.get("overall_sentiment", "neutral")
            sentiment_score = sentiment_data.get("sentiment_score", 0.0)
            trend = sentiment_data.get("sentiment_trend", "stable")
            confidence = sentiment_data.get("confidence", 0.0)
            
            insights = {}
            
            # Overall assessment
            if overall_sentiment == "positive":
                insights["engagement"] = "High - Candidate shows positive engagement"
                insights["communication"] = "Good - Responses indicate confidence and enthusiasm"
            elif overall_sentiment == "negative":
                insights["engagement"] = "Low - Candidate may be disengaged or stressed"
                insights["communication"] = "Concerning - May indicate nervousness or dissatisfaction"
            else:
                insights["engagement"] = "Moderate - Neutral engagement level"
                insights["communication"] = "Standard - Professional but not particularly enthusiastic"
            
            # Trend analysis
            if trend == "improving":
                insights["progression"] = "Positive - Candidate became more comfortable during interview"
            elif trend == "declining":
                insights["progression"] = "Concerning - Candidate engagement decreased over time"
            else:
                insights["progression"] = "Stable - Consistent engagement throughout interview"
            
            # Confidence assessment
            if confidence > 0.7:
                insights["reliability"] = "High - Sentiment analysis is highly confident"
            elif confidence > 0.4:
                insights["reliability"] = "Moderate - Sentiment analysis shows reasonable confidence"
            else:
                insights["reliability"] = "Low - Sentiment analysis has limited confidence"
            
            # Recommendations
            if overall_sentiment == "positive" and trend in ["improving", "stable"]:
                insights["recommendation"] = "Proceed - Candidate shows good engagement and communication"
            elif overall_sentiment == "negative" or trend == "declining":
                insights["recommendation"] = "Review - Consider additional screening or follow-up"
            else:
                insights["recommendation"] = "Standard - Continue with normal evaluation process"
            
            return insights
            
        except Exception as e:
            return {"error": f"Failed to generate insights: {str(e)}"}
    
    def _get_fallback_sentiment(self, text: str) -> SentimentAnalysis:
        """Get fallback sentiment when analysis fails"""
        return SentimentAnalysis(
            text=text,
            sentiment_score=0.0,
            sentiment_label="neutral",
            confidence=0.0
        )
    
    def _get_neutral_analysis(self) -> Dict[str, Any]:
        """Get neutral analysis when conversation analysis fails"""
        return {
            "overall_sentiment": "neutral",
            "sentiment_score": 0.0,
            "confidence": 0.0,
            "message_count": 0,
            "sentiment_trend": "stable"
        }
    
    def format_sentiment_for_display(self, sentiment_data: Dict[str, Any]) -> str:
        """Format sentiment data for display in UI"""
        try:
            sentiment = sentiment_data.get("overall_sentiment", "neutral")
            score = sentiment_data.get("sentiment_score", 0.0)
            trend = sentiment_data.get("sentiment_trend", "stable")
            
            # Create emoji representation
            emoji_map = {
                "positive": "😊",
                "negative": "😟",
                "neutral": "😐"
            }
            
            trend_map = {
                "improving": "📈",
                "declining": "📉",
                "stable": "➡️"
            }
            
            emoji = emoji_map.get(sentiment, "😐")
            trend_emoji = trend_map.get(trend, "➡️")
            
            return f"{emoji} {sentiment.title()} ({score:.2f}) {trend_emoji} {trend.title()}"
            
        except Exception:
            return "😐 Neutral (0.00) ➡️ Stable"
    
    def is_positive_response(self, text: str, threshold: float = 0.1) -> bool:
        """Check if response is positive (for quick validation)"""
        try:
            analysis = self.analyze_sentiment(text)
            return analysis.sentiment_score > threshold
        except Exception:
            return False
    
    def detect_emotional_state(self, text: str) -> str:
        """Detect emotional state from text"""
        try:
            # Keywords for different emotional states
            emotions = {
                "excited": ["excited", "thrilled", "amazing", "fantastic", "love", "passionate"],
                "nervous": ["nervous", "worried", "anxious", "scared", "uncertain"],
                "confident": ["confident", "sure", "certain", "definitely", "absolutely"],
                "frustrated": ["frustrated", "annoyed", "difficult", "hard", "struggle"],
                "curious": ["interesting", "curious", "wonder", "learn", "explore"]
            }
            
            text_lower = text.lower()
            emotion_scores = {}
            
            for emotion, keywords in emotions.items():
                score = sum(1 for keyword in keywords if keyword in text_lower)
                if score > 0:
                    emotion_scores[emotion] = score
            
            if emotion_scores:
                return max(emotion_scores, key=emotion_scores.get)
            else:
                return "neutral"
                
        except Exception:
            return "neutral"
