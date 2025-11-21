#!/usr/bin/env python3
"""
SearXNG API Demo Script
Shows how to use the SearXNG REST API for automated searches
"""

import requests
import json
from typing import Dict, List, Any

class SearXNGClient:
    def __init__(self, base_url: str = "http://localhost:8888"):
        self.base_url = base_url
        self.session = requests.Session()
        # Set a browser-like user agent to avoid bot detection
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def search(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Perform a search using the SearXNG API

        Args:
            query: The search query
            **kwargs: Additional search parameters like:
                - format: 'json', 'html', 'csv', 'rss'
                - categories: comma-separated list (general, images, videos, etc.)
                - engines: comma-separated list of engines to use
                - language: language code (en, de, fr, etc.)
                - pageno: page number for pagination
                - time_range: 'day', 'month', 'year'
                - safesearch: 0 (off), 1 (moderate), 2 (strict)

        Returns:
            Dict containing search results
        """
        params = {
            'q': query,
            'format': kwargs.get('format', 'json'),
            **kwargs
        }

        try:
            response = self.session.get(f"{self.base_url}/search", params=params)
            response.raise_for_status()

            if params['format'] == 'json':
                return response.json()
            else:
                return {'html': response.text}

        except requests.RequestException as e:
            return {'error': str(e)}

    def get_config(self) -> Dict[str, Any]:
        """Get instance configuration"""
        try:
            response = self.session.get(f"{self.base_url}/config")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {'error': str(e)}

def demo_api():
    """Demonstrate SearXNG API usage"""
    client = SearXNGClient()

    print("🔍 SearXNG API Demo")
    print("=" * 50)

    # Get instance configuration
    print("\n📋 Instance Configuration:")
    config = client.get_config()
    if 'error' not in config:
        print(f"Instance Name: {config.get('instance_name', 'Unknown')}")
        print(f"Enabled Engines: {len(config.get('engines', []))}")
        print(f"Available Categories: {list(config.get('categories', {}).keys())}")
    else:
        print(f"Error getting config: {config['error']}")

    # Perform searches
    queries = [
        "python programming",
        "artificial intelligence",
        "renewable energy"
    ]

    for query in queries:
        print(f"\n🔎 Searching for: '{query}'")
        print("-" * 40)

        results = client.search(query, format='json', pageno=1)

        if 'error' in results:
            print(f"❌ Error: {results['error']}")
        elif 'results' in results:
            print(f"✅ Found {len(results['results'])} results")
            print(f"Query: {results.get('query', 'N/A')}")
            print(f"Search time: {results.get('search', {}).get('timing', {}).get('all', 'N/A')}s")

            # Show first 3 results
            for i, result in enumerate(results['results'][:3], 1):
                print(f"\n{i}. {result.get('title', 'No title')}")
                print(f"   URL: {result.get('url', 'No URL')}")
                print(f"   Engine: {result.get('engine', 'Unknown')}")
        else:
            print("❌ Unexpected response format")
            print(results)

        print()

def show_api_examples():
    """Show various API usage examples"""
    print("\n📚 API Usage Examples:")
    print("=" * 50)

    examples = [
        {
            'description': 'Basic JSON search',
            'url': 'http://localhost:8888/search?q=python&format=json'
        },
        {
            'description': 'Search with specific engines',
            'url': 'http://localhost:8888/search?q=linux&engines=duckduckgo,wikipedia&format=json'
        },
        {
            'description': 'Search in images category',
            'url': 'http://localhost:8888/search?q=cats&categories=images&format=json'
        },
        {
            'description': 'Safe search enabled',
            'url': 'http://localhost:8888/search?q=games&safesearch=2&format=json'
        },
        {
            'description': 'Search in German',
            'url': 'http://localhost:8888/search?q=künstliche intelligenz&language=de&format=json'
        },
        {
            'description': 'Get CSV results',
            'url': 'http://localhost:8888/search?q=data&format=csv'
        },
        {
            'description': 'Get RSS feed',
            'url': 'http://localhost:8888/search?q=news&format=rss'
        }
    ]

    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['description']}")
        print(f"   curl '{example['url']}'")

    print("\n💡 POST method also supported:")
    print("   curl -X POST -d 'q=python&format=json' http://localhost:8888/search")

if __name__ == "__main__":
    print("🚀 SearXNG API Automation Demo")
    print("Note: Make sure SearXNG is running on http://localhost:8888")

    try:
        demo_api()
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted")

    show_api_examples()

    print("\n🎯 Key Features for Automation:")
    print("• JSON, CSV, RSS output formats")
    print("• Multiple search engines")
    print("• Category-based searches")
    print("• Language-specific searches")
    print("• Safe search filtering")
    print("• Pagination support")
    print("• RESTful API design")

