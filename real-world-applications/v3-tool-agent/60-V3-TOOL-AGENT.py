"""
Week 3, Version 3: Tool-Integrated Agent with RAG

Adds tool calling and retrieval augmented generation.
- Define callable tools (credit check, income verify)
- Use RAG for policy retrieval (Week 2 Pattern 1)
- Agent reasoning loop
- Real data lookups

Time to implement: 90 minutes
Lines of code: ~350
Complexity: ⭐⭐⭐ (Advanced)
"""

import anthropic
import json
from typing import Dict, List, Any
from sentence_transformers import SentenceTransformer

# ============================================================================
# WEEK 2 PATTERN 1: RAG - KNOWLEDGE BASE
# ============================================================================

class PolicyKnowledgeBase:
    """RAG system for loan policies"""
    
    def __init__(self):
        self.documents = [
            {
                "id": "policy-001",
                "title": "DTI Requirement",
                "content": "Maximum debt-to-income ratio is 43%. Calculate by dividing total monthly debt by gross monthly income."
            },
            {
                "id": "policy-002",
                "title": "Credit Score Minimum",
                "content": "Minimum credit score of 600 required for loan approval. Scores above 720 qualify for better rates."
            },
            {
                "id": "policy-003",
                "title": "Employment History",
                "content": "Minimum 2 years of employment history required. Current employment must be stable."
            },
            {
                "id": "policy-004",
                "title": "Loan Amounts",
                "content": "Loans range from $5,000 to $50,000. Amount depends on income and credit score."
            },
            {
                "id": "policy-005",
                "title": "Interest Rates",
                "content": "Rates range from 5.99% to 15.99% based on credit score. Better credit gets better rates."
            }
        ]
        
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.embeddings = self._embed_docs()
    
    def _embed_docs(self) -> Dict:
        """Embed all documents"""
        return {
            doc['id']: self.embedder.encode(doc['content'])
            for doc in self.documents
        }
    
    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        """Retrieve relevant policies (RAG Pattern 1)"""
        query_emb = self.embedder.encode(query)
        
        scores = {}
        for doc in self.documents:
            doc_emb = self.embeddings[doc['id']]
            similarity = float(query_emb.dot(doc_emb))
            scores[doc['id']] = similarity
        
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [
            next(d for d in self.documents if d['id'] == doc_id)
            for doc_id, _ in ranked[:top_k]
        ]


# ============================================================================
# TOOL DEFINITIONS
# ============================================================================

def check_credit_tool(credit_score: int) -> Dict:
    """Tool: Check if credit score meets requirements"""
    min_credit = 600
    if credit_score >= min_credit:
        rate_tier = "Prime" if credit_score >= 720 else "Standard"
        return {
            "eligible": True,
            "score": credit_score,
            "rate_tier": rate_tier,
            "message": f"Credit score {credit_score} is eligible (minimum {min_credit})"
        }
    else:
        return {
            "eligible": False,
            "score": credit_score,
            "message": f"Credit score {credit_score} is below minimum {min_credit}"
        }


def verify_income_tool(annual_income: int, requested_loan: int) -> Dict:
    """Tool: Verify income meets loan requirements"""
    monthly_income = annual_income / 12
    estimated_monthly_payment = requested_loan / 60  # 5-year loan
    
    return {
        "monthly_income": monthly_income,
        "estimated_payment": estimated_monthly_payment,
        "payment_ratio": (estimated_monthly_payment / monthly_income) * 100,
        "message": f"Monthly income: ${monthly_income:,.0f}, Estimated payment: ${estimated_monthly_payment:,.0f}"
    }


def check_employment_tool(years_employed: int) -> Dict:
    """Tool: Verify employment history"""
    min_years = 2
    eligible = years_employed >= min_years
    
    return {
        "eligible": eligible,
        "years": years_employed,
        "message": f"Employment history: {years_employed} years (minimum {min_years} required)"
    }


TOOLS = {
    "check_credit": check_credit_tool,
    "verify_income": verify_income_tool,
    "check_employment": check_employment_tool
}


# ============================================================================
# LOAN EVALUATION SYSTEM - V3: TOOL AGENT
# ============================================================================

class LoanEvaluationV3:
    """Loan evaluation with tool calling and RAG"""
    
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"
        self.kb = PolicyKnowledgeBase()
        self.tool_calls = []
        self.decision = None
    
    def evaluate_loan(self, customer: Dict) -> Dict:
        """Evaluate loan using tool calling"""
        
        # Step 1: Retrieve relevant policies (RAG)
        policies = self.kb.retrieve(
            f"Evaluate loan for credit {customer['credit_score']} income {customer['income']}"
        )
        policies_text = "\n".join([f"- {p['title']}: {p['content']}" for p in policies])
        
        # Step 2: Build initial prompt
        prompt = f"""
You are a loan officer with access to tools. Evaluate this loan application.

APPLICANT:
- Name: {customer['name']}
- Credit score: {customer['credit_score']}
- Annual income: ${customer['income']:,}
- Years employed: {customer['employment_years']}
- Requested loan: ${customer.get('loan_amount', 25000):,}

RELEVANT POLICIES:
{policies_text}

AVAILABLE TOOLS:
1. check_credit(credit_score) - Verify credit score eligibility
2. verify_income(annual_income, requested_loan) - Check income sufficiency
3. check_employment(years_employed) - Verify employment history

TASK:
1. Use tools to check all three criteria
2. Based on tool results, make an APPROVE or DENY decision
3. Provide reasoning for your decision

Use tools first, then decide.
"""
        
        # Step 3: Agent loop with tool calling
        messages = [{"role": "user", "content": prompt}]
        
        max_iterations = 5
        for iteration in range(max_iterations):
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=messages
            )
            
            # Check if Claude wants to use tools
            response_text = response.content[0].text
            
            # Parse tool calls from response (simple pattern matching)
            # In production, use proper tool_use blocks
            tool_results = []
            
            if "check_credit" in response_text:
                result = check_credit_tool(customer['credit_score'])
                tool_results.append(f"Credit check: {result['message']}")
                self.tool_calls.append("check_credit")
            
            if "verify_income" in response_text:
                result = verify_income_tool(
                    customer['income'],
                    customer.get('loan_amount', 25000)
                )
                tool_results.append(f"Income verification: {result['message']}")
                self.tool_calls.append("verify_income")
            
            if "check_employment" in response_text:
                result = check_employment_tool(customer['employment_years'])
                tool_results.append(f"Employment check: {result['message']}")
                self.tool_calls.append("check_employment")
            
            # If no tools called or decision reached, stop
            if not tool_results or "APPROVE" in response_text or "DENY" in response_text:
                break
            
            # Add tool results to conversation
            messages.append({"role": "assistant", "content": response_text})
            tool_summary = "\n".join(tool_results)
            messages.append({
                "role": "user",
                "content": f"Tool results:\n{tool_summary}\n\nNow make your final decision."
            })
        
        # Extract final decision
        final_response = response_text
        if "APPROVE" in final_response.upper():
            self.decision = "APPROVE"
        elif "DENY" in final_response.upper():
            self.decision = "DENY"
        else:
            self.decision = "REVIEW"
        
        return {
            "customer": customer['name'],
            "decision": self.decision,
            "explanation": final_response[:300],
            "tools_used": self.tool_calls,
            "policies_referenced": len(policies),
            "iterations": iteration + 1
        }


# ============================================================================
# TEST
# ============================================================================

def main():
    print("="*80)
    print("WEEK 3, VERSION 3: TOOL-INTEGRATED AGENT WITH RAG")
    print("="*80)
    print()
    
    test_customers = [
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
        }
    ]
    
    system = LoanEvaluationV3()
    
    results = []
    for customer in test_customers:
        print(f"Evaluating: {customer['name']}")
        result = system.evaluate_loan(customer)
        results.append(result)
        
        print(f"  Decision: {result['decision']}")
        print(f"  Tools used: {result['tools_used']}")
        print(f"  Policies referenced: {result['policies_referenced']}")
        print()
    
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total evaluations: {len(results)}")
    print(f"Approvals: {sum(1 for r in results if r['decision'] == 'APPROVE')}")
    print(f"Denials: {sum(1 for r in results if r['decision'] == 'DENY')}")
    print()
    print("✅ V3 Tool Agent Complete!")


if __name__ == "__main__":
    main()

