"""
CCA-F DEEP: Chapter 1 - Hands-On Agent Exercises
================================================

6 Progressive exercises building from simple to complex agents.
Each exercise can be run independently and tests specific concepts.

Requirements:
    pip install anthropic python-dotenv
"""

import anthropic
import json
import os
from dotenv import load_dotenv
from collections import deque
import sqlite3
from datetime import datetime
import uuid

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ============================================================================
# EXERCISE 2.1: Simple Agent (No Memory, No Persistence)
# ============================================================================

print("\n" + "="*70)
print("EXERCISE 2.1: Simple Agent - Research Task")
print("="*70)

def exercise_2_1_simple_agent():
    """
    Build a simple research agent that answers questions.
    
    Concepts Tested:
    - Tool use
    - Basic loop control
    - stop_reason handling
    - Error handling
    
    Question: Research what Claude 3.5 Sonnet can do and report findings.
    """
    
    TOOLS = [
        {
            "name": "search_knowledge_base",
            "description": "Search internal knowledge base for information",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of results (max 5)"
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "synthesize_findings",
            "description": "Combine findings into summary",
            "input_schema": {
                "type": "object",
                "properties": {
                    "findings": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of findings to synthesize"
                    }
                },
                "required": ["findings"]
            }
        }
    ]
    
    def execute_tool(tool_name: str, tool_input: dict) -> str:
        """Simulate tool execution"""
        if tool_name == "search_knowledge_base":
            query = tool_input.get("query", "")
            if "claude 3.5" in query.lower() or "sonnet" in query.lower():
                return json.dumps([
                    "Claude 3.5 Sonnet: 200K context window",
                    "Claude 3.5 Sonnet: Improved reasoning",
                    "Claude 3.5 Sonnet: Better code generation",
                    "Claude 3.5 Sonnet: Faster inference",
                    "Claude 3.5 Sonnet: 2024 release"
                ])
            return json.dumps(["No results found"])
        
        elif tool_name == "synthesize_findings":
            findings = tool_input.get("findings", [])
            return f"Synthesis complete: Reviewed {len(findings)} findings"
        
        return "Unknown tool"
    
    messages = []
    user_query = "What are the key capabilities of Claude 3.5 Sonnet?"
    messages.append({"role": "user", "content": user_query})
    
    max_iterations = 10
    iteration = 0
    
    print(f"\n🔍 Query: {user_query}\n")
    
    while iteration < max_iterations:
        iteration += 1
        print(f"📍 Iteration {iteration}")
        
        # Phase ②: Reason & Decide
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            tools=TOOLS,
            messages=messages
        )
        
        print(f"   Stop reason: {response.stop_reason}")
        
        # Phase ④: Check if done
        if response.stop_reason == "end_turn":
            print("   ✅ Agent finished")
            final_text = next(
                (block.text for block in response.content if hasattr(block, "text")),
                ""
            )
            print(f"\n📝 Answer:\n{final_text}\n")
            return final_text
        
        # Phase ③: Take action
        elif response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            
            for block in response.content:
                if block.type == "tool_use":
                    print(f"   🔧 Calling {block.name}({block.input})")
                    result = execute_tool(block.name, block.input)
                    print(f"      → {result[:60]}...")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })
            
            messages.append({"role": "user", "content": tool_results})
    
    print("⚠️ Max iterations reached")
    return None

# Run exercise
exercise_2_1_simple_agent()

# ============================================================================
# EXERCISE 2.2: Agent with Persistent Memory
# ============================================================================

print("\n" + "="*70)
print("EXERCISE 2.2: Agent with Persistent Memory (Database)")
print("="*70)

class PersistentAgent:
    """Agent that saves state to database"""
    
    def __init__(self, agent_id: str, db_path: str = "agent_exercise.db"):
        self.agent_id = agent_id
        self.db_path = db_path
        self.session_id = str(uuid.uuid4())[:8]
        self.messages = []
        self.iteration = 0
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                agent_id TEXT,
                created_at TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                session_id TEXT,
                role TEXT,
                content TEXT,
                created_at TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_state (
                session_id TEXT PRIMARY KEY,
                iteration_count INTEGER,
                is_complete BOOLEAN,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        """)
        conn.commit()
        
        # Create session
        cursor.execute(
            "INSERT INTO sessions (session_id, agent_id, created_at) VALUES (?, ?, ?)",
            (self.session_id, self.agent_id, datetime.now())
        )
        cursor.execute(
            "INSERT INTO agent_state (session_id, iteration_count, is_complete) VALUES (?, ?, ?)",
            (self.session_id, 0, False)
        )
        conn.commit()
        conn.close()
    
    def add_message(self, role: str, content: str):
        """Add message and immediately persist"""
        self.messages.append({"role": role, "content": content})
        
        # Persist to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO messages (session_id, role, content, created_at) VALUES (?, ?, ?, ?)",
            (self.session_id, role, str(content)[:1000], datetime.now())
        )
        conn.commit()
        conn.close()
    
    def update_iteration(self, count: int):
        """Update iteration count"""
        self.iteration = count
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE agent_state SET iteration_count = ? WHERE session_id = ?",
            (count, self.session_id)
        )
        conn.commit()
        conn.close()
    
    def load_messages(self) -> list:
        """Load messages from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT role, content FROM messages WHERE session_id = ? ORDER BY id",
            (self.session_id,)
        )
        self.messages = [{"role": r, "content": c} for r, c in cursor.fetchall()]
        conn.close()
        return self.messages
    
    def __repr__(self):
        return f"Agent(id={self.agent_id}, session={self.session_id}, messages={len(self.messages)})"

def exercise_2_2_persistent_agent():
    """
    Demonstrate agent memory persistence.
    
    Concepts Tested:
    - Database persistence
    - Session recovery
    - Message recovery
    
    Scenario: Simulate agent crash and recovery
    """
    
    print("\n🚀 Creating agent and running 2 iterations...")
    agent = PersistentAgent("research-bot-001")
    
    # Simulate first execution
    agent.add_message("user", "Research Python programming")
    agent.add_message("assistant", "I will search for Python information")
    agent.update_iteration(1)
    
    print(f"✅ Agent created: {agent}")
    print(f"   Session ID: {agent.session_id}")
    print(f"   Messages stored: {len(agent.messages)}")
    
    # Simulate crash and restart
    print("\n💥 Simulating crash...")
    print("🔄 Restarting agent...")
    
    # Create new agent instance with SAME session_id
    recovered_agent = PersistentAgent.__new__(PersistentAgent)
    recovered_agent.agent_id = "research-bot-001"
    recovered_agent.session_id = agent.session_id
    recovered_agent.db_path = agent.db_path
    
    # Load messages from database
    messages = recovered_agent.load_messages()
    print(f"✅ Recovery successful!")
    print(f"   Messages recovered: {len(messages)}")
    for msg in messages:
        print(f"      - {msg['role']}: {msg['content'][:50]}...")

# Run exercise
exercise_2_2_persistent_agent()

# ============================================================================
# EXERCISE 2.3: Loop Detection & Prevention
# ============================================================================

print("\n" + "="*70)
print("EXERCISE 2.3: Detecting and Preventing Infinite Loops")
print("="*70)

def exercise_2_3_loop_detection():
    """
    Demonstrate loop detection patterns.
    
    Concepts Tested:
    - Tool call history tracking
    - Loop detection logic
    - Breaking out of loops
    """
    
    print("\n📊 Simulating tool call history:\n")
    
    tool_history = deque(maxlen=5)
    tool_calls = ["search", "fetch", "search", "fetch", "search"]  # Loop pattern
    
    for i, tool in enumerate(tool_calls):
        tool_history.append(tool)
        
        # Check for infinite loop
        unique_tools = set(tool_history)
        print(f"Call {i+1}: {tool}")
        print(f"  History: {list(tool_history)}")
        print(f"  Unique tools: {unique_tools}")
        
        # Loop detection: if only 1-2 unique tools in last 5 calls
        if len(unique_tools) <= 2 and len(tool_history) >= 4:
            print(f"  ⚠️ LOOP DETECTED! Breaking...")
            break
        print()
    
    print("✅ Loop detection complete")

exercise_2_3_loop_detection()

# ============================================================================
# EXERCISE 2.4: Memory Summarization Pattern
# ============================================================================

print("\n" + "="*70)
print("EXERCISE 2.4: Memory Summarization to Prevent Token Overflow")
print("="*70)

def exercise_2_4_memory_summarization():
    """
    Demonstrate memory summarization pattern.
    
    Concepts Tested:
    - Detecting token growth
    - Summarizing old messages
    - Keeping recent context
    """
    
    print("\n📈 Simulating token growth:\n")
    
    messages = []
    iteration = 0
    max_token_window = 8000  # Hypothetical limit
    current_tokens = 0
    summarization_threshold = 6000  # Summarize when reaching 75%
    
    for iteration in range(15):
        # Each iteration adds ~500 tokens
        message_tokens = 500
        current_tokens += message_tokens
        
        print(f"Iteration {iteration+1}: +{message_tokens} tokens = {current_tokens} total")
        
        # Check if we need to summarize
        if current_tokens > summarization_threshold:
            print(f"  ⚠️ Approaching limit ({summarization_threshold}/{max_token_window})")
            print(f"  📝 SUMMARIZING old messages...")
            
            # Keep only recent messages, summarize old ones
            old_messages_summary = f"[SUMMARY OF ITERATIONS 1-{iteration-2}]: Agent researched topic, found key findings]"
            recent_messages = f"[Recent iterations: {iteration-1}, {iteration}]"
            
            current_tokens = len(old_messages_summary.split()) * 1.3 + len(recent_messages.split()) * 1.3
            print(f"  ✅ After summarization: {current_tokens:.0f} tokens\n")
        else:
            print()

exercise_2_4_memory_summarization()

# ============================================================================
# EXERCISE 2.5: Error Handling in Tool Execution
# ============================================================================

print("\n" + "="*70)
print("EXERCISE 2.5: Robust Tool Error Handling")
print("="*70)

def exercise_2_5_error_handling():
    """
    Demonstrate error handling patterns.
    
    Concepts Tested:
    - Tool error responses
    - Retry logic
    - Graceful degradation
    """
    
    print("\n🔧 Simulating tool calls with errors:\n")
    
    def call_unreliable_tool(attempt: int) -> dict:
        """Simulate tool that fails intermittently"""
        if attempt < 2:
            return {
                "status": "error",
                "message": "Connection timeout",
                "recoverable": True,
                "retry_after": 1
            }
        return {
            "status": "success",
            "data": "Tool executed successfully",
            "duration_ms": 245
        }
    
    # Retry pattern
    max_retries = 3
    for attempt in range(max_retries):
        result = call_unreliable_tool(attempt)
        print(f"Attempt {attempt+1}:")
        print(f"  Result: {result}")
        
        if result["status"] == "success":
            print("  ✅ Success!")
            break
        elif result.get("recoverable"):
            print(f"  ⚠️ Recoverable error, retrying...")
        else:
            print(f"  ❌ Fatal error, giving up")
            break

exercise_2_5_error_handling()

print("\n" + "="*70)
print("✅ ALL EXERCISES COMPLETED")
print("="*70)
print("\nKey Learnings:")
print("  1. Simple agents are just loops: Gather → Reason → Act → Reflect")
print("  2. Memory must be persisted IMMEDIATELY after each message")
print("  3. Always detect and break infinite loops")
print("  4. Summarize old messages to prevent token overflow")
print("  5. Handle tool errors gracefully with retries")
print("\nNext: Review production patterns and assessment questions")
