"""
Week 3, Version 2: Multi-Turn Conversation with Context Windowing

Adds conversation memory using Week 2 Pattern 2 (Context Windowing).
- Remember conversation history
- Manage tokens efficiently
- Compress old context with summarization

Time to implement: 60 minutes
Lines of code: ~250
Complexity: ⭐⭐ (Intermediate)
"""

import anthropic
import json
from datetime import datetime
from typing import Dict, List

# ============================================================================
# WEEK 2 PATTERN 2: CONTEXT WINDOWING
# ============================================================================

class ConversationWindow:
    """Manage conversation with automatic summarization"""
    
    def __init__(self, max_recent: int = 10):
        self.max_recent = max_recent
        self.turns = []
        self.summary = ""
        self.client = anthropic.Anthropic()
    
    def add(self, user: str, assistant: str):
        """Add turn and compress if needed"""
        self.turns.append({
            "user": user,
            "assistant": assistant,
            "timestamp": datetime.now().isoformat()
        })
        
        if len(self.turns) > self.max_recent * 2:
            self._compress()
    
    def _compress(self):
        """Summarize old turns"""
        old_turns = self.turns[:-self.max_recent]
        text = "\n".join([
            f"Customer: {t['user']}\nLoan Officer: {t['assistant']}"
            for t in old_turns
        ])
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            messages=[{
                "role": "user",
                "content": f"Summarize this loan discussion in 100 words:\n{text}"
            }]
        )
        
        self.summary = response.content[0].text
        self.turns = self.turns[-self.max_recent:]
    
    def get_context(self) -> str:
        """Get full context for Claude"""
        ctx = ""
        if self.summary:
            ctx += f"EARLIER DISCUSSION SUMMARY:\n{self.summary}\n\n"
        
        ctx += "RECENT CONVERSATION:\n"
        for t in self.turns:
            ctx += f"Customer: {t['user']}\n"
            ctx += f"Loan Officer: {t['assistant']}\n\n"
        
        return ctx


# ============================================================================
# LOAN EVALUATION SYSTEM - V2: MULTI-TURN
# ============================================================================

class LoanEvaluationV2:
    """Loan evaluation with conversation memory"""
    
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"
        self.window = ConversationWindow(max_recent=10)
        self.customer_data = None
        self.decision = None
    
    def start_conversation(self, customer: Dict) -> str:
        """Start conversation with customer"""
        self.customer_data = customer
        
        initial_prompt = f"""
You are a friendly loan officer evaluating a loan application.

APPLICANT INFORMATION:
- Name: {customer['name']}
- Credit score: {customer['credit_score']}
- Annual income: ${customer['income']:,}
- Years employed: {customer['employment_years']}

APPROVAL CRITERIA:
- Minimum credit score: 600
- Maximum DTI: 43%
- Minimum employment: 2 years
- Loan amount: $5,000 - $50,000

Greet the customer and ask about their loan needs.
Be conversational and helpful. This is the first message.
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": initial_prompt}]
        )
        
        greeting = response.content[0].text
        self.window.add("(Starting conversation)", greeting)
        
        return greeting
    
    def respond_to_customer(self, customer_message: str) -> str:
        """Process customer message and respond"""
        
        # Build context with conversation history
        conversation_context = self.window.get_context()
        
        prompt = f"""
You are a loan officer. The conversation so far:

{conversation_context}

Customer just said: {customer_message}

APPROVAL CRITERIA:
- Minimum credit score: 600
- Maximum DTI: 43%
- Minimum employment: 2 years
- Loan amount: $5,000 - $50,000

APPLICANT: {self.customer_data['name']}
- Credit: {self.customer_data['credit_score']}
- Income: ${self.customer_data['income']:,}
- Employment: {self.customer_data['employment_years']} years

Respond conversationally. Ask clarifying questions as needed.
If you have enough info, evaluate and provide a decision.
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        
        assistant_message = response.content[0].text
        self.window.add(customer_message, assistant_message)
        
        # Check if decision made
        if "APPROVE" in assistant_message.upper() or "DENY" in assistant_message.upper():
            self._extract_decision(assistant_message)
        
        return assistant_message
    
    def _extract_decision(self, response_text: str):
        """Extract decision from response"""
        if "APPROVE" in response_text.upper():
            self.decision = "APPROVE"
        elif "DENY" in response_text.upper():
            self.decision = "DENY"
        else:
            self.decision = "REVIEW"
    
    def get_conversation_stats(self) -> Dict:
        """Get conversation statistics"""
        return {
            "turns": len(self.turns),
            "has_summary": bool(self.window.summary),
            "decision": self.decision,
            "conversation_length": len(self.window.get_context())
        }
    
    @property
    def turns(self) -> List:
        """Get conversation turns"""
        return self.window.turns


# ============================================================================
# INTERACTIVE CONVERSATION
# ============================================================================

def run_conversation():
    """Run a multi-turn conversation"""
    
    print("="*80)
    print("WEEK 3, VERSION 2: MULTI-TURN CONVERSATION WITH WINDOWING")
    print("="*80)
    print()
    
    customer = {
        "name": "John Smith",
        "credit_score": 680,
        "income": 80000,
        "employment_years": 3
    }
    
    system = LoanEvaluationV2()
    
    # Start conversation
    print(f"Starting conversation with {customer['name']}...\n")
    greeting = system.start_conversation(customer)
    print(f"Loan Officer: {greeting}\n")
    
    # Multi-turn conversation
    customer_inputs = [
        "Hi, I'm looking to borrow $20,000 for home improvements.",
        "I've been working at TechCorp for 3 years now.",
        "My credit score is 680. Will that be a problem?",
        "My annual salary is around $80,000. Is that enough?",
        "Yes, I can make monthly payments. What would the rate be?",
        "So am I approved?"
    ]
    
    for i, customer_input in enumerate(customer_inputs, 1):
        print(f"Turn {i}:")
        print(f"Customer: {customer_input}")
        
        response = system.respond_to_customer(customer_input)
        print(f"Loan Officer: {response[:200]}...")
        print()
        
        # Show stats periodically
        if i % 3 == 0:
            stats = system.get_conversation_stats()
            print(f"Stats: {stats['turns']} turns, Summary: {stats['has_summary']}")
            print()
        
        if system.decision:
            print(f"\n✅ DECISION: {system.decision}")
            break
    
    # Summary
    print("\n" + "="*80)
    print("CONVERSATION SUMMARY")
    print("="*80)
    print(f"Turns: {len(system.turns)}")
    print(f"Summary used: {bool(system.window.summary)}")
    print(f"Final decision: {system.decision}")
    print(f"Context length: {len(system.window.get_context())} chars")
    print()
    print("✅ V2 Multi-Turn Complete!")
    
    return system


# ============================================================================
# COMPARISON WITH V1
# ============================================================================

def show_comparison():
    """Show V1 vs V2 comparison"""
    print("\n" + "="*80)
    print("V1 vs V2 COMPARISON")
    print("="*80)
    print("""
V1 (Simple MVP):
- Single prompt, no memory
- All customer info in one message
- No token optimization
- Decision in one turn

V2 (Multi-Turn):
- Conversation memory
- Windowing for token efficiency
- Summarization of old context
- Multiple turns possible
- More natural interaction
- Better for complex decisions

Key V2 Features:
✅ Pattern 2: Context Windowing
✅ Summarization for efficiency
✅ Multi-turn conversation
✅ Natural dialogue flow
✅ Token optimization
""")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    system = run_conversation()
    show_comparison()
    
    # Save conversation
    with open("/mnt/user-data/outputs/v2_conversation.json", "w") as f:
        json.dump({
            "turns": len(system.turns),
            "decision": system.decision,
            "has_summary": bool(system.window.summary)
        }, f, indent=2)
    
    print("Conversation saved to: v2_conversation.json")

