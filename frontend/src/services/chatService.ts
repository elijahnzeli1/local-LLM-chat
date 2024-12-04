import axios from 'axios';
import { ChatMessage, ChatResponse, Conversation } from '../types/chat';

const API_BASE_URL = 'http://localhost:8000/api';

// Configure axios with a longer timeout
const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 70000, // 70 seconds timeout to account for model processing time
});

export class ChatService {
    static async sendMessage(chatMessage: ChatMessage): Promise<ChatResponse> {
        try {
            const response = await api.post('/chat', {
                message: chatMessage.message,
                conversation_id: chatMessage.conversationId,
                use_internet: chatMessage.useInternet
            });
            return response.data;
        } catch (error) {
            console.error('Error sending message:', error);
            throw error;
        }
    }

    static async getConversations(): Promise<Conversation[]> {
        try {
            const response = await api.get('/conversations');
            return response.data;
        } catch (error) {
            console.error('Error fetching conversations:', error);
            throw error;
        }
    }

    static async exportConversations(): Promise<Blob> {
        try {
            const response = await api.get('/conversations/export', {
                responseType: 'blob'
            });
            return response.data;
        } catch (error) {
            console.error('Error exporting conversations:', error);
            throw error;
        }
    }

    static async importConversations(file: File): Promise<void> {
        try {
            const formData = new FormData();
            formData.append('file', file);
            await api.post('/conversations/import', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
        } catch (error) {
            console.error('Error importing conversations:', error);
            throw error;
        }
    }
}
