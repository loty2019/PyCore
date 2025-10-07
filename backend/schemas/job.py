"""
Pydantic schemas for job endpoints
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class JobBase(BaseModel):
    """Base job schema"""
    name: str
    description: Optional[str] = None
    job_type: str  # 'timelapse', 'grid', 'zstack', 'manual'
    parameters: dict = {}


class JobCreate(JobBase):
    """Schema for creating a new job"""
    pass


class JobUpdate(BaseModel):
    """Schema for updating a job"""
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None  # 'pending', 'running', 'paused', 'completed', 'failed', 'cancelled'
    parameters: Optional[dict] = None


class JobResponse(JobBase):
    """Schema for job response"""
    id: int
    status: str
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    progress: int
    total_steps: Optional[int] = None
    error_message: Optional[str] = None
    retry_count: int

    class Config:
        from_attributes = True


class JobListResponse(BaseModel):
    """Schema for listing jobs"""
    total: int
    jobs: List[JobResponse]
