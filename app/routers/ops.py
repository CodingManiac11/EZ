from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from .. import models, schemas, auth, deps
from fastapi.security import OAuth2PasswordRequestForm
import os

router = APIRouter(prefix="/ops", tags=["ops"])

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(deps.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username, models.User.is_ops == True).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token = auth.create_access_token({"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/upload")
def upload_file(file: UploadFile = File(...), current_user: models.User = Depends(deps.get_current_ops_user), db: Session = Depends(deps.get_db)):
    allowed_types = ["application/vnd.openxmlformats-officedocument.presentationml.presentation", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type")
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    db_file = models.File(filename=file.filename, filepath=file_location, owner_id=current_user.id)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return {"filename": file.filename, "message": "File uploaded successfully"} 