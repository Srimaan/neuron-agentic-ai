# Setup: Advanced Context Patterns

Prepare your environment for production context patterns.

---

## Prerequisites

✅ Week 2 Day 1 completed
✅ Python 3.9+
✅ SQLite/PostgreSQL running
✅ Redis available (for caching)
✅ API keys configured

---

## Step 1: Install Additional Dependencies

```bash
# RAG & Embeddings
pip install sentence-transformers
pip install pinecone-client
pip install weaviate-client

# Caching
pip install redis

# Monitoring
pip install prometheus-client
pip install opentelemetry-api opentelemetry-sdk

# Async support
pip install aioredis
pip install asyncio

# Database
pip install sqlalchemy
pip install alembic
```

---

## Step 2: Set Up Redis (Caching)

### Option A: Docker (Easiest)
```bash
docker run -d -p 6379:6379 redis:alpine
docker ps  # Verify running
```

### Option B: Local Installation
```bash
# macOS
brew install redis
brew services start redis

# Linux
sudo apt-get install redis-server
sudo systemctl start redis-server

# Windows
# Download from https://github.com/microsoftarchive/redis/releases
```

### Test Connection
```python
import redis

redis_client = redis.Redis(host='localhost', port=6379)
redis_client.ping()  # Should print: True
```

---

## Step 3: Set Up Vector Database (RAG)

### Option A: Pinecone (Cloud, Easiest)
```bash
# Sign up at https://www.pinecone.io/
# Get API key from dashboard

export PINECONE_API_KEY="your-key-here"
```

```python
import pinecone

pinecone.init(api_key="your-key", environment="us-west1-gcp")
pinecone.create_index("documents", dimension=384)
```

### Option B: Weaviate (Local + Docker)
```bash
docker run -d -p 8080:8080 semitechnologies/weaviate:latest
```

```python
import weaviate

client = weaviate.Client("http://localhost:8080")
```

### Option C: Chroma (Lightweight, Local)
```bash
pip install chromadb
```

```python
import chromadb

client = chromadb.Client()
collection = client.create_collection("documents")
```

---

## Step 4: Download Pre-Trained Embeddings

```python
from sentence_transformers import SentenceTransformer

# First run downloads model (500MB)
# Subsequent runs use cached version
model = SentenceTransformer('all-MiniLM-L6-v2')

# Verify it works
embedding = model.encode("Hello world")
print(f"Embedding shape: {embedding.shape}")  # Should be (384,)
```

---

## Step 5: Set Up Monitoring

### Option A: Prometheus (Docker)
```bash
docker run -d -p 9090:9090 prom/prometheus
```

### Option B: Simple File-Based
```python
import json
from datetime import datetime

class SimpleMetricsLogger:
    def __init__(self, filepath="metrics.jsonl"):
        self.filepath = filepath
    
    def log(self, metric):
        metric["timestamp"] = datetime.now().isoformat()
        with open(self.filepath, "a") as f:
            f.write(json.dumps(metric) + "\n")
```

---

## Step 6: Database Migration (Advanced Context Versioning)

```bash
# Create migration
alembic init migrations

# Create migration for context versions
alembic revision --autogenerate -m "Add context_versions table"

# Apply migration
alembic upgrade head
```

---

## Step 7: Configuration File

Create `advanced_config.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_TTL = int(os.getenv("REDIS_TTL", "3600"))  # 1 hour

# Vector Database
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV", "us-west1-gcp")
VECTOR_DB_INDEX = os.getenv("VECTOR_DB_INDEX", "documents")

# Embeddings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384

# Context Limits
MAX_CONTEXT_TOKENS = int(os.getenv("MAX_CONTEXT_TOKENS", "4000"))
MAX_RECENT_TURNS = int(os.getenv("MAX_RECENT_TURNS", "10"))

# RAG
RAG_TOP_K = int(os.getenv("RAG_TOP_K", "5"))
RAG_SIMILARITY_THRESHOLD = float(os.getenv("RAG_SIMILARITY_THRESHOLD", "0.7"))

# Monitoring
ENABLE_MONITORING = os.getenv("ENABLE_MONITORING", "true").lower() == "true"
METRICS_LOG_FILE = os.getenv("METRICS_LOG_FILE", "metrics.jsonl")

# API
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = "claude-3-5-sonnet-20241022"
```

---

## Step 8: Create .env File

```bash
# .env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_TTL=3600

PINECONE_API_KEY=your-key-here
PINECONE_ENV=us-west1-gcp

MAX_CONTEXT_TOKENS=4000
MAX_RECENT_TURNS=10
RAG_TOP_K=5

ENABLE_MONITORING=true
METRICS_LOG_FILE=metrics.jsonl

ANTHROPIC_API_KEY=sk-ant-...
```

---

## Step 9: Verify All Components

```python
#!/usr/bin/env python3
"""verify_advanced_setup.py"""

import sys

def verify_redis():
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379)
        r.ping()
        print("✅ Redis: OK")
        return True
    except Exception as e:
        print(f"❌ Redis: {e}")
        return False

def verify_embeddings():
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embedding = model.encode("test")
        print(f"✅ Embeddings: OK (dim={len(embedding)})")
        return True
    except Exception as e:
        print(f"❌ Embeddings: {e}")
        return False

def verify_vector_db():
    try:
        import pinecone
        # Just test import, not actual connection
        print("✅ Pinecone: Available")
        return True
    except Exception as e:
        print(f"❌ Pinecone: {e}")
        return False

def verify_anthropic():
    try:
        from anthropic import Anthropic
        client = Anthropic()
        # Quick call
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=10,
            messages=[{"role": "user", "content": "hi"}]
        )
        print("✅ Anthropic: OK")
        return True
    except Exception as e:
        print(f"❌ Anthropic: {e}")
        return False

if __name__ == "__main__":
    checks = [
        verify_redis(),
        verify_embeddings(),
        verify_vector_db(),
        verify_anthropic()
    ]
    
    if all(checks):
        print("\n✅ All systems ready!")
        sys.exit(0)
    else:
        print("\n❌ Some components missing. See above.")
        sys.exit(1)
```

Run verification:
```bash
python verify_advanced_setup.py
```

---

## Step 10: Sample Data for RAG

Create `sample_documents.py`:

```python
documents = [
    {
        "id": "policy-001",
        "content": "Loan policies: Maximum DTI ratio 43%, minimum credit score 600, "
                   "minimum annual income $30,000, employment history 2+ years required.",
        "metadata": {"type": "policy", "version": "2024-Q1"}
    },
    {
        "id": "faq-001",
        "content": "Can I get approved with bad credit? We require minimum 600 credit score. "
                   "If your score is lower, consider credit repair first.",
        "metadata": {"type": "faq", "category": "credit"}
    },
    {
        "id": "product-001",
        "content": "Personal loans from $5,000 to $50,000. Interest rates from 5.99% to 15.99% "
                   "depending on credit profile. Flexible terms 24-84 months.",
        "metadata": {"type": "product", "category": "personal-loan"}
    },
]

def load_sample_documents_to_vector_db():
    from sentence_transformers import SentenceTransformer
    import pinecone
    
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Get vectors
    vectors = []
    for doc in documents:
        embedding = embedder.encode(doc["content"])
        vectors.append((
            doc["id"],
            embedding,
            {"text": doc["content"], **doc["metadata"]}
        ))
    
    # Upload to Pinecone
    index = pinecone.Index("documents")
    index.upsert(vectors=vectors)
    
    print(f"Loaded {len(vectors)} documents to vector DB")
```

---

## Step 11: Create Project Structure

```
advanced-context/
├── .env
├── advanced_config.py
├── verify_setup.py
├── sample_documents.py
├── src/
│   ├── __init__.py
│   ├── rag.py
│   ├── windowing.py
│   ├── caching.py
│   ├── adaptive.py
│   ├── monitoring.py
│   └── versioning.py
├── exercises/
│   ├── 01_rag_basic.py
│   ├── 02_windowing.py
│   ├── 03_adaptive.py
│   └── ...
└── tests/
    └── test_patterns.py
```

---

## Troubleshooting

### Redis Connection Error
```bash
# Check if running
redis-cli ping  # Should print: PONG

# If not, start it
redis-server
```

### Embedding Model Download Slow
```python
# Set cache directory
import os
os.environ['SENTENCE_TRANSFORMERS_HOME'] = '/path/to/cache'

# Models download to ~/.cache/huggingface by default
```

### Pinecone Connection
```python
# Test connection
import pinecone
try:
    pinecone.init(api_key="your-key", environment="us-west1-gcp")
    print(pinecone.list_indexes())
except Exception as e:
    print(f"Error: {e}")
    # Check API key and environment
```

### Memory Issues
```bash
# If embeddings crash (out of memory)
# Use smaller model
model = SentenceTransformer('all-MiniLM-L6-v2')  # Smaller
# vs
model = SentenceTransformer('all-mpnet-base-v2')  # Larger
```

---

## Ready!

✅ Redis running
✅ Embeddings model downloaded
✅ Vector DB configured
✅ Monitoring set up
✅ API keys configured
✅ Sample data loaded

**Start with Exercise 1!** 🚀

