# 16-WEEK LEARNING PATH
## Production AI Bootcamp - Detailed Schedule

---

## PHASE 1: FOUNDATIONS (Weeks 1-2)

### **Week 1: Five Engineering Disciplines**

**Goal:** Understand the fundamental layers that power production agents.

| Day | Topic | Duration | Format | Learning Outcomes | Status |
|-----|-------|----------|--------|------------------|--------|
| 1 | Prompt Engineering 101 | 120 min | WHITE bg lecture | Understand how prompts guide agent behavior | To Build |
| 2 | Context Engineering 101 | 120 min | WHITE bg lecture | Learn how to structure data for agents | To Build |
| 3 | Harness Engineering 101 | 120 min | WHITE bg lecture | Learn tool design and integration patterns | To Build |
| 4 | Loop Engineering 101 | 120 min | WHITE bg lecture | Understand iteration, feedback, exit conditions | To Build |
| 5 | Graph Engineering 101 | 120 min | WHITE bg lecture | Learn workflow orchestration and branching | To Build |
| 6 | Why Each Layer Exists | 180 min | GRAY bg deep dive | See how each layer solves a different problem | To Build |
| 7-8 | Integration & Setup | 240 min | WHITE bg hands-on | Set up local dev environment with Docker | To Build |

**Week 1 Details:**

**Day 1: Prompt Engineering**
```
Problems Covered:
├─ How to structure instructions for Claude
├─ Few-shot vs zero-shot prompting
├─ Prompt versioning and iteration
├─ Role prompting ("You are a loan officer")
└─ Chain-of-thought prompting

Hands-on:
├─ Write 3 different prompts for loan approval
├─ See how output changes
├─ Learn what makes a good vs bad prompt

Resources:
├─ Anthropic prompt guide
├─ Real examples from Sentinel AI
├─ Claude documentation
└─ Best practices checklist

Key Takeaway:
"Prompts are like instructions to a human. 
Be clear, specific, and show examples."
```

**Day 2: Context Engineering**
```
Problems Covered:
├─ How to feed real data to agents
├─ Structuring context windows
├─ Context size limitations
├─ Information retrieval
└─ Dynamic context updates

Hands-on:
├─ Add customer data to prompt
├─ See improvement in decisions
├─ Learn when context isn't enough

Resources:
├─ Context window management
├─ Token counting tools
├─ Vector DB introduction
└─ Real world context examples

Key Takeaway:
"Better information → Better decisions.
But context window is finite."
```

**Day 3: Harness Engineering**
```
Problems Covered:
├─ Tool design patterns
├─ Function calling vs API calls
├─ Tool validation
├─ Error handling
└─ Tool composition

Hands-on:
├─ Build 2 simple tools (credit check, verification)
├─ Integrate with agent
├─ Handle tool failures

Resources:
├─ Claude tool use guide
├─ Tool design best practices
├─ Error handling patterns
└─ Real API integration examples

Key Takeaway:
"Tools let agents affect the real world.
But tools can fail. Plan for it."
```

**Day 4: Loop Engineering**
```
Problems Covered:
├─ Four-phase loop structure
├─ State management
├─ Exit conditions
├─ Retry logic
└─ Feedback collection

Hands-on:
├─ Build basic agent loop
├─ Add retry logic
├─ Test exit conditions

Resources:
├─ Loop patterns (gather → reason → act → observe)
├─ State machines
├─ Iterator patterns
└─ Production loop examples

Key Takeaway:
"One shot rarely works. 
Loops with feedback create intelligence."
```

**Day 5: Graph Engineering**
```
Problems Covered:
├─ Linear vs branching workflows
├─ State machines
├─ Node and edge design
├─ Parallel execution
└─ Conditional routing

Hands-on:
├─ Build graph for loan decisions
├─ Add multiple paths
├─ Test routing logic

Resources:
├─ LangGraph introduction
├─ State machine patterns
├─ DAG vs cyclic graphs
└─ Real workflow examples

Key Takeaway:
"Graphs handle complexity that loops can't.
Use when decisions have multiple paths."
```

**Day 6: Why Each Layer Exists**
```
Deep Dive Format (GRAY box):

Question: Why do we need all 5 layers?

Story Arc:
1. "Just ask Claude" (Prompt only)
   └─ Problem: Doesn't work without data

2. Add context (Prompt + Context)
   └─ Problem: Still can't do anything

3. Add tools (Prompt + Context + Tools)
   └─ Problem: One-shot isn't enough

4. Add loops (Prompt + Context + Tools + Loops)
   └─ Problem: Can't handle complex workflows

5. Add graphs (Prompt + Context + Tools + Loops + Graphs)
   └─ Solution: Now we have production system

Why certification covers all 5:
├─ Each solves real problems
├─ Must understand tradeoffs
├─ Can't skip any in production
└─ Different use cases need different emphasis
```

**Days 7-8: Local Setup**
```
Installation:
├─ Python 3.11+
├─ Claude SDK: pip install anthropic
├─ Docker Desktop
├─ PostgreSQL (Docker): docker run -d postgres:15
├─ Redis (Docker): docker run -d redis:7
└─ Git + GitHub

Validation:
├─ Run: python -c "import anthropic; print(anthropic.__version__)"
├─ Test Docker: docker ps
├─ Test databases: psql -U postgres (should connect)
└─ Clone starter repo

Outcome:
"Everyone has same dev environment. 
Ready to start building Day 1 Week 2."
```

---

### **Week 2: Evolution Story - V1→V5**

**Goal:** See each engineering layer solve a specific problem through one real use case.

| Day | Version | Problem | Solution | Output | Status |
|-----|---------|---------|----------|--------|--------|
| 1 | V1: Prompt Only | No data access | Add context | Decisions guess | To Build |
| 2 | V2: Context | Rigid static data | Database queries | Better decisions | To Build |
| 3 | V3: Harness | Can't verify data | Add tools | Real verification | To Build |
| 4 | V4: Loops | One shot not enough | Add iteration | Clarification questions | To Build |
| 5 | V5: Graph | Linear can't route | State machine | Multiple paths | To Build |
| 6 | V5+: Verify | How know if good? | Add testing framework | Quality metrics | To Build |
| 7-8 | Integration | Full system | All layers | Production agent | To Build |

**Week 2 Details:**

**Day 1: V1 - Prompt Engineering Only**

```
Scenario: Bank wants to evaluate loan applications

Agent: Just Claude + prompt
├─ No access to applicant data
├─ No loan rules
├─ No tool integration
└─ One-shot response

Code Structure (50 lines):
```python
from anthropic import Anthropic

client = Anthropic()

prompt = """You are a loan officer. 
Evaluate this loan application and decide: Approved/Denied/Review.
Always explain your reasoning.

Application: {application}
"""

def evaluate_loan(application):
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt.format(application=application)}
        ]
    )
    return message.content[0].text

# Test
result = evaluate_loan("$50,000 loan, 750 credit score, $100k income")
print(result)
```

Problems Discovered:
```
❌ "I don't have access to the applicant's employment status"
❌ "I can't verify their credit score"
❌ "I'm guessing without real data"
❌ "One response isn't thorough enough"

Why it fails:
├─ No ground truth data
├─ Can't verify anything
├─ No clear decision criteria
└─ No way to improve answer
```

Learnings:
```
✓ Understand baseline
✓ See prompt limitations
✓ This is why V2 exists
```

---

**Day 2: V2 - Add Context Engineering**

```
Solution: Add applicant data and loan rules to prompt

Code Structure (100 lines):
```python
# Load structured data
applicant = {
    "name": "John Doe",
    "credit_score": 750,
    "annual_income": 100000,
    "employment": "employed",
    "debt_to_income": 0.25,
    "loan_amount": 50000,
    "loan_term": 60
}

loan_rules = """
Approval criteria:
- Credit score > 700: Good
- Credit score > 750: Excellent
- Debt-to-income < 0.50: Good
- Employment status verified: Required
- Loan amount < income × 5: Acceptable
"""

prompt = f"""You are a loan officer.
Use these rules: {loan_rules}

Applicant: {applicant}

Decision: Approved/Denied/Review (cite rules)
"""

def evaluate_loan_v2(applicant):
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text
```

Problems Discovered:
```
✓ Claude can now use real data
✓ Better decisions (cites rules)

BUT:
❌ Rules are hard-coded in prompt
❌ Can't handle changes easily
❌ No way to query credit score API
❌ One-shot still isn't enough for verification
```

Learnings:
```
✓ Real data is crucial
✓ But context is static
✓ Can't do dynamic lookups
✓ This is why V3 exists
```

---

**Day 3: V3 - Add Harness Engineering (Tools)**

```
Solution: Add real tool integration

Code Structure (200 lines):
```python
import json
import anthropic

client = anthropic.Anthropic()

# Define tools
tools = [
    {
        "name": "check_credit_score",
        "description": "Check applicant's credit score from credit bureau",
        "input_schema": {
            "type": "object",
            "properties": {
                "ssn": {"type": "string", "description": "Social Security Number"}
            }
        }
    },
    {
        "name": "verify_employment",
        "description": "Verify employment status with employer",
        "input_schema": {
            "type": "object",
            "properties": {
                "employer_name": {"type": "string"},
                "employee_id": {"type": "string"}
            }
        }
    },
    {
        "name": "check_collateral",
        "description": "Get market value of collateral",
        "input_schema": {
            "type": "object",
            "properties": {
                "property_id": {"type": "string"}
            }
        }
    }
]

def check_credit_score(ssn):
    # Mock API call
    return {"score": 750, "source": "Equifax"}

def verify_employment(employer_name, employee_id):
    return {"verified": True, "status": "active"}

def check_collateral(property_id):
    return {"value": 250000, "date": "2024-08-26"}

# Execute tool
def execute_tool(name, input_params):
    if name == "check_credit_score":
        return check_credit_score(**input_params)
    elif name == "verify_employment":
        return verify_employment(**input_params)
    elif name == "check_collateral":
        return check_collateral(**input_params)

def evaluate_loan_v3(applicant):
    messages = [
        {"role": "user", "content": f"Evaluate loan for {applicant['name']}"}
    ]
    
    while True:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            tools=tools,
            messages=messages
        )
        
        # Check if done
        if response.stop_reason == "end_turn":
            return response.content[0].text
        
        # Process tool calls
        for block in response.content:
            if block.type == "tool_use":
                tool_result = execute_tool(block.name, block.input)
                messages.append({
                    "role": "assistant",
                    "content": response.content
                })
                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(tool_result)
                        }
                    ]
                })
                break
```

Problems Discovered:
```
✓ Can call real APIs
✓ Can verify data
✓ Better decisions

BUT:
❌ One-shot tool calls (no retries)
❌ Can't ask clarifying questions
❌ Can't handle complex workflows
❌ No decision branching
```

Learnings:
```
✓ Tools are powerful
✓ Error handling matters
✓ But linear isn't enough
✓ This is why V4 exists
```

---

**Day 4: V4 - Add Loop Engineering**

```
Solution: Add agentic loop with state management

Code Structure (400 lines - see full repo):
Key additions:
├─ Loop controller (gather → reason → act → observe)
├─ State management (what's decided so far?)
├─ Retry logic (what if tool fails?)
├─ Clarification questions (ask for more info)
└─ Exit conditions (when to stop)

Problems Discovered:
```
✓ Can handle complexity
✓ Can ask questions
✓ Can retry failures

BUT:
❌ All paths linear
❌ Can't say "check this AND that separately"
❌ Can't parallel process
❌ Always sequential
```

Learnings:
```
✓ Loops are powerful
✓ State matters
✓ But linear is limiting
✓ This is why V5 exists
```

---

**Day 5: V5 - Add Graph Engineering**

```
Solution: State machine with branching paths

Loan Decision Graph:
```
[START: Loan Application]
    ↓
[GATHER: Collect applicant data]
    ├─→ Can proceed? 
    │   ├─ No → [DENY: Insufficient info]
    │   └─ Yes ↓
    ├→ [VERIFY_CREDIT: Check score]
    ├→ [VERIFY_EMPLOYMENT: Confirm job]
    ├→ [VERIFY_COLLATERAL: Get property value]
    │   ↓
    ├→ [ANALYZE: Score all factors]
        ↓
        ├─→ Clear approval?
        │   └─ Yes → [APPROVE: Set terms]
        ├─→ Clear denial?
        │   └─ Yes → [DENY: Reason]
        └─→ Unclear?
            └─ Yes → [ESCALATE: Human review]
```

Problems Discovered:
```
✓ Complex workflows work
✓ Multiple paths handled
✓ Can parallelize checks

BUT:
❌ How do you know decisions are good?
❌ What if agent is biased?
❌ What if it makes mistakes?
❌ How do you monitor in production?
```

Learnings:
```
✓ V5 is complete agent
✓ But not production yet
✓ This is why verification exists
```

---

**Day 6: V5+ - Add Verification Layer**

```
Solution: Evals, Governance, Monitoring

Verification Suite:
```
After agent decides:
├─ Schema Check: Is output valid JSON?
├─ Business Check: Follows loan rules?
├─ Governance Check: Any bias detected?
├─ Compliance Check: PII, regulations?
└─ Quality Check: Evals score high?

If all pass → Execute decision
If any fail → Escalate to human
```

Problems Solved:
```
✓ Catch agent mistakes
✓ Detect bias
✓ Ensure compliance
✓ Monitor quality

Remaining question:
"How do we know this works at scale?"
This is why observability exists.
```

---

**Days 7-8: Complete Integration**

```
Combine all layers:
├─ V1 (Prompt): Instructions
├─ V2 (Context): Data feeding
├─ V3 (Harness): Tools & APIs
├─ V4 (Loops): Iteration
├─ V5 (Graph): Workflows
└─ V5+ (Verify): Quality assurance

Outcomes:
✓ Understand why each layer exists
✓ See evolution in action
✓ Ready for frameworks (Week 3-4)
✓ Ready for production patterns (Week 10+)
```

---

## PHASE 2: LOAN APPLICATION EVOLUTION (Weeks 3-4)

### **Week 3: V1→V3 Implementation**

| Day | Focus | Repo | Lines | Key Skills | Status |
|-----|-------|------|-------|------------|--------|
| 1 | V1: Prompt | loan-v1/ | 50 | Prompt structure | To Build |
| 2 | V2: Context | loan-v2/ | 100 | Data feeding | To Build |
| 3 | V3: Harness | loan-v3/ | 200 | Tool integration | To Build |
| 4 | V3: Error handling | loan-v3/ | 250 | Resilience | To Build |
| 5 | V3: Testing | loan-v3/ | 300 | Unit tests | To Build |
| 6-7 | Review & Extend | loan-v3/ | 350+ | Experimentation | To Build |

**Code structure for each:**
```
loan-application-evolution/v1-prompt-only/
├── agent.py (main agent)
├── example.py (how to use)
├── tests.py (unit tests)
├── results.md (what works/fails)
├── learnings.md (key takeaways)
└── README.md (setup & run)
```

---

### **Week 4: V4→V5 Implementation**

| Day | Focus | Repo | Key Skills | Status |
|-----|-------|------|------------|--------|
| 1-2 | V4: Loops | loan-v4/ | Loop patterns, state | To Build |
| 3-4 | V5: Graph | loan-v5/ | State machines, routing | To Build |
| 5 | V5+: Verification | loan-v5/ | Evals, governance | To Build |
| 6-7 | Integration test | loan-v5/ | Full pipeline testing | To Build |

---

## PHASE 3: FRAMEWORKS (Weeks 5-7)

### **Week 5: Raw Python SDK + LangChain**

| Framework | Approach | Complexity | Best For | Status |
|-----------|----------|-----------|----------|--------|
| Raw Python + SDK | Maximum control | High | Learning, custom | To Build |
| LangChain | Components | Medium | Rapid dev | To Build |

---

### **Week 6: LangGraph + AutoGen**

| Framework | Approach | Complexity | Best For | Status |
|-----------|----------|-----------|----------|--------|
| LangGraph | State machines | Medium | Complex workflows | To Build |
| AutoGen | Multi-agent | High | Agent teams | To Build |

---

### **Week 7: CrewAI + Comparison**

| Framework | Approach | Complexity | Best For | Status |
|-----------|----------|-----------|----------|--------|
| CrewAI | Role-based | Low | Role hierarchies | To Build |
| Comparison | All side-by-side | - | Decision making | To Build |

---

## PHASE 4: SYSTEM COMPONENTS (Weeks 8-9)

### **Week 8: RAG + MCP**

| Topic | Depth | Key Skills | Status |
|-------|-------|-----------|--------|
| RAG Fundamentals | Concept | Why RAG matters | To Build |
| Vector Databases | Hands-on | Embeddings, retrieval | To Build |
| RAG Implementation | Full code | Document loading, ranking | To Build |
| Agent + RAG | Integration | Memory + retrieval | To Build |
| MCP Introduction | Concept | Tool standardization | To Build |
| MCP Implementation | Hands-on | Build custom tools | To Build |

---

### **Week 9: Memory + Token Optimization**

| Topic | Depth | Key Skills | Status |
|-------|-------|-----------|--------|
| Session Memory | Hands-on | Redis patterns | To Build |
| Persistent Memory | Hands-on | PostgreSQL design | To Build |
| Vector Memory | Hands-on | Semantic search | To Build |
| Hybrid Pattern | Integration | Coordinate all 3 | To Build |
| Token Counting | Hands-on | Cost tracking | To Build |
| Optimization | Strategy | Reduce costs 10x | To Build |

---

## PHASE 5: PRODUCTION MASTERY (Weeks 10-11)

### **Week 10: Testing & Verification**

| Day | Focus | Tools | Status |
|-----|-------|-------|--------|
| 1-2 | Unit Testing | pytest | To Build |
| 3 | Integration Testing | Docker, pytest | To Build |
| 4 | E2E Testing | Playwright | To Build |
| 5 | Payment Testing | Stripe test cards | To Build |
| 6 | Evals Suite | LangSmith evaluators | To Build |
| 7-8 | Governance | Presidio, fairness | To Build |

---

### **Week 11: Observability & MLOps**

| Day | Focus | Tools | Status |
|-----|-------|-------|--------|
| 1 | LangSmith Monitoring | LangSmith | To Build |
| 2 | Metrics Collection | Prometheus | To Build |
| 3 | Tracing | Jaeger, OpenTelemetry | To Build |
| 4 | Logging | CloudWatch | To Build |
| 5 | Cost Analysis | Custom calculator | To Build |
| 6-7 | Alerting & Dashboards | Grafana, Slack | To Build |

---

## PHASE 6: AWS & DEPLOYMENT (Week 12)

| Day | Focus | Tech | Status |
|-----|-------|------|--------|
| 1-2 | Infrastructure design | Terraform | To Build |
| 3 | Bedrock setup | AWS Bedrock | To Build |
| 4 | Containerization | Docker, Kubernetes | To Build |
| 5 | CI/CD pipeline | GitHub Actions | To Build |
| 6-7 | First deployment | Terraform + Lambda | To Build |

---

## PHASE 7: CAPSTONE (Week 13)

**Project:** Production loan processor system

**Deliverables:**
- ✅ Complete working agent
- ✅ Test suite (all types)
- ✅ Infrastructure-as-code
- ✅ Monitoring dashboards
- ✅ API documentation
- ✅ README & deployment guide

**Evaluation:**
- Code quality (30%)
- Testing coverage (20%)
- Documentation (20%)
- Architecture (20%)
- Presentation (10%)

---

## PHASE 8: CERTIFICATION & CAREER (Weeks 14-16)

### **Week 14: CCA-F Study**
- Review all domains
- Complete practice exercises
- Take mock exam
- Target: 80%+ on practice

### **Week 15: Interview Prep**
- Technical questions
- System design problems
- Behavioral questions
- Portfolio walkthrough

### **Week 16: Final Prep + Exam**
- Rest & review
- Take official exam
- Plan job search
- Network with community

---

## ✅ DAILY SCHEDULE EXAMPLE

**Typical Study Day:**

```
Time     | Activity        | Duration
---------|-----------------|----------
9:00-10:30 | Concept lecture | 90 min
           | (GRAY/WHITE bg) |
---------|-----------------|----------
10:30-11:00 | Break | 30 min
---------|-----------------|----------
11:00-1:00 | Hands-on coding | 120 min
           | (Follow along)  |
---------|-----------------|----------
1:00-2:00 | Lunch | 60 min
---------|-----------------|----------
2:00-3:30 | Challenges      | 90 min
           | (Solve yourself)|
---------|-----------------|----------
3:30-4:00 | Code review     | 30 min
           | (Show solutions)|
---------|-----------------|----------
4:00-5:00 | Stretch/Review  | 60 min
           | Next day prep   |

Total: 480 min (8 hours) per day
Sustainable: ~5 days/week for 16 weeks
```

---

**Status:** Complete 16-week schedule outlined
**Next Steps:** CCA-F domain mapping, technology stack documentation
