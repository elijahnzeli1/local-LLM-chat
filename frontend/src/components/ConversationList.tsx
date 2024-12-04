import { useState, useEffect } from 'react';
import { useToast } from '@chakra-ui/react';
import { ChatService } from '../services/chatService';
import { Conversation } from '../types/chat';
import { FiSearch, FiPlus, FiMessageSquare } from 'react-icons/fi';

interface ConversationListProps {
    onSelectConversation: (conversationId: string) => void;
    selectedConversationId?: string;
}

export const ConversationList: React.FC<ConversationListProps> = ({
    onSelectConversation,
    selectedConversationId
}) => {
    const [conversations, setConversations] = useState<Conversation[]>([]);
    const [searchTerm, setSearchTerm] = useState('');
    const toast = useToast();

    useEffect(() => {
        loadConversations();
    }, []);

    const loadConversations = async () => {
        try {
            const data = await ChatService.getConversations();
            setConversations(data);
        } catch (error) {
            toast({
                title: 'Error',
                description: 'Failed to load conversations',
                status: 'error',
                duration: 3000,
                isClosable: true,
            });
        }
    };

    const filteredConversations = conversations.filter(conv => 
        conv.messages.some(msg => 
            msg.content.toLowerCase().includes(searchTerm.toLowerCase())
        )
    );

    return (
        <div className="h-full flex flex-col">
            {/* Header */}
            <div className="p-4 border-b border-dark-lighter">
                <h1 className="text-lg text-primary font-semibold mb-4">My Chats</h1>
                <div className="relative">
                    <FiSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                    <input
                        type="text"
                        placeholder="Search conversations..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="w-full bg-dark text-white rounded-lg pl-10 pr-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
                    />
                </div>
            </div>

            {/* Conversation List */}
            <div className="flex-1 overflow-y-auto p-2">
                {filteredConversations.length === 0 ? (
                    <div className="text-center text-gray-400 mt-8">
                        <FiMessageSquare className="mx-auto text-4xl mb-2" />
                        <p className="text-sm">No conversations found</p>
                    </div>
                ) : (
                    filteredConversations.map(conv => {
                        const lastMessage = conv.messages[conv.messages.length - 1];
                        return (
                            <div
                                key={conv.id}
                                onClick={() => onSelectConversation(conv.id)}
                                className={`sidebar-item ${conv.id === selectedConversationId ? 'active' : ''}`}
                            >
                                <FiMessageSquare />
                                <div className="flex-1 min-w-0">
                                    <div className="flex justify-between items-start">
                                        <p className="font-medium truncate">
                                            {conv.messages[0]?.content.slice(0, 30) || 'New Chat'}
                                        </p>
                                        <span className="text-xs text-gray-400 whitespace-nowrap ml-2">
                                            {new Date(lastMessage?.timestamp || '').toLocaleDateString()}
                                        </span>
                                    </div>
                                    <p className="text-sm text-gray-400 truncate">
                                        {lastMessage?.content.slice(0, 50) || 'No messages yet'}
                                    </p>
                                </div>
                            </div>
                        );
                    })
                )}
            </div>

            {/* New Chat Button */}
            <div className="p-4 border-t border-dark-lighter">
                <button
                    onClick={() => onSelectConversation('')}
                    className="w-full flex items-center justify-center gap-2 primary-button"
                >
                    <FiPlus />
                    New Chat
                </button>
            </div>
        </div>
    );
};
