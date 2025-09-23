"""
Auth service.

Handles registration, login (password hashing, token issuance), logout, profile,
and token verification.
"""

from __future__ import annotations

from datetime import timedelta
from typing import Dict, Optional

from models.user_model import UserModel
from utils.auth import generate_jwt_token, hash_password, verify_password
from utils.errors import ConflictError, UnauthorizedError, ValidationError
from utils.time import get_current_timestamp, generate_default_avatar, get_default_availability
from utils.validation import validate_email, validate_password_strength, validate_timezone, sanitize_input


class AuthService:
    """Authentication and user management service."""

    def __init__(self):
        self.token_expiry = timedelta(hours=24)

    def register_user(self, user_data: Dict) -> Dict:
        """Register a new user with validation and password hashing."""
        # Sanitize input
        data = sanitize_input(user_data)
        
        # Validate required fields
        if not data.get('name'):
            raise ValidationError("Name is required")
        if not data.get('email'):
            raise ValidationError("Email is required")
        if not data.get('password'):
            raise ValidationError("Password is required")
        
        # Validate email format
        if not validate_email(data['email']):
            raise ValidationError("Invalid email format")
        
        # Validate password strength
        if not validate_password_strength(data['password']):
            raise ValidationError("Password must be at least 8 characters with uppercase, lowercase, and digit")
        
        # Validate timezone
        timezone = data.get('timezone', 'UTC')
        if not validate_timezone(timezone):
            raise ValidationError("Invalid timezone")
        
        # Check if user already exists
        existing_user = UserModel.get_member_by_name(data['name'])
        if existing_user:
            raise ConflictError("User with this name already exists")
        
        # Check if email already exists (simple check by looking through all users)
        all_users = UserModel.list_members()
        for user in all_users:
            if user.get('email') == data['email']:
                raise ConflictError("User with this email already exists")
        
        # Hash password
        hashed_password = hash_password(data['password'])
        
        # Create user record
        user_payload = {
            'name': data['name'],
            'email': data['email'],
            'timezone': timezone,
            'role': 'member',
            'status': 'offline',
            'availability': get_default_availability(),
            'teams': [],
            'avatar': generate_default_avatar(data['name']),
            'createdAt': get_current_timestamp(),
            'password_hash': hashed_password  # Store hashed password
        }
        
        user = UserModel.create_member(user_payload)
        return user

    def authenticate_user(self, *, email: Optional[str] = None, name: Optional[str] = None, password: str) -> Dict:
        """Authenticate user with either email or name and a password."""
        if (email is None and name is None) or (email is not None and name is not None):
            raise ValidationError("Provide exactly one of email or name")
        if not password:
            raise ValidationError("Password is required")

        # Find user by email or name
        all_users = UserModel.list_members()
        user = None
        if email is not None:
            for u in all_users:
                if u.get('email') == email:
                    user = u
                    break
        else:
            for u in all_users:
                if u.get('name') == name:
                    user = u
                    break

        if not user:
            raise UnauthorizedError("Invalid credentials")

        # Get stored password hash (we need to access the raw storage for this)
        from utils.storage import read_json
        members_data = read_json('members.json', default_factory=list)
        stored_hash = None
        for member in members_data:
            if email is not None and member.get('email') == email:
                stored_hash = member.get('password_hash')
                break
            if name is not None and member.get('name') == name:
                stored_hash = member.get('password_hash')
                break

        if not stored_hash or not verify_password(password, stored_hash):
            raise UnauthorizedError("Invalid credentials")

        return user

    def generate_token(self, user_id: str) -> str:
        """Generate JWT token for user."""
        return generate_jwt_token(user_id, self.token_expiry)

    def verify_token(self, token: str) -> Dict:
        """Verify JWT token and return payload."""
        from utils.auth import verify_jwt_token
        return verify_jwt_token(token)

    def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """Get user profile by ID."""
        return UserModel.get_member(user_id)

    def update_user_profile(self, user_id: str, updates: Dict) -> Optional[Dict]:
        """Update user profile with validation."""
        data = sanitize_input(updates)
        
        # Validate timezone if provided
        if 'timezone' in data and not validate_timezone(data['timezone']):
            raise ValidationError("Invalid timezone")
        
        # Don't allow updating email or password through this method
        if 'email' in data:
            del data['email']
        if 'password' in data:
            del data['password']
        
        return UserModel.update_member(user_id, data)

    def hash_password(self, password: str) -> str:
        """Hash password using PBKDF2."""
        return hash_password(password)
