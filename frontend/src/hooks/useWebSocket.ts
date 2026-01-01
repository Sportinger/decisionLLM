import { useEffect, useRef, useCallback, useState } from 'react';
import { usePipelineStore } from '../stores/pipelineStore';
import { NodeUpdateEvent, PipelineUpdateEvent } from '../types/pipeline';

const WS_URL = 'ws://localhost:8000/ws/pipeline';

export function useWebSocket() {
  const wsRef = useRef<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const reconnectTimeoutRef = useRef<number | null>(null);

  const { updateNodeState, updateExecutionProgress, finishExecution } =
    usePipelineStore();

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      return;
    }

    const ws = new WebSocket(WS_URL);

    ws.onopen = () => {
      console.log('WebSocket connected');
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.event === 'node_update') {
          const nodeEvent = data as NodeUpdateEvent;
          updateNodeState(nodeEvent.nodeId, {
            status: nodeEvent.status,
            output: nodeEvent.output,
            error: nodeEvent.error,
          });
        } else if (data.event === 'pipeline_update') {
          const pipelineEvent = data as PipelineUpdateEvent;
          updateExecutionProgress(
            pipelineEvent.currentLayer,
            pipelineEvent.progress
          );

          if (pipelineEvent.status === 'completed') {
            // Final output will come from API response
          }
        }
      } catch (err) {
        console.error('Failed to parse WebSocket message:', err);
      }
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
      setIsConnected(false);

      // Attempt to reconnect after 3 seconds
      reconnectTimeoutRef.current = window.setTimeout(() => {
        connect();
      }, 3000);
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    wsRef.current = ws;
  }, [updateNodeState, updateExecutionProgress]);

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
  }, []);

  const sendMessage = useCallback((message: object) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
    }
  }, []);

  const subscribe = useCallback(
    (executionId: string) => {
      sendMessage({ type: 'subscribe', execution_id: executionId });
    },
    [sendMessage]
  );

  useEffect(() => {
    connect();
    return () => disconnect();
  }, [connect, disconnect]);

  return {
    isConnected,
    sendMessage,
    subscribe,
    connect,
    disconnect,
  };
}
