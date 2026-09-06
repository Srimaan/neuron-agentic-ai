# Advanced Context Patterns

Master production-grade context strategies for handling real-world systems.

---

## Pattern 1: RAG (Retrieval Augmented Generation)

### The Problem
Large Language Models have fixed knowledge cutoff. Your application needs:
- Current product information
- Legal documents updated monthly
- Customer-specific data
- Domain-specific knowledge base

You can't fit everything in context. Need to retrieve what's relevant.

### The Solution

**RAG = Retrieval + Augmentation + Generation**

```
Query
  ↓
[1] Retrieve: Semantic search for relevant documents
  ↓
[2] Augment: Inject retrieved documents into context
  ↓
[3] Generate: Claude generates response with augmented context
```

### Implementation Pattern

```python
# Step 1: Build document index (one-time, on upload)
from sentence_transformers import SentenceTransformer
import pinecone

embedder = SentenceTransformer('all-MiniLM-L6-v2')
pinecone.init(api_key="...", environment="us-west1-gcp")
index = pinecone.Index("documents")

# When document uploaded:
def index_document(doc_id: str, text: str):
    embedding = embedder.encode(text)
    index.upsert([(doc_id, embedding, {"text": text})])

# Step 2: At query time, retrieve relevant
def rag_query(query: str, top_k: int = 5) -> str:
    query_embedding = embedder.encode(query)
    results = index.query(query_embedding, top_k=top_k)
    
    # Get actual documents
    retrieved_docs = [match.metadata["text"] for match in results.matches]
    
    # Build context
    context = "Relevant documents:\n"
    for doc in retrieved_docs:
        context += f"- {doc}\n"
    
    # Step 3: Augment prompt
    prompt = f"""
    {context}
    
    User question: {query}
    
    Answer based on the documents above.
    """
    
    # Generate response
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text

# Usage
answer = rag_query("What are the current warranty terms?")
```

### Token Cost Analysis

**Without RAG:**
- Full document: 10,000 tokens
- Query: 100 tokens
- Total: ~10,100 tokens per request
- Cost: $0.03 per request

**With RAG:**
- Retrieve top 5 documents: ~500 tokens
- Query: 100 tokens
- Total: ~600 tokens per request
- Cost: $0.002 per request
- **Savings: 15x cheaper!**

### When to Use
✅ Knowledge bases (>100 documents)
✅ Product information systems
✅ Legal document review
✅ FAQ systems
✅ Multi-tenant applications

### Framework Support

| Framework | RAG Support | Notes |
|-----------|---|---|
| Raw SDK | Manual | Most control |
| LangChain | LangChain-RAG | Built-in chains |
| LangGraph | Via nodes | Explicit flow |
| Haystack | Native | RAG-first design |
| AutoGen | Via tools | Plugin pattern |

---

## Pattern 2: Context Windowing

### The Problem

Conversation grows unbounded:
- Turn 1: 100 tokens
- Turn 10: 1,000 tokens
- Turn 50: 5,000 tokens
- Turn 100: 10,000 tokens (getting expensive)
- Turn 200: 20,000 tokens (approaching limits)

Can't keep full conversation forever.

### The Solution

**Keep recent, summarize old**

```python
class ContextWindow:
    def __init__(self, max_recent_turns: int = 10):
        self.max_recent_turns = max_recent_turns
        self.conversation = []
        self.summary = ""
    
    def add_turn(self, user_msg: str, assistant_msg: str):
        """Add turn and manage windowing"""
        self.conversation.append({
            "user": user_msg,
            "assistant": assistant_msg
        })
        
        # If too long, summarize old turns
        if len(self.conversation) > self.max_recent_turns:
            # Get old turns
            old_turns = self.conversation[:len(self.conversation) - self.max_recent_turns]
            
            # Summarize
            self.summary = self._summarize_turns(old_turns)
            
            # Keep only recent
            self.conversation = self.conversation[-self.max_recent_turns:]
    
    def get_context(self) -> str:
        """Get full context with summary + recent"""
        context = ""
        
        if self.summary:
            context += f"Earlier conversation summary:\n{self.summary}\n\n"
        
        context += "Recent conversation:\n"
        for turn in self.conversation:
            context += f"User: {turn['user']}\n"
            context += f"Assistant: {turn['assistant']}\n\n"
        
        return context
    
    def _summarize_turns(self, turns: list) -> str:
        """Summarize old turns"""
        text = "\n".join([f"User: {t['user']}\nAssistant: {t['assistant']}" for t in turns])
        
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=[{
                "role": "user",
                "content": f"Summarize this conversation in 100 words:\n{text}"
            }]
        )
        
        return response.content[0].text
```

### Token Efficiency

**Without windowing:**
- 100 turns @ 100 tokens each = 10,000 tokens
- Cost: $0.03 per request

**With windowing (keep 10 recent, summarize 90):**
- Summary: 500 tokens
- Recent 10: 1,000 tokens
- Total: 1,500 tokens
- Cost: $0.004 per request
- **Savings: 6.7x cheaper!**

### When to Use
✅ Long conversations (100+ turns)
✅ Customer support sessions
✅ Research assistants
✅ Any multi-turn application

---

## Pattern 3: Adaptive Context Selection

### The Problem

Not all context is equally important:

```
Context items:
- User name (critical)
- Phone number (nice to have)
- Marketing preferences (optional)
- Birthday (rarely needed)
- Entire purchase history (too much)
- Recent purchases (important)
```

You want to include important stuff, exclude fluff.

### The Solution

**Score relevance, select top-K**

```python
from sentence_transformers import util
import numpy as np

class AdaptiveContextSelector:
    def __init__(self, max_context_tokens: int = 4000):
        self.max_context_tokens = max_context_tokens
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
    
    def select_context(self, query: str, all_context: dict) -> dict:
        """Select most relevant context for query"""
        
        # Embed query
        query_embedding = self.embedder.encode(query)
        
        # Score each context item
        scores = {}
        for key, value in all_context.items():
            # Embed context item
            item_embedding = self.embedder.encode(str(value))
            
            # Similarity score
            similarity = util.pytorch_cos_sim(query_embedding, item_embedding)
            scores[key] = float(similarity)
        
        # Manual relevance boost (domain-specific)
        if "credit_score" in all_context:
            scores["credit_score"] *= 2.0  # Very important for loan
        if "income" in all_context:
            scores["income"] *= 2.0
        if "birthday" in all_context:
            scores["birthday"] *= 0.5  # Less important
        
        # Sort by relevance
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Select until we hit token limit
        selected = {}
        token_count = 0
        
        for key, _ in ranked:
            value_str = str(all_context[key])
            tokens_needed = len(value_str) // 4  # Rough estimate
            
            if token_count + tokens_needed <= self.max_context_tokens:
                selected[key] = all_context[key]
                token_count += tokens_needed
            else:
                break  # Hit token limit
        
        return selected
```

### When to Use
✅ Mixed-importance context
✅ Cost-sensitive applications
✅ Token-limited scenarios
✅ Production optimization

---

## Pattern 4: Context Caching

### The Problem

Same context requested repeatedly:
- Same customer asked 10 questions
- Same document reviewed 5 times
- Same market data for 100 queries

Computing embeddings/summaries every time = wasteful.

### The Solution

**Cache computed context**

```python
import redis
import json
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379)

class ContextCache:
    def __init__(self, ttl_seconds: int = 3600):
        self.ttl = ttl_seconds
    
    def get_cached_context(self, context_id: str) -> str:
        """Get context from cache"""
        cached = redis_client.get(f"context:{context_id}")
        return json.loads(cached) if cached else None
    
    def cache_context(self, context_id: str, context: str):
        """Store context in cache"""
        redis_client.setex(
            f"context:{context_id}",
            self.ttl,
            json.dumps(context)
        )
    
    def get_or_compute(self, context_id: str, compute_fn):
        """Get cached or compute new"""
        # Try cache
        cached = self.get_cached_context(context_id)
        if cached:
            return cached
        
        # Compute
        context = compute_fn()
        
        # Cache
        self.cache_context(context_id, context)
        
        return context

# Usage
cache = ContextCache(ttl_seconds=3600)

def get_customer_context(customer_id: int):
    return cache.get_or_compute(
        f"customer:{customer_id}",
        lambda: fetch_customer_from_db(customer_id)  # Expensive
    )
```

### Performance Improvement

**First request:** 500ms (database query + network)
**Cached requests:** 5ms (Redis lookup)
**Speedup:** 100x faster!

### When to Use
✅ Frequently requested context
✅ Expensive computations (embeddings)
✅ Multi-user systems
✅ High-traffic applications

---

## Pattern 5: Multi-Tier Context

### The Problem

Context has conflicting requirements:
- Policies are always needed
- Customer data is critical
- Preferences are nice-to-have
- Marketing info is optional

Can't treat all the same when approaching token limits.

### The Solution

**Tiered inclusion strategy**

```python
class MultiTierContext:
    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens
        
        # Define tiers (ordered by importance)
        self.tiers = {
            "required": [],      # Always include
            "important": [],     # Include if space
            "optional": []       # Include if space left
        }
    
    def build_context(self) -> str:
        """Build context respecting tiers"""
        context = ""
        token_count = 0
        
        # Tier 1: Required (always include)
        for item in self.tiers["required"]:
            context += item + "\n"
            token_count += len(item) // 4
        
        # Tier 2: Important (if space)
        for item in self.tiers["important"]:
            tokens_needed = len(item) // 4
            if token_count + tokens_needed <= self.max_tokens * 0.8:  # 80%
                context += item + "\n"
                token_count += tokens_needed
        
        # Tier 3: Optional (if space left)
        for item in self.tiers["optional"]:
            tokens_needed = len(item) // 4
            if token_count + tokens_needed <= self.max_tokens:
                context += item + "\n"
                token_count += tokens_needed
        
        return context

# Usage
ctx = MultiTierContext(max_tokens=4000)

# Required
ctx.tiers["required"] = [
    "Loan policies: Max DTI 43%, Min credit 600",
    f"Customer: {customer.name}, Credit: {customer.credit_score}"
]

# Important
ctx.tiers["important"] = [
    "Recent transactions (last 6 months)",
    "Previous loan decisions"
]

# Optional
ctx.tiers["optional"] = [
    "Marketing preferences",
    "Communication history",
    "Demographic info"
]

context = ctx.build_context()
```

### When to Use
✅ Mixed-criticality context
✅ Dynamic feature inclusion
✅ Graceful degradation
✅ Multi-tenant systems

---

## Pattern 6: Automated Summarization

### The Problem

Large documents take space. Summarizing manually is slow.

### The Solution

**Pre-compute and cache summaries**

```python
class DocumentSummarizer:
    def __init__(self):
        self.summary_cache = {}
    
    def summarize_on_upload(self, doc_id: str, text: str) -> dict:
        """Summarize document when uploaded"""
        
        # For very long docs, chunk first
        if len(text) > 20000:
            chunks = self.chunk_text(text, chunk_size=5000)
            chunk_summaries = [
                self._summarize_chunk(chunk) for chunk in chunks
            ]
            full_summary = "\n".join(chunk_summaries)
        else:
            full_summary = self._summarize_chunk(text)
        
        # Store
        self.summary_cache[doc_id] = {
            "full": text,
            "summary": full_summary,
            "chunks": len(text) // 5000
        }
        
        return {
            "original_tokens": len(text) // 4,
            "summary_tokens": len(full_summary) // 4,
            "compression": (1 - len(full_summary) / len(text)) * 100
        }
    
    def _summarize_chunk(self, text: str) -> str:
        """Summarize a chunk"""
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            messages=[{
                "role": "user",
                "content": f"Summarize in 100 words:\n{text}"
            }]
        )
        return response.content[0].text
    
    def chunk_text(self, text: str, chunk_size: int = 5000) -> list:
        """Split text into chunks with overlap"""
        chunks = []
        overlap = 200
        for i in range(0, len(text), chunk_size - overlap):
            chunks.append(text[i:i + chunk_size])
        return chunks

# Usage
summarizer = DocumentSummarizer()
stats = summarizer.summarize_on_upload("doc123", long_document_text)
print(f"Compressed by {stats['compression']:.0f}%")
```

### Compression Results

- **50-page document:** 20,000 tokens → 300 tokens (98% compression!)
- **One-time cost:** 15 seconds to summarize
- **Repeated benefit:** Every query uses compact summary

### When to Use
✅ Document-heavy systems
✅ Content platforms
✅ Legal/financial applications
✅ Batch processing systems

---

## Pattern 7: Real-Time Context

### The Problem

Context changes during conversation:
- Customer status update
- Market data changed
- File was modified
- New information arrived

Stale context = wrong decisions.

### The Solution

**Stream context updates**

```python
import asyncio
from typing import AsyncGenerator

class RealtimeContextStream:
    async def stream_context_updates(
        self, 
        query: str,
        context_sources: list
    ) -> AsyncGenerator:
        """Stream updates to context during processing"""
        
        # Initial context
        yield {
            "type": "initial",
            "context": self._get_current_context(context_sources)
        }
        
        # Stream updates as they arrive
        async for update in self._listen_for_updates(context_sources):
            yield {
                "type": "update",
                "changed_field": update["field"],
                "new_value": update["value"],
                "timestamp": update["timestamp"]
            }
    
    async def _listen_for_updates(self, sources):
        """Listen for real-time updates (websockets, etc)"""
        # Example: market data stream
        async for tick in market_data_stream():
            yield {
                "field": "market_rate",
                "value": tick["rate"],
                "timestamp": tick["time"]
            }
        
        # Example: customer status
        async for status in customer_status_stream():
            yield {
                "field": "customer_status",
                "value": status["new_status"],
                "timestamp": status["time"]
            }

# Usage
async def evaluate_with_realtime_context(customer_id, loan_amount):
    sources = [
        "market_data_stream",
        f"customer:{customer_id}",
        "policy_updates"
    ]
    
    context_stream = RealtimeContextStream()
    
    async for context_update in context_stream.stream_context_updates(
        f"Evaluate {loan_amount} for customer {customer_id}",
        sources
    ):
        if context_update["type"] == "initial":
            # Send initial request with first context
            pass
        elif context_update["type"] == "update":
            # Significant update - might want to re-evaluate
            if context_update["changed_field"] in ["market_rate", "customer_status"]:
                # Re-run evaluation with new context
                pass
```

### When to Use
✅ Financial systems (live rates)
✅ Logistics (real-time status)
✅ Live customer interactions
✅ Sensor data integration

---

## Pattern 8: Context Versioning

### The Problem

Context changes mid-stream:
- Need audit trail for compliance
- Want to trace decisions to context state
- Must support rollback if error found
- Regulatory requirements

### The Solution

**Version and track context**

```python
from datetime import datetime
import json

class VersionedContext:
    def __init__(self, context_id: str):
        self.context_id = context_id
        self.versions = []
        self.current_version = 0
    
    def set_context(self, data: dict, reason: str = ""):
        """Create new version"""
        version = {
            "version": self.current_version + 1,
            "timestamp": datetime.now().isoformat(),
            "data": data,
            "reason": reason,
            "hash": self._hash_data(data)
        }
        
        self.versions.append(version)
        self.current_version += 1
        
        # Store in database for audit trail
        db.store_context_version(self.context_id, version)
        
        return version["version"]
    
    def get_version(self, version_num: int) -> dict:
        """Get specific version"""
        for v in self.versions:
            if v["version"] == version_num:
                return v["data"]
        return None
    
    def get_audit_trail(self) -> list:
        """Full history for compliance"""
        return [
            {
                "version": v["version"],
                "timestamp": v["timestamp"],
                "reason": v["reason"],
                "hash": v["hash"]
            }
            for v in self.versions
        ]
    
    def _hash_data(self, data: dict) -> str:
        """Create fingerprint of context"""
        import hashlib
        json_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(json_str.encode()).hexdigest()[:16]

# Usage
context = VersionedContext("customer:12345")

# Initial context
context.set_context({
    "credit_score": 750,
    "income": 150000,
    "employment": "5 years"
}, reason="Initial application")

# Update from credit check
context.set_context({
    "credit_score": 745,  # Minor change
    "income": 150000,
    "employment": "5 years"
}, reason="Credit check returned")

# Audit trail for compliance
print(context.get_audit_trail())
# Output:
# [
#   {"version": 1, "timestamp": "...", "reason": "Initial application", "hash": "abc123..."},
#   {"version": 2, "timestamp": "...", "reason": "Credit check returned", "hash": "def456..."}
# ]
```

### When to Use
✅ Financial/legal systems
✅ Compliance requirements
✅ Audit trail needed
✅ Regulated industries

---

## Monitoring & Observability

### Track Context Metrics

```python
class ContextMonitor:
    def __init__(self):
        self.metrics = {
            "avg_context_size": 0,
            "cache_hit_rate": 0,
            "rag_relevance": 0,
            "cost_per_request": 0
        }
    
    def track_request(self, request_data):
        """Log metrics for each request"""
        metrics = {
            "timestamp": datetime.now(),
            "context_tokens": request_data["tokens"],
            "total_tokens": request_data["total"],
            "cache_hit": request_data["cached"],
            "cost": request_data["cost"],
            "rag_score": request_data.get("relevance", 0)
        }
        
        # Store for analysis
        self.log_to_database(metrics)
        
        # Update aggregates
        self._update_aggregates()
    
    def get_cost_report(self):
        """Weekly cost analysis"""
        return {
            "total_context_tokens": self._sum_metric("context_tokens"),
            "total_cost": self._sum_metric("cost"),
            "avg_context_size": self._avg_metric("context_tokens"),
            "cache_hit_rate": self._avg_metric("cache_hit"),
            "top_expensive_queries": self._get_top_queries()
        }
```

### Create Dashboards

Monitor:
- Average context size over time
- Cache hit rate
- RAG retrieval quality
- Cost per request
- Token usage distribution

---

## Production Checklist

Before deploying advanced patterns:

✅ Implement monitoring
✅ Set up alerts for cost spikes
✅ Test with production data volume
✅ Measure compression ratios
✅ Calculate ROI of each pattern
✅ Document versioning strategy
✅ Set cache TTLs appropriately
✅ Test fallback strategies
✅ Load test (1000+ concurrent)
✅ Security review (PII handling)

---

## Key Takeaways

1. **RAG**: Retrieve relevant knowledge, not everything
2. **Windowing**: Summarize old context, keep recent
3. **Adaptive**: Score relevance, select what matters
4. **Caching**: Reuse expensive computations
5. **Multi-Tier**: Include based on criticality
6. **Summarization**: Pre-compute compressed versions
7. **Real-Time**: Stream updates as they arrive
8. **Versioning**: Audit trail for compliance

**Combining patterns can reduce costs 50-90% while improving quality!**

