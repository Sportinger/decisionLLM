import { useCallback } from 'react';
import { useChatStore } from '../stores/chatStore';
import { usePipelineStore } from '../stores/pipelineStore';
import { useWebSocket } from './useWebSocket';
import type { Message } from '../types/message';
import { api } from '../lib/api';

export function useChat() {
  const { messages, isLoading, addMessage, setLoading } = useChatStore();
  const { currentPipeline, startExecution, finishExecution } = usePipelineStore();
  const { subscribe } = useWebSocket();

  const sendMessage = useCallback(
    async (content: string) => {
      if (!content.trim() || isLoading) return;

      // Add user message
      const userMessage: Message = {
        id: crypto.randomUUID(),
        role: 'user',
        content,
        timestamp: new Date().toISOString(),
      };
      addMessage(userMessage);
      setLoading(true);

      try {
        const response = await api.sendChatMessage({
          message: content,
          pipelineId: currentPipeline?.id,
        });

        // Subscribe to WebSocket updates for this execution
        subscribe(response.pipelineExecutionId);

        // Start execution in store
        if (currentPipeline) {
          startExecution(response.pipelineExecutionId, currentPipeline.id);
        }

        // Add assistant message
        const assistantMessage: Message = {
          id: response.id,
          role: 'assistant',
          content: response.message.content,
          timestamp: response.message.timestamp,
          metadata: {
            pipelineExecutionId: response.pipelineExecutionId,
            consensusScore: response.consensusScore,
            nodeResponses: response.nodeResponses,
          },
        };
        addMessage(assistantMessage);

        // Finish execution
        if (response.consensusScore !== undefined) {
          finishExecution(response.message.content, response.consensusScore);
        }
      } catch (error) {
        console.error('Failed to send message:', error);

        // Add error message
        const errorMessage: Message = {
          id: crypto.randomUUID(),
          role: 'assistant',
          content: 'Sorry, an error occurred while processing your request.',
          timestamp: new Date().toISOString(),
        };
        addMessage(errorMessage);
      } finally {
        setLoading(false);
      }
    },
    [
      isLoading,
      currentPipeline,
      addMessage,
      setLoading,
      startExecution,
      finishExecution,
      subscribe,
    ]
  );

  return {
    messages,
    isLoading,
    sendMessage,
  };
}
