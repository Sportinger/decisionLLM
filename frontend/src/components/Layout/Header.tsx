import { Settings, GitBranch } from 'lucide-react';

export function Header() {
  return (
    <header className="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <GitBranch className="w-6 h-6 text-primary-600" />
        <h1 className="text-xl font-semibold text-gray-900">DecisionLLM</h1>
        <span className="text-sm text-gray-500">Multi-Layer Consensus System</span>
      </div>

      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 text-sm text-gray-600">
          <span className="w-2 h-2 bg-green-500 rounded-full"></span>
          <span>Connected</span>
        </div>

        <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
          <Settings className="w-5 h-5 text-gray-600" />
        </button>
      </div>
    </header>
  );
}
