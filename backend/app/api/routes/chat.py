from fastapi import APIRouter, HTTPException
from typing import Optional

from app.models.message import ChatRequest, ChatResponse, Message, MessageRole
from app.core.pipeline import PipelineExecutor
from app.core.pipeline_store import pipeline_store

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """Send a message through the consensus pipeline."""
    # Get pipeline config
    pipeline_id = request.pipeline_id or "default"
    pipeline_config = pipeline_store.get(pipeline_id)

    if not pipeline_config:
        raise HTTPException(status_code=404, detail=f"Pipeline '{pipeline_id}' not found")

    # Create pipeline executor
    executor = PipelineExecutor(pipeline_config)

    # Execute pipeline
    try:
        result = await executor.execute(request.message)

        return ChatResponse(
            message=Message(
                role=MessageRole.ASSISTANT,
                content=result.final_output or "",
            ),
            pipeline_execution_id=result.execution_id,
            consensus_score=result.consensus_score,
            node_responses=[
                {
                    "node_id": node_id,
                    "status": state.status.value,
                    "output": state.output,
                }
                for node_id, state in result.node_states.items()
            ],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
async def get_chat_history(conversation_id: Optional[str] = None):
    """Get chat history for a conversation."""
    # TODO: Implement persistent storage
    return {"messages": [], "conversation_id": conversation_id}
