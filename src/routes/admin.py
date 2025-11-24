from fastapi import APIRouter, Request, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
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

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    apps = db.list_apps(sort_by="views")
    return templates.TemplateResponse("index.html", {"request": request, "apps": apps})

@router.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

from src.config import config

@router.get("/api/check_app")
async def check_app(name: str):
    app = db.get_app_by_name(name)
    if app:
        return {
            "found": True,
            "name": app["name"],
            "author": app["author"],
            "description": app["description"],
            "slug": app["slug"]
        }
    return {"found": False}


@router.post("/api/upload")
async def upload_app(
    name: str = Form(...),
    description: str = Form(None),
    slug: str = Form(None),
    author: str = Form(...),
    password: str = Form(...),
    file: UploadFile = File(None),
    html_content: str = Form(None)
):
    if password != config.upload_password:
        raise HTTPException(status_code=401, detail="Invalid password")

    if not file and not html_content:
        raise HTTPException(status_code=400, detail="Either file or HTML content must be provided")

    if not slug:
        slug = generate_slug()
    
    # Check if slug exists
    existing_app = db.get_app(slug)

    try:
        # Save file (will backup if exists)
        await FileService.save_upload(slug=slug, file=file, html_content=html_content)
        
        if existing_app:
            # Update existing app
            db.update_app(slug=slug, name=name, description=description, author=author)
            logger.info(f"Updated app: {slug}")
        else:
            # Create new app
            db.create_app(slug=slug, name=name, description=description, author=author)
            logger.info(f"Created new app: {slug}")
        
        return RedirectResponse(url=f"/i/{slug}", status_code=303)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/iflow-key")
async def get_iflow_key():
    return {"key": config.iflow_api_key}

@router.post("/api/iflow-key")
async def update_iflow_key(
    key: str = Form(...),
    password: str = Form(...)
):
    if password != config.upload_password:
        raise HTTPException(status_code=401, detail="Invalid password")
    
    try:
        config.update_iflow_key(key)
        return {"status": "success", "key": key}
    except Exception as e:
        logger.error(f"Failed to update iflow key: {e}")
        raise HTTPException(status_code=500, detail=str(e))
