"""
Social Features Module

Provides social functionality including sharing and comments.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime


@dataclass
class Comment:
    """
    Represents a user comment.
    
    Attributes:
        comment_id: Unique comment identifier
        user_id: ID of the commenting user
        content_id: ID of the content being commented on
        text: Comment text
        created_at: When the comment was created
        updated_at: When the comment was last updated
        likes: Number of likes
        parent_id: ID of parent comment (for replies)
    """
    comment_id: str
    user_id: str
    content_id: str
    text: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: Optional[str] = None
    likes: int = 0
    parent_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Comment':
        """Create from dictionary."""
        return cls(**data)


@dataclass
class Share:
    """
    Represents a content share.
    
    Attributes:
        share_id: Unique share identifier
        user_id: ID of the sharing user
        content_id: ID of the shared content
        platform: Platform shared to (twitter, facebook, etc.)
        shared_at: When the share occurred
        message: Optional message with share
    """
    share_id: str
    user_id: str
    content_id: str
    platform: str
    shared_at: str = field(default_factory=lambda: datetime.now().isoformat())
    message: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Share':
        """Create from dictionary."""
        return cls(**data)


@dataclass
class ContentStats:
    """
    Statistics for a piece of content.
    
    Attributes:
        content_id: Content identifier
        views: Number of views
        shares: Number of shares
        comments_count: Number of comments
        likes: Number of likes
        avg_rating: Average rating
    """
    content_id: str
    views: int = 0
    shares: int = 0
    comments_count: int = 0
    likes: int = 0
    avg_rating: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


class SocialManager:
    """Manages social features."""
    
    def __init__(self):
        self._comments: Dict[str, List[Comment]] = {}  # content_id -> comments
        self._shares: Dict[str, List[Share]] = {}  # content_id -> shares
        self._stats: Dict[str, ContentStats] = {}
        self._user_likes: Dict[str, set] = {}  # user_id -> set of comment_ids
    
    def add_comment(
        self,
        comment_id: str,
        user_id: str,
        content_id: str,
        text: str,
        parent_id: Optional[str] = None
    ) -> Comment:
        """Add a comment to content."""
        comment = Comment(
            comment_id=comment_id,
            user_id=user_id,
            content_id=content_id,
            text=text,
            parent_id=parent_id
        )
        
        if content_id not in self._comments:
            self._comments[content_id] = []
        self._comments[content_id].append(comment)
        
        # Update stats
        self._ensure_stats(content_id)
        self._stats[content_id].comments_count += 1
        
        return comment
    
    def get_comments(self, content_id: str) -> List[Comment]:
        """Get comments for content."""
        return self._comments.get(content_id, [])
    
    def delete_comment(self, content_id: str, comment_id: str) -> bool:
        """Delete a comment."""
        if content_id not in self._comments:
            return False
        
        for i, comment in enumerate(self._comments[content_id]):
            if comment.comment_id == comment_id:
                self._comments[content_id].pop(i)
                self._stats[content_id].comments_count -= 1
                return True
        return False
    
    def like_comment(self, user_id: str, comment_id: str, content_id: str) -> bool:
        """Like a comment."""
        if user_id not in self._user_likes:
            self._user_likes[user_id] = set()
        
        if comment_id in self._user_likes[user_id]:
            return False  # Already liked
        
        self._user_likes[user_id].add(comment_id)
        
        # Find and update comment
        for comment in self._comments.get(content_id, []):
            if comment.comment_id == comment_id:
                comment.likes += 1
                return True
        return False
    
    def share_content(
        self,
        share_id: str,
        user_id: str,
        content_id: str,
        platform: str,
        message: str = ""
    ) -> Share:
        """Share content to a platform."""
        share = Share(
            share_id=share_id,
            user_id=user_id,
            content_id=content_id,
            platform=platform,
            message=message
        )
        
        if content_id not in self._shares:
            self._shares[content_id] = []
        self._shares[content_id].append(share)
        
        # Update stats
        self._ensure_stats(content_id)
        self._stats[content_id].shares += 1
        
        return share
    
    def get_shares(self, content_id: str) -> List[Share]:
        """Get shares for content."""
        return self._shares.get(content_id, [])
    
    def record_view(self, content_id: str) -> None:
        """Record a content view."""
        self._ensure_stats(content_id)
        self._stats[content_id].views += 1
    
    def get_stats(self, content_id: str) -> ContentStats:
        """Get statistics for content."""
        self._ensure_stats(content_id)
        return self._stats[content_id]
    
    def _ensure_stats(self, content_id: str) -> None:
        """Ensure stats exist for content."""
        if content_id not in self._stats:
            self._stats[content_id] = ContentStats(content_id=content_id)
    
    def get_share_url(self, content_id: str, platform: str) -> str:
        """Generate a share URL for a platform."""
        base_url = f"https://ai-reader.example.com/content/{content_id}"
        
        share_urls = {
            "twitter": f"https://twitter.com/intent/tweet?url={base_url}",
            "facebook": f"https://www.facebook.com/sharer/sharer.php?u={base_url}",
            "linkedin": f"https://www.linkedin.com/shareArticle?mini=true&url={base_url}",
            "line": f"https://line.me/R/msg/text/?{base_url}",
            "copy": base_url
        }
        
        return share_urls.get(platform, base_url)


# Global instance
_social_manager: Optional[SocialManager] = None


def get_social_manager() -> SocialManager:
    """Get the global social manager instance."""
    global _social_manager
    if _social_manager is None:
        _social_manager = SocialManager()
    return _social_manager
