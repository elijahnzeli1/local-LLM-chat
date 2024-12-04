import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import json
from datetime import datetime
import os

class WebRetriever:
    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        
    def _get_cache_path(self, query: str) -> str:
        """Generate a cache file path for a given query."""
        safe_query = "".join(x for x in query if x.isalnum() or x in [' ', '-', '_'])[:50]
        return os.path.join(self.cache_dir, f"{safe_query}.json")
        
    def _load_from_cache(self, query: str) -> Optional[Dict]:
        """Load cached results if they exist and are recent."""
        cache_path = self._get_cache_path(query)
        if os.path.exists(cache_path):
            with open(cache_path, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)
                # Check if cache is less than 1 hour old
                cache_time = datetime.fromisoformat(cached_data['timestamp'])
                if (datetime.now() - cache_time).total_seconds() < 3600:
                    return cached_data
        return None
        
    def _save_to_cache(self, query: str, data: List[Dict]):
        """Save results to cache."""
        cache_path = self._get_cache_path(query)
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)

    def search(self, query: str, use_cache: bool = True) -> List[Dict]:
        """
        Search the web for relevant information.
        Returns a list of dictionaries containing titles and snippets.
        """
        if use_cache:
            cached_result = self._load_from_cache(query)
            if cached_result:
                return cached_result['data']

        try:
            # Using DuckDuckGo HTML as it doesn't require API key
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(
                f'https://html.duckduckgo.com/html/?q={query}',
                headers=headers
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            # Extract search results
            for result in soup.select('.result'):
                title_elem = result.select_one('.result__title')
                snippet_elem = result.select_one('.result__snippet')
                
                if title_elem and snippet_elem:
                    results.append({
                        'title': title_elem.get_text(strip=True),
                        'snippet': snippet_elem.get_text(strip=True)
                    })
            
            if results and use_cache:
                self._save_to_cache(query, results)
                
            return results[:5]  # Return top 5 results
            
        except Exception as e:
            print(f"Error in web retrieval: {str(e)}")
            return []

    def format_results(self, results: List[Dict]) -> str:
        """Format search results into a string for the LLM."""
        if not results:
            return "No relevant information found."
            
        formatted = "Here is the relevant information I found:\n\n"
        for i, result in enumerate(results, 1):
            formatted += f"{i}. {result['title']}\n"
            formatted += f"   {result['snippet']}\n\n"
        
        return formatted
