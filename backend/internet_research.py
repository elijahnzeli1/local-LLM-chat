from typing import List, Dict, Optional
from langchain.tools import Tool
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from bs4 import BeautifulSoup
import requests
import json
import os
from config import get_settings

settings = get_settings()

class InternetResearch:
    def __init__(self):
        self.search_wrapper = GoogleSerperAPIWrapper()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        # Use local embeddings model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            cache_folder=os.path.join(settings.storage_dir, "models")
        )
        
    async def search_and_analyze(self, query: str, max_results: int = 5) -> Dict:
        """
        Perform a search and analyze the results using RAG
        """
        # Perform search
        search_results = self.search_wrapper.results(query, max_results)
        
        # Extract URLs and snippets
        urls = [result.get('link') for result in search_results if result.get('link')]
        
        # Load and process web content
        documents = []
        for url in urls:
            try:
                loader = WebBaseLoader(url)
                web_docs = await loader.aload()
                # Split documents into chunks
                splits = self.text_splitter.split_documents(web_docs)
                documents.extend(splits)
            except Exception as e:
                print(f"Error loading {url}: {str(e)}")
                
        if not documents:
            return {
                "success": False,
                "error": "No valid documents found"
            }
            
        # Create vector store
        vectorstore = FAISS.from_documents(documents, self.embeddings)
        
        # Perform similarity search
        relevant_chunks = vectorstore.similarity_search(query, k=3)
        
        # Format results
        results = {
            "success": True,
            "sources": urls,
            "relevant_content": [
                {
                    "content": doc.page_content,
                    "source": doc.metadata.get("source", "Unknown")
                }
                for doc in relevant_chunks
            ]
        }
        
        return results
    
    async def scrape_webpage(self, url: str) -> Dict:
        """
        Scrape and extract content from a webpage
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
                
            # Extract text content
            text = soup.get_text(separator='\n', strip=True)
            
            # Split into chunks
            chunks = self.text_splitter.split_text(text)
            
            return {
                "success": True,
                "url": url,
                "content": chunks
            }
            
        except Exception as e:
            return {
                "success": False,
                "url": url,
                "error": str(e)
            }
    
    def format_research_for_llm(self, research_results: Dict) -> str:
        """
        Format research results for the LLM context
        """
        if not research_results.get("success"):
            return f"Error performing research: {research_results.get('error', 'Unknown error')}"
            
        formatted = "Internet Research Results:\n\n"
        
        # Add relevant content
        for i, content in enumerate(research_results["relevant_content"], 1):
            formatted += f"Source {i}: {content['source']}\n"
            formatted += f"Content: {content['content']}\n\n"
            
        # Add sources
        formatted += "\nSources:\n"
        for url in research_results["sources"]:
            formatted += f"- {url}\n"
            
        return formatted
