import { ReactNode, useState, useCallback } from 'react';

interface SplitPaneProps {
  left: ReactNode;
  right: ReactNode;
  defaultSplit?: number;
}

export function SplitPane({ left, right, defaultSplit = 50 }: SplitPaneProps) {
  const [splitPosition, setSplitPosition] = useState(defaultSplit);
  const [isDragging, setIsDragging] = useState(false);

  const handleMouseDown = useCallback(() => {
    setIsDragging(true);
  }, []);

  const handleMouseUp = useCallback(() => {
    setIsDragging(false);
  }, []);

  const handleMouseMove = useCallback(
    (e: React.MouseEvent<HTMLDivElement>) => {
      if (!isDragging) return;

      const container = e.currentTarget;
      const rect = container.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const percentage = (x / rect.width) * 100;

      // Limit split between 20% and 80%
      setSplitPosition(Math.min(80, Math.max(20, percentage)));
    },
    [isDragging]
  );

  return (
    <div
      className="flex-1 flex relative"
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
    >
      {/* Left Panel */}
      <div
        className="h-full overflow-hidden"
        style={{ width: `${splitPosition}%` }}
      >
        {left}
      </div>

      {/* Divider */}
      <div
        className={`w-1 bg-gray-200 cursor-col-resize hover:bg-primary-400 transition-colors ${
          isDragging ? 'bg-primary-500' : ''
        }`}
        onMouseDown={handleMouseDown}
      />

      {/* Right Panel */}
      <div
        className="h-full overflow-hidden"
        style={{ width: `${100 - splitPosition}%` }}
      >
        {right}
      </div>
    </div>
  );
}
