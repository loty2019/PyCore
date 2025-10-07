"""
Control endpoints for camera and stage
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from backend.api.deps import get_db
from backend.schemas.control import (
    CaptureRequest, CaptureResponse, MoveRequest, MoveResponse,
    PositionResponse, CameraSettings, StatusResponse, HealthResponse
)
from backend.services.camera import camera_service
from backend.services.stage import stage_service
from backend.services.image_service import image_service
from backend.services.websocket_manager import websocket_manager
from backend.database.models import Image
from backend.core.watchdog import PositionValidator
from backend.core.logging import logger

router = APIRouter(prefix="/api/control", tags=["Control"])


@router.post("/capture", response_model=CaptureResponse)
async def capture_image(request: CaptureRequest, db: Session = Depends(get_db)):
    """Capture an image from the camera"""
    try:
        # Set camera settings
        if request.exposure:
            camera_service.set_exposure(request.exposure)
        if request.gain:
            camera_service.set_gain(request.gain)

        # Get current position
        position = stage_service.get_position()

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"image_{timestamp}.jpg"

        # Capture image
        success, img_info = camera_service.capture_image(filename)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to capture image")

        # Create thumbnail
        thumbnail_path = image_service.create_thumbnail(img_info["filename"])

        # Save to database
        image = Image(
            filename=img_info["filename"],
            thumbnail_path=thumbnail_path,
            x_position=position["x"],
            y_position=position["y"],
            z_position=position["z"],
            exposure_time=request.exposure,
            gain=request.gain,
            width=img_info.get("width"),
            height=img_info.get("height"),
            file_size=img_info.get("file_size")
        )
        db.add(image)
        db.commit()
        db.refresh(image)

        # Broadcast to websocket clients
        await websocket_manager.broadcast_image_captured(
            image.id, image.filename, thumbnail_path or ""
        )

        logger.info(f"Image captured: {filename} (ID: {image.id})")

        return CaptureResponse(
            status="success",
            image_id=image.id,
            filename=image.filename,
            thumbnail_path=thumbnail_path or "",
            timestamp=image.captured_at
        )

    except Exception as e:
        logger.error(f"Error capturing image: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/move", response_model=MoveResponse)
async def move_stage(request: MoveRequest):
    """Move the motorized stage"""
    try:
        # Validate position if absolute move
        if not request.relative:
            is_valid, error_msg = PositionValidator.validate_position(
                request.x, request.y, request.z
            )
            if not is_valid:
                raise HTTPException(status_code=400, detail=error_msg)

        # Move stage
        success, position = await stage_service.move(
            request.x, request.y, request.z, request.relative
        )

        if not success:
            raise HTTPException(status_code=500, detail="Failed to move stage")

        # Broadcast position update
        await websocket_manager.broadcast_position(
            position["x"], position["y"], position["z"], False
        )

        return MoveResponse(
            status="moving" if stage_service.is_moving else "complete",
            target_position=position
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error moving stage: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/position", response_model=PositionResponse)
async def get_position():
    """Get current stage position"""
    position = stage_service.get_position()
    return PositionResponse(**position)


@router.post("/home")
async def home_stage():
    """Home all axes"""
    try:
        success, position = await stage_service.home()
        if not success:
            raise HTTPException(status_code=500, detail="Failed to home stage")

        return {"status": "homing", "message": "Homing in progress"}

    except Exception as e:
        logger.error(f"Error homing stage: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stop")
async def emergency_stop():
    """Emergency stop - halt all movement"""
    try:
        success = await stage_service.stop()
        if not success:
            raise HTTPException(status_code=500, detail="Failed to stop stage")

        return {"status": "stopped", "message": "All movement stopped"}

    except Exception as e:
        logger.error(f"Error stopping stage: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/camera/settings", response_model=CameraSettings)
async def get_camera_settings():
    """Get current camera settings"""
    settings = camera_service.get_settings()
    return CameraSettings(**settings)


@router.put("/camera/settings")
async def update_camera_settings(settings: CameraSettings):
    """Update camera settings"""
    try:
        if settings.exposure:
            camera_service.set_exposure(settings.exposure)
        if settings.gain:
            camera_service.set_gain(settings.gain)

        return {"status": "success", "message": "Camera settings updated"}

    except Exception as e:
        logger.error(f"Error updating camera settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status", response_model=StatusResponse)
async def get_status():
    """Get system status"""
    return StatusResponse(
        camera="connected" if camera_service.is_initialized else "disconnected",
        stage="connected" if stage_service.is_connected else "disconnected",
        database="connected",
        queue="running"
    )


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        checks={
            "database": True,
            "raspberry_pi": stage_service.is_connected,
            "camera": camera_service.is_initialized
        },
        version="1.0.0",
        timestamp=datetime.now()
    )
