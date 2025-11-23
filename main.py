from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from src.routes import admin, showcase, serve
from src.utils.logger import logger

app = FastAPI(title="AI 产品库")

# Ensure static directory exists
Path("static").mkdir(exist_ok=True)

# Mount static files for the platform itself (css, js)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
from src.routes import management
app.include_router(management.router)

app.include_router(admin.router)
app.include_router(showcase.router)
app.include_router(serve.router)

logger.info("Application started")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
