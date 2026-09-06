# Week 2 Setup Guide

## Environment Preparation

### Prerequisites
✅ Python 3.9+
✅ pip or poetry
✅ API keys (Anthropic, optional: LangChain, etc.)
✅ Database (PostgreSQL, SQLite, or in-memory for learning)

---

## Step 1: Install Dependencies

```bash
# Core
pip install anthropic

# Framework options (install what you need)
pip install langchain langchain-core
pip install langgraph
pip install pyautogen
pip install crewai

# Optional: More frameworks
pip install semantic-kernel
pip install haystack-ai
pip install dspy-ai
pip install phidata

# Database & utilities
pip install sqlalchemy
pip install psycopg2-binary  # PostgreSQL
pip install redis  # Caching
pip install python-dotenv

# Token counting
pip install tiktoken

# Testing
pip install pytest
```

---

## Step 2: Setup API Keys

Create `.env` file:

```bash
# .env
ANTHROPIC_API_KEY=sk-ant-your-key-here
OPENAI_API_KEY=sk-your-key-here  # Optional for some frameworks

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=loan_db
DB_USER=postgres
DB_PASSWORD=password

# Redis (caching)
REDIS_URL=redis://localhost:6379
```

Load in Python:

```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
```

---

## Step 3: Database Setup

### Option A: SQLite (Quick, Local)
```python
import sqlite3

# Create database
conn = sqlite3.connect("loans.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        credit_score INTEGER,
        income REAL,
        email TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS loans (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        amount REAL,
        status TEXT,
        created_at TIMESTAMP
    )
""")

conn.commit()
print("SQLite database created: loans.db")
```

### Option B: PostgreSQL (Production)
```bash
# Create database
createdb loan_db

# Connect
psql loan_db
```

```sql
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    credit_score INTEGER,
    income NUMERIC,
    email VARCHAR(100)
);

CREATE TABLE loans (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    amount NUMERIC,
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Step 4: Sample Data

```python
import sqlite3

conn = sqlite3.connect("loans.db")
cursor = conn.cursor()

# Insert sample customers
customers = [
    ("Alice Johnson", 750, 150000, "alice@example.com"),
    ("Bob Smith", 650, 80000, "bob@example.com"),
    ("Charlie Brown", 580, 40000, "charlie@example.com"),
]

cursor.executemany(
    "INSERT INTO customers (name, credit_score, income, email) VALUES (?, ?, ?, ?)",
    customers
)

# Insert sample loans
loans = [
    (1, 50000, "approved", "2024-01-15"),
    (1, 100000, "denied", "2024-02-20"),
    (2, 30000, "pending", "2024-03-10"),
]

cursor.executemany(
    "INSERT INTO loans (customer_id, amount, status, created_at) VALUES (?, ?, ?, ?)",
    loans
)

conn.commit()
print("Sample data inserted")
```

---

## Step 5: Verify Setup

### Test Anthropic API
```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)

print(message.content[0].text)
```

### Test Token Counting
```python
response = client.messages.count_tokens(
    model="claude-3-5-sonnet-20241022",
    messages=[
        {"role": "user", "content": "Hello" * 100}
    ]
)

print(f"Tokens: {response.input_tokens}")
```

### Test Database
```python
import sqlite3

conn = sqlite3.connect("loans.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM customers")
print(cursor.fetchall())
```

---

## Step 6: Framework-Specific Setup

### LangChain Setup
```bash
pip install langchain langchain-anthropic
```

```python
from langchain_anthropic import ChatAnthropic
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory)
```

### LangGraph Setup
```bash
pip install langgraph langgraph-core
```

```python
from langgraph.graph import StateGraph
from typing_extensions import TypedDict

class State(TypedDict):
    context: str
    messages: list
```

### Strands Setup
```bash
pip install strands-agents
```

```python
from strands import Agent, Tool

agent = Agent(
    model="claude-3-5-sonnet-20241022"
)
```

---

## Step 7: Create Project Structure

```
week2-context-engineering/
├── .env
├── requirements.txt
├── loans.db
├── src/
│   ├── __init__.py
│   ├── database.py
│   ├── context.py
│   ├── frameworks/
│   │   ├── raw_sdk.py
│   │   ├── langchain_impl.py
│   │   ├── langgraph_impl.py
│   │   └── ... (other frameworks)
│   └── utils.py
├── exercises/
│   ├── 01_token_counting.py
│   ├── 02_context_retrieval.py
│   ├── 03_compression.py
│   └── ... (other exercises)
└── tests/
    └── test_context.py
```

---

## Step 8: Troubleshooting

### Issue: `ModuleNotFoundError`
```bash
# Reinstall
pip install --upgrade anthropic
pip install --force-reinstall langchain
```

### Issue: API Key Not Found
```python
# Verify
import os
print(os.getenv("ANTHROPIC_API_KEY"))  # Should print your key
```

### Issue: Database Connection Error
```python
# Test connection
import sqlite3
try:
    conn = sqlite3.connect("loans.db")
    print("✓ Database connected")
except Exception as e:
    print(f"✗ Error: {e}")
```

### Issue: Token Count Too High
```python
# Count before sending
response = client.messages.count_tokens(
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": your_context}]
)

if response.input_tokens > 150000:
    print("⚠️ Context is too large, consider compression")
```

---

## Step 9: Verify All Frameworks

```bash
# Test each framework
python -c "from anthropic import Anthropic; print('✓ Raw SDK')"
python -c "from langchain_anthropic import ChatAnthropic; print('✓ LangChain')"
python -c "from langgraph.graph import StateGraph; print('✓ LangGraph')"
python -c "import pyautogen; print('✓ AutoGen')"
python -c "from crewai import Agent; print('✓ CrewAI')"
# ... etc
```

---

## Ready to Go! ✅

All setup complete. Start with:
1. **Tutorial:** 24-CONTEXT-ENGINEERING-101.md
2. **Exercises:** 26-CONTEXT-ENGINEERING-EXERCISES.md
3. **Frameworks:** 27-36 (Code examples)

