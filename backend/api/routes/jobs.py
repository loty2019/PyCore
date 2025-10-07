"""
Job management endpoints
"""
from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional
from backend.api.deps import get_db
from backend.schemas.job import JobCreate, JobUpdate, JobResponse, JobListResponse
from backend.database.models import Job
from backend.services.job_queue import job_queue_service
from backend.core.logging import logger

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])


@router.get("", response_model=JobListResponse)
async def list_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[str] = None,
    job_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all jobs with filtering"""
    query = db.query(Job)

    # Apply filters
    if status:
        query = query.filter(Job.status == status)
    if job_type:
        query = query.filter(Job.job_type == job_type)

    # Get total count
    total = query.count()

    # Get paginated results
    jobs = query.order_by(Job.created_at.desc()).offset(skip).limit(limit).all()

    return JobListResponse(total=total, jobs=jobs)


@router.post("", response_model=JobResponse)
async def create_job(
    job_data: JobCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create a new job"""
    try:
        # Create job in database
        job = Job(
            name=job_data.name,
            description=job_data.description,
            job_type=job_data.job_type,
            parameters=job_data.parameters,
            status="pending"
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        logger.info(f"Job created: {job.id} - {job.name}")

        # Start job execution in background
        background_tasks.add_task(job_queue_service.execute_job, job, db)

        return job

    except Exception as e:
        logger.error(f"Error creating job: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: int, db: Session = Depends(get_db)):
    """Get job details"""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job


@router.patch("/{job_id}", response_model=JobResponse)
async def update_job(job_id: int, job_data: JobUpdate, db: Session = Depends(get_db)):
    """Update job status (pause/resume/cancel)"""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    try:
        # Update fields
        if job_data.name:
            job.name = job_data.name
        if job_data.description:
            job.description = job_data.description
        if job_data.status:
            job.status = job_data.status
            logger.info(f"Job {job_id} status changed to {job_data.status}")
        if job_data.parameters:
            job.parameters = job_data.parameters

        db.commit()
        db.refresh(job)

        return job

    except Exception as e:
        logger.error(f"Error updating job {job_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{job_id}")
async def delete_job(job_id: int, db: Session = Depends(get_db)):
    """Delete a job and its associated images"""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    try:
        # Delete job (images will be set to NULL due to ON DELETE SET NULL)
        db.delete(job)
        db.commit()

        logger.info(f"Job {job_id} deleted")

        return {"status": "deleted", "message": "Job deleted successfully"}

    except Exception as e:
        logger.error(f"Error deleting job {job_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
