import os
from typing import List, Dict, Optional
from tavily import TavilyClient
import arxiv
import scholarly
import wikipedia
from pymed import PubMed
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSearch:
    def __init__(self):
        load_dotenv(override=True)
        self.tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        
    def search_tavily(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search using Tavily API."""
        try:
            response = self.tavily_client.search(query, search_depth="advanced", max_results=max_results)
            return [{
                "title": result["title"],
                "url": result["url"],
                "snippet": result["content"],
                "source": "tavily"
            } for result in response["results"]]
        except Exception as e:
            logger.error(f"Tavily search failed: {str(e)}")
            return []

    def search_arxiv(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search academic papers using arXiv."""
        try:
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            results = []
            for paper in search.results():
                results.append({
                    "title": paper.title,
                    "url": paper.entry_id,
                    "snippet": paper.summary,
                    "source": "arxiv"
                })
            return results
        except Exception as e:
            logger.error(f"arXiv search failed: {str(e)}")
            return []

    def search_scholar(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search using Google Scholar."""
        try:
            # Use the correct method for scholarly
            search_query = scholarly.search_pubs(query)
            results = []
            for _ in range(max_results):
                try:
                    paper = next(search_query)
                    results.append({
                        "title": paper.bib.get('title', ''),
                        "url": paper.bib.get('url', ''),
                        "snippet": paper.bib.get('abstract', ''),
                        "source": "scholar"
                    })
                except StopIteration:
                    break
            return results
        except Exception as e:
            logger.error(f"Scholar search failed: {str(e)}")
            return []

    def search_wikipedia(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search Wikipedia articles."""
        try:
            search_results = wikipedia.search(query, results=max_results)
            results = []
            for title in search_results:
                try:
                    page = wikipedia.page(title)
                    results.append({
                        "title": page.title,
                        "url": page.url,
                        "snippet": page.summary,
                        "source": "wikipedia"
                    })
                except:
                    continue
            return results
        except Exception as e:
            logger.error(f"Wikipedia search failed: {str(e)}")
            return []

    def search_pubmed(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search medical research using PubMed."""
        try:
            pubmed = PubMed()
            results = []
            for article in pubmed.query(query, max_results=max_results):
                # Get the PMID from the article's attributes
                pmid = getattr(article, 'pubmed_id', None)
                if pmid:
                    results.append({
                        "title": article.title,
                        "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                        "snippet": article.abstract,
                        "source": "pubmed"
                    })
            return results
        except Exception as e:
            logger.error(f"PubMed search failed: {str(e)}")
            return []

    def search_all(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search across all available sources."""
        all_results = []
        
        # Search from different sources
        all_results.extend(self.search_tavily(query, max_results))
        all_results.extend(self.search_arxiv(query, max_results))
        all_results.extend(self.search_scholar(query, max_results))
        all_results.extend(self.search_wikipedia(query, max_results))
        all_results.extend(self.search_pubmed(query, max_results))
        
        return all_results 