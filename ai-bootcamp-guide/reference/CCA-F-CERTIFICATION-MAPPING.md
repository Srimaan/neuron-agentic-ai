# CCA-F CERTIFICATION MAPPING
## How the Bootcamp Covers All 5 Domains

**Status:** Claude Certified Architect - Foundations
**Exam Format:** 60 questions, 90 minutes, 70% passing score

---

## DOMAIN OVERVIEW

| Domain | Coverage | Weeks | % of Exam | Status |
|--------|----------|-------|----------|--------|
| 1: Agentic Architecture & Orchestration | Deep | 1-14 | 27% | Comprehensive |
| 2: Claude Code Config & Workflows | Medium | 5-7, 12 | 20% | Strong |
| 3: Prompt Engineering & Structured Output | Deep | 1-3, 14 | 20% | Comprehensive |
| 4: Tool Design & MCP Integration | Deep | 3, 8, 12 | 20% | Comprehensive |
| 5: Context Management & Evaluation | Medium | 2, 9, 10-11 | 13% | Strong |

**Total Coverage:** 100% of exam domains
**Learning Depth:** Mixed (lecture + hands-on + certification exercises)

---

## DOMAIN 1: AGENTIC ARCHITECTURE & ORCHESTRATION (27%)

### **What's Tested**

```
Multi-agent systems and orchestration patterns
├─ Agent design patterns
├─ Communication between agents
├─ Error handling at scale
├─ State management across agents
├─ Performance optimization
└─ Deployment considerations
```

### **Bootcamp Coverage**

**Weeks 1-2: Foundations**
```
Loop Engineering concept
├─ Four-phase loop (gather → reason → act → observe)
├─ State machines
├─ Exit conditions
└─ Feedback loops

Graph Engineering concept
├─ DAGs vs cyclic graphs
├─ Node/edge design
├─ Branching logic
├─ Parallel execution
```

**Weeks 3-4: Loan Application Evolution**
```
V4: Loop Engineering
├─ Single-agent iteration
├─ State management
├─ Retry logic
├─ Escalation paths

V5: Graph Engineering
├─ Multi-path workflows
├─ Conditional routing
├─ Parallel verification
└─ Final state transitions
```

**Weeks 5-7: Framework Implementations**
```
Raw Python SDK
├─ Manual loop implementation
├─ Full control over flow
├─ State management from scratch

LangGraph (PRIMARY)
├─ Explicit state machines
├─ Node and edge management
├─ Debugging capabilities

AutoGen (multi-agent)
├─ Agent communication
├─ Conversation management
├─ Orchestration patterns

CrewAI (role-based)
├─ Role hierarchy
├─ Task assignment
├─ Team coordination
```

**Week 12: Production Deployment**
```
Kubernetes orchestration
├─ Container management
├─ Scaling patterns
├─ Health monitoring
├─ Load balancing

AWS Lambda
├─ Serverless orchestration
├─ Event-driven workflows
├─ Auto-scaling
```

### **Key Concepts to Know**

```
✓ State machines (deterministic vs probabilistic)
✓ Loop patterns and when to use each
✓ Multi-agent vs single-agent tradeoffs
✓ Scaling from 1 to 1M concurrent agents
✓ Error handling strategies
✓ Monitoring distributed agents
✓ Cost optimization at scale
✓ Deployment patterns (monolith vs microservices)
```

### **Practice Exercises**

**Exercise 1.1:** Design agent for 10K concurrent users
```
Question: Your agent processes 10K concurrent loan applications.
How do you orchestrate them?

Answer should cover:
- State management strategy
- Communication patterns
- Error handling
- Cost optimization
- Monitoring approach
```

**Exercise 1.2:** Multi-agent system
```
Question: Build 3-agent team: (1) Analyzer, (2) Verifier, (3) Decision maker

Answer should cover:
- How agents communicate
- State sharing strategy
- Error propagation
- Testing approach
```

**Exercise 1.3:** Production incident
```
Question: Your agent is in infinite loop for 5% of requests.
How do you debug and fix?

Answer should cover:
- Detection strategy
- Root cause analysis
- Emergency fixes
- Prevention
```

---

## DOMAIN 2: CLAUDE CODE CONFIGURATION & WORKFLOWS (20%)

### **What's Tested**

```
Claude SDK, API configuration, and workflow optimization
├─ Model selection and configuration
├─ API rate limits and quotas
├─ Batch processing
├─ Token management
├─ Vision capabilities
├─ Tool use configuration
└─ Performance tuning
```

### **Bootcamp Coverage**

**Week 1: Foundations**
```
Prompt Engineering
├─ Claude capabilities
├─ Model versions (Opus, Sonnet, Haiku)
├─ When to use each model
└─ API basics
```

**Weeks 3-4: Loan Application Evolution**
```
Raw Python + Claude SDK
├─ Direct API calls
├─ Response handling
├─ Error management
├─ Token counting
├─ Cost tracking
```

**Week 5: Raw Python SDK Deep Dive**
```
Comprehensive coverage:
├─ SDK installation and setup
├─ Async vs sync clients
├─ Streaming responses
├─ Vision capabilities
├─ Tool use (function calling)
├─ Batch API for scale
├─ Rate limit handling
└─ Error recovery
```

**Week 12: Production Configuration**
```
AWS Bedrock setup
├─ Model access configuration
├─ Rate limiting
├─ Cost controls
├─ Regional deployment
├─ Cross-region failover
└─ Performance tuning
```

### **Key Concepts to Know**

```
✓ Claude models (latest versions, capabilities)
✓ API rate limits (requests/min, tokens/min)
✓ Streaming vs batching tradeoffs
✓ Vision capabilities (images, documents, PDFs)
✓ Tool use vs retrieval-augmented generation
✓ Token costs and optimization
✓ Batch API for throughput
✓ Error handling (rate limits, timeouts)
✓ Regional deployment
✓ Model selection criteria
```

### **Practice Exercises**

**Exercise 2.1:** Model Selection
```
Question: Your agent needs to process 1M+ documents daily.
Which model(s) would you use and why?

Answer should cover:
- Speed vs accuracy tradeoffs
- Cost considerations
- Batching strategy
- Error handling
```

**Exercise 2.2:** API Configuration**
```
Question: You're hitting rate limits in production.
How would you restructure to handle 100K req/hour?

Answer should cover:
- Batch API strategy
- Request queuing
- Resource allocation
- Monitoring
```

**Exercise 2.3:** Vision Integration
```
Question: Add document analysis to your agent.
How do you handle PDFs, images, etc.?

Answer should cover:
- Document loading
- Vision capabilities
- Error handling
- Cost optimization
```

---

## DOMAIN 3: PROMPT ENGINEERING & STRUCTURED OUTPUT (20%)

### **What's Tested**

```
Prompt design, prompt versions, output formatting
├─ Prompt structure and best practices
├─ Few-shot vs zero-shot prompting
├─ Chain-of-thought prompting
├─ Structured output formats (JSON, XML)
├─ Prompt versioning and experimentation
├─ Temperature and sampling parameters
└─ Output validation
```

### **Bootcamp Coverage**

**Week 1: Prompt Engineering 101**
```
Comprehensive deep dive:
├─ Instruction clarity
├─ Role prompting
├─ Few-shot examples
├─ Chain-of-thought
├─ Output formatting
├─ Testing approaches
└─ Iteration strategies
```

**Weeks 3-4: Loan Application V1-V2**
```
V1: Prompt Only
├─ Simple prompts (not enough)
├─ Why they fail
├─ What to improve

V2: With Context
├─ Structured data in prompt
├─ Format clarity
├─ Rules specification
```

**Week 5: Hands-on Prompting**
```
PromptFoo testing framework:
├─ Create test cases
├─ Version control prompts
├─ A/B testing
├─ Scoring functions
├─ Automated evaluation
└─ Results tracking
```

**Week 14: CCA-F Study**
```
Deep domain review:
├─ Prompt best practices
├─ Common pitfalls
├─ Advanced techniques
├─ Exam-specific patterns
```

### **Key Concepts to Know**

```
✓ Clear, specific instructions
✓ Role definition ("You are a loan officer")
✓ Few-shot examples (show, don't tell)
✓ Chain-of-thought (explain reasoning)
✓ Structured output formats (JSON, XML)
✓ Constraints (what NOT to do)
✓ Context window management
✓ Token optimization in prompts
✓ Versioning and experimentation
✓ Testing frameworks (PromptFoo, etc)
```

### **Practice Exercises**

**Exercise 3.1:** Improve Loan Prompt
```
Question: Your loan agent says "I don't have enough information"
Rewrite the prompt to be more specific.

Answer should cover:
- Clear decision criteria
- Examples of good/bad loans
- Explicit constraints
- Output format specification
```

**Exercise 3.2:** Structured Output
```
Question: Design a prompt that ALWAYS outputs valid JSON
with fields: decision, reason, score, confidence

Answer should cover:
- Output schema in prompt
- Examples with valid JSON
- Error cases
- Validation approach
```

**Exercise 3.3:** Chain-of-Thought
```
Question: Add chain-of-thought to improve reasoning quality
Show before/after with metrics.

Answer should cover:
- Prompt modification
- Examples with reasoning
- Testing approach
- Metrics improvement
```

---

## DOMAIN 4: TOOL DESIGN & MCP INTEGRATION (20%)

### **What's Tested**

```
Tool/function design, Model Context Protocol, tool composition
├─ Tool definition and schema
├─ Error handling in tools
├─ Tool chaining and composition
├─ MCP protocol and servers
├─ Custom tool development
├─ Tool versioning
└─ Performance and cost
```

### **Bootcamp Coverage**

**Week 1: Harness Engineering 101**
```
Tool design concepts:
├─ Function calling basics
├─ Tool schema definition
├─ Error handling strategies
├─ Validation patterns
└─ Tool composition
```

**Weeks 3-4: Loan Application V3**
```
V3: Harness Engineering
├─ Build 3 real tools
│  ├─ Credit check API
│  ├─ Employment verification
│  └─ Collateral evaluation
├─ Tool error handling
├─ Retry logic
└─ Tool validation
```

**Week 8: MCP Deep Dive**
```
MCP Protocol:
├─ Architecture overview
├─ Building MCP servers
├─ Tool standardization
├─ Agent integration
├─ Error handling
└─ Testing strategies
```

**Week 8: RAG + MCP**
```
MCP Implementation:
├─ Build 3 production tools
├─ Expose as MCP servers
├─ Document with OpenAPI
├─ Test with agents
└─ Deploy and monitor
```

**Week 12: Production Integration**
```
AWS + MCP:
├─ Lambda-based tools
├─ API Gateway integration
├─ Authorization
├─ Monitoring
└─ Scaling strategies
```

### **Key Concepts to Know**

```
✓ Tool schema design (JSON Schema)
✓ Clear tool descriptions
✓ Error handling (timeouts, failures)
✓ Tool validation and constraints
✓ Tool composition patterns
✓ MCP protocol (standardization)
✓ Custom MCP server development
✓ Tool versioning
✓ Performance optimization (caching)
✓ Cost management (api call costs)
✓ Authorization and security
✓ Monitoring tool usage
```

### **Practice Exercises**

**Exercise 4.1:** Tool Design
```
Question: Design 3 tools for your agent with full schemas

Answer should cover:
- Clear descriptions
- Input validation
- Error cases
- Example calls
- Performance considerations
```

**Exercise 4.2:** Tool Error Handling
```
Question: One of your tools fails 5% of the time.
Design error handling strategy.

Answer should cover:
- Retry logic
- Fallback behavior
- Escalation
- Monitoring
```

**Exercise 4.3:** MCP Server
```
Question: Build MCP server wrapping your tools

Answer should cover:
- Server architecture
- Tool exposure
- Error handling
- Testing
- Deployment
```

---

## DOMAIN 5: CONTEXT MANAGEMENT & EVALUATION (13%)

### **What's Tested**

```
Information retrieval, context optimization, evaluation
├─ Context window management
├─ RAG (retrieval-augmented generation)
├─ Memory patterns
├─ Evaluation frameworks
├─ Quality metrics
├─ Bias and fairness
└─ Cost optimization
```

### **Bootcamp Coverage**

**Week 1: Context Engineering 101**
```
Concepts:
├─ Context window limitations
├─ Information hierarchy
├─ Retrieval patterns
└─ Token counting
```

**Weeks 3-4: Loan Application V2**
```
V2: Context Engineering
├─ Structured data feeding
├─ Database schema design
├─ Query optimization
└─ Context relevance
```

**Week 8: RAG Systems**
```
Comprehensive RAG:
├─ Document loading
├─ Chunking strategies
├─ Embeddings
├─ Vector database
├─ Retrieval ranking
├─ RAG evaluation (RAGAs)
└─ Agent + RAG integration
```

**Week 9: Memory Architectures**
```
Memory patterns:
├─ Session memory (Redis)
├─ Persistent memory (PostgreSQL)
├─ Vector memory (semantic search)
├─ Hybrid strategies
├─ Memory optimization
└─ Cost analysis
```

**Weeks 10-11: Evaluation & Monitoring**
```
Evaluation frameworks:
├─ Evals (decision quality)
├─ RAGAs (if using RAG)
├─ Governance (bias, compliance)
├─ LangSmith monitoring
├─ Custom metrics
└─ Cost tracking
```

### **Key Concepts to Know**

```
✓ Context window size and cost
✓ Token counting and optimization
✓ RAG pipeline components
✓ Vector embeddings
✓ Retrieval strategies
✓ Ranking and re-ranking
✓ Memory types (session, persistent, vector)
✓ Hybrid memory architecture
✓ Evaluation metrics
✓ RAGAs evaluation framework
✓ Bias and fairness testing
✓ Cost optimization
✓ Monitoring and alerting
```

### **Practice Exercises**

**Exercise 5.1:** RAG Pipeline
```
Question: Design RAG system for your agent
Load 1000 loan documents and retrieve relevant ones.

Answer should cover:
- Document chunking
- Embedding model
- Vector store choice
- Retrieval strategy
- Evaluation approach
```

**Exercise 5.2:** Memory Strategy
```
Question: Design memory for agent handling 10K daily users

Answer should cover:
- Session memory (Redis)
- Persistent memory (PostgreSQL)
- Vector memory (semantic)
- Cost breakdown
- Scaling approach
```

**Exercise 5.3:** Evaluation Framework
```
Question: Set up evaluation for your agent

Answer should cover:
- Quality metrics
- Bias testing
- Compliance checks
- Monitoring setup
- Alert thresholds
```

---

## EXAM PREPARATION STRATEGY

### **Timeline**

```
Weeks 1-12: Learn (primary focus on coding)
├─ Week 1-2: Foundations (all domains start here)
├─ Weeks 3-4: Hands-on with V1-V5
├─ Weeks 5-7: Frameworks (domains 1, 2 emphasis)
├─ Weeks 8-9: Components (domains 4, 5 emphasis)
└─ Weeks 10-12: Production (all domains integrated)

Week 13: Capstone (demonstrate mastery)

Weeks 14-15: Exam prep (focused study)
├─ Week 14: Domain review
│  ├─ Domain 1 deep dive
│  ├─ Domain 2 deep dive
│  ├─ Domain 3 deep dive
│  ├─ Domain 4 deep dive
│  └─ Domain 5 deep dive
└─ Week 15: Practice exam + weak areas

Week 16: Final prep + Exam
├─ Rest
├─ Mock exam (3 passes, 80%+ each)
├─ Review high-miss questions
└─ Take official exam
```

### **Study Resources**

For each domain, you'll have:

```
1. Domain lecture (BLUE box content)
2. Hands-on implementation
3. 5 practice exercises
4. Case study analysis
5. Mock exam questions (12 questions per domain)
6. Quick reference cards
```

### **Practice Exam Structure**

**Mock Exam 1: Take early (Week 12)**
```
- 60 questions (matching real exam)
- 90 minutes (real timing)
- Reveals weak areas
- No studying between Q's (realistic)
- Score: Usually 60-70% (normal)
```

**Mock Exam 2: After domain review (Week 14)**
```
- 60 questions
- Focus on weak domains
- Should see 70-80% (improving)
```

**Mock Exam 3: Pre-exam (Week 15)**
```
- 60 questions
- Full simulation
- Should see 80%+ (ready)
- If <80%, don't take official yet
```

### **Question Patterns**

**Domain 1 (27%): ~16 questions**
```
- Design multi-agent system (3-4 Qs)
- Handle scaling (2-3 Qs)
- Error handling in orchestration (2-3 Qs)
- State management (2-3 Qs)
- Performance optimization (2-3 Qs)
- Scenario-based (2-3 Qs)
```

**Domain 2 (20%): ~12 questions**
```
- Model selection (2-3 Qs)
- API configuration (2-3 Qs)
- Rate limiting (2 Qs)
- Token management (2 Qs)
- Bedrock/AWS setup (2-3 Qs)
- Performance tuning (1-2 Qs)
```

**Domain 3 (20%): ~12 questions**
```
- Prompt structure (3-4 Qs)
- Few-shot examples (2-3 Qs)
- Output formatting (2-3 Qs)
- Chain-of-thought (1-2 Qs)
- Prompt testing (2 Qs)
- Common mistakes (1-2 Qs)
```

**Domain 4 (20%): ~12 questions**
```
- Tool design (3-4 Qs)
- Error handling (2-3 Qs)
- MCP protocol (2-3 Qs)
- Tool composition (2 Qs)
- Integration scenarios (2-3 Qs)
```

**Domain 5 (13%): ~8 questions**
```
- RAG implementation (2-3 Qs)
- Memory design (2 Qs)
- Evaluation frameworks (2 Qs)
- Context optimization (1-2 Qs)
```

---

## CCA-F CERTIFICATION CHECKLIST

### **Before Exam Day**

```
□ Completed all 16 weeks (or equivalent)
□ Built capstone project (portfolio-ready)
□ Passed all practice exercises
□ Scored 80%+ on mock exam (3x)
□ Reviewed all domain concepts
□ Understand tradeoffs for each concept
□ Can explain your capstone project
□ Have a good night's sleep
□ Know exam location/time
□ Have ID ready
```

### **During Exam**

```
Strategy:
□ Read questions carefully (misreading loses points)
□ Skip unknown questions (come back later)
□ Flag confusing questions (review at end)
□ Manage time (1.5 min per question)
□ Don't second-guess (first instinct usually right)
□ Review answers (if time permits)
```

### **After Exam**

```
If you pass:
□ Celebrate! 🎉
□ Update resume
□ Add to LinkedIn
□ Start job search

If you don't pass:
□ Review score breakdown
□ Focus on weak domains
□ Study 2-3 weeks more
□ Retake exam
```

---

## LEARNING OUTCOMES BY DOMAIN

### **Domain 1: After bootcamp, you can:**
- ✅ Design single and multi-agent systems from scratch
- ✅ Choose between agent architectures (loop vs graph vs multi-agent)
- ✅ Handle errors and failures gracefully
- ✅ Scale from 1 to 1M concurrent agents
- ✅ Monitor and debug agent behavior
- ✅ Optimize for cost and performance
- ✅ Deploy on AWS, Kubernetes, or serverless

### **Domain 2: After bootcamp, you can:**
- ✅ Select the right Claude model for your task
- ✅ Configure API calls efficiently
- ✅ Handle rate limits and quotas
- ✅ Use vision capabilities
- ✅ Optimize token usage
- ✅ Deploy via Bedrock or direct API
- ✅ Implement error recovery

### **Domain 3: After bootcamp, you can:**
- ✅ Write clear, specific prompts
- ✅ Use few-shot learning effectively
- ✅ Implement chain-of-thought reasoning
- ✅ Structure outputs (JSON, XML, etc)
- ✅ Test and version prompts
- ✅ Avoid common prompt mistakes
- ✅ Optimize prompts for different models

### **Domain 4: After bootcamp, you can:**
- ✅ Design robust tool/function definitions
- ✅ Handle tool errors and edge cases
- ✅ Compose tools into workflows
- ✅ Build MCP servers
- ✅ Integrate external APIs safely
- ✅ Version and maintain tools
- ✅ Monitor tool usage and costs

### **Domain 5: After bootcamp, you can:**
- ✅ Implement RAG systems
- ✅ Choose vector databases wisely
- ✅ Design memory architectures
- ✅ Optimize context window usage
- ✅ Evaluate agent performance
- ✅ Detect and mitigate bias
- ✅ Monitor and alert on quality metrics

---

**Certification readiness:** 100%
**Exam pass probability:** 85-90% (if you complete all weeks)
**Timeline:** 16 weeks + 2 weeks exam prep = 18 weeks total

**Next:** Interview preparation guide & career planning
