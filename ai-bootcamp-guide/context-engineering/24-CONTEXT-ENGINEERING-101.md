# Context Engineering 101

## What is Context?

**Context** is all the information Claude uses to make decisions.

Examples:
- User's message (explicit)
- Customer history (background)
- Loan policies (rules)
- Market data (market facts)
- Company documents (reference)
- Conversation history (memory)

**Context ≠ Memory**
- **Context:** Information in the current conversation
- **Memory:** Information persisted across conversations

---

## Claude's Context Window

### The 200K Token Limit

Claude 3.5 Sonnet: **200,000 tokens** per conversation

Think of it like a library:
- **Input tokens:** Everything Claude reads (context + user message)
- **Output tokens:** Everything Claude writes

### What Takes Tokens?

| Content | Tokens | Notes |
|---------|--------|-------|
| Short sentence | 20 | "Hello world" |
| Paragraph | 100 | ~300 words |
| Page of text | 400 | ~1000 words |
| Code file | 100-500 | Depends on length |
| Document | 1000+ | Average document |
| Full conversation | Variable | All messages |

### Token Counting

```python
import anthropic

client = anthropic.Anthropic()

# Count tokens before sending
message = "Your message here"
context = "Your context here"

response = client.messages.count_tokens(
    model="claude-3-5-sonnet-20241022",
    messages=[
        {
            "role": "user",
            "content": context + "\n\n" + message
        }
    ]
)

print(f"Input tokens: {response.input_tokens}")
print(f"Cache creation tokens: {response.cache_creation_input_tokens}")
```

---

## Context Strategies

### Strategy 1: Inline Context
Put context directly in the message:

```python
prompt = f"""
Here is the customer history:
{customer_history}

Here are the loan policies:
{loan_policies}

Question: {user_question}
"""
```

**Pros:** Simple, direct, transparent
**Cons:** Inefficient for large context, repeated in each call

### Strategy 2: System Message
Put persistent context in system:

```python
system_prompt = """
You are a loan officer. You have access to:
- Loan policies (see below)
- Customer data (per request)

Policies:
- DTI ratio max: 43%
- Min credit score: 600
- Income verification required
"""

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system=system_prompt,
    messages=[
        {"role": "user", "content": user_input}
    ]
)
```

**Pros:** Persistent, efficient, clear
**Cons:** Limited to ~2K tokens typically

### Strategy 3: Database Retrieval
Fetch context dynamically:

```python
def get_context(customer_id):
    # Query database
    customer = db.query("SELECT * FROM customers WHERE id=?", customer_id)
    history = db.query("SELECT * FROM loan_history WHERE customer_id=?", customer_id)
    
    context = f"""
    Customer: {customer.name}
    Credit Score: {customer.credit_score}
    History: {history.count()} previous loans
    """
    return context

# Use in prompt
context = get_context(customer_id)
prompt = f"{context}\n\nAnalyze loan application..."
```

**Pros:** Dynamic, scalable, efficient
**Cons:** Database latency, may need caching

### Strategy 4: Chunking for Long Documents
Split large documents into chunks:

```python
def chunk_text(text, chunk_size=2000, overlap=200):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i + chunk_size])
    return chunks

# Process chunks
for chunk in chunks:
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=512,
        messages=[
            {"role": "user", "content": f"Analyze: {chunk}"}
        ]
    )
    results.append(response.content[0].text)
```

**Pros:** Handles large documents, manageable chunks
**Cons:** May lose context between chunks

---

## Token Optimization

### ⚠️ Problem: Context Bloat
Large context = High cost + Slow response

```
Context Size | Input Tokens | Cost (Sonnet) | Speed |
1 KB         | 250          | $0.00075      | Fast
10 KB        | 2,500        | $0.0075       | Medium
100 KB       | 25,000       | $0.075        | Slow
200 KB       | 50,000       | $0.15         | Very Slow
```

### ✅ Solution: Context Compression

**Technique 1: Summarization**
```python
# Instead of full document
context = full_document  # 50,000 tokens

# Use summary
context = f"""
Document: {document.title}
Summary: {llm_summarize(full_document)}  # 500 tokens
Key Points: {extract_key_points(full_document)}  # 200 tokens
"""
```

**Technique 2: Filtering**
```python
# Only include relevant info
relevant_context = []
for item in all_context:
    if item.relevance_score > 0.7:  # Only high relevance
        relevant_context.append(item)
```

**Technique 3: Chunking**
```python
# Process large context in chunks
for chunk in chunks:
    # Process each chunk separately
    # Keep only important results
```

**Technique 4: Prompt Compression**
```python
# Use concise language
# Remove fluff
# Focus on essentials

# BAD: "Please kindly provide an analysis of..."
# GOOD: "Analyze:"
```

---

## Database Integration

### Pattern 1: Query-Time Retrieval

```python
def evaluate_loan(customer_id, loan_amount):
    # Get context from database
    customer = db.get_customer(customer_id)
    credit_history = db.get_credit_history(customer_id)
    similar_loans = db.get_similar_loans(loan_amount)
    
    # Build context
    context = f"""
    Customer: {customer.name}
    Credit Score: {customer.credit_score}
    Income: ${customer.income}
    
    Credit History:
    {format_history(credit_history)}
    
    Similar Loans (benchmarks):
    {format_loans(similar_loans)}
    """
    
    # Use in LLM
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": context + "\nEvaluate this loan..."}
        ]
    )
    return response
```

### Pattern 2: Cached Retrieval

```python
import redis

cache = redis.Redis()

def get_context_cached(customer_id):
    # Check cache
    cached = cache.get(f"context:{customer_id}")
    if cached:
        return cached
    
    # Fetch from database
    context = fetch_from_database(customer_id)
    
    # Cache for 1 hour
    cache.setex(f"context:{customer_id}", 3600, context)
    
    return context
```

### Pattern 3: Embedding-Based Retrieval

```python
import numpy as np

def retrieve_relevant_context(query, all_docs):
    # Embed query
    query_embedding = embed(query)
    
    # Find similar documents
    similarities = []
    for doc in all_docs:
        doc_embedding = embed(doc)
        sim = cosine_similarity(query_embedding, doc_embedding)
        similarities.append((doc, sim))
    
    # Return top-k relevant
    relevant = sorted(similarities, key=lambda x: x[1], reverse=True)[:5]
    context = "\n".join([doc for doc, _ in relevant])
    
    return context
```

---

## Long Context Applications

### Use Case 1: Document Analysis
Analyze 50K+ token document:

```python
def analyze_long_document(doc_text):
    # Split into chunks
    chunks = chunk_text(doc_text, chunk_size=10000)
    
    # Analyze each chunk
    chunk_summaries = []
    for i, chunk in enumerate(chunks):
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=[{
                "role": "user",
                "content": f"Summarize this section:\n{chunk}"
            }]
        )
        chunk_summaries.append(response.content[0].text)
    
    # Combine summaries
    full_summary = "\n".join(chunk_summaries)
    
    # Final analysis
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"Here are summaries of all sections:\n{full_summary}\n\nProvide final analysis..."
        }]
    )
    return response
```

### Use Case 2: Conversation with Context
Long conversation with growing context:

```python
def multi_turn_conversation(user_id, messages):
    # Get conversation history from database
    history = db.get_conversation_history(user_id, limit=10)
    
    # Build context from history
    context = "Previous conversation:\n"
    for msg in history:
        context += f"User: {msg.user_message}\n"
        context += f"Assistant: {msg.assistant_response}\n"
    
    # Add new message
    context += f"User: {messages[-1]}\n"
    
    # Check token count
    tokens = count_tokens(context)
    if tokens > 150000:  # Getting close to limit
        # Compress old history
        old_history = history[:5]
        new_history = history[5:]
        
        # Summarize old
        summary = summarize(old_history)
        
        # Rebuild with summary
        context = f"Summary of earlier conversation:\n{summary}\n"
        context += "Recent conversation:\n"
        for msg in new_history:
            context += f"User: {msg.user_message}\n"
            context += f"Assistant: {msg.assistant_response}\n"
        context += f"User: {messages[-1]}\n"
    
    # Get response
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": context}]
    )
    return response
```

---

## Context Best Practices

✅ **DO:**
- Count tokens before sending
- Summarize large documents
- Cache frequently accessed context
- Prioritize important information
- Use database retrieval for dynamic data
- Monitor context growth
- Compress old conversation history

❌ **DON'T:**
- Send same large context repeatedly
- Include irrelevant information
- Forget to count tokens
- Hardcode large context strings
- Ignore database performance
- Keep unlimited conversation history
- Mix context with prompt instruction

---

## Key Takeaways

1. **Context ≠ Memory** — Context is current conversation, memory is persistent
2. **200K tokens** — Claude's context limit per conversation
3. **Token counting** — Critical for cost and performance
4. **Retrieval** — Pull context dynamically from databases
5. **Compression** — Summarize to save tokens
6. **Monitoring** — Track token usage to avoid surprises
7. **Optimization** — Trade-off between context size and quality

---

## Next: Implementation

See frameworks 27-36 for how different frameworks handle context.

