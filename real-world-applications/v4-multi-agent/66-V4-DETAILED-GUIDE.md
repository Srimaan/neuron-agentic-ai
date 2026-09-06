# V4 Build Guide: Multi-Agent System

## Overview
**What:** Three specialized agents evaluate different aspects and reach consensus
**Why:** Different expertise (policy, risk, decision) → better evaluation
**Patterns:** Agent specialization + orchestration
**Time:** 120 minutes
**Complexity:** ⭐⭐⭐⭐

---

## Architecture

```
Customer Data
  ↓
┌─────────────────────────┬──────────────────────────┬──────────────────────┐
│                         │                          │                      │
↓                         ↓                          ↓
Policy Agent          Risk Agent              Decision Agent
(Check rules)         (Calculate risk)        (Make decision)
  ↓                     ↓                        ↓
Policy Report         Risk Report            Consensus Decision
(Eligible? Yes/No)    (Risk: Low/Med/High)   (APPROVE/DENY/REFER)
  ↓                     ↓                        ↓
└─────────────────────────┴──────────────────────────┴──────────────────────┘
                         ↓
                   Final Decision
```

---

## Step 1: PolicyAgent (30 min)

### Goal
Check if customer meets all policy requirements.

### What to Build

```python
class PolicyAgent:
    """Evaluates policy compliance"""
    
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"
        self.name = "Policy Agent"
    
    def evaluate(self, customer: Dict) -> Dict:
        """Check all policies"""
        
        prompt = f"""
You are a policy compliance expert. Evaluate this applicant:

APPLICANT:
- Credit score: {customer['credit_score']}
- Annual income: ${customer['income']:,}
- Employment: {customer['employment_years']} years
- Requested loan: ${customer.get('loan_amount', 25000):,}

POLICIES:
1. Minimum credit score: 600
2. Minimum employment: 2 years
3. Maximum loan: $50,000
4. Minimum loan: $5,000

TASK: For each policy, determine:
1. Is it met? (YES/NO)
2. Evidence

Format your response as:
POLICY RESULTS:
- Credit (600 min): [MET/VIOLATED] ({score})
- Employment (2 years min): [MET/VIOLATED] ({years})
- Loan range ($5K-$50K): [MET/VIOLATED] ({amount})

OVERALL ELIGIBLE: [YES/NO]
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result_text = response.content[0].text
        
        # Parse overall eligibility
        eligible = "OVERALL ELIGIBLE: YES" in result_text
        
        return {
            "agent": self.name,
            "evaluation": result_text,
            "eligible": eligible
        }
```

### Key Point
- Policy Agent: **Binary decision** (Eligible or Not)
- Checks rules, not judgment

---

## Step 2: RiskAgent (30 min)

### Goal
Calculate risk score using weighted criteria.

### What to Build

```python
class RiskAgent:
    """Calculates risk level"""
    
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"
        self.name = "Risk Agent"
    
    def evaluate(self, customer: Dict) -> Dict:
        """Calculate risk score"""
        
        prompt = f"""
You are a credit risk analyst. Calculate risk for this applicant:

APPLICANT:
- Credit score: {customer['credit_score']}
- Income: ${customer['income']:,}
- Employment: {customer['employment_years']} years
- Loan: ${customer.get('loan_amount', 25000):,}

SCORING WEIGHTS:
- Credit score: 40%
- Income stability: 30%
- Employment history: 20%
- Loan amount: 10%

RISK SCALE:
- 0-30: LOW RISK → approve
- 31-60: MEDIUM RISK → manual review
- 61-100: HIGH RISK → deny

TASK: Calculate risk score (0-100).

Format:
RISK SCORE: [0-100]
RISK LEVEL: [LOW/MEDIUM/HIGH]

REASONING:
- Credit score contributes: [XX%]
- Income contributes: [XX%]
- Employment contributes: [XX%]
- Loan amount contributes: [XX%]

RECOMMENDATION: [Recommend approval/review/denial]
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result_text = response.content[0].text
        
        # Parse risk level
        risk_level = "MEDIUM"
        if "LOW RISK" in result_text:
            risk_level = "LOW"
        elif "HIGH RISK" in result_text:
            risk_level = "HIGH"
        
        return {
            "agent": self.name,
            "evaluation": result_text,
            "risk_level": risk_level
        }
```

### Key Point
- Risk Agent: **Quantified assessment** (0-100)
- Weighs multiple factors

---

## Step 3: DecisionAgent (30 min)

### Goal
Make final decision using both reports.

### What to Build

```python
class DecisionAgent:
    """Makes final decision"""
    
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"
        self.name = "Decision Agent"
    
    def decide(
        self,
        policy_eval: Dict,
        risk_eval: Dict,
        customer: Dict
    ) -> Dict:
        """Make final decision"""
        
        prompt = f"""
You are the final decision maker.

CUSTOMER: {customer['name']}

POLICY AGENT REPORT:
{policy_eval['evaluation']}

RISK AGENT REPORT:
{risk_eval['evaluation']}

DECISION RULES:
- Policy violations → DENY
- Eligible + Low risk → APPROVE
- Eligible + Medium risk → REFER for manual review
- High risk → DENY

TASK: Make final decision.

Format:
FINAL DECISION: [APPROVE/DENY/REFER]
REASONING: [2-3 sentences]
CONDITIONS: [Any conditions for approval]
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result_text = response.content[0].text
        
        # Parse decision
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
```

### Key Point
- Decision Agent: **Final judgment** (APPROVE/DENY/REFER)
- Synthesizes other agents' findings

---

## Step 4: Orchestrator (30 min)

### Goal
Coordinate the three agents.

### What to Build

```python
class LoanEvaluationV4:
    """Multi-agent orchestration"""
    
    def __init__(self):
        self.policy_agent = PolicyAgent()
        self.risk_agent = RiskAgent()
        self.decision_agent = DecisionAgent()
    
    def evaluate_loan(self, customer: Dict) -> Dict:
        """Orchestrate evaluation"""
        
        print(f"Evaluating: {customer['name']}")
        
        # Step 1: Policy evaluation
        print("  [1/3] Policy Agent...")
        policy_result = self.policy_agent.evaluate(customer)
        print(f"        Eligible: {policy_result['eligible']}")
        
        # Step 2: Risk evaluation
        print("  [2/3] Risk Agent...")
        risk_result = self.risk_agent.evaluate(customer)
        print(f"        Risk: {risk_result['risk_level']}")
        
        # Step 3: Final decision
        print("  [3/3] Decision Agent...")
        decision_result = self.decision_agent.decide(
            policy_result,
            risk_result,
            customer
        )
        print(f"        Decision: {decision_result['decision']}")
        
        return {
            "customer_name": customer['name'],
            "policy_result": policy_result,
            "risk_result": risk_result,
            "final_decision": decision_result['decision'],
            "reasoning": decision_result['reasoning']
        }
```

### Key Point
- Orchestrator: **Coordinates workflow**
- Passes results between agents
- Returns final decision

---

## HOMEWORK ASSIGNMENT

### Build Features:

1. **Agent Performance**
   - Measure latency of each agent
   - Track API calls
   - Calculate total cost

2. **Decision Confidence**
   - Show if all agents agree
   - Note any conflicts
   - Rate consistency

3. **Audit Trail**
   - Save all three reports
   - Record timestamps
   - Create audit.json

### Solution Example
```python
result = system.evaluate_loan(customer)
# Should show:
#
# Policy Agent: ELIGIBLE (meets all rules)
# Risk Agent: MEDIUM RISK (risk score: 45)
# Decision Agent: REFER (medium risk needs review)
```

---

## Key Differences: V3 → V4

| Feature | V3 | V4 |
|---------|----|----|
| Agents | 1 (general) | 3 (specialized) |
| Evaluation | Single pass | Multi-phase |
| Perspectives | Functional | Policy + Risk + Decision |
| Conflict | No | Possible, resolved by Decision Agent |
| Complexity | Linear | Orchestrated |

---

## Why Multiple Agents?

**Single agent** (V3):
- Jack of all trades
- May miss specialized insights
- Less robust

**Multiple agents** (V4):
- Policy expert knows rules
- Risk expert knows scoring
- Decision maker synthesizes
- More robust, auditable

---

## Orchestration Patterns

### Sequential (what we built):
```
Policy → Risk → Decision
```

### Parallel (optional challenge):
```
Policy ─┐
        ├─→ Decision
Risk ──┘
```

### Iterative (advanced):
```
Policy ↔ Risk ↔ Decision
(agents discuss)
```

---

## Time Breakdown
- Step 1 (PolicyAgent): 30 min
- Step 2 (RiskAgent): 30 min
- Step 3 (DecisionAgent): 30 min
- Step 4 (Orchestrator): 30 min
- **Total: 120 minutes**

---

## Next: V5 Production
V4 has *three specialized agents*. V5 has *all 8 patterns + monitoring*.

