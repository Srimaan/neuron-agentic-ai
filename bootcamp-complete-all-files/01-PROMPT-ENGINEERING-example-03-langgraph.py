"""
FRAMEWORK 3: LANGGRAPH
======================

Loan evaluation using LangGraph state machines.

ADVANTAGES:
- Explicit workflows (can see flow clearly)
- State management built-in
- Easy debugging (trace through states)
- Perfect for agents
- Control flow is clear

DISADVANTAGES:
- More verbose than LangChain
- Requires thinking about states
- More setup code
- Learning curve

WHEN TO USE:
- Complex workflows
- Production agents
- Debugging needed
- Multi-step processes
- When you need explicit control

INSTALLATION:
pip install langgraph langchain langchain-anthropic
"""

import json
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain.chat_models import ChatAnthropic


# ============================================================================
# STEP 1: Define the state
# ============================================================================

class LoanApplicationState(TypedDict):
    """
    State that flows through the graph.
    
    This TypedDict defines what data moves between nodes.
    """
    # Input
    application: dict
    
    # Processing
    system_prompt: str
    evaluation_prompt: str
    
    # Output
    decision: dict
    error: str


# ============================================================================
# STEP 2: Define nodes (steps in the workflow)
# ============================================================================

def format_application_node(state: LoanApplicationState) -> LoanApplicationState:
    """
    Node 1: Format the application data.
    
    Calculate derived fields like DTI, loan-to-income, etc.
    """
    app = state["application"]
    
    monthly_debt = (app.get("debt_per_year", 0) / 12)
    monthly_income = (app.get("annual_income", 0) / 12)
    dti = monthly_debt / monthly_income if monthly_income > 0 else 0
    loan_to_income = app.get("loan_amount", 0) / app.get("annual_income", 1)
    
    # Build evaluation prompt
    evaluation_prompt = f"""Evaluate this application:

Name: {app.get('name', 'Unknown')}
Credit Score: {app.get('credit_score', 'Unknown')}
Annual Income: ${app.get('annual_income', 0):,}
Monthly Debt: ${monthly_debt:,.0f}
Debt-to-Income Ratio: {dti:.2f}
Loan Amount: ${app.get('loan_amount', 0):,}
Loan Duration: {app.get('loan_months', 60)} months
Loan-to-Income Ratio: {loan_to_income:.2f}
Employment: {app.get('employment', 'Unknown')}
Years at Job: {app.get('years_employed', 'Unknown')}
Purpose: {app.get('purpose', 'Unknown')}
Savings: ${app.get('assets', 0):,}

[Output JSON only. No explanation.]"""
    
    state["evaluation_prompt"] = evaluation_prompt
    return state


def evaluate_with_claude_node(state: LoanApplicationState) -> LoanApplicationState:
    """
    Node 2: Call Claude to evaluate.
    
    This node calls Claude API with the formatted prompt.
    """
    try:
        # Initialize Claude
        client = ChatAnthropic(model="claude-3-5-sonnet-20241022")
        
        # Get the system and evaluation prompts from state
        system_prompt = state["system_prompt"]
        eval_prompt = state["evaluation_prompt"]
        
        # Call Claude
        response = client.invoke([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": eval_prompt}
        ])
        
        # Parse response
        response_text = response.content
        decision = json.loads(response_text)
        
        state["decision"] = decision
        state["error"] = ""
        
    except json.JSONDecodeError as e:
        state["error"] = f"JSON parse error: {str(e)}"
        state["decision"] = {}
    except Exception as e:
        state["error"] = f"Claude call error: {str(e)}"
        state["decision"] = {}
    
    return state


def format_output_node(state: LoanApplicationState) -> LoanApplicationState:
    """
    Node 3: Format the output for display.
    
    This node doesn't change state, just formats for display.
    """
    # In a real system, you might save to database here
    # For now, we just ensure the decision is clean
    if not state["decision"]:
        state["decision"] = {
            "decision": "error",
            "reason": state.get("error", "Unknown error"),
            "score": 0,
            "factors": [],
            "next_step": "Manual review"
        }
    
    return state


# ============================================================================
# STEP 3: Build the graph
# ============================================================================

def create_loan_evaluation_graph():
    """
    Create a LangGraph state machine for loan evaluation.
    
    Graph flow:
    format_application → evaluate_with_claude → format_output → END
    """
    
    # Create the graph
    graph_builder = StateGraph(LoanApplicationState)
    
    # Add nodes (steps)
    graph_builder.add_node("format_application", format_application_node)
    graph_builder.add_node("evaluate_claude", evaluate_with_claude_node)
    graph_builder.add_node("format_output", format_output_node)
    
    # Define edges (flow between nodes)
    graph_builder.set_entry_point("format_application")  # Start here
    graph_builder.add_edge("format_application", "evaluate_claude")  # format → evaluate
    graph_builder.add_edge("evaluate_claude", "format_output")  # evaluate → format
    graph_builder.add_edge("format_output", END)  # format → done
    
    # Compile the graph (create the executable version)
    graph = graph_builder.compile()
    
    return graph


# ============================================================================
# STEP 4: Define the system prompt
# ============================================================================

SYSTEM_PROMPT = """You are an automated loan evaluation system for a community bank.

Your job: Evaluate loan applications and output a structured decision.

OUTPUT FORMAT (JSON ONLY):
{
  "decision": "approved" | "denied" | "review",
  "reason": "brief explanation",
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


# ============================================================================
# STEP 5: Evaluate function
# ============================================================================

def evaluate_loan_langgraph(application: dict) -> dict:
    """
    Evaluate a loan using LangGraph.
    
    This runs through the graph:
    1. Format application
    2. Call Claude
    3. Format output
    4. Return result
    """
    
    # Create the graph
    graph = create_loan_evaluation_graph()
    
    # Create initial state
    initial_state = LoanApplicationState(
        application=application,
        system_prompt=SYSTEM_PROMPT,
        evaluation_prompt="",
        decision={},
        error=""
    )
    
    # Run the graph
    # This invokes all nodes in sequence
    final_state = graph.invoke(initial_state)
    
    return final_state["decision"]


# ============================================================================
# STEP 6: Pretty print
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
    print("LOAN EVALUATION SYSTEM - LANGGRAPH")
    print("="*60)
    print("\nNote: This uses explicit state machine workflow:")
    print("1. Format application (calculate derived fields)")
    print("2. Call Claude to evaluate")
    print("3. Format output for display")
    print("\nEach step is a 'node' in the graph.")
    
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
    
    decision1 = evaluate_loan_langgraph(good_app)
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
    
    decision2 = evaluate_loan_langgraph(borderline_app)
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
    
    decision3 = evaluate_loan_langgraph(risky_app)
    print_decision(decision3)
    
    
    print("\n" + "="*60)
    print("LANGGRAPH ADVANTAGES SHOWN:")
    print("="*60)
    print("✓ Explicit workflow (can visualize the flow)")
    print("✓ State management (all data in one dict)")
    print("✓ Node composition (each step is a function)")
    print("✓ Easy to debug (can trace through each node)")
    print("✓ Easy to extend (add new nodes/edges)")
    print("✓ Production-ready (used in many agents)")
