from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError
from fastapi.security import OAuth2PasswordBearer
from .database import SessionLocal
from .auth import decode_access_token
from .models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/client/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    user = db.query(User).filter(User.id == payload.get("sub")).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_ops_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_ops:
        raise HTTPException(status_code=403, detail="Not authorized as Ops user")
    return current_user

def get_current_client_user(current_user: User = Depends(get_current_user)):
    if current_user.is_ops:
        raise HTTPException(status_code=403, detail="Not authorized as Client user")
    return current_user 