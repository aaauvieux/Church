from fastapi import File,UploadFile
import uuid

IMAGEDIR = "issets/avatar/"

async def upload_image(file: UploadFile = File(...)):
    file.filename=f"{uuid.uuid4()}.jpg"
    contens = await file.read()
    
    #Save the file
    with open(f"{IMAGEDIR}{file.filename}","wb") as f:
        f.write(contens)
        
    return {"filename": file.filename}


 