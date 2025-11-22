from fastapi import APIRouter, Request, Form, HTTPException, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from src.database import db
from src.config import config
from src.utils.logger import logger

router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
@router.get("", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("admin/login.html", {"request": request})

@router.post("/login")
async def login(password: str = Form(...)):
    if password == config.upload_password:
        response = RedirectResponse(url="/admin/dashboard", status_code=303)
        response.set_cookie(key="admin_token", value=password)
        return response
    return RedirectResponse(url="/admin?error=Invalid password", status_code=303)

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    token = request.cookies.get("admin_token")
    if token != config.upload_password:
        return RedirectResponse(url="/admin")
    
    apps = db.list_apps(sort_by="created")
    return templates.TemplateResponse("admin/dashboard.html", {"request": request, "apps": apps})

@router.get("/edit/{slug}", response_class=HTMLResponse)
async def edit_page(request: Request, slug: str):
    token = request.cookies.get("admin_token")
    if token != config.upload_password:
        return RedirectResponse(url="/admin")
    
    app = db.get_app(slug)
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
        
    return templates.TemplateResponse("admin/edit.html", {"request": request, "app": app})

@router.post("/api/edit/{slug}")
async def edit_app(
    slug: str,
    request: Request,
    name: str = Form(...),
    description: str = Form(None),
    author: str = Form(...)
):
    token = request.cookies.get("admin_token")
    if token != config.upload_password:
        raise HTTPException(status_code=401, detail="Unauthorized")
        
    db.update_app(slug=slug, name=name, description=description, author=author)
    logger.info(f"Admin updated app: {slug}")
    return RedirectResponse(url="/admin/dashboard", status_code=303)

@router.post("/api/delete/{slug}")
async def delete_app(slug: str, request: Request):
    token = request.cookies.get("admin_token")
    if token != config.upload_password:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Note: Database class doesn't have delete_app yet, need to add it or use raw query if I can't modify db class easily?
    # I should check database.py again. It didn't have delete_app.
    # I'll add delete_app to database.py first or now.
    # For now, I'll just add the route and then update database.py.
    
    # Actually, I should update database.py first or concurrently.
    # I'll assume I'll update database.py next.
    db.delete_app(slug) 
    logger.info(f"Admin deleted app: {slug}")
    return RedirectResponse(url="/admin/dashboard", status_code=303)

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/admin")
    response.delete_cookie("admin_token")
    return response
