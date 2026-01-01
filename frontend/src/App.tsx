import { ReactFlowProvider } from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { Header } from './components/Layout/Header';
import { SplitPane } from './components/Layout/SplitPane';
import { ChatContainer } from './components/Chat/ChatContainer';
import { PipelineFlow } from './components/Pipeline/PipelineFlow';

function App() {
  return (
    <ReactFlowProvider>
      <div className="min-h-screen flex flex-col bg-gray-900">
        <Header />
        <main className="flex-1 flex overflow-hidden">
          <SplitPane
            left={<ChatContainer />}
            right={<PipelineFlow />}
          />
        </main>
      </div>
    </ReactFlowProvider>
  );
}

export default App;
