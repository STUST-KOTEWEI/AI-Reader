"""
Recommendation System Module

Provides content recommendations based on reading history and preferences.
"""

from .recommendation_engine import (
    ContentItem,
    UserPreference,
    Recommendation,
    RecommendationEngine,
    get_recommendation_engine
)

__all__ = [
    'ContentItem',
    'UserPreference',
    'Recommendation',
    'RecommendationEngine',
    'get_recommendation_engine'
]
