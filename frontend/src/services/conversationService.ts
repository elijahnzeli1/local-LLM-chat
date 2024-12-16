import axios from 'axios';
import { Conversation, Message, ConversationMetadata, ChatMode } from '../types/chat';

const API_BASE_URL = 'http://localhost:8000';

export class ConversationService {
    static async getConversations(): Promise<Conversation[]> {
        const response = await axios.get(`${API_BASE_URL}/conversations`);
        return response.data;
    }

    static async createConversation(title?: string, mode: ChatMode = 'normal'): Promise<Conversation> {
        const response = await axios.post(`${API_BASE_URL}/conversations`, { 
            title,
            metadata: {
                mode,
                title,
                lastUpdated: new Date().toISOString()
            }
        });
        return response.data;
    }

    static async getConversationHistory(conversationId: string): Promise<Message[]> {
        const response = await axios.get(`${API_BASE_URL}/conversations/${conversationId}/history`);
        return response.data;
    }

    static async addMessage(conversationId: string, role: string, content: string): Promise<Message[]> {
        const response = await axios.post(`${API_BASE_URL}/conversations/${conversationId}/messages`, {
            role,
            content
        });
        return response.data;
    }

    static async updateConversation(
        conversationId: string, 
        update: Partial<ConversationMetadata>
    ): Promise<Conversation> {
        const response = await axios.patch(`${API_BASE_URL}/conversations/${conversationId}`, update);
        return response.data;
    }

    static async createCodingProject(
        conversationId: string,
        projectConfig: {
            name: string;
            type: string;
            framework?: string;
            dependencies?: string[];
        }
    ): Promise<void> {
        await axios.post(`${API_BASE_URL}/conversations/${conversationId}/coding/init`, projectConfig);
    }

    static async executeCommand(
        conversationId: string,
        command: string,
        args: string[] = []
    ): Promise<{ output: string; exitCode: number }> {
        const response = await axios.post(`${API_BASE_URL}/conversations/${conversationId}/coding/execute`, {
            command,
            args
        });
        return response.data;
    }

    static async writeFile(
        conversationId: string,
        path: string,
        content: string
    ): Promise<void> {
        await axios.post(`${API_BASE_URL}/conversations/${conversationId}/coding/write`, {
            path,
            content
        });
    }

    static async readFile(
        conversationId: string,
        path: string
    ): Promise<string> {
        const response = await axios.get(`${API_BASE_URL}/conversations/${conversationId}/coding/read`, {
            params: { path }
        });
        return response.data.content;
    }
}