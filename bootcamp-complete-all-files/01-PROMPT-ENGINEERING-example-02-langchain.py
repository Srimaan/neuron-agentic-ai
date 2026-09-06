"""
FRAMEWORK 2: LANGCHAIN
======================

Loan evaluation using LangChain abstractions.

ADVANTAGES:
- Built-in prompt templates
- Composable components (chains)
- Less boilerplate
- Memory built-in
- Many integrations

DISADVANTAGES:
- Additional abstraction layer
- Less control than raw SDK
- Learning curve (new concepts)
- API changes frequently

WHEN TO USE:
- Rapid prototyping
- Building chains
- Reusable components
- Production (often)

INSTALLATION:
pip install langchain langchain-anthropic langchain-core
"""

import json
from langchain.chat_models import ChatAnthropic
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser


# ============================================================================
# STEP 1: Define the system prompt using LangChain template
# ============================================================================

SYSTEM_TEMPLATE = """You are an automated loan evaluation system for a community bank.

Your job: Evaluate loan applications and output a structured decision.

OUTPUT FORMAT (JSON ONLY):
{{
  "decision": "approved" | "denied" | "review",
  "reason": "brief explanation",
  "score": number (0-100),
  "factors": ["factor1", "factor2"],
  "next_step": "what happens now"
}}

EVALUATION CRITERIA:

Credit Score:
- 750+: Excellent (80 points)
- 700-749: Good (60 points)
- 650-699: Fair (40 points)
- <650: Poor (0 points, typically deny)

Debt-to-Income Ratio:
- <0.25: Excellent (80 points)
- 0.25-0.36: Good (60 points)
- 0.37-0.43: Fair (40 points)
- >0.43: Poor (0 points, typically deny)

Employment:
- Currently employed: 20 points
- Unemployed: 0 points (escalate)
- Stable employment >2 years: +10 bonus

Loan-to-Income Ratio:
- Loan < Annual Income × 3: Good (20 points)
- Loan < Annual Income × 5: Fair (10 points)
- Loan > Annual Income × 5: Poor (deny)

DECISION THRESHOLDS:
- 200+: Approved (low risk)
- 150-199: Approved (standard)
- 100-149: Review (escalate)
- <100: Denied (high risk)

EXCEPTIONS:
- If employment unverified: Always escalate
- If credit <600: Escalate unless exceptional"""


HUMAN_TEMPLATE = """Evaluate this application:

Name: {name}
Credit Score: {credit_score}
Annual Income: ${annual_income:,}
Monthly Debt: ${monthly_debt:,.0f}
Debt-to-Income Ratio: {dti:.2f}
Loan Amount: ${loan_amount:,}
Loan Duration: {loan_months} months
Loan-to-Income Ratio: {loan_to_income:.2f}
Employment: {employment}
Years at Job: {years_employed}
Purpose: {purpose}
Savings: ${assets:,}

[Output JSON only. No explanation.]"""


# ============================================================================
# STEP 2: Create the prompt template
# ============================================================================

def create_prompt():
    """Create a LangChain prompt template."""
    return ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(SYSTEM_TEMPLATE),
        HumanMessagePromptTemplate.from_template(HUMAN_TEMPLATE),
    ])


# ============================================================================
# STEP 3: Create the LangChain chain
# ============================================================================

def create_chain():
    """Create a LangChain chain (prompt → model → output parser)."""
    
    # Initialize the model
    model = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        temperature=0  # Deterministic (not random)
    )
    
    # Create prompt
    prompt = create_prompt()
    
    # Create output parser (automatically parses JSON)
    output_parser = JsonOutputParser()
    
    # Chain them together: prompt → model → parser
    # This is the "chain" - it runs each step in sequence
    chain = prompt | model | output_parser
    
    return chain


# ============================================================================
# STEP 4: Format application data
# ============================================================================

def format_application(app: dict) -> dict:
    """Calculate derived fields for the application."""
    monthly_debt = (app.get("debt_per_year", 0) / 12)
    monthly_income = (app.get("annual_income", 0) / 12)
    dti = monthly_debt / monthly_income if monthly_income > 0 else 0
    loan_to_income = app.get("loan_amount", 0) / app.get("annual_income", 1)
    
    return {
        **app,
        "monthly_debt": monthly_debt,
        "dti": dti,
        "loan_to_income": loan_to_income
    }


# ============================================================================
# STEP 5: Evaluate loan
# ============================================================================

def evaluate_loan_langchain(application: dict) -> dict:
    """
    Evaluate a loan using LangChain chain.
    
    This is cleaner than raw SDK because:
    1. Prompt template handles formatting
    2. Chain handles the flow
    3. Output parser handles JSON parsing
    """
    
    # Get the chain
    chain = create_chain()
    
    # Format application (add calculated fields)
    formatted_app = format_application(application)
    
    # Invoke the chain with the application data
    # This automatically:
    # 1. Fills the template with values
    # 2. Sends to Claude
    # 3. Parses the JSON output
    try:
        decision = chain.invoke(formatted_app)
        return decision
    except Exception as e:
        return {
            "decision": "error",
            "reason": f"Error during evaluation: {str(e)}",
            "score": 0,
            "factors": [],
            "next_step": "Manual review required"
        }


# ============================================================================
# STEP 6: Pretty print results
# ============================================================================

def print_decision(decision: dict):
    """Pretty print a decision."""
    print(f"\n{'='*60}")
    print(f"DECISION: {decision.get('decision', 'ERROR').upper()}")
    print(f"{'='*60}")
    print(f"Score: {decision.get('score', 'N/A')}")
    print(f"Reason: {decision.get('reason', 'N/A')}")
    print(f"Factors: {', '.join(decision.get('factors', []))}")
    print(f"Next Step: {decision.get('next_step', 'N/A')}")
    print(f"{'='*60}\n")


# ============================================================================
# EXAMPLES
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("LOAN EVALUATION SYSTEM - LANGCHAIN")
    print("="*60)
    print("\nNote: This uses the same logic as raw SDK, but with:")
    print("- Prompt templates (reusable)")
    print("- Chains (composable steps)")
    print("- Output parser (automatic JSON parsing)")
    
    # Example 1: Good applicant
    print("\n\nEXAMPLE 1: Strong Applicant")
    print("-" * 60)
    
    good_app = {
        "name": "John Doe",
        "credit_score": 750,
        "annual_income": 100000,
        "debt_per_year": 10000,
        "loan_amount": 50000,
        "loan_months": 60,
        "employment": "Employed, 4 years",
        "years_employed": 4,
        "purpose": "Home improvement",
        "assets": 50000
    }
    
    print(f"Applicant: {good_app['name']}")
    print(f"Credit: {good_app['credit_score']}, Income: ${good_app['annual_income']:,}")
    
    decision1 = evaluate_loan_langchain(good_app)
    print_decision(decision1)
    
    
    # Example 2: Borderline
    print("\nEXAMPLE 2: Borderline Applicant")
    print("-" * 60)
    
    borderline_app = {
        "name": "Sarah Johnson",
        "credit_score": 680,
        "annual_income": 60000,
        "debt_per_year": 18000,
        "loan_amount": 40000,
        "loan_months": 60,
        "employment": "Employed, 2 years",
        "years_employed": 2,
        "purpose": "Car purchase",
        "assets": 10000
    }
    
    print(f"Applicant: {borderline_app['name']}")
    print(f"Credit: {borderline_app['credit_score']}, Income: ${borderline_app['annual_income']:,}")
    
    decision2 = evaluate_loan_langchain(borderline_app)
    print_decision(decision2)
    
    
    # Example 3: Risky
    print("\nEXAMPLE 3: Risky Applicant")
    print("-" * 60)
    
    risky_app = {
        "name": "Mike Smith",
        "credit_score": 580,
        "annual_income": 40000,
        "debt_per_year": 24000,
        "loan_amount": 50000,
        "loan_months": 60,
        "employment": "Between jobs",
        "years_employed": 0,
        "purpose": "Debt consolidation",
        "assets": 1000
    }
    
    print(f"Applicant: {risky_app['name']}")
    print(f"Credit: {risky_app['credit_score']}, Income: ${risky_app['annual_income']:,}")
    
    decision3 = evaluate_loan_langchain(risky_app)
    print_decision(decision3)
    
    
    print("\n" + "="*60)
    print("LANGCHAIN ADVANTAGES SHOWN:")
    print("="*60)
    print("✓ Prompt template (reusable across different tasks)")
    print("✓ Chain composition (prompt → model → parser)")
    print("✓ Automatic JSON parsing (no manual parsing needed)")
    print("✓ Less code than raw SDK")
    print("✓ Easy to add memory, logging, other tools")
