import argparse
from web_search import WebSearch
from summarizer import Summarizer
import os
from datetime import datetime

def save_report(report: str, query: str):
    """Save the report to a file."""
    # Create reports directory if it doesn't exist
    os.makedirs('reports', exist_ok=True)
    
    # Create filename from query and timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"reports/research_{query.replace(' ', '_')}_{timestamp}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return filename

def main():
    parser = argparse.ArgumentParser(description='SageScope - Cross-domain Research Assistant')
    parser.add_argument('query', help='Research query')
    parser.add_argument('--max-results', type=int, default=5, help='Maximum number of results per source')
    parser.add_argument('--output', choices=['console', 'file', 'both'], default='both',
                      help='Output format (console, file, or both)')
    
    args = parser.parse_args()
    
    print(f"\n🔍 SageScope Research Assistant")
    print(f"Query: {args.query}")
    print("\nSearching across multiple sources...")
    
    # Initialize components
    searcher = WebSearch()
    summarizer = Summarizer()
    
    # Perform search
    search_results = searcher.search_all(args.query, args.max_results)
    
    if not search_results:
        print("No results found. Please try a different query.")
        return
    
    print(f"\nFound {len(search_results)} results. Processing and summarizing...")
    
    # Process and summarize results
    processed_results = summarizer.process_search_results(search_results)
    
    if not processed_results:
        print("Failed to process any results. Please try again.")
        return
    
    # Generate report
    report = summarizer.generate_report(processed_results)
    
    # Output handling
    if args.output in ['console', 'both']:
        print("\n" + "="*80 + "\n")
        print(report)
    
    if args.output in ['file', 'both']:
        filename = save_report(report, args.query)
        print(f"\nReport saved to: {filename}")

if __name__ == "__main__":
    main() 