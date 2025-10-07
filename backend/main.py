"""
Microscope Control System - Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from backend.config import get_settings
from backend.core.logging import logger
from backend.database.base import Base
from backend.database.session import engine
from backend.services.camera import camera_service
from backend.services.stage import stage_service

# Import routes
from backend.api.routes import control, images, jobs, positions, websocket

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events for the application"""
    # Startup
    logger.info("Starting Microscope Control System...")

    # Create database tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created/verified")

    # Create necessary directories
    os.makedirs(settings.IMAGES_PATH, exist_ok=True)
    os.makedirs(settings.THUMBNAILS_PATH, exist_ok=True)
    logger.info("Storage directories created/verified")

    # Initialize camera
    if camera_service.initialize():
        logger.info("Camera initialized successfully")
    else:
        logger.warning("Camera initialization failed - running without camera")

    # Connect to stage
    if await stage_service.connect():
        logger.info("Stage controller connected")
    else:
        logger.warning("Stage controller connection failed - running without stage")

    logger.info("Application started successfully")

    yield

    # Shutdown
    logger.info("Shutting down Microscope Control System...")
    camera_service.uninitialize()
    await stage_service.disconnect()
    logger.info("Application shut down complete")


# Create FastAPI application
app = FastAPI(
    title="Microscope Control API",
    description="""
    ## Microscope Control System API

    Control microscope camera, motorized stage, and automated jobs.

    ### Features
    * **Camera Control**: Capture images with custom exposure and gain
    * **Stage Control**: Move X/Y/Z axes with position validation
    * **Job Automation**: Timelapse, grid scans, z-stacks
    * **Real-time Updates**: WebSocket for live position and status
    * **Image Management**: Store, retrieve, and delete images

    ### Safety Features
    * Position validation before movement
    * Watchdog timers for hardware operations
    * Emergency stop functionality
    """,
    version="1.0.0",
    contact={
        "name": "Microscope Lab",
        "email": "lab@example.com",
    },
    license_info={
        "name": "MIT",
    },
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(control.router)
app.include_router(images.router)
app.include_router(jobs.router)
app.include_router(positions.router)
app.include_router(websocket.router)

# Serve static files (frontend)
if os.path.exists("frontend"):
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


@app.get("/api")
async def root():
    """API root endpoint"""
    return {
        "message": "Microscope Control System API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/control/health"
    }


if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting server on {settings.HOST}:{settings.PORT}")

    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
