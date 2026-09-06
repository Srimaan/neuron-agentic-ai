"""
Framework 52: Integrated System - All 8 Patterns Combined

Combines all advanced patterns into ONE cohesive production system:
1. RAG (Retrieval Augmented Generation)
2. Context Windowing
3. Adaptive Selection
4. Caching
5. Multi-Tier Context
6. Summarization
7. Real-Time Updates
8. Versioning

Use case: Loan application system that handles customer context intelligently
"""

import anthropic
import redis
import sqlite3
import json
from datetime import datetime
from sentence_transformers import SentenceTransformer
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import time

client = anthropic.Anthropic()
redis_client = redis.Redis(host='localhost', port=6379)
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# ============================================================================
# PATTERN 1: RAG - Knowledge Base
# ============================================================================

@dataclass
class Document:
    id: str
    text: str
    category: str
    version: int = 1

class KnowledgeBase:
    """RAG system for loan policies"""
    
    def __init__(self):
        self.documents = [
            Document("policy-001", "Max DTI 43%, Min credit 600, Min income $30k", "policy"),
            Document("policy-002", "Employment history required 2+ years", "policy"),
            Document("faq-001", "Bad credit? Min 600 required for approval", "faq"),
            Document("product-001", "Personal loans $5k-$50k, rates 5.99%-15.99%", "product"),
        ]
        self.embeddings = self._embed_all()
    
    def _embed_all(self):
        """Embed all documents"""
        return {
            doc.id: embedder.encode(doc.text)
            for doc in self.documents
        }
    
    def retrieve(self, query: str, top_k: int = 3) -> List[Document]:
        """Retrieve relevant documents"""
        query_embedding = embedder.encode(query)
        
        scores = {}
        for doc in self.documents:
            doc_embedding = self.embeddings[doc.id]
            similarity = float(query_embedding.dot(doc_embedding))
            scores[doc.id] = similarity
        
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [
            next(d for d in self.documents if d.id == doc_id)
            for doc_id, _ in ranked[:top_k]
        ]


# ============================================================================
# PATTERN 2: Context Windowing - Conversation Management
# ============================================================================

class ConversationWindow:
    """Manage conversation with automatic summarization"""
    
    def __init__(self, max_recent: int = 10):
        self.max_recent = max_recent
        self.turns = []
        self.summary = ""
    
    def add(self, user: str, assistant: str):
        """Add turn and compress if needed"""
        self.turns.append({"user": user, "assistant": assistant, "ts": datetime.now()})
        
        if len(self.turns) > self.max_recent * 2:
            self._compress()
    
    def _compress(self):
        """Summarize old turns"""
        old = self.turns[:-self.max_recent]
        text = "\n".join([f"U: {t['user']}\nA: {t['assistant']}" for t in old])
        
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            messages=[{
                "role": "user",
                "content": f"Summarize in 100 words:\n{text}"
            }]
        )
        
        self.summary = response.content[0].text
        self.turns = self.turns[-self.max_recent:]
    
    def get_context(self) -> str:
        """Get full context for Claude"""
        ctx = ""
        if self.summary:
            ctx += f"Summary:\n{self.summary}\n\n"
        ctx += "Recent:\n"
        for t in self.turns:
            ctx += f"User: {t['user']}\nAssistant: {t['assistant']}\n"
        return ctx


# ============================================================================
# PATTERN 3: Adaptive Selection - Relevance Scoring
# ============================================================================

class ContextAdaptor:
    """Select only relevant context"""
    
    def __init__(self, max_tokens: int = 3000):
        self.max_tokens = max_tokens
    
    def select(self, query: str, all_context: dict) -> dict:
        """Score and select"""
        query_emb = embedder.encode(query)
        
        scores = {}
        for key, value in all_context.items():
            value_emb = embedder.encode(str(value))
            scores[key] = float(query_emb.dot(value_emb))
        
        # Domain boosts
        if "credit" in query.lower():
            scores["credit_score"] = scores.get("credit_score", 0) * 2.0
        if "income" in query.lower():
            scores["income"] = scores.get("income", 0) * 2.0
        
        selected = {}
        tokens = 0
        for key, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            value_str = str(all_context[key])
            needed = len(value_str) // 4
            if tokens + needed <= self.max_tokens:
                selected[key] = all_context[key]
                tokens += needed
        
        return selected


# ============================================================================
# PATTERN 4: Caching - Redis
# ============================================================================

class CacheLayer:
    """Redis caching for expensive operations"""
    
    def __init__(self, ttl: int = 3600):
        self.ttl = ttl
    
    def get(self, key: str) -> Optional[dict]:
        """Get from cache"""
        data = redis_client.get(f"ctx:{key}")
        return json.loads(data) if data else None
    
    def set(self, key: str, value: dict):
        """Store in cache"""
        redis_client.setex(f"ctx:{key}", self.ttl, json.dumps(value, default=str))
    
    def get_or_compute(self, key: str, compute_fn):
        """Cache-aside pattern"""
        cached = self.get(key)
        if cached:
            return cached
        
        result = compute_fn()
        self.set(key, result)
        return result


# ============================================================================
# PATTERN 5: Multi-Tier Context
# ============================================================================

class MultiTierBuilder:
    """Build context by tier"""
    
    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens
        self.tiers = {"required": [], "important": [], "optional": []}
    
    def build(self) -> str:
        """Build respecting tiers"""
        result = ""
        tokens = 0
        
        # Required (always)
        for item in self.tiers["required"]:
            result += item + "\n"
            tokens += len(item) // 4
        
        # Important (80%)
        for item in self.tiers["important"]:
            needed = len(item) // 4
            if tokens + needed <= self.max_tokens * 0.8:
                result += item + "\n"
                tokens += needed
        
        # Optional (rest)
        for item in self.tiers["optional"]:
            needed = len(item) // 4
            if tokens + needed <= self.max_tokens:
                result += item + "\n"
                tokens += needed
        
        return result


# ============================================================================
# PATTERN 6: Summarization
# ============================================================================

class DocumentSummarizer:
    """Pre-compute summaries"""
    
    def __init__(self):
        self.cache = redis_client
    
    def summarize(self, doc_id: str, text: str, force: bool = False) -> str:
        """Summarize or get cached"""
        cache_key = f"summary:{doc_id}"
        
        if not force:
            cached = self.cache.get(cache_key)
            if cached:
                return cached.decode()
        
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            messages=[{
                "role": "user",
                "content": f"Summarize in 100 words:\n{text}"
            }]
        )
        
        summary = response.content[0].text
        self.cache.setex(cache_key, 86400, summary)  # 24h
        return summary


# ============================================================================
# PATTERN 7: Real-Time Updates (Simulated)
# ============================================================================

class RealtimeContextUpdater:
    """Stream context changes"""
    
    def __init__(self):
        self.updates = []
        self.subscriptions = []
    
    def subscribe(self, callback):
        """Listen for updates"""
        self.subscriptions.append(callback)
    
    def update(self, field: str, value: any, reason: str = ""):
        """Broadcast update"""
        update = {
            "field": field,
            "value": value,
            "timestamp": datetime.now().isoformat(),
            "reason": reason
        }
        self.updates.append(update)
        
        for callback in self.subscriptions:
            callback(update)


# ============================================================================
# PATTERN 8: Versioning - Audit Trail
# ============================================================================

class VersionedContextStore:
    """Version all context changes"""
    
    def __init__(self, context_id: str):
        self.context_id = context_id
        self.versions = []
        self.current = 0
    
    def set(self, data: dict, reason: str = ""):
        """Create new version"""
        version = {
            "v": self.current + 1,
            "ts": datetime.now().isoformat(),
            "data": data,
            "reason": reason,
            "hash": self._hash(data)
        }
        
        self.versions.append(version)
        self.current += 1
        return version["v"]
    
    def get(self, v: int = None) -> dict:
        """Get specific version"""
        v = v or self.current
        return next((ver["data"] for ver in self.versions if ver["v"] == v), None)
    
    def audit_trail(self) -> list:
        """Full history"""
        return [
            {
                "v": v["v"],
                "ts": v["ts"],
                "reason": v["reason"],
                "hash": v["hash"]
            }
            for v in self.versions
        ]
    
    def _hash(self, data: dict) -> str:
        """Content hash"""
        import hashlib
        json_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(json_str.encode()).hexdigest()[:12]


# ============================================================================
# INTEGRATED SYSTEM - All 8 Patterns Combined
# ============================================================================

class LoanEvaluationSystem:
    """Production loan evaluation using all 8 patterns"""
    
    def __init__(self):
        # Initialize all components
        self.kb = KnowledgeBase()
        self.window = ConversationWindow()
        self.adaptor = ContextAdaptor()
        self.cache = CacheLayer()
        self.tiers = MultiTierBuilder()
        self.summarizer = DocumentSummarizer()
        self.updater = RealtimeContextUpdater()
        self.versioned = None
        
        # Tracking
        self.metrics = {
            "requests": 0,
            "cache_hits": 0,
            "tokens_saved": 0,
            "latencies": []
        }
    
    def evaluate_loan(self, customer_id: int, query: str) -> Dict:
        """Main evaluation method"""
        start = time.time()
        
        # Initialize versioning for this customer
        self.versioned = VersionedContextStore(f"customer:{customer_id}")
        
        # PATTERN 4: Check cache first
        cached = self.cache.get(f"customer:{customer_id}")
        customer_data = cached or self._fetch_customer(customer_id)
        
        if cached:
            self.metrics["cache_hits"] += 1
        
        # PATTERN 1: RAG - Retrieve relevant policies
        policies = self.kb.retrieve(query, top_k=3)
        policies_text = "\n".join([f"- {doc.text}" for doc in policies])
        
        # PATTERN 6: Summarization - Pre-summarized docs
        summarized_policies = "\n".join([
            f"- {self.summarizer.summarize(doc.id, doc.text)}"
            for doc in policies[:2]
        ])
        
        # PATTERN 3: Adaptive - Select only relevant context
        all_context = {
            "customer_name": customer_data["name"],
            "credit_score": customer_data["credit_score"],
            "income": customer_data["income"],
            "employment_years": customer_data["employment_years"],
            "existing_loans": len(customer_data["loans"]),
            "policies": policies_text,
            "birthday": customer_data["birthday"],
            "phone": customer_data["phone"]
        }
        
        selected_context = self.adaptor.select(query, all_context)
        
        # PATTERN 5: Multi-Tier - Prioritize context
        self.tiers.tiers["required"] = [
            f"Policies:\n{policies_text}",
            f"Customer: {selected_context.get('customer_name', 'N/A')} (Credit: {selected_context.get('credit_score', 0)})"
        ]
        self.tiers.tiers["important"] = [
            f"Income: ${selected_context.get('income', 0)}",
            f"Employment: {selected_context.get('employment_years', 0)} years"
        ]
        self.tiers.tiers["optional"] = [
            f"Existing loans: {selected_context.get('existing_loans', 0)}"
        ]
        
        tiered_context = self.tiers.build()
        
        # PATTERN 2: Windowing - Conversation history
        conv_context = self.window.get_context()
        
        # PATTERN 8: Versioning - Record this evaluation
        self.versioned.set(selected_context, reason="Loan evaluation")
        
        # Build final prompt
        prompt = f"""
Customer Context (Adaptive + Multi-Tier):
{tiered_context}

Conversation History:
{conv_context}

Customer Query: {query}

Provide loan evaluation decision and explanation.
"""
        
        # Get Claude's response
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        
        decision = response.content[0].text
        
        # Add to conversation window
        self.window.add(query, decision)
        
        # PATTERN 7: Real-time update (simulate)
        self.updater.update("evaluation_complete", True, "Loan decision made")
        
        # Record metrics
        elapsed = time.time() - start
        self.metrics["requests"] += 1
        self.metrics["latencies"].append(elapsed)
        self.metrics["tokens_saved"] += len(all_context) - len(selected_context)  # Rough
        
        return {
            "decision": decision,
            "context_used": len(selected_context),
            "context_available": len(all_context),
            "context_efficiency": f"{(1 - len(selected_context)/len(all_context)) * 100:.0f}%",
            "latency_ms": elapsed * 1000,
            "cache_used": cached is not None,
            "audit_trail": self.versioned.audit_trail()
        }
    
    def _fetch_customer(self, customer_id: int) -> dict:
        """Fetch from database"""
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        
        # Mock data
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER, name TEXT, credit_score INTEGER, 
                income INTEGER, employment_years INTEGER, birthday TEXT, phone TEXT
            )
        """)
        
        cursor.execute("INSERT INTO customers VALUES (?,?,?,?,?,?,?)",
            (customer_id, f"Customer {customer_id}", 750, 150000, 5, "1990-01-15", "555-1234"))
        cursor.execute("SELECT * FROM customers WHERE id=?", (customer_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "id": result[0],
                "name": result[1],
                "credit_score": result[2],
                "income": result[3],
                "employment_years": result[4],
                "birthday": result[5],
                "phone": result[6],
                "loans": []
            }
        return {}
    
    def print_metrics(self):
        """Summary statistics"""
        print("\n" + "="*70)
        print("INTEGRATED SYSTEM METRICS")
        print("="*70)
        print(f"Requests processed: {self.metrics['requests']}")
        print(f"Cache hits: {self.metrics['cache_hits']}")
        if self.metrics['latencies']:
            avg_latency = sum(self.metrics['latencies']) / len(self.metrics['latencies'])
            print(f"Avg latency: {avg_latency*1000:.1f}ms")
        print(f"Tokens saved (approx): {self.metrics['tokens_saved']}")


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("INTEGRATED SYSTEM - All 8 Patterns Combined")
    print("="*70)
    
    system = LoanEvaluationSystem()
    
    # Simulate multiple requests
    queries = [
        "Can I get approved with 650 credit score?",
        "What's the interest rate?",
        "Can I borrow $30,000?"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n[Request {i}] {query}")
        result = system.evaluate_loan(1, query)
        print(f"  Decision: {result['decision'][:100]}...")
        print(f"  Context used: {result['context_used']}/{result['context_available']} ({result['context_efficiency']} saved)")
        print(f"  Latency: {result['latency_ms']:.0f}ms")
        print(f"  Cache: {'HIT' if result['cache_used'] else 'MISS'}")
    
    system.print_metrics()

