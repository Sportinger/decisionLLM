export type MessageRole = 'user' | 'assistant' | 'system';

export interface Message {
  id: string;
  role: MessageRole;
  content: string;
  timestamp: string;
  metadata?: {
    pipelineExecutionId?: string;
    consensusScore?: number;
    nodeResponses?: Array<{
      nodeId: string;
      status: string;
      output?: string;
    }>;
  };
}

export interface ChatRequest {
  message: string;
  pipelineId?: string;
  conversationId?: string;
}

export interface ChatResponse {
  id: string;
  message: Message;
  pipelineExecutionId: string;
  consensusScore?: number;
  nodeResponses?: Array<{
    nodeId: string;
    status: string;
    output?: string;
  }>;
}
