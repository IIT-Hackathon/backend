# crud operation with authorization check for photos
from fastapi import Depends, APIRouter, HTTPException, status, File, UploadFile, Path, Form, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..database import get_db, SessionLocal
from .. import models, oauth2
from ..models import Photo
import shutil
import os
from pydantic import BaseModel
from app.oauth2 import check_authorization

router = APIRouter()

class PhotoResponse(BaseModel):
    id: int
    photo: str
    title: str
    description: str
    category: str
    
# function to download the file uploaded by the user, create new folder if not exist
def save_file(file, file_path):
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
@router.post("/photos", status_code=201, tags=['photo'])
async def upload_photo(request: Request, photo: UploadFile = File(...), title: str = Form(...), description: str = Form(...), category: str = Form(...), user = Depends(oauth2.get_current_user)):
    check_authorization(user)
    
    # Get the server's base URL
    base_url = request.base_url

    # Get the directory path of the current module
    current_directory = os.path.dirname(os.path.realpath(__file__))

    # Create a new folder named 'photos' in the current directory if it doesn't exist
    folder_path = os.path.join(current_directory, "..", "..", "..", "frontend", "src", "assets")
    os.makedirs(folder_path, exist_ok=True)

    # Save the uploaded photo to the specified folder
    file_location = os.path.join(folder_path, f"{title}.png")
    with open(file_location, "wb") as file_object:
        file_object.write(photo.file.read())

    # Construct the URL for the uploaded photo
    photo_url = f"src/assets/{title}.png"

    # Save photo information to the database
    db = SessionLocal()
    db_photo = Photo(photo=photo_url, title=title, description=description, category=category)
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    db.close()

    return {"filename": photo.filename, "title": title, "description": description, "category": category, "photo_url": photo_url}

@router.get("/photos", tags=['photo'])
def get_photos(db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    photos = db.query(models.Photo).all()
    return photos

@router.get("/photos/{photo_id}", tags=['photo'])
def get_photo(photo_id: int, db: Session = Depends(get_db)):
    photo = db.query(models.Photo).filter(models.Photo.id == photo_id).first()
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    return photo

@router.delete("/photos/{photo_id}", status_code = 204, tags=['photo'])
def delete_photo(photo_id: int, db : Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    check_authorization(user)
    photo = db.query(models.Photo).filter(models.Photo.id == photo_id).first()
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    db.delete(photo)
    db.commit()
    return {"detail": "Photo deleted successfully"}