# SearXNG REST API - Usage Guide

## ✅ Status: **FULLY OPERATIONAL**

Your SearXNG instance is running at: **http://localhost:8888**

## 🔍 Quick API Examples

### 1. Basic JSON Search
```bash
curl "http://localhost:8888/search?q=python&format=json"
```

### 2. Search with Specific Engines
```bash
curl "http://localhost:8888/search?q=linux&engines=duckduckgo,wikipedia&format=json"
```

### 3. CSV Format
```bash
curl "http://localhost:8888/search?q=data&format=csv"
```

### 4. RSS Feed
```bash
curl "http://localhost:8888/search?q=news&format=rss"
```

### 5. POST Method
```bash
curl -X POST -d "q=automation&format=json" "http://localhost:8888/search"
```

### 6. Category-based Search
```bash
# Search images only
curl "http://localhost:8888/search?q=cats&categories=images&format=json"

# Search videos only  
curl "http://localhost:8888/search?q=tutorials&categories=videos&format=json"
```

### 7. Advanced Parameters
```bash
# Safe search + language + time range
curl "http://localhost:8888/search?q=python&safesearch=2&language=en&time_range=month&format=json"

# Pagination
curl "http://localhost:8888/search?q=programming&pageno=2&format=json"
```

### 8. Get Instance Configuration
```bash
curl "http://localhost:8888/config"
```

## 📊 API Parameters

| Parameter | Description | Values |
|-----------|-------------|---------|
| `q` | Search query (required) | Any string |
| `format` | Output format | `html`, `json`, `csv`, `rss` |
| `categories` | Search categories | `general`, `images`, `videos`, `news`, `music`, `files`, `it`, `science`, `map` |
| `engines` | Specific engines to use | `duckduckgo`, `google`, `bing`, `wikipedia`, etc. (comma-separated) |
| `language` | Search language | `en`, `de`, `fr`, `es`, etc. |
| `pageno` | Page number | Integer (default: 1) |
| `time_range` | Time filter | `day`, `month`, `year` |
| `safesearch` | Safe search level | `0` (off), `1` (moderate), `2` (strict) |

## 🐍 Python Example

```python
import requests
import json

# Simple search
response = requests.get('http://localhost:8888/search', params={
    'q': 'machine learning',
    'format': 'json',
    'engines': 'duckduckgo,wikipedia'
})

data = response.json()
print(f"Found {len(data['results'])} results")

for result in data['results'][:5]:
    print(f"- {result['title']}")
    print(f"  {result['url']}")
```

## 🌐 JavaScript Example

```javascript
async function searchSearXNG(query) {
    const response = await fetch(`http://localhost:8888/search?q=${encodeURIComponent(query)}&format=json`);
    const data = await response.json();
    
    console.log(`Found ${data.results.length} results`);
    return data.results;
}

searchSearXNG('artificial intelligence').then(results => {
    results.forEach(r => console.log(r.title, r.url));
});
```

## 📁 JSON Response Structure

```json
{
  "query": "python programming",
  "number_of_results": 17,
  "results": [
    {
      "url": "https://www.python.org/",
      "title": "Welcome to Python.org",
      "content": "The official home of the Python Programming Language...",
      "engine": "startpage",
      "parsed_url": ["https", "www.python.org", "/", "", "", ""],
      "template": "default.html",
      "engines": ["startpage"],
      "positions": [1],
      "score": 2.0,
      "category": "general"
    }
  ],
  "answers": [],
  "corrections": [],
  "infoboxes": [],
  "suggestions": [],
  "unresponsive_engines": []
}
```

## 🔒 Security Notes

- **Current Setup**: Limiter is DISABLED for development/local use
- **For Production**: 
  - Enable the limiter in `settings.yml`
  - Configure `limiter.toml` with appropriate IP whitelists
  - Set up HTTPS with a reverse proxy (nginx/apache)
  - Use a strong secret key (already configured)

## 🚀 Automation Use Cases

- **Data Collection**: Aggregate search results from multiple sources
- **Research Tools**: Academic and market research automation
- **Monitoring**: Track search trends and results over time
- **Integration**: Add search capabilities to applications
- **Chatbots/AI**: Power conversational agents with web search
- **Content Discovery**: Automated content curation

## 🛠️ Management Commands

```bash
# Check status
docker ps | grep searxng

# View logs
docker logs searxng

# Restart
docker restart searxng

# Stop
docker stop searxng

# Start
docker start searxng

# Remove (warning: will lose data if volumes not properly mounted)
docker rm -f searxng
```

## 📝 Configuration Files

- **Settings**: `/c/Users/Iverson Lab/Documents/GitHub/searxng-deployment/config/settings.yml`
- **Rate Limiting**: `/c/Users/Iverson Lab/Documents/GitHub/searxng-deployment/config/limiter.toml`
- **Data/Cache**: `/c/Users/Iverson Lab/Documents/GitHub/searxng-deployment/data/`

## 🎯 Key Features

✅ **Multiple Output Formats**: JSON, HTML, CSV, RSS  
✅ **244 Search Engines** available  
✅ **No Rate Limiting** (currently disabled for local development)  
✅ **Privacy-Focused**: No tracking or profiling  
✅ **Category Filtering**: Images, videos, news, science, IT, etc.  
✅ **Language Support**: Multi-language searches  
✅ **Time Filters**: Recent results (day, month, year)  
✅ **Safe Search**: Configurable content filtering  
✅ **RESTful API**: Clean, predictable endpoints  

## 📚 Documentation

- **Official API Docs**: https://docs.searxng.org/dev/search_api.html
- **Engine List**: https://docs.searxng.org/admin/engines/configured_engines.html
- **Admin Guide**: https://docs.searxng.org/admin/index.html

---

**Instance**: SearXNG (Local Development)  
**Version**: 2025.11.21-b876d0bed  
**Port**: 8888  
**Status**: ✅ Running

