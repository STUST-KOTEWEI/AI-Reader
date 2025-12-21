"""
Tests for Emotion Analyzer Module
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from holo.nlp.emotion_analyzer import EmotionAnalyzer, analyze_emotion


class TestEmotionAnalyzer:
    """Test cases for EmotionAnalyzer."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.analyzer = EmotionAnalyzer()
    
    def test_initialization(self):
        """Test analyzer initialization."""
        assert self.analyzer is not None
        assert self.analyzer.emotion_patterns is not None
    
    def test_analyze_happy_text(self):
        """Test analysis of happy text."""
        text = "I am so happy and delighted today! This is wonderful!"
        result = self.analyzer.analyze(text)
        
        assert result["primary_emotion"] == "joy"
        assert result["confidence"] > 0
        assert "emotions" in result
        assert result["emotions"]["joy"] > 0
    
    def test_analyze_sad_text(self):
        """Test analysis of sad text."""
        text = "I feel so sad and lonely. This is depressing."
        result = self.analyzer.analyze(text)
        
        assert result["primary_emotion"] == "sadness"
        assert result["emotions"]["sadness"] > 0
    
    def test_analyze_angry_text(self):
        """Test analysis of angry text."""
        text = "I am so angry and furious! This is outrageous!"
        result = self.analyzer.analyze(text)
        
        assert result["primary_emotion"] == "anger"
        assert result["emotions"]["anger"] > 0
    
    def test_analyze_fear_text(self):
        """Test analysis of fearful text."""
        text = "I am afraid and scared. This is terrifying."
        result = self.analyzer.analyze(text)
        
        assert result["primary_emotion"] == "fear"
        assert result["emotions"]["fear"] > 0
    
    def test_analyze_surprise_text(self):
        """Test analysis of surprised text."""
        text = "I am shocked and amazed! This is incredible!"
        result = self.analyzer.analyze(text)
        
        assert result["primary_emotion"] == "surprise"
        assert result["emotions"]["surprise"] > 0
    
    def test_analyze_empty_text(self):
        """Test analysis of empty text."""
        result = self.analyzer.analyze("")
        
        assert result["primary_emotion"] == "neutral"
        assert result["confidence"] == 0.0
    
    def test_analyze_neutral_text(self):
        """Test analysis of neutral text."""
        text = "The weather is cloudy today."
        result = self.analyzer.analyze(text)
        
        assert result["primary_emotion"] == "neutral"
    
    def test_sentiment_polarity(self):
        """Test sentiment polarity calculation."""
        positive_text = "I am happy and excited!"
        negative_text = "I am sad and angry."
        
        positive_result = self.analyzer.analyze(positive_text)
        negative_result = self.analyzer.analyze(negative_text)
        
        assert positive_result["sentiment"]["polarity"] > 0
        assert negative_result["sentiment"]["polarity"] < 0
    
    def test_intensity_with_exclamations(self):
        """Test intensity with exclamation marks."""
        mild_text = "I am happy."
        intense_text = "I am happy! So happy! Very very happy!"
        
        mild_result = self.analyzer.analyze(mild_text)
        intense_result = self.analyzer.analyze(intense_text)
        
        assert intense_result["intensity"] > mild_result["intensity"]
    
    def test_intensity_with_intensifiers(self):
        """Test intensity with intensifier words."""
        text = "I am extremely very incredibly happy!"
        result = self.analyzer.analyze(text)
        
        assert result["intensity"] > 0.5
    
    def test_chinese_text(self):
        """Test analysis of Chinese text."""
        text = "我今天很開心，非常快樂！"
        result = self.analyzer.analyze(text)
        
        assert "joy" in result["emotions"]
    
    def test_detailed_analysis(self):
        """Test detailed analysis mode."""
        text = "I am very happy and excited!"
        result = self.analyzer.analyze(text, detailed=True)
        
        assert "keyword_counts" in result
        assert "text_length" in result
        assert "has_negation" in result
        assert "has_intensifier" in result
    
    def test_get_emotion_for_haptics(self):
        """Test emotion mapping for haptic feedback."""
        text = "I am so excited and thrilled!"
        emotion, intensity = self.analyzer.get_emotion_for_haptics(text)
        
        assert emotion in ["happy", "sad", "tense", "calm", "surprised", "excited"]
        assert 0 <= intensity <= 1
    
    def test_convenience_function(self):
        """Test the convenience function."""
        result = analyze_emotion("I am happy!")
        
        assert "primary_emotion" in result
        assert "confidence" in result
        assert "emotions" in result
