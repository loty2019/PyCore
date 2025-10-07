"""
WebSocket connection manager for real-time updates
"""
from typing import List
from fastapi import WebSocket
from backend.core.logging import logger
import json


class WebSocketManager:
    """Manages WebSocket connections and broadcasts"""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accept and store a new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send a message to a specific WebSocket connection"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")

    async def broadcast(self, message: dict):
        """Broadcast a message to all connected WebSocket clients"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.append(connection)

        # Remove disconnected clients
        for connection in disconnected:
            self.disconnect(connection)

    async def broadcast_position(self, x: float, y: float, z: float, is_moving: bool):
        """Broadcast position update"""
        await self.broadcast({
            "type": "position",
            "data": {
                "x": x,
                "y": y,
                "z": z,
                "is_moving": is_moving
            }
        })

    async def broadcast_job_progress(self, job_id: int, progress: int, total_steps: int, status: str):
        """Broadcast job progress update"""
        await self.broadcast({
            "type": "job_progress",
            "data": {
                "job_id": job_id,
                "progress": progress,
                "total_steps": total_steps,
                "status": status
            }
        })

    async def broadcast_image_captured(self, image_id: int, filename: str, thumbnail_path: str):
        """Broadcast image captured event"""
        await self.broadcast({
            "type": "image_captured",
            "data": {
                "image_id": image_id,
                "filename": filename,
                "thumbnail_path": thumbnail_path
            }
        })

    async def broadcast_status(self, camera: str, stage: str):
        """Broadcast system status update"""
        await self.broadcast({
            "type": "status",
            "data": {
                "camera": camera,
                "stage": stage
            }
        })

    async def broadcast_error(self, component: str, message: str, severity: str = "error"):
        """Broadcast error message"""
        await self.broadcast({
            "type": "error",
            "data": {
                "component": component,
                "message": message,
                "severity": severity
            }
        })


# Global WebSocket manager instance
websocket_manager = WebSocketManager()
