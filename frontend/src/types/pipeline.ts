export type NodeStatus = 'pending' | 'running' | 'completed' | 'error';
export type NodeRole = 'generator' | 'aggregator' | 'final';

export interface NodeConfig {
  id: string;
  provider: string;
  model: string;
  role: NodeRole;
  temperature?: number;
  maxTokens?: number;
  systemPrompt?: string;
}

export interface NodeState {
  nodeId: string;
  status: NodeStatus;
  output?: string;
  error?: string;
  startedAt?: string;
  completedAt?: string;
}

export interface PipelineLayer {
  level: number;
  nodes: NodeConfig[];
}

export interface PipelineConfig {
  id: string;
  name: string;
  description?: string;
  layers: PipelineLayer[];
  createdAt?: string;
  updatedAt?: string;
}

export interface PipelineState {
  executionId: string;
  pipelineId: string;
  status: 'pending' | 'running' | 'completed' | 'error';
  currentLayer: number;
  nodeStates: Record<string, NodeState>;
  finalOutput?: string;
  consensusScore?: number;
}

export interface NodeUpdateEvent {
  event: 'node_update';
  nodeId: string;
  status: NodeStatus;
  output?: string;
  error?: string;
  consensusScore?: number;
  timestamp: string;
}

export interface PipelineUpdateEvent {
  event: 'pipeline_update';
  executionId: string;
  status: string;
  currentLayer: number;
  progress: number;
  timestamp: string;
}
