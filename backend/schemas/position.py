"""
Pydantic schemas for position endpoints
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class PositionBase(BaseModel):
    """Base position schema"""
    name: str
    description: Optional[str] = None
    x_position: float
    y_position: float
    z_position: float
    camera_settings: Optional[dict] = {}


class PositionCreate(PositionBase):
    """Schema for creating a new position"""
    pass


class PositionUpdate(BaseModel):
    """Schema for updating a position"""
    name: Optional[str] = None
    description: Optional[str] = None
    x_position: Optional[float] = None
    y_position: Optional[float] = None
    z_position: Optional[float] = None
    camera_settings: Optional[dict] = None


class PositionResponse(PositionBase):
    """Schema for position response"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PositionListResponse(BaseModel):
    """Schema for listing positions"""
    positions: List[PositionResponse]
