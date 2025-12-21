"""
Authentication Module

Provides user authentication functionality.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
import hashlib
import secrets
import json


@dataclass
class User:
    """
    Represents a user account.
    
    Attributes:
        user_id: Unique user identifier
        username: User's username
        email: User's email address
        password_hash: Hashed password
        created_at: Account creation timestamp
        last_login: Last login timestamp
        is_active: Whether the account is active
        role: User role (user, admin)
    """
    user_id: str
    username: str
    email: str
    password_hash: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_login: Optional[str] = None
    is_active: bool = True
    role: str = "user"
    
    def to_dict(self, include_password: bool = False) -> Dict[str, Any]:
        """Convert to dictionary."""
        data = asdict(self)
        if not include_password:
            del data['password_hash']
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """Create from dictionary."""
        return cls(**data)


@dataclass
class Session:
    """
    Represents an authentication session.
    
    Attributes:
        session_id: Unique session identifier
        user_id: Associated user ID
        token: Session token
        created_at: Session creation time
        expires_at: Session expiration time
        is_valid: Whether session is still valid
    """
    session_id: str
    user_id: str
    token: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    expires_at: str = field(
        default_factory=lambda: (datetime.now() + timedelta(days=7)).isoformat()
    )
    is_valid: bool = True
    
    def is_expired(self) -> bool:
        """Check if session is expired."""
        return datetime.fromisoformat(self.expires_at) < datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash."""
    return hash_password(password) == password_hash


def generate_token() -> str:
    """Generate a secure random token."""
    return secrets.token_urlsafe(32)


def generate_user_id() -> str:
    """Generate a unique user ID."""
    return f"user_{secrets.token_hex(8)}"


def generate_session_id() -> str:
    """Generate a unique session ID."""
    return f"sess_{secrets.token_hex(8)}"


class AuthManager:
    """Manages user authentication."""
    
    def __init__(self):
        self._users: Dict[str, User] = {}
        self._sessions: Dict[str, Session] = {}
        self._email_index: Dict[str, str] = {}  # email -> user_id
        self._username_index: Dict[str, str] = {}  # username -> user_id
    
    def register(
        self,
        username: str,
        email: str,
        password: str
    ) -> Optional[User]:
        """
        Register a new user.
        
        Returns None if username or email already exists.
        """
        if username in self._username_index:
            return None
        if email in self._email_index:
            return None
        
        user_id = generate_user_id()
        user = User(
            user_id=user_id,
            username=username,
            email=email,
            password_hash=hash_password(password)
        )
        
        self._users[user_id] = user
        self._username_index[username] = user_id
        self._email_index[email] = user_id
        
        return user
    
    def login(
        self,
        username_or_email: str,
        password: str
    ) -> Optional[Session]:
        """
        Login a user.
        
        Returns a session if credentials are valid, None otherwise.
        """
        # Find user by username or email
        user_id = self._username_index.get(username_or_email)
        if not user_id:
            user_id = self._email_index.get(username_or_email)
        
        if not user_id:
            return None
        
        user = self._users.get(user_id)
        if not user or not user.is_active:
            return None
        
        if not verify_password(password, user.password_hash):
            return None
        
        # Update last login
        user.last_login = datetime.now().isoformat()
        
        # Create session
        session = Session(
            session_id=generate_session_id(),
            user_id=user_id,
            token=generate_token()
        )
        self._sessions[session.token] = session
        
        return session
    
    def logout(self, token: str) -> bool:
        """Logout by invalidating session."""
        if token in self._sessions:
            self._sessions[token].is_valid = False
            return True
        return False
    
    def validate_token(self, token: str) -> Optional[User]:
        """
        Validate a session token.
        
        Returns the user if valid, None otherwise.
        """
        session = self._sessions.get(token)
        if not session or not session.is_valid or session.is_expired():
            return None
        
        return self._users.get(session.user_id)
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return self._users.get(user_id)
    
    def update_password(
        self,
        user_id: str,
        old_password: str,
        new_password: str
    ) -> bool:
        """Update user password."""
        user = self._users.get(user_id)
        if not user:
            return False
        
        if not verify_password(old_password, user.password_hash):
            return False
        
        user.password_hash = hash_password(new_password)
        return True
    
    def deactivate_user(self, user_id: str) -> bool:
        """Deactivate a user account."""
        user = self._users.get(user_id)
        if user:
            user.is_active = False
            return True
        return False


# Global instance
_auth_manager: Optional[AuthManager] = None


def get_auth_manager() -> AuthManager:
    """Get the global auth manager instance."""
    global _auth_manager
    if _auth_manager is None:
        _auth_manager = AuthManager()
    return _auth_manager
