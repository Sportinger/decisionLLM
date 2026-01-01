from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

from app.models.node import NodeConfig, NodeState


class PipelineLayer(BaseModel):
    level: int
    nodes: list[NodeConfig]


class PipelineConfig(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    layers: list[PipelineLayer]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def get_total_nodes(self) -> int:
        return sum(len(layer.nodes) for layer in self.layers)

    def get_node_by_id(self, node_id: str) -> Optional[NodeConfig]:
        for layer in self.layers:
            for node in layer.nodes:
                if node.id == node_id:
                    return node
        return None


class PipelineState(BaseModel):
    execution_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    pipeline_id: str
    status: str = "pending"  # pending, running, completed, error
    current_layer: int = 0
    node_states: dict[str, NodeState] = {}
    final_output: Optional[str] = None
    consensus_score: Optional[float] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class PipelineExecutionEvent(BaseModel):
    event: str = "pipeline_update"
    execution_id: str
    status: str
    current_layer: int
    progress: float  # 0.0 - 1.0
    timestamp: datetime = Field(default_factory=datetime.utcnow)
