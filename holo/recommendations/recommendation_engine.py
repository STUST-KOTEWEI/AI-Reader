"""
Recommendation System Module

Provides content recommendations based on reading history and preferences.
"""

from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass, field, asdict
from datetime import datetime
import random


@dataclass
class ContentItem:
    """
    Represents a content item for recommendations.
    
    Attributes:
        content_id: Unique content identifier
        title: Content title
        author: Content author
        genre: Content genre/category
        tags: Content tags
        rating: Average rating
        popularity_score: Popularity score
        created_at: When content was added
    """
    content_id: str
    title: str
    author: str = ""
    genre: str = ""
    tags: List[str] = field(default_factory=list)
    rating: float = 0.0
    popularity_score: float = 0.0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContentItem':
        """Create from dictionary."""
        return cls(**data)


@dataclass
class UserPreference:
    """
    User preferences for recommendations.
    
    Attributes:
        user_id: User identifier
        favorite_genres: Preferred genres
        favorite_authors: Preferred authors
        favorite_tags: Preferred tags
        reading_speed: User's reading speed
        content_length_preference: Preferred content length
    """
    user_id: str
    favorite_genres: List[str] = field(default_factory=list)
    favorite_authors: List[str] = field(default_factory=list)
    favorite_tags: List[str] = field(default_factory=list)
    reading_speed: str = "normal"  # slow, normal, fast
    content_length_preference: str = "medium"  # short, medium, long
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class Recommendation:
    """
    A content recommendation.
    
    Attributes:
        content_id: Recommended content ID
        title: Content title
        reason: Why this was recommended
        score: Recommendation score (0-1)
        source: Source of recommendation
    """
    content_id: str
    title: str
    reason: str
    score: float
    source: str  # "history", "preference", "popular", "similar"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


class RecommendationEngine:
    """Generates content recommendations."""
    
    def __init__(self):
        self._content_catalog: Dict[str, ContentItem] = {}
        self._user_preferences: Dict[str, UserPreference] = {}
        self._user_history: Dict[str, List[str]] = {}  # user_id -> list of content_ids
        self._user_ratings: Dict[str, Dict[str, float]] = {}  # user_id -> {content_id: rating}
    
    def add_content(self, content: ContentItem) -> None:
        """Add content to the catalog."""
        self._content_catalog[content.content_id] = content
    
    def get_content(self, content_id: str) -> Optional[ContentItem]:
        """Get content by ID."""
        return self._content_catalog.get(content_id)
    
    def set_user_preference(self, preference: UserPreference) -> None:
        """Set user preferences."""
        self._user_preferences[preference.user_id] = preference
    
    def get_user_preference(self, user_id: str) -> Optional[UserPreference]:
        """Get user preferences."""
        return self._user_preferences.get(user_id)
    
    def record_reading(self, user_id: str, content_id: str) -> None:
        """Record that a user read content."""
        if user_id not in self._user_history:
            self._user_history[user_id] = []
        if content_id not in self._user_history[user_id]:
            self._user_history[user_id].append(content_id)
    
    def rate_content(self, user_id: str, content_id: str, rating: float) -> None:
        """Record a user's rating for content."""
        if user_id not in self._user_ratings:
            self._user_ratings[user_id] = {}
        self._user_ratings[user_id][content_id] = rating
        
        # Update content average rating
        if content_id in self._content_catalog:
            self._update_content_rating(content_id)
    
    def _update_content_rating(self, content_id: str) -> None:
        """Update the average rating for content."""
        ratings = [
            r[content_id] 
            for r in self._user_ratings.values() 
            if content_id in r
        ]
        if ratings:
            self._content_catalog[content_id].rating = sum(ratings) / len(ratings)
    
    def get_recommendations(
        self,
        user_id: str,
        limit: int = 10
    ) -> List[Recommendation]:
        """Get personalized recommendations for a user."""
        recommendations: List[Recommendation] = []
        
        # Get user data
        preference = self._user_preferences.get(user_id)
        history = set(self._user_history.get(user_id, []))
        
        # Score each content item
        scored_items: List[tuple] = []
        
        for content_id, content in self._content_catalog.items():
            if content_id in history:
                continue  # Skip already read content
            
            score = 0.0
            reasons = []
            
            # Genre matching
            if preference and content.genre in preference.favorite_genres:
                score += 0.3
                reasons.append(f"喜歡的類別: {content.genre}")
            
            # Author matching
            if preference and content.author in preference.favorite_authors:
                score += 0.25
                reasons.append(f"喜歡的作者: {content.author}")
            
            # Tag matching
            if preference:
                matching_tags = set(content.tags) & set(preference.favorite_tags)
                if matching_tags:
                    score += 0.2 * (len(matching_tags) / max(len(preference.favorite_tags), 1))
                    reasons.append(f"相關標籤: {', '.join(list(matching_tags)[:3])}")
            
            # Rating boost
            score += content.rating * 0.15
            
            # Popularity boost
            score += content.popularity_score * 0.1
            
            if score > 0:
                reason = reasons[0] if reasons else "熱門內容"
                scored_items.append((content, score, reason))
        
        # Sort by score and take top items
        scored_items.sort(key=lambda x: x[1], reverse=True)
        
        for content, score, reason in scored_items[:limit]:
            source = "preference" if preference else "popular"
            recommendations.append(Recommendation(
                content_id=content.content_id,
                title=content.title,
                reason=reason,
                score=min(score, 1.0),
                source=source
            ))
        
        return recommendations
    
    def get_similar_content(
        self,
        content_id: str,
        limit: int = 5
    ) -> List[Recommendation]:
        """Get content similar to the given content."""
        source_content = self._content_catalog.get(content_id)
        if not source_content:
            return []
        
        recommendations: List[Recommendation] = []
        scored_items: List[tuple] = []
        
        for cid, content in self._content_catalog.items():
            if cid == content_id:
                continue
            
            score = 0.0
            reasons = []
            
            # Same genre
            if content.genre == source_content.genre:
                score += 0.4
                reasons.append(f"相同類別: {content.genre}")
            
            # Same author
            if content.author == source_content.author:
                score += 0.3
                reasons.append(f"同作者: {content.author}")
            
            # Overlapping tags
            common_tags = set(content.tags) & set(source_content.tags)
            if common_tags:
                score += 0.3 * (len(common_tags) / max(len(source_content.tags), 1))
                reasons.append(f"相似標籤: {', '.join(list(common_tags)[:2])}")
            
            if score > 0:
                scored_items.append((content, score, reasons[0] if reasons else "相似內容"))
        
        scored_items.sort(key=lambda x: x[1], reverse=True)
        
        for content, score, reason in scored_items[:limit]:
            recommendations.append(Recommendation(
                content_id=content.content_id,
                title=content.title,
                reason=reason,
                score=min(score, 1.0),
                source="similar"
            ))
        
        return recommendations
    
    def get_popular_content(self, limit: int = 10) -> List[Recommendation]:
        """Get popular content."""
        items = list(self._content_catalog.values())
        items.sort(key=lambda x: (x.popularity_score, x.rating), reverse=True)
        
        return [
            Recommendation(
                content_id=item.content_id,
                title=item.title,
                reason="熱門推薦",
                score=item.popularity_score,
                source="popular"
            )
            for item in items[:limit]
        ]
    
    def get_trending_content(self, limit: int = 10) -> List[Recommendation]:
        """Get trending content (recently popular)."""
        items = list(self._content_catalog.values())
        # Sort by created_at (recent) and popularity
        items.sort(key=lambda x: (x.created_at, x.popularity_score), reverse=True)
        
        return [
            Recommendation(
                content_id=item.content_id,
                title=item.title,
                reason="最新熱門",
                score=item.popularity_score,
                source="popular"
            )
            for item in items[:limit]
        ]


# Global instance
_recommendation_engine: Optional[RecommendationEngine] = None


def get_recommendation_engine() -> RecommendationEngine:
    """Get the global recommendation engine instance."""
    global _recommendation_engine
    if _recommendation_engine is None:
        _recommendation_engine = RecommendationEngine()
    return _recommendation_engine
