"""
Framework 42: Raw SDK - Advanced Pattern Implementations
Shows: RAG, Caching, Windowing with explicit control
Best for: Learning, custom implementations, maximum control
"""

import anthropic
import redis
from sentence_transformers import SentenceTransformer
import sqlite3
from datetime import datetime

client = anthropic.Anthropic()
redis_client = redis.Redis(host='localhost', port=6379)
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# ============================================================================
# Pattern 1: RAG with Raw SDK
# ============================================================================

class RAGSystem:
    """Retrieval Augmented Generation"""
    
    def __init__(self, documents: list):
        """Initialize with documents"""
        self.documents = documents
        self.embeddings = self._embed_documents()
    
    def _embed_documents(self):
        """Embed all documents for similarity search"""
        embeddings = {}
        for doc in self.documents:
            embedding = embedder.encode(doc['text'])
            embeddings[doc['id']] = embedding
        return embeddings
    
    def retrieve(self, query: str, top_k: int = 3) -> list:
        """Retrieve most relevant documents"""
        query_embedding = embedder.encode(query)
        
        # Score all documents
        scores = {}
        for doc_id, doc_embedding in self.embeddings.items():
            # Cosine similarity
            similarity = float(
                embedder.encode(query).dot(doc_embedding) / 
                (len(embedder.encode(query)) * len(doc_embedding) + 1e-10)
            )
            scores[doc_id] = similarity
        
        # Return top-k
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        retrieved_ids = [doc_id for doc_id, _ in ranked[:top_k]]
        
        return [
            self.documents[i] for i, doc in enumerate(self.documents)
            if doc['id'] in retrieved_ids
        ]
    
    def generate_with_context(self, query: str) -> str:
        """Retrieve + Generate with context"""
        # Retrieve
        relevant_docs = self.retrieve(query, top_k=3)
        
        # Build context
        context = "Relevant information:\n"
        for doc in relevant_docs:
            context += f"- {doc['text']}\n"
        
        # Generate
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": f"{context}\n\nQuestion: {query}\n\nAnswer based on the above:"
            }]
        )
        
        return response.content[0].text


# ============================================================================
# Pattern 2: Context Windowing with Summarization
# ============================================================================

class ContextWindow:
    """Manage long conversations with sliding window"""
    
    def __init__(self, max_recent_turns: int = 10):
        self.max_recent_turns = max_recent_turns
        self.conversation = []
        self.summary = ""
    
    def add_turn(self, user_msg: str, assistant_msg: str):
        """Add turn and manage window"""
        self.conversation.append({
            "user": user_msg,
            "assistant": assistant_msg,
            "timestamp": datetime.now().isoformat()
        })
        
        # Summarize if too long
        if len(self.conversation) > self.max_recent_turns * 2:
            self._compress()
    
    def _compress(self):
        """Compress old turns"""
        old_turns = self.conversation[:-self.max_recent_turns]
        
        # Summarize
        text = "\n".join([
            f"User: {t['user']}\nAssistant: {t['assistant']}"
            for t in old_turns
        ])
        
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            messages=[{
                "role": "user",
                "content": f"Summarize this conversation in 100 words:\n{text}"
            }]
        )
        
        self.summary = response.content[0].text
        self.conversation = self.conversation[-self.max_recent_turns:]
    
    def get_context(self) -> str:
        """Get full context"""
        context = ""
        
        if self.summary:
            context += f"Summary of earlier conversation:\n{self.summary}\n\n"
        
        context += "Recent conversation:\n"
        for turn in self.conversation:
            context += f"User: {turn['user']}\n"
            context += f"Assistant: {turn['assistant']}\n\n"
        
        return context
    
    def chat(self, user_msg: str) -> str:
        """Add message and get response"""
        context = self.get_context()
        
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": f"{context}\n\nUser: {user_msg}\n\nAssistant response:"
            }]
        )
        
        assistant_msg = response.content[0].text
        self.add_turn(user_msg, assistant_msg)
        
        return assistant_msg


# ============================================================================
# Pattern 3: Context Caching with Redis
# ============================================================================

class CachedContextManager:
    """Cache expensive context computations"""
    
    def __init__(self, ttl_seconds: int = 3600):
        self.ttl = ttl_seconds
    
    def get_customer_context(self, customer_id: int, use_cache: bool = True) -> dict:
        """Get customer context with caching"""
        cache_key = f"customer_context:{customer_id}"
        
        # Try cache
        if use_cache:
            cached = redis_client.get(cache_key)
            if cached:
                import json
                return json.loads(cached)
        
        # Compute
        conn = sqlite3.connect("loans.db")
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT name, credit_score, income FROM customers WHERE id=?",
            (customer_id,)
        )
        customer = cursor.fetchone()
        
        cursor.execute(
            "SELECT amount, status FROM loans WHERE customer_id=? LIMIT 5",
            (customer_id,)
        )
        loans = cursor.fetchall()
        
        conn.close()
        
        context = {
            "name": customer[0] if customer else "Unknown",
            "credit_score": customer[1] if customer else 0,
            "income": customer[2] if customer else 0,
            "loans": loans or []
        }
        
        # Cache
        import json
        redis_client.setex(
            cache_key,
            self.ttl,
            json.dumps(context, default=str)
        )
        
        return context


# ============================================================================
# Pattern 4: Multi-Tier Context Priority
# ============================================================================

class MultiTierContextBuilder:
    """Build context respecting tiers and token limits"""
    
    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens
        self.tiers = {
            "required": [],
            "important": [],
            "optional": []
        }
    
    def build_context(self) -> dict:
        """Build context respecting tiers"""
        context = {
            "required": "",
            "important": "",
            "optional": "",
            "token_count": 0
        }
        
        token_count = 0
        
        # Required tier (always include)
        for item in self.tiers["required"]:
            context["required"] += item + "\n"
            token_count += len(item) // 4
        
        # Important tier (if 80% not exceeded)
        for item in self.tiers["important"]:
            tokens_needed = len(item) // 4
            if token_count + tokens_needed <= self.max_tokens * 0.8:
                context["important"] += item + "\n"
                token_count += tokens_needed
        
        # Optional tier (remaining space)
        for item in self.tiers["optional"]:
            tokens_needed = len(item) // 4
            if token_count + tokens_needed <= self.max_tokens:
                context["optional"] += item + "\n"
                token_count += tokens_needed
        
        context["token_count"] = token_count
        return context


# ============================================================================
# Pattern 5: Adaptive Context Selection
# ============================================================================

class AdaptiveContextSelector:
    """Select most relevant context based on query"""
    
    def __init__(self, max_tokens: int = 2000):
        self.max_tokens = max_tokens
    
    def select(self, query: str, all_context: dict) -> dict:
        """Select relevant context"""
        query_embedding = embedder.encode(query)
        
        # Score relevance
        scores = {}
        for key, value in all_context.items():
            value_embedding = embedder.encode(str(value))
            
            # Cosine similarity
            similarity = float(query_embedding.dot(value_embedding))
            scores[key] = similarity
        
        # Domain-specific boosts
        if "loan" in query.lower():
            scores["credit_score"] = scores.get("credit_score", 0) * 2.0
            scores["income"] = scores.get("income", 0) * 2.0
        
        # Select until token limit
        selected = {}
        token_count = 0
        
        for key, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            value_str = str(all_context[key])
            tokens_needed = len(value_str) // 4
            
            if token_count + tokens_needed <= self.max_tokens:
                selected[key] = all_context[key]
                token_count += tokens_needed
        
        return selected


# ============================================================================
# Usage Examples
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("RAW SDK - Advanced Pattern Examples")
    print("=" * 70)
    
    # RAG Example
    print("\n1. RAG (Retrieval Augmented Generation):")
    documents = [
        {
            "id": "policy-001",
            "text": "Max DTI 43%, min credit 600, min income $30k"
        },
        {
            "id": "faq-001",
            "text": "Can I get approved with bad credit? Min 600 required."
        },
    ]
    rag = RAGSystem(documents)
    # answer = rag.generate_with_context("Can I get approved with 580 credit?")
    # print(f"   {answer[:100]}...")
    
    # Windowing Example
    print("\n2. Context Windowing:")
    window = ContextWindow(max_recent_turns=3)
    # response = window.chat("Hi, I need a loan")
    # print(f"   {response[:100]}...")
    
    # Caching Example
    print("\n3. Context Caching:")
    cache = CachedContextManager()
    context1 = cache.get_customer_context(1)
    print(f"   Got cached context for customer 1")
    
    # Multi-Tier Example
    print("\n4. Multi-Tier Context:")
    multi_tier = MultiTierContextBuilder()
    multi_tier.tiers["required"] = ["Policies: Max DTI 43%"]
    multi_tier.tiers["important"] = ["Credit: 750", "Income: $150k"]
    multi_tier.tiers["optional"] = ["Birthday: 1990-01-15"]
    result = multi_tier.build_context()
    print(f"   Built multi-tier context ({result['token_count']} tokens)")
    
    # Adaptive Example
    print("\n5. Adaptive Selection:")
    adapter = AdaptiveContextSelector()
    context = {
        "name": "John",
        "credit_score": 750,
        "income": 150000,
        "birthday": "1990-01-15",
        "preferences": "Email only"
    }
    selected = adapter.select("What's my credit score?", context)
    print(f"   Selected {len(selected)} context items: {list(selected.keys())}")

