import { useState, useEffect } from 'react';
import { useToast, Switch, FormControl, FormLabel } from '@chakra-ui/react';
import { ConversationService } from '../services/conversationService';
import { webContainerService } from '../services/webContainerService';
import { Conversation, ChatMode } from '../types/chat';
import { FiSearch, FiPlus, FiMessageSquare, FiCode } from 'react-icons/fi';

interface ConversationListProps {
    onSelectConversation: (conversationId: string, mode: ChatMode) => void;
    selectedConversationId?: string;
}

export const ConversationList: React.FC<ConversationListProps> = ({
    onSelectConversation,
    selectedConversationId
}) => {
    const [conversations, setConversations] = useState<Conversation[]>([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [isCreatingNew, setIsCreatingNew] = useState(false);
    const [isCodingMode, setIsCodingMode] = useState(false);
    const toast = useToast();

    useEffect(() => {
        loadConversations();
        initializeWebContainer();
    }, []);

    const initializeWebContainer = async () => {
        try {
            await webContainerService.initialize();
        } catch (error) {
            toast({
                title: 'Error',
                description: 'Failed to initialize development environment',
                status: 'error',
                duration: 3000,
                isClosable: true,
            });
        }
    };

    const loadConversations = async () => {
        try {
            const data = await ConversationService.getConversations();
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

    const handleNewChat = async () => {
        if (isCreatingNew) return;
        
        try {
            setIsCreatingNew(true);
            const newConversation = await ConversationService.createConversation(undefined, isCodingMode ? 'coding' : 'normal');
            setConversations(prev => [newConversation, ...prev]);
            onSelectConversation(newConversation.id, isCodingMode ? 'coding' : 'normal');
        } catch (error) {
            toast({
                title: 'Error',
                description: 'Failed to create new conversation',
                status: 'error',
                duration: 3000,
                isClosable: true,
            });
        } finally {
            setIsCreatingNew(false);
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
                <div className="relative mb-4">
                    <FiSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                    <input
                        type="text"
                        placeholder="Search conversations..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="w-full bg-dark text-white rounded-lg pl-10 pr-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
                    />
                </div>
                <FormControl display="flex" alignItems="center">
                    <FormLabel htmlFor="coding-mode" mb="0" className="flex items-center gap-2">
                        <FiCode />
                        Coding Mode
                    </FormLabel>
                    <Switch
                        id="coding-mode"
                        isChecked={isCodingMode}
                        onChange={(e) => setIsCodingMode(e.target.checked)}
                        colorScheme="green"
                    />
                </FormControl>
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
                                onClick={() => onSelectConversation(conv.id, conv.metadata.mode)}
                                className={`sidebar-item ${conv.id === selectedConversationId ? 'active' : ''}`}
                            >
                                {conv.metadata.mode === 'coding' ? <FiCode /> : <FiMessageSquare />}
                                <div className="flex-1 min-w-0">
                                    <div className="flex justify-between items-start">
                                        <p className="font-medium truncate">
                                            {conv.metadata?.title || (conv.metadata.mode === 'coding' ? 'New Project' : 'New Chat')}
                                        </p>
                                        <span className="text-xs text-gray-400 whitespace-nowrap ml-2">
                                            {lastMessage?.timestamp ? new Date(lastMessage.timestamp).toLocaleDateString() : ''}
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
                    onClick={handleNewChat}
                    className="w-full flex items-center justify-center gap-2 primary-button"
                    disabled={isCreatingNew}
                >
                    <FiPlus />
                    {isCreatingNew ? 'Creating...' : isCodingMode ? 'New Project' : 'New Chat'}
                </button>
            </div>
        </div>
    );
};
