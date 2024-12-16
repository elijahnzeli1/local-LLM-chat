export interface Message {
    role: 'user' | 'assistant';
    content: string;
    timestamp: string;
}

export interface ChatMessage {
    message: string;
    conversationId?: string;
    useInternet?: boolean;
    mode?: ChatMode;
}

export type ChatMode = 'normal' | 'coding';

export interface ProjectConfig {
    name: string;
    type: string;
    framework?: string;
    dependencies?: string[];
    devDependencies?: string[];
}

export interface CodingContext {
    projectConfig?: ProjectConfig;
    currentFile?: string;
    currentStep?: string;
    webContainerId?: string;
}

export interface ChatResponse {
    response: string;
    conversationId: string;
    codingContext?: CodingContext;
}

export interface ConversationMetadata {
    title?: string;
    description?: string;
    tags?: string[];
    category?: string;
    lastUpdated: string;
    mode: ChatMode;
    codingContext?: CodingContext;
}

export interface Conversation {
    id: string;
    messages: Message[];
    metadata: ConversationMetadata;
}

export interface ConversationExport {
    version: string;
    conversations: Conversation[];
    exportDate: string;
}
