from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from .. import models, schemas, auth, deps, utils, email_utils
from fastapi.security import OAuth2PasswordRequestForm
from ..database import SessionLocal
from fastapi.responses import FileResponse
import os

router = APIRouter(prefix="/client", tags=["client"])

@router.post("/signup")
def signup(user: schemas.UserCreate, request: Request, db: Session = Depends(deps.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password, is_active=False, is_ops=False)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # Generate verification token
    import uuid
    token = str(uuid.uuid4())
    verify_token = models.EmailVerificationToken(user_id=new_user.id, token=token)
    db.add(verify_token)
    db.commit()
    # Send email
    verify_url = str(request.base_url) + f"client/verify-email?token={token}"
    email_utils.send_verification_email(new_user.email, verify_url)
    # Return encrypted URL
    encrypted_url = str(request.base_url) + f"client/verify-email?token={token}"
    return {"verify_url": encrypted_url, "message": "Signup successful. Please verify your email."}

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(deps.get_db)):
    db_token = db.query(models.EmailVerificationToken).filter(models.EmailVerificationToken.token == token).first()
    if not db_token:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user = db.query(models.User).filter(models.User.id == db_token.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    user.is_active = True
    db.delete(db_token)
    db.commit()
    return {"message": "Email verified successfully"}

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(deps.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username, models.User.is_ops == False).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token = auth.create_access_token({"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/files", response_model=list[schemas.FileOut])
def list_files(current_user: models.User = Depends(deps.get_current_client_user), db: Session = Depends(deps.get_db)):
    files = db.query(models.File).all()
    return files

@router.get("/download-file/{file_id}", response_model=schemas.DownloadLinkResponse)
def get_download_link(file_id: int, current_user: models.User = Depends(deps.get_current_client_user)):
    from ..utils import encrypt_id
    token = encrypt_id(file_id)
    download_link = f"/download/{token}"
    return {"download_link": download_link, "message": "success"} 