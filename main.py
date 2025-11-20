from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.routes import admin, showcase, serve
from src.utils.logger import logger

app = FastAPI(title="AI-App Host Platform")

# Ensure static directory exists
Path("static").mkdir(exist_ok=True)

# Mount static files for the platform itself (css, js)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(admin.router)
app.include_router(showcase.router)
app.include_router(serve.router)

logger.info("Application started")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
