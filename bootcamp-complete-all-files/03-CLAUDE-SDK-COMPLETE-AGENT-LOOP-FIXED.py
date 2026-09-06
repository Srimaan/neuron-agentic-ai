#!/usr/bin/env python3
"""
CLAUDE SDK: COMPLETE AGENT LOOP - BROKEN vs FIXED

This file shows EXACTLY what breaks in naive implementations and HOW to fix it.

APPLICATION: Build a Research Agent
=========================================
Goal: Create an agent that finds information about Python learning resources

User asks: "Find 3 Python learning resources and summarize what they do"

What should happen:
  1. Agent searches: "Python learning resources"
  2. Agent gets back a list (e.g., "Python.org, Real Python, Codecademy")
  3. Agent decides to search each one individually
  4. Agent gets back info on each (costs, features, etc.)
  5. Agent summarizes all findings
  6. Agent returns final answer

Why this needs a LOOP:
  - Can't do all searches in one API call
  - Each tool result needs to feed back to the model
  - Model needs to decide what to do NEXT based on results
  - Multiple iterations required

Now let's build it...
"""

from anthropic import Anthropic
import sys

# =============================================================================
# PART 1: BROKEN VERSION (What Beginners Write)
# =============================================================================

def research_agent_BROKEN():
    """
    This is what beginners write. It will CRASH.
    
    Errors that will happen:
    1. IndexError: response.content[1] doesn't exist (unsafe indexing)
    2. Lost messages history (no accumulation)
    3. Missing tool_use_id (broken tool formatting)
    4. IndexError when accessing blocks that don't exist
    """
    
    client = Anthropic()
    MODEL = "claude-3-5-sonnet-20241022"
    
    TOOLS = [
        {
            "name": "web_search",
            "description": "Search the web for information",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    ]
    
    # USER QUERY
    user_query = "Find 3 Python learning resources and summarize what they do"
    
    # ❌ BROKEN CODE STARTS HERE
    print("\n" + "="*70)
    print("DEMONSTRATING BROKEN VERSION")
    print("="*70)
    print(f"\nUser Query: {user_query}\n")
    
    try:
        # MISTAKE #1: Creating messages INSIDE the loop context
        # (This gets overwritten)
        messages = [{"role": "user", "content": user_query}]
        
        print("Calling Claude API for first time...")
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            tools=TOOLS,
            messages=messages
        )
        
        print(f"Response received. Stop reason: {response.stop_reason}")
        print(f"Number of blocks: {len(response.content)}")
        
        # MISTAKE #2: Unsafe indexing - assuming structure
        print("\nTrying to access response.content[1]...")
        try:
            tool_call = response.content[1]  # ❌ CRASHES if doesn't exist
            print(f"Tool call: {tool_call}")
        except IndexError as e:
            print(f"❌ INDEXERROR: {e}")
            print(f"   Why? response.content might only have 1 block, not 2!")
            print(f"   response.content[0] exists: {response.content[0]}")
            print(f"   Trying to access [1] when it doesn't exist = CRASH")
            return
        
        # MISTAKE #3: If we got here, format tool result wrong
        if response.content[0].type == "tool_use":
            tool_name = response.content[0].name
            tool_input = response.content[0].input
            tool_use_id = response.content[0].id  # ✓ Got ID
            
            # Simulate tool execution
            tool_result = f"Simulated result for: {tool_input.get('query', 'unknown')}"
            
            # ❌ BROKEN: Missing tool_use_id!
            print(f"\nTool executed: {tool_name}")
            print(f"Tool result: {tool_result}")
            print(f"\nAdding tool result to messages (BROKEN WAY - missing tool_use_id)...")
            
            messages.append({
                "role": "assistant",
                "content": response.content
            })
            
            # ❌ THIS IS BROKEN - no tool_use_id link!
            messages.append({
                "role": "user",
                "content": tool_result  # ❌ WRONG! Should be structured with tool_use_id
            })
            
            print(f"Messages now: {len(messages)} items")
            print("❌ Problem: Tool result is disconnected from tool call!")
            print("   Model doesn't know which result belongs to which tool.")
        
        # MISTAKE #4: No termination checking
        print(f"\nNo check on stop_reason: {response.stop_reason}")
        print("❌ Problem: Don't know if model wants to continue or is done!")
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {type(e).__name__}: {e}")


# =============================================================================
# PART 2: FIXED VERSION (Production Grade)
# =============================================================================

def research_agent_FIXED():
    """
    This is the correct implementation.
    
    Fixes applied:
    1. ✓ Loop through response.content, check block.type (no unsafe indexing)
    2. ✓ Maintain messages list across iterations
    3. ✓ Include tool_use_id when adding tool results
    4. ✓ Check stop_reason to know when to exit
    5. ✓ Add max_iterations safety limit
    """
    
    client = Anthropic()
    MODEL = "claude-3-5-sonnet-20241022"
    
    TOOLS = [
        {
            "name": "web_search",
            "description": "Search the web for information",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    ]
    
    # USER QUERY
    user_query = "Find 3 Python learning resources and summarize what they do"
    
    # ✓ FIXED CODE STARTS HERE
    print("\n" + "="*70)
    print("DEMONSTRATING FIXED VERSION")
    print("="*70)
    print(f"\nUser Query: {user_query}\n")
    
    # ✓ FIX #1: Messages created ONCE, outside loop
    messages = []
    messages.append({"role": "user", "content": user_query})
    print(f"✓ Messages initialized with user query")
    
    max_iterations = 5
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        print(f"\n{'─'*70}")
        print(f"ITERATION {iteration}")
        print(f"{'─'*70}")
        
        print(f"Messages in context: {len(messages)}")
        print(f"Calling Claude API...")
        
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            tools=TOOLS,
            messages=messages
        )
        
        print(f"Response received")
        print(f"  Stop reason: {response.stop_reason}")
        print(f"  Number of blocks: {len(response.content)}")
        
        # ✓ FIX #2: Loop through blocks, check type (SAFE)
        print(f"\nProcessing response blocks:")
        has_tool_use = False
        
        for i, block in enumerate(response.content):
            print(f"  Block {i}: type={block.type}", end="")
            
            if block.type == "text":
                print(f" - text='{block.text[:60]}...'")
            
            elif block.type == "tool_use":
                print(f" - tool={block.name}")
                has_tool_use = True
                tool_name = block.name
                tool_input = block.input
                tool_use_id = block.id
                
                print(f"    Input: {tool_input}")
                
                # Simulate tool execution
                query = tool_input.get("query", "unknown")
                tool_result = f"Found 3 resources about '{query}': Python.org, Real Python, Codecademy"
                
                print(f"    Tool executed → Result: {tool_result}")
                print(f"    Tool Use ID: {tool_use_id}")
        
        # ✓ FIX #3: Add assistant message to history
        print(f"\n✓ Adding assistant response to message history...")
        messages.append({
            "role": "assistant",
            "content": response.content
        })
        
        # ✓ FIX #4: If tools were used, add results with tool_use_id
        if has_tool_use:
            print(f"✓ Tool was used, adding tool result with tool_use_id...")
            
            # Re-iterate to add results (in real code, collect these)
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    tool_result = f"Found 3 resources about '{block.input.get('query')}': Python.org, Real Python, Codecademy"
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,  # ✓ CRITICAL: Links result to tool call
                        "content": tool_result
                    })
            
            # Add all tool results at once
            messages.append({
                "role": "user",
                "content": tool_results
            })
            
            print(f"  Added {len(tool_results)} tool result(s) with tool_use_id links")
            print(f"  Total messages now: {len(messages)}")
        
        # ✓ FIX #5: Check stop_reason to know when to exit
        print(f"\n✓ Checking exit condition...")
        if response.stop_reason == "end_turn":
            print(f"✓ Model finished (stop_reason='end_turn')")
            
            # Extract final text response
            for block in response.content:
                if block.type == "text":
                    print(f"\n{'='*70}")
                    print("FINAL ANSWER:")
                    print(f"{'='*70}")
                    print(block.text)
            break
        
        elif not has_tool_use:
            print(f"✓ No tools used and stop_reason='{response.stop_reason}' → exiting")
            break
        
        else:
            print(f"→ Continuing loop (tool was used, need to continue)")
    
    if iteration >= max_iterations:
        print(f"\n⚠️ Reached max iterations ({max_iterations})")


# =============================================================================
# PART 3: COMPARISON - Side by side what's different
# =============================================================================

def show_comparison():
    """Shows the key differences between broken and fixed"""
    
    print("\n\n" + "="*70)
    print("COMPARISON: BROKEN vs FIXED")
    print("="*70)
    
    comparison = [
        {
            "issue": "Accessing response blocks",
            "broken": "tool_call = response.content[1]  # ❌ Assumes index",
            "fixed": "for block in response.content:\n    if block.type == 'tool_use':  # ✓ Type check",
            "why": "Blocks may not exist at expected index"
        },
        {
            "issue": "Messages history",
            "broken": "messages = [...]  # Inside loop (recreated each time)",
            "fixed": "messages = []  # Outside loop (persists)",
            "why": "Recreating = agent loses all context from previous iterations"
        },
        {
            "issue": "Tool result format",
            "broken": "messages.append(tool_result)  # Just raw text",
            "fixed": "{\"type\": \"tool_result\", \"tool_use_id\": block.id, \"content\": result}",
            "why": "Model needs to know which result belongs to which tool call"
        },
        {
            "issue": "Exit condition",
            "broken": "# No check (just keeps going or crashes)",
            "fixed": "if response.stop_reason == 'end_turn': break",
            "why": "Need to know when model is actually done"
        },
        {
            "issue": "Safety limit",
            "broken": "# Infinite loop possible (confuses = keeps asking)",
            "fixed": "max_iterations = 5; for i in range(max_iterations):",
            "why": "Prevent runaway costs and infinite loops"
        }
    ]
    
    for i, item in enumerate(comparison, 1):
        print(f"\n{i}. {item['issue'].upper()}")
        print(f"   ❌ Broken: {item['broken']}")
        print(f"   ✓ Fixed:  {item['fixed']}")
        print(f"   Why:     {item['why']}")


# =============================================================================
# MAIN: Run both versions
# =============================================================================

if __name__ == "__main__":
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  CLAUDE SDK: AGENT LOOP - BROKEN vs FIXED DEMONSTRATION".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    print("\n📚 This script demonstrates:")
    print("   1. What beginners write (BROKEN)")
    print("   2. Specific errors that happen")
    print("   3. Why each error occurs")
    print("   4. The correct way to fix it (FIXED)")
    print("   5. Side-by-side comparison")
    
    print("\n" + "="*70)
    print("STEP 1: Run the BROKEN version (will show errors)")
    print("="*70)
    research_agent_BROKEN()
    
    print("\n\n" + "="*70)
    print("STEP 2: Run the FIXED version (should work)")
    print("="*70)
    research_agent_FIXED()
    
    print("\n")
    show_comparison()
    
    print("\n\n" + "="*70)
    print("KEY INSIGHTS FROM THIS EXERCISE")
    print("="*70)
    print("""
1. SAFE ITERATION
   ❌ Never assume response.content[N] exists
   ✓ Always loop + check block.type
   
2. PERSISTENT STATE
   ❌ Don't recreate messages list in loop
   ✓ Create once outside, append each iteration
   
3. TOOL LINKING
   ❌ Don't send raw results
   ✓ Include tool_use_id to link result to call
   
4. LOOP CONTROL
   ❌ Don't ignore stop_reason
   ✓ Always check: "end_turn" or "tool_use"?
   
5. SAFETY GUARDRAIL
   ❌ No max_iterations = possible infinite loop
   ✓ Always set a max that prevents runaway
    """)
    
    print("\n" + "="*70)
    print("Ready for Part 2: Framework comparison (LangChain, LangGraph, etc.)")
    print("="*70)
