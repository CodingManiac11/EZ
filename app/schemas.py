from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    is_ops: bool
    class Config:
        orm_mode = True

class FileOut(BaseModel):
    id: int
    filename: str
    uploaded_at: datetime
    owner_id: int
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class DownloadLinkResponse(BaseModel):
    download_link: str
    message: str 