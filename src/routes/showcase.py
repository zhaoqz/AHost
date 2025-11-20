from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from src.database import db
from src.services.qr_service import QRService

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/i/{slug}")
async def showcase_page(request: Request, slug: str):
    app = db.get_app(slug)
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    
    qr_code = QRService.generate_qr_base64(slug)
    
    return templates.TemplateResponse("showcase.html", {
        "request": request,
        "app": app,
        "qr_code": qr_code
    })
