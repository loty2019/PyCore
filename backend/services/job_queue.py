"""
Job queue system for automated tasks
"""
import asyncio
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from backend.database.models import Job, Image
from backend.services.camera import camera_service
from backend.services.stage import stage_service
from backend.services.websocket_manager import websocket_manager
from backend.core.logging import logger


class JobQueueService:
    """Service for executing automated jobs"""

    def __init__(self):
        self.running_jobs = {}
        self.is_running = False

    async def execute_job(self, job: Job, db: Session):
        """Execute a job based on its type"""
        try:
            job.status = "running"
            job.started_at = datetime.now()
            db.commit()

            logger.info(f"Starting job {job.id}: {job.name} ({job.job_type})")

            if job.job_type == "timelapse":
                await self._execute_timelapse(job, db)
            elif job.job_type == "grid":
                await self._execute_grid_scan(job, db)
            elif job.job_type == "zstack":
                await self._execute_zstack(job, db)
            else:
                raise ValueError(f"Unknown job type: {job.job_type}")

            job.status = "completed"
            job.completed_at = datetime.now()
            db.commit()

            logger.info(f"Job {job.id} completed successfully")

        except Exception as e:
            logger.error(f"Error executing job {job.id}: {e}")
            job.status = "failed"
            job.error_message = str(e)
            job.completed_at = datetime.now()
            db.commit()

    async def _execute_timelapse(self, job: Job, db: Session):
        """Execute timelapse job"""
        params = job.parameters
        interval = params.get("interval", 60)  # seconds
        duration = params.get("duration", 3600)  # seconds
        exposure = params.get("exposure", 100)
        gain = params.get("gain", 1.0)

        # Calculate total steps
        total_steps = int(duration / interval)
        job.total_steps = total_steps
        db.commit()

        # Set camera settings
        camera_service.set_exposure(exposure)
        camera_service.set_gain(gain)

        for step in range(total_steps):
            if job.status != "running":
                logger.info(f"Job {job.id} paused or cancelled")
                break

            # Capture image
            filename = f"timelapse_{job.id}_{step:04d}.jpg"
            success, img_info = camera_service.capture_image(filename)

            if success:
                # Save image to database
                image = Image(
                    filename=img_info["filename"],
                    job_id=job.id,
                    exposure_time=exposure,
                    gain=gain,
                    width=img_info.get("width"),
                    height=img_info.get("height"),
                    file_size=img_info.get("file_size")
                )
                db.add(image)
                db.commit()

                # Broadcast update
                await websocket_manager.broadcast_image_captured(
                    image.id, image.filename, image.thumbnail_path or ""
                )

            # Update progress
            job.progress = step + 1
            db.commit()

            await websocket_manager.broadcast_job_progress(
                job.id, job.progress, job.total_steps, job.status
            )

            # Wait for interval
            await asyncio.sleep(interval)

    async def _execute_grid_scan(self, job: Job, db: Session):
        """Execute grid scan job"""
        params = job.parameters
        start_x = params.get("start_x", 0)
        end_x = params.get("end_x", 1000)
        step_x = params.get("step_x", 100)
        start_y = params.get("start_y", 0)
        end_y = params.get("end_y", 1000)
        step_y = params.get("step_y", 100)
        z_position = params.get("z_position", 0)
        exposure = params.get("exposure", 100)
        gain = params.get("gain", 1.0)

        # Calculate total steps
        x_steps = int((end_x - start_x) / step_x) + 1
        y_steps = int((end_y - start_y) / step_y) + 1
        total_steps = x_steps * y_steps
        job.total_steps = total_steps
        db.commit()

        # Set camera settings
        camera_service.set_exposure(exposure)
        camera_service.set_gain(gain)

        step_count = 0
        for y in range(start_y, end_y + 1, step_y):
            for x in range(start_x, end_x + 1, step_x):
                if job.status != "running":
                    logger.info(f"Job {job.id} paused or cancelled")
                    return

                # Move to position
                await stage_service.move(x, y, z_position)

                # Capture image
                filename = f"grid_{job.id}_x{x}_y{y}.jpg"
                success, img_info = camera_service.capture_image(filename)

                if success:
                    # Save image to database
                    image = Image(
                        filename=img_info["filename"],
                        job_id=job.id,
                        x_position=x,
                        y_position=y,
                        z_position=z_position,
                        exposure_time=exposure,
                        gain=gain,
                        width=img_info.get("width"),
                        height=img_info.get("height"),
                        file_size=img_info.get("file_size")
                    )
                    db.add(image)
                    db.commit()

                    await websocket_manager.broadcast_image_captured(
                        image.id, image.filename, image.thumbnail_path or ""
                    )

                # Update progress
                step_count += 1
                job.progress = step_count
                db.commit()

                await websocket_manager.broadcast_job_progress(
                    job.id, job.progress, job.total_steps, job.status
                )

    async def _execute_zstack(self, job: Job, db: Session):
        """Execute z-stack job"""
        params = job.parameters
        x_position = params.get("x_position", 0)
        y_position = params.get("y_position", 0)
        start_z = params.get("start_z", 0)
        end_z = params.get("end_z", 1000)
        step_z = params.get("step_z", 50)
        exposure = params.get("exposure", 100)
        gain = params.get("gain", 1.0)

        # Calculate total steps
        total_steps = int((end_z - start_z) / step_z) + 1
        job.total_steps = total_steps
        db.commit()

        # Set camera settings
        camera_service.set_exposure(exposure)
        camera_service.set_gain(gain)

        # Move to XY position
        await stage_service.move(x_position, y_position, start_z)

        step_count = 0
        for z in range(start_z, end_z + 1, step_z):
            if job.status != "running":
                logger.info(f"Job {job.id} paused or cancelled")
                return

            # Move to Z position
            await stage_service.move(z=z)

            # Capture image
            filename = f"zstack_{job.id}_z{z}.jpg"
            success, img_info = camera_service.capture_image(filename)

            if success:
                # Save image to database
                image = Image(
                    filename=img_info["filename"],
                    job_id=job.id,
                    x_position=x_position,
                    y_position=y_position,
                    z_position=z,
                    exposure_time=exposure,
                    gain=gain,
                    width=img_info.get("width"),
                    height=img_info.get("height"),
                    file_size=img_info.get("file_size")
                )
                db.add(image)
                db.commit()

                await websocket_manager.broadcast_image_captured(
                    image.id, image.filename, image.thumbnail_path or ""
                )

            # Update progress
            step_count += 1
            job.progress = step_count
            db.commit()

            await websocket_manager.broadcast_job_progress(
                job.id, job.progress, job.total_steps, job.status
            )


# Global job queue service instance
job_queue_service = JobQueueService()
