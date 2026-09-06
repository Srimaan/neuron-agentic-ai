"""
FRAMEWORK 4: AUTOGEN
====================

Loan evaluation using AutoGen multi-agent system.

ADVANTAGES:
- Multi-agent conversations
- Agents collaborate on tasks
- Agent communication built-in
- Can have multiple specialists
- Agents can review each other's work

DISADVANTAGES:
- Higher abstraction level
- Less transparent control
- Harder to debug
- Complex conversations
- Slower than single agent

WHEN TO USE:
- Multiple specialists needed
- Agents need to collaborate
- Complex decisions requiring review
- Agent discussions/debates
- When you want agent autonomy

INSTALLATION:
pip install pyautogen
"""

import os
import json
from autogen import AssistantAgent, UserProxyAgent


# ============================================================================
# STEP 1: Define the evaluation rules as a function
# ============================================================================

def evaluate_loan_internal(application: dict) -> dict:
    """
    Internal evaluation logic (what the agent should do).
    
    This is the evaluation rules in code form, separate from the agents.
    """
    monthly_debt = (application.get("debt_per_year", 0) / 12)
    monthly_income = (application.get("annual_income", 0) / 12)
    dti = monthly_debt / monthly_income if monthly_income > 0 else 0
    loan_to_income = application.get("loan_amount", 0) / application.get("annual_income", 1)
    
    return {
        "dti": dti,
        "loan_to_income": loan_to_income,
        "monthly_income": monthly_income,
        "monthly_debt": monthly_debt
    }


# ============================================================================
# STEP 2: Create AutoGen agents
# ============================================================================

def create_agents():
    """
    Create a team of agents that collaborate on loan evaluation.
    
    - LoanAnalyst: Reviews the application
    - LoanReviewer: Checks the analysis
    - UserProxy: Simulates user interaction
    """
    
    # AGENT 1: Loan Analyst (Claude-based)
    loan_analyst = AssistantAgent(
        name="LoanAnalyst",
        system_message="""You are an expert loan analyst for a community bank.
        
Your job: Review loan applications and provide detailed analysis.

When analyzing an application, consider:
1. Credit score (750+ excellent, 700-749 good, 650-699 fair, <650 poor)
2. Debt-to-income ratio (<0.25 excellent, 0.25-0.36 good, 0.37-0.43 fair, >0.43 poor)
3. Employment status (must be employed or self-employed >1 year)
4. Loan-to-income ratio (should be <5x annual income)
5. Available assets and savings

Provide a structured analysis with:
- Positive factors
- Risk factors
- Initial recommendation (approve/deny/review)
- Confidence level (high/medium/low)

Always cite the specific numbers and rules you're using.""",
        llm_config={
            "config_list": [{"model": "claude-3-5-sonnet-20241022"}],
            "temperature": 0,
        },
        is_termination_msg=lambda x: "recommendation" in str(x).lower()
    )
    
    # AGENT 2: Loan Reviewer (Claude-based)
    loan_reviewer = AssistantAgent(
        name="LoanReviewer",
        system_message="""You are a senior loan reviewer for a community bank.

Your job: Review the loan analyst's analysis and make the final decision.

Check the analyst's work:
1. Are the calculations correct?
2. Were all criteria considered?
3. Is the recommendation justified?
4. Any edge cases missed?

Provide a final decision with:
- Decision (Approved/Denied/Review)
- Score (0-100)
- Justification
- Any conditions (if applicable)

Be critical and thorough. This is the final check.""",
        llm_config={
            "config_list": [{"model": "claude-3-5-sonnet-20241022"}],
            "temperature": 0,
        },
        is_termination_msg=lambda x: "decision" in str(x).lower() or "approved" in str(x).lower()
    )
    
    # AGENT 3: User Proxy (simulates human interaction)
    user_proxy = UserProxyAgent(
        name="user",
        human_input_mode="NEVER",  # Fully automated (no human input)
        max_consecutive_auto_reply=10,  # Prevent infinite loops
        system_message="You are a loan application submission system. Forward the application for analysis."
    )
    
    return loan_analyst, loan_reviewer, user_proxy


# ============================================================================
# STEP 3: Format application for agent discussion
# ============================================================================

def format_application_for_agents(app: dict) -> str:
    """Format application as a message for agents to discuss."""
    metrics = evaluate_loan_internal(app)
    
    return f"""LOAN APPLICATION FOR ANALYSIS:

Applicant: {app.get('name', 'Unknown')}
Credit Score: {app.get('credit_score', 'Unknown')}
Annual Income: ${app.get('annual_income', 0):,}
Monthly Income: ${metrics['monthly_income']:,.0f}
Existing Monthly Debt: ${metrics['monthly_debt']:,.0f}
Debt-to-Income Ratio: {metrics['dti']:.2f}
Loan Amount: ${app.get('loan_amount', 0):,}
Loan Duration: {app.get('loan_months', 60)} months
Loan-to-Income Ratio: {metrics['loan_to_income']:.2f}
Employment: {app.get('employment', 'Unknown')}
Years at Current Job: {app.get('years_employed', 'Unknown')}
Purpose: {app.get('purpose', 'Unknown')}
Savings/Assets: ${app.get('assets', 0):,}

Please analyze this application according to your role.
LoanAnalyst: Provide your analysis.
LoanReviewer: Review the analysis and provide final decision."""


# ============================================================================
# STEP 4: Evaluate using agent conversation
# ============================================================================

def evaluate_loan_autogen(application: dict) -> dict:
    """
    Evaluate a loan using AutoGen agent conversation.
    
    This creates a conversation flow:
    1. User submits application
    2. LoanAnalyst analyzes it
    3. LoanReviewer reviews and decides
    4. Final decision is extracted
    """
    
    try:
        # Create agents
        analyst, reviewer, user_proxy = create_agents()
        
        # Prepare application message
        app_message = format_application_for_agents(application)
        
        # Start conversation: user → analyst
        # (This is a simplified version; in production you'd use groupchat)
        user_proxy.initiate_chat(
            analyst,
            message=app_message
        )
        
        # Get analyst's response
        analyst_response = user_proxy.last_message()["content"]
        
        # Now reviewer reviews it
        user_proxy.initiate_chat(
            reviewer,
            message=f"Review this analysis:\n\n{analyst_response}\n\nProvide your final decision."
        )
        
        reviewer_response = user_proxy.last_message()["content"]
        
        # Extract decision from reviewer's response
        decision = {
            "decision": "review",  # Default to review
            "reason": reviewer_response[:200],  # First 200 chars
            "score": 75,  # Default score
            "factors": ["analyst_reviewed", "reviewer_approved"],
            "next_step": "Process application"
        }
        
        # Try to extract structured data
        if "approved" in reviewer_response.lower():
            decision["decision"] = "approved"
        elif "denied" in reviewer_response.lower():
            decision["decision"] = "denied"
        elif "review" in reviewer_response.lower():
            decision["decision"] = "review"
        
        return decision
        
    except Exception as e:
        return {
            "decision": "error",
            "reason": f"Error in agent conversation: {str(e)}",
            "score": 0,
            "factors": [],
            "next_step": "Manual review required"
        }


# ============================================================================
# STEP 5: Pretty print
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
    print("LOAN EVALUATION SYSTEM - AUTOGEN")
    print("="*60)
    print("\nNote: This uses multi-agent conversation flow:")
    print("1. LoanAnalyst reviews the application")
    print("2. LoanReviewer checks the analysis")
    print("3. Agents collaborate to reach decision")
    print("\nThis is slower but more thorough than single agent.")
    print("Real conversations enable complex reasoning.\n")
    
    # Example 1: Good applicant
    print("\nEXAMPLE 1: Strong Applicant")
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
    print("\nStarting agent conversation...\n")
    
    # NOTE: This would run the actual agent conversation
    # For testing without API calls, we skip the actual invocation
    # In production, uncomment the line below:
    # decision1 = evaluate_loan_autogen(good_app)
    
    print("(Agent conversation would occur here)")
    print("LoanAnalyst would analyze the application...")
    print("LoanReviewer would check the analysis...")
    print("Final decision would be extracted from conversation.")
    
    
    print("\n" + "="*60)
    print("AUTOGEN ADVANTAGES SHOWN:")
    print("="*60)
    print("✓ Multiple agents collaborate")
    print("✓ Each agent has a role/expertise")
    print("✓ Agents can review each other's work")
    print("✓ Enables complex reasoning through conversation")
    print("✓ More transparent decision-making")
    print("✓ Good for regulatory compliance (audit trail)")
    print("\nNOTE: This example shows structure.")
    print("Real execution requires AutoGen with proper LLM setup.")
