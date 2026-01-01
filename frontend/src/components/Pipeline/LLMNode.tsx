import { memo } from 'react';
import { Handle, Position, NodeProps } from '@xyflow/react';
import { Bot, Loader2, CheckCircle, XCircle, Sparkles } from 'lucide-react';
import type { NodeStatus } from '../../types/pipeline';

interface LLMNodeData {
  label: string;
  provider: string;
  role: string;
  status: NodeStatus;
  output?: string;
  error?: string;
}

function LLMNodeComponent({ data }: NodeProps) {
  const nodeData = data as LLMNodeData;
  const { label, provider, role, status, output, error } = nodeData;

  const getStatusIcon = () => {
    switch (status) {
      case 'running':
        return <Loader2 className="w-4 h-4 animate-spin text-blue-500" />;
      case 'completed':
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'error':
        return <XCircle className="w-4 h-4 text-red-500" />;
      default:
        return <Bot className="w-4 h-4 text-gray-400" />;
    }
  };

  const getStatusColor = () => {
    switch (status) {
      case 'running':
        return 'border-blue-500 bg-blue-50';
      case 'completed':
        return 'border-green-500 bg-green-50';
      case 'error':
        return 'border-red-500 bg-red-50';
      default:
        return 'border-gray-300 bg-white';
    }
  };

  const getRoleIcon = () => {
    if (role === 'aggregator' || role === 'final') {
      return <Sparkles className="w-3 h-3 text-purple-500" />;
    }
    return null;
  };

  return (
    <div
      className={`px-4 py-3 rounded-lg border-2 shadow-md min-w-[160px] ${getStatusColor()}`}
    >
      <Handle
        type="target"
        position={Position.Top}
        className="w-3 h-3 bg-gray-400"
      />

      {/* Header */}
      <div className="flex items-center justify-between gap-2 mb-2">
        <div className="flex items-center gap-2">
          {getStatusIcon()}
          <span className="text-xs font-medium text-gray-600 uppercase">
            {provider}
          </span>
        </div>
        {getRoleIcon()}
      </div>

      {/* Model Name */}
      <div className="text-sm font-semibold text-gray-900 truncate">
        {label}
      </div>

      {/* Role Badge */}
      <div className="mt-1">
        <span
          className={`text-xs px-2 py-0.5 rounded-full ${
            role === 'generator'
              ? 'bg-blue-100 text-blue-700'
              : role === 'aggregator'
              ? 'bg-purple-100 text-purple-700'
              : 'bg-orange-100 text-orange-700'
          }`}
        >
          {role}
        </span>
      </div>

      {/* Output Preview */}
      {status === 'completed' && output && (
        <div className="mt-2 p-2 bg-white rounded border border-gray-200 text-xs text-gray-600 max-h-20 overflow-hidden">
          {output.substring(0, 100)}
          {output.length > 100 && '...'}
        </div>
      )}

      {/* Error Message */}
      {status === 'error' && error && (
        <div className="mt-2 p-2 bg-red-100 rounded text-xs text-red-700">
          {error}
        </div>
      )}

      <Handle
        type="source"
        position={Position.Bottom}
        className="w-3 h-3 bg-gray-400"
      />
    </div>
  );
}

export const LLMNode = memo(LLMNodeComponent);
