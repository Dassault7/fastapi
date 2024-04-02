from datetime import timedelta

from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app import auth, schemas, models, security
from app.db import get_db


router = APIRouter()


@router.post("/token", responses={
    200: {"model": schemas.Token, "description": "Get a token for the given user"},
    400: {"description": "Incorrect username or password"}
})
async def token(from_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Get a token for the given user
    """
    
    print(from_data.username, from_data.password)
    
    user = auth.get_user(db, from_data.username)
    if not user or not security.verify_password(from_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token = security.create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", responses={
    201: {"model": schemas.UserInDBBase, "description": "Register a new user"},
    400: {"description": "User already exists"}
})
async def register(user_in: schemas.UserIn, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    
    if auth.get_user(db, user_in.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    if auth.get_user_by_email(db, user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = security.get_password_hash(user_in.password)
    user = models.User(**user_in.model_dump(exclude={"password"}), hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/protected", responses={
    200: {"description": "Protected route"},
    401: {"description": "Unauthorized"}
})
async def protected(current_user: schemas.UserInDB = Depends(auth.get_current_user)):
    """
    Protected route
    """
    
    return {"message": f"Hello {current_user.username}!"}