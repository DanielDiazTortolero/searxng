#!/bin/bash
echo "Testing SearXNG Engine Rotation & Load Distribution"
echo "===================================================="
echo ""

# Test 1: Default search (uses multiple engines)
echo "Test 1: Default search (multiple engines automatically)"
curl -s "http://localhost:8888/search?q=test&format=json" | python -c "
import sys, json
data = json.load(sys.stdin)
engines_used = {}
for result in data.get('results', []):
    for engine in result.get('engines', []):
        engines_used[engine] = engines_used.get(engine, 0) + 1
print(f'Engines used: {len(engines_used)}')
for engine, count in sorted(engines_used.items(), key=lambda x: -x[1]):
    print(f'  - {engine}: {count} results')
"

echo ""
echo "Test 2: 5 consecutive searches to see engine distribution"
for i in {1..5}; do
    echo "Search $i:"
    curl -s "http://localhost:8888/search?q=python+test+$i&format=json" | python -c "
import sys, json
data = json.load(sys.stdin)
engines = set()
for result in data.get('results', []):
    engines.update(result.get('engines', []))
print(f'  Engines: {sorted(engines)[:5]}...')
print(f'  Total results: {len(data.get(\"results\", []))}')
"
    sleep 1
done

echo ""
echo "Test 3: Check if engines are being suspended/rotated"
curl -s "http://localhost:8888/search?q=automation&format=json" | python -c "
import sys, json
data = json.load(sys.stdin)
print(f'Unresponsive engines: {data.get(\"unresponsive_engines\", [])}')
print(f'Total results: {len(data.get(\"results\", []))}')
"
