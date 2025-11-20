from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from src.database import db
from src.services.qr_service import QRService
from src.config import config

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/i/{slug}", response_class=HTMLResponse)
async def showcase_app(request: Request, slug: str):
    app = db.get_app(slug)
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    
    qr_base64 = QRService.generate_qr_base64(f"{config.base_url}/{slug}")
    comments = db.get_comments(slug)
    
    return templates.TemplateResponse(
        "showcase.html", 
        {
            "request": request, 
            "app": app, 
            "qr_code": qr_base64,
            "comments": comments
        }
    )

@router.post("/api/comment/{slug}")
async def add_comment(slug: str, content: str = Form(...), author: str = Form("Anonymous")):
    app = db.get_app(slug)
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    
    db.add_comment(slug, content, author)
    return RedirectResponse(url=f"/i/{slug}", status_code=303)
