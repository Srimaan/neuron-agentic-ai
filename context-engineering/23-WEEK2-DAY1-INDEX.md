# Week 2, Day 1: Context Engineering 101

## Learning Objectives

By end of this day, you will understand:

✅ **Context in Claude** — How Claude uses context
✅ **Context Window** — Token management (200K tokens)
✅ **Context Strategies** — How to structure information
✅ **Database Integration** — Retrieving context from databases
✅ **Long Context** — Managing 100K+ token conversations
✅ **Context Compression** — Summarization techniques
✅ **Frameworks Approach** — 15 frameworks + context patterns

---

## 📚 Learning Paths

### **Path 1: Theory First (Recommended for Learning)**
1. **Tutorial:** 24-CONTEXT-ENGINEERING-101.md (30 min)
2. **Setup:** 25-SETUP-WEEK2.md (15 min)
3. **Exercises:** 26-CONTEXT-ENGINEERING-EXERCISES.md (45 min)
4. **Framework Pick:** Choose 2-3 frameworks
5. **Implementation:** 27-36 (Code examples)

### **Path 2: Hands-On First (Quick Start)**
1. **Setup:** 25-SETUP-WEEK2.md (15 min)
2. **Pick Framework:** 27-36 (Start coding)
3. **Tutorial:** 24-CONTEXT-ENGINEERING-101.md (Reference)
4. **Exercises:** 26 (Validation)

### **Path 3: Framework Comparison (Advanced)**
1. **Comparison:** Review 19-COMPLETE-FRAMEWORK-COMPARISON.md
2. **Select Frameworks:** Choose top 3
3. **Implement:** 27-36 (Compare approaches)
4. **Analyze:** Which handles context best?

---

## 🎯 Today's Topics

### **Topic 1: Understanding Context (30 min)**
- What is context?
- Claude's context window (200K tokens)
- Token counting
- Context limits

### **Topic 2: Context Strategies (45 min)**
- Structuring context
- Retrieval patterns
- Compression techniques
- Memory integration

### **Topic 3: Database Integration (30 min)**
- Pulling context from databases
- Real-time context retrieval
- Caching strategies
- Performance optimization

### **Topic 4: Long Context Applications (30 min)**
- 100K+ token conversations
- Document processing
- Code analysis
- Meeting transcripts

### **Topic 5: Framework Implementations (60 min)**
- See frameworks 27-36
- Each handles context differently
- Compare approaches
- Choose best for your use case

---

## 💻 Code Examples Overview

### Raw SDK (27)
```python
# Explicit context management
messages = [
    {"role": "user", "content": "Here is context: " + context_text}
]
```

### LangChain (28)
```python
# Built-in context handling
chain = ConversationChain(
    memory=ConversationBufferMemory()
)
```

### LangGraph (29)
```python
# Stateful context
class State(TypedDict):
    context: str
    messages: list
```

### And 7 more frameworks...

---

## 📊 Quick Comparison

| Framework | Context Handling | Memory | Best For |
|-----------|---|---|---|
| Raw SDK | Manual | None | Learning |
| LangChain | Built-in chains | ConversationMemory | Quick apps |
| LangGraph | State management | Stateful | Complex |
| AutoGen | Message history | Conversation | Multi-agent |
| CrewAI | Task context | Agent memory | Teams |
| Strands | Model-managed | Built-in | Autonomous |
| Semantic Kernel | Plugin-based | Skills | Enterprise |
| Haystack | Pipeline-based | Document stores | RAG |
| DSPy | Modular context | Example cache | Optimization |
| Phidata | Simple memory | Built-in | Fast proto |

---

## 🔄 Framework Applications This Week

**All 10 frameworks will show:**
1. How to manage context
2. How to add information
3. How to retrieve from database
4. How to handle 100K+ tokens
5. How to optimize costs

Same loan evaluator example, but now with:
- Customer history context
- Loan policies context
- Market data context
- Document context

---

## 📋 Exercise Overview

### Exercise 1: Token Counting (Easy, 10 min)
Count tokens in different context sizes

### Exercise 2: Context Retrieval (Medium, 20 min)
Pull context from simulated database

### Exercise 3: Context Compression (Medium, 25 min)
Summarize long context for token efficiency

### Exercise 4: Multi-Round Context (Hard, 30 min)
Handle conversation with growing context

### Exercise 5: Long Document (Hard, 35 min)
Process 50K+ token document

### Exercise 6: Framework Comparison (Hard, 40 min)
Implement same task in 2+ frameworks

---

## 🚀 Learning Checklist

By end of today, check off:

- [ ] Understand context window (200K tokens)
- [ ] Know how to count tokens
- [ ] Can structure context effectively
- [ ] Can retrieve context from database
- [ ] Handled long conversations (100K+ tokens)
- [ ] Implemented context in 2-3 frameworks
- [ ] Compared framework approaches
- [ ] Made decision: which framework for context?

---

## 📚 Resources

**Tutorial:** 24-CONTEXT-ENGINEERING-101.md
**Setup:** 25-SETUP-WEEK2.md
**Exercises:** 26-CONTEXT-ENGINEERING-EXERCISES.md
**Frameworks:** 27-36 (Code examples for each)
**HTML Version:** 37-CONTEXT-ENGINEERING-101-MODERN.html

---

## ⏱️ Time Allocation

| Activity | Time | File |
|----------|------|------|
| Tutorial | 30 min | 24 |
| Setup | 15 min | 25 |
| Exercises | 60 min | 26 |
| Framework reading | 45 min | 27-36 |
| Coding practice | 60 min | Choose 2-3 |
| Comparison | 30 min | 19 |
| **Total** | **240 min (4 hours)** | |

---

## 🎓 Next Steps

**After Week 2, Day 1:**
- Deep understanding of context handling
- Know which framework fits your needs
- Ready for Week 2, Day 2 (Advanced patterns)

**Before Week 3:**
- Build context manager for loan app
- Implement in chosen framework
- Test with 100K+ token conversations

---

## 💡 Key Concepts to Remember

1. **Context Window:** Claude has 200K tokens to work with
2. **Token Counting:** Matters for cost & performance
3. **Retrieval:** Context comes from databases, not just user input
4. **Compression:** Summarize to fit more information
5. **Memory:** Different from context (persists across conversations)
6. **Frameworks:** Different approaches to context management
7. **Optimization:** Trade-off between context size and cost

---

**Ready? Start with Tutorial (24) or Setup (25)!** 🚀

