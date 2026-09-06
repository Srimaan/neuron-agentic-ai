# Context Engineering Exercises

Complete all 6 exercises. Solutions provided below each.

---

## Exercise 1: Token Counting (Easy, 10 min)

### Task
Count tokens in different contexts and identify the most efficient.

```python
import anthropic

client = anthropic.Anthropic()

contexts = [
    "Customer: John Doe, Credit: 750, Income: $150k",
    "John has excellent credit score of 750 and annual income of $150,000",
    """Customer Information:
    Name: John Doe
    Credit Score: 750
    Annual Income: $150,000
    Employment: 5 years at TechCorp
    Previous Loans: 3 approved
    Current Debts: $25,000""",
]

# TODO: Count tokens for each context
# TODO: Which is most efficient (fewest tokens)?
# TODO: What's the token/information ratio?
```

### Solution
```python
import anthropic

client = anthropic.Anthropic()

contexts = [
    "Customer: John Doe, Credit: 750, Income: $150k",
    "John has excellent credit score of 750 and annual income of $150,000",
    """Customer Information:
    Name: John Doe
    Credit Score: 750
    Annual Income: $150,000
    Employment: 5 years at TechCorp
    Previous Loans: 3 approved
    Current Debts: $25,000""",
]

for i, context in enumerate(contexts, 1):
    response = client.messages.count_tokens(
        model="claude-3-5-sonnet-20241022",
        messages=[{"role": "user", "content": context}]
    )
    
    tokens = response.input_tokens
    info_items = len(context.split(','))
    ratio = info_items / tokens
    
    print(f"Context {i}: {tokens} tokens (ratio: {ratio:.2f} items/token)")

# Most efficient: Context 1 (shortest, most concise)
```

---

## Exercise 2: Database Context Retrieval (Medium, 20 min)

### Task
Retrieve customer context from database and use in prompt.

```python
import sqlite3
import anthropic

client = anthropic.Anthropic()

def get_customer_context(customer_id: int) -> str:
    # TODO: Query database for customer
    # TODO: Return formatted context string
    pass

def evaluate_loan_with_context(customer_id: int, loan_amount: float):
    # TODO: Get context from database
    # TODO: Create prompt with context
    # TODO: Send to Claude
    pass

# TODO: Call evaluate_loan_with_context(1, 50000)
```

### Solution
```python
import sqlite3
import anthropic

client = anthropic.Anthropic()

def get_customer_context(customer_id: int) -> str:
    conn = sqlite3.connect("loans.db")
    cursor = conn.cursor()
    
    # Get customer
    cursor.execute("SELECT name, credit_score, income FROM customers WHERE id=?", (customer_id,))
    customer = cursor.fetchone()
    
    # Get loan history
    cursor.execute(
        "SELECT amount, status FROM loans WHERE customer_id=? ORDER BY id DESC LIMIT 5",
        (customer_id,)
    )
    loans = cursor.fetchall()
    
    conn.close()
    
    if not customer:
        return "Customer not found"
    
    name, credit_score, income = customer
    
    context = f"""
    Customer: {name}
    Credit Score: {credit_score}
    Annual Income: ${income:,.0f}
    
    Loan History:
    """
    
    for amount, status in loans:
        context += f"\n- ${amount:,.0f} ({status})"
    
    return context

def evaluate_loan_with_context(customer_id: int, loan_amount: float):
    context = get_customer_context(customer_id)
    
    prompt = f"""
    {context}
    
    Evaluate this loan application:
    Requested Amount: ${loan_amount:,.0f}
    
    Provide: decision (APPROVED/DENIED/REVIEW), score (0-100), reasoning
    """
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text

# Test
result = evaluate_loan_with_context(1, 50000)
print(result)
```

---

## Exercise 3: Context Compression (Medium, 25 min)

### Task
Compress long context to save tokens.

```python
import anthropic

client = anthropic.Anthropic()

long_document = """
[Very long document text...]
[Multiple paragraphs...]
[Lots of details...]
"""

def compress_context(text: str, max_tokens: int = 1000) -> str:
    # TODO: Summarize text to fit within token limit
    # TODO: Preserve key information
    # TODO: Return compressed version
    pass

def compare_compression():
    # TODO: Count tokens before compression
    # TODO: Compress
    # TODO: Count tokens after
    # TODO: Show savings
    pass
```

### Solution
```python
import anthropic

client = anthropic.Anthropic()

def count_tokens(text: str) -> int:
    response = client.messages.count_tokens(
        model="claude-3-5-sonnet-20241022",
        messages=[{"role": "user", "content": text}]
    )
    return response.input_tokens

def compress_context(text: str) -> str:
    """Summarize long text to key points"""
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": f"Summarize this text in 100 words, keeping only key facts:\n{text}"
        }]
    )
    return response.content[0].text

def compare_compression(text: str):
    # Count before
    before = count_tokens(text)
    
    # Compress
    compressed = compress_context(text)
    
    # Count after
    after = count_tokens(compressed)
    
    savings = ((before - after) / before) * 100
    
    print(f"Before: {before} tokens")
    print(f"After: {after} tokens")
    print(f"Savings: {savings:.1f}%")
    print(f"\nCompressed:\n{compressed}")

# Example with loan policy document
policy_doc = """
Our loan approval process follows these criteria:
1. Minimum credit score: 600
2. Maximum debt-to-income ratio: 43%
3. Minimum income: $30,000 annually
4. Employment history: At least 2 years
5. Income verification: Required documentation
6. Property appraisal: For amounts over $100,000
7. Background check: Mandatory
8. References: At least 2 professional references
9. Collateral: May be required for high-risk applicants
10. Processing time: 5-7 business days
...
[More details...]
"""

compare_compression(policy_doc)
```

---

## Exercise 4: Multi-Round Conversation Context (Hard, 30 min)

### Task
Handle growing context in multi-turn conversation.

```python
def multi_turn_conversation():
    conversation_history = []
    
    # Round 1
    user_input_1 = "I want to apply for a loan"
    # TODO: Add to history, send to Claude
    
    # Round 2
    user_input_2 = "My credit score is 720"
    # TODO: Add to history, send to Claude
    # TODO: Check token count
    
    # Round 3
    user_input_3 = "Can I get $100,000?"
    # TODO: If tokens > 150k, compress history
    # TODO: Send to Claude
    # TODO: Show final response

# TODO: Implement function
```

### Solution
```python
import anthropic

client = anthropic.Anthropic()

def multi_turn_conversation():
    conversation_history = []
    
    def send_message(user_input: str) -> str:
        nonlocal conversation_history
        
        conversation_history.append({"role": "user", "content": user_input})
        
        # Check tokens
        response = client.messages.count_tokens(
            model="claude-3-5-sonnet-20241022",
            messages=conversation_history
        )
        tokens = response.input_tokens
        print(f"Tokens: {tokens}")
        
        # Compress if needed
        if tokens > 150000:
            print("⚠️ Compressing history...")
            # Keep only recent messages
            conversation_history = conversation_history[-10:]
        
        # Get response
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=conversation_history
        )
        
        assistant_response = response.content[0].text
        conversation_history.append({"role": "assistant", "content": assistant_response})
        
        return assistant_response
    
    # Round 1
    print("Round 1:")
    response = send_message("I want to apply for a loan of $50,000")
    print(response)
    print()
    
    # Round 2
    print("Round 2:")
    response = send_message("My credit score is 720 and income is $120,000")
    print(response)
    print()
    
    # Round 3
    print("Round 3:")
    response = send_message("What are my approval chances?")
    print(response)

multi_turn_conversation()
```

---

## Exercise 5: Long Document Processing (Hard, 35 min)

### Task
Process and analyze a 50K+ token document.

```python
def process_long_document(filepath: str) -> str:
    # TODO: Read document
    # TODO: Split into chunks
    # TODO: Summarize each chunk
    # TODO: Combine summaries
    # TODO: Return final analysis
    pass
```

### Solution
```python
import anthropic

client = anthropic.Anthropic()

def chunk_text(text: str, chunk_size: int = 5000, overlap: int = 200) -> list:
    """Split text into overlapping chunks"""
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)
    return chunks

def process_long_document(filepath: str) -> str:
    # Read document
    with open(filepath, 'r') as f:
        full_text = f.read()
    
    # Split into chunks
    chunks = chunk_text(full_text)
    print(f"Processing {len(chunks)} chunks...")
    
    # Summarize each chunk
    chunk_summaries = []
    for i, chunk in enumerate(chunks):
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            messages=[{
                "role": "user",
                "content": f"Summarize this section in 100 words:\n{chunk}"
            }]
        )
        summary = response.content[0].text
        chunk_summaries.append(summary)
        print(f"  Chunk {i+1}/{len(chunks)} summarized")
    
    # Combine summaries
    all_summaries = "\n\n".join(chunk_summaries)
    
    # Final analysis
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"Based on these section summaries, provide a comprehensive analysis:\n{all_summaries}"
        }]
    )
    
    return response.content[0].text

# Test with sample document
# process_long_document("large_document.txt")
```

---

## Exercise 6: Framework Comparison (Hard, 40 min)

### Task
Implement context handling in 2+ frameworks and compare.

**Your choices:**
- [ ] Raw SDK vs LangChain
- [ ] LangChain vs LangGraph
- [ ] Any 2 frameworks you choose

Compare:
- Code complexity
- Token usage
- Response time
- Memory handling
- Which you prefer?

---

## Submission Checklist

- [ ] Exercise 1: Token counting working
- [ ] Exercise 2: Database retrieval working
- [ ] Exercise 3: Context compression working
- [ ] Exercise 4: Multi-turn conversation working
- [ ] Exercise 5: Long document processing working
- [ ] Exercise 6: Framework comparison complete
- [ ] All code runs without errors
- [ ] Understand context trade-offs

---

## Next Steps

✅ Exercises complete → Move to framework implementations (27-36)

