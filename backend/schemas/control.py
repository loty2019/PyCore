"""
Pydantic schemas for control endpoints
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CaptureRequest(BaseModel):
    """Request schema for capturing an image"""
    exposure: Optional[int] = 100  # milliseconds
    gain: Optional[float] = 1.0


class CaptureResponse(BaseModel):
    """Response schema for image capture"""
    status: str
    image_id: int
    filename: str
    thumbnail_path: str
    timestamp: datetime


class MoveRequest(BaseModel):
    """Request schema for stage movement"""
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None
    relative: bool = False


class MoveResponse(BaseModel):
    """Response schema for stage movement"""
    status: str
    target_position: dict


class PositionResponse(BaseModel):
    """Response schema for current position"""
    x: float
    y: float
    z: float
    is_moving: bool


class CameraSettings(BaseModel):
    """Camera settings schema"""
    exposure: Optional[int] = None
    gain: Optional[float] = None
    resolution: Optional[dict] = None


class StatusResponse(BaseModel):
    """System status response"""
    camera: str
    stage: str
    database: str
    queue: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    checks: dict
    version: str
    timestamp: datetime
