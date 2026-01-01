from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class NodeStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"


class NodeRole(str, Enum):
    GENERATOR = "generator"
    AGGREGATOR = "aggregator"
    FINAL = "final"


class NodeConfig(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    provider: str  # openai, anthropic, google, mistral, local
    model: str
    role: NodeRole = NodeRole.GENERATOR
    temperature: float = 0.7
    max_tokens: int = 2048
    system_prompt: Optional[str] = None


class NodeState(BaseModel):
    node_id: str
    status: NodeStatus = NodeStatus.PENDING
    output: Optional[str] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    tokens_used: Optional[int] = None


class NodeUpdateEvent(BaseModel):
    event: str = "node_update"
    node_id: str
    status: NodeStatus
    output: Optional[str] = None
    error: Optional[str] = None
    consensus_score: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
