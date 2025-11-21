"""
Google Custom Search API script for grant names.
Reads grant names from CSV, searches each one using Google, and saves the top result link to CSV.
"""

import argparse
import csv
import os
from pathlib import Path

import requests
from dotenv import load_dotenv


# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_SEARCH_ENGINE_ID = os.getenv('GOOGLE_SEARCH_ENGINE_ID')

# Validate credentials
if not GOOGLE_API_KEY or not GOOGLE_SEARCH_ENGINE_ID:
    print("ERROR: GOOGLE_API_KEY or GOOGLE_SEARCH_ENGINE_ID not found in .env")
    exit(1)


def clean_grant_name(grant_name: str) -> str:
    """Add 'grant' to the query if it's not already there."""
    grant_name = grant_name.strip()
    if grant_name.lower().endswith('grant') or ' grant ' in grant_name.lower():
        return grant_name
    return f"{grant_name} grant"


def search_grant_google(query: str) -> list:
    """
    Search Google Custom Search API for a query and return all result links.
    Returns empty list if no results or API error.
    """
    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'q': query,
            'key': GOOGLE_API_KEY,
            'cx': GOOGLE_SEARCH_ENGINE_ID,
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            
            if items:
                # Return all result links
                links = [item.get('link', '') for item in items]
                return [link for link in links if link]  # Filter out empty links
        else:
            print(f"  API Error (status {response.status_code}): {response.text}")
        
        return []
    
    except Exception as e:
        print(f"  ERROR: {e}")
        return []


def main():
    parser = argparse.ArgumentParser(
        description='Search grants using Google Custom Search API'
    )
    parser.add_argument(
        '--input',
        default='grant_queries_for_ddg.csv',
        help='Input CSV file with grant names (default: grant_queries_for_ddg.csv)'
    )
    parser.add_argument(
        '--output',
        default='grant_links_discovered_google.csv',
        help='Output CSV file for top results (default: grant_links_discovered_google.csv)'
    )
    
    args = parser.parse_args()
    input_file = args.input
    output_file = args.output
    output_file_full = output_file.replace('.csv', '_full.csv')
    
    # Check if input file exists
    if not Path(input_file).exists():
        print(f"ERROR: Input file '{input_file}' not found!")
        return
    
    query_count = 0
    
    # Open both output files for writing in real-time
    with open(output_file, 'w', newline='', encoding='utf-8') as out_csv, \
         open(output_file_full, 'w', newline='', encoding='utf-8') as out_csv_full:
        
        writer = csv.writer(out_csv)
        writer.writerow(['grant_name', 'search_query', 'link'])
        
        writer_full = csv.writer(out_csv_full)
        writer_full.writerow(['grant_name', 'search_query', 'link'])
        
        # Read input CSV and process each grant
        with open(input_file, 'r', encoding='utf-8') as in_csv:
            reader = csv.DictReader(in_csv)
            
            for idx, row in enumerate(reader, start=1):
                grant_name = row.get('grant_name', '').strip()
                
                # Skip empty rows or header-like entries
                if not grant_name or grant_name.lower() == 'grant_name':
                    continue
                
                # Create search query
                search_query = clean_grant_name(grant_name)
                
                print(f"\n[{idx}] Searching: {grant_name}")
                print(f"    Query: {search_query}")
                
                # Search and get all links (single API call)
                all_links = search_grant_google(search_query)
                query_count += 1
                
                if all_links:
                    print(f"    ✓ Found {len(all_links)} results")
                    
                    # Write top result to main CSV
                    writer.writerow([grant_name, search_query, all_links[0]])
                    out_csv.flush()
                    
                    # Write all results to full CSV (each as separate row)
                    for link in all_links:
                        writer_full.writerow([grant_name, search_query, link])
                    out_csv_full.flush()
                else:
                    print(f"    ✗ No results")
                    writer.writerow([grant_name, search_query, ''])
                    out_csv.flush()
    
    print(f"\n✓ Complete!")
    print(f"  Top results saved to: {output_file}")
    print(f"  Full results saved to: {output_file_full}")
    print(f"✓ Total queries made: {query_count}")
    print(f"  (Free tier: 100 queries/day. $5 per 1,000 queries above that)")


if __name__ == "__main__":
    main()

