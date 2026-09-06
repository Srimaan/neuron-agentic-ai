# V2 Build Guide: Multi-Turn Conversation with Windowing

## Overview
**What:** Add conversation memory and token management to V1
**Why:** Real loans need multiple questions, not one-shot evaluation
**Pattern:** Week 2 Pattern 2 (Context Windowing)
**Time:** 60 minutes

---

## Architecture

```
Customer → Conversation Input
            ↓
        Conversation Window
        (Remember turns 1-10)
            ↓
        Automatic Summarization
        (Compress old turns)
            ↓
        Build Context
        (Summary + Recent)
            ↓
        Claude API
            ↓
        Conversation Response
```

---

## Step 1: ConversationWindow Class (15 min)

### Goal
Store and compress conversation history.

### What to Build

```python
class ConversationWindow:
    def __init__(self, max_recent: int = 10):
        self.max_recent = max_recent  # Keep last 10 turns
        self.turns = []                # Current turns
        self.summary = ""              # Compressed old turns
        self.client = anthropic.Anthropic()
    
    def add(self, user: str, assistant: str):
        """Add a turn"""
        self.turns.append({
            "user": user,
            "assistant": assistant,
            "timestamp": datetime.now().isoformat()
        })
        
        # Auto-compress if too many
        if len(self.turns) > self.max_recent * 2:
            self._compress()
    
    def _compress(self):
        """Summarize old turns using Claude"""
        old_turns = self.turns[:-self.max_recent]
        
        # Build text from old turns
        text = "\n".join([
            f"Customer: {t['user']}\nLoan Officer: {t['assistant']}"
            for t in old_turns
        ])
        
        # Use Claude to summarize
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            messages=[{
                "role": "user",
                "content": f"Summarize in 100 words:\n{text}"
            }]
        )
        
        self.summary = response.content[0].text
        self.turns = self.turns[-self.max_recent:]  # Keep only recent
    
    def get_context(self) -> str:
        """Get formatted context for Claude"""
        ctx = ""
        if self.summary:
            ctx += f"EARLIER:\n{self.summary}\n\n"
        
        ctx += "RECENT:\n"
        for t in self.turns:
            ctx += f"Customer: {t['user']}\n"
            ctx += f"Loan Officer: {t['assistant']}\n\n"
        
        return ctx
```

### Key Concepts
- `add()`: Store each conversation turn
- `_compress()`: When history > 20 turns, summarize first 10 and keep last 10
- `get_context()`: Format history for Claude

### Testing
```python
window = ConversationWindow(max_recent=3)
window.add("Hi", "Hello!")
window.add("Need $20k", "What for?")
ctx = window.get_context()  # Should show both turns
```

---

## Step 2: LoanEvaluationV2 Class (30 min)

### Goal
Use windowing for multi-turn loan conversations.

### What to Build

```python
class LoanEvaluationV2:
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"
        self.window = ConversationWindow(max_recent=10)
        self.customer_data = None
        self.decision = None
    
    def start_conversation(self, customer: Dict) -> str:
        """Initiate conversation"""
        self.customer_data = customer
        
        prompt = f"""
You are a friendly loan officer.

CUSTOMER: {customer['name']}
CREDIT: {customer['credit_score']}
INCOME: ${customer['income']:,}
EMPLOYMENT: {customer['employment_years']} years

RULES:
- Min credit: 600
- Min employment: 2 years
- Loan range: $5K-$50K

Greet them and ask about their loan needs.
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        
        greeting = response.content[0].text
        self.window.add("(Starting)", greeting)  # Mark start
        return greeting
    
    def respond_to_customer(self, customer_message: str) -> str:
        """Process customer input"""
        
        # Get full context with history
        context = self.window.get_context()
        
        # New prompt with context
        prompt = f"""
You are a loan officer. Conversation so far:

{context}

Customer just said: {customer_message}

CUSTOMER DATA:
- Name: {self.customer_data['name']}
- Credit: {self.customer_data['credit_score']}
- Income: ${self.customer_data['income']:,}
- Employment: {self.customer_data['employment_years']} years

RULES:
- Min credit: 600
- Max DTI: 43%
- Min employment: 2 years
- Loan range: $5K-$50K

Respond. If you have enough info, decide: APPROVE/DENY/REVIEW.
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        
        message = response.content[0].text
        self.window.add(customer_message, message)
        
        # Check for decision
        if "APPROVE" in message.upper() or "DENY" in message.upper():
            self._extract_decision(message)
        
        return message
```

### Key Points
- `start_conversation()`: Send first prompt, establish context
- `respond_to_customer()`: Get history via `window.get_context()`
- Claude sees previous turns + new message
- Auto-summarization happens in background

---

## Step 3: Run Multi-Turn Conversation (15 min)

### What to Build

```python
def run_conversation():
    customer = {
        "name": "John Smith",
        "credit_score": 680,
        "income": 80000,
        "employment_years": 3
    }
    
    system = LoanEvaluationV2()
    
    # Start
    greeting = system.start_conversation(customer)
    print(f"Officer: {greeting}\n")
    
    # Multiple turns
    turns = [
        "Hi, I need $20,000 for home improvements",
        "I've been at my job for 3 years",
        "My credit score is 680",
        "Annual salary is $80,000",
        "Can you approve me?"
    ]
    
    for turn in turns:
        print(f"Customer: {turn}")
        response = system.respond_to_customer(turn)
        print(f"Officer: {response[:200]}...\n")
        
        if system.decision:
            break
```

---

## HOMEWORK ASSIGNMENT

### Build These Features:

1. **Conversation Metrics**
   - Count total turns
   - Show compression rate
   - Display context size

2. **Decision Tracking**
   - Record when decision made
   - Track turn number
   - Show confidence

3. **Context Analysis**
   - Print context size before/after
   - Show summary content
   - Track token usage

### Solution Check
```python
# Should show:
Turn 1: context = 200 chars (no history yet)
Turn 3: context = 400 chars (1 summary + 2 recent)
Turn 5: context = 600 chars (1 summary + 4 recent)
```

---

## Key Differences: V1 → V2

| Feature | V1 | V2 |
|---------|----|----|
| Input | All customer info once | Multi-turn conversation |
| Memory | None | Last 10 turns |
| Compression | None | Auto-summarize old |
| Turns | 1 | Many (5-10+) |
| Prompts | 1 simple | Multiple with history |
| Pattern | Static | Dynamic windowing |

---

## Expected Output

```
Loan Officer: Hello! I'm here to help with your loan application...

Customer: I need $20,000 for home improvements
Loan Officer: That's a great use of funds! How long have you worked...

Customer: I've been at my job for 3 years
Loan Officer: Excellent, that meets our requirements...

[After 5-6 turns]
Loan Officer: Based on our discussion, I'm happy to APPROVE your...
```

---

## Debugging Tips

**Problem:** Claude asks same questions twice
- **Fix:** Use window.get_context() to include history

**Problem:** Context gets too long
- **Fix:** Decrease max_recent (was 10, try 5)

**Problem:** Summary loses important info
- **Fix:** Improve summarization prompt

---

## Time Breakdown
- Step 1 (ConversationWindow): 15 min
- Step 2 (LoanEvaluationV2): 30 min
- Step 3 (Run): 15 min
- **Total: 60 minutes**

---

## Next: V3 Tool Agent
V2 adds *conversation history*. V3 adds *tool calling* and *RAG*.

