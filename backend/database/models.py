"""
Database models for the microscope control system
"""
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, Text, ForeignKey, CheckConstraint, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base


class Image(Base):
    """Images captured by the microscope"""
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False, unique=True)
    thumbnail_path = Column(String(255))
    captured_at = Column(TIMESTAMP, default=func.now())

    # Position when captured
    x_position = Column(Float)
    y_position = Column(Float)
    z_position = Column(Float)

    # Camera settings
    exposure_time = Column(Integer)  # milliseconds
    gain = Column(Float)

    # File information
    file_size = Column(Integer)  # bytes
    width = Column(Integer)  # pixels
    height = Column(Integer)  # pixels

    # Relationship to job
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True)

    # Additional metadata
    metadata = Column(JSONB, default={})

    # Relationship
    job = relationship("Job", back_populates="images")

    __table_args__ = (
        CheckConstraint("x_position >= 0 AND y_position >= 0 AND z_position >= 0", name="valid_position"),
        Index("idx_images_captured_at", "captured_at"),
        Index("idx_images_job_id", "job_id"),
    )


class Job(Base):
    """Automated jobs (timelapse, grid scans, z-stacks)"""
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)

    # Job type: 'timelapse', 'grid', 'zstack', 'manual'
    job_type = Column(String(50), nullable=False)

    # Status: 'pending', 'running', 'paused', 'completed', 'failed', 'cancelled'
    status = Column(String(50), default="pending")

    # Timestamps
    created_at = Column(TIMESTAMP, default=func.now())
    started_at = Column(TIMESTAMP)
    completed_at = Column(TIMESTAMP)

    # Progress tracking
    progress = Column(Integer, default=0)
    total_steps = Column(Integer)

    # Job-specific parameters
    parameters = Column(JSONB, default={})

    # Error handling
    error_message = Column(Text)
    retry_count = Column(Integer, default=0)

    # Relationship
    images = relationship("Image", back_populates="job")

    __table_args__ = (
        Index("idx_jobs_status", "status"),
        Index("idx_jobs_created_at", "created_at"),
        Index("idx_jobs_type", "job_type"),
    )


class Position(Base):
    """Saved positions for quick navigation"""
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)

    # 3D coordinates
    x_position = Column(Float, nullable=False)
    y_position = Column(Float, nullable=False)
    z_position = Column(Float, nullable=False)

    # Optional: camera settings at this position
    camera_settings = Column(JSONB, default={})

    created_at = Column(TIMESTAMP, default=func.now())

    __table_args__ = (
        CheckConstraint("x_position >= 0 AND y_position >= 0 AND z_position >= 0", name="valid_position"),
        Index("idx_positions_name", "name"),
    )


class SystemLog(Base):
    """System event logging for debugging and audit trail"""
    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(TIMESTAMP, default=func.now())

    # Level: 'debug', 'info', 'warning', 'error', 'critical'
    level = Column(String(20), nullable=False)

    # Component: 'camera', 'stage', 'web', 'job', 'watchdog'
    component = Column(String(50), nullable=False)

    message = Column(Text, nullable=False)

    # Additional structured data
    details = Column(JSONB, default={})

    __table_args__ = (
        Index("idx_logs_timestamp", "timestamp"),
        Index("idx_logs_level", "level"),
        Index("idx_logs_component", "component"),
    )


class Setting(Base):
    """Persistent application settings"""
    __tablename__ = "settings"

    key = Column(String(100), primary_key=True)
    value = Column(JSONB, nullable=False)
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())
    description = Column(Text)
