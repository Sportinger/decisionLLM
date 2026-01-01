import { create } from 'zustand';
import { PipelineConfig, PipelineState, NodeState, NodeStatus } from '../types/pipeline';

interface PipelineStore {
  // Current pipeline config
  currentPipeline: PipelineConfig | null;
  pipelines: PipelineConfig[];

  // Execution state
  executionState: PipelineState | null;
  isExecuting: boolean;

  // Actions
  setCurrentPipeline: (pipeline: PipelineConfig | null) => void;
  setPipelines: (pipelines: PipelineConfig[]) => void;
  addPipeline: (pipeline: PipelineConfig) => void;
  removePipeline: (id: string) => void;

  // Execution actions
  startExecution: (executionId: string, pipelineId: string) => void;
  updateNodeState: (nodeId: string, state: Partial<NodeState>) => void;
  updateExecutionProgress: (currentLayer: number, progress: number) => void;
  finishExecution: (finalOutput: string, consensusScore: number) => void;
  resetExecution: () => void;
}

const defaultPipeline: PipelineConfig = {
  id: 'default',
  name: 'Default 3-Layer Consensus',
  description: '3 generators → 2 aggregators → 1 final',
  layers: [
    {
      level: 0,
      nodes: [
        { id: 'gen-1', provider: 'openai', model: 'gpt-4', role: 'generator' },
        { id: 'gen-2', provider: 'anthropic', model: 'claude-3-sonnet', role: 'generator' },
        { id: 'gen-3', provider: 'mistral', model: 'mistral-large', role: 'generator' },
      ],
    },
    {
      level: 1,
      nodes: [
        { id: 'agg-1', provider: 'openai', model: 'gpt-4', role: 'aggregator' },
        { id: 'agg-2', provider: 'anthropic', model: 'claude-3-sonnet', role: 'aggregator' },
      ],
    },
    {
      level: 2,
      nodes: [
        { id: 'final-1', provider: 'openai', model: 'gpt-4', role: 'final' },
      ],
    },
  ],
};

export const usePipelineStore = create<PipelineStore>((set) => ({
  currentPipeline: defaultPipeline,
  pipelines: [defaultPipeline],
  executionState: null,
  isExecuting: false,

  setCurrentPipeline: (pipeline) => set({ currentPipeline: pipeline }),

  setPipelines: (pipelines) => set({ pipelines }),

  addPipeline: (pipeline) =>
    set((state) => ({
      pipelines: [...state.pipelines, pipeline],
    })),

  removePipeline: (id) =>
    set((state) => ({
      pipelines: state.pipelines.filter((p) => p.id !== id),
    })),

  startExecution: (executionId, pipelineId) =>
    set((state) => {
      const pipeline = state.pipelines.find((p) => p.id === pipelineId);
      if (!pipeline) return state;

      const nodeStates: Record<string, NodeState> = {};
      pipeline.layers.forEach((layer) => {
        layer.nodes.forEach((node) => {
          nodeStates[node.id] = {
            nodeId: node.id,
            status: 'pending' as NodeStatus,
          };
        });
      });

      return {
        isExecuting: true,
        executionState: {
          executionId,
          pipelineId,
          status: 'running',
          currentLayer: 0,
          nodeStates,
        },
      };
    }),

  updateNodeState: (nodeId, state) =>
    set((prev) => {
      if (!prev.executionState) return prev;

      return {
        executionState: {
          ...prev.executionState,
          nodeStates: {
            ...prev.executionState.nodeStates,
            [nodeId]: {
              ...prev.executionState.nodeStates[nodeId],
              ...state,
            },
          },
        },
      };
    }),

  updateExecutionProgress: (currentLayer, progress) =>
    set((state) => {
      if (!state.executionState) return state;

      return {
        executionState: {
          ...state.executionState,
          currentLayer,
        },
      };
    }),

  finishExecution: (finalOutput, consensusScore) =>
    set((state) => {
      if (!state.executionState) return state;

      return {
        isExecuting: false,
        executionState: {
          ...state.executionState,
          status: 'completed',
          finalOutput,
          consensusScore,
        },
      };
    }),

  resetExecution: () =>
    set({
      isExecuting: false,
      executionState: null,
    }),
}));
