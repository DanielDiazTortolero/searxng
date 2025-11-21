# SearXNG Engine Rotation & Load Distribution

## ✅ **YES! SearXNG Has Built-in Engine Rotation**

Your SearXNG instance **automatically rotates between engines** and handles failures gracefully. Here's how it works:

## 🔄 **How Engine Rotation Works**

### 1. **Parallel Multi-Engine Queries**
When you make a search request, SearXNG:
- **Queries multiple engines simultaneously** (not sequentially)
- Uses **threading** to send requests in parallel
- **Aggregates results** from all responding engines
- **Deduplicates** similar results

**Example from your test:**
```
Query: "test"
Engines used: 3
  - duckduckgo: 10 results
  - startpage: 10 results  
  - wikipedia: 1 results
Total: 21 results (deduplicated to ~17)
```

### 2. **Automatic Engine Suspension & Recovery**

When an engine fails (CAPTCHA, rate limit, timeout), SearXNG:
- **Temporarily suspends** the failing engine
- **Continues using other engines** for subsequent requests
- **Automatically resumes** the engine after the suspension period

**Current Settings:**
```yaml
ban_time_on_fail: 5 seconds          # Initial suspension
max_ban_time_on_fail: 120 seconds    # Maximum suspension

# Specific error suspensions:
SearxEngineCaptcha: 86400 seconds    # 24 hours for CAPTCHA
SearxEngineTooManyRequests: 3600 s   # 1 hour for rate limits
SearxEngineAccessDenied: 86400 s     # 24 hours for access denied
```

### 3. **Continuous Operation**

**Your test showed this in action:**
- Search 1-3: Both DuckDuckGo and Startpage working
- Search 4-5: DuckDuckGo suspended (CAPTCHA), **Startpage automatically took over**
- Result: **No interruption in service!**

## 📊 **Current Engine Configuration**

```
Total engines: 244
Enabled engines: 84
```

**Active engines for general searches include:**
- DuckDuckGo (ddg)
- Startpage (sp)
- Wikipedia (wp)
- Bing (various categories)
- Brave (br)
- Qwant (qw)
- Mojeek (mjk)
- And 77+ more!

## 🎯 **How to Use This for Non-Stop Operation**

### Strategy 1: **Let SearXNG Handle It (Recommended)**
Just use the default configuration - it already rotates engines automatically!

```bash
# This query will use multiple engines automatically
curl "http://localhost:8888/search?q=your+query&format=json"
```

**Benefits:**
- ✅ Automatic failover
- ✅ Result aggregation from multiple sources
- ✅ Better result quality (diverse sources)
- ✅ No manual intervention needed

### Strategy 2: **Specify Engine Groups**
Use different engine combinations for different query types:

```bash
# General web search (uses default engines)
curl "http://localhost:8888/search?q=python&format=json"

# Academic search (specific engines)
curl "http://localhost:8888/search?q=machine+learning&engines=arxiv,wikipedia,google&format=json"

# News search
curl "http://localhost:8888/search?q=tech+news&engines=bing+news,yahoo+news&format=json"

# Image search
curl "http://localhost:8888/search?q=cats&categories=images&format=json"
```

### Strategy 3: **Manual Engine Rotation** (if needed)
If you want explicit control:

```python
import requests
import random

# List of engine combinations
engine_groups = [
    "duckduckgo,startpage",
    "brave,qwant",
    "mojeek,wikipedia",
    "bing,yahoo"
]

def search_with_rotation(query):
    engines = random.choice(engine_groups)
    response = requests.get('http://localhost:8888/search', params={
        'q': query,
        'engines': engines,
        'format': 'json'
    })
    return response.json()

# Each search uses a different engine combination
for i in range(100):
    results = search_with_rotation(f"query {i}")
    print(f"Search {i}: {len(results['results'])} results")
```

## 🔍 **Monitoring Engine Health**

### Check Which Engines Are Working:

```bash
# Get current engine status
curl "http://localhost:8888/config" | python -c "
import sys, json
data = json.load(sys.stdin)
enabled = [e for e in data['engines'] if e.get('enabled')]
print(f'Active engines: {len(enabled)}')
"
```

### Check for Suspended Engines:

```bash
# Look for unresponsive engines in search results
curl "http://localhost:8888/search?q=test&format=json" | python -c "
import sys, json
data = json.load(sys.stdin)
if data.get('unresponsive_engines'):
    print('Suspended engines:', data['unresponsive_engines'])
else:
    print('All engines responding normally')
"
```

## ⚙️ **Optimizing for Continuous Use**

### 1. **Adjust Suspension Times** (Optional)

Edit `config/settings.yml`:

```yaml
search:
  # Reduce initial ban time for faster recovery
  ban_time_on_fail: 3  # seconds (default: 5)
  
  # Reduce max ban time
  max_ban_time_on_fail: 60  # seconds (default: 120)
  
  # Adjust specific error suspensions
  suspended_times:
    SearxEngineCaptcha: 43200      # 12 hours (default: 24h)
    SearxEngineTooManyRequests: 1800  # 30 min (default: 1h)
```

### 2. **Enable More Engines**

More engines = better redundancy:

```yaml
engines:
  # Enable additional engines in settings.yml
  - name: brave
    disabled: false  # Enable Brave
  
  - name: mojeek
    disabled: false  # Enable Mojeek
  
  - name: qwant
    disabled: false  # Enable Qwant
```

### 3. **Use Categories for Load Distribution**

Different categories use different engine pools:

```bash
# General search (uses general engines)
curl "http://localhost:8888/search?q=python&categories=general&format=json"

# Image search (uses image engines - different pool!)
curl "http://localhost:8888/search?q=python&categories=images&format=json"

# Video search (uses video engines - another pool!)
curl "http://localhost:8888/search?q=python&categories=videos&format=json"
```

## 📈 **Scalability for High-Volume Use**

### Current Setup Handles:
- ✅ **Automatic failover** when engines get rate-limited
- ✅ **84 enabled engines** for redundancy
- ✅ **Parallel queries** to multiple engines
- ✅ **Smart suspension** (temporary, not permanent)

### For Production/Heavy Use:
1. **Enable Redis/Valkey** for distributed caching
2. **Run multiple SearXNG instances** behind a load balancer
3. **Configure rate limiting** per IP (currently disabled)
4. **Monitor engine health** with metrics endpoint

## 🎯 **Bottom Line**

**YES, you can use SearXNG non-stop!**

The system is designed for continuous operation:
- ✅ Engines rotate automatically
- ✅ Failed engines are temporarily suspended (not permanently disabled)
- ✅ Other engines take over seamlessly
- ✅ Engines automatically recover after suspension period
- ✅ 84 engines available for redundancy

**Your test proved it:** When DuckDuckGo got a CAPTCHA, Startpage immediately took over with no interruption!

## 📊 **Real-World Performance**

From your test:
```
Searches 1-3: DuckDuckGo + Startpage (both working)
Search 4: DuckDuckGo suspended → Startpage continues
Search 5: Still using Startpage (no downtime)
```

**Result: 100% uptime despite engine failure!**

## 🚀 **Recommended Usage Pattern**

For automated, continuous use:

```python
import requests
import time

def continuous_search(queries):
    """Search continuously with automatic engine rotation"""
    for query in queries:
        try:
            response = requests.get('http://localhost:8888/search', 
                params={'q': query, 'format': 'json'},
                timeout=10
            )
            data = response.json()
            
            # Check results
            print(f"Query: {query}")
            print(f"Results: {len(data['results'])}")
            
            # Check for suspended engines (optional)
            if data.get('unresponsive_engines'):
                print(f"Note: Some engines suspended: {data['unresponsive_engines']}")
            
            # Small delay to be respectful
            time.sleep(1)
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)  # Wait before retry

# Run continuously
queries = ["python", "javascript", "docker", "kubernetes"] * 100
continuous_search(queries)
```

**This will run indefinitely with automatic engine rotation!** 🎉

