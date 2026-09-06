# PRODUCTION TECHNOLOGY STACK
## AI Agents Bootcamp - Complete Tools & Services

---

## 🏗️ ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────┐
│ USER / UI LAYER                                         │
├─────────────────────────────────────────────────────────┤
│ Frontend (React/HTML) | Playwright (E2E Testing)        │
├─────────────────────────────────────────────────────────┤
│ API LAYER (REST + WebSocket)                            │
├─────────────────────────────────────────────────────────┤
│ Application Layer (Agent orchestration)                 │
│                                                          │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ AGENTIC AI LAYER                                    │ │
│ │                                                      │ │
│ │ Frameworks:                                         │ │
│ │  ├─ Raw Python + Claude SDK                         │ │
│ │  ├─ LangChain / LangGraph                          │ │
│ │  ├─ AutoGen                                         │ │
│ │  └─ CrewAI                                          │ │
│ │                                                      │ │
│ │ Libraries:                                          │ │
│ │  ├─ Evals (LangSmith)                              │ │
│ │  ├─ RAGAs (RAG evaluation)                         │ │
│ │  ├─ PromptFoo (prompt testing)                     │ │
│ │  └─ Presidio (PII detection)                       │ │
│ └─────────────────────────────────────────────────────┘ │
│                            ↓                             │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ MEMORY & CONTEXT LAYER                              │ │
│ │                                                      │ │
│ │  ├─ Session: Redis (hot data)                      │ │
│ │  ├─ Persistent: PostgreSQL (history)               │ │
│ │  └─ Semantic: Pinecone / Weaviate (embeddings)     │ │
│ └─────────────────────────────────────────────────────┘ │
│                            ↓                             │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ INTEGRATION & TOOLS LAYER (MCP)                     │ │
│ │                                                      │ │
│ │  ├─ Custom MCP servers                             │ │
│ │  ├─ External APIs (Stripe, etc)                    │ │
│ │  └─ Database connectors                            │ │
│ └─────────────────────────────────────────────────────┘ │
│                            ↓                             │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ LLM LAYER                                           │ │
│ │                                                      │ │
│ │  AWS Bedrock (Production)                          │ │
│ │   └─ Claude 3 Sonnet / Opus                        │ │
│ │                                                      │ │
│ │  Direct Claude API (Testing/Dev)                   │ │
│ │   └─ Same models, direct access                    │ │
│ └─────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│ MONITORING & OBSERVABILITY LAYER                        │
│                                                         │
│ Tracing:       Jaeger / OpenTelemetry                   │
│ Metrics:       Prometheus / CloudWatch                  │
│ Logging:       CloudWatch / Structured logs             │
│ Tracking:      LangSmith (runs & feedback)              │
│ Dashboards:    Grafana                                  │
│ Alerting:      PagerDuty / Slack                        │
├─────────────────────────────────────────────────────────┤
│ TESTING & QUALITY LAYER                                 │
│                                                         │
│ Unit:          pytest                                   │
│ Integration:   Docker, pytest-docker                    │
│ E2E:           Playwright                               │
│ Payments:      Stripe test mode                         │
│ Governance:    Presidio, Fairness ML, Evals            │
│ Load:          Locust                                   │
├─────────────────────────────────────────────────────────┤
│ INFRASTRUCTURE & DEPLOYMENT LAYER                       │
│                                                         │
│ IaC:           Terraform                                │
│ Containers:    Docker / Docker Compose                  │
│ Orchestration: Kubernetes (optional)                    │
│ Serverless:    AWS Lambda                               │
│ API:           API Gateway                              │
│ CI/CD:         GitHub Actions                           │
│ Storage:       S3 (logs, documents)                     │
│ Database:      RDS (PostgreSQL)                         │
│ Cache:         ElastiCache (Redis)                      │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 DEVELOPMENT TOOLS

### **Language & Runtime**

```
Python 3.11+ (minimum)
├─ Type hints (pydantic, typing)
├─ Async support (asyncio)
├─ Virtual environments
└─ Package management (pip, poetry)

Node.js 18+ (optional, for frontend)
├─ React or vanilla HTML/JS
├─ npm/yarn for dependencies
└─ TypeScript (recommended)
```

### **IDE & Editors**

```
Recommended:
├─ VS Code (free, lightweight)
├─ PyCharm Pro (powerful)
├─ JetBrains Fleet (modern)
└─ Cursor (AI-assisted)

Essential Extensions (VS Code):
├─ Python (Microsoft)
├─ Docker
├─ REST Client
├─ Database Client
├─ Git Graph
└─ Thunder Client (API testing)
```

### **Version Control**

```
Git + GitHub
├─ Repositories for each phase
├─ Feature branches for development
├─ PR-based reviews
├─ Tags for releases
└─ Actions for CI/CD
```

---

## 🤖 AI / LLM LAYER

### **Primary: Claude via Bedrock (Production)**

```
AWS Bedrock
├─ Models:
│  ├─ Claude 3 Opus (most capable)
│  ├─ Claude 3 Sonnet (balanced, recommended)
│  ├─ Claude 3 Haiku (fast, cheap)
│  └─ Claude 3.5 Sonnet (latest)
├─ Setup:
│  ├─ AWS account required
│  ├─ Bedrock API access (request)
│  ├─ IAM roles/credentials
│  └─ Regional endpoint selection
├─ Cost:
│  ├─ Input tokens: $3/MTok
│  ├─ Output tokens: $15/MTok
│  └─ Volume discounts available
└─ Advantages:
   ├─ Enterprise features
   ├─ VPC integration
   ├─ Audit trails
   └─ Cost controls
```

### **Secondary: Direct Claude API (Development)**

```
Anthropic API
├─ Models: (Same as Bedrock)
├─ Setup:
│  ├─ api.anthropic.com
│  ├─ API key in environment
│  └─ Python SDK
├─ Cost:
│  ├─ Same pricing as Bedrock
│  └─ Pay-as-you-go
└─ Advantages:
   ├─ Simpler setup
   ├─ Good for testing
   └─ No AWS required
```

### **Anthropic SDKs**

```
Python SDK
├─ pip install anthropic
├─ Async support
├─ Streaming
├─ Tool use
└─ Vision capability

Node.js SDK (optional)
├─ npm install @anthropic-ai/sdk
├─ Similar features
└─ TypeScript types
```

---

## 🔧 AGENT FRAMEWORKS

### **1. Raw Python + Claude SDK**

```
When to use:
├─ Learning (understand fundamentals)
├─ Custom requirements
├─ Maximum control
└─ Production (sometimes)

Pros:
├─ Full control
├─ No abstraction
├─ Maximum flexibility
└─ Good for learning

Cons:
├─ More boilerplate
├─ Maintenance burden
├─ Must handle errors manually
└─ Testing harder

Example repo:
framework-raw-python-sdk/
├── agent.py (main loop)
├── tools.py (tool definitions)
├── memory.py (state management)
├── utils.py (helpers)
└── tests/ (pytest)
```

### **2. LangChain**

```
Installation:
pip install langchain langchain-anthropic langchain-community

When to use:
├─ Rapid development
├─ Composable chains
├─ Agent abstraction
└─ Production (often)

Components:
├─ LLMChain (Claude calls)
├─ Tools (tool definitions)
├─ Memory (conversation history)
├─ AgentExecutor (loop management)
└─ Callbacks (monitoring hooks)

Pros:
├─ Rich component library
├─ Handles loops for you
├─ Tool management built-in
├─ Memory abstractions
└─ Community (lots of examples)

Cons:
├─ Abstraction overhead
├─ Less control than raw
├─ Rapid API changes
└─ Learning curve

Example repo:
framework-langchain/
├── chain.py (chain definition)
├── tools.py (LangChain tools)
├── memory.py (LangChain memory)
├── agent.py (AgentExecutor)
└── tests/
```

### **3. LangGraph**

```
Installation:
pip install langgraph langchain-anthropic

When to use:
├─ Complex workflows
├─ Explicit state machines
├─ Debugging required
├─ Production (most often)

Components:
├─ StateGraph (explicit DAG)
├─ Nodes (decision points)
├─ Edges (transitions)
├─ State (shared data structure)
└─ Persistence (optional)

Pros:
├─ Explicit workflows
├─ Easy debugging
├─ Clear control flow
├─ State management built-in
├─ Testable design
└─ Production-ready

Cons:
├─ More verbose
├─ Requires state design
└─ Newer (less examples)

Example repo:
framework-langgraph/
├── graph.py (state machine)
├── nodes/ (decision nodes)
├── edges/ (routing)
├── state.py (state definition)
└── tests/
```

### **4. AutoGen**

```
Installation:
pip install pyautogen

When to use:
├─ Multi-agent systems
├─ Agent conversations
├─ Complex orchestration
└─ Specialized tasks

Components:
├─ AssistantAgent (Claude-backed)
├─ UserProxyAgent (user input)
├─ GroupChat (multi-agent)
├─ Functions (tool calling)

Pros:
├─ Multi-agent out-of-box
├─ Natural conversations
├─ Composition patterns
└─ Scaling capabilities

Cons:
├─ High abstraction
├─ Less transparency
├─ Harder to debug
└─ Opinionated design

Example repo:
framework-autogen/
├── agents.py (agent definitions)
├── functions.py (tool definitions)
├── group_chat.py (orchestration)
└── tests/
```

### **5. CrewAI**

```
Installation:
pip install crewai

When to use:
├─ Role-based systems
├─ Team hierarchies
├─ Task management
└─ Specialized roles

Components:
├─ Agent (role definition)
├─ Task (objective)
├─ Crew (team coordination)
├─ Process (execution flow)

Pros:
├─ Simple role abstraction
├─ Task-driven design
├─ Good for teams
└─ Clean API

Cons:
├─ High-level abstraction
├─ Less control
├─ Limited customization
└─ Smaller community

Example repo:
framework-crewai/
├── agents.py (role agents)
├── tasks.py (task definitions)
├── crew.py (team setup)
└── tests/
```

### **Framework Comparison Matrix**

```
                Raw SDK  LangChain  LangGraph  AutoGen  CrewAI
Control        ████      ████       ████       ██       ██
Learning Curve ███       ████       ████       ████     ██
Documentation  ██        ████       ███        ███      ███
Community      ██        ████       ███        ███      ██
Production     ████      ████       ████       ███      ███
Scalability    ███       ███        ████       ███      ██
Debugging      ███       ███        ████       ██       ██
Testing        ███       ███        ████       ██       ██

Best for:
├─ Raw SDK: Learning, custom requirements
├─ LangChain: Rapid dev, standard patterns
├─ LangGraph: Production, complex flows
├─ AutoGen: Multi-agent conversations
└─ CrewAI: Role-based team systems
```

---

## 🧠 EVALUATION & VERIFICATION

### **Prompt Testing: PromptFoo**

```
Installation:
npm install -g promptfoo

Use for:
├─ Test cases for prompts
├─ Version control prompts
├─ A/B testing
├─ Automated scoring
└─ Results tracking

Typical workflow:
1. Define test cases (JSON)
2. Define prompts to test
3. Run: promptfoo eval
4. Compare results
5. Commit best version

Output:
├─ Results table
├─ Comparison charts
├─ Score aggregation
└─ Provenance tracking

Example config (promptfoo.yaml):
```yaml
providers:
  - id: bedrock-claude
    config:
      modelId: anthropic.claude-3-sonnet-20240229-v1:0

tests:
  - description: "Should approve good loans"
    prompt: "Evaluate: {application}"
    expected:
      - type: contains
        value: "Approved"

  - description: "Should deny risky loans"
    prompt: "Evaluate: {application}"
    expected:
      - type: not-contains
        value: "Approved"

outputs:
  - type: table
  - type: json
```
```

### **Agent Output Evaluation: LangSmith Evals**

```
Installation:
pip install langsmith

Use for:
├─ Track agent runs
├─ Define evaluators
├─ Collect feedback
├─ Aggregate metrics
└─ A/B test agents

Typical workflow:
1. Run agent with LangSmith
2. Define eval functions
3. Collect feedback
4. View dashboard
5. Improve based on metrics

Example eval:
```python
from langsmith import evaluate, Client
from langsmith.schemas import Example

def validate_decision(run: Run, example: Example) -> dict:
    output = run.outputs.get("decision", {})
    
    return {
        "score": 1.0 if output.get("status") else 0.0,
        "details": {
            "has_decision": "status" in output,
            "has_reason": len(output.get("reason", "")) > 50,
            "valid_amount": output.get("amount", 0) > 0
        }
    }

# Evaluate
client = Client()
evaluate(
    agent.invoke,
    data=client.list_examples(dataset_name="loans"),
    evaluators=[validate_decision],
    experiment_prefix="v1"
)
```
```

### **RAG Evaluation: RAGAs**

```
Installation:
pip install ragas

Use for:
├─ Evaluate retrieval quality
├─ Measure answer faithfulness
├─ Track RAG improvements
└─ Detect degradation

Metrics:
├─ faithfulness (answer grounded in context?)
├─ answer_relevancy (answer relevant to query?)
├─ context_recall (relevant context retrieved?)
├─ context_precision (irrelevant context avoided?)
└─ answer_similarity (similar to reference?)

Example:
```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy

results = evaluate(
    dataset=rag_dataset,
    metrics=[faithfulness, answer_relevancy]
)

# faithfulness > 0.8 = good
# answer_relevancy > 0.7 = good
```
```

### **AI Governance: Presidio + Fairness**

```
Installation:
pip install presidio-analyzer presidio-anonymizer

Use for:
├─ PII detection/redaction
├─ Bias detection
├─ Compliance checking
└─ Fairness auditing

Example:
```python
from presidio_analyzer import AnalyzerEngine

analyzer = AnalyzerEngine()
results = analyzer.analyze(text="...", language="en")

for result in results:
    print(f"Found {result.entity_type}: {result.start}:{result.end}")
    # PERSON, CREDIT_CARD, EMAIL, etc

# Redact PII
from presidio_anonymizer import AnonymizerEngine
anonymizer = AnonymizerEngine()
redacted = anonymizer.anonymize(text="...", analyzer_results=results)
```
```

---

## 💾 DATA & MEMORY LAYER

### **Session Memory: Redis**

```
What it's for:
├─ Real-time state
├─ Current conversation
├─ TTL-based expiry
└─ High performance

Setup (Docker):
docker run -d -p 6379:6379 redis:7

Python client:
pip install redis

Usage:
```python
import redis
r = redis.Redis(host='localhost', port=6379)

# Store
r.set('session_123', json.dumps(state), ex=3600)  # 1 hour TTL

# Retrieve
state = json.loads(r.get('session_123'))

# List keys
keys = r.keys('session_*')
```
```

### **Persistent Memory: PostgreSQL**

```
What it's for:
├─ Permanent storage
├─ Audit trails
├─ Full history
└─ Complex queries

Setup (Docker):
docker run -d -e POSTGRES_PASSWORD=password \
  -p 5432:5432 postgres:15

Python client:
pip install psycopg2-binary sqlalchemy

Schema example:
```sql
CREATE TABLE agents_runs (
  id UUID PRIMARY KEY,
  timestamp TIMESTAMP,
  input TEXT,
  output JSON,
  tokens_used INT,
  cost DECIMAL(10, 4),
  decision_type VARCHAR(50),
  approved BOOLEAN,
  reason TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_timestamp ON agents_runs(timestamp);
CREATE INDEX idx_decision_type ON agents_runs(decision_type);
```

Usage:
```python
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base, Session

engine = create_engine('postgresql://user:pass@localhost/db')
Base = declarative_base()

class AgentRun(Base):
    __tablename__ = 'agents_runs'
    id = Column(String, primary_key=True)
    output = Column(JSON)
    # ... other fields

# Save
session = Session(engine)
session.add(AgentRun(id='123', output={...}))
session.commit()

# Query
results = session.query(AgentRun).filter_by(decision_type='approved').all()
```
```

### **Semantic Memory: Vector Database**

```
Options (choose one):
├─ Pinecone (managed, simplest)
├─ Weaviate (self-hosted or cloud)
├─ Milvus (open source)
└─ Chroma (lightweight)

Setup (Weaviate Docker):
docker run -d -p 8080:8080 semitechnologies/weaviate:latest

Python client:
pip install weaviate-client

Usage:
```python
import weaviate
import weaviate.classes.config as wvcc

client = weaviate.connect_to_local()

# Define collection
client.collections.create(
    name="LoanDocuments",
    vectorizer_config=wvcc.Configure.Vectorizer.text2vec_openai(),
)

collection = client.collections.get("LoanDocuments")

# Add documents with embeddings
collection.data.insert(
    properties={
        "title": "Loan Policy 001",
        "content": "...",
    },
    vector=[0.1, 0.2, 0.3, ...]  # Embedding from OpenAI/Anthropic
)

# Search
results = collection.query.near_vector(
    near_vector=[...],
    limit=5
)
```
```

---

## 🔌 INTEGRATION & TOOLS

### **MCP (Model Context Protocol)**

```
What it is:
├─ Standard tool definition format
├─ Server-client architecture
├─ JSON-based protocol
└─ Language-agnostic

Building MCP Server:
```python
from mcp.server import Server, Request
from mcp.types import Tool, TextContent

server = Server("loan-tools")

@server.define_tool(
    name="check_credit",
    description="Check credit score",
    input_schema={
        "type": "object",
        "properties": {
            "ssn": {"type": "string"}
        }
    }
)
async def check_credit(ssn: str) -> TextContent:
    score = fetch_credit_score(ssn)
    return TextContent(text=str(score))

if __name__ == "__main__":
    server.run()
```

MCP Servers we'll build:
├─ Credit check service
├─ Employment verification
├─ Collateral evaluation
└─ Compliance check
```

### **External APIs: Stripe**

```
For: Payment processing, testing

Setup:
1. Create Stripe account
2. Get API keys (test mode)
3. pip install stripe

Test cards:
├─ 4242 4242 4242 4242 - Success
├─ 4000 0000 0000 0002 - Decline
├─ 3782 822463 10005 - Amex

Usage:
```python
import stripe

stripe.api_key = "sk_test_..."

# Create payment intent
intent = stripe.PaymentIntent.create(
    amount=50000,
    currency="usd",
)

# Confirm payment
confirmed = stripe.PaymentIntent.confirm(
    intent.id,
    payment_method="pm_card_visa"
)

# Handle webhooks
@app.post("/webhook")
def handle_webhook(request):
    event = stripe.Event.construct_from(
        json.loads(request.body), stripe.api_key
    )
    
    if event["type"] == "charge.succeeded":
        # Handle success
        pass
```
```

---

## 🧪 TESTING LAYER

### **Unit Testing: pytest**

```
Installation:
pip install pytest pytest-asyncio pytest-cov

Basic structure:
```
tests/
├── conftest.py (shared fixtures)
├── test_agent.py (agent tests)
├── test_tools.py (tool tests)
├── test_memory.py (memory tests)
└── test_utils.py (utility tests)
```

Example test:
```python
import pytest
from agent import evaluate_loan

@pytest.fixture
def good_applicant():
    return {
        "name": "John",
        "credit_score": 750,
        "income": 100000
    }

def test_approve_good_loan(good_applicant):
    result = evaluate_loan(good_applicant)
    assert result["status"] == "approved"
    assert "reason" in result

def test_deny_bad_loan():
    bad = {"credit_score": 600, "income": 20000}
    result = evaluate_loan(bad)
    assert result["status"] == "denied"

# Run: pytest tests/
# Coverage: pytest --cov=. tests/
```
```

### **Integration Testing: Docker**

```
Docker Compose for test environment:
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"

  redis:
    image: redis:7
    ports:
      - "6379:6379"

  app:
    build: .
    depends_on:
      - postgres
      - redis
    environment:
      DATABASE_URL: postgresql://postgres:password@postgres:5432/test
      REDIS_URL: redis://redis:6379

  tests:
    build: .
    depends_on:
      - app
    command: pytest tests/integration/
```

Run: `docker-compose -f docker-compose.test.yml up`
```

### **E2E Testing: Playwright**

```
Installation:
pip install playwright
playwright install

Example:
```python
from playwright.sync_api import sync_playwright

def test_loan_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Navigate to app
        page.goto("http://localhost:3000")
        
        # Fill form
        page.fill("#name", "John Doe")
        page.fill("#amount", "50000")
        
        # Submit
        page.click("#submit")
        
        # Wait for result
        page.wait_for_selector("#decision", timeout=30000)
        
        # Assert
        decision = page.inner_text("#decision")
        assert "approved" in decision.lower() or "denied" in decision.lower()
        
        browser.close()
```
```

### **Load Testing: Locust**

```
Installation:
pip install locust

Example:
```python
from locust import HttpUser, task, between

class LoanAgentUser(HttpUser):
    wait_time = between(1, 5)
    
    @task
    def evaluate_loan(self):
        self.client.post("/evaluate", json={
            "amount": 50000,
            "income": 100000,
            "credit_score": 750
        })

# Run: locust -f locustfile.py -u 100 -r 10 -t 5m
# -u: 100 concurrent users
# -r: spawn 10 users/sec
# -t: run for 5 minutes
```
```

---

## 📊 OBSERVABILITY & MONITORING

### **Metrics: Prometheus**

```
Installation:
docker run -d -p 9090:9090 prom/prometheus

Config (prometheus.yml):
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'agent'
    static_configs:
      - targets: ['localhost:8000']
```

Python instrumentation:
```python
from prometheus_client import Counter, Histogram, Gauge

decisions_total = Counter(
    'decisions_total',
    'Total decisions',
    ['status']  # approved, denied, review
)

decision_duration = Histogram(
    'decision_duration_seconds',
    'Time to decide',
    buckets=(1, 5, 10, 30, 60)
)

tokens_used = Counter(
    'tokens_used_total',
    'Total tokens used',
    ['model']
)

# Usage
decisions_total.labels(status='approved').inc()
decision_duration.observe(2.5)
```
```

### **Logging: CloudWatch**

```
AWS-native logging service

Setup:
```python
import boto3
import watchtower
import logging

logger = logging.getLogger(__name__)
logger.addHandler(
    watchtower.CloudWatchLogHandler(
        log_group='/aws/lambda/loan-agent',
        stream_name='production'
    )
)

# Usage
logger.info("Loan evaluated", extra={
    "decision": "approved",
    "amount": 50000,
    "tokens": 250
})
```
```

### **Tracing: Jaeger + OpenTelemetry**

```
Installation:
docker run -d -p 6831:6831/udp -p 16686:16686 jaegertracing/all-in-one

pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-jaeger

Setup:
```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

tracer = trace.get_tracer(__name__)

# Usage
with tracer.start_as_current_span("evaluate_loan") as span:
    span.set_attribute("amount", 50000)
    # ... code ...
```

Access UI: http://localhost:16686
```

### **Dashboards: Grafana**

```
Installation:
docker run -d -p 3000:3000 grafana/grafana

Setup:
1. Create Prometheus data source
2. Import/create dashboards
3. Add alerts

Key dashboards:
├─ Agent health (uptime, errors)
├─ Token usage (cost tracking)
├─ Decision quality (approval rate)
├─ Latency (p50, p95, p99)
└─ System resources (CPU, memory)
```

### **Tracing Agent Runs: LangSmith**

```
Installation:
pip install langsmith

Setup:
```python
import os
from langsmith import Client

os.environ["LANGSMITH_API_KEY"] = "your_key"
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = "loan-agent"

client = Client()

# Runs are automatically traced in LangSmith
# View at: https://smith.langchain.com
```

Features:
├─ Run tracking (inputs/outputs)
├─ Latency monitoring
├─ Token usage
├─ Error tracking
├─ Feedback collection
└─ A/B testing
```

---

## ☁️ AWS & DEPLOYMENT

### **Infrastructure as Code: Terraform**

```
Structure:
```
terraform/
├── main.tf (provider, backend)
├── lambda.tf (Lambda functions)
├── api.tf (API Gateway)
├── rds.tf (PostgreSQL)
├── cache.tf (Redis)
├── iam.tf (roles/policies)
├── cloudwatch.tf (monitoring)
└── variables.tf (configuration)
```

Key resources:
├─ Lambda (agent function)
├─ API Gateway (REST API)
├─ RDS (PostgreSQL)
├─ ElastiCache (Redis)
├─ Secrets Manager (API keys)
├─ CloudWatch (logs, metrics)
└─ IAM (permissions)
```

### **Containers: Docker**

```
Dockerfile:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

docker-compose.yml:
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:pass@db:5432/db
      REDIS_URL: redis://redis:6379
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7

volumes:
  postgres_data:
```
```

### **Orchestration: Kubernetes (Optional)**

```
For scaling to 1000+ concurrent agents

Deployment:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: loan-agent
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: agent
        image: loan-agent:latest
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
```

Service:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: loan-agent
spec:
  type: LoadBalancer
  selector:
    app: loan-agent
  ports:
  - port: 80
    targetPort: 8000
```
```

### **CI/CD: GitHub Actions**

```
.github/workflows/deploy.yml:
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: pytest tests/
      - run: pytest --cov=. tests/

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: docker build -t loan-agent .
      - run: docker push loan-agent:latest
      - run: terraform apply -auto-approve
```
```

---

## 📋 COMPLETE STACK SUMMARY

### **By Layer**

```
LLM:              Claude (Bedrock or API)
Frameworks:       Python SDK, LangChain, LangGraph, AutoGen, CrewAI
Evaluation:       PromptFoo, LangSmith, RAGAs, Presidio
Memory:           Redis, PostgreSQL, Pinecone/Weaviate
Integration:      MCP, Stripe, Custom APIs
Testing:          pytest, Docker, Playwright, Locust
Observability:    Prometheus, Grafana, Jaeger, CloudWatch, LangSmith
Infrastructure:   Terraform, Docker, Kubernetes (optional)
CI/CD:            GitHub Actions
Cloud:            AWS (Bedrock, Lambda, RDS, ElastiCache, S3)
```

### **By Learning Phase**

```
Week 1-2:     Python, Claude SDK, Docker
Week 3-4:     Databases (PostgreSQL, Redis)
Week 5-7:     LangChain, LangGraph, AutoGen, CrewAI
Week 8:       RAG (Weaviate), MCP
Week 9:       Token optimization, Memory patterns
Week 10-11:   Testing (pytest, Playwright), Evals, Monitoring
Week 12:      AWS Bedrock, Terraform, Lambda
Week 13:      Complete integration
Week 14-16:   Deployment, scaling, operations
```

---

**Status:** Complete technology stack defined
**Next:** Environment setup guide, GitHub repository structure
