

@router.put("/photos/{photo_id}", response_model = Photo, tags=['photo'])
def update_photo(photo_id: int, photo : Photo, db : Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    photo_to_update = db.query(models.Photo).filter(models.Photo.id == photo_id).first()
    if photo_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    for key, value in photo.dict().items():
        setattr(photo_to_update, key, value)
    db.commit()
    db.refresh(photo_to_update)
    return photo_to_update