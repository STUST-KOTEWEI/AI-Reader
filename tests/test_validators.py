"""
Tests for Validators Module
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from holo.utils.validators import (
    validate_text_input,
    validate_intensity,
    validate_haptic_pattern,
    validate_haptic_event,
    validate_emotion,
    validate_strategy,
    ValidationError
)


class TestValidateTextInput:
    """Test cases for validate_text_input."""
    
    def test_valid_text(self):
        """Test validation of valid text."""
        result = validate_text_input("Hello world")
        assert result == "Hello world"
    
    def test_text_with_whitespace(self):
        """Test that whitespace is stripped."""
        result = validate_text_input("  Hello world  ")
        assert result == "Hello world"
    
    def test_empty_text_allowed(self):
        """Test empty text when allowed."""
        result = validate_text_input("", allow_empty=True)
        assert result == ""
    
    def test_empty_text_not_allowed(self):
        """Test empty text when not allowed."""
        with pytest.raises(ValidationError):
            validate_text_input("", allow_empty=False)
    
    def test_none_allowed(self):
        """Test None when empty is allowed."""
        result = validate_text_input(None, allow_empty=True)
        assert result == ""
    
    def test_none_not_allowed(self):
        """Test None when empty is not allowed."""
        with pytest.raises(ValidationError):
            validate_text_input(None, allow_empty=False)
    
    def test_non_string_input(self):
        """Test non-string input."""
        with pytest.raises(ValidationError):
            validate_text_input(123)
    
    def test_min_length(self):
        """Test minimum length validation."""
        with pytest.raises(ValidationError):
            validate_text_input("Hi", min_length=5)
    
    def test_max_length(self):
        """Test maximum length validation."""
        with pytest.raises(ValidationError):
            validate_text_input("Hello world", max_length=5)


class TestValidateIntensity:
    """Test cases for validate_intensity."""
    
    def test_valid_intensity(self):
        """Test validation of valid intensity."""
        result = validate_intensity(0.5)
        assert result == 0.5
    
    def test_intensity_zero(self):
        """Test intensity at zero."""
        result = validate_intensity(0.0)
        assert result == 0.0
    
    def test_intensity_one(self):
        """Test intensity at one."""
        result = validate_intensity(1.0)
        assert result == 1.0
    
    def test_intensity_integer(self):
        """Test integer intensity."""
        result = validate_intensity(1)
        assert result == 1.0
    
    def test_intensity_too_low(self):
        """Test intensity below minimum."""
        with pytest.raises(ValidationError):
            validate_intensity(-0.1)
    
    def test_intensity_too_high(self):
        """Test intensity above maximum."""
        with pytest.raises(ValidationError):
            validate_intensity(1.5)
    
    def test_intensity_none(self):
        """Test None intensity."""
        with pytest.raises(ValidationError):
            validate_intensity(None)
    
    def test_intensity_non_number(self):
        """Test non-numeric intensity."""
        with pytest.raises(ValidationError):
            validate_intensity("high")


class TestValidateHapticPattern:
    """Test cases for validate_haptic_pattern."""
    
    def test_valid_pattern(self):
        """Test validation of valid pattern."""
        pattern = {
            "name": "test",
            "events": [
                {"time": 0, "intensity": 0.5, "duration": 100}
            ]
        }
        result = validate_haptic_pattern(pattern)
        assert result == pattern
    
    def test_pattern_missing_name(self):
        """Test pattern missing name."""
        pattern = {
            "events": []
        }
        with pytest.raises(ValidationError):
            validate_haptic_pattern(pattern)
    
    def test_pattern_missing_events(self):
        """Test pattern missing events."""
        pattern = {
            "name": "test"
        }
        with pytest.raises(ValidationError):
            validate_haptic_pattern(pattern)
    
    def test_pattern_not_dict(self):
        """Test non-dict pattern."""
        with pytest.raises(ValidationError):
            validate_haptic_pattern("pattern")
    
    def test_pattern_empty_name(self):
        """Test empty pattern name."""
        pattern = {
            "name": "",
            "events": []
        }
        with pytest.raises(ValidationError):
            validate_haptic_pattern(pattern)


class TestValidateHapticEvent:
    """Test cases for validate_haptic_event."""
    
    def test_valid_event(self):
        """Test validation of valid event."""
        event = {"time": 0, "intensity": 0.5, "duration": 100}
        result = validate_haptic_event(event)
        assert result == event
    
    def test_event_missing_time(self):
        """Test event missing time."""
        event = {"intensity": 0.5, "duration": 100}
        with pytest.raises(ValidationError):
            validate_haptic_event(event)
    
    def test_event_negative_time(self):
        """Test event with negative time."""
        event = {"time": -1, "intensity": 0.5, "duration": 100}
        with pytest.raises(ValidationError):
            validate_haptic_event(event)
    
    def test_event_invalid_intensity(self):
        """Test event with invalid intensity."""
        event = {"time": 0, "intensity": 1.5, "duration": 100}
        with pytest.raises(ValidationError):
            validate_haptic_event(event)
    
    def test_event_negative_duration(self):
        """Test event with negative duration."""
        event = {"time": 0, "intensity": 0.5, "duration": -100}
        with pytest.raises(ValidationError):
            validate_haptic_event(event)


class TestValidateEmotion:
    """Test cases for validate_emotion."""
    
    def test_valid_emotion(self):
        """Test validation of valid emotion."""
        result = validate_emotion("happy")
        assert result == "happy"
    
    def test_emotion_uppercase(self):
        """Test emotion is lowercased."""
        result = validate_emotion("HAPPY")
        assert result == "happy"
    
    def test_emotion_with_whitespace(self):
        """Test emotion whitespace is stripped."""
        result = validate_emotion("  happy  ")
        assert result == "happy"
    
    def test_emotion_none(self):
        """Test None emotion."""
        with pytest.raises(ValidationError):
            validate_emotion(None)
    
    def test_emotion_empty(self):
        """Test empty emotion."""
        with pytest.raises(ValidationError):
            validate_emotion("")
    
    def test_emotion_invalid_with_list(self):
        """Test invalid emotion with valid list."""
        with pytest.raises(ValidationError):
            validate_emotion("unknown", valid_emotions=["happy", "sad"])
    
    def test_emotion_valid_with_list(self):
        """Test valid emotion with valid list."""
        result = validate_emotion("happy", valid_emotions=["happy", "sad"])
        assert result == "happy"


class TestValidateStrategy:
    """Test cases for validate_strategy."""
    
    def test_valid_strategy(self):
        """Test validation of valid strategy."""
        result = validate_strategy("adaptive", ["sentences", "paragraphs", "adaptive"])
        assert result == "adaptive"
    
    def test_invalid_strategy(self):
        """Test invalid strategy."""
        with pytest.raises(ValidationError):
            validate_strategy("unknown", ["sentences", "paragraphs"])
    
    def test_strategy_none(self):
        """Test None strategy."""
        with pytest.raises(ValidationError):
            validate_strategy(None, ["sentences"])


class TestValidationError:
    """Test cases for ValidationError."""
    
    def test_error_message(self):
        """Test error message."""
        error = ValidationError("Test error")
        assert error.message == "Test error"
        assert str(error) == "Test error"
    
    def test_error_field(self):
        """Test error field."""
        error = ValidationError("Test error", field="test_field")
        assert error.field == "test_field"
    
    def test_to_dict(self):
        """Test to_dict method."""
        error = ValidationError("Test error", field="test_field")
        result = error.to_dict()
        
        assert result["error"] == "Test error"
        assert result["field"] == "test_field"
