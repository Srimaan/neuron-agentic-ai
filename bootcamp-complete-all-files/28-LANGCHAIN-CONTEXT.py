"""
Framework 28: LangChain - Built-in Memory & Context
Showing: Conversation chains, memory types, automatic context management
Best for: Quick apps, simple context handling, memory persistence
"""

from langchain_anthropic import ChatAnthropic
from langchain.memory import (
    ConversationBufferMemory,
    ConversationSummaryMemory,
    ConversationBufferWindowMemory
)
from langchain.chains import ConversationChain, LLMChain
from langchain.prompts import PromptTemplate
import sqlite3

llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")

# ============================================================================
# Strategy 1: Simple Conversation with Buffer Memory
# ============================================================================

def simple_loan_conversation():
    """Basic conversation with automatic memory"""
    
    memory = ConversationBufferMemory(human_prefix="Customer", ai_prefix="Officer")
    
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=False
    )
    
    # Turn 1
    response1 = conversation.predict(input="Hi, I want to apply for a loan")
    print(f"Officer: {response1}")
    
    # Turn 2 - Memory is automatic
    response2 = conversation.predict(input="My credit score is 720")
    print(f"Officer: {response2}")
    
    # Turn 3 - Can access full history
    response3 = conversation.predict(input="How much can I borrow?")
    print(f"Officer: {response3}")
    
    # View memory
    print(f"\nConversation History:\n{memory.buffer}")


# ============================================================================
# Strategy 2: Context Window Management
# ============================================================================

def conversation_with_window():
    """Keep only recent N turns to manage context"""
    
    memory = ConversationBufferWindowMemory(
        k=5,  # Keep only last 5 exchanges
        human_prefix="Customer",
        ai_prefix="Officer"
    )
    
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=False
    )
    
    # Multiple turns - old ones will be dropped
    for i in range(10):
        user_input = f"Turn {i+1}: Can I get $50,000?"
        response = conversation.predict(input=user_input)
        print(f"Turn {i+1} - Tokens in memory: ~{len(memory.buffer) // 4}")
    
    print(f"\nFinal Memory (only last 5 turns):\n{memory.buffer}")


# ============================================================================
# Strategy 3: Summary Memory (Auto-Compression)
# ============================================================================

def conversation_with_summary():
    """Automatically summarize old context"""
    
    memory = ConversationSummaryMemory(
        llm=llm,
        human_prefix="Customer",
        ai_prefix="Officer"
    )
    
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=False
    )
    
    # Many turns
    turns = [
        "I'm looking for a mortgage",
        "My credit score is 750",
        "My annual income is $150,000",
        "I want to borrow $400,000",
        "I have 20% down payment",
        "What about closing costs?",
    ]
    
    for turn in turns:
        response = conversation.predict(input=turn)
        print(f"Officer: {response[:50]}...")
    
    print(f"\nSummary of Conversation:\n{memory.buffer}")


# ============================================================================
# Strategy 4: Custom Context with Prompt Template
# ============================================================================

def custom_context_template():
    """Use custom prompts with injected context"""
    
    # Get customer context from database
    conn = sqlite3.connect("loans.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, credit_score, income FROM customers WHERE id=1")
    customer = cursor.fetchone()
    conn.close()
    
    if not customer:
        return
    
    name, credit_score, income = customer
    
    # Custom template with context
    template = """
    You are a loan officer. Here is customer context:
    
    Customer: {customer_name}
    Credit Score: {credit_score}
    Annual Income: ${income:,}
    
    Respond to this question or statement:
    {{input}}
    
    Provide helpful guidance based on their profile.
    """
    
    prompt = PromptTemplate(
        input_variables=["customer_name", "credit_score", "income", "input"],
        template=template
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    response = chain.run(
        customer_name=name,
        credit_score=credit_score,
        income=income,
        input="How much can I borrow?"
    )
    
    print(response)


# ============================================================================
# Strategy 5: Multi-Memory for Different Contexts
# ============================================================================

class LoanApplicationManager:
    """Manage multiple concurrent conversations"""
    
    def __init__(self):
        self.conversations = {}
    
    def start_conversation(self, customer_id: int):
        """Start new conversation for customer"""
        memory = ConversationBufferMemory(
            human_prefix=f"Customer {customer_id}",
            ai_prefix="Officer"
        )
        
        self.conversations[customer_id] = ConversationChain(
            llm=llm,
            memory=memory,
            verbose=False
        )
    
    def send_message(self, customer_id: int, message: str) -> str:
        """Send message to specific customer's conversation"""
        if customer_id not in self.conversations:
            self.start_conversation(customer_id)
        
        response = self.conversations[customer_id].predict(input=message)
        return response
    
    def get_context(self, customer_id: int) -> str:
        """Get full conversation context for customer"""
        if customer_id not in self.conversations:
            return "No conversation found"
        
        return self.conversations[customer_id].memory.buffer


# ============================================================================
# Strategy 6: Database Integration
# ============================================================================

def conversation_with_db_context():
    """Pull fresh context from database each turn"""
    
    def get_updated_context(customer_id: int) -> str:
        """Fetch latest customer data"""
        conn = sqlite3.connect("loans.db")
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT name, credit_score, income FROM customers WHERE id=?",
            (customer_id,)
        )
        customer = cursor.fetchone()
        
        cursor.execute(
            "SELECT amount, status FROM loans WHERE customer_id=? LIMIT 3",
            (customer_id,)
        )
        loans = cursor.fetchall()
        conn.close()
        
        if not customer:
            return ""
        
        context = f"Customer: {customer[0]}, Credit: {customer[1]}, Income: ${customer[2]:,}\n"
        context += "Recent loans: "
        for amount, status in loans:
            context += f"${amount:,} ({status}), "
        
        return context
    
    # Custom prompt that refreshes context
    template = """
    Context: {customer_context}
    
    {{input}}
    
    Based on the customer profile above, provide guidance.
    """
    
    prompt = PromptTemplate(
        input_variables=["customer_context", "input"],
        template=template
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # Each turn refreshes context
    for turn in range(3):
        customer_context = get_updated_context(1)
        response = chain.run(
            customer_context=customer_context,
            input=f"Turn {turn+1}: What should I do about my loan options?"
        )
        print(f"Turn {turn+1}: {response[:100]}...\n")


# ============================================================================
# Usage Examples
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("LANGCHAIN - Context Handling Examples")
    print("=" * 70)
    
    print("\n1. Simple Conversation with Buffer Memory:")
    print("-" * 70)
    # simple_loan_conversation()  # Uncomment to run
    
    print("\n2. Conversation with Window Memory (last 5 turns):")
    print("-" * 70)
    # conversation_with_window()  # Uncomment to run
    
    print("\n3. Conversation with Summary Memory (auto-compression):")
    print("-" * 70)
    # conversation_with_summary()  # Uncomment to run
    
    print("\n4. Custom Context Template:")
    print("-" * 70)
    # custom_context_template()  # Uncomment to run
    
    print("\n5. Multiple Conversations with Memory Manager:")
    print("-" * 70)
    manager = LoanApplicationManager()
    manager.start_conversation(1)
    r1 = manager.send_message(1, "I need a loan")
    print(f"Response: {r1[:50]}...")
    r2 = manager.send_message(1, "My credit is 720")
    print(f"Response: {r2[:50]}...")
    
    print("\n6. Database Integration with Fresh Context:")
    print("-" * 70)
    # conversation_with_db_context()  # Uncomment to run

