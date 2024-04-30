

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


# Get the server's base URL
    base_url = request.base_url

    # Get the directory path of the current module
    current_directory = os.path.dirname(os.path.realpath(__file__))

    # Create a new folder named 'photos' in the current directory if it doesn't exist
    folder_path = os.path.join(current_directory, "photos")
    os.makedirs(folder_path, exist_ok=True)

    # Save the uploaded photo to the specified folder
    file_location = os.path.join(folder_path, f"{title}.png")  # Assuming the uploaded photo is always in PNG format
    with open(file_location, "wb") as file_object:
        file_object.write(photo.file.read())

    # Construct the URL for the uploaded photo
    photo_url = f"{base_url}photos/{title}.png"