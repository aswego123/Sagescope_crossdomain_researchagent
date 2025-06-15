import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from urllib.parse import urlparse
import time
from gemini_api import GeminiAPI

class Summarizer:
    def __init__(self):
        self.gemini = GeminiAPI()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def extract_content(self, url: str) -> Optional[str]:
        """Extract main content from a URL."""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'header']):
                element.decompose()
            
            # Extract text content
            text = ' '.join([p.get_text().strip() for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])])
            
            return text if text else None
            
        except Exception as e:
            print(f"Failed to extract content from {url}: {str(e)}")
            return None

    def process_search_results(self, search_results: List[Dict]) -> List[Dict]:
        """Process search results and generate summaries."""
        processed_results = []
        
        for result in search_results:
            url = result['url']
            source = result['source']
            
            # Skip if we already have a good snippet
            if len(result['snippet']) > 200:
                content = result['snippet']
            else:
                content = self.extract_content(url)
                if not content:
                    continue
            
            try:
                # Generate summary using Gemini
                summary = self.gemini.generate_summary(content)
                key_points = self.gemini.extract_key_points(content)
                
                processed_results.append({
                    'title': result['title'],
                    'url': url,
                    'source': source,
                    'summary': summary,
                    'key_points': key_points
                })
                
                # Be nice to servers
                time.sleep(1)
                
            except Exception as e:
                print(f"Failed to process {url}: {str(e)}")
                continue
        
        return processed_results

    def generate_report(self, processed_results: List[Dict]) -> str:
        """Generate a formatted research report."""
        report = "# Research Report\n\n"
        
        for result in processed_results:
            report += f"## {result['title']}\n"
            report += f"Source: {result['source']} - {result['url']}\n\n"
            
            report += "### Summary\n"
            report += f"{result['summary']}\n\n"
            
            report += "### Key Points\n"
            for point in result['key_points']:
                report += f"- {point}\n"
            report += "\n---\n\n"
        
        return report 