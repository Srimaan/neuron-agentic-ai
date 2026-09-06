# Agent Architecture Paradigms Deep Dive

## 6 Core Patterns for Building Agents

---

## 1. ReAct Pattern (Reason → Act → Observe)

**The Loop:** Think → Do → See Result → Repeat

```
┌─────────────────────────────────────┐
│  OBSERVE (What's the current state?)│
├─────────────────────────────────────┤
│  REASON (What should I do?)         │
├─────────────────────────────────────┤
│  ACT (Call a tool)                  │
├─────────────────────────────────────┤
│  OBSERVE (What happened?)           │
└─────────────────────────────────────┘
         ↑ Loop back if needed ↓
```

**Used By:** Raw SDK, Strands, Custom Agent Loop, LangGraph

**Code Pattern:**
```python
while True:
    # Observe
    state = get_current_state()
    
    # Reason
    thought = llm.think(state)
    
    # Act
    if thought.needs_tool:
        result = call_tool(thought.tool)
    else:
        return thought.answer
    
    # Observe
    state = update_state(result)
```

**Pros:**
- ✓ Handles multi-step tasks naturally
- ✓ LLM does the reasoning
- ✓ Autonomous problem-solving
- ✓ Works for unpredictable workflows

**Cons:**
- ✗ Can be inefficient (many loops)
- ✗ Hard to predict cost
- ✗ Requires error handling
- ✗ Debugging difficult

**Best For:**
- Autonomous agents
- Unpredictable workflows
- Learning how to think
- Complex reasoning

**Cost:** Medium-High (depends on problem complexity)

---

## 2. Component Chain Pattern

**The Pattern:** Input → Component1 → Component2 → ... → Output

```
Input
  ↓
[Prompt Formatter]
  ↓
[LLM Call]
  ↓
[Output Parser]
  ↓
[Tool Executor]
  ↓
Output
```

**Used By:** LangChain, Phidata, Haystack

**Code Pattern:**
```python
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Define each step
prompt = PromptTemplate(template="Evaluate: {credit}")
llm_call = ChatOpenAI(model="claude-...")
parser = StrOutputParser()

# Chain them
chain = prompt | llm_call | parser

result = chain.invoke({"credit": 780})
```

**Pros:**
- ✓ Simple to understand
- ✓ Linear flow
- ✓ Predictable cost (you know steps)
- ✓ Easy to debug
- ✓ Testable

**Cons:**
- ✗ Not flexible for complex logic
- ✗ Hard for conditional branches
- ✗ Limited to sequential
- ✗ Debugging harder when chained

**Best For:**
- Simple pipelines
- Linear workflows
- Rapid prototyping
- Learning LLMs

**Cost:** Low (predictable, minimal loops)

---

## 3. State Machine Pattern

**The Pattern:** Define explicit states and transitions

```
                Credit Check
                     ↓
    [Initial] ────→ [Assessing] ────→ [Risk Analysis]
                                           ↓
                                      [Decision]
                                    ↙         ↘
                            [Approved]    [Rejected]
                                ↓              ↓
                            [Final]  ←────────┘
```

**Used By:** LangGraph, LangFlow

**Code Pattern:**
```python
from langgraph.graph import StateGraph, END

class LoanState(TypedDict):
    credit: int
    income: float
    decision: str

graph = StateGraph(LoanState)

# Define nodes
def check_credit(state):
    state['credit_approved'] = state['credit'] >= 600
    return state

def analyze_risk(state):
    state['risk_level'] = "high" if state['credit'] < 650 else "low"
    return state

def make_decision(state):
    state['decision'] = "APPROVED" if state['credit_approved'] else "DENIED"
    return state

graph.add_node("credit", check_credit)
graph.add_node("risk", analyze_risk)
graph.add_node("decision", make_decision)

graph.add_edge("credit", "risk")
graph.add_edge("risk", "decision")
graph.add_edge("decision", END)

result = graph.invoke({"credit": 750, "income": 150000})
```

**Pros:**
- ✓ Explicit control flow
- ✓ Easy to visualize
- ✓ Deterministic
- ✓ Great for complex logic
- ✓ Easy to test edge cases

**Cons:**
- ✗ More code
- ✗ Requires planning
- ✗ Not good for exploratory AI
- ✗ Rigid structure

**Best For:**
- Complex workflows
- Deterministic logic
- Production systems
- Business logic

**Cost:** Low (explicit, no looping)

---

## 4. Plugin Architecture Pattern

**The Pattern:** Modular plugins that compose

```
┌──────────────────────────┐
│   Kernel/Core            │
├──────────────────────────┤
│  Plugin: Credit Check    │
│  Plugin: Risk Analysis   │
│  Plugin: Decision Maker  │
└──────────────────────────┘
```

**Used By:** Semantic Kernel, Spring AI

**Code Pattern:**
```java
class CreditPlugin {
    @Plugin
    public String checkCredit(int score) {
        return score >= 650 ? "Approved" : "Denied";
    }
}

class RiskPlugin {
    @Plugin
    public String analyzeRisk(int score, double income) {
        return "High" if score < 650 else "Low";
    }
}

Kernel kernel = new Kernel();
kernel.registerPlugin(new CreditPlugin(), "credit");
kernel.registerPlugin(new RiskPlugin(), "risk");

String result = kernel.invokePlugin("credit", "check", params);
```

**Pros:**
- ✓ Reusable components
- ✓ Modular design
- ✓ Enterprise-friendly
- ✓ Easy composition
- ✓ Shareable plugins

**Cons:**
- ✗ Overkill for simple tasks
- ✗ More setup
- ✗ Less dynamic
- ✗ Plugin management

**Best For:**
- Enterprise systems
- Reusable components
- Team collaboration
- Plugin marketplaces

**Cost:** Low (explicit, no looping)

---

## 5. Conversation-Based Pattern

**The Pattern:** Agents communicate via messages

```
Agent A                    Agent B
  │                          │
  ├─→ "Here's my proposal" ──→│
  │                          │
  │ ←─ "I disagree because" ─│
  │                          │
  ├─→ "Let me counter..." ───→│
  │                          │
  │ ←─ "Point conceded" ──────│
  │                          │
  └─→ "Consensus reached" ───→│
```

**Used By:** AutoGen, CAMEL, JADE

**Code Pattern:**
```python
from autogen import AssistantAgent, UserProxyAgent

# Define agents
credit_agent = AssistantAgent(
    name="Credit Expert",
    system_message="You evaluate credit scores"
)

risk_agent = AssistantAgent(
    name="Risk Analyst", 
    system_message="You analyze risk factors"
)

# They chat
credit_agent.initiate_chat(
    risk_agent,
    message="Evaluate loan application with 700 credit score"
)
```

**Pros:**
- ✓ Natural collaboration
- ✓ Multi-perspective analysis
- ✓ Debate/reasoning
- ✓ Explainable decisions
- ✓ Great for research

**Cons:**
- ✗ Expensive (many LLM calls)
- ✗ Hard to predict behavior
- ✗ Slower
- ✗ Complex coordination

**Best For:**
- Multi-agent research
- Consensus building
- Complex decision-making
- Educational demos

**Cost:** Very High (many LLM calls)

---

## 6. Pipeline/DAG Pattern

**The Pattern:** Process flows through connected stages

```
Input Document
      ↓
[Preprocess]
      ↓
[Chunk]
      ↓
[Embed]
      ↓
[Store]
      ↓
[Retrieve]
      ↓
[Rank]
      ↓
[Generate]
      ↓
Output
```

**Used By:** Haystack, Airflow, Apache Beam

**Code Pattern:**
```python
from haystack import Pipeline, Document

pipeline = Pipeline()

# Add components
pipeline.add_component("retriever", 
    BM25Retriever(document_store))
pipeline.add_component("ranker", 
    SentenceTransformerRanker())
pipeline.add_component("generator", 
    GenerativeQA())

# Connect them
pipeline.connect("retriever.documents", "ranker.documents")
pipeline.connect("ranker.documents", "generator.documents")

# Run
result = pipeline.run({"retriever": {"query": "..."}})
```

**Pros:**
- ✓ Scalable
- ✓ Parallelizable
- ✓ Maintainable
- ✓ Optimizable
- ✓ Observable

**Cons:**
- ✗ Overkill for simple tasks
- ✗ Setup overhead
- ✗ Less flexible
- ✗ Requires monitoring

**Best For:**
- Data pipelines
- RAG systems
- Document processing
- ETL workflows
- Production systems

**Cost:** Medium (depends on pipeline)

---

## Pattern Comparison Matrix

| Pattern | Complexity | Flexibility | Cost | Speed | Control |
|---------|-----------|------------|------|-------|---------|
| **ReAct** | Medium | ✓✓✓ | High | Slow | LLM decides |
| **Chain** | Low | ✓ | Low | Fast | You define |
| **State Machine** | Medium | ✓✓ | Low | Fast | Explicit |
| **Plugin** | Medium | ✓✓ | Low | Fast | Modular |
| **Conversation** | High | ✓✓✓ | Very High | Slow | Emergent |
| **Pipeline** | High | ✓ | Medium | Fast | DAG-based |

---

## Choosing Your Pattern

```
START
│
├─ Need autonomous reasoning?
│  └─ Use: ReAct
│
├─ Simple linear workflow?
│  └─ Use: Chain
│
├─ Complex deterministic logic?
│  └─ Use: State Machine
│
├─ Reusable components?
│  └─ Use: Plugin
│
├─ Multiple agents debating?
│  └─ Use: Conversation
│
├─ Document processing pipeline?
│  └─ Use: Pipeline/DAG
│
└─ Combination/Hybrid?
   └─ Mix patterns!
```

---

## Hybrid Patterns

### ReAct + State Machine
Use ReAct within defined states:
```
[State: Evaluating]
  ├─ ReAct Loop 1
  ├─ ReAct Loop 2
  └─ Decision → Next State
```

### Chain + Plugin
Chain uses plugins as components:
```
Input → [Plugin: Credit] → [Plugin: Risk] → Output
```

### Conversation + State Machine
Agents communicate to drive state changes:
```
State: [Initial]
  Agent A ↔ Agent B (discussion)
  └─ Consensus → Next State
```

---

## Framework-to-Pattern Mapping

| Framework | Primary Pattern | Secondary |
|-----------|---|---|
| Raw SDK | ReAct | Any (you choose) |
| LangChain | Chain | ReAct |
| LangGraph | State Machine | ReAct |
| AutoGen | Conversation | ReAct |
| CrewAI | Conversation + Chain | State Machine |
| Strands | ReAct | State Machine |
| Semantic Kernel | Plugin | Chain |
| Haystack | Pipeline | Chain |
| DSPy | Chain | ReAct |
| Phidata | Chain | ReAct |

---

## Cost by Pattern

**Cheapest to Most Expensive:**
1. **Chain** - Predictable, single pass
2. **State Machine** - Explicit, no looping
3. **Plugin** - Modular, single invocations
4. **Pipeline** - Multi-stage but efficient
5. **ReAct** - Loops, unpredictable
6. **Conversation** - Many LLM calls

---

## Production Readiness by Pattern

| Pattern | Local | Stage | Prod |
|---------|-------|-------|------|
| ReAct | ✓ Simple | 🟡 Needs monitoring | ✓ Strands/LangGraph |
| Chain | ✓ Great | ✓ Good | ✓ Best |
| State Machine | ✓ Good | ✓ Excellent | ✓ Best |
| Plugin | 🟡 Overkill | ✓ Good | ✓ Best |
| Conversation | ✓ Fun | ✓ Research | 🟡 Risky |
| Pipeline | 🟡 Setup | ✓ Good | ✓ Best |

