from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Set
import json
import asyncio

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)

    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients."""
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.add(connection)

        # Clean up disconnected clients
        for conn in disconnected:
            self.active_connections.discard(conn)

    async def send_to_client(self, websocket: WebSocket, message: dict):
        """Send message to a specific client."""
        try:
            await websocket.send_json(message)
        except Exception:
            self.disconnect(websocket)


# Global connection manager
manager = ConnectionManager()


@router.websocket("/pipeline")
async def pipeline_websocket(websocket: WebSocket):
    """WebSocket endpoint for pipeline execution updates."""
    await manager.connect(websocket)

    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()

            try:
                message = json.loads(data)

                if message.get("type") == "ping":
                    await manager.send_to_client(websocket, {"type": "pong"})
                elif message.get("type") == "subscribe":
                    # Client wants to subscribe to specific execution updates
                    execution_id = message.get("execution_id")
                    await manager.send_to_client(websocket, {
                        "type": "subscribed",
                        "execution_id": execution_id,
                    })

            except json.JSONDecodeError:
                await manager.send_to_client(websocket, {
                    "type": "error",
                    "message": "Invalid JSON",
                })

    except WebSocketDisconnect:
        manager.disconnect(websocket)


async def broadcast_node_update(event: dict):
    """Broadcast a node update event to all connected clients."""
    await manager.broadcast(event)


async def broadcast_pipeline_update(event: dict):
    """Broadcast a pipeline update event to all connected clients."""
    await manager.broadcast(event)
