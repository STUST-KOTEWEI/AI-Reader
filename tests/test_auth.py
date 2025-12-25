"""
Tests for Authentication Module
"""

import pytest
from holo.auth import (
    User,
    Session,
    AuthManager,
    get_auth_manager,
    hash_password,
    verify_password,
    generate_token
)


class TestPasswordFunctions:
    """Tests for password utility functions."""
    
    def test_hash_password(self):
        """Test password hashing."""
        password = "test_password_123"
        hashed = hash_password(password)
        assert hashed != password
        assert len(hashed) == 64  # SHA-256 hex length
    
    def test_verify_password_correct(self):
        """Test verifying correct password."""
        password = "test_password_123"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        """Test verifying incorrect password."""
        password = "test_password_123"
        hashed = hash_password(password)
        assert verify_password("wrong_password", hashed) is False
    
    def test_generate_token(self):
        """Test token generation."""
        token = generate_token()
        assert len(token) > 0
        # Tokens should be unique
        token2 = generate_token()
        assert token != token2


class TestUser:
    """Tests for User dataclass."""
    
    def test_create_user(self):
        """Test creating a user."""
        user = User(
            user_id="user_001",
            username="testuser",
            email="test@example.com",
            password_hash=hash_password("password123")
        )
        assert user.user_id == "user_001"
        assert user.username == "testuser"
        assert user.is_active is True
        assert user.role == "user"
    
    def test_user_to_dict_without_password(self):
        """Test converting user to dict without password."""
        user = User(
            user_id="user_001",
            username="testuser",
            email="test@example.com",
            password_hash=hash_password("password123")
        )
        data = user.to_dict(include_password=False)
        assert 'password_hash' not in data
        assert data['username'] == "testuser"
    
    def test_user_to_dict_with_password(self):
        """Test converting user to dict with password."""
        user = User(
            user_id="user_001",
            username="testuser",
            email="test@example.com",
            password_hash=hash_password("password123")
        )
        data = user.to_dict(include_password=True)
        assert 'password_hash' in data


class TestSession:
    """Tests for Session dataclass."""
    
    def test_create_session(self):
        """Test creating a session."""
        session = Session(
            session_id="sess_001",
            user_id="user_001",
            token=generate_token()
        )
        assert session.session_id == "sess_001"
        assert session.is_valid is True
    
    def test_session_not_expired(self):
        """Test session is not expired."""
        session = Session(
            session_id="sess_001",
            user_id="user_001",
            token=generate_token()
        )
        assert session.is_expired() is False


class TestAuthManager:
    """Tests for AuthManager."""
    
    def test_register_user(self):
        """Test registering a new user."""
        manager = AuthManager()
        user = manager.register(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        assert user is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"
    
    def test_register_duplicate_username(self):
        """Test registering with duplicate username."""
        manager = AuthManager()
        manager.register(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        user = manager.register(
            username="testuser",
            email="test2@example.com",
            password="password123"
        )
        assert user is None
    
    def test_register_duplicate_email(self):
        """Test registering with duplicate email."""
        manager = AuthManager()
        manager.register(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        user = manager.register(
            username="testuser2",
            email="test@example.com",
            password="password123"
        )
        assert user is None
    
    def test_login_with_username(self):
        """Test login with username."""
        manager = AuthManager()
        manager.register(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        session = manager.login("testuser", "password123")
        assert session is not None
        assert session.token is not None
    
    def test_login_with_email(self):
        """Test login with email."""
        manager = AuthManager()
        manager.register(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        session = manager.login("test@example.com", "password123")
        assert session is not None
    
    def test_login_wrong_password(self):
        """Test login with wrong password."""
        manager = AuthManager()
        manager.register(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        session = manager.login("testuser", "wrongpassword")
        assert session is None
    
    def test_login_nonexistent_user(self):
        """Test login with nonexistent user."""
        manager = AuthManager()
        session = manager.login("nonexistent", "password123")
        assert session is None
    
    def test_logout(self):
        """Test logout."""
        manager = AuthManager()
        manager.register(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        session = manager.login("testuser", "password123")
        
        result = manager.logout(session.token)
        assert result is True
        
        # Token should be invalid after logout
        user = manager.validate_token(session.token)
        assert user is None
    
    def test_validate_token(self):
        """Test validating token."""
        manager = AuthManager()
        manager.register(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        session = manager.login("testuser", "password123")
        
        user = manager.validate_token(session.token)
        assert user is not None
        assert user.username == "testuser"
    
    def test_validate_invalid_token(self):
        """Test validating invalid token."""
        manager = AuthManager()
        user = manager.validate_token("invalid_token")
        assert user is None
    
    def test_get_user(self):
        """Test getting user by ID."""
        manager = AuthManager()
        registered_user = manager.register(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        
        user = manager.get_user(registered_user.user_id)
        assert user is not None
        assert user.username == "testuser"
    
    def test_update_password(self):
        """Test updating password."""
        manager = AuthManager()
        user = manager.register(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        
        result = manager.update_password(
            user.user_id,
            "password123",
            "newpassword456"
        )
        assert result is True
        
        # Old password should not work
        session = manager.login("testuser", "password123")
        assert session is None
        
        # New password should work
        session = manager.login("testuser", "newpassword456")
        assert session is not None
    
    def test_update_password_wrong_old(self):
        """Test updating password with wrong old password."""
        manager = AuthManager()
        user = manager.register(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        
        result = manager.update_password(
            user.user_id,
            "wrongpassword",
            "newpassword456"
        )
        assert result is False
    
    def test_deactivate_user(self):
        """Test deactivating user."""
        manager = AuthManager()
        user = manager.register(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        
        result = manager.deactivate_user(user.user_id)
        assert result is True
        
        # Deactivated user should not be able to login
        session = manager.login("testuser", "password123")
        assert session is None


class TestGetAuthManager:
    """Tests for global auth manager."""
    
    def test_get_global_manager(self):
        """Test getting global auth manager."""
        manager = get_auth_manager()
        assert manager is not None
        assert isinstance(manager, AuthManager)
