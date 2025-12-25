"""
Tests for User Profile Module
"""

import pytest
import json
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from holo.profile.user_profile import (
    UserProfile,
    UserPreferences,
    AccessibilitySettings,
    ProfileManager,
    get_profile_manager
)


class TestAccessibilitySettings:
    """Tests for AccessibilitySettings class."""
    
    def test_default_values(self):
        """Test default accessibility settings."""
        settings = AccessibilitySettings()
        assert settings.haptic_enabled is True
        assert settings.haptic_intensity == 0.6
        assert settings.audio_enabled is True
        assert settings.audio_speed == 1.0
        assert settings.high_contrast is False
        assert settings.font_size == 16
        assert settings.reduce_motion is False
        assert settings.screen_reader_mode is False
    
    def test_custom_values(self):
        """Test custom accessibility settings."""
        settings = AccessibilitySettings(
            haptic_enabled=False,
            haptic_intensity=0.3,
            audio_enabled=False,
            audio_speed=1.5,
            high_contrast=True,
            font_size=24,
            reduce_motion=True,
            screen_reader_mode=True
        )
        assert settings.haptic_enabled is False
        assert settings.haptic_intensity == 0.3
        assert settings.audio_enabled is False
        assert settings.audio_speed == 1.5
        assert settings.high_contrast is True
        assert settings.font_size == 24
        assert settings.reduce_motion is True
        assert settings.screen_reader_mode is True
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        settings = AccessibilitySettings()
        data = settings.to_dict()
        assert isinstance(data, dict)
        assert 'haptic_enabled' in data
        assert 'haptic_intensity' in data
        assert 'audio_enabled' in data
        assert 'audio_speed' in data
    
    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {
            'haptic_enabled': False,
            'haptic_intensity': 0.8,
            'high_contrast': True
        }
        settings = AccessibilitySettings.from_dict(data)
        assert settings.haptic_enabled is False
        assert settings.haptic_intensity == 0.8
        assert settings.high_contrast is True
        # Default values should be used for missing keys
        assert settings.audio_enabled is True


class TestUserPreferences:
    """Tests for UserPreferences class."""
    
    def test_default_values(self):
        """Test default user preferences."""
        prefs = UserPreferences()
        assert prefs.preferred_language == 'zh-tw'
        assert prefs.preferred_voice is None
        assert prefs.theme == 'dark'
        assert prefs.auto_play_audio is False
        assert prefs.save_history is True
    
    def test_custom_values(self):
        """Test custom user preferences."""
        prefs = UserPreferences(
            preferred_language='en',
            preferred_voice='voice_123',
            theme='light',
            auto_play_audio=True,
            save_history=False
        )
        assert prefs.preferred_language == 'en'
        assert prefs.preferred_voice == 'voice_123'
        assert prefs.theme == 'light'
        assert prefs.auto_play_audio is True
        assert prefs.save_history is False
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        prefs = UserPreferences()
        data = prefs.to_dict()
        assert isinstance(data, dict)
        assert 'preferred_language' in data
        assert 'theme' in data
    
    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {
            'preferred_language': 'ja',
            'theme': 'auto'
        }
        prefs = UserPreferences.from_dict(data)
        assert prefs.preferred_language == 'ja'
        assert prefs.theme == 'auto'
        # Default values should be used for missing keys
        assert prefs.auto_play_audio is False


class TestUserProfile:
    """Tests for UserProfile class."""
    
    def test_default_profile(self):
        """Test default user profile."""
        profile = UserProfile()
        assert profile.user_id == 'default'
        assert profile.display_name == '使用者'
        assert isinstance(profile.accessibility, AccessibilitySettings)
        assert isinstance(profile.preferences, UserPreferences)
    
    def test_custom_profile(self):
        """Test custom user profile."""
        profile = UserProfile(
            user_id='user_123',
            display_name='Test User'
        )
        assert profile.user_id == 'user_123'
        assert profile.display_name == 'Test User'
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        profile = UserProfile(user_id='test', display_name='Tester')
        data = profile.to_dict()
        assert data['user_id'] == 'test'
        assert data['display_name'] == 'Tester'
        assert 'accessibility' in data
        assert 'preferences' in data
    
    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {
            'user_id': 'user_456',
            'display_name': 'New User',
            'accessibility': {'haptic_enabled': False},
            'preferences': {'theme': 'light'}
        }
        profile = UserProfile.from_dict(data)
        assert profile.user_id == 'user_456'
        assert profile.display_name == 'New User'
        assert profile.accessibility.haptic_enabled is False
        assert profile.preferences.theme == 'light'
    
    def test_to_json(self):
        """Test conversion to JSON string."""
        profile = UserProfile()
        json_str = profile.to_json()
        assert isinstance(json_str, str)
        data = json.loads(json_str)
        assert data['user_id'] == 'default'
    
    def test_from_json(self):
        """Test creation from JSON string."""
        json_str = '{"user_id": "json_user", "display_name": "JSON User"}'
        profile = UserProfile.from_json(json_str)
        assert profile.user_id == 'json_user'
        assert profile.display_name == 'JSON User'
    
    def test_update_accessibility(self):
        """Test updating accessibility settings."""
        profile = UserProfile()
        profile.update_accessibility(
            haptic_enabled=False,
            font_size=20
        )
        assert profile.accessibility.haptic_enabled is False
        assert profile.accessibility.font_size == 20
    
    def test_update_preferences(self):
        """Test updating user preferences."""
        profile = UserProfile()
        profile.update_preferences(
            theme='light',
            preferred_language='en'
        )
        assert profile.preferences.theme == 'light'
        assert profile.preferences.preferred_language == 'en'
    
    def test_get_haptic_multiplier_enabled(self):
        """Test haptic multiplier when enabled."""
        profile = UserProfile()
        profile.accessibility.haptic_enabled = True
        profile.accessibility.haptic_intensity = 0.8
        assert profile.get_haptic_multiplier() == 0.8
    
    def test_get_haptic_multiplier_disabled(self):
        """Test haptic multiplier when disabled."""
        profile = UserProfile()
        profile.accessibility.haptic_enabled = False
        assert profile.get_haptic_multiplier() == 0.0
    
    def test_get_audio_speed_enabled(self):
        """Test audio speed when enabled."""
        profile = UserProfile()
        profile.accessibility.audio_enabled = True
        profile.accessibility.audio_speed = 1.25
        assert profile.get_audio_speed() == 1.25
    
    def test_get_audio_speed_disabled(self):
        """Test audio speed when disabled."""
        profile = UserProfile()
        profile.accessibility.audio_enabled = False
        assert profile.get_audio_speed() == 0.0


class TestProfileManager:
    """Tests for ProfileManager class."""
    
    def test_default_profile_exists(self):
        """Test that default profile exists on initialization."""
        manager = ProfileManager()
        profile = manager.get_profile('default')
        assert profile is not None
        assert profile.user_id == 'default'
    
    def test_get_nonexistent_profile_creates_new(self):
        """Test that getting a nonexistent profile creates a new one."""
        manager = ProfileManager()
        profile = manager.get_profile('new_user')
        assert profile is not None
        assert profile.user_id == 'new_user'
    
    def test_update_profile(self):
        """Test updating a profile."""
        manager = ProfileManager()
        manager.update_profile('default', {
            'display_name': 'Updated User',
            'accessibility': {'haptic_enabled': False}
        })
        profile = manager.get_profile('default')
        assert profile.display_name == 'Updated User'
        assert profile.accessibility.haptic_enabled is False
    
    def test_delete_profile(self):
        """Test deleting a profile."""
        manager = ProfileManager()
        manager.get_profile('temp_user')  # Create the profile
        result = manager.delete_profile('temp_user')
        assert result is True
        # Getting it again should create a new one
        profile = manager.get_profile('temp_user')
        assert profile.display_name == '使用者'  # Back to default
    
    def test_cannot_delete_default_profile(self):
        """Test that default profile cannot be deleted."""
        manager = ProfileManager()
        result = manager.delete_profile('default')
        assert result is False
        profile = manager.get_profile('default')
        assert profile is not None
    
    def test_list_profiles(self):
        """Test listing all profiles."""
        manager = ProfileManager()
        manager.get_profile('user_1')
        manager.get_profile('user_2')
        profiles = manager.list_profiles()
        assert 'default' in profiles
        assert 'user_1' in profiles
        assert 'user_2' in profiles


class TestGlobalProfileManager:
    """Tests for global profile manager."""
    
    def test_get_profile_manager_singleton(self):
        """Test that get_profile_manager returns a singleton."""
        manager1 = get_profile_manager()
        manager2 = get_profile_manager()
        assert manager1 is manager2
