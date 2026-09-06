# Advanced Context Patterns: Exercises

Complete all 8 exercises to master production patterns.

---

## Exercise 1: RAG Implementation (Medium, 45 min)

### Task
Build a RAG system that retrieves product information for customer queries.

**Data:** 10 product documents (included in setup)
**Query:** "Can I get a loan with 580 credit score?"
**Expected:** Retrieved policy doc + FAQ doc + ranked by relevance

### Starter Code
```python
from sentence_transformers import SentenceTransformer
import pinecone

# TODO: Initialize embedder and Pinecone index
# TODO: Encode and store sample documents
# TODO: Query with customer question
# TODO: Rank results by similarity
# TODO: Inject top 3 into context
# TODO: Send to Claude
# TODO: Compare accuracy with/without RAG
```

### Solution Approach
1. Embed sample documents
2. Store in Pinecone
3. Embed user query
4. Retrieve top-5 similar
5. Build context from results
6. Send to Claude
7. Measure relevance

### Bonus
- Calculate token savings (before/after)
- Try different embedding models
- Measure latency

---

## Exercise 2: Context Windowing (Medium, 35 min)

### Task
Implement sliding window for long conversations (50+ turns).

**Scenario:** Customer support chatbot with conversation history
**Requirement:** Keep recent 10 turns in full, summarize older
**Test:** 50-turn conversation

### Starter Code
```python
class ContextWindow:
    def __init__(self, max_recent_turns: int = 10):
        self.max_recent_turns = max_recent_turns
        self.conversation = []
        self.summary = ""
    
    # TODO: Implement add_turn()
    # TODO: Implement get_context()
    # TODO: Implement _summarize_turns()
    # TODO: Test with 50-turn conversation
    # TODO: Measure token savings
```

### Solution Approach
1. Add turns to conversation
2. Track total turns
3. When exceeding threshold, summarize old
4. Keep only recent
5. Return combined (summary + recent)

### Bonus
- Compare fixed vs dynamic window size
- Try different summarization strategies
- Measure quality loss

---

## Exercise 3: Adaptive Context Selection (Hard, 40 min)

### Task
Build context selector that picks only relevant items.

**Context items:**
- Customer name
- Credit score
- Income
- Loan history
- Marketing preferences
- Birthday
- Phone number

**Constraint:** 2000 token limit
**Queries:** Mix of loan questions and general questions

### Starter Code
```python
class AdaptiveContextSelector:
    def __init__(self, max_tokens: int = 2000):
        self.max_tokens = max_tokens
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
    
    def select_context(self, query: str, all_context: dict) -> dict:
        # TODO: Score relevance of each item
        # TODO: Apply domain-specific weights
        # TODO: Select until token limit
        # TODO: Return selected context
        
        # TODO: Test with loan queries
        # TODO: Test with non-loan queries
        # TODO: Measure inclusion rates
```

### Bonus
- A/B test different relevance algorithms
- Measure impact on answer quality
- Cost analysis

---

## Exercise 4: Context Caching (Medium, 30 min)

### Task
Implement Redis caching for expensive operations.

**Cache:**
- Document embeddings
- Context summaries
- Customer lookups

**Test:** 100 queries, same customer, measure speed difference

### Starter Code
```python
import redis
import json

class ContextCache:
    def __init__(self, ttl_seconds: int = 3600):
        self.redis = redis.Redis(host='localhost', port=6379)
        self.ttl = ttl_seconds
    
    # TODO: Implement get_cached()
    # TODO: Implement set_cached()
    # TODO: Implement get_or_compute()
    # TODO: Test with 100 repeated queries
    # TODO: Measure speedup (first vs cached)
```

### Bonus
- Measure cache hit rate
- Implement cache invalidation strategy
- Cost analysis (Redis vs API calls)

---

## Exercise 5: Multi-Tier Context (Easy, 25 min)

### Task
Implement tier-based context inclusion.

**Tiers:**
- Required: Policies, customer name
- Important: Credit score, income
- Optional: Preferences, history

**Test:** Build context at different token limits

### Starter Code
```python
class MultiTierContext:
    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens
        self.tiers = {
            "required": [],
            "important": [],
            "optional": []
        }
    
    # TODO: Add items to tiers
    # TODO: Implement build_context()
    # TODO: Test at different token limits
    # TODO: Verify all required items included
```

### Bonus
- Experiment with tier thresholds
- Measure impact on decision quality
- Compare to flat prioritization

---

## Exercise 6: Automated Summarization (Medium, 35 min)

### Task
Pre-compute summaries for documents on upload.

**Documents:** 5 long documents (2000+ words each)
**Requirement:** Summarize to <10% of original size
**Verify:** Summary captures key points

### Starter Code
```python
class DocumentSummarizer:
    def __init__(self):
        self.summaries = {}
    
    def summarize_on_upload(self, doc_id: str, text: str) -> dict:
        # TODO: Chunk if >20K tokens
        # TODO: Summarize each chunk
        # TODO: Combine summaries
        # TODO: Store result
        # TODO: Return compression stats
    
    # TODO: Test with 5 documents
    # TODO: Measure compression ratio
    # TODO: Verify quality
```

### Bonus
- Compare chunk sizes
- Different summarization lengths
- Measure latency (pre-compute vs on-demand)

---

## Exercise 7: Real-Time Context (Hard, 45 min)

### Task
Stream context updates during long request.

**Simulate:** Market rate changes + customer status updates
**Requirement:** Agent aware of updates
**Test:** Multi-turn conversation with mid-stream updates

### Starter Code
```python
import asyncio

async def stream_realtime_context():
    # TODO: Simulate market data stream
    # TODO: Simulate customer status updates
    # TODO: Yield updates as they arrive
    # TODO: Track which updates affected decision

async def evaluate_with_updates(customer_id, loan_amount):
    # TODO: Get initial context
    # TODO: Listen for updates
    # TODO: Re-evaluate if critical update
    # TODO: Return decision + audit trail
```

### Bonus
- Measure update frequency impact
- Test decision stability
- Compare sync vs async

---

## Exercise 8: Context Versioning (Hard, 50 min)

### Task
Implement context versioning with audit trail.

**Requirement:** Track all context changes with reason
**Use Case:** Loan decision needs audit trail
**Verify:** Can retrieve any historical version

### Starter Code
```python
class VersionedContext:
    def __init__(self, context_id: str):
        self.context_id = context_id
        self.versions = []
        self.current_version = 0
    
    # TODO: Implement set_context()
    # TODO: Implement get_version()
    # TODO: Implement get_audit_trail()
    # TODO: Store in database
    
    # TODO: Test with 5 updates
    # TODO: Verify audit trail
    # TODO: Test retrieval of specific version
```

### Test Scenario
```
V1: Initial application (credit 750, income $150k)
V2: Credit check (credit 745)
V3: Employment verification (confirmed 5 years)
V4: Income verification (confirmed $150k)
V5: Final decision (APPROVED)

Should be able to trace decision back to each version.
```

---

## Bonus Challenge: Production Integration

Combine multiple patterns into one system:

```
Customer Query
    ↓
├─ RAG: Find relevant policies
├─ Cache: Get customer data (cached)
├─ Adaptive: Select context based on query type
├─ Windowing: Include recent conversation
├─ Multi-tier: Prioritize critical context
├─ Real-time: Check market rates
└─ Versioning: Track decision
    ↓
Claude + Context
    ↓
Decision + Audit Trail
```

Implement and measure:
- Total latency
- Token usage
- Cost
- Decision quality
- Audit trail completeness

---

## Submission Checklist

- [ ] Exercise 1: RAG working, token savings calculated
- [ ] Exercise 2: Windowing handles 50+ turns
- [ ] Exercise 3: Adaptive selection respects limits
- [ ] Exercise 4: Caching 50x+ faster for cached queries
- [ ] Exercise 5: Multi-tier includes all required items
- [ ] Exercise 6: Summarization <10% of original
- [ ] Exercise 7: Real-time updates tracked
- [ ] Exercise 8: Full audit trail for versions
- [ ] Bonus: Integrated system working
- [ ] All code runs without errors
- [ ] Measurements/results documented

---

## Performance Benchmarks

Aim for:

| Pattern | Metric | Target |
|---------|--------|--------|
| RAG | Retrieval latency | <100ms |
| RAG | Compression | 10:1 (10K tokens → 1K) |
| Windowing | Handles | 1000+ turns |
| Adaptive | Token savings | 30%+ |
| Caching | Speedup | 50x+ |
| Summarization | Compression | 10:1+ |
| Real-time | Update latency | <1s |
| Versioning | Query latency | <10ms |

---

## Next Steps

After exercises:
1. Combine patterns into production system
2. Implement monitoring dashboard
3. Load test (1000+ concurrent)
4. Cost analysis report
5. Production deployment

