from typing import Dict, Optional
from app.models.pipeline import PipelineConfig, PipelineLayer
from app.models.node import NodeConfig, NodeRole


class PipelineStore:
    """In-memory store for pipeline configurations."""

    def __init__(self):
        self._pipelines: Dict[str, PipelineConfig] = {}
        self._init_default_pipeline()

    def _init_default_pipeline(self):
        """Initialize the default 3-layer consensus pipeline."""
        default = PipelineConfig(
            id="default",
            name="Default 3-Layer Consensus",
            description="3 generators → 2 aggregators → 1 final decision maker",
            layers=[
                PipelineLayer(
                    level=0,
                    nodes=[
                        NodeConfig(
                            id="gen-1",
                            provider="openai",
                            model="gpt-4",
                            role=NodeRole.GENERATOR,
                        ),
                        NodeConfig(
                            id="gen-2",
                            provider="anthropic",
                            model="claude-3-sonnet-20240229",
                            role=NodeRole.GENERATOR,
                        ),
                        NodeConfig(
                            id="gen-3",
                            provider="mistral",
                            model="mistral-large-latest",
                            role=NodeRole.GENERATOR,
                        ),
                    ],
                ),
                PipelineLayer(
                    level=1,
                    nodes=[
                        NodeConfig(
                            id="agg-1",
                            provider="openai",
                            model="gpt-4",
                            role=NodeRole.AGGREGATOR,
                            system_prompt="You are an aggregator. Analyze the following responses and synthesize the key points into a coherent summary.",
                        ),
                        NodeConfig(
                            id="agg-2",
                            provider="anthropic",
                            model="claude-3-sonnet-20240229",
                            role=NodeRole.AGGREGATOR,
                            system_prompt="You are an aggregator. Analyze the following responses and synthesize the key points into a coherent summary.",
                        ),
                    ],
                ),
                PipelineLayer(
                    level=2,
                    nodes=[
                        NodeConfig(
                            id="final-1",
                            provider="openai",
                            model="gpt-4",
                            role=NodeRole.FINAL,
                            system_prompt="You are the final decision maker. Based on the aggregated responses, provide the best possible answer.",
                        ),
                    ],
                ),
            ],
        )
        self._pipelines["default"] = default

    def get(self, pipeline_id: str) -> Optional[PipelineConfig]:
        return self._pipelines.get(pipeline_id)

    def get_all(self) -> Dict[str, PipelineConfig]:
        return self._pipelines.copy()

    def save(self, config: PipelineConfig) -> None:
        self._pipelines[config.id] = config

    def delete(self, pipeline_id: str) -> bool:
        if pipeline_id in self._pipelines:
            del self._pipelines[pipeline_id]
            return True
        return False


# Global singleton
pipeline_store = PipelineStore()
