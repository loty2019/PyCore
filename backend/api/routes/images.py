"""
Image management endpoints
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from backend.api.deps import get_db
from backend.schemas.image import ImageResponse, ImageListResponse
from backend.database.models import Image
from backend.services.image_service import image_service
from backend.core.logging import logger

router = APIRouter(prefix="/api/images", tags=["Images"])


@router.get("", response_model=ImageListResponse)
async def list_images(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    job_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """List images with pagination and filtering"""
    query = db.query(Image)

    # Apply filters
    if job_id is not None:
        query = query.filter(Image.job_id == job_id)
    if start_date:
        query = query.filter(Image.captured_at >= start_date)
    if end_date:
        query = query.filter(Image.captured_at <= end_date)

    # Get total count
    total = query.count()

    # Get paginated results
    images = query.order_by(Image.captured_at.desc()).offset(skip).limit(limit).all()

    return ImageListResponse(
        total=total,
        skip=skip,
        limit=limit,
        images=images
    )


@router.get("/{image_id}", response_model=ImageResponse)
async def get_image(image_id: int, db: Session = Depends(get_db)):
    """Get specific image details"""
    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    return image


@router.delete("/{image_id}")
async def delete_image(image_id: int, db: Session = Depends(get_db)):
    """Delete an image"""
    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    try:
        # Delete files
        image_service.delete_image(image.filename, image.thumbnail_path)

        # Delete from database
        db.delete(image)
        db.commit()

        logger.info(f"Image {image_id} deleted")

        return {"status": "deleted", "message": "Image deleted successfully"}

    except Exception as e:
        logger.error(f"Error deleting image {image_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
