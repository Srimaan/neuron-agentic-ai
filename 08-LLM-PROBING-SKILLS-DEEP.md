# LLM Probing Skills for Agentic AI Expertise

These are prompts/skills you can use with Claude or other LLMs to probe deep understanding of agentic AI concepts. Use these to test yourself or evaluate learners.

---

## Probing Skill 1: Memory Management Scenarios

**Use this skill to test memory architecture understanding**

```
PROMPT TEMPLATE: Memory Architecture Decisions

You are an expert AI architect evaluating a learner's understanding of agent memory.

Present this SCENARIO:

"An autonomous agent will run for 8 hours straight, handling 100+ requests. 
Each request generates ~50 message tokens. The LLM context window is 200K tokens.

QUESTION 1: What memory strategy would you use? Why?
QUESTION 2: If the process crashes after 4 hours, what happens to memory in each strategy?
QUESTION 3: How would you handle the token overflow problem?

Evaluate the learner's response on these criteria:
- Do they mention persistent storage (database)?
- Do they consider recovery from crashes?
- Do they address token overflow?
- Do they discuss trade-offs between strategies?

If their answer misses any criterion, ask a FOLLOW-UP:
'Your answer mentions [X] but doesn't address [Y]. 
When the agent crashes, how would you recover [Y]? 
What database schema would you use?'

Keep probing until they fully understand:
1. In-memory = fast but loses data on crash
2. Database = persistent and recoverable
3. Semantic memory = smart retrieval of large knowledge bases
4. Hybrid = combine strategies based on use case
"
```

---

## Probing Skill 2: Loop Control Scenarios

**Test their understanding of termination conditions and loop detection**

```
PROMPT TEMPLATE: Agent Loop Control

Present this CODE SCENARIO:

```python
for iteration in range(20):
    response = client.messages.create(...)
    
    if response.stop_reason == "tool_use":
        tool_result = execute_tool(...)  # Tool always returns same result
        messages.append(tool_result)
    elif response.stop_reason == "end_turn":
        break
```

QUESTION 1: What problem does this code have?
QUESTION 2: Write code to detect and prevent this problem.
QUESTION 3: What's the difference between max_iterations and tool_call_limit?

If they miss the infinite loop problem, prompt:
'This agent calls the same tool 10 times, gets the same result each time.
What's the LLM likely to do? Why is this dangerous?
How would you fix it?'

If they don't mention tracking tool history, ask:
'How do you know if a tool was called before? What data structure would you use?
Show me the detection code.'

Keep probing until they understand:
- Loop detection via tool history tracking
- Difference between loop termination signals
- Why detecting infinite loops is critical in production
```

---

## Probing Skill 3: Error Recovery Scenarios

**Test their understanding of robust error handling**

```
PROMPT TEMPLATE: Production Error Handling

Present this FAILURE SCENARIO:

"Your agent calls an external API to search. The API:
- Returns rate limit (429) on attempt 1
- Returns timeout (504) on attempt 2
- Returns success on attempt 3

The API tells you: 'Retry-After: 60' on rate limit
The timeout has no retry info.

QUESTION 1: How would you handle each error type differently?
QUESTION 2: Write code for exponential backoff retry logic.
QUESTION 3: When should you give up and escalate to human?

Then ask follow-ups:
- 'Should rate limit errors be retried immediately or after delay?'
- 'How many retries before giving up? Why?'
- 'What information should you log for debugging?'

Probe deeper:
- 'If a tool fails 3 times, should the agent restart from beginning or keep state?'
- 'How does error recovery differ for different tool types (read vs. write)?'
- 'What happens if the agent retries inside a database transaction?'

They should understand:
- Transient errors (retry) vs. fatal errors (escalate)
- Exponential backoff to avoid overwhelming systems
- Circuit breakers to disable failing tools temporarily
- Atomic operations to prevent partial failures
"
```

---

## Probing Skill 4: Framework Selection Scenarios

**Test their ability to choose right framework for use case**

```
PROMPT TEMPLATE: Framework Decision Matrix

Give learner 5 SCENARIOS. For each, ask:
"Which framework would you choose? Why?"

SCENARIO 1:
"Build a code generation agent. 
- Must support human-in-the-loop approval
- Complex branching logic (generate → review → revise)
- Need to visualize agent decision flow"
Expected answer: LangGraph
Probe: "Why not Claude SDK alone? What does LangGraph add?"

SCENARIO 2:
"Build a research agent that searches web and synthesizes findings.
- Simple sequential flow (search → fetch → summarize)
- Need to prototype quickly"
Expected answer: LangChain or Claude SDK
Probe: "What's the trade-off between LangChain and Claude SDK?"

SCENARIO 3:
"Build multi-agent system where agents debate about problem.
- 3 agents with different roles (analyzer, critic, synthesizer)
- Agents send messages to each other autonomously"
Expected answer: AutoGen
Probe: "Why can't you use LangChain for this? What makes AutoGen better?"

SCENARIO 4:
"Build an agentic system where you need maximum control and debugging.
- Must see exactly what agent does at each step
- Will run for long time, need memory recovery
- Custom error handling for sensitive operations"
Expected answer: Claude SDK
Probe: "You're trading speed for control. How is this worth it?"

SCENARIO 5:
"Build an agent for a startup MVP. 
- Limited engineering resources
- Need to launch in 2 weeks
- Simple agent that answers questions"
Expected answer: Crew AI or LangChain
Probe: "What's the risk of choosing Crew AI? When would you switch to something else?"

Score depth:
- Level 1: Picks correct framework
- Level 2: Explains key trade-offs
- Level 3: Discusses migration paths (Crew AI → LangGraph when complexity grows)
- Level 4: Explains production implications (monitoring, scaling, cost)
"
```

---

## Probing Skill 5: Deep Architecture Decisions

**Test comprehensive system design understanding**

```
PROMPT TEMPLATE: Full Agent Architecture Design

Give learner this DESIGN CHALLENGE:

"Design an autonomous agent system for a customer support company.

REQUIREMENTS:
- Handle 1,000 concurrent agents
- Each agent may run for 10+ minutes
- Agents must persist state (DB crash recovery)
- Track costs (charge customer based on agent usage)
- Monitor for failures (alert if agent loops infinitely)
- Audit trail for compliance

QUESTIONS:
1. What's your architecture? Draw it (describe components)
2. How do you handle 1,000 concurrent agents with limited API quota?
3. How do you prevent cost runaway (agent uses $100 for $10 task)?
4. How do you detect and break infinite loops?
5. How do you recover if the agent service crashes?
6. How do you scale this to 10,000 concurrent agents?

Then probe each answer:
- Architecture Q: Ask about bottlenecks, failure modes
- Concurrency Q: Ask about queueing, load balancing
- Cost Q: Ask how you'd implement per-agent token budget
- Loop detection Q: Ask for specific code
- Recovery Q: Ask what you'd persist to DB and why
- Scaling Q: Ask about database choice, sharding strategy

Score at levels:
- Level 1: Basic architecture sketch
- Level 2: Includes persistence layer
- Level 3: Addresses monitoring and cost control
- Level 4: Complete production-ready design with failure recovery

Examples of level 4 thinking:
- 'Each agent gets token budget. Track tokens spent per iteration.'
- 'Use queue + worker pool to handle 1000 concurrent agents'
- 'Persist messages immediately after each step (not after agent completes)'
- 'Circuit breaker: disable tool after 3 consecutive failures'
- 'Use distributed tracing to track agent execution path'
"
```

---

## Probing Skill 6: Real-World Debugging

**Test their ability to debug production issues**

```
PROMPT TEMPLATE: Debug Real-World Problems

Present PROBLEM SCENARIOS:

PROBLEM 1: "Agent is taking 2 minutes per query but should take 30 seconds. What could be wrong?"
Probes:
- Are tokens accumulating? (Check message history growth)
- Is tool execution slow? (Add timing to tool calls)
- Is LLM slow? (Compare to benchmarks)
- Is there unnecessary retrying? (Check retry logic)
Expected answer: Systematic instrumentation to find bottleneck

PROBLEM 2: "Agent works perfectly in testing but crashes in production after 30 minutes. Why?"
Probes:
- Could be memory leak (messages growing unbounded)
- Could be database connection pool exhaustion
- Could be API rate limiting (subtle - no error returned)
- Could be context window overflow
Expected answer: Add logging to find root cause

PROBLEM 3: "Agent sometimes succeeds, sometimes fails on same input. Non-deterministic behavior."
Probes:
- Is temperature set correctly? (Randomness in LLM)
- Are tools non-deterministic? (External API changes)
- Is race condition in concurrent execution?
- Is memory state different each time?
Expected answer: Find and isolate variable behavior

For each problem, ask:
- 'How would you instrument code to find this?'
- 'What metrics would you monitor?'
- 'What logs would be helpful?'
- 'How would you reproduce this locally?'

Score based on:
- Do they ask right questions? (Debug mindset)
- Do they use systematic approach? (Not random guessing)
- Do they understand common failure modes?
"
```

---

## Probing Skill 7: Memory Patterns - Deep Scenarios

**Test understanding of memory architecture subtleties**

```
PROMPT TEMPLATE: Memory Pattern Expert

SCENARIO A: "Agent has been running for 4 hours. Messages history is 50K tokens.
LLM context is 200K. Agent can still run, but for how long?"

Expected answer calculations:
- 50K history + 1K LLM response + 1K new messages = 52K per iteration
- Can fit ~3 more iterations (52 * 3 = 156K < 200K)
- After that, fails or needs summarization

Probe: "How would you redesign to run forever?"
- Implement summarization (reduce old messages to 5K summary)
- Keep only recent N messages (last 10 messages = ~5K tokens)
- Use semantic memory (embed messages, retrieve relevant ones)

SCENARIO B: "Agent database has 10M messages from 1000 agents.
When agent restarts, how long to load history?"

Expected answer:
- Loading 10K messages per agent from DB = ~1-2 seconds
- Can optimize with indexed queries
- Could paginate: load last 100 messages, lazy load older

Probe: "Scale to 1M messages per agent. Now what?"
- Can't load all. Implement memory tier strategy.
- Hot: Recent messages (in memory)
- Warm: Last N days (indexed DB, quick query)
- Cold: Archive storage (rarely accessed)

SCENARIO C: "Two agent instances run in parallel. Both read same messages from DB.
Both add new messages simultaneously. Race condition?"

Expected answer:
- Yes, if not careful. Last write might overwrite previous.
- Solution: Use database transactions (ACID guarantees)
- Or: Use optimistic locking (version numbers)
- Or: Use message queue (atomic writes)

Probe: "What if database transaction fails mid-message-write?"
- Message partially written to DB
- Agent crashed before saving to local memory
- On restart, which messages load?
- Need idempotent operations (safe to retry)
"
```

---

## How to Use These Skills

### With Claude (Self-Assessment)
```
Send this prompt to Claude:

"I'm learning agentic AI architecture. Use Probing Skill 3 (Error Recovery)
to test my understanding. Give me a scenario, ask questions, and probe
deeper based on my answers. Keep going until you think I really understand
error handling in production agents."

Then engage in dialogue. Claude will ask probing questions and evaluate.
```

### With Team (Group Assessment)
```
Pick a skill (e.g., Skill 5: Architecture Design)
Have each person solve independently (30 min)
Then discuss as a group, comparing approaches
Use probing questions to deepen understanding
```

### Self-Study Checklist
```
✅ Can I pass Probing Skill 1? (Memory management)
✅ Can I pass Probing Skill 2? (Loop control)
✅ Can I pass Probing Skill 3? (Error recovery)
✅ Can I pass Probing Skill 4? (Framework selection)
✅ Can I pass Probing Skill 5? (Full architecture design)
✅ Can I pass Probing Skill 6? (Debugging real problems)
✅ Can I pass Probing Skill 7? (Advanced memory patterns)

If you fail any skill, go back to that section and study harder.
```

---

## Grading Rubric

### Level 1: Surface Understanding
- Can explain basic concepts
- Knows frameworks exist
- Passes simple questions

### Level 2: Working Knowledge
- Can build simple agents
- Understands trade-offs
- Can debug basic issues

### Level 3: Production Expertise
- Can architect complex systems
- Anticipates failure modes
- Knows when to use each framework
- Handles edge cases

### Level 4: Expert Mastery
- Can design for scale (1000+ agents)
- Minimizes cost and latency
- Handles all failure scenarios
- Mentors others

**You should aim for Level 3-4 to become a production-ready agentic AI architect.**

---

## Tips for Using These Skills Effectively

1. **Don't peek at answers** - Try each scenario on your own first
2. **Write actual code** - Not just describe it
3. **Think about failure modes** - "What could go wrong?"
4. **Compare frameworks** - Don't just memorize "Claude SDK is best"
5. **Practice at scale** - Think about 1000 agents, not just 1
6. **Debug systematically** - Instrumentation before guessing
7. **Read production code** - See how real companies do it

---

**Created:** CCA-F Deep Training
**Purpose:** Assess and develop production-ready agentic AI expertise
**Target:** Architects building systems with 100+ agents, 24/7 operation

Use these skills to continuously evaluate and deepen your understanding! 🚀
