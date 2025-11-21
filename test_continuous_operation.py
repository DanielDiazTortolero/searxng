#!/usr/bin/env python3
"""
Test SearXNG Continuous Operation with Engine Rotation
Demonstrates that SearXNG can handle continuous queries with automatic failover
"""

import requests
import time
import json
from datetime import datetime
from collections import defaultdict

SEARXNG_URL = "http://localhost:8888"

def test_continuous_operation(num_searches=20, delay=1):
    """
    Test continuous operation with engine rotation tracking
    
    Args:
        num_searches: Number of searches to perform
        delay: Delay between searches in seconds
    """
    
    print("=" * 70)
    print("SearXNG Continuous Operation Test")
    print("=" * 70)
    print(f"Testing {num_searches} consecutive searches with {delay}s delay")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Track statistics
    stats = {
        'total_searches': 0,
        'successful_searches': 0,
        'failed_searches': 0,
        'total_results': 0,
        'engines_used': defaultdict(int),
        'suspended_engines': defaultdict(int),
        'response_times': []
    }
    
    # Test queries
    queries = [
        "python programming",
        "machine learning",
        "docker containers",
        "kubernetes deployment",
        "artificial intelligence",
        "web development",
        "data science",
        "cloud computing",
        "cybersecurity",
        "blockchain technology"
    ]
    
    for i in range(num_searches):
        query = queries[i % len(queries)]
        stats['total_searches'] += 1
        
        print(f"\n[{i+1}/{num_searches}] Query: '{query}'")
        
        try:
            start_time = time.time()
            
            response = requests.get(
                f"{SEARXNG_URL}/search",
                params={'q': query, 'format': 'json'},
                timeout=15
            )
            
            elapsed = time.time() - start_time
            stats['response_times'].append(elapsed)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                num_results = len(results)
                
                stats['successful_searches'] += 1
                stats['total_results'] += num_results
                
                # Track engines used
                engines_in_this_search = set()
                for result in results:
                    for engine in result.get('engines', []):
                        stats['engines_used'][engine] += 1
                        engines_in_this_search.add(engine)
                
                # Track suspended engines
                unresponsive = data.get('unresponsive_engines', [])
                for engine_info in unresponsive:
                    if isinstance(engine_info, list) and len(engine_info) > 0:
                        engine_name = engine_info[0]
                        reason = engine_info[1] if len(engine_info) > 1 else 'unknown'
                        stats['suspended_engines'][engine_name] += 1
                        print(f"  ⚠️  Engine suspended: {engine_name} ({reason})")
                
                print(f"  ✅ Success: {num_results} results from {len(engines_in_this_search)} engines")
                print(f"  ⏱️  Response time: {elapsed:.2f}s")
                print(f"  🔍 Engines: {', '.join(sorted(engines_in_this_search))}")
                
            else:
                stats['failed_searches'] += 1
                print(f"  ❌ Failed: HTTP {response.status_code}")
                
        except requests.exceptions.Timeout:
            stats['failed_searches'] += 1
            print(f"  ❌ Failed: Timeout")
        except Exception as e:
            stats['failed_searches'] += 1
            print(f"  ❌ Failed: {str(e)}")
        
        # Delay before next search
        if i < num_searches - 1:
            time.sleep(delay)
    
    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total searches: {stats['total_searches']}")
    print(f"Successful: {stats['successful_searches']} ({stats['successful_searches']/stats['total_searches']*100:.1f}%)")
    print(f"Failed: {stats['failed_searches']} ({stats['failed_searches']/stats['total_searches']*100:.1f}%)")
    print(f"Total results: {stats['total_results']}")
    print(f"Average results per search: {stats['total_results']/max(stats['successful_searches'],1):.1f}")
    
    if stats['response_times']:
        avg_time = sum(stats['response_times']) / len(stats['response_times'])
        min_time = min(stats['response_times'])
        max_time = max(stats['response_times'])
        print(f"\nResponse Times:")
        print(f"  Average: {avg_time:.2f}s")
        print(f"  Min: {min_time:.2f}s")
        print(f"  Max: {max_time:.2f}s")
    
    print(f"\nEngines Used (Top 10):")
    sorted_engines = sorted(stats['engines_used'].items(), key=lambda x: -x[1])
    for engine, count in sorted_engines[:10]:
        print(f"  {engine}: {count} results")
    
    if stats['suspended_engines']:
        print(f"\n⚠️  Engines Suspended During Test:")
        for engine, count in sorted(stats['suspended_engines'].items()):
            print(f"  {engine}: {count} times")
        print(f"\n✅ Despite suspensions, searches continued successfully!")
        print(f"   This proves automatic engine rotation is working!")
    else:
        print(f"\n✅ No engines were suspended during this test!")
        print(f"   All engines performed normally.")
    
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Final verdict
    success_rate = stats['successful_searches'] / stats['total_searches'] * 100
    if success_rate >= 95:
        print("\n🎉 EXCELLENT: SearXNG is ready for continuous operation!")
    elif success_rate >= 80:
        print("\n✅ GOOD: SearXNG can handle continuous operation with minor issues.")
    else:
        print("\n⚠️  WARNING: Success rate is lower than expected. Check configuration.")
    
    return stats

if __name__ == "__main__":
    import sys
    
    # Parse arguments
    num_searches = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    delay = float(sys.argv[2]) if len(sys.argv) > 2 else 1
    
    try:
        stats = test_continuous_operation(num_searches, delay)
        
        # Exit with success if success rate is good
        success_rate = stats['successful_searches'] / stats['total_searches'] * 100
        sys.exit(0 if success_rate >= 80 else 1)
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\n\nFatal error: {e}")
        sys.exit(1)

