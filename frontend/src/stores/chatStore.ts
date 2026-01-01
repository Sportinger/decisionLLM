import { create } from 'zustand';
import type { Message } from '../types/message';

interface ChatState {
  messages: Message[];
  isLoading: boolean;
  conversationId: string | null;

  addMessage: (message: Message) => void;
  setMessages: (messages: Message[]) => void;
  setLoading: (loading: boolean) => void;
  clearMessages: () => void;
  setConversationId: (id: string | null) => void;
}

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  isLoading: false,
  conversationId: null,

  addMessage: (message) =>
    set((state) => ({
      messages: [...state.messages, message],
    })),

  setMessages: (messages) => set({ messages }),

  setLoading: (loading) => set({ isLoading: loading }),

  clearMessages: () => set({ messages: [], conversationId: null }),

  setConversationId: (id) => set({ conversationId: id }),
}));
