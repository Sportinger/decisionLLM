import { NodeStatus as NodeStatusType } from '../../types/pipeline';

interface NodeStatusProps {
  status: NodeStatusType;
  label: string;
}

export function NodeStatus({ status, label }: NodeStatusProps) {
  const getColor = () => {
    switch (status) {
      case 'running':
        return 'bg-blue-500';
      case 'completed':
        return 'bg-green-500';
      case 'error':
        return 'bg-red-500';
      default:
        return 'bg-gray-400';
    }
  };

  return (
    <div className="flex items-center gap-1.5">
      <span className={`w-2 h-2 rounded-full ${getColor()}`} />
      <span className="text-gray-600">{label}</span>
    </div>
  );
}
