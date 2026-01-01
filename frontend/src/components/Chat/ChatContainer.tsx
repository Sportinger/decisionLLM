import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { useChat } from '../../hooks/useChat';

export function ChatContainer() {
  const { messages, isLoading, sendMessage } = useChat();

  return (
    <div className="h-full flex flex-col bg-gray-900">
      {/* Messages Area */}
      <div className="flex-1 overflow-hidden">
        <MessageList messages={messages} isLoading={isLoading} />
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-700 p-4">
        <MessageInput onSend={sendMessage} disabled={isLoading} />
      </div>
    </div>
  );
}
