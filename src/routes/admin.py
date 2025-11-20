from fastapi import APIRouter, Request, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import random
import string
from src.database import db
from src.services.file_service import FileService
from src.utils.logger import logger

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def generate_slug(length=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

@router.get("/")
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

from src.config import config

@router.post("/api/upload")
async def upload_app(
    name: str = Form(...),
    description: str = Form(None),
    slug: str = Form(None),
    author: str = Form(...),
    password: str = Form(...),
    file: UploadFile = File(...)
):
    if password != config.upload_password:
        raise HTTPException(status_code=401, detail="Invalid password")

    if not slug:
        slug = generate_slug()
    
    # Check if slug exists
    existing_app = db.get_app(slug)

    try:
        # Save file (will backup if exists)
        await FileService.save_upload(file, slug)
        
        if existing_app:
            # Update existing app
            db.update_app(slug=slug, name=name, description=description, author=author)
            logger.info(f"Updated app: {slug}")
        else:
            # Create new app
            db.create_app(slug=slug, name=name, description=description, author=author)
            logger.info(f"Created new app: {slug}")
        
        return RedirectResponse(url=f"/i/{slug}", status_code=303)
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
