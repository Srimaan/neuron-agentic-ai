# WEEK 1, DAY 1: PROMPT ENGINEERING 101
## How to Instruct Claude to Make Good Decisions

> **Goal:** Understand how to structure prompts so Claude makes consistent, reliable decisions.
>
> **Real Use Case:** A bank needs to evaluate loan applications. You'll learn to prompt Claude to approve/deny loans correctly.
>
> **Time Commitment:** 90 minutes (lecture) + 120 minutes (hands-on)
>
> **Difficulty:** Beginner (but important foundation)

---

## THE PROBLEM

Imagine you're building an AI system for a bank that evaluates loan applications. You have Claude API access. Your first instinct:

```
"Claude, should we approve this loan?"
```

**What happens?**

Claude might say:
```
"I would need to see the applicant's credit score, income, 
employment status, loan amount, and other factors to make 
an informed decision. Could you provide more details?"
```

**The problem:** Claude doesn't know WHAT to decide or HOW to structure the answer. It's like asking a person to "make a decision" without context, criteria, or format expectations.

This is where **prompt engineering** comes in.

---

## WHAT IS PROMPT ENGINEERING?

**Simple definition:** Writing clear, specific instructions so Claude understands:
1. **What role to play** ("You are a loan officer")
2. **What information matters** ("Consider credit score, income, employment")
3. **What to decide** ("Approve, deny, or escalate to review")
4. **How to structure output** ("Format as JSON with decision and reason")

**Not magic.** It's just being specific and clear. Like explaining a task to a colleague.

---

## THE EVOLUTION: FROM BAD TO GOOD

Let's see how a prompt evolves from bad to good using our loan agent.

### **Version 1: Vague (❌ This fails)**

```
Evaluate this loan application.

Applicant: John Doe
Amount: $50,000
Credit Score: 750
Income: $100,000
Employment: Yes
```

**Claude's response:**
```
This applicant appears to have good credit and stable income. 
The $50,000 loan is reasonable given the income level. 
However, I would need more information about existing debts 
and employment duration to make a final recommendation.
```

**What's wrong?**
- No clear decision (approve/deny/review?)
- No structured format
- Vague output ("appears to," "would need")
- No clear rules to follow

### **Version 2: Better (✅ Getting closer)**

```
You are a loan officer evaluating applications.
Your job is to decide: Approved, Denied, or Review.

Decision rules:
- Credit score > 700: Good
- Credit score < 650: Poor
- Income > loan amount × 5: Can handle payment
- Employment status: Must be employed

Application:
Name: John Doe
Amount: $50,000
Credit Score: 750
Income: $100,000
Employment: Employed
```

**Claude's response:**
```
DECISION: Approved

Reasoning:
- Credit score of 750 is above 700 (Good)
- Income of $100,000 is 2× the loan amount of $50,000 (Can handle)
- Employment status is employed

This loan meets all criteria.
```

**What's better?**
- Clear decision required
- Explicit rules provided
- Structured output
- Better reasoning shown

**What's still missing?**
- No format specification (JSON, XML, etc.)
- No edge cases handled
- No reason for denial if denied

### **Version 3: Production-Ready (✅ This works)**

```
You are a loan evaluation system.

Your job: Evaluate loan applications and output a decision.

Output format (JSON):
{
  "decision": "approved" | "denied" | "review",
  "reason": "explanation of decision",
  "score": 0-100,
  "factors_considered": ["factor1", "factor2"]
}

Evaluation criteria:
- Credit score > 750: Excellent (+30 points)
- 700-750: Good (+20 points)
- < 650: Poor (deny unless exceptional)

- Debt-to-income < 0.3: Excellent (+25 points)
- 0.3-0.5: Good (+15 points)
- > 0.5: Poor (deny unless exceptional)

- Employment: Required (if missing, escalate to review)

Scoring:
- 80+: Approved
- 50-79: Review
- < 50: Denied

Exception: If score is 45-50 AND employment verified, escalate to review.

APPLICATION:
Name: John Doe
Credit Score: 750
Annual Income: $100,000
Existing Debt: $10,000
Loan Amount: $50,000
Employment: Employed (3 years)
```

**Claude's response:**
```json
{
  "decision": "approved",
  "reason": "Strong credit score (750, +30 points) and excellent debt-to-income ratio (0.1, +25 points). Total score: 85/100, well above approval threshold.",
  "score": 85,
  "factors_considered": [
    "credit_score_excellent",
    "debt_to_income_excellent",
    "employment_verified",
    "income_sufficient"
  ]
}
```

**Why this works:**
- ✅ Clear role ("loan evaluation system")
- ✅ Explicit format (JSON structure specified)
- ✅ Clear rules (points system)
- ✅ Thresholds defined (80+ = approve)
- ✅ Edge cases handled (exceptions)
- ✅ Structured output (machine-readable)

---

## KEY PRINCIPLES OF PROMPT ENGINEERING

### **Principle 1: Be Specific**

❌ **Bad:**
```
Evaluate this loan application.
```

✅ **Good:**
```
You are a loan evaluation system. Your job is to output a decision 
(approved/denied/review) based on these criteria...
```

### **Principle 2: Give Context**

❌ **Bad:**
```
Application: John Doe, $50k, 750 credit score
```

✅ **Good:**
```
John Doe is applying for a $50,000 loan.
His credit score is 750 (excellent range is 750+).
His annual income is $100,000.
He has been employed for 3 years.
```

### **Principle 3: Show Examples**

❌ **Bad:**
```
Decide if this loan should be approved.
```

✅ **Good:**
```
Example 1 (SHOULD APPROVE):
- Credit: 780, Income: $120k, Debt: $5k, Loan: $40k
- Decision: Approved (score 90+)

Example 2 (SHOULD DENY):
- Credit: 580, Income: $30k, Debt: $20k, Loan: $50k
- Decision: Denied (score 20, too risky)

Now evaluate this application:
[actual application]
```

### **Principle 4: Specify Format**

❌ **Bad:**
```
Tell me what you think about this loan.
```

✅ **Good:**
```
Output ONLY valid JSON. No other text.
{
  "decision": "approved" | "denied" | "review",
  "reason": "string (one sentence)",
  "confidence": 0-100
}
```

### **Principle 5: Define Constraints**

❌ **Bad:**
```
Be objective about this decision.
```

✅ **Good:**
```
Rules:
1. You MUST include a numeric score (0-100)
2. You MUST cite which criteria were considered
3. You MUST never approve if employment unverified
4. Do NOT make judgments beyond the criteria provided
```

---

## PROMPT ENGINEERING IN PRACTICE

### **Scenario: Bank's Loan System**

You're building the first version. Here's a complete, working prompt:

```
ROLE: You are an automated loan evaluation system for a community bank.

TASK: Evaluate loan applications and output a structured decision.

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
- Currently employed (20 points)
- Unemployed (0 points, escalate to review)
- Self-employed <1 year (escalate to review)
- Stable employment >2 years (+10 bonus)

Loan-to-Income Ratio:
- Loan < Annual Income × 3: Good (20 points)
- Loan < Annual Income × 5: Fair (10 points)
- Loan > Annual Income × 5: Poor (0 points, deny)

DECISION THRESHOLDS:
- 200+: Approved (low risk)
- 150-199: Approved (standard)
- 100-149: Review (borderline, escalate to human)
- <100: Denied (high risk)

EXCEPTIONS:
- If employment unverified: Always escalate to review (don't auto-deny)
- If credit <600: Escalate unless other factors exceptional
- If first-time homebuyer: Can adjust thresholds by -10

APPLICATION TO EVALUATE:
Name: John Doe
Credit Score: 750
Annual Income: $100,000
Existing Debt: $10,000 (monthly: ~$300)
Loan Amount: $50,000
Loan Duration: 60 months (5 years)
Employment: Employed, 4 years at current company
Purpose: Home improvement
Existing Assets: $50,000 savings

[Evaluate and output JSON]
```

**Claude's response:**
```json
{
  "decision": "approved",
  "reason": "Strong credit (750), excellent debt-to-income (0.09), stable employment (4 yrs), reasonable loan-to-income (0.5). Total score: 250/250.",
  "score": 250,
  "factors": [
    "credit_score_excellent",
    "dti_excellent", 
    "stable_employment_bonus",
    "loan_to_income_good",
    "sufficient_assets"
  ],
  "next_step": "Auto-approve and initiate loan origination process"
}
```

---

## PROMPT ENGINEERING IN ALL 5 FRAMEWORKS

The principles are the same across all frameworks. The difference is HOW you pass the prompt to Claude.

### **Framework 1: Raw Python SDK (Most Control)**

```python
from anthropic import Anthropic

client = Anthropic()

# Your prompt (from above)
SYSTEM_PROMPT = """You are an automated loan evaluation system..."""

# Application data
application = {
    "name": "John Doe",
    "credit_score": 750,
    "annual_income": 100000,
    ...
}

# Call Claude
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=500,
    system=SYSTEM_PROMPT,  # ← Role & rules
    messages=[
        {
            "role": "user",
            "content": f"Evaluate: {application}"
        }
    ]
)

print(message.content[0].text)
```

**Advantage:** You control everything. You see exactly what's sent to Claude.

### **Framework 2: LangChain (Abstraction)**

```python
from langchain.chat_models import ChatAnthropic
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage

chat = ChatAnthropic(model="claude-3-5-sonnet-20241022")

# Prompt template
prompt = ChatPromptTemplate.from_template(
    """You are an automated loan evaluation system...
    
    Evaluate this application: {application}
    
    Output JSON only."""
)

# Create messages
messages = [
    SystemMessage(content="You are a loan evaluation system..."),
    HumanMessage(content=f"Evaluate: {application}")
]

# Call Claude
response = chat(messages)
print(response.content)
```

**Advantage:** Less boilerplate. Templates for reuse.

### **Framework 3: LangGraph (Workflow)**

```python
from langgraph.graph import StateGraph, END
from langchain.chat_models import ChatAnthropic

graph_builder = StateGraph(dict)

# Add node (evaluation step)
def evaluate_loan(state):
    client = ChatAnthropic(model="claude-3-5-sonnet-20241022")
    
    prompt = """You are an automated loan evaluation system...
    
    Application: {application}"""
    
    result = client.invoke(prompt.format(application=state["application"]))
    state["decision"] = result.content
    return state

graph_builder.add_node("evaluate", evaluate_loan)
graph_builder.set_entry_point("evaluate")
graph_builder.add_edge("evaluate", END)

graph = graph_builder.compile()

# Run
result = graph.invoke({"application": {...}})
```

**Advantage:** Part of larger workflow. Explicitly defined steps.

### **Framework 4: AutoGen (Multi-Agent)**

```python
import autogen

# Agent with prompt instructions
agent = autogen.AssistantAgent(
    name="loan_evaluator",
    system_message="You are an automated loan evaluation system..."
)

# User proxy (simulates user)
user = autogen.UserProxyAgent(
    name="user",
    human_input_mode="NEVER"
)

# Conversation
user.initiate_chat(
    agent,
    message="Evaluate this loan application: [details]"
)
```

**Advantage:** Multi-agent conversations. Agent collaboration.

### **Framework 5: CrewAI (Role-Based)**

```python
from crewai import Agent, Task, Crew

agent = Agent(
    role="Loan Evaluation Officer",
    goal="Accurately evaluate loan applications",
    backstory="You have 10 years of banking experience...",
    allow_delegation=False
)

task = Task(
    description="Evaluate this loan application: [details]",
    expected_output="JSON with decision, reason, and score",
    agent=agent
)

crew = Crew(agents=[agent], tasks=[task])
result = crew.kickoff()
```

**Advantage:** Role-based abstraction. Clear responsibilities.

---

## WHY PROMPT ENGINEERING MATTERS

### **Good Prompts = Good Decisions**

Compare these two loan decisions:

**Poor Prompt:**
```
Should we approve this loan?
```
Claude: "It depends on several factors. More information needed."
❌ No decision made

**Good Prompt:**
```
Evaluate using these rules:
- Credit > 750: 80 pts
- DTI < 0.25: 80 pts
- Employed: 20 pts
- Threshold 150+: Approve

Score: 250/250 based on criteria above.
```
Claude: 
```json
{
  "decision": "approved",
  "score": 250,
  "reason": "Meets all criteria"
}
```
✅ Clear decision

### **Common Mistakes**

❌ **Mistake 1: Assuming Claude knows context**
```
"Is this a good loan?"
```
Claude doesn't know YOUR rules. Tell it.

❌ **Mistake 2: Vague instructions**
```
"Be objective."
```
What does objective mean? Give specific criteria.

❌ **Mistake 3: Forgetting examples**
```
"Decide if approved."
```
Show examples of approved and denied.

❌ **Mistake 4: Not specifying format**
```
"Give me the result."
```
JSON? Natural language? Structured table?

✅ **Do this instead:**
```
Role: Loan evaluator
Rules: [specific criteria]
Format: JSON with {decision, reason, score}
Examples: [what approve/deny looks like]
```

---

## YOUR FIRST PROMPT EXERCISE

**The Challenge:** Write a prompt that makes Claude evaluate this loan consistently.

```
Applicant: Jane Smith
Credit Score: 680
Income: $75,000
Debt: $15,000/year
Loan Amount: $40,000
Employment: Employed (2 years)

You need to write a prompt that Claude will follow EVERY TIME,
always outputting the same format.
```

**What to include:**
1. Clear role
2. Specific rules
3. Scoring system
4. Decision thresholds
5. JSON format
6. At least one example

*Solution provided in exercises below.*

---

## KEY TAKEAWAYS

1. **Prompts are instructions.** They tell Claude what to do.

2. **Be specific.** Vague prompts = vague answers.

3. **Give context.** Explain the rules and criteria.

4. **Show examples.** "This should approve. This should deny."

5. **Specify format.** JSON, plain text, structured output.

6. **Define thresholds.** When to approve, deny, escalate.

7. **Handle exceptions.** What if credit score is low but income high?

8. **Test your prompt.** Does Claude behave consistently?

---

## WHAT'S NEXT

Tomorrow: **Context Engineering** (how to feed real data to Claude)

But first: Complete the exercises below. Write and test your prompts.

---

## QUICK REFERENCE: Prompt Template

Use this template for your own AI systems:

```
ROLE: You are a [specific role].

TASK: Your job is to [specific task].

INPUT FORMAT:
[Describe what information you'll receive]

OUTPUT FORMAT (EXACT):
[Show the exact format - JSON, XML, etc.]

EVALUATION CRITERIA:
[List specific rules/thresholds]

DECISION THRESHOLDS:
[When to approve/deny/escalate]

EXCEPTIONS:
[Edge cases to handle]

APPLICATION/DATA:
[Actual data to evaluate]
```

---

**Ready for code examples? Check the Python files next.**
**Ready for exercises? See the exercises document.**
**Ready for setup? See the Docker setup guide.**
