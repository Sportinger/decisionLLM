import { useState, KeyboardEvent } from 'react';
import { Send } from 'lucide-react';

interface MessageInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export function MessageInput({ onSend, disabled }: MessageInputProps) {
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim() && !disabled) {
      onSend(input.trim());
      setInput('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex items-end gap-2">
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Type your message..."
        disabled={disabled}
        rows={1}
        className="flex-1 resize-none rounded-lg border border-gray-300 px-4 py-2
                   focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent
                   disabled:bg-gray-100 disabled:cursor-not-allowed
                   min-h-[44px] max-h-[200px]"
        style={{
          height: 'auto',
          overflowY: input.split('\n').length > 5 ? 'auto' : 'hidden',
        }}
      />

      <button
        onClick={handleSend}
        disabled={disabled || !input.trim()}
        className="p-3 bg-primary-500 text-white rounded-lg
                   hover:bg-primary-600 transition-colors
                   disabled:bg-gray-300 disabled:cursor-not-allowed"
      >
        <Send className="w-5 h-5" />
      </button>
    </div>
  );
}
