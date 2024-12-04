import { useState } from 'react'
import { Message } from './types/chat'
import { ChatService } from './services/chatService'
import { ConversationList } from './components/ConversationList'
import { FiSend } from 'react-icons/fi'
import axios, { AxiosError } from 'axios'

interface ErrorResponse {
  detail?: string;
  message?: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [useInternet, setUseInternet] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [currentConversationId, setCurrentConversationId] = useState<string>()
  const [error, setError] = useState<string | null>(null)

  const handleSend = async (message: string) => {
    if (!message.trim()) return;

    setMessages(prev => [...prev, { 
      role: 'user', 
      content: message,
      timestamp: new Date().toISOString() 
    }]);
    setIsLoading(true);
    setError(null);

    try {
      const response = await ChatService.sendMessage({
        message,
        conversationId: currentConversationId,
        useInternet: false
      });

      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: response.response,
        timestamp: new Date().toISOString()
      }]);
      setCurrentConversationId(response.conversationId);
    } catch (error) {
      console.error('Failed to send message:', error);
      let errorMessage = 'Failed to send message. ';
      
      if (axios.isAxiosError(error)) {
        const axiosError = error as AxiosError<ErrorResponse>;
        if (axiosError.response?.status === 503) {
          errorMessage += 'LM Studio is not available. Please make sure it\'s running and try again.';
        } else if (axiosError.response?.data?.detail) {
          errorMessage += axiosError.response.data.detail;
        } else {
          errorMessage += axiosError.message || 'Please try again later.';
        }
      } else if (error instanceof Error) {
        errorMessage += error.message;
      } else {
        errorMessage += 'Please try again later.';
      }
      
      setError(errorMessage);
      // Remove the user message if it failed
      setMessages(prev => prev.slice(0, -1));
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="fixed inset-0 flex bg-dark">
      {/* Sidebar */}
      <div className="w-80 min-w-[320px] flex-shrink-0 bg-dark-light border-r border-dark-lighter">
        <ConversationList
          onSelectConversation={id => setCurrentConversationId(id)}
          selectedConversationId={currentConversationId}
        />
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-6 bg-dark">
          <div className="max-w-3xl mx-auto">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-gray-400">
                <div className="w-24 h-24 mb-6">
                  <img src="/logo.svg" alt="Chat Logo" className="w-full h-full" />
                </div>
                <h1 className="text-2xl font-semibold mb-2 text-white">How can I help you today?</h1>
                <p className="text-gray-500">Start a conversation by typing a message below.</p>
              </div>
            ) : (
              <div className="space-y-6">
                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[80%] rounded-2xl px-4 py-3 shadow-md ${
                        message.role === 'user'
                          ? 'bg-primary text-white'
                          : 'bg-dark-light text-white border border-gray-700'
                      }`}
                    >
                      <div className="message-content">
                        <p className="text-sm whitespace-pre-wrap break-words leading-relaxed">
                          {message.content}
                        </p>
                        <div className="message-timestamp mt-2 flex justify-end">
                          <span className="text-xs text-gray-300">
                            {new Date(message.timestamp || Date.now()).toLocaleTimeString([], {
                              hour: '2-digit',
                              minute: '2-digit',
                              hour12: true
                            })}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="bg-dark-light text-white rounded-2xl px-4 py-3 max-w-[80%] border border-gray-700">
                      <p className="text-sm">Thinking...</p>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Input Area */}
        <div className="border-t border-dark-lighter p-6">
          <div className="max-w-3xl mx-auto">
            {error && (
              <div className="text-red-500 text-sm mb-4">{error}</div>
            )}
            <div className="flex items-center gap-4">
              <label className="flex items-center gap-2 text-sm text-gray-400">
                <input
                  type="checkbox"
                  checked={useInternet}
                  onChange={e => setUseInternet(e.target.checked)}
                  className="rounded border-gray-600 text-primary focus:ring-primary"
                />
                Use Internet
              </label>
              <div className="flex-1 text-white flex gap-2">
                <input
                  type="text"
                  value={input}
                  onChange={e => setInput(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && !e.shiftKey && handleSend(input)}
                  placeholder="Type your message..."
                  className="chat-input"
                  disabled={isLoading}
                />
                <button
                  onClick={() => handleSend(input)}
                  disabled={isLoading}
                  className="primary-button px-6"
                >
                  <FiSend className={isLoading ? 'animate-spin' : ''} />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
