import { memo } from 'react';
import { Handle, Position, NodeProps } from '@xyflow/react';
import { TrendingUp, CheckCircle, Clock } from 'lucide-react';

interface ConsensusNodeData {
  score: number;
  status: string;
}

function ConsensusNodeComponent({ data }: NodeProps) {
  const nodeData = data as ConsensusNodeData;
  const { score, status } = nodeData;

  const percentage = Math.round(score * 100);

  const getScoreColor = () => {
    if (percentage >= 80) return 'text-green-600';
    if (percentage >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getProgressColor = () => {
    if (percentage >= 80) return 'bg-green-500';
    if (percentage >= 60) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className="px-6 py-4 rounded-xl border-2 border-primary-500 bg-white shadow-lg min-w-[200px]">
      <Handle
        type="target"
        position={Position.Top}
        className="w-3 h-3 bg-primary-500"
      />

      {/* Header */}
      <div className="flex items-center gap-2 mb-3">
        <TrendingUp className="w-5 h-5 text-primary-600" />
        <span className="text-sm font-semibold text-gray-900">
          Consensus Score
        </span>
        {status === 'completed' ? (
          <CheckCircle className="w-4 h-4 text-green-500 ml-auto" />
        ) : (
          <Clock className="w-4 h-4 text-gray-400 ml-auto animate-pulse" />
        )}
      </div>

      {/* Score Display */}
      <div className="text-center mb-3">
        <span className={`text-4xl font-bold ${getScoreColor()}`}>
          {percentage}%
        </span>
      </div>

      {/* Progress Bar */}
      <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
        <div
          className={`h-full ${getProgressColor()} transition-all duration-500`}
          style={{ width: `${percentage}%` }}
        />
      </div>

      {/* Description */}
      <div className="mt-2 text-xs text-gray-500 text-center">
        {percentage >= 80
          ? 'High agreement between models'
          : percentage >= 60
          ? 'Moderate agreement'
          : 'Low agreement - review responses'}
      </div>
    </div>
  );
}

export const ConsensusNode = memo(ConsensusNodeComponent);
