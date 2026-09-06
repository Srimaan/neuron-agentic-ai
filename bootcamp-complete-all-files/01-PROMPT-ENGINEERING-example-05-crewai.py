"""
FRAMEWORK 5: CREWAI
===================

Loan evaluation using CrewAI role-based agent system.

ADVANTAGES:
- Role-based abstraction (simple, intuitive)
- Task-driven design (what not how)
- Clean API
- Good for hierarchical teams
- Easy to understand

DISADVANTAGES:
- High-level abstraction (less control)
- Limited customization
- Smaller community than LangChain
- Less flexible than other frameworks

WHEN TO USE:
- Role hierarchies (manager, specialist, reviewer)
- Task-oriented workflows
- Rapid prototyping
- When you want simplicity
- Team simulations

INSTALLATION:
pip install crewai langchain-anthropic
"""

from crewai import Agent, Task, Crew
from langchain.chat_models import ChatAnthropic


# ============================================================================
# STEP 1: Create agents with roles
# ============================================================================

def create_loan_evaluation_crew():
    """
    Create a CrewAI crew (team) for loan evaluation.
    
    Each agent has a specific role and expertise.
    """
    
    # AGENT 1: Loan Analyst (specialist)
    loan_analyst = Agent(
        role="Loan Analysis Specialist",
        goal="Thoroughly analyze loan applications to identify key financial factors",
        backstory="""You are an expert loan analyst with 8 years of experience 
        in the banking industry. You excel at analyzing financial data and 
        identifying risk factors. Your analysis is detailed and thorough, 
        citing specific numbers and criteria.""",
        allow_delegation=False
    )
    
    # AGENT 2: Risk Assessor (specialist)
    risk_assessor = Agent(
        role="Risk Assessment Officer",
        goal="Assess the risk profile of loan applicants based on financial metrics",
        backstory="""You are a risk assessment expert with deep knowledge of 
        lending regulations and risk management. You understand credit scoring, 
        debt ratios, and employment stability. You provide clear, justified risk ratings.""",
        allow_delegation=False
    )
    
    # AGENT 3: Loan Manager (decision maker)
    loan_manager = Agent(
        role="Loan Approval Manager",
        goal="Make final loan approval decisions based on analysis and risk assessment",
        backstory="""You are a senior loan manager responsible for final approval decisions. 
        You balance business opportunities with risk management. You make final calls 
        based on analysis from your team. Your decisions are fair and defensible.""",
        allow_delegation=True  # Can delegate to other agents
    )
    
    return loan_analyst, risk_assessor, loan_manager


# ============================================================================
# STEP 2: Create tasks
# ============================================================================

def create_loan_evaluation_tasks(application: dict, agents):
    """
    Create tasks for the crew to execute.
    
    Each task has an objective, expected output, and responsible agent.
    """
    
    analyst, risk_assessor, manager = agents
    
    # Format application data for tasks
    app_summary = f"""
Applicant: {application.get('name')}
Credit Score: {application.get('credit_score')}
Annual Income: ${application.get('annual_income'):,}
Monthly Debt: ${application.get('debt_per_year', 0)/12:,.0f}
Loan Amount: ${application.get('loan_amount'):,}
Employment: {application.get('employment')}
Years at Job: {application.get('years_employed')}
Purpose: {application.get('purpose')}
Assets: ${application.get('assets', 0):,}
"""
    
    # TASK 1: Analyze the application
    analysis_task = Task(
        description=f"""Analyze this loan application:
{app_summary}

Calculate and analyze:
1. Debt-to-Income Ratio (monthly debt / monthly income)
2. Loan-to-Income Ratio (loan amount / annual income)
3. Credit quality assessment
4. Employment stability
5. Asset coverage

Provide detailed analysis with specific numbers.""",
        expected_output="Detailed financial analysis with calculations and assessment",
        agent=analyst
    )
    
    # TASK 2: Assess risk
    risk_task = Task(
        description=f"""Based on the analysis provided, assess the risk profile:
{app_summary}

Consider:
1. Credit score implications
2. Debt-to-income ratio implications
3. Employment stability
4. Loan-to-income ratio implications
5. Overall risk level (Low/Medium/High)

Provide a risk assessment with score (0-100, higher = more risk).""",
        expected_output="Risk assessment with score and justification",
        agent=risk_assessor
    )
    
    # TASK 3: Make approval decision
    approval_task = Task(
        description=f"""Make the final loan approval decision based on:
1. The financial analysis
2. The risk assessment
3. Bank lending criteria:
   - Approve if score <50 (low risk)
   - Review if score 50-70 (medium risk)
   - Deny if score >70 (high risk)

Decision must include:
- Final decision (Approved/Denied/Review)
- Score (0-100)
- Reason (2-3 sentences)
- Conditions (if any)

Be firm and clear in your decision.""",
        expected_output="Final loan decision with score and justification",
        agent=manager
    )
    
    return analysis_task, risk_task, approval_task


# ============================================================================
# STEP 3: Create and run crew
# ============================================================================

def evaluate_loan_crewai(application: dict) -> dict:
    """
    Evaluate a loan using CrewAI crew execution.
    
    Flow:
    1. Create agents (Analyst, RiskAssessor, Manager)
    2. Create tasks (Analyze, Assess Risk, Approve)
    3. Create crew (coordinate agents and tasks)
    4. Execute crew (get final decision)
    """
    
    try:
        # Create agents
        agents_tuple = create_loan_evaluation_crew()
        analyst, risk_assessor, manager = agents_tuple
        
        # Create tasks
        tasks = create_loan_evaluation_tasks(application, agents_tuple)
        analysis_task, risk_task, approval_task = tasks
        
        # Create crew (orchestrates agents and tasks)
        crew = Crew(
            agents=[analyst, risk_assessor, manager],
            tasks=[analysis_task, risk_task, approval_task],
            verbose=True,  # Show execution details
            process="sequential"  # Execute tasks in order
        )
        
        # Execute crew (this runs the agents on the tasks)
        result = crew.kickoff()
        
        # Parse result into structured decision
        result_text = str(result)
        
        decision = {
            "decision": "review",  # Default
            "reason": result_text[:200],
            "score": 50,
            "factors": ["analyst_approved", "risk_assessed", "manager_decided"],
            "next_step": "Process application"
        }
        
        # Try to extract decision from result
        if "approved" in result_text.lower():
            decision["decision"] = "approved"
        elif "denied" in result_text.lower():
            decision["decision"] = "denied"
        
        return decision
        
    except Exception as e:
        return {
            "decision": "error",
            "reason": f"Error in crew execution: {str(e)}",
            "score": 0,
            "factors": [],
            "next_step": "Manual review required"
        }


# ============================================================================
# STEP 4: Pretty print
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
    print("LOAN EVALUATION SYSTEM - CREWAI")
    print("="*60)
    print("\nNote: This uses role-based agent team:")
    print("1. Loan Analyst: Analyzes financial data")
    print("2. Risk Assessor: Assesses risk profile")
    print("3. Loan Manager: Makes final decision")
    print("\nTasks are executed sequentially by the crew.")
    print("Clean abstraction over agent coordination.\n")
    
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
    print("\nStarting crew execution...\n")
    
    print("Loan Analyst would:")
    print("  - Calculate debt-to-income ratio")
    print("  - Calculate loan-to-income ratio")
    print("  - Assess credit quality")
    print("  - Check employment stability")
    print("\nRisk Assessor would:")
    print("  - Review analyst's findings")
    print("  - Assign risk score (0-100)")
    print("  - Identify key risk factors")
    print("\nLoan Manager would:")
    print("  - Make final decision")
    print("  - Provide reasoning")
    print("  - Set any conditions")
    
    # NOTE: Actual execution commented out (requires CrewAI with API setup)
    # Uncomment to run:
    # decision1 = evaluate_loan_crewai(good_app)
    # print_decision(decision1)
    
    
    print("\n" + "="*60)
    print("CREWAI ADVANTAGES SHOWN:")
    print("="*60)
    print("✓ Role-based agents (intuitive)")
    print("✓ Task-driven workflow (clear objectives)")
    print("✓ Clean API (simple to use)")
    print("✓ Delegation support (complex task routing)")
    print("✓ Sequential or parallel execution")
    print("✓ Good for team simulations")
    print("\nNOTE: This example shows the structure.")
    print("Real execution requires CrewAI with proper LLM config.")
