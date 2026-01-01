import asyncio
from datetime import datetime
from typing import Optional, List

from app.models.pipeline import PipelineConfig, PipelineState
from app.models.node import NodeConfig, NodeState, NodeStatus, NodeRole, NodeUpdateEvent
from app.providers import provider_registry
from app.core.consensus import ConsensusCalculator
from app.api.websocket import broadcast_node_update, broadcast_pipeline_update


class PipelineExecutor:
    """Executes a pipeline configuration with multiple LLM nodes."""

    def __init__(self, config: PipelineConfig):
        self.config = config
        self.state = PipelineState(
            pipeline_id=config.id,
            node_states={
                node.id: NodeState(node_id=node.id)
                for layer in config.layers
                for node in layer.nodes
            },
        )
        self.consensus_calculator = ConsensusCalculator()

    async def execute(self, user_message: str) -> PipelineState:
        """Execute the entire pipeline with the given user message."""
        self.state.status = "running"
        self.state.started_at = datetime.utcnow()

        await self._broadcast_pipeline_status()

        try:
            # Process each layer sequentially
            previous_outputs: List[str] = []

            for layer in self.config.layers:
                self.state.current_layer = layer.level
                await self._broadcast_pipeline_status()

                # Build input for this layer
                if layer.level == 0:
                    layer_input = user_message
                else:
                    # Combine previous layer outputs for aggregators
                    layer_input = self._format_aggregator_input(
                        user_message, previous_outputs
                    )

                # Execute all nodes in this layer in parallel
                layer_outputs = await self._execute_layer(layer.nodes, layer_input)
                previous_outputs = layer_outputs

            # Final output is the last layer's output
            if previous_outputs:
                self.state.final_output = previous_outputs[0] if len(previous_outputs) == 1 else previous_outputs[0]

            # Calculate overall consensus
            all_outputs = [
                state.output
                for state in self.state.node_states.values()
                if state.output
            ]
            self.state.consensus_score = self.consensus_calculator.calculate_pairwise_consensus(
                all_outputs
            )

            self.state.status = "completed"
            self.state.completed_at = datetime.utcnow()

        except Exception as e:
            self.state.status = "error"
            self.state.completed_at = datetime.utcnow()
            raise

        await self._broadcast_pipeline_status()
        return self.state

    async def _execute_layer(
        self, nodes: List[NodeConfig], layer_input: str
    ) -> List[str]:
        """Execute all nodes in a layer in parallel."""
        tasks = [self._execute_node(node, layer_input) for node in nodes]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        outputs = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                # Node failed, error already recorded in state
                continue
            outputs.append(result)

        return outputs

    async def _execute_node(self, node: NodeConfig, input_text: str) -> str:
        """Execute a single node."""
        node_state = self.state.node_states[node.id]
        node_state.status = NodeStatus.RUNNING
        node_state.started_at = datetime.utcnow()

        await self._broadcast_node_status(node.id)

        try:
            # Get provider
            provider_class = provider_registry.get(node.provider)
            if not provider_class:
                raise ValueError(f"Provider '{node.provider}' not found")

            provider = provider_class()

            # Build messages
            messages = []
            if node.system_prompt:
                messages.append({"role": "system", "content": node.system_prompt})
            elif node.role == NodeRole.GENERATOR:
                messages.append({
                    "role": "system",
                    "content": "You are a helpful assistant. Provide a clear and comprehensive answer.",
                })

            messages.append({"role": "user", "content": input_text})

            # Call LLM
            response = await provider.generate(
                model=node.model,
                messages=messages,
                temperature=node.temperature,
                max_tokens=node.max_tokens,
            )

            node_state.output = response
            node_state.status = NodeStatus.COMPLETED
            node_state.completed_at = datetime.utcnow()

        except Exception as e:
            node_state.status = NodeStatus.ERROR
            node_state.error = str(e)
            node_state.completed_at = datetime.utcnow()
            await self._broadcast_node_status(node.id)
            raise

        await self._broadcast_node_status(node.id)
        return node_state.output

    def _format_aggregator_input(
        self, original_question: str, previous_outputs: List[str]
    ) -> str:
        """Format input for aggregator nodes."""
        formatted = f"Original Question: {original_question}\n\n"
        formatted += "Previous Responses:\n"
        for i, output in enumerate(previous_outputs, 1):
            formatted += f"\n--- Response {i} ---\n{output}\n"

        formatted += "\n---\n\nPlease analyze these responses and provide a synthesized answer."
        return formatted

    async def _broadcast_node_status(self, node_id: str):
        """Broadcast node status update via WebSocket."""
        node_state = self.state.node_states[node_id]
        event = NodeUpdateEvent(
            node_id=node_id,
            status=node_state.status,
            output=node_state.output,
            error=node_state.error,
        )
        await broadcast_node_update(event.model_dump())

    async def _broadcast_pipeline_status(self):
        """Broadcast pipeline status update via WebSocket."""
        total_nodes = len(self.state.node_states)
        completed_nodes = sum(
            1 for state in self.state.node_states.values()
            if state.status in (NodeStatus.COMPLETED, NodeStatus.ERROR)
        )
        progress = completed_nodes / total_nodes if total_nodes > 0 else 0

        event = {
            "event": "pipeline_update",
            "execution_id": self.state.execution_id,
            "status": self.state.status,
            "current_layer": self.state.current_layer,
            "progress": progress,
        }
        await broadcast_pipeline_update(event)
