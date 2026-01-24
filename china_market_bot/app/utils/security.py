"""
🔐 Security Utilities Module

Encryption, hashing, and JWT utilities.
"""

import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
import jwt
from cryptography.fernet import Fernet

from app.config import settings


class PasswordHasher:
    """
    Password hashing utility using bcrypt.
    """
    
    @staticmethod
    def hash(password: str) -> str:
        """
        Hash password using bcrypt.
        
        Args:
            password: Plain text password
        
        Returns:
            Hashed password
        """
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode(), salt).decode()
    
    @staticmethod
    def verify(password: str, hashed: str) -> bool:
        """
        Verify password against hash.
        
        Args:
            password: Plain text password
            hashed: Hashed password
        
        Returns:
            True if password matches
        """
        try:
            return bcrypt.checkpw(password.encode(), hashed.encode())
        except Exception:
            return False


class JWTHandler:
    """
    JWT token handler for authentication.
    """
    
    def __init__(
        self,
        secret_key: str = None,
        algorithm: str = "HS256",
    ):
        """
        Initialize JWT handler.
        
        Args:
            secret_key: Secret key for signing
            algorithm: JWT algorithm
        """
        self.secret_key = secret_key or settings.secret_key
        self.algorithm = algorithm or settings.jwt_algorithm
    
    def create_access_token(
        self,
        user_id: int,
        role: str,
        expires_delta: timedelta = None,
    ) -> str:
        """
        Create access token.
        
        Args:
            user_id: User ID
            role: User role
            expires_delta: Token expiration time
        
        Returns:
            JWT token string
        """
        if expires_delta is None:
            expires_delta = timedelta(hours=settings.access_token_expire_hours)
        
        expire = datetime.utcnow() + expires_delta
        
        payload = {
            "sub": str(user_id),
            "role": role,
            "exp": expire,
            "iat": datetime.utcnow(),
            "jti": secrets.token_hex(16),
        }
        
        return jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm,
        )
    
    def verify_token(self, token: str) -> Optional[dict]:
        """
        Verify and decode token.
        
        Args:
            token: JWT token string
        
        Returns:
            Decoded payload or None if invalid
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def get_user_id(self, token: str) -> Optional[int]:
        """
        Get user ID from token.
        
        Args:
            token: JWT token string
        
        Returns:
            User ID or None
        """
        payload = self.verify_token(token)
        if payload:
            try:
                return int(payload.get("sub"))
            except (ValueError, TypeError):
                return None
        return None


class DataEncryption:
    """
    Data encryption utility using Fernet.
    """
    
    def __init__(self, key: bytes = None):
        """
        Initialize encryption handler.
        
        Args:
            key: Fernet key (32 bytes base64 encoded)
        """
        if key is None:
            key = settings.encryption_key
            if key:
                key = key.encode()
            else:
                key = Fernet.generate_key()
        
        self.cipher = Fernet(key)
    
    def encrypt(self, data: str) -> str:
        """
        Encrypt string data.
        
        Args:
            data: Plain text data
        
        Returns:
            Encrypted data as base64 string
        """
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypt encrypted data.
        
        Args:
            encrypted_data: Encrypted data as base64 string
        
        Returns:
            Decrypted plain text
        """
        return self.cipher.decrypt(encrypted_data.encode()).decode()


def generate_token(length: int = 32) -> str:
    """
    Generate secure random token.
    
    Args:
        length: Token length in bytes
    
    Returns:
        Hex token string
    """
    return secrets.token_hex(length)


def generate_otp(length: int = 6) -> str:
    """
    Generate numeric OTP code.
    
    Args:
        length: OTP length
    
    Returns:
        Numeric OTP string
    """
    return "".join(str(secrets.randbelow(10)) for _ in range(length))


def hash_string(data: str, salt: str = "") -> str:
    """
    Hash string using SHA256.
    
    Args:
        data: String to hash
        salt: Optional salt
    
    Returns:
        Hex hash string
    """
    return hashlib.sha256((data + salt).encode()).hexdigest()


def verify_signature(
    data: str,
    signature: str,
    secret: str,
) -> bool:
    """
    Verify HMAC signature.
    
    Args:
        data: Original data
        signature: Signature to verify
        secret: Secret key
    
    Returns:
        True if signature is valid
    """
    expected = hmac.new(
        secret.encode(),
        data.encode(),
        hashlib.sha256,
    ).hexdigest()
    
    return hmac.compare_digest(expected, signature)


def create_signature(data: str, secret: str) -> str:
    """
    Create HMAC signature.
    
    Args:
        data: Data to sign
        secret: Secret key
    
    Returns:
        Signature hex string
    """
    return hmac.new(
        secret.encode(),
        data.encode(),
        hashlib.sha256,
    ).hexdigest()


# Global instances
password_hasher = PasswordHasher()
jwt_handler = JWTHandler()
