import { useEffect, useRef } from 'react';
import { Message as MessageType } from '../../types/message';
import { Message } from './Message';
import { Loader2 } from 'lucide-react';

interface MessageListProps {
  messages: MessageType[];
  isLoading: boolean;
}

export function MessageList({ messages, isLoading }: MessageListProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  if (messages.length === 0 && !isLoading) {
    return (
      <div className="h-full flex items-center justify-center text-gray-500">
        <div className="text-center">
          <p className="text-lg font-medium">Start a conversation</p>
          <p className="text-sm mt-1">
            Your message will be processed through the consensus pipeline
          </p>
        </div>
      </div>
    );
  }

  return (
    <div ref={scrollRef} className="h-full overflow-y-auto p-4 space-y-4">
      {messages.map((message) => (
        <Message key={message.id} message={message} />
      ))}

      {isLoading && (
        <div className="flex items-center gap-2 text-gray-500 p-4">
          <Loader2 className="w-5 h-5 animate-spin" />
          <span>Processing through pipeline...</span>
        </div>
      )}
    </div>
  );
}
