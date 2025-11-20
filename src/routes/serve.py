from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from src.config import config
from src.database import db

router = APIRouter()

@router.get("/{slug}/{path:path}")
async def serve_app_file(slug: str, path: str):
    # Check if app exists in DB (optional, but good for consistency)
    # app = db.get_app(slug)
    # if not app:
    #     raise HTTPException(status_code=404, detail="App not found")

    base_path = config.upload_dir / slug
    file_path = base_path / path

    # Security check: ensure file_path is within base_path
    try:
        file_path.relative_to(base_path)
    except ValueError:
        raise HTTPException(status_code=403, detail="Access denied")

    if file_path.is_dir():
        file_path = file_path / "index.html"

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)

@router.get("/{slug}")
async def serve_app_root(slug: str):
    return await serve_app_file(slug, "")
