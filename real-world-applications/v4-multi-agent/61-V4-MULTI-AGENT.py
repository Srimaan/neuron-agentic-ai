"""
Week 3, Version 4: Multi-Agent System

Multiple specialized agents evaluate different aspects:
- Policy Agent: Checks eligibility rules
- Risk Agent: Calculates risk score
- Decision Agent: Makes final approval

Agents communicate and reach consensus.

Time to implement: 120 minutes
Lines of code: ~400
Complexity: ⭐⭐⭐⭐ (Expert)
"""

import anthropic
from typing import Dict, List
import json

# ============================================================================
# SPECIALIZED AGENTS
# ============================================================================

class PolicyAgent:
    """Evaluates against loan policies"""
    
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"
        self.name = "Policy Agent"
    
    def evaluate(self, customer: Dict) -> Dict:
        """Check policy compliance"""
        
        prompt = f"""
You are a policy compliance expert.

APPLICANT:
- Credit score: {customer['credit_score']}
- Income: ${customer['income']:,}
- Employment: {customer['employment_years']} years

POLICIES:
- Min credit: 600
- Min employment: 2 years
- Max loan: $50,000
- Min loan: $5,000

TASK: List which policies are met and which are violated.
Be concise. Return JSON with: met_policies (list), violated_policies (list), eligible (bool)
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result_text = response.content[0].text
        
        # Parse result
        return {
            "agent": self.name,
            "evaluation": result_text,
            "eligible": "eligible: true" in result_text.lower() or "met all" in result_text.lower()
        }


class RiskAgent:
    """Calculates risk score"""
    
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"
        self.name = "Risk Agent"
    
    def evaluate(self, customer: Dict) -> Dict:
        """Calculate risk score (0-100, higher = riskier)"""
        
        prompt = f"""
You are a credit risk analyst.

APPLICANT:
- Credit score: {customer['credit_score']}
- Income: ${customer['income']:,}
- Employment: {customer['employment_years']} years
- Requested loan: ${customer.get('loan_amount', 25000):,}

TASK: Calculate risk score (0-100).
- 0-30: Low risk (approve)
- 31-60: Medium risk (review)
- 61-100: High risk (deny)

Consider: Credit score (weight: 40%), Income stability (30%), Employment (20%), Loan amount (10%)

Return JSON: {"risk_score": <0-100>, "risk_level": "<low|medium|high>", "reasoning": "..."}
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result_text = response.content[0].text
        
        # Extract risk level
        risk_level = "medium"
        if "low risk" in result_text.lower():
            risk_level = "low"
        elif "high risk" in result_text.lower():
            risk_level = "high"
        
        return {
            "agent": self.name,
            "evaluation": result_text,
            "risk_level": risk_level
        }


class DecisionAgent:
    """Makes final approval decision"""
    
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"
        self.name = "Decision Agent"
    
    def decide(
        self,
        policy_evaluation: Dict,
        risk_evaluation: Dict,
        customer: Dict
    ) -> Dict:
        """Make final decision based on other agents"""
        
        prompt = f"""
You are the final decision maker.

CUSTOMER: {customer['name']}

POLICY AGENT REPORT:
{policy_evaluation['evaluation']}

RISK AGENT REPORT:
{risk_evaluation['evaluation']}

TASK: Make a final decision: APPROVE, DENY, or REFER
Consider both reports. Policy violations = automatic DENY.
Low risk + policy compliant = APPROVE.
Medium risk = REFER for manual review.

Provide: Decision, reasoning, conditions (if approved)
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result_text = response.content[0].text
        
        # Extract decision
        if "APPROVE" in result_text.upper():
            decision = "APPROVE"
        elif "DENY" in result_text.upper():
            decision = "DENY"
        else:
            decision = "REFER"
        
        return {
            "agent": self.name,
            "decision": decision,
            "reasoning": result_text
        }


# ============================================================================
# ORCHESTRATOR
# ============================================================================

class LoanEvaluationV4:
    """Multi-agent orchestration"""
    
    def __init__(self):
        self.policy_agent = PolicyAgent()
        self.risk_agent = RiskAgent()
        self.decision_agent = DecisionAgent()
    
    def evaluate_loan(self, customer: Dict) -> Dict:
        """Orchestrate multi-agent evaluation"""
        
        print(f"\n{'='*60}")
        print(f"Evaluating: {customer['name']}")
        print(f"{'='*60}")
        
        # Step 1: Policy evaluation
        print("\n[Policy Agent] Evaluating policies...")
        policy_result = self.policy_agent.evaluate(customer)
        print(f"  Result: {policy_result['eligible']}")
        
        # Step 2: Risk evaluation
        print("[Risk Agent] Calculating risk...")
        risk_result = self.risk_agent.evaluate(customer)
        print(f"  Risk level: {risk_result['risk_level']}")
        
        # Step 3: Final decision
        print("[Decision Agent] Making final decision...")
        decision_result = self.decision_agent.decide(
            policy_result,
            risk_result,
            customer
        )
        print(f"  Decision: {decision_result['decision']}")
        
        return {
            "customer": customer['name'],
            "policy_evaluation": policy_result,
            "risk_evaluation": risk_result,
            "final_decision": decision_result['decision'],
            "reasoning": decision_result['reasoning'],
            "agents_involved": 3
        }


# ============================================================================
# TEST
# ============================================================================

def main():
    print("="*80)
    print("WEEK 3, VERSION 4: MULTI-AGENT SYSTEM")
    print("="*80)
    
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
        },
        {
            "name": "Carol White",
            "credit_score": 680,
            "income": 80000,
            "employment_years": 3,
            "loan_amount": 15000
        }
    ]
    
    system = LoanEvaluationV4()
    results = []
    
    for customer in test_customers:
        result = system.evaluate_loan(customer)
        results.append(result)
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total evaluations: {len(results)}")
    print(f"Approvals: {sum(1 for r in results if r['final_decision'] == 'APPROVE')}")
    print(f"Denials: {sum(1 for r in results if r['final_decision'] == 'DENY')}")
    print(f"Referrals: {sum(1 for r in results if r['final_decision'] == 'REFER')}")
    print()
    print("✅ V4 Multi-Agent Complete!")
    
    return results


if __name__ == "__main__":
    main()

