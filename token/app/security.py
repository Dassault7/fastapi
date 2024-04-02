"""
token: Security for the token app
"""
from typing import Optional
from datetime import datetime, timedelta, UTC

import bcrypt
from jose import jwt

SECRET_KEY = "erKsyJO-fHsfF_H6WWiZ60UNES6wN2lEn-W_zR1bI0o"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_password_hash(password: str):
    """
    Get the password hash for the given password
    
    :param password: The password to hash
    :type password: str
    """
    
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def verify_password(plain_password: str, hashed_password: bytes):
    """
    Verify the given plain password against the hashed password
    
    :param plain_password: The plain password to verify
    :type plain_password: str
    :param hashed_password: The hashed password to verify against
    :type hashed_password: str
    """
    
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password)



def create_access_token(data: dict):
    """
    Create an access token for the given data
    
    :param data: The data to include in the token
    :type data: dict
    :param expires_delta: The time delta for the token to expire
    :type expires_delta: Optional[timedelta]
    """
    
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt