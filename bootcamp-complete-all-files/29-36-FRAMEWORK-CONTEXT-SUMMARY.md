# Frameworks 29-36: Context Handling Comparison

## Quick Reference: How Each Framework Handles Context

### Framework 29: LangGraph - Stateful Context

**Approach:** Explicit state management + graph-based flow

```python
from langgraph.graph import StateGraph
from typing_extensions import TypedDict

class State(TypedDict):
    context: str
    messages: list
    customer_id: int
    loan_amount: float

def get_customer_context(state: State) -> State:
    # Retrieve from database
    state["context"] = fetch_customer_data(state["customer_id"])
    return state

def evaluate_loan(state: State) -> State:
    # Use context in evaluation
    response = llm.invoke(state["context"] + state["messages"])
    state["messages"].append(response)
    return state

# Build graph
graph = StateGraph(State)
graph.add_node("get_context", get_customer_context)
graph.add_node("evaluate", evaluate_loan)
graph.add_edge("get_context", "evaluate")

app = graph.compile()
```

**Context Handling:** Explicit, stateful, great for complex flows
**Memory:** Built-in through state, no auto-persistence
**Best For:** Multi-step workflows, explicit context control

---

### Framework 30: AutoGen - Message-Based Context

**Approach:** Conversation registry + automatic message history

```python
import pyautogen

config_list = [{"model": "claude-3-5-sonnet-20241022", "api_key": "..."}]

# Agents maintain their own message context
user_proxy = autogen.UserProxyAgent(name="user", human_input_mode="NEVER")

loan_officer = autogen.AssistantAgent(
    name="loan_officer",
    system_message="""
    You are a loan officer. You have access to:
    - Customer database
    - Loan policies
    - Market data
    
    Evaluate loans based on this context.
    """,
    llm_config={"config_list": config_list}
)

# Context automatically managed in conversation
user_proxy.initiate_chat(
    loan_officer,
    message="Customer with credit 720 wants $50k. Evaluate."
)

# Access conversation history
print(user_proxy.chat_messages[loan_officer])
```

**Context Handling:** Message-based, automatic history
**Memory:** Full conversation stored, can be large
**Best For:** Multi-agent conversations, automatic memory

---

### Framework 31: CrewAI - Task-Based Context

**Approach:** Tasks carry context, agents reference as needed

```python
from crewai import Agent, Task, Crew

# Agents with role context
loan_officer = Agent(
    role="Loan Officer",
    goal="Evaluate loan applications fairly",
    backstory="Expert in loan assessment with 10 years experience",
    context="Use customer history and loan policies to decide"
)

# Tasks define context scope
evaluation_task = Task(
    description="Evaluate loan of ${loan_amount} for customer ${customer_id}",
    agent=loan_officer,
    context=[
        "Customer credit score: ${credit_score}",
        "Annual income: ${income}",
        "Loan policies (max DTI: 43%)",
        "Market rates today"
    ]
)

crew = Crew(agents=[loan_officer], tasks=[evaluation_task])
result = crew.kickoff()
```

**Context Handling:** Task-scoped, role-based context
**Memory:** Per-task context, agents persist knowledge
**Best For:** Team-based workflows, role hierarchies

---

### Framework 32: Strands - Model-Managed Context

**Approach:** Model decides what context to retrieve

```python
from strands_agents import Agent, Tool

agent = Agent(model="claude-3-5-sonnet-20241022")

@agent.tool
def get_customer_context(customer_id: int) -> str:
    """Get customer from database"""
    conn = sqlite3.connect("loans.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE id=?", (customer_id,))
    return str(cursor.fetchone())

@agent.tool
def get_market_rates() -> str:
    """Get current market rates"""
    return "30yr: 6.5%, 15yr: 6.0%, ARM: 5.8%"

@agent.tool
def get_policies() -> str:
    """Get loan policies"""
    return "Min credit: 600, Max DTI: 43%, Min income: $30k"

# Agent autonomously decides which context to retrieve
result = agent.invoke(
    task="Evaluate $50k loan for customer 1",
    max_tokens=1024
)
```

**Context Handling:** Model-driven retrieval, selective
**Memory:** Only retrieved context is used
**Best For:** Production systems, autonomous operation

---

### Framework 33: Semantic Kernel - Plugin Context

**Approach:** Context as plugins/skills

```python
import semantic_kernel as sk

kernel = sk.Kernel()

# Add OpenAI backend
kernel.add_text_completion_service(
    "claude", ChatAnthropic(model="claude-3-5-sonnet-20241022")
)

# Add plugins that provide context
@sk.skill_description("Customer and Loan Skills")
class LoanSkills:
    @sk.function_description("Get customer context")
    def get_customer(self, customer_id: str) -> str:
        # Database query
        return f"Customer {customer_id}: credit 720, income $150k"
    
    @sk.function_description("Get loan policies")
    def get_policies(self) -> str:
        return "Max DTI: 43%, Min credit: 600"

# Use plugins in prompts
prompt = """
Context:
{{LoanSkills.get_customer $customerId}}
{{LoanSkills.get_policies}}

Task: {{$task}}
"""

# Invoke with context
result = kernel.run_async(
    prompt,
    customerId="1",
    task="Evaluate $50k loan"
)
```

**Context Handling:** Plugin-based, composable
**Memory:** Skills provide/manage context
**Best For:** Enterprise, modular systems

---

### Framework 34: Haystack - Pipeline Context

**Approach:** Context flows through pipeline stages

```python
from haystack import Pipeline
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.builders import AnswerBuilder, PromptBuilder

# Build pipeline that manages context
pipeline = Pipeline()

# Retrieval stage (context gets fetched)
pipeline.add_component(
    "retriever",
    InMemoryBM25Retriever(
        document_store=InMemoryDocumentStore()
    )
)

# Prompt building stage (context injected)
prompt_builder = PromptBuilder(
    template="""
    Context: {{documents}}
    
    Customer: {{customer_id}}
    Task: {{task}}
    """
)
pipeline.add_component("prompt", prompt_builder)

# LLM stage
pipeline.add_component(
    "llm",
    ChatAnthropic(model="claude-3-5-sonnet-20241022")
)

# Connect stages
pipeline.connect("retriever.documents", "prompt.documents")
pipeline.connect("prompt.prompt", "llm.input")

# Run with context flowing through
result = pipeline.run({
    "retriever": {"query": "customer context"},
    "prompt": {"customer_id": "1", "task": "evaluate loan"}
})
```

**Context Handling:** Pipeline-based, document flow
**Memory:** Document stores, RAG-friendly
**Best For:** Document processing, RAG systems

---

### Framework 35: DSPy - Declarative Context

**Approach:** Declare context patterns, optimize via examples

```python
import dspy

# Define context pattern
class LoanEvaluation(dspy.Signature):
    """Evaluate loan application with context."""
    
    customer_context = dspy.InputField(
        description="Customer info: credit, income, history"
    )
    loan_policies = dspy.InputField(
        description="Loan approval policies"
    )
    loan_details = dspy.InputField(
        description="Loan amount and terms"
    )
    decision = dspy.OutputField(
        description="Approval decision and confidence"
    )

# Create program with context
class LoanEvaluator(dspy.ChainOfThought):
    def __init__(self):
        super().__init__(LoanEvaluation)
    
    def forward(self, customer_context, loan_policies, loan_details):
        return super().forward(
            customer_context=customer_context,
            loan_policies=loan_policies,
            loan_details=loan_details
        )

# Optimize with examples (teaching it best context patterns)
from dspy.teleprompt import BootstrapFewShot

metric = lambda pred, trace, example: "APPROVED" in pred.decision

teleprompter = BootstrapFewShot(metric=metric)
program = teleprompter.compile(
    LoanEvaluator(),
    trainset=examples  # Examples teach best context patterns
)

# Run with optimized context
result = program(
    customer_context="Credit 720, income $150k",
    loan_policies="Max DTI 43%",
    loan_details="$50k loan"
)
```

**Context Handling:** Declarative, example-based optimization
**Memory:** Learn from examples, improve over time
**Best For:** Production optimization, pattern learning

---

### Framework 36: Phidata - Simple Context

**Approach:** Lightweight context with tools

```python
from phidata import Agent, Tool
import sqlite3

# Simple context through tools
def get_customer(customer_id: str) -> str:
    conn = sqlite3.connect("loans.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE id=?", (customer_id,))
    return str(cursor.fetchone())

def get_policies() -> str:
    return "Policies: Min 600 credit, Max 43% DTI"

# Create agent with context tools
agent = Agent(
    model="claude-3-5-sonnet-20241022",
    tools=[
        Tool(name="get_customer", fn=get_customer),
        Tool(name="get_policies", fn=get_policies)
    ],
    system_message="You are a loan officer. Use provided tools for context."
)

# Simple invocation with automatic context retrieval
response = agent.chat("Evaluate $50k loan for customer 1")
```

**Context Handling:** Tool-based, simple and direct
**Memory:** Minimal, just message history
**Best For:** Quick prototypes, simple agents

---

## Comparison Matrix: Context Strategies

| Framework | Context Type | Retrieval | Auto-Memory | Best For |
|-----------|---|---|---|---|
| 27: Raw SDK | Manual | Manual | None | Learning |
| 28: LangChain | Automatic | Via chains | ✅ Buffer/Summary | Quick apps |
| 29: LangGraph | Stateful | Explicit | ✅ State-based | Complex flows |
| 30: AutoGen | Message-based | Auto | ✅ Full history | Multi-agent |
| 31: CrewAI | Task-scoped | Per-task | ✅ Agent memory | Teams |
| 32: Strands | Model-managed | LLM decides | Selective | Production |
| 33: Semantic Kernel | Plugin-based | Via skills | Via plugins | Enterprise |
| 34: Haystack | Pipeline | Document flow | Document store | RAG |
| 35: DSPy | Declarative | Via patterns | Example cache | Optimization |
| 36: Phidata | Tool-based | Tool calling | Minimal | Prototypes |

---

## Context Handling by Use Case

### Large Documents (50K+ tokens)
**Best:** Haystack (chunking), DSPy (pattern optimization), Raw SDK (explicit control)

### Long Conversations (100+ turns)
**Best:** LangChain (summary memory), Strands (selective retrieval), Phidata (simple)

### Database Integration
**Best:** Raw SDK (explicit), Strands (model-driven), Haystack (document store)

### Enterprise Systems
**Best:** Semantic Kernel (plugins), CrewAI (teams), Strands (autonomous)

### Real-Time Context
**Best:** Raw SDK (control), LangGraph (stateful), Strands (model-driven)

### Production Optimization
**Best:** DSPy (learn patterns), LangChain (mature), Semantic Kernel (proven)

---

## Implementation Recommendations

### Start With:
1. **Raw SDK** - Understand context fundamentals
2. **LangChain** - Quick context-aware apps
3. **LangGraph** - Complex stateful workflows

### Level Up:
4. **Strands** - Production autonomous systems
5. **CrewAI** - Multi-agent coordination
6. **Haystack** - Document/RAG systems

### Advanced:
7. **Semantic Kernel** - Enterprise modularity
8. **DSPy** - Optimization & learning
9. **AutoGen** - Multi-agent conversations
10. **Phidata** - Lightweight simplicity

---

## Next: Practical Implementation

See framework examples 27-28 for working code.

For frameworks 29-36, refer to:
- Official documentation
- GitHub repositories
- Community examples

Most important: **Choose based on your architecture needs, not hype.**

