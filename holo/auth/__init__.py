"""
Authentication Module

Provides user authentication functionality.
"""

from .authentication import (
    User,
    Session,
    AuthManager,
    get_auth_manager,
    hash_password,
    verify_password,
    generate_token
)

__all__ = [
    'User',
    'Session',
    'AuthManager',
    'get_auth_manager',
    'hash_password',
    'verify_password',
    'generate_token'
]
