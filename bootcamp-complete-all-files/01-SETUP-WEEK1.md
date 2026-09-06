# WEEK 1 SETUP GUIDE
## Get Your Local Development Environment Ready

---

## 🎯 WHAT YOU'LL SET UP

By the end of this guide, you'll have:

```
✓ Python 3.11+ running
✓ Claude SDK installed  
✓ All 5 frameworks installed (Python SDK, LangChain, LangGraph, AutoGen, CrewAI)
✓ PostgreSQL database (Docker)
✓ Redis cache (Docker)
✓ API keys configured
✓ First example running
```

**Time:** 30-45 minutes  
**Difficulty:** Easy (mostly copy-paste)  
**Prerequisite:** Docker Desktop installed

---

## ✅ PREREQUISITES

Before starting, make sure you have:

### 1. Docker Desktop
- **Mac/Windows:** [Download Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Linux:** `sudo apt-get install docker.io docker-compose`
- **Verify:** `docker --version` (should show v20+)

### 2. Git
- **Mac:** `brew install git`
- **Windows:** [Download Git](https://git-scm.com/download/win)
- **Linux:** `sudo apt-get install git`
- **Verify:** `git --version`

### 3. Claude API Key
- Go to [console.anthropic.com](https://console.anthropic.com)
- Create account (free tier available)
- Generate API key
- **⚠️ Keep this secret!**

### 4. Python 3.11+
- **Mac:** `brew install python@3.11`
- **Windows:** [Download Python](https://www.python.org/downloads/)
- **Linux:** `sudo apt-get install python3.11`
- **Verify:** `python3 --version` (should show 3.11+)

---

## 📦 STEP 1: Create Project Directory

```bash
# Create directory
mkdir ai-bootcamp-week1
cd ai-bootcamp-week1

# Clone examples (or download files manually)
git clone https://github.com/your-repo/ai-bootcamp .

# List files
ls -la
# Should show:
# 01-PROMPT-ENGINEERING-101.md
# 01-PROMPT-ENGINEERING-example-01-raw-sdk.py
# 01-PROMPT-ENGINEERING-example-02-langchain.py
# ... etc
```

---

## 🐍 STEP 2: Python Environment

### Option A: Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Verify (should show "(venv)" in prompt)
python --version  # Should show 3.11+
```

### Option B: Poetry (Alternative)

```bash
# Install poetry
curl -sSL https://install.python-poetry.org | python3 -

# Create project
poetry init

# Add dependencies
poetry add anthropic langchain langchain-anthropic langgraph
```

---

## 📥 STEP 3: Install Python Packages

### Create requirements.txt

Save this as `requirements.txt`:

```
# Core
anthropic==0.29.0
python-dotenv==1.0.0

# Frameworks
langchain==0.1.0
langchain-anthropic==0.1.0
langgraph==0.0.40
pyautogen==0.2.0
crewai==0.1.0

# Utilities
requests==2.31.0
pydantic==2.5.0
```

### Install packages

```bash
pip install -r requirements.txt

# Verify installation
python -c "import anthropic; print(anthropic.__version__)"
# Should print version without error
```

---

## 🔐 STEP 4: Configure API Key

### Option A: Environment Variable (Recommended)

**Mac/Linux:**
```bash
# Create .env file
echo 'ANTHROPIC_API_KEY=your_api_key_here' > .env

# Or edit manually
nano .env
# Paste your API key

# Source it (add to ~/.bashrc or ~/.zshrc for persistence)
export ANTHROPIC_API_KEY=$(cat .env | grep ANTHROPIC_API_KEY | cut -d '=' -f 2)
```

**Windows (PowerShell):**
```powershell
# Create .env file
'ANTHROPIC_API_KEY=your_api_key_here' | Out-File -Encoding utf8 .env

# Or set environment variable permanently
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "your_key", "User")
$env:ANTHROPIC_API_KEY = "your_key"
```

### Option B: Python Code

Add to top of your Python files:

```python
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not set!")
```

### Verify

```bash
# Check it's set
echo $ANTHROPIC_API_KEY  # Should show your key
```

---

## 🗄️ STEP 5: Database Setup (Optional for Week 1)

We'll add PostgreSQL and Redis later, but here's the setup:

### Create docker-compose.yml

Save this as `docker-compose.yml`:

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: bootcamp-postgres
    environment:
      POSTGRES_USER: bootcamp
      POSTGRES_PASSWORD: bootcamp123
      POSTGRES_DB: bootcamp_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U bootcamp"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: bootcamp-redis
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

### Start databases (optional for Week 1)

```bash
# Start services
docker-compose up -d

# Verify they're running
docker-compose ps
# Should show:
# postgres    Up (healthy)
# redis       Up (healthy)

# Stop later
docker-compose down
```

---

## ✨ STEP 6: First Test Run

### Test Raw Python SDK

```bash
# Run the first example
python 01-PROMPT-ENGINEERING-example-01-raw-sdk.py
```

**Expected output:**
```
============================================================
LOAN EVALUATION SYSTEM - RAW PYTHON SDK
============================================================

EXAMPLE 1: Strong Applicant
────────────────────────────────────────────────────────
Applicant: John Doe
Credit: 750, Income: $100,000
Loan: $50,000

============================================================
DECISION: APPROVED
============================================================
Score: 250
Reason: Strong credit (750), excellent debt-to-income (0.09)...
Factors: credit_score_excellent, dti_excellent, ...
Next Step: Auto-approve and initiate loan origination process
============================================================
```

If you see JSON output with decisions, **you're set up correctly! ✅**

### Troubleshooting

**Error: ModuleNotFoundError: No module named 'anthropic'**
```bash
# Fix: Install packages
pip install -r requirements.txt
```

**Error: ANTHROPIC_API_KEY not found**
```bash
# Fix: Set environment variable
export ANTHROPIC_API_KEY=your_key
```

**Error: Connection refused**
```bash
# Fix: Check if Docker is running
docker --version
docker ps  # Should show running containers
```

---

## 🔍 STEP 7: Verify Everything Works

Run this verification script (`verify_setup.py`):

```python
#!/usr/bin/env python3
"""Verify your environment is set up correctly."""

import os
import sys

print("🔍 VERIFICATION STARTING...\n")

# Check 1: Python version
print("1️⃣ Checking Python version...")
if sys.version_info >= (3, 11):
    print("   ✅ Python 3.11+ installed")
else:
    print(f"   ❌ Python {sys.version_info.major}.{sys.version_info.minor} (need 3.11+)")
    sys.exit(1)

# Check 2: API Key
print("\n2️⃣ Checking API key...")
api_key = os.getenv("ANTHROPIC_API_KEY")
if api_key:
    print(f"   ✅ API key found (starts with {api_key[:8]}...)")
else:
    print("   ❌ ANTHROPIC_API_KEY not set")
    print("      Run: export ANTHROPIC_API_KEY=your_key")
    sys.exit(1)

# Check 3: Core packages
print("\n3️⃣ Checking core packages...")
packages = [
    ("anthropic", "Claude SDK"),
    ("langchain", "LangChain"),
    ("langgraph", "LangGraph"),
    ("autogen", "AutoGen"),
    ("crewai", "CrewAI"),
]

for package_name, display_name in packages:
    try:
        __import__(package_name)
        print(f"   ✅ {display_name} installed")
    except ImportError:
        print(f"   ❌ {display_name} not found")
        print(f"      Run: pip install {package_name}")

# Check 4: Docker
print("\n4️⃣ Checking Docker...")
import subprocess
try:
    result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"   ✅ Docker installed: {result.stdout.strip()}")
    else:
        print("   ⚠️  Docker not accessible")
except FileNotFoundError:
    print("   ⚠️  Docker not found (install Docker Desktop)")

# Check 5: Files
print("\n5️⃣ Checking example files...")
files = [
    "01-PROMPT-ENGINEERING-101.md",
    "01-PROMPT-ENGINEERING-example-01-raw-sdk.py",
    "01-PROMPT-ENGINEERING-example-02-langchain.py",
]

for file in files:
    if os.path.exists(file):
        print(f"   ✅ {file}")
    else:
        print(f"   ⚠️  {file} not found")

print("\n" + "="*60)
print("✅ SETUP VERIFICATION COMPLETE!")
print("="*60)
print("\nYou're ready to start Week 1!\n")
print("Next steps:")
print("1. Read: 01-PROMPT-ENGINEERING-101.md")
print("2. Run: python 01-PROMPT-ENGINEERING-example-01-raw-sdk.py")
print("3. Complete: Exercises in 01-PROMPT-ENGINEERING-EXERCISES.md")
```

Run it:
```bash
python verify_setup.py

# Expected output:
# ✅ Python 3.11+ installed
# ✅ API key found
# ✅ Claude SDK installed
# ✅ LangChain installed
# ✅ LangGraph installed
# ✅ AutoGen installed
# ✅ CrewAI installed
# ✅ Docker installed
# ✅ SETUP VERIFICATION COMPLETE!
```

---

## 🚀 STEP 8: Run All Examples

Once verified, try all frameworks:

```bash
# Example 1: Raw Python SDK
python 01-PROMPT-ENGINEERING-example-01-raw-sdk.py

# Example 2: LangChain
python 01-PROMPT-ENGINEERING-example-02-langchain.py

# Example 3: LangGraph
python 01-PROMPT-ENGINEERING-example-03-langgraph.py

# Example 4: AutoGen (may need additional setup)
python 01-PROMPT-ENGINEERING-example-04-autogen.py

# Example 5: CrewAI (may need additional setup)
python 01-PROMPT-ENGINEERING-example-05-crewai.py
```

Each should output loan decisions with JSON.

---

## 📋 CHECKLIST: You're Ready When...

- [ ] Python 3.11+ installed and verified
- [ ] Virtual environment created and activated
- [ ] All packages installed (`pip install -r requirements.txt`)
- [ ] ANTHROPIC_API_KEY set and verified
- [ ] First example runs successfully
- [ ] Verification script passes
- [ ] You can see JSON output from examples
- [ ] Docker running (optional for Week 1)

---

## 💡 QUICK REFERENCE

### Activate environment each session

```bash
# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Reset/clean install

```bash
# Remove old environment
rm -rf venv

# Create fresh
python3 -m venv venv
source venv/bin/activate  # or Windows equivalent
pip install -r requirements.txt
```

### Common issues

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| API key not found | Run `export ANTHROPIC_API_KEY=your_key` |
| Connection refused | Make sure Docker is running |
| Permission denied | Windows: Run PowerShell as Admin |

---

## ✅ YOU'RE DONE!

Your environment is ready. Now:

1. 📖 **Read** the main tutorial: `01-PROMPT-ENGINEERING-101.md`
2. 💻 **Run** the examples to see prompts in action
3. ✍️ **Complete** the exercises in `01-PROMPT-ENGINEERING-EXERCISES.md`
4. 🧪 **Experiment** by modifying the prompts

**Next:** Day 2 - Context Engineering 101

---

**Need help?** Check troubleshooting section above or ask in community forum.
