"""
Framework 27: Raw SDK - Manual Context Management
Showing: Explicit control over context, token counting, compression
Best for: Learning, understanding internals, maximum control
"""

import anthropic
import sqlite3

client = anthropic.Anthropic()

# ============================================================================
# Strategy 1: Simple Inline Context
# ============================================================================

def evaluate_loan_inline_context(customer_id: int, loan_amount: float) -> str:
    """Most basic: context directly in message"""
    
    # Build context
    context = f"Customer ID: {customer_id}, Loan Amount: ${loan_amount:,.0f}"
    
    # Create message with context
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=512,
        messages=[{
            "role": "user",
            "content": f"{context}\n\nEvaluate this loan application."
        }]
    )
    
    return response.content[0].text


# ============================================================================
# Strategy 2: Database Retrieval + Inline Context
# ============================================================================

def get_customer_context(customer_id: int) -> dict:
    """Query database for customer information"""
    
    conn = sqlite3.connect("loans.db")
    cursor = conn.cursor()
    
    # Get customer
    cursor.execute(
        "SELECT name, credit_score, income FROM customers WHERE id=?",
        (customer_id,)
    )
    customer_row = cursor.fetchone()
    
    if not customer_row:
        conn.close()
        return {}
    
    name, credit_score, income = customer_row
    
    # Get loan history
    cursor.execute(
        "SELECT amount, status FROM loans WHERE customer_id=? ORDER BY id DESC LIMIT 5",
        (customer_id,)
    )
    loans = cursor.fetchall()
    
    conn.close()
    
    return {
        "name": name,
        "credit_score": credit_score,
        "income": income,
        "loans": loans
    }


def evaluate_loan_with_db_context(customer_id: int, loan_amount: float) -> str:
    """Pull context from database"""
    
    # Get context from database
    customer_context = get_customer_context(customer_id)
    
    if not customer_context:
        return "Customer not found"
    
    # Format context
    context = f"""
    Customer: {customer_context['name']}
    Credit Score: {customer_context['credit_score']}
    Annual Income: ${customer_context['income']:,.0f}
    
    Loan History:
    """
    
    for amount, status in customer_context['loans']:
        context += f"\n    - ${amount:,.0f} ({status})"
    
    # Create message
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=512,
        messages=[{
            "role": "user",
            "content": f"""
            {context}
            
            New Loan Request: ${loan_amount:,.0f}
            
            Evaluate and provide: decision, confidence score, key reasoning
            """
        }]
    )
    
    return response.content[0].text


# ============================================================================
# Strategy 3: Token Counting + Compression
# ============================================================================

def count_tokens(messages: list) -> int:
    """Count tokens before sending"""
    response = client.messages.count_tokens(
        model="claude-3-5-sonnet-20241022",
        messages=messages
    )
    return response.input_tokens


def compress_context(long_text: str, max_tokens: int = 500) -> str:
    """Compress large context to save tokens"""
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=300,
        messages=[{
            "role": "user",
            "content": f"Summarize this in key points only, under 100 words:\n{long_text}"
        }]
    )
    
    return response.content[0].text


def evaluate_loan_compressed(customer_id: int, loan_amount: float) -> dict:
    """Token-aware context handling"""
    
    customer_context = get_customer_context(customer_id)
    if not customer_context:
        return {"error": "Customer not found"}
    
    # Format context
    context = f"""
    Customer: {customer_context['name']}
    Credit Score: {customer_context['credit_score']}
    Income: ${customer_context['income']:,.0f}
    Loans: {len(customer_context['loans'])} previous
    """
    
    # Build message
    messages = [{
        "role": "user",
        "content": f"{context}\n\nEvaluate ${loan_amount:,.0f} loan"
    }]
    
    # Count tokens
    tokens = count_tokens(messages)
    compressed = False
    
    # Compress if too large
    if tokens > 4000:  # Arbitrary threshold
        compressed_context = compress_context(context)
        messages = [{
            "role": "user",
            "content": f"{compressed_context}\n\nEvaluate ${loan_amount:,.0f} loan"
        }]
        tokens = count_tokens(messages)
        compressed = True
    
    # Get response
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=512,
        messages=messages
    )
    
    return {
        "tokens_used": tokens,
        "compressed": compressed,
        "result": response.content[0].text
    }


# ============================================================================
# Strategy 4: Multi-Turn with Context Growth Management
# ============================================================================

class RawSDKConversation:
    """Manage multi-turn conversation with context awareness"""
    
    def __init__(self, max_context_tokens: int = 150000):
        self.messages = []
        self.max_context_tokens = max_context_tokens
        self.system_prompt = """
        You are a loan officer assistant.
        Help customers understand their loan options and provide guidance.
        """
    
    def add_user_message(self, content: str):
        """Add user message and check context size"""
        self.messages.append({"role": "user", "content": content})
        
        # Check context size
        tokens = count_tokens(self.messages)
        print(f"Current tokens: {tokens}")
        
        if tokens > self.max_context_tokens * 0.9:  # 90% threshold
            print("⚠️ Warning: Context getting large, trimming...")
            # Keep only recent messages
            self.messages = self.messages[-20:]
    
    def get_response(self) -> str:
        """Get Claude response"""
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=self.system_prompt,
            messages=self.messages
        )
        
        assistant_message = response.content[0].text
        self.messages.append({"role": "assistant", "content": assistant_message})
        
        return assistant_message


# ============================================================================
# Strategy 5: Context from Multiple Sources
# ============================================================================

def evaluate_with_multi_source_context(customer_id: int, loan_amount: float) -> str:
    """Combine context from multiple sources"""
    
    customer_context = get_customer_context(customer_id)
    
    # Source 1: Customer data
    customer_context_str = f"""
    Customer: {customer_context['name']}
    Credit: {customer_context['credit_score']}
    Income: ${customer_context['income']:,.0f}
    """
    
    # Source 2: Hardcoded policies
    policies_context = """
    Loan Policies:
    - Min credit: 600
    - Max DTI: 43%
    - Min income: $30,000
    """
    
    # Source 3: Market data (simulated)
    market_context = """
    Market Rates Today:
    - 30yr Fixed: 6.5%
    - 15yr Fixed: 6.0%
    - ARM: 5.8%
    """
    
    # Combine all context
    full_context = f"""
    {customer_context_str}
    
    {policies_context}
    
    {market_context}
    
    Requested Loan: ${loan_amount:,.0f}
    """
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"{full_context}\n\nProvide recommendation with rates"
        }]
    )
    
    return response.content[0].text


# ============================================================================
# Usage Examples
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("RAW SDK - Context Handling Examples")
    print("=" * 70)
    
    # Example 1: Simple inline
    print("\n1. Simple Inline Context:")
    result = evaluate_loan_inline_context(1, 50000)
    print(result[:200])
    
    # Example 2: Database retrieval
    print("\n2. Database Retrieval:")
    result = evaluate_loan_with_db_context(1, 50000)
    print(result[:200])
    
    # Example 3: Token-aware with compression
    print("\n3. Token Counting & Compression:")
    result = evaluate_loan_compressed(1, 50000)
    print(f"   Tokens: {result['tokens_used']}, Compressed: {result['compressed']}")
    print(f"   Result: {result['result'][:100]}")
    
    # Example 4: Multi-turn conversation
    print("\n4. Multi-Turn Conversation:")
    conversation = RawSDKConversation()
    
    conversation.add_user_message("Hi, I'm looking for a loan")
    response1 = conversation.get_response()
    print(f"   {response1[:100]}")
    
    conversation.add_user_message("My credit score is 720")
    response2 = conversation.get_response()
    print(f"   {response2[:100]}")
    
    # Example 5: Multi-source context
    print("\n5. Multi-Source Context:")
    result = evaluate_with_multi_source_context(1, 100000)
    print(result[:200])

