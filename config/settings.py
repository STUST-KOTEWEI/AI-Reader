"""
Configuration settings for Project-HOLO.

Centralized configuration management using environment variables
with sensible defaults.
"""

import os
from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class TTSSettings:
    """Text-to-Speech configuration."""
    elevenlabs_api_key: Optional[str] = field(
        default_factory=lambda: os.getenv("ELEVENLABS_API_KEY")
    )
    default_voice_id: str = "21m00Tcm4TlvDq8ikWAM"  # Rachel
    default_language: str = "en"
    fallback_enabled: bool = True


@dataclass
class HapticsSettings:
    """Haptics configuration."""
    max_intensity: float = 1.0
    default_intensity: float = 0.5
    default_duration_ms: int = 100
    max_events_per_pattern: int = 100


@dataclass
class SegmentationSettings:
    """Text segmentation configuration."""
    max_chunk_size: int = 500
    default_strategy: str = "adaptive"
    supported_strategies: List[str] = field(
        default_factory=lambda: ["sentences", "paragraphs", "adaptive"]
    )


@dataclass
class EmotionAnalysisSettings:
    """Emotion analysis configuration."""
    default_emotions: List[str] = field(
        default_factory=lambda: ["joy", "sadness", "anger", "fear", "surprise", "disgust"]
    )
    confidence_threshold: float = 0.3
    enable_sentiment: bool = True


@dataclass
class VisualSettings:
    """Visual generation configuration."""
    supported_styles: List[str] = field(
        default_factory=lambda: ["realistic", "artistic", "abstract", "minimalist"]
    )
    default_style: str = "realistic"
    max_concepts: int = 5


@dataclass
class OlfactorySettings:
    """Olfactory/scent configuration."""
    scent_families: List[str] = field(
        default_factory=lambda: [
            "floral", "woody", "citrus", "spicy", "fresh", 
            "sweet", "earthy", "oceanic", "smoky", "herbal"
        ]
    )
    max_blend_components: int = 5
    default_intensity: float = 0.5


@dataclass
class APISettings:
    """API server configuration."""
    host: str = field(default_factory=lambda: os.getenv("API_HOST", "127.0.0.1"))
    port: int = field(default_factory=lambda: int(os.getenv("API_PORT", "8000")))
    debug: bool = field(default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true")
    cors_origins: List[str] = field(
        default_factory=lambda: [
            "http://localhost",
            "http://localhost:5173",
            "capacitor://localhost",
        ]
    )
    api_version: str = "0.1.0"
    api_title: str = "Project-HOLO API"


@dataclass
class Settings:
    """Main application settings."""
    tts: TTSSettings = field(default_factory=TTSSettings)
    haptics: HapticsSettings = field(default_factory=HapticsSettings)
    segmentation: SegmentationSettings = field(default_factory=SegmentationSettings)
    emotion: EmotionAnalysisSettings = field(default_factory=EmotionAnalysisSettings)
    visual: VisualSettings = field(default_factory=VisualSettings)
    olfactory: OlfactorySettings = field(default_factory=OlfactorySettings)
    api: APISettings = field(default_factory=APISettings)


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get the global settings instance."""
    return settings


def reload_settings() -> Settings:
    """Reload settings from environment variables."""
    global settings
    settings = Settings()
    return settings
