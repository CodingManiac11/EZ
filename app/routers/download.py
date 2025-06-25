from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from .. import models, deps, utils
import os

router = APIRouter(tags=["download"])

@router.get("/download/{token}")
def download_file(token: str, current_user: models.User = Depends(deps.get_current_client_user), db: Session = Depends(deps.get_db)):
    try:
        file_id = utils.decrypt_id(token)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid download token")
    db_file = db.query(models.File).filter(models.File.id == file_id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")
    if not os.path.exists(db_file.filepath):
        raise HTTPException(status_code=404, detail="File missing on server")
    return FileResponse(db_file.filepath, filename=db_file.filename) 