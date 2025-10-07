"""
Position management endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.api.deps import get_db
from backend.schemas.position import (
    PositionCreate, PositionUpdate, PositionResponse, PositionListResponse
)
from backend.database.models import Position
from backend.services.stage import stage_service
from backend.core.watchdog import PositionValidator
from backend.core.logging import logger

router = APIRouter(prefix="/api/positions", tags=["Positions"])


@router.get("", response_model=PositionListResponse)
async def list_positions(db: Session = Depends(get_db)):
    """List all saved positions"""
    positions = db.query(Position).order_by(Position.created_at.desc()).all()
    return PositionListResponse(positions=positions)


@router.post("", response_model=PositionResponse)
async def create_position(position_data: PositionCreate, db: Session = Depends(get_db)):
    """Save current or specified position"""
    try:
        # Validate position
        is_valid, error_msg = PositionValidator.validate_position(
            position_data.x_position,
            position_data.y_position,
            position_data.z_position
        )
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)

        # Create position
        position = Position(
            name=position_data.name,
            description=position_data.description,
            x_position=position_data.x_position,
            y_position=position_data.y_position,
            z_position=position_data.z_position,
            camera_settings=position_data.camera_settings
        )
        db.add(position)
        db.commit()
        db.refresh(position)

        logger.info(f"Position saved: {position.name} (ID: {position.id})")

        return position

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error saving position: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{position_id}", response_model=PositionResponse)
async def get_position(position_id: int, db: Session = Depends(get_db)):
    """Get specific position details"""
    position = db.query(Position).filter(Position.id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")

    return position


@router.post("/{position_id}/goto")
async def goto_position(position_id: int, db: Session = Depends(get_db)):
    """Move to saved position"""
    position = db.query(Position).filter(Position.id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")

    try:
        # Move to position
        success, result = await stage_service.move(
            position.x_position,
            position.y_position,
            position.z_position
        )

        if not success:
            raise HTTPException(status_code=500, detail="Failed to move to position")

        return {
            "status": "moving",
            "target_position": result
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error moving to position {position_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{position_id}", response_model=PositionResponse)
async def update_position(
    position_id: int,
    position_data: PositionUpdate,
    db: Session = Depends(get_db)
):
    """Update a saved position"""
    position = db.query(Position).filter(Position.id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")

    try:
        # Validate new position if provided
        if (position_data.x_position is not None or
            position_data.y_position is not None or
            position_data.z_position is not None):

            x = position_data.x_position if position_data.x_position is not None else position.x_position
            y = position_data.y_position if position_data.y_position is not None else position.y_position
            z = position_data.z_position if position_data.z_position is not None else position.z_position

            is_valid, error_msg = PositionValidator.validate_position(x, y, z)
            if not is_valid:
                raise HTTPException(status_code=400, detail=error_msg)

        # Update fields
        if position_data.name:
            position.name = position_data.name
        if position_data.description:
            position.description = position_data.description
        if position_data.x_position is not None:
            position.x_position = position_data.x_position
        if position_data.y_position is not None:
            position.y_position = position_data.y_position
        if position_data.z_position is not None:
            position.z_position = position_data.z_position
        if position_data.camera_settings:
            position.camera_settings = position_data.camera_settings

        db.commit()
        db.refresh(position)

        logger.info(f"Position {position_id} updated")

        return position

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating position {position_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{position_id}")
async def delete_position(position_id: int, db: Session = Depends(get_db)):
    """Delete saved position"""
    position = db.query(Position).filter(Position.id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")

    try:
        db.delete(position)
        db.commit()

        logger.info(f"Position {position_id} deleted")

        return {"status": "deleted", "message": "Position deleted successfully"}

    except Exception as e:
        logger.error(f"Error deleting position {position_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
