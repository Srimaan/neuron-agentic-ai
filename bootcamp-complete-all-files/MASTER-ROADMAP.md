# AI AGENTS PRODUCTION BOOTCAMP
## Complete 16-Week Learning Path

**Goal:** Train AI Architects who can build, deploy, monitor, and scale production agent systems.

**Outcomes:** By week 16, learner has:
- ✅ Deep understanding of 5 engineering disciplines
- ✅ Built 1 complete loan application agent (5 evolving versions)
- ✅ Implemented same agent in 5 frameworks (Python SDK, LangChain, LangGraph, AutoGen, CrewAI)
- ✅ Deployed to AWS using Bedrock, Lambda, RDS, ElastiCache
- ✅ Built verification & testing suite (Evals, RAGAs, Governance, Playwright, Stripe)
- ✅ Set up complete observability (LangSmith, Prometheus, Grafana, Jaeger, CloudWatch)
- ✅ Passed CCA-F certification (all 5 domains covered)
- ✅ Built capstone: Production-ready loan processor system
- ✅ Portfolio-ready project for interviews

---

## 📊 COURSE STRUCTURE (16 Weeks)

### **PHASE 1: FOUNDATIONS (Weeks 1-2)**

**Goal:** Understand the 5 engineering disciplines that power production agents.

**Week 1: Engineering Disciplines Introduction**

| Day | Topic | Format | Outcome |
|-----|-------|--------|---------|
| 1-2 | Prompt Engineering (101) | WHITE bg lecture + examples | Understand how to structure prompts for agents |
| 3 | Context Engineering (101) | WHITE bg lecture + examples | Understand information flow to agents |
| 4 | Harness Engineering (101) | WHITE bg lecture + examples | Understand tool design and integration |
| 5 | Loop Engineering (101) | WHITE bg lecture + examples | Understand agent iteration patterns |
| 6 | Graph Engineering (101) | WHITE bg lecture + examples | Understand workflow orchestration |
| 7 | Summary & Concepts | GRAY bg deep dive | "Why do we need each layer?" |

**Week 2: Evolution Story - Why Each Layer Exists**

| Day | Topic | Problem → Solution | Output |
|-----|-------|-------------------|--------|
| 1 | Prompt Engineering Problems | "Just ask Claude" doesn't work | Show limitations |
| 2 | Context Engineering Problems | Need access to real data | Add database context |
| 3 | Harness Engineering Problems | Need to affect real world | Add tool execution |
| 4 | Loop Engineering Problems | One shot isn't enough | Add iteration with feedback |
| 5 | Graph Engineering Problems | Linear loops don't work | Add branching/complex flows |
| 6 | Verification Layer Problems | Agent mistakes break things | Add validation/governance |
| 7-8 | Complete Picture | See evolution from V1→V5 | Understand WHY architecture |

**Local Setup:**
- Python 3.11+
- Claude SDK installed
- PostgreSQL locally (Docker)
- Redis locally (Docker)
- Basic Docker Compose knowledge

---

### **PHASE 2: LOAN APPLICATION EVOLUTION (Weeks 3-4)**

**Goal:** See one real use case evolve through all 5 engineering layers.

**Application:** Bank needs to evaluate $10K-$500K loan applications

**Version 1 (Week 3, Day 1): Prompt Engineering Only**
```
Problem: Just asking Claude doesn't work
- No access to applicant data
- No loan rules
- No decision criteria
- Output: Claude guesses

Learnings:
- Why you need real data
- Prompt limitations
- Move to V2
```

**Version 2 (Week 3, Day 2): Add Context Engineering**
```
Problem: Static context works partially but rigid
- Hard-coded applicant data in prompt
- Hard-coded loan rules
- Can't handle dynamic changes
- Output: Better decisions, but limited

Learnings:
- Why you need dynamic context
- Database design for agents
- Move to V3
```

**Version 3 (Week 3, Day 3): Add Harness Engineering**
```
Problem: No tools means can't verify applicant data
- Can't call credit score API
- Can't verify employment
- Can't check collateral value
- Output: Real tool integration

Learnings:
- Tool design patterns
- Error handling for tool calls
- Tool validation
- Move to V4
```

**Version 4 (Week 3, Day 4): Add Loop Engineering**
```
Problem: Single decision isn't enough
- Need to ask clarifying questions
- Need to retry failed tools
- Need to follow decision rules
- Output: Iterative agent

Learnings:
- Loop patterns (4-phase)
- State management
- Exit conditions
- Move to V5
```

**Version 5 (Week 3, Day 5): Add Graph Engineering**
```
Problem: Linear loops can't handle complex workflows
- Multiple paths (approve/deny/review)
- Conditional execution
- Parallel verification
- Output: Graph-based workflow

Learnings:
- State machine design
- Branching logic
- Parallel execution
- This is production
```

**Version 5+ (Week 4): Verification & Observability**
```
Problem: How do you know if decisions are good?
- Add Evals (decision quality)
- Add RAGAs (if using RAG)
- Add Governance (bias, compliance, PII)
- Add PromptFoo (prompt testing)
- Output: Verified, monitored agent

Learnings:
- Testing agents (non-deterministic)
- Governance requirements
- Observability setup
- Production readiness
```

**Repo Structure for Each Version:**
```
loan-application-evolution/
├── v1-prompt-only/
│   ├── agent.py (50 lines)
│   ├── run_example.py
│   ├── results.md (what works/fails)
│   └── learnings.md
├── v2-context-engineering/
│   ├── agent.py (100 lines)
│   ├── database_context.py
│   ├── schema.sql
│   └── learnings.md
├── v3-harness-engineering/
│   ├── agent.py (200 lines)
│   ├── tools/ (credit check, employment verify, collateral)
│   ├── tool_error_handling.py
│   └── learnings.md
├── v4-loop-engineering/
│   ├── agent.py (400 lines)
│   ├── loop_controller.py
│   ├── state_manager.py
│   └── learnings.md
└── v5-graph-engineering/
    ├── graph.py (LangGraph state machine)
    ├── nodes/ (approve, deny, review, verify)
    ├── edges/ (conditional routing)
    ├── memory_manager.py
    ├── verification.py (Evals + Governance)
    ├── observability.py (monitoring)
    └── learnings.md
```

---

### **PHASE 3: FRAMEWORK IMPLEMENTATIONS (Weeks 5-7)**

**Goal:** Implement same loan agent in 5 different frameworks.

**Week 5: Raw Python + LangChain**
```
Repo: framework-implementations/

1. raw-python-claude-sdk/
   ├── agent.py (Claude SDK directly)
   ├── memory/ (Redis + PostgreSQL)
   ├── tools/ (all 5 verification tools)
   ├── docker-compose.yml
   ├── tests/
   └── README.md

   Learnings:
   - Maximum control
   - Full understanding of loop
   - Painful to maintain
   - Good for learning
   - But also production-worthy
   
2. langchain-implementation/
   ├── agent.py (LangChain chains)
   ├── memory_handler.py (LangChain memory)
   ├── tools/ (LangChain tools)
   ├── docker-compose.yml
   ├── tests/
   └── README.md

   Learnings:
   - Composable components
   - Less boilerplate
   - Easier to maintain
   - Less control
   - Good for rapid development
```

**Week 6: LangGraph + AutoGen**
```
3. langgraph-implementation/
   ├── graph.py (State machine)
   ├── nodes/ (decision nodes)
   ├── edges/ (routing)
   ├── memory/ (persistent)
   ├── docker-compose.yml
   ├── tests/
   └── README.md

   Learnings:
   - Explicit workflows
   - Easy debugging
   - Clear control flow
   - More verbose
   - Best for complex agents

4. autogen-implementation/
   ├── agent_setup.py (multi-agent)
   ├── user_proxy.py
   ├── assistant_agents.py
   ├── memory/ (shared state)
   ├── docker-compose.yml
   ├── tests/
   └── README.md

   Learnings:
   - Multi-agent conversations
   - Agent orchestration
   - Complex to debug
   - Great for team simulations
```

**Week 7: CrewAI + Comparison**
```
5. crewai-implementation/
   ├── crew.py (crew setup)
   ├── agents/ (role-based)
   ├── tasks/ (role tasks)
   ├── memory/ (crew memory)
   ├── docker-compose.yml
   ├── tests/
   └── README.md

   Learnings:
   - Role-based abstraction
   - High-level interface
   - Limited customization
   - Good for role hierarchies

COMPARISON/
├── feature-comparison.md
│   (Which framework has what)
├── performance-comparison.md
│   (Speed, tokens, cost)
├── developer-experience.md
│   (Ease of use, learning curve)
├── production-readiness.md
│   (Monitoring, testing, scaling)
└── decision-tree.md
   (Which to choose for what)
```

---

### **PHASE 4: SYSTEM COMPONENTS (Weeks 8-9)**

**Goal:** Add specialized systems that production agents need.

**Week 8: RAG + MCP**
```
RAG-SYSTEMS/
├── 01-RAG-Fundamentals/
│   ├── retrieval-augmented-generation.md (GRAY bg - concept)
│   ├── why-rag.md (why we need it)
│   ├── vector-databases.md (Pinecone, Weaviate, Milvus)
│   └── ragas-evaluation.md (measure RAG quality)

├── 02-RAG-Implementation/
│   ├── document-loader.py (load PDFs, web, etc)
│   ├── chunking-strategies.py (how to split docs)
│   ├── embedding-models.py (sentence-transformers)
│   ├── retrieval.py (query vector store)
│   ├── ranking.py (re-rank results)
│   └── integration.py (add to loan agent)

├── 03-RAG-with-Agent/
│   ├── rag-agent.py (agent with retrieval)
│   ├── memory/ (context manager)
│   ├── evaluation/ (measure quality)
│   └── tests/

├── Real Use Case:
   Agent needs to cite loan regulations
   - Load all bank loan policies
   - Agent retrieves relevant ones
   - Agent cites them in decisions

MCP-SYSTEMS/
├── 01-MCP-Fundamentals/
│   ├── what-is-mcp.md (GRAY bg - concept)
│   ├── why-mcp.md (standardized tools)
│   └── mcp-architecture.md

├── 02-Building-Tools/
│   ├── credit-check-tool.py (MCP server)
│   ├── employment-verify-tool.py (MCP server)
│   ├── collateral-eval-tool.py (MCP server)
│   └── tool-testing.py

├── 03-Agent-Integration/
│   ├── connect-mcp-to-agent.py
│   ├── error-handling.py
│   └── tests/

├── Real Use Case:
   Build 3 MCP tools for loan verification
   - Credit check API wrapper
   - Employment verification API wrapper
   - Collateral valuation API wrapper
   - Agent calls them via MCP protocol
```

**Week 9: Memory + Token Optimization**
```
MEMORY-ARCHITECTURES/
├── 01-Memory-Types/
│   ├── session-memory.md (Redis - current)
│   ├── persistent-memory.md (PostgreSQL - history)
│   ├── vector-memory.md (Embeddings - semantic)
│   ├── hybrid-memory.md (all three combined)
│   └── tradeoffs.md (GRAY bg - why each)

├── 02-Implementation/
│   ├── redis-session.py (Real-time state)
│   ├── postgres-history.py (Permanent records)
│   ├── vector-db-semantic.py (Search similar cases)
│   ├── hybrid-manager.py (Coordinate all 3)
│   └── tests/

├── 03-Token-Optimization/
│   ├── token-counting.py (measure usage)
│   ├── context-truncation.py (keep recent)
│   ├── prompt-caching.py (avoid re-processing)
│   ├── semantic-chunking.py (compress intelligently)
│   ├── cost-calculator.py ($ per decision)
│   └── optimization-strategies.md

├── Real Use Case:
   Loan agent processes 1000 applications/day
   - Each costs $0.01 in tokens (without optimization)
   - Optimize to $0.002 per decision
   - Save $8k/month
```

---

### **PHASE 5: PRODUCTION MASTERY (Weeks 10-11)**

**Goal:** Make agents production-ready, monitored, secure, and scalable.

**Week 10: Testing & Verification**
```
TESTING-VERIFICATION/
├── 01-Unit-Testing/
│   ├── pytest-setup.py
│   ├── test_agent_logic.py
│   ├── test_tools.py
│   ├── test_memory.py
│   └── fixtures.py (test data)

├── 02-Integration-Testing/
│   ├── docker-test-stack.yml
│   ├── test_full_pipeline.py
│   ├── test_database.py
│   ├── test_redis.py
│   └── test_bedrock_connection.py

├── 03-E2E-Testing-Playwright/
│   ├── test_loan_form.py (UI testing)
│   ├── test_workflow.py (complete flow)
│   ├── test_error_states.py (failures)
│   ├── fixtures.py (test env)
│   └── README.md

├── 04-Payment-Testing-Stripe/
│   ├── test_payment_flow.py
│   ├── test_payment_failure.py
│   ├── test_webhook.py
│   ├── test_refunds.py
│   └── stripe-test-cards.md

├── 05-Verification-Suite/
│   ├── evals/ (decision quality)
│   │   ├── decision_validator.py
│   │   ├── reason_validator.py
│   │   └── consistency_checks.py
│   │
│   ├── ragas/ (if using RAG)
│   │   ├── faithfulness_eval.py
│   │   ├── retrieval_eval.py
│   │   └── rag_scorer.py
│   │
│   ├── governance/
│   │   ├── bias_detection.py (gender, racial bias)
│   │   ├── pii_check.py (Presidio)
│   │   ├── compliance_check.py (business rules)
│   │   └── fairness_audit.py
│   │
│   ├── promptfoo/
│   │   ├── promptfoo.yaml (test cases)
│   │   ├── run_tests.sh
│   │   └── results.json

├── 06-Load-Testing/
│   ├── locust-tests.py (concurrent users)
│   ├── load-profile.yaml
│   └── bottleneck-analysis.py

└── Real Use Case:
   Test loan agent for:
   - Correct loan decisions
   - No bias in approvals
   - No PII leakage
   - Payment flow works
   - Handles 100 concurrent users
```

**Week 11: Observability & Monitoring**
```
OBSERVABILITY-MLOPS/
├── 01-LangSmith-Monitoring/
│   ├── langsmith-setup.py
│   ├── trace-agent-runs.py
│   ├── feedback-collection.py
│   ├── analytics.py (track metrics)
│   └── README.md

├── 02-Metrics-Prometheus/
│   ├── prometheus-config.yaml
│   ├── metrics.py (define metrics)
│   ├── prometheus-docker.yml
│   └── grafana-dashboards/ (JSON)
│       ├── agent-health.json
│       ├── token-usage.json
│       ├── decision-quality.json
│       └── cost-tracking.json

├── 03-Tracing-OpenTelemetry/
│   ├── jaeger-docker.yml
│   ├── tracing-setup.py
│   ├── span-collection.py
│   └── trace-analysis.md

├── 04-Logging-CloudWatch/
│   ├── cloudwatch-config.py
│   ├── structured-logging.py
│   ├── log-parser.py
│   └── aws-setup.md

├── 05-Cost-Tracking/
│   ├── token-counter.py
│   ├── cost-calculator.py
│   ├── cost-alerts.py
│   ├── monthly-report.py
│   └── optimization-suggestions.py

├── 06-Alerting/
│   ├── alert-rules.yaml
│   ├── slack-alerts.py
│   ├── pagerduty-setup.py
│   ├── incident-response.md
│   └── escalation-policy.md

├── 07-Dashboards/
│   ├── grafana-setup.md
│   ├── loan-dashboard.json
│   ├── agent-performance.json
│   ├── system-health.json
│   └── business-metrics.json

└── Real Use Case:
   Monitor loan agent in production:
   - Track decision quality
   - Monitor token costs
   - Alert on anomalies
   - Trace user journeys
   - Log all decisions (audit trail)
   - Trigger alerts if approval rate changes
```

---

### **PHASE 6: AWS & DEPLOYMENT (Week 12)**

**Goal:** Deploy production system to AWS using infrastructure-as-code.

```
DEPLOYMENT-AWS/
├── 01-Architecture/
│   ├── system-diagram.md (visual)
│   ├── lambda-architecture.md
│   ├── data-flow.md
│   └── security-model.md (GRAY bg)

├── 02-Infrastructure-as-Code/
│   ├── terraform/
│   │   ├── main.tf (AWS provider)
│   │   ├── lambda.tf (agent function)
│   │   ├── api-gateway.tf (REST API)
│   │   ├── rds.tf (PostgreSQL)
│   │   ├── elasticache.tf (Redis)
│   │   ├── cloudwatch.tf (monitoring)
│   │   ├── iam.tf (permissions)
│   │   ├── vpc.tf (networking)
│   │   ├── s3.tf (logging)
│   │   └── variables.tf (config)
│   │
│   └── alternative-cloudformation/
│       ├── agent-template.yaml
│       └── parameters.json

├── 03-Bedrock-Configuration/
│   ├── bedrock-setup.py
│   ├── model-config.yaml
│   ├── credentials-setup.md
│   ├── rate-limiting.md
│   └── cost-controls.md

├── 04-Containerization/
│   ├── Dockerfile
│   ├── docker-compose.yml (for testing)
│   ├── ECR-setup.md (push to AWS)
│   ├── kubernetes-deployment.yaml (if scaling)
│   └── helm-chart/ (Kubernetes package)

├── 05-CI-CD-Pipeline/
│   ├── github-actions/
│   │   ├── test.yml (run tests)
│   │   ├── build.yml (build docker)
│   │   ├── deploy.yml (deploy to AWS)
│   │   └── rollback.yml (if issues)
│   │
│   └── alternative-gitlab-ci/
│       ├── .gitlab-ci.yml

├── 06-Deployment-Guide/
│   ├── first-deployment.md (step-by-step)
│   ├── environment-setup.md
│   ├── secrets-management.md (API keys)
│   ├── database-migrations.md
│   ├── rollback-procedures.md
│   └── monitoring-post-deploy.md

└── Real Deployment:
   Deploy loan agent to AWS:
   - Lambda functions for agent
   - API Gateway for REST endpoints
   - RDS for PostgreSQL
   - ElastiCache for Redis
   - CloudWatch for monitoring
   - Bedrock for Claude access
   - S3 for logs/documents
   - Full infrastructure-as-code
```

---

### **PHASE 7: CAPSTONE PROJECT (Week 13)**

**Goal:** Build complete production system integrating everything learned.

```
CAPSTONE-LOAN-PROCESSOR/
├── 01-Project-Overview/
│   ├── requirements.md (what to build)
│   ├── success-criteria.md
│   ├── architecture-diagram.md
│   ├── timeline.md (8 days)
│   └── rubric.md (how you're graded)

├── 02-Implementation/
│   ├── agent/ (complete implementation)
│   │   ├── loan_agent.py (main agent)
│   │   ├── memory/ (Redis + PostgreSQL)
│   │   ├── tools/ (all verification tools)
│   │   ├── verification/ (Evals + Governance)
│   │   └── observability/ (LangSmith + Prometheus)
│   │
│   ├── tests/ (complete test suite)
│   │   ├── unit_tests.py
│   │   ├── integration_tests.py
│   │   ├── e2e_tests.py (Playwright)
│   │   ├── load_tests.py
│   │   └── payment_tests.py (Stripe)
│   │
│   ├── infrastructure/
│   │   ├── terraform/ (AWS setup)
│   │   ├── docker-compose.yml (local)
│   │   └── deployment.md
│   │
│   ├── monitoring/
│   │   ├── dashboards.json
│   │   ├── alerts.yaml
│   │   └── metrics.py
│   │
│   ├── api/ (REST endpoints)
│   │   ├── main.py (FastAPI)
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   └── swagger.yaml (OpenAPI)
│   │
│   └── docs/
│       ├── README.md (how to run)
│       ├── ARCHITECTURE.md (design decisions)
│       ├── DEPLOYMENT.md (how to deploy)
│       ├── MONITORING.md (how to monitor)
│       └── COST.md (cost breakdown)

├── 03-Submission-Checklist/
│   ├── Code (complete, tested)
│   ├── Documentation (clear, detailed)
│   ├── Tests (all passing)
│   ├── Deployment (works on clean AWS account)
│   ├── Monitoring (dashboards live)
│   └── Cost (analysis provided)

└── Success = Portfolio-ready project
   (Can show to employers)
```

---

### **PHASE 8: CERTIFICATION & CAREER (Weeks 14-16)**

**Week 14: CCA-F Deep Dive**
```
CCA-F-CERTIFICATION/
├── 01-Domain-Mapping/
│   ├── domain-1-architecture.md (27%)
│   ├── domain-2-claude-code.md (20%)
│   ├── domain-3-prompting.md (20%)
│   ├── domain-4-tools.md (20%)
│   ├── domain-5-context.md (13%)
│   └── coverage.md (what we've covered)

├── 02-Domain-Exercises/
│   ├── domain-1/ (5 exercises)
│   ├── domain-2/ (5 exercises)
│   ├── domain-3/ (5 exercises)
│   ├── domain-4/ (5 exercises)
│   └── domain-5/ (5 exercises)

├── 03-Study-Guide/
│   ├── key-concepts.md
│   ├── tradeoffs.md
│   ├── common-mistakes.md
│   └── quick-reference.md

├── 04-Mock-Exam/
│   ├── mock-exam-60-questions.md
│   ├── answer-key.md
│   ├── scoring.md
│   └── performance-analysis.md

└── Study Plan:
   - Review all course material
   - Do domain exercises (25 total)
   - Take mock exam multiple times
   - Target: >80% on mock before real exam
```

**Week 15: Interview Preparation**
```
INTERVIEW-PREP/
├── 01-Common-Questions/
│   ├── technical-questions.md
│   │   "Why LangGraph over LangChain?"
│   │   "How do you handle tool failures?"
│   │   "Design an agent that scales to 1M users"
│   │   "How would you debug an infinite loop?"
│   │   "Cost optimization strategies"
│   │
│   ├── architecture-questions.md
│   │   "Monolithic vs microservices agents"
│   │   "Memory strategies for long conversations"
│   │   "Error handling patterns"
│   │   "Deployment strategies"
│   │
│   └── behavioral-questions.md
│       "Tell me about a production incident"
│       "How do you approach new framework?"
│       "Team collaboration experience"

├── 02-STAR-Method/
│   ├── situation-examples.md
│   ├── task-breakdown.md
│   ├── action-frameworks.md
│   └── result-metrics.md

├── 03-System-Design/
│   ├── agent-for-1000-users.md
│   ├── agent-for-1M-users.md
│   ├── agent-with-complex-workflows.md
│   └── agent-with-compliance.md

├── 04-Portfolio-Review/
│   ├── capstone-project-walkthrough.md
│   ├── talking-points.md
│   ├── challenges-overcome.md
│   └── learnings-gained.md

└── Mock-Interview:
   - Practice with actual questions
   - Record yourself
   - Get feedback
   - Refine responses
```

**Week 16: Final Prep**
```
FINAL-PREPARATION/
├── Exam Registration
├── Last-minute Review (high-level)
├── Rest & Recovery
├── Exam Strategy
│   ├── Time management (60 min, 60 questions)
│   ├── Question approach (read carefully)
│   ├── Skipping strategy (come back to hard ones)
│   └── Final review (10 min before submit)
└── Post-Exam
    ├── Career next steps
    ├── Job search strategy
    ├── Networking
    └── Continuous learning path
```

---

## 🎨 VISUAL DESIGN SYSTEM

### **Background Colors (Semantic)**

```
WHITE (#ffffff)
├─ Basic tutorials
├─ Tool documentation
├─ Simple examples
├─ "How to do X" content

LIGHT GRAY (#f5f5f5)
├─ Concept introductions
├─ "Why we need this"
├─ Design pattern sections
├─ Problem definitions
├─ Architecture discussions

LIGHT BLUE (#f0f4ff)
├─ Certification concepts (CCA-F)
├─ Exam preparation
├─ Domain-specific deep dives
├─ Production patterns

LIGHT GREEN (#f0fff4)
├─ Working solutions
├─ Best practices
├─ Success cases
├─ Production-ready code

LIGHT RED (#f8d7da)
├─ Problems/errors
├─ Warnings
├─ What NOT to do
├─ Pitfalls
```

### **Typography**

```
Headlines (h1/h2): System fonts (-apple-system, BlinkMacSystemFont, Segoe UI)
Body: 16px line-height 1.8
Code: Courier New / Monaco, 12px
Tables: Clean borders, alternating rows
```

### **Components**

```
Info Box: Blue border left, blue background
Warning Box: Yellow border left, yellow background
Error Box: Red border left, red background
Success Box: Green border left, green background
Concept Box: GRAY background, "why this matters"
Code Block: Dark gray background, syntax highlighting
Comparison: Two columns, before/after
```

---

## 📦 GITHUB REPOSITORIES STRUCTURE

```
Main Repo (Overview + Roadmap):
AI-Agents-Production-Bootcamp/
├── 00-MASTER-ROADMAP.md (this file)
├── 01-VISUAL-DESIGN.md
├── 02-LEARNING-PATH.md
├── 03-CCA-F-MAPPING.md
├── 04-TECH-STACK.md
├── 05-ENVIRONMENT-SETUP.md
└── README.md (entry point)

Separate Repos (by phase):

Phase 1-2: Foundations
├── foundations-prompt-engineering/
├── foundations-context-engineering/
├── foundations-harness-engineering/
├── foundations-loop-engineering/
└── foundations-graph-engineering/

Phase 3-4: Loan Application
├── loan-application-evolution/
│   ├── v1-prompt-only/
│   ├── v2-context-engineering/
│   ├── v3-harness-engineering/
│   ├── v4-loop-engineering/
│   └── v5-graph-engineering/

Phase 5: Frameworks
├── framework-raw-python-sdk/
├── framework-langchain/
├── framework-langgraph/
├── framework-autogen/
├── framework-crewai/
└── framework-comparison/

Phase 6: Components
├── rag-systems-complete/
├── mcp-integration-guide/
├── memory-architectures/
└── token-optimization/

Phase 7: Production
├── testing-verification-suite/
├── observability-mlops/
└── aws-deployment-guide/

Phase 8: Capstone
├── capstone-loan-processor/

Phase 9: Certification
├── cca-f-study-guide/
├── cca-f-practice-exercises/
└── interview-prep-guide/
```

---

## ✅ KEY METRICS

**By End of Course:**
- 16 weeks of learning
- 5 engineering disciplines mastered
- 1 real use case (loan app) evolved 5 times
- 5 framework implementations
- 1 AWS deployment
- 50+ pages of documentation
- 100+ hours of hands-on coding
- 30+ test cases written
- 1 capstone project
- CCA-F certification ready
- Portfolio-ready project

**Career Outcome:**
- Can design agent systems
- Can implement with multiple frameworks
- Can deploy to AWS/production
- Can test, monitor, scale agents
- Can explain tradeoffs
- Ready for AI Architect interviews
- Has portfolio to show employers

---

**Status:** Complete outline ready for building
**Next Steps:** Build visual design guide, learning path, CCA-F mapping
