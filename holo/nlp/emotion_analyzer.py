"""
Emotion Analyzer Module

Analyzes text to detect emotions, sentiment, and emotional intensity.
Uses keyword-based analysis with support for multiple languages.
"""

import re
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class EmotionResult:
    """Result of emotion analysis."""
    primary_emotion: str
    confidence: float
    emotions: Dict[str, float]
    sentiment: Dict[str, float]
    intensity: float


class EmotionAnalyzer:
    """
    Analyzes emotional content in text.
    
    Uses keyword-based analysis to detect emotions and sentiment.
    Supports English and Chinese text.
    """
    
    # Emotion keywords with associated weights
    EMOTION_KEYWORDS = {
        "joy": {
            "en": ["happy", "joy", "delight", "excited", "thrilled", "wonderful", 
                   "amazing", "great", "love", "fantastic", "excellent", "cheerful",
                   "elated", "pleased", "glad", "content", "smile", "laugh"],
            "zh": ["開心", "快樂", "高興", "歡喜", "幸福", "愉快", "興奮", "棒"]
        },
        "sadness": {
            "en": ["sad", "unhappy", "depressed", "sorrow", "grief", "miserable",
                   "heartbroken", "devastated", "lonely", "melancholy", "gloomy",
                   "despair", "hopeless", "cry", "tears", "mourn"],
            "zh": ["悲傷", "難過", "傷心", "沮喪", "憂鬱", "哀傷", "痛苦", "哭"]
        },
        "anger": {
            "en": ["angry", "furious", "rage", "mad", "irritated", "annoyed",
                   "outraged", "hostile", "bitter", "resentful", "frustrated",
                   "hate", "loathe", "despise"],
            "zh": ["生氣", "憤怒", "惱怒", "氣憤", "火大", "討厭", "恨"]
        },
        "fear": {
            "en": ["afraid", "scared", "terrified", "fearful", "anxious", "worried",
                   "nervous", "panic", "dread", "horror", "frightened", "alarmed",
                   "uneasy", "threatened"],
            "zh": ["害怕", "恐懼", "擔心", "焦慮", "緊張", "驚恐", "不安"]
        },
        "surprise": {
            "en": ["surprised", "shocked", "amazed", "astonished", "stunned",
                   "startled", "unexpected", "incredible", "unbelievable",
                   "wonder", "awe"],
            "zh": ["驚訝", "震驚", "意外", "吃驚", "驚奇", "驚嘆"]
        },
        "disgust": {
            "en": ["disgusted", "revolted", "repulsed", "sick", "nauseated",
                   "gross", "awful", "terrible", "horrible", "unpleasant"],
            "zh": ["噁心", "厭惡", "反感", "討厭", "作嘔"]
        }
    }
    
    # Sentiment intensifiers
    INTENSIFIERS = {
        "en": ["very", "extremely", "incredibly", "absolutely", "totally", 
               "completely", "so", "really", "quite", "truly"],
        "zh": ["非常", "極度", "超級", "十分", "太"]
    }
    
    # Negation words
    NEGATIONS = {
        "en": ["not", "no", "never", "neither", "none", "nobody", "nothing",
               "nowhere", "hardly", "barely", "scarcely", "don't", "doesn't",
               "didn't", "won't", "wouldn't", "couldn't", "shouldn't"],
        "zh": ["不", "沒有", "沒", "別", "未", "無"]
    }
    
    def __init__(self):
        """Initialize the emotion analyzer."""
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile regex patterns for efficient matching."""
        self.emotion_patterns = {}
        for emotion, keywords in self.EMOTION_KEYWORDS.items():
            all_keywords = keywords["en"] + keywords["zh"]
            pattern = r'\b(' + '|'.join(re.escape(k) for k in all_keywords) + r')\b'
            self.emotion_patterns[emotion] = re.compile(pattern, re.IGNORECASE)
        
        all_intensifiers = self.INTENSIFIERS["en"] + self.INTENSIFIERS["zh"]
        self.intensifier_pattern = re.compile(
            r'\b(' + '|'.join(re.escape(i) for i in all_intensifiers) + r')\b',
            re.IGNORECASE
        )
        
        all_negations = self.NEGATIONS["en"] + self.NEGATIONS["zh"]
        self.negation_pattern = re.compile(
            r'\b(' + '|'.join(re.escape(n) for n in all_negations) + r')\b',
            re.IGNORECASE
        )
    
    def analyze(self, text: str, detailed: bool = False) -> Dict[str, Any]:
        """
        Analyze emotional content in text.
        
        Args:
            text: Text to analyze
            detailed: Whether to return detailed analysis
            
        Returns:
            Dictionary containing emotion analysis results
        """
        if not text or not text.strip():
            return self._empty_result()
        
        # Count emotion keywords
        emotion_scores = self._count_emotions(text)
        
        # Calculate sentiment
        sentiment = self._calculate_sentiment(emotion_scores, text)
        
        # Determine intensity
        intensity = self._calculate_intensity(text)
        
        # Find primary emotion
        primary_emotion, confidence = self._get_primary_emotion(emotion_scores)
        
        result = {
            "primary_emotion": primary_emotion,
            "confidence": confidence,
            "emotions": emotion_scores,
            "sentiment": sentiment,
            "intensity": intensity
        }
        
        if detailed:
            result["keyword_counts"] = self._get_keyword_counts(text)
            result["text_length"] = len(text)
            result["has_negation"] = bool(self.negation_pattern.search(text))
            result["has_intensifier"] = bool(self.intensifier_pattern.search(text))
        
        return result
    
    def _count_emotions(self, text: str) -> Dict[str, float]:
        """Count emotion keywords and calculate scores."""
        scores = {}
        total_matches = 0
        
        for emotion, pattern in self.emotion_patterns.items():
            matches = pattern.findall(text)
            scores[emotion] = len(matches)
            total_matches += len(matches)
        
        # Normalize scores
        if total_matches > 0:
            for emotion in scores:
                scores[emotion] = round(scores[emotion] / total_matches, 3)
        
        return scores
    
    def _calculate_sentiment(self, emotion_scores: Dict[str, float], text: str) -> Dict[str, float]:
        """Calculate sentiment polarity and subjectivity."""
        positive_emotions = ["joy", "surprise"]
        negative_emotions = ["sadness", "anger", "fear", "disgust"]
        
        positive_score = sum(emotion_scores.get(e, 0) for e in positive_emotions)
        negative_score = sum(emotion_scores.get(e, 0) for e in negative_emotions)
        
        # Check for negations that might flip sentiment
        negation_count = len(self.negation_pattern.findall(text))
        if negation_count > 0:
            positive_score, negative_score = negative_score * 0.7, positive_score * 0.7
        
        total = positive_score + negative_score
        if total > 0:
            polarity = (positive_score - negative_score) / total
        else:
            polarity = 0.0
        
        # Calculate subjectivity based on emotion presence
        subjectivity = min(1.0, sum(emotion_scores.values()) * 2)
        
        return {
            "polarity": round(polarity, 3),
            "subjectivity": round(subjectivity, 3)
        }
    
    def _calculate_intensity(self, text: str) -> float:
        """Calculate emotional intensity."""
        intensifier_count = len(self.intensifier_pattern.findall(text))
        exclamation_count = text.count('!') + text.count('！')
        uppercase_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        
        # Base intensity from modifiers
        intensity = 0.5 + (intensifier_count * 0.1) + (exclamation_count * 0.05)
        intensity += uppercase_ratio * 0.2
        
        return round(min(1.0, max(0.0, intensity)), 3)
    
    def _get_primary_emotion(self, emotion_scores: Dict[str, float]) -> Tuple[str, float]:
        """Determine the primary emotion and confidence."""
        if not emotion_scores or all(v == 0 for v in emotion_scores.values()):
            return "neutral", 0.5
        
        max_emotion = max(emotion_scores, key=emotion_scores.get)
        max_score = emotion_scores[max_emotion]
        
        if max_score == 0:
            return "neutral", 0.5
        
        # Calculate confidence based on how dominant the primary emotion is
        total_score = sum(emotion_scores.values())
        if total_score > 0:
            confidence = max_score / total_score
        else:
            confidence = 0.0
        
        return max_emotion, round(confidence, 3)
    
    def _get_keyword_counts(self, text: str) -> Dict[str, int]:
        """Get raw keyword counts for detailed analysis."""
        counts = {}
        for emotion, pattern in self.emotion_patterns.items():
            matches = pattern.findall(text)
            counts[emotion] = len(matches)
        return counts
    
    def _empty_result(self) -> Dict[str, Any]:
        """Return empty result for empty input."""
        return {
            "primary_emotion": "neutral",
            "confidence": 0.0,
            "emotions": {emotion: 0.0 for emotion in self.EMOTION_KEYWORDS.keys()},
            "sentiment": {"polarity": 0.0, "subjectivity": 0.0},
            "intensity": 0.0
        }
    
    def get_emotion_for_haptics(self, text: str) -> Tuple[str, float]:
        """
        Get emotion suitable for haptic feedback generation.
        
        Args:
            text: Text to analyze
            
        Returns:
            Tuple of (emotion_name, intensity) suitable for haptics
        """
        result = self.analyze(text)
        
        # Map emotions to haptic-compatible emotions
        haptic_emotion_map = {
            "joy": "happy",
            "sadness": "sad",
            "anger": "tense",
            "fear": "tense",
            "surprise": "surprised",
            "disgust": "calm",  # Default to calm for disgust
            "neutral": "calm"
        }
        
        haptic_emotion = haptic_emotion_map.get(result["primary_emotion"], "calm")
        intensity = result["intensity"]
        
        return haptic_emotion, intensity


def analyze_emotion(text: str, detailed: bool = False) -> Dict[str, Any]:
    """
    Convenience function to analyze emotion in text.
    
    Args:
        text: Text to analyze
        detailed: Whether to return detailed analysis
        
    Returns:
        Emotion analysis results
    """
    analyzer = EmotionAnalyzer()
    return analyzer.analyze(text, detailed)
