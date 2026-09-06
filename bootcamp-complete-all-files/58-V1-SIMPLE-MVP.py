"""
Week 3, Version 1: Simple Loan Evaluation MVP

The simplest possible loan evaluation system.
- Single prompt to Claude
- No memory, no tools, no complexity
- Just ask a question, get a decision
- Perfect starting point

Time to implement: 30 minutes
Lines of code: ~150
Complexity: ⭐ (Beginner)
"""

import anthropic
import json
from typing import Dict

# Initialize Anthropic client
client = anthropic.Anthropic()

# ============================================================================
# LOAN EVALUATION SYSTEM - V1: SIMPLE MVP
# ============================================================================

class LoanEvaluationV1:
    """Simplest possible loan evaluation system"""
    
    def __init__(self):
        self.model = "claude-3-5-sonnet-20241022"
        self.max_tokens = 1024
    
    def evaluate_loan(self, customer: Dict) -> Dict:
        """
        Evaluate a loan application using a single prompt to Claude.
        
        Args:
            customer: Dict with keys: name, credit_score, income, employment_years, loan_amount
        
        Returns:
            Dict with decision and explanation
        """
        
        # Build the prompt
        prompt = self._build_prompt(customer)
        
        # Call Claude
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        # Extract response
        decision_text = response.content[0].text
        
        # Parse decision
        decision = self._parse_decision(decision_text)
        
        return {
            "customer": customer["name"],
            "decision": decision,
            "explanation": decision_text,
            "model": self.model,
            "tokens_used": response.usage.input_tokens + response.usage.output_tokens
        }
    
    def _build_prompt(self, customer: Dict) -> str:
        """Build the evaluation prompt"""
        
        return f"""
You are a loan officer evaluating a loan application.

LOAN APPROVAL CRITERIA:
- Minimum credit score: 600
- Maximum debt-to-income ratio: 43%
- Minimum employment history: 2 years
- Loan amount: $5,000 - $50,000

APPLICANT INFORMATION:
- Name: {customer['name']}
- Credit score: {customer['credit_score']}
- Annual income: ${customer['income']:,}
- Years employed: {customer['employment_years']}
- Requested loan amount: ${customer['loan_amount']:,}

TASK:
1. Check if applicant meets eligibility criteria
2. Calculate debt-to-income ratio (use $300/month estimate for loan payment)
3. Make an APPROVE or DENY decision
4. Provide a brief explanation

Be concise and professional.
"""
    
    def _parse_decision(self, response_text: str) -> str:
        """Extract APPROVE or DENY from response"""
        if "APPROVE" in response_text.upper():
            return "APPROVE"
        elif "DENY" in response_text.upper():
            return "DENY"
        else:
            return "REVIEW"  # Need manual review


# ============================================================================
# TEST DATA
# ============================================================================

TEST_CUSTOMERS = [
    {
        "name": "Alice Johnson",
        "credit_score": 750,
        "income": 150000,
        "employment_years": 5,
        "loan_amount": 25000
    },
    {
        "name": "Bob Smith",
        "credit_score": 580,
        "income": 50000,
        "employment_years": 1,
        "loan_amount": 30000
    },
    {
        "name": "Carol White",
        "credit_score": 680,
        "income": 80000,
        "employment_years": 3,
        "loan_amount": 15000
    }
]


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("="*80)
    print("WEEK 3, VERSION 1: SIMPLE LOAN EVALUATION MVP")
    print("="*80)
    print()
    
    # Initialize system
    system = LoanEvaluationV1()
    
    # Evaluate each customer
    results = []
    
    for customer in TEST_CUSTOMERS:
        print(f"Evaluating: {customer['name']}")
        print(f"  Credit score: {customer['credit_score']}")
        print(f"  Income: ${customer['income']:,}")
        print(f"  Employment: {customer['employment_years']} years")
        print(f"  Loan amount: ${customer['loan_amount']:,}")
        print()
        
        # Evaluate
        result = system.evaluate_loan(customer)
        results.append(result)
        
        # Show decision
        print(f"  DECISION: {result['decision']}")
        print(f"  Explanation: {result['explanation'][:200]}...")
        print()
        print("-"*80)
        print()
    
    # Summary
    print()
    print("="*80)
    print("SUMMARY")
    print("="*80)
    approvals = sum(1 for r in results if r['decision'] == 'APPROVE')
    denials = sum(1 for r in results if r['decision'] == 'DENY')
    
    print(f"Total applications: {len(results)}")
    print(f"Approvals: {approvals}")
    print(f"Denials: {denials}")
    print(f"Average tokens per decision: {sum(r['tokens_used'] for r in results) // len(results)}")
    print()
    print("✅ V1 Simple MVP Complete!")
    print()
    
    return results


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    results = main()
    
    # Save results
    with open("/mnt/user-data/outputs/v1_results.json", "w") as f:
        # Convert to serializable format
        for result in results:
            result.pop('explanation')  # Remove long text for JSON
        json.dump(results, f, indent=2)
    
    print("Results saved to: v1_results.json")

