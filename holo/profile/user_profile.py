"""
User Profile Module

Provides user profile management for personalized multi-modal immersive experiences.
Includes accessibility settings and sensory preferences.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum
import json


class HapticIntensityLevel(Enum):
    """Haptic feedback intensity levels for accessibility."""
    OFF = 0.0
    LOW = 0.3
    MEDIUM = 0.6
    HIGH = 1.0


class AudioSpeed(Enum):
    """Audio playback speed options."""
    SLOW = 0.75
    NORMAL = 1.0
    FAST = 1.25
    VERY_FAST = 1.5


class FontSize(Enum):
    """Font size options for accessibility."""
    SMALL = 12
    MEDIUM = 16
    LARGE = 20
    EXTRA_LARGE = 24


@dataclass
class AccessibilitySettings:
    """
    Accessibility settings for inclusive reading experience.
    
    Attributes:
        haptic_enabled: Whether haptic feedback is enabled
        haptic_intensity: Haptic feedback intensity level
        audio_enabled: Whether audio output is enabled
        audio_speed: Audio playback speed
        high_contrast: Whether high contrast mode is enabled
        font_size: Font size for text display
        reduce_motion: Whether to reduce motion/animations
        screen_reader_mode: Whether screen reader mode is enabled
    """
    haptic_enabled: bool = True
    haptic_intensity: float = 0.6
    audio_enabled: bool = True
    audio_speed: float = 1.0
    high_contrast: bool = False
    font_size: int = 16
    reduce_motion: bool = False
    screen_reader_mode: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert accessibility settings to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AccessibilitySettings':
        """Create AccessibilitySettings from dictionary."""
        return cls(
            haptic_enabled=data.get('haptic_enabled', True),
            haptic_intensity=data.get('haptic_intensity', 0.6),
            audio_enabled=data.get('audio_enabled', True),
            audio_speed=data.get('audio_speed', 1.0),
            high_contrast=data.get('high_contrast', False),
            font_size=data.get('font_size', 16),
            reduce_motion=data.get('reduce_motion', False),
            screen_reader_mode=data.get('screen_reader_mode', False)
        )


@dataclass
class UserPreferences:
    """
    User preferences for personalized experience.
    
    Attributes:
        preferred_language: Preferred language code (e.g., 'zh-tw', 'en')
        preferred_voice: Preferred TTS voice ID
        theme: UI theme preference ('dark', 'light', 'auto')
        auto_play_audio: Whether to auto-play audio on generation
        save_history: Whether to save reading history
    """
    preferred_language: str = 'zh-tw'
    preferred_voice: Optional[str] = None
    theme: str = 'dark'
    auto_play_audio: bool = False
    save_history: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user preferences to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserPreferences':
        """Create UserPreferences from dictionary."""
        return cls(
            preferred_language=data.get('preferred_language', 'zh-tw'),
            preferred_voice=data.get('preferred_voice'),
            theme=data.get('theme', 'dark'),
            auto_play_audio=data.get('auto_play_audio', False),
            save_history=data.get('save_history', True)
        )


@dataclass
class UserProfile:
    """
    User profile for personalized multi-modal immersive experiences.
    
    Attributes:
        user_id: Unique user identifier
        display_name: User display name
        accessibility: Accessibility settings
        preferences: User preferences
    """
    user_id: str = "default"
    display_name: str = "使用者"
    accessibility: AccessibilitySettings = field(
        default_factory=AccessibilitySettings
    )
    preferences: UserPreferences = field(default_factory=UserPreferences)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user profile to dictionary."""
        return {
            'user_id': self.user_id,
            'display_name': self.display_name,
            'accessibility': self.accessibility.to_dict(),
            'preferences': self.preferences.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserProfile':
        """Create UserProfile from dictionary."""
        accessibility_data = data.get('accessibility', {})
        preferences_data = data.get('preferences', {})
        
        return cls(
            user_id=data.get('user_id', 'default'),
            display_name=data.get('display_name', '使用者'),
            accessibility=AccessibilitySettings.from_dict(accessibility_data),
            preferences=UserPreferences.from_dict(preferences_data)
        )
    
    def to_json(self) -> str:
        """Convert user profile to JSON string."""
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'UserProfile':
        """Create UserProfile from JSON string."""
        return cls.from_dict(json.loads(json_str))
    
    def update_accessibility(self, **kwargs) -> None:
        """
        Update accessibility settings.
        
        Args:
            **kwargs: Accessibility settings to update
        """
        for key, value in kwargs.items():
            if hasattr(self.accessibility, key):
                setattr(self.accessibility, key, value)
    
    def update_preferences(self, **kwargs) -> None:
        """
        Update user preferences.
        
        Args:
            **kwargs: User preferences to update
        """
        for key, value in kwargs.items():
            if hasattr(self.preferences, key):
                setattr(self.preferences, key, value)
    
    def get_haptic_multiplier(self) -> float:
        """
        Get haptic intensity multiplier based on user settings.
        
        Returns:
            Haptic intensity multiplier (0.0 if disabled)
        """
        if not self.accessibility.haptic_enabled:
            return 0.0
        return self.accessibility.haptic_intensity
    
    def get_audio_speed(self) -> float:
        """
        Get audio playback speed based on user settings.
        
        Returns:
            Audio playback speed multiplier
        """
        if not self.accessibility.audio_enabled:
            return 0.0
        return self.accessibility.audio_speed


class ProfileManager:
    """
    Manages user profiles in memory.
    
    Note: This is a simple in-memory implementation.
    For production, this should be backed by a database.
    """
    
    def __init__(self):
        """Initialize the profile manager."""
        self._profiles: Dict[str, UserProfile] = {}
        # Create default profile
        self._profiles['default'] = UserProfile()
    
    def get_profile(self, user_id: str = 'default') -> UserProfile:
        """
        Get user profile by ID.
        
        Args:
            user_id: User ID to retrieve
            
        Returns:
            UserProfile instance
        """
        if user_id not in self._profiles:
            # Create new profile if not exists
            self._profiles[user_id] = UserProfile(user_id=user_id)
        return self._profiles[user_id]
    
    def update_profile(
        self,
        user_id: str,
        data: Dict[str, Any]
    ) -> UserProfile:
        """
        Update user profile.
        
        Args:
            user_id: User ID to update
            data: Profile data to update
            
        Returns:
            Updated UserProfile instance
        """
        profile = self.get_profile(user_id)
        
        if 'display_name' in data:
            profile.display_name = data['display_name']
        
        if 'accessibility' in data:
            profile.update_accessibility(**data['accessibility'])
        
        if 'preferences' in data:
            profile.update_preferences(**data['preferences'])
        
        return profile
    
    def delete_profile(self, user_id: str) -> bool:
        """
        Delete user profile.
        
        Args:
            user_id: User ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        if user_id in self._profiles and user_id != 'default':
            del self._profiles[user_id]
            return True
        return False
    
    def list_profiles(self) -> Dict[str, Dict[str, Any]]:
        """
        List all profiles.
        
        Returns:
            Dictionary of user profiles
        """
        return {
            user_id: profile.to_dict()
            for user_id, profile in self._profiles.items()
        }


# Global profile manager instance
_profile_manager: Optional[ProfileManager] = None


def get_profile_manager() -> ProfileManager:
    """
    Get the global profile manager instance.
    
    Returns:
        ProfileManager instance
    """
    global _profile_manager
    if _profile_manager is None:
        _profile_manager = ProfileManager()
    return _profile_manager
