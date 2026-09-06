# WEEK 1, DAY 1: EXERCISES
## Prompt Engineering Practice

---

## EXERCISE 1: Write a Loan Evaluation Prompt
**Difficulty:** Easy  
**Time:** 30 minutes  
**Goal:** Write a prompt that makes Claude consistently evaluate loans

### Challenge

You work at a bank. Write a prompt that Claude will follow EVERY TIME to produce the same output format.

**Requirements:**
1. ✓ Clear role definition
2. ✓ Specific evaluation criteria
3. ✓ Scoring system (how to calculate score)
4. ✓ Decision thresholds (when to approve/deny/review)
5. ✓ Output format (JSON structure)
6. ✓ At least one example

**Test Case:**
```
Applicant: Jane Smith
Credit Score: 680
Annual Income: $75,000
Monthly Debt: $1,200
Loan Amount: $40,000
Employment: Employed, 2 years
Purpose: Car purchase
Savings: $12,000
```

Your prompt should produce:
- Clear JSON output
- Same format every time
- Numeric score
- Decision with reasoning

### Solution

Here's a complete, production-ready prompt:

```
ROLE: You are a loan evaluation system.

OUTPUT FORMAT (JSON ONLY):
{
  "decision": "approved" | "denied" | "review",
  "reason": "brief justification",
  "score": 0-100,
  "debt_to_income": number,
  "loan_to_income": number,
  "factors": ["list", "of", "factors"]
}

SCORING SYSTEM:

Credit Score:
- 750+: 80 points (excellent)
- 700-749: 60 points (good)
- 650-699: 40 points (fair)
- <650: 0 points (poor)

Debt-to-Income Ratio (monthly debt / monthly income):
- <0.25: 80 points (excellent)
- 0.25-0.35: 60 points (good)
- 0.36-0.45: 40 points (fair)
- >0.45: 0 points (poor)

Employment:
- Current & stable (>2 years): 20 points
- Current & newer (<2 years): 10 points
- Unemployed: 0 points (escalate)

Loan-to-Income:
- <3x annual income: 20 points (excellent)
- 3-5x: 10 points (good)
- >5x: 0 points (poor)

DECISION THRESHOLDS:
- 200+: Approved (low risk)
- 150-199: Approved (standard risk)
- 100-149: Review (medium risk, escalate)
- <100: Denied (high risk)

CALCULATE AND PROVIDE EXACT NUMBERS.

Application to evaluate:
{application data}
```

---

## EXERCISE 2: Identify Problems in Broken Prompts
**Difficulty:** Easy  
**Time:** 20 minutes  
**Goal:** Find what's wrong with poorly written prompts

### Challenge

For each prompt below, identify:
1. What's wrong (specific problems)
2. How it could fail
3. How to fix it

### Prompt A (❌ Too Vague)

```
Evaluate this loan application and tell me if it's good or bad.

Applicant: John, credit 750, income $100k, loan $50k
```

**Problems:**
1. ❌ No clear decision format ("good or bad" is vague)
2. ❌ No evaluation criteria specified
3. ❌ No scoring system
4. ❌ No JSON format specified
5. ❌ Claude won't know what to output

**How it fails:**
Claude might output: "This looks like a reasonable application. The credit score is good and the income is sufficient. However, I would need more information..."

**Fix:**
Add specific criteria, scoring system, and output format (as shown in Exercise 1).

---

### Prompt B (❌ Ambiguous Rules)

```
You are a loan officer. Approve loans if they seem reasonable.

Credit: 750, Income: $100k, Loan: $50k
```

**Problems:**
1. ❌ "Seem reasonable" is subjective (not defined)
2. ❌ No numerical thresholds
3. ❌ No decision options (approve/deny/review)
4. ❌ No output format specified
5. ❌ Claude will guess what "reasonable" means

**How it fails:**
Claude might approve based on different criteria than you expect.

**Fix:**
Define "reasonable" explicitly:
- "Approve if score > 150"
- "Deny if credit < 650"
- "Review if employment unverified"

---

### Prompt C (❌ Missing Examples)

```
Evaluate this loan. Provide your analysis.

Credit: 650, Income: $40k, Loan: $50k, Debt: $2k/month
```

**Problems:**
1. ❌ No examples of approved/denied loans
2. ❌ Claude doesn't know what "good" looks like
3. ❌ Decisions will be inconsistent
4. ❌ No reference point

**How it fails:**
Claude might approve a risky loan (no bad example shown).

**Fix:**
Add examples:
```
Example (SHOULD DENY):
Credit: 580, Income: $30k, Loan: $50k, Debt: $2k/month
Reason: High risk - low credit, high debt-to-income

Example (SHOULD APPROVE):
Credit: 750, Income: $100k, Loan: $50k, Debt: $500/month
Reason: Low risk - excellent credit, low debt-to-income
```

---

## EXERCISE 3: Test Prompt Consistency
**Difficulty:** Medium  
**Time:** 40 minutes  
**Goal:** Test if a prompt produces consistent results

### Challenge

Write code (using any of the 5 frameworks) that:
1. Takes 3 different applications
2. Evaluates each with your prompt (from Exercise 1)
3. Shows the 3 decisions
4. Checks if decisions are consistent

**Requirements:**
- Use the prompt from Exercise 1
- Test with 3 applications of different risk levels (good, borderline, risky)
- Show all 3 decisions
- Verify format consistency

### Solution

Here's a testing script (using raw Python SDK):

```python
import json
from anthropic import Anthropic

client = Anthropic()

# Your system prompt from Exercise 1
SYSTEM_PROMPT = """[Your prompt here]"""

def test_loan(application: dict, test_num: int):
    """Test one application."""
    print(f"\n{'='*60}")
    print(f"TEST {test_num}: {application['name']}")
    print(f"{'='*60}")
    
    # Format application
    app_text = f"""
Name: {application['name']}
Credit: {application['credit_score']}
Income: ${application['annual_income']:,}
Debt/month: ${application['debt_per_year']/12:,.0f}
Loan: ${application['loan_amount']:,}
Employment: {application['employment']}
"""
    
    # Call Claude
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": app_text}]
    )
    
    response = message.content[0].text
    print(f"Response:\n{response}")
    
    # Try to parse JSON
    try:
        decision = json.loads(response)
        print(f"\nParsed Decision:")
        print(f"  Decision: {decision['decision']}")
        print(f"  Score: {decision.get('score', 'N/A')}")
        return decision
    except:
        print("\n⚠️  Could not parse JSON!")
        print("   (Your prompt may need adjustment)")
        return None

# Test cases
test_cases = [
    {
        "name": "GOOD: Strong applicant",
        "credit_score": 750,
        "annual_income": 100000,
        "debt_per_year": 10000,
        "loan_amount": 50000,
        "employment": "Employed, 4 years"
    },
    {
        "name": "BORDERLINE: Medium risk",
        "credit_score": 680,
        "annual_income": 60000,
        "debt_per_year": 18000,
        "loan_amount": 40000,
        "employment": "Employed, 1 year"
    },
    {
        "name": "RISKY: High risk",
        "credit_score": 580,
        "annual_income": 40000,
        "debt_per_year": 24000,
        "loan_amount": 50000,
        "employment": "Unemployed"
    }
]

# Run tests
results = []
for i, test_case in enumerate(test_cases, 1):
    result = test_loan(test_case, i)
    if result:
        results.append(result)

# Verify consistency
print(f"\n{'='*60}")
print("CONSISTENCY CHECK")
print(f"{'='*60}")

if results:
    # Check format consistency
    keys_in_first = set(results[0].keys()) if results else set()
    
    for i, result in enumerate(results, 1):
        keys_in_result = set(result.keys())
        if keys_in_first != keys_in_result:
            print(f"⚠️  Test {i} has different JSON structure!")
        else:
            print(f"✓ Test {i} has consistent format")
    
    # Check decisions
    print(f"\nDecisions:")
    print(f"  Test 1 (Good): {results[0]['decision']}")
    if results[1]['decision'] in ['approved', 'review']:
        print(f"  Test 2 (Borderline): {results[1]['decision']} ✓")
    else:
        print(f"  Test 2 (Borderline): {results[1]['decision']} (unexpected)")
    
    if results[2]['decision'] in ['denied', 'review']:
        print(f"  Test 3 (Risky): {results[2]['decision']} ✓")
    else:
        print(f"  Test 3 (Risky): {results[2]['decision']} (unexpected)")
```

### Expected Output

If your prompt is good:
```
TEST 1: Good applicant
Response: {JSON with decision: "approved", score: 200+}
✓ Test 1 has consistent format

TEST 2: Borderline
Response: {JSON with decision: "review", score: 100-150}
✓ Test 2 has consistent format

TEST 3: Risky
Response: {JSON with decision: "denied", score: <100}
✓ Test 3 has consistent format

✓ Test 1 (Good): approved
✓ Test 2 (Borderline): review
✓ Test 3 (Risky): denied
```

---

## EXERCISE 4: Adapt Prompt for Different Frameworks
**Difficulty:** Medium  
**Time:** 45 minutes  
**Goal:** Use your prompt in different frameworks

### Challenge

Take your prompt from Exercise 1 and adapt it for:
1. LangChain (using ChatPromptTemplate)
2. LangGraph (as system prompt in a node)

Show that the same prompt works in all frameworks.

### Solution

**Adapt for LangChain:**

```python
from langchain.prompts import ChatPromptTemplate

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a loan evaluation system..."),
    ("human", "Evaluate: {application}")
])

# Use it
formatted = prompt_template.format_prompt(
    application="Credit: 750, Income: $100k..."
)
```

**Adapt for LangGraph:**

```python
from langgraph.graph import StateGraph

# Use same prompt in system message
message = {
    "role": "system",
    "content": "You are a loan evaluation system..."
}
```

**Key insight:** The core prompt doesn't change. Only HOW you pass it to Claude changes.

---

## EXERCISE 5: Improve Prompt Based on Failures
**Difficulty:** Hard  
**Time:** 60 minutes  
**Goal:** Debug and improve a prompt that's failing

### Challenge

Imagine your initial prompt is producing inconsistent results. The prompt approves some risky loans and denies some good loans.

Write the improved prompt that:
1. More clearly defines thresholds
2. Adds more context
3. Includes edge case handling
4. Has better examples

### Solution

Here's an improved prompt with better edge case handling:

```
ROLE: You are a loan evaluation system for a bank.

CRITICAL RULES:
1. ALWAYS output valid JSON
2. ALWAYS calculate exact numbers
3. NEVER approve if employment unverified
4. NEVER approve if credit < 600
5. ALWAYS escalate borderline cases

OUTPUT FORMAT (MUST BE VALID JSON):
{
  "decision": "approved" | "denied" | "review",
  "reason": "specific reason citing criteria",
  "score": number (0-100),
  "factors_positive": ["factor1"],
  "factors_negative": ["factor2"],
  "edge_cases": ["if applicable"],
  "next_step": "description"
}

SCORING (BE EXACT):

Credit Score Analysis:
- 750+: +80 pts | Classification: Excellent | Risk: Low
- 700-749: +60 pts | Classification: Good | Risk: Low
- 650-699: +40 pts | Classification: Fair | Risk: Medium
- <650: 0 pts | WARN: High risk | Action: Check other factors

[... more detailed rules ...]

DECISION LOGIC (MUST FOLLOW):
- Score 200+: APPROVED (can approve directly)
- Score 150-199: APPROVED (standard approval)
- Score 100-149: REVIEW (must escalate to human)
- Score <100: DENIED (must deny)

EXCEPTION HANDLING:
IF credit <600 AND employment unverified: MUST ESCALATE
IF debt-to-income >0.5 AND credit <700: MUST ESCALATE
IF assets <$5k AND loan-to-income >5: MUST REVIEW

REQUIRED FIELDS IN JSON:
- "decision" (must be exactly: "approved", "denied", or "review")
- "score" (must be integer 0-100)
- "reason" (must cite specific criteria)
- "factors_positive" (list of positive factors)
- "factors_negative" (list of risk factors)
```

**Key improvements:**
1. More explicit rules (MUST ESCALATE, NEVER approve)
2. Better edge case handling
3. More detailed JSON structure
4. Required field validation
5. Clearer exception handling

---

## EXERCISE 6 (BONUS): Write Test Cases for Your Prompt
**Difficulty:** Medium  
**Time:** 30 minutes  
**Goal:** Create test cases to validate your prompt works

### Challenge

Write 5 test applications that should test different scenarios:
1. Clear approval (high credit, low debt)
2. Clear denial (low credit, high debt)
3. Borderline/review (medium everything)
4. Edge case 1 (unemployed)
5. Edge case 2 (very high debt-to-income)

### Solution

```python
test_cases = [
    {
        "name": "Clear Approval",
        "credit_score": 780,
        "annual_income": 120000,
        "debt_per_year": 6000,
        "loan_amount": 40000,
        "employment": "Employed, 5+ years",
        "expected": "approved"
    },
    {
        "name": "Clear Denial",
        "credit_score": 550,
        "annual_income": 30000,
        "debt_per_year": 18000,
        "loan_amount": 50000,
        "employment": "Unemployed",
        "expected": "denied"
    },
    {
        "name": "Borderline Review",
        "credit_score": 700,
        "annual_income": 60000,
        "debt_per_year": 18000,
        "loan_amount": 35000,
        "employment": "Employed, 1 year",
        "expected": "review"
    },
    {
        "name": "Edge Case: Unemployed",
        "credit_score": 750,
        "annual_income": 0,
        "debt_per_year": 0,
        "loan_amount": 50000,
        "employment": "Unemployed",
        "expected": "review"  # Must escalate
    },
    {
        "name": "Edge Case: High DTI",
        "credit_score": 700,
        "annual_income": 40000,
        "debt_per_year": 24000,
        "loan_amount": 50000,
        "employment": "Employed, 2 years",
        "expected": "review"  # High debt-to-income
    }
]
```

---

## SUMMARY: What You Learned

After these exercises, you understand:

1. ✅ How to write clear prompts
2. ✅ The importance of specific criteria
3. ✅ JSON output formatting
4. ✅ Scoring systems and thresholds
5. ✅ Testing prompt consistency
6. ✅ Framework-agnostic prompts
7. ✅ Edge case handling
8. ✅ Prompt debugging

---

## NEXT STEPS

1. Complete all 6 exercises
2. Run the code examples to see them work
3. Modify the prompts to test your understanding
4. Read tomorrow's topic: Context Engineering

---

**Ready to test your prompts? Run the examples and exercises now!**
