"""
WebSocket endpoint for real-time updates
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.services.websocket_manager import websocket_manager
from backend.core.logging import logger

router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket_manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and receive messages
            data = await websocket.receive_text()
            logger.debug(f"Received WebSocket message: {data}")

            # Echo back for testing
            await websocket_manager.send_personal_message(
                {"type": "echo", "data": data},
                websocket
            )

    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        websocket_manager.disconnect(websocket)
