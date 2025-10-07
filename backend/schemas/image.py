"""
Pydantic schemas for image endpoints
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ImageBase(BaseModel):
    """Base image schema"""
    filename: str
    thumbnail_path: Optional[str] = None
    x_position: Optional[float] = None
    y_position: Optional[float] = None
    z_position: Optional[float] = None
    exposure_time: Optional[int] = None
    gain: Optional[float] = None
    file_size: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    job_id: Optional[int] = None
    metadata: Optional[dict] = {}


class ImageCreate(ImageBase):
    """Schema for creating a new image"""
    pass


class ImageUpdate(BaseModel):
    """Schema for updating an image"""
    filename: Optional[str] = None
    thumbnail_path: Optional[str] = None
    metadata: Optional[dict] = None


class ImageResponse(ImageBase):
    """Schema for image response"""
    id: int
    captured_at: datetime

    class Config:
        from_attributes = True


class ImageListResponse(BaseModel):
    """Schema for listing images"""
    total: int
    skip: int
    limit: int
    images: List[ImageResponse]
