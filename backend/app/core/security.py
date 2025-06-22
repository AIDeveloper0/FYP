"""
Security utilities for the application
"""
import secrets


def generate_api_key() -> str:
    """Generate a secure API key"""
    return secrets.token_urlsafe(32)