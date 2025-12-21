"""
Validators Module

Common validation utilities for Project-HOLO.
Provides consistent input validation across all modules.
"""

from typing import Dict, Any, List, Optional, Union


class ValidationError(Exception):
    """Custom exception for validation errors."""
    
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, str]:
        """Convert error to dictionary format."""
        result = {"error": self.message}
        if self.field:
            result["field"] = self.field
        return result


def validate_text_input(
    text: str,
    min_length: int = 0,
    max_length: int = 100000,
    allow_empty: bool = True,
    field_name: str = "text"
) -> str:
    """
    Validate text input.
    
    Args:
        text: Text to validate
        min_length: Minimum allowed length
        max_length: Maximum allowed length
        allow_empty: Whether to allow empty text
        field_name: Field name for error messages
        
    Returns:
        Validated text (stripped)
        
    Raises:
        ValidationError: If validation fails
    """
    if text is None:
        if not allow_empty:
            raise ValidationError(f"{field_name} is required", field_name)
        return ""
    
    if not isinstance(text, str):
        raise ValidationError(f"{field_name} must be a string", field_name)
    
    text = text.strip()
    
    if not allow_empty and len(text) == 0:
        raise ValidationError(f"{field_name} cannot be empty", field_name)
    
    if len(text) < min_length:
        raise ValidationError(
            f"{field_name} must be at least {min_length} characters",
            field_name
        )
    
    if len(text) > max_length:
        raise ValidationError(
            f"{field_name} must not exceed {max_length} characters",
            field_name
        )
    
    return text


def validate_intensity(
    intensity: Union[int, float],
    min_value: float = 0.0,
    max_value: float = 1.0,
    field_name: str = "intensity"
) -> float:
    """
    Validate intensity value.
    
    Args:
        intensity: Intensity value to validate
        min_value: Minimum allowed value
        max_value: Maximum allowed value
        field_name: Field name for error messages
        
    Returns:
        Validated intensity as float
        
    Raises:
        ValidationError: If validation fails
    """
    if intensity is None:
        raise ValidationError(f"{field_name} is required", field_name)
    
    try:
        intensity = float(intensity)
    except (TypeError, ValueError):
        raise ValidationError(f"{field_name} must be a number", field_name)
    
    if intensity < min_value or intensity > max_value:
        raise ValidationError(
            f"{field_name} must be between {min_value} and {max_value}",
            field_name
        )
    
    return intensity


def validate_haptic_pattern(pattern: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate a haptic pattern structure.
    
    Args:
        pattern: Pattern dictionary to validate
        
    Returns:
        Validated pattern
        
    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(pattern, dict):
        raise ValidationError("Pattern must be a dictionary", "pattern")
    
    # Check required fields
    required_fields = ["name", "events"]
    for field in required_fields:
        if field not in pattern:
            raise ValidationError(f"Pattern must contain '{field}'", field)
    
    # Validate name
    if not isinstance(pattern["name"], str) or len(pattern["name"]) == 0:
        raise ValidationError("Pattern name must be a non-empty string", "name")
    
    # Validate events
    if not isinstance(pattern["events"], list):
        raise ValidationError("Pattern events must be a list", "events")
    
    for i, event in enumerate(pattern["events"]):
        validate_haptic_event(event, f"events[{i}]")
    
    # Validate optional fields
    if "repeat" in pattern and not isinstance(pattern["repeat"], bool):
        raise ValidationError("repeat must be a boolean", "repeat")
    
    if "repeat_interval" in pattern:
        if not isinstance(pattern["repeat_interval"], (int, float)):
            raise ValidationError("repeat_interval must be a number", "repeat_interval")
        if pattern["repeat_interval"] < 0:
            raise ValidationError("repeat_interval must be non-negative", "repeat_interval")
    
    return pattern


def validate_haptic_event(event: Dict[str, Any], field_name: str = "event") -> Dict[str, Any]:
    """
    Validate a single haptic event.
    
    Args:
        event: Event dictionary to validate
        field_name: Field name for error messages
        
    Returns:
        Validated event
        
    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(event, dict):
        raise ValidationError(f"{field_name} must be a dictionary", field_name)
    
    required_fields = ["time", "intensity", "duration"]
    for field in required_fields:
        if field not in event:
            raise ValidationError(f"{field_name} must contain '{field}'", field)
    
    # Validate time
    if not isinstance(event["time"], (int, float)):
        raise ValidationError(f"{field_name}.time must be a number", f"{field_name}.time")
    if event["time"] < 0:
        raise ValidationError(f"{field_name}.time must be non-negative", f"{field_name}.time")
    
    # Validate intensity
    if not isinstance(event["intensity"], (int, float)):
        raise ValidationError(
            f"{field_name}.intensity must be a number",
            f"{field_name}.intensity"
        )
    if event["intensity"] < 0 or event["intensity"] > 1.0:
        raise ValidationError(
            f"{field_name}.intensity must be between 0 and 1",
            f"{field_name}.intensity"
        )
    
    # Validate duration
    if not isinstance(event["duration"], (int, float)):
        raise ValidationError(
            f"{field_name}.duration must be a number",
            f"{field_name}.duration"
        )
    if event["duration"] < 0:
        raise ValidationError(
            f"{field_name}.duration must be non-negative",
            f"{field_name}.duration"
        )
    
    return event


def validate_emotion(
    emotion: str,
    valid_emotions: Optional[List[str]] = None
) -> str:
    """
    Validate emotion input.
    
    Args:
        emotion: Emotion string to validate
        valid_emotions: List of valid emotions (optional)
        
    Returns:
        Validated emotion (lowercase)
        
    Raises:
        ValidationError: If validation fails
    """
    if emotion is None:
        raise ValidationError("emotion is required", "emotion")
    
    if not isinstance(emotion, str):
        raise ValidationError("emotion must be a string", "emotion")
    
    emotion = emotion.lower().strip()
    
    if len(emotion) == 0:
        raise ValidationError("emotion cannot be empty", "emotion")
    
    if valid_emotions and emotion not in valid_emotions:
        valid_list = ", ".join(valid_emotions)
        raise ValidationError(
            f"Invalid emotion. Must be one of: {valid_list}",
            "emotion"
        )
    
    return emotion


def validate_strategy(
    strategy: str,
    valid_strategies: List[str]
) -> str:
    """
    Validate segmentation strategy.
    
    Args:
        strategy: Strategy to validate
        valid_strategies: List of valid strategies
        
    Returns:
        Validated strategy
        
    Raises:
        ValidationError: If validation fails
    """
    if strategy is None:
        raise ValidationError("strategy is required", "strategy")
    
    if not isinstance(strategy, str):
        raise ValidationError("strategy must be a string", "strategy")
    
    strategy = strategy.lower().strip()
    
    if strategy not in valid_strategies:
        valid_list = ", ".join(valid_strategies)
        raise ValidationError(
            f"Invalid strategy. Must be one of: {valid_list}",
            "strategy"
        )
    
    return strategy


def validate_language(
    lang: str,
    valid_languages: Optional[List[str]] = None
) -> str:
    """
    Validate language code.
    
    Args:
        lang: Language code to validate
        valid_languages: List of valid language codes (optional)
        
    Returns:
        Validated language code
        
    Raises:
        ValidationError: If validation fails
    """
    if lang is None:
        return "en"  # Default to English
    
    if not isinstance(lang, str):
        raise ValidationError("lang must be a string", "lang")
    
    lang = lang.lower().strip()
    
    if len(lang) == 0:
        return "en"
    
    if valid_languages and lang not in valid_languages:
        valid_list = ", ".join(valid_languages)
        raise ValidationError(
            f"Invalid language. Must be one of: {valid_list}",
            "lang"
        )
    
    return lang
