from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app import models, schemas, security
from app.db import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(db: Session, username: str):
    """
    Get the user with the given username
    
    :param db: The database session
    :type db: Session
    :param username: The username of the user to get
    :type username: str
    """
    
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    """
    Get the user with the given email
    
    :param db: The database session
    :type db: Session
    :param email: The email of the user to get
    :type email: str
    """
    
    return db.query(models.User).filter(models.User.email == email).first()


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Get the current user from the token provided
    
    :param db: The database session
    :type db: Session
    :param token: The token to get the user from
    :type token: str
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    try:
        payload = jwt.decode(
            token=token,
            key=security.SECRET_KEY,
            algorithms=security.ALGORITHM
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    
    except JWTError:
        raise credentials_exception
    
    user = get_user(db, username)
    if user is None:
        raise credentials_exception
    
    return user
