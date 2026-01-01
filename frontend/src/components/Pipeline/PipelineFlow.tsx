import { useMemo, useCallback } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  Node,
  Edge,
  ConnectionLineType,
} from '@xyflow/react';
import { usePipelineStore } from '../../stores/pipelineStore';
import { LLMNode } from './LLMNode';
import { ConsensusNode } from './ConsensusNode';
import { NodeStatus } from './NodeStatus';

const nodeTypes = {
  llm: LLMNode,
  consensus: ConsensusNode,
};

export function PipelineFlow() {
  const { currentPipeline, executionState, isExecuting } = usePipelineStore();

  // Convert pipeline config to ReactFlow nodes and edges
  const { initialNodes, initialEdges } = useMemo(() => {
    if (!currentPipeline) {
      return { initialNodes: [], initialEdges: [] };
    }

    const nodes: Node[] = [];
    const edges: Edge[] = [];

    const layerSpacing = 200;
    const nodeSpacing = 180;

    currentPipeline.layers.forEach((layer, layerIndex) => {
      const layerWidth = layer.nodes.length * nodeSpacing;
      const startX = -layerWidth / 2 + nodeSpacing / 2;

      layer.nodes.forEach((nodeConfig, nodeIndex) => {
        const nodeId = nodeConfig.id;
        const nodeState = executionState?.nodeStates[nodeId];

        nodes.push({
          id: nodeId,
          type: 'llm',
          position: {
            x: startX + nodeIndex * nodeSpacing,
            y: layerIndex * layerSpacing,
          },
          data: {
            label: nodeConfig.model,
            provider: nodeConfig.provider,
            role: nodeConfig.role,
            status: nodeState?.status || 'pending',
            output: nodeState?.output,
            error: nodeState?.error,
          },
        });

        // Create edges to next layer
        if (layerIndex < currentPipeline.layers.length - 1) {
          const nextLayer = currentPipeline.layers[layerIndex + 1];
          nextLayer.nodes.forEach((targetNode) => {
            edges.push({
              id: `${nodeId}-${targetNode.id}`,
              source: nodeId,
              target: targetNode.id,
              type: 'smoothstep',
              animated: isExecuting && nodeState?.status === 'running',
              style: {
                stroke:
                  nodeState?.status === 'completed'
                    ? '#22c55e'
                    : nodeState?.status === 'running'
                    ? '#3b82f6'
                    : nodeState?.status === 'error'
                    ? '#ef4444'
                    : '#9ca3af',
                strokeWidth: 2,
              },
            });
          });
        }
      });
    });

    // Add consensus indicator node at the bottom
    if (executionState?.consensusScore !== undefined) {
      nodes.push({
        id: 'consensus-result',
        type: 'consensus',
        position: {
          x: 0,
          y: currentPipeline.layers.length * layerSpacing + 50,
        },
        data: {
          score: executionState.consensusScore,
          status: executionState.status,
        },
      });
    }

    return { initialNodes: nodes, initialEdges: edges };
  }, [currentPipeline, executionState, isExecuting]);

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  // Update nodes when execution state changes
  useMemo(() => {
    setNodes(initialNodes);
    setEdges(initialEdges);
  }, [initialNodes, initialEdges, setNodes, setEdges]);

  return (
    <div className="h-full bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-gray-900">
            Pipeline Visualisierung
          </h2>
          <p className="text-sm text-gray-500">
            {currentPipeline?.name || 'No pipeline selected'}
          </p>
        </div>

        {/* Status Legend */}
        <div className="flex items-center gap-4 text-xs">
          <NodeStatus status="pending" label="Pending" />
          <NodeStatus status="running" label="Running" />
          <NodeStatus status="completed" label="Completed" />
          <NodeStatus status="error" label="Error" />
        </div>
      </div>

      {/* Flow Canvas */}
      <div className="h-[calc(100%-60px)]">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          nodeTypes={nodeTypes}
          connectionLineType={ConnectionLineType.SmoothStep}
          fitView
          fitViewOptions={{ padding: 0.2 }}
          minZoom={0.5}
          maxZoom={1.5}
        >
          <Background color="#e5e7eb" gap={20} />
          <Controls />
          <MiniMap
            nodeColor={(node) => {
              const status = node.data?.status;
              if (status === 'completed') return '#22c55e';
              if (status === 'running') return '#3b82f6';
              if (status === 'error') return '#ef4444';
              return '#9ca3af';
            }}
            maskColor="rgba(255, 255, 255, 0.8)"
          />
        </ReactFlow>
      </div>
    </div>
  );
}
