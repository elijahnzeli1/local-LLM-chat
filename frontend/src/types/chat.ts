export interface Message {
    role: 'user' | 'assistant';
    content: string;
    timestamp: string;
}

export interface ChatMessage {
    message: string;
    conversationId?: string;
    useInternet?: boolean;
}

export interface ChatResponse {
    response: string;
    conversationId: string;
}

export interface Conversation {
    id: string;
    messages: Message[];
    lastUpdated: string;
    title?: string;
}

export interface ConversationExport {
    version: string;
    conversations: Conversation[];
    exportDate: string;
}
