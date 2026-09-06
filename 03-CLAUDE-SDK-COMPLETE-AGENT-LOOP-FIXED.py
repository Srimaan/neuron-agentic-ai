"""
FIXED: Claude SDK Complete Agent Loop
======================================

This is the CORRECT implementation of the 4-phase agent loop:
  Phase ①: Gather Context (add user message to history)
  Phase ②: Reason & Decide (call Claude, get response)
  Phase ③: Take Action (execute tools)
  Phase ④: Observe & Reflect (add results to history, continue or exit)

Key fixes from previous version:
✅ Don't assume response.content[1] - loop through blocks
✅ Maintain messages list across iterations
✅ Properly format tool results with tool_use_id
✅ Handle no-tool-call case (end_turn)
✅ Safety max_iterations limit

Run this file:
    python CLAUDE-SDK-COMPLETE-AGENT-LOOP-FIXED.py
"""

from anthropic import Anthropic

# Initialize client
client = Anthropic()

# ============================================================================
# STEP 1: Define the tools agent can use
# ============================================================================

TOOLS = [
    {
        "name": "search_web",
        "description": "Search the web for information about a topic",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "What to search for"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "fetch_page",
        "description": "Fetch the full content of a webpage",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL to fetch"
                }
            },
            "required": ["url"]
        }
    },
    {
        "name": "analyze_data",
        "description": "Analyze data or information",
        "input_schema": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "string",
                    "description": "Data to analyze"
                }
            },
            "required": ["data"]
        }
    }
]


# ============================================================================
# STEP 2: Implement tool execution
# ============================================================================

def execute_tool(tool_name: str, tool_input: dict) -> str:
    """
    Execute a tool and return results.
    
    In production, this would call real APIs.
    Here we simulate the results.
    """
    if tool_name == "search_web":
        query = tool_input.get("query", "")
        print(f"      🌐 Searching web for: '{query}'")
        return f"""
        Search Results for '{query}':
        
        1. "AI Breakthroughs 2024" - TechNews.com
           Recent developments in large language models and multimodal AI
        
        2. "Evolution of Claude" - AnthropicBlog.com
           Claude 3.5 Sonnet released with 200K context window
        
        3. "AI Safety & Alignment" - ResearchPaper.com
           New approaches to AI safety and constitutional AI
        """
    
    elif tool_name == "fetch_page":
        url = tool_input.get("url", "")
        print(f"      📄 Fetching page: {url}")
        return f"""
        Full Content from {url}:
        
        Title: Latest AI Breakthroughs in 2024
        
        The field of AI has seen remarkable progress this year:
        - Claude 3.5 Sonnet with improved reasoning
        - Multimodal models that understand images and text together
        - Advances in long-context understanding (200K tokens)
        - Better cost-performance tradeoffs
        - Improved safety and alignment techniques
        
        Key developments highlighted by industry experts...
        """
    
    elif tool_name == "analyze_data":
        data = tool_input.get("data", "")
        print(f"      📊 Analyzing data...")
        return f"""
        Analysis Results:
        
        Analyzed content: {data[:50]}...
        
        Key Findings:
        - Main topics: AI, advancement, 2024, models
        - Sentiment: Positive (78%)
        - Relevance: High
        - Actionable insights: Multiple
        
        Recommendation: Compile findings into comprehensive summary
        """
    
    else:
        return f"Unknown tool: {tool_name}"


# ============================================================================
# STEP 3: Implement the complete 4-phase loop
# ============================================================================

def run_agent(user_query: str, max_iterations: int = 10) -> str:
    """
    Run the agent loop with proper 4-phase structure.
    
    Phase ①: Gather Context
    Phase ②: Reason & Decide
    Phase ③: Take Action
    Phase ④: Observe & Reflect
    
    Args:
        user_query: The user's question/request
        max_iterations: Maximum loop iterations (safety limit)
    
    Returns:
        Final response from the agent
    """
    
    # Initialize conversation history
    messages = []
    iteration = 0
    
    print("\n" + "="*70)
    print(f"🔍 STARTING AGENT")
    print(f"📝 User Query: {user_query}")
    print("="*70)
    
    # ✅ PHASE ①: GATHER CONTEXT
    print("\n✅ PHASE ① - GATHER CONTEXT")
    print("   Adding user message to conversation history...")
    messages.append({
        "role": "user",
        "content": user_query
    })
    print(f"   Messages in history: {len(messages)}")
    
    # Loop until agent stops or we hit max iterations
    while iteration < max_iterations:
        iteration += 1
        print(f"\n{'='*70}")
        print(f"📍 ITERATION {iteration}")
        print(f"{'='*70}")
        
        # ✅ PHASE ②: REASON & DECIDE
        print("\n✅ PHASE ② - REASON & DECIDE")
        print(f"   Calling Claude with {len(messages)} messages in history...")
        
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            tools=TOOLS,
            messages=messages
        )
        
        print(f"   Response received")
        print(f"   Stop reason: {response.stop_reason}")
        
        # Check if agent is done or wants to use tools
        if response.stop_reason == "end_turn":
            # Agent says it's done - extract final answer
            print("\n✅ PHASE ④ - OBSERVE & REFLECT")
            print("   Agent decided to stop (end_turn)")
            print("   Extracting final answer...")
            
            # Extract text from response
            final_answer = ""
            for block in response.content:
                if hasattr(block, 'text'):
                    final_answer = block.text
                    break
            
            print(f"\n{'='*70}")
            print("🎉 AGENT COMPLETED TASK")
            print(f"{'='*70}")
            print(f"\n📝 FINAL ANSWER:\n{final_answer}\n")
            return final_answer
        
        elif response.stop_reason == "tool_use":
            # Agent wants to use tools
            print("\n✅ PHASE ③ - TAKE ACTION")
            print("   Agent wants to use tools")
            
            # Add agent's response to messages
            # ⚠️ CRITICAL: Add the response with all blocks, not just tool_use
            messages.append({
                "role": "assistant",
                "content": response.content
            })
            print(f"   Added agent response to history")
            
            # Collect all tool results
            tool_results = []
            
            # ✅ CRITICAL FIX: Loop through blocks, don't assume index!
            for block in response.content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input
                    tool_use_id = block.id
                    
                    print(f"\n   🔧 Tool Call Detected")
                    print(f"      Tool: {tool_name}")
                    print(f"      Input: {tool_input}")
                    
                    # Execute the tool (Phase ③)
                    result = execute_tool(tool_name, tool_input)
                    print(f"      ✓ Tool executed, got result")
                    
                    # Format tool result correctly
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use_id,  # ⚠️ Must match the request!
                        "content": result
                    })
            
            # ✅ PHASE ④: OBSERVE & REFLECT
            print("\n✅ PHASE ④ - OBSERVE & REFLECT")
            print(f"   Adding {len(tool_results)} tool results to history...")
            
            # Add all tool results so LLM can see them
            messages.append({
                "role": "user",
                "content": tool_results
            })
            
            print(f"   Messages in history: {len(messages)}")
            print(f"   Loop continues → Back to PHASE ①")
        
        else:
            # Unexpected stop reason
            print(f"\n⚠️ Unexpected stop_reason: {response.stop_reason}")
            break
    
    # If we get here, we hit max iterations
    print(f"\n⚠️ Reached max iterations ({max_iterations})")
    return "Task incomplete - max iterations reached"


# ============================================================================
# STEP 4: Main execution
# ============================================================================

if __name__ == "__main__":
    # Example 1: Simple research query
    print("\n")
    print("█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "  CLAUDE SDK: COMPLETE AGENT LOOP EXAMPLE".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    
    # Run the agent
    result = run_agent(
        user_query="Research the latest AI breakthroughs in 2024 and summarize the key developments"
    )
    
    print("\n" + "="*70)
    print("✅ AGENT SESSION COMPLETE")
    print("="*70)
    print("\nKey Lessons:")
    print("  ✓ Maintained messages list across iterations")
    print("  ✓ Looped through response.content blocks safely")
    print("  ✓ Formatted tool results with tool_use_id")
    print("  ✓ Followed 4-phase loop: Gather → Reason → Act → Reflect")
    print("  ✓ Had safety max_iterations limit")
