# V3 Build Guide: Tool-Integrated Agent with RAG

## Overview
**What:** Add tool calling and retrieval-augmented generation
**Why:** Verify facts with real tools, retrieve policies from knowledge base
**Patterns:** Week 2 Pattern 1 (RAG) + Tool Calling
**Time:** 90 minutes
**Complexity:** ⭐⭐⭐

---

## Architecture

```
Query
  ↓
RAG Retrieval (Pattern 1)
  ├─ Vector search policies
  └─ Return top-3 relevant
  ↓
Agent Loop
  ├─ Claude thinks about tools
  ├─ Check credit_score()
  ├─ Verify income()
  ├─ Verify employment()
  └─ Collect results
  ↓
Decision Making
  └─ Synthesize findings
```

---

## Step 1: Knowledge Base with RAG (25 min)

### Goal
Store policies and retrieve relevant ones.

### What to Build

```python
from sentence_transformers import SentenceTransformer

class PolicyKnowledgeBase:
    def __init__(self):
        self.documents = [
            {
                "id": "policy-001",
                "title": "DTI Requirement",
                "content": "Max debt-to-income ratio is 43%. Calculate..."
            },
            {
                "id": "policy-002",
                "title": "Credit Score Minimum",
                "content": "Minimum credit score of 600 required..."
            },
            # More policies...
        ]
        
        # Load embedding model
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.embeddings = self._embed_docs()
    
    def _embed_docs(self) -> Dict:
        """Convert text to vectors"""
        embeddings = {}
        for doc in self.documents:
            embedding = self.embedder.encode(doc['content'])
            embeddings[doc['id']] = embedding
        return embeddings
    
    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        """RAG retrieval: find relevant policies"""
        
        # Embed the query
        query_embedding = self.embedder.encode(query)
        
        # Score against all policies
        scores = {}
        for doc in self.documents:
            doc_emb = self.embeddings[doc['id']]
            # Cosine similarity
            similarity = float(query_emb.dot(doc_emb))
            scores[doc['id']] = similarity
        
        # Return top-k
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score in ranked[:top_k]:
            doc = next(d for d in self.documents if d['id'] == doc_id)
            results.append(doc)
        
        return results
```

### Key Concepts
- **Embeddings**: Convert text to numbers (768-dim vector)
- **Similarity**: Measure how related two texts are
- **Retrieval**: Find top-3 most relevant policies

### Install Dependencies
```bash
pip install sentence-transformers
```

---

## Step 2: Tool Definitions (20 min)

### Goal
Define functions Claude can call.

### What to Build

```python
def check_credit_tool(credit_score: int) -> Dict:
    """Tool: Verify credit score"""
    min_credit = 600
    
    if credit_score >= min_credit:
        rate_tier = "Prime" if credit_score >= 720 else "Standard"
        return {
            "eligible": True,
            "score": credit_score,
            "rate_tier": rate_tier,
            "message": f"Credit {credit_score} is eligible"
        }
    else:
        return {
            "eligible": False,
            "score": credit_score,
            "message": f"Credit {credit_score} is below minimum {min_credit}"
        }


def verify_income_tool(annual_income: int, requested_loan: int) -> Dict:
    """Tool: Check income sufficiency"""
    monthly = annual_income / 12
    payment = requested_loan / 60  # 5-year loan
    ratio = (payment / monthly) * 100
    
    return {
        "monthly_income": monthly,
        "estimated_payment": payment,
        "payment_ratio": ratio,
        "message": f"Payment ratio: {ratio:.1f}%"
    }


def check_employment_tool(years_employed: int) -> Dict:
    """Tool: Verify employment"""
    min_years = 2
    eligible = years_employed >= min_years
    
    return {
        "eligible": eligible,
        "years": years_employed,
        "message": f"Employment: {years_employed} years (min {min_years})"
    }

# Tools registry
TOOLS = {
    "check_credit": check_credit_tool,
    "verify_income": verify_income_tool,
    "check_employment": check_employment_tool
}
```

### Key Points
- Functions return structured data (Dict)
- Each tool handles one responsibility
- Tools are deterministic (same input = same output)

---

## Step 3: Agent Loop (35 min)

### Goal
Have Claude decide which tools to use and process results.

### What to Build

```python
class LoanEvaluationV3:
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"
        self.kb = PolicyKnowledgeBase()
        self.tool_calls = []
    
    def evaluate_loan(self, customer: Dict) -> Dict:
        # Step 1: Retrieve relevant policies (RAG)
        policies = self.kb.retrieve(
            f"credit {customer['credit_score']} income {customer['income']}"
        )
        policies_text = "\n".join([
            f"- {p['title']}: {p['content']}" for p in policies
        ])
        
        # Step 2: Build prompt with policies
        prompt = f"""
You are a loan officer with tools available.

APPLICANT: {customer['name']}
- Credit: {customer['credit_score']}
- Income: ${customer['income']:,}
- Employment: {customer['employment_years']} years
- Requested: ${customer.get('loan_amount', 25000):,}

RELEVANT POLICIES:
{policies_text}

AVAILABLE TOOLS:
1. check_credit(score) - Verify credit eligibility
2. verify_income(annual, loan_amount) - Check income
3. check_employment(years) - Verify employment

TASK:
1. Use tools to verify each criterion
2. Based on results, decide: APPROVE or DENY
3. Explain your reasoning

Use tools first, then decide.
"""
        
        # Step 3: Agent loop
        messages = [{"role": "user", "content": prompt}]
        
        for iteration in range(5):  # Max 5 rounds
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=messages
            )
            
            response_text = response.content[0].text
            
            # Step 4: Parse tool calls from response
            tool_results = []
            
            if "check_credit" in response_text:
                result = check_credit_tool(customer['credit_score'])
                tool_results.append(f"Credit: {result['message']}")
                self.tool_calls.append("check_credit")
            
            if "verify_income" in response_text:
                result = verify_income_tool(
                    customer['income'],
                    customer.get('loan_amount', 25000)
                )
                tool_results.append(f"Income: {result['message']}")
                self.tool_calls.append("verify_income")
            
            if "check_employment" in response_text:
                result = check_employment_tool(customer['employment_years'])
                tool_results.append(f"Employment: {result['message']}")
                self.tool_calls.append("check_employment")
            
            # Step 5: Stop if no tools or decision made
            if not tool_results or "APPROVE" in response_text or "DENY" in response_text:
                break
            
            # Step 6: Add tool results and continue
            messages.append({"role": "assistant", "content": response_text})
            summary = "\n".join(tool_results)
            messages.append({
                "role": "user",
                "content": f"Tool results:\n{summary}\n\nNow decide."
            })
        
        return {
            "decision": "APPROVE" if "APPROVE" in response_text else "DENY",
            "reasoning": response_text[:300],
            "tools_used": self.tool_calls
        }
```

### Agent Loop Explanation

1. **Initial Prompt**: Claude sees customer + tools
2. **First Response**: Claude thinks, mentions which tools to call
3. **Parse Tools**: We detect tool mentions in text
4. **Execute Tools**: Call the functions, get results
5. **Tool Results**: Feed results back to Claude
6. **Final Response**: Claude makes decision

---

## HOMEWORK ASSIGNMENT

### Build Features:

1. **Tool Tracking**
   - Count how many tools called
   - Show which tools used
   - Track tool latency

2. **Policy Relevance**
   - Show retrieved policies
   - Display similarity scores
   - Prove RAG is working

3. **Decision Confidence**
   - Track how many iterations needed
   - Note if all tools called
   - Measure consistency

### Solution Check
```python
# Should see:
Retrieved policies:
- DTI Requirement (similarity: 0.87)
- Credit Score Minimum (similarity: 0.92)
- Employment History (similarity: 0.85)

Tools used: ['check_credit', 'verify_income', 'check_employment']
Decision: APPROVE
```

---

## Key Differences: V2 → V3

| Feature | V2 | V3 |
|---------|----|----|
| Memory | Multi-turn | Single turn |
| Data | Hardcoded | Retrieved (RAG) |
| Verification | None | Tool calling |
| Policies | Implicit | Explicit + retrieved |
| Agent | None | Agentic loop |

---

## Why RAG + Tools Together?

**Without RAG:** Hardcode all policies in prompt
**Without Tools:** Trust customer's reported numbers

**With both:** 
- Retrieve only relevant policies (RAG)
- Verify claims with tools
- More accurate, more efficient

---

## Common Issues

**Problem:** Claude doesn't call tools
- **Fix:** Make tools clearer in prompt, explicit instructions

**Problem:** Similar policies not retrieved
- **Fix:** Policies need clearer text, better descriptions

**Problem:** Tool results ignored
- **Fix:** Add explicit instruction: "Use tool results to decide"

---

## Time Breakdown
- Step 1 (Knowledge Base): 25 min
- Step 2 (Tools): 20 min
- Step 3 (Agent Loop): 35 min
- Step 4 (Debug): 10 min
- **Total: 90 minutes**

---

## Next: V4 Multi-Agent
V3 has *one agent with tools*. V4 has *three specialized agents*.

