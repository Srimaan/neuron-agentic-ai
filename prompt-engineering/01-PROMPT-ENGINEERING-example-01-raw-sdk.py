"""
FRAMEWORK 1: RAW PYTHON + CLAUDE SDK
=====================================

Loan evaluation using direct Anthropic API calls.

ADVANTAGES:
- Maximum control
- No abstraction layers
- Easiest to understand
- Perfect for learning

DISADVANTAGES:
- More boilerplate code
- You handle everything manually
- More error handling needed

WHEN TO USE:
- Learning
- Simple scripts
- Custom requirements
- Understanding fundamentals
"""

import os
import json
from anthropic import Anthropic

# Initialize client
client = Anthropic()

# SYSTEM PROMPT: This is the role and rules for Claude
SYSTEM_PROMPT = """You are an automated loan evaluation system for a community bank.

Your job: Evaluate loan applications and output a structured decision.

OUTPUT FORMAT (JSON ONLY - No other text):
{
  "decision": "approved" | "denied" | "review",
  "reason": "brief explanation of decision",
  "score": number (0-100),
  "factors": ["factor1", "factor2"],
  "next_step": "what happens now"
}

EVALUATION CRITERIA:

Credit Score:
- 750+: Excellent (80 points)
- 700-749: Good (60 points)
- 650-699: Fair (40 points)
- <650: Poor (0 points, typically deny)

Debt-to-Income Ratio (monthly debt / monthly income):
- <0.25: Excellent (80 points)
- 0.25-0.36: Good (60 points)
- 0.37-0.43: Fair (40 points)
- >0.43: Poor (0 points, typically deny)

Employment:
- Currently employed: 20 points
- Unemployed: 0 points (escalate to review)
- Self-employed <1 year: Escalate to review
- Stable employment >2 years: +10 bonus

Loan-to-Income Ratio:
- Loan < Annual Income × 3: Good (20 points)
- Loan < Annual Income × 5: Fair (10 points)
- Loan > Annual Income × 5: Poor (0 points, deny)

DECISION THRESHOLDS:
- 200+: Approved (low risk)
- 150-199: Approved (standard)
- 100-149: Review (escalate to human)
- <100: Denied (high risk)

EXCEPTIONS:
- If employment unverified: Always escalate to review
- If credit <600: Escalate unless exceptional
- If first-time homebuyer: Adjust thresholds by -10"""


def format_application_for_prompt(app: dict) -> str:
    """Format application data as readable text for Claude."""
    monthly_debt = (app.get("debt_per_year", 0) / 12)
    monthly_income = (app.get("annual_income", 0) / 12)
    dti = monthly_debt / monthly_income if monthly_income > 0 else 0
    loan_to_income = app.get("loan_amount", 0) / app.get("annual_income", 1)
    
    return f"""
APPLICATION TO EVALUATE:

Name: {app.get('name', 'Unknown')}
Credit Score: {app.get('credit_score', 'Unknown')}
Annual Income: ${app.get('annual_income', 0):,}
Monthly Debt: ${monthly_debt:,.0f}
Debt-to-Income Ratio: {dti:.2f}
Loan Amount: ${app.get('loan_amount', 0):,}
Loan Duration: {app.get('loan_months', 60)} months
Loan-to-Income Ratio: {loan_to_income:.2f}
Employment: {app.get('employment', 'Unknown')}
Years at Current Job: {app.get('years_employed', 'Unknown')}
Purpose: {app.get('purpose', 'Unknown')}
Savings/Assets: ${app.get('assets', 0):,}

[Evaluate and output JSON only. No explanation.]
"""


def evaluate_loan(application: dict) -> dict:
    """
    Evaluate a loan application using Claude.
    
    Args:
        application: Dict with loan details
        
    Returns:
        Parsed JSON decision from Claude
    """
    
    # Format the application
    app_text = format_application_for_prompt(application)
    
    # Create message (this is what gets sent to Claude)
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",  # Use the latest Sonnet model
        max_tokens=500,  # Limit response length
        system=SYSTEM_PROMPT,  # The role & rules (doesn't change per request)
        messages=[
            {
                "role": "user",
                "content": app_text  # The specific application to evaluate
            }
        ]
    )
    
    # Extract the text response
    response_text = message.content[0].text
    
    # Parse JSON from response
    try:
        # Claude should output pure JSON, so we can parse directly
        decision = json.loads(response_text)
        return decision
    except json.JSONDecodeError:
        # If parsing fails, return error
        return {
            "decision": "error",
            "reason": f"Could not parse Claude response: {response_text}",
            "score": 0,
            "factors": [],
            "next_step": "Manual review required"
        }


def print_decision(decision: dict):
    """Pretty print a decision."""
    print(f"\n{'='*60}")
    print(f"DECISION: {decision['decision'].upper()}")
    print(f"{'='*60}")
    print(f"Score: {decision.get('score', 'N/A')}/250")
    print(f"Reason: {decision.get('reason', 'N/A')}")
    print(f"Factors: {', '.join(decision.get('factors', []))}")
    print(f"Next Step: {decision.get('next_step', 'N/A')}")
    print(f"{'='*60}\n")


# ============================================================================
# EXAMPLES: Test with different applications
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("LOAN EVALUATION SYSTEM - RAW PYTHON SDK")
    print("="*60)
    
    # Example 1: Good applicant (should APPROVE)
    print("\nEXAMPLE 1: Strong Applicant")
    print("-" * 60)
    
    good_applicant = {
        "name": "John Doe",
        "credit_score": 750,
        "annual_income": 100000,
        "debt_per_year": 10000,  # ~$833/month
        "loan_amount": 50000,
        "loan_months": 60,
        "employment": "Employed, 4 years at current company",
        "years_employed": 4,
        "purpose": "Home improvement",
        "assets": 50000
    }
    
    print(f"Applicant: {good_applicant['name']}")
    print(f"Credit: {good_applicant['credit_score']}, Income: ${good_applicant['annual_income']:,}")
    print(f"Loan: ${good_applicant['loan_amount']:,}")
    
    decision1 = evaluate_loan(good_applicant)
    print_decision(decision1)
    
    
    # Example 2: Borderline applicant (should REVIEW)
    print("\nEXAMPLE 2: Borderline Applicant")
    print("-" * 60)
    
    borderline_applicant = {
        "name": "Sarah Johnson",
        "credit_score": 680,
        "annual_income": 60000,
        "debt_per_year": 18000,  # $1500/month
        "loan_amount": 40000,
        "loan_months": 60,
        "employment": "Employed, 2 years at current company",
        "years_employed": 2,
        "purpose": "Car purchase",
        "assets": 10000
    }
    
    print(f"Applicant: {borderline_applicant['name']}")
    print(f"Credit: {borderline_applicant['credit_score']}, Income: ${borderline_applicant['annual_income']:,}")
    print(f"Loan: ${borderline_applicant['loan_amount']:,}")
    
    decision2 = evaluate_loan(borderline_applicant)
    print_decision(decision2)
    
    
    # Example 3: Risky applicant (should DENY)
    print("\nEXAMPLE 3: Risky Applicant")
    print("-" * 60)
    
    risky_applicant = {
        "name": "Mike Smith",
        "credit_score": 580,
        "annual_income": 40000,
        "debt_per_year": 24000,  # $2000/month
        "loan_amount": 50000,
        "loan_months": 60,
        "employment": "Between jobs",
        "years_employed": 0,
        "purpose": "Debt consolidation",
        "assets": 1000
    }
    
    print(f"Applicant: {risky_applicant['name']}")
    print(f"Credit: {risky_applicant['credit_score']}, Income: ${risky_applicant['annual_income']:,}")
    print(f"Loan: ${risky_applicant['loan_amount']:,}")
    
    decision3 = evaluate_loan(risky_applicant)
    print_decision(decision3)
    
    
    print("\n" + "="*60)
    print("EVALUATION COMPLETE")
    print("="*60)
    print("\nKey takeaways:")
    print("1. Same system prompt used for all evaluations")
    print("2. Different applications get different decisions")
    print("3. Decisions are consistent (same rules applied)")
    print("4. Output format is structured JSON")
