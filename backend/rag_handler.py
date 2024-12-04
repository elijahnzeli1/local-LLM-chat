from typing import Optional, Tuple
from web_retriever import WebRetriever
from llm_handler import LMStudioHandler
from conversation_manager import ConversationManager
from config import get_settings

settings = get_settings()

class RAGHandler:
    def __init__(self):
        self.web_retriever = WebRetriever(cache_dir=settings.CACHE_DIR)
        self.llm_handler = LMStudioHandler(
            base_url=settings.LM_STUDIO_URL,
            max_tokens=settings.LM_STUDIO_MAX_TOKENS,
            temperature=settings.LM_STUDIO_TEMPERATURE
        )
        self.conversation_manager = ConversationManager()
        
    def _create_augmented_prompt(self, user_message: str, context: str, conversation_history: str) -> str:
        """Create a prompt that includes conversation history, context, and the user's message."""
        prompt = "You are a helpful AI assistant. "
        
        if conversation_history:
            prompt += f"\n\n{conversation_history}\n"
        
        prompt += f"""
Please help answer the user's question using the provided context information. If the context doesn't contain relevant information, you can answer based on your general knowledge.

Context information:
{context}

User's question: {user_message}

Please provide a helpful and accurate response:"""
        return prompt

    def _create_direct_prompt(self, user_message: str, conversation_history: str) -> str:
        """Create a prompt for direct LLM interaction with conversation history."""
        prompt = "You are a helpful AI assistant. "
        
        if conversation_history:
            prompt += f"\n\n{conversation_history}\n"
        
        prompt += f"""Please help answer the user's question. If you're not sure about something, please acknowledge that.

User's question: {user_message}

Please provide a helpful and accurate response:"""
        return prompt

    async def generate_response(
        self,
        message: str,
        conv_id: str,
        use_internet: bool = False
    ) -> Tuple[Optional[str], str]:
        """Generate a response using RAG if internet is enabled, or direct LLM if not."""
        try:
            # Create new conversation if conv_id is not provided or invalid
            if not conv_id or not self.conversation_manager.get_conversation_history(conv_id):
                conv_id = self.conversation_manager.create_conversation()
            
            # Get conversation history
            conversation_history = self.conversation_manager.format_history_for_llm(conv_id)
            
            if use_internet:
                # Get relevant information from the web
                search_results = self.web_retriever.search(message)
                context = self.web_retriever.format_results(search_results)
                prompt = self._create_augmented_prompt(message, context, conversation_history)
            else:
                prompt = self._create_direct_prompt(message, conversation_history)
            
            # Add user message to conversation
            self.conversation_manager.add_message(conv_id, "user", message)
            
            # Generate response using LLM
            response = self.llm_handler.generate_response(prompt)
            
            if response:
                # Add assistant response to conversation
                self.conversation_manager.add_message(conv_id, "assistant", response)
                return response, conv_id
            
            return "I apologize, but I couldn't generate a response at this time.", conv_id
            
        except Exception as e:
            print(f"Error in RAG handler: {str(e)}")
            return None, conv_id
            
    def is_available(self) -> bool:
        """Check if the LLM service is available."""
        return self.llm_handler.is_available()
        
    def cleanup(self):
        """Clean up expired conversations."""
        self.conversation_manager.cleanup_expired_conversations()
