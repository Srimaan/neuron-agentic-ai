# Agent Frameworks in Java

Since you asked about Java — here's a comprehensive guide to building agents in Java, plus how they compare to Python frameworks.

---

## Top 5 Java Agent Frameworks

### 1. **LangChain4j** — Direct Java Port of LangChain
**Most Popular Java Agent Framework**

```java
import dev.langchain4j.agent.tool.Tool;
import dev.langchain4j.service.AiServices;

class LoanTools {
    @Tool("Check credit score")
    int checkCredit(String name, int score) {
        return score >= 750 ? 40 : score >= 650 ? 25 : 0;
    }
}

class LoanEvaluator {
    public static void main(String[] args) {
        LoanEvaluator evaluator = AiServices.builder(LoanEvaluator.class)
            .chatLanguageModel(OpenAiChatModel.withApiKey("sk-..."))
            .tools(new LoanTools())
            .build();
        
        String result = evaluator.evaluate(780, 150000, 50000);
        System.out.println(result);
    }
    
    String evaluate(int credit, double income, double loan);
}
```

**Pros:**
- ✓ Closest to Python LangChain
- ✓ Great documentation
- ✓ Spring Boot integration
- ✓ Production-ready
- ✓ Active community

**Cons:**
- ✗ Fewer plugins than Python
- ✗ Java verbosity
- ✗ Smaller ecosystem

**When to Use:** Enterprise Java teams, Spring Boot applications, migrating from Python LangChain

**Maturity:** ✓ Mature (active development)

---

### 2. **Spring AI** — Spring Boot Native
**Best for Enterprise Spring Ecosystems**

```java
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.openai.OpenAiChatModel;
import org.springframework.context.annotation.Bean;
import org.springframework.stereotype.Service;

@Service
public class LoanEvaluationService {
    private final ChatClient chatClient;
    
    public LoanEvaluationService(OpenAiChatModel model) {
        this.chatClient = ChatClient.create(model);
    }
    
    public String evaluateLoan(int credit, double income, double loan) {
        return chatClient.prompt()
            .user(u -> u.text("Evaluate loan: credit={0}, income={1}, amount={2}")
                .param(credit)
                .param(income)
                .param(loan))
            .call()
            .content();
    }
}
```

**Pros:**
- ✓ Spring Boot native
- ✓ Dependency injection
- ✓ Enterprise standard
- ✓ Great tooling
- ✓ Vector DB integration

**Cons:**
- ✗ Requires Spring Boot
- ✗ Less agent-focused
- ✗ Newer than LangChain4j

**When to Use:** Existing Spring Boot applications, enterprise architecture teams, microservices

**Maturity:** 🟡 Growing (1.0+ released)

---

### 3. **Quarkus + Langchain4j** — Lightweight Cloud-Native
**Best for Kubernetes/Cloud**

```java
// Quarkus application with LangChain4j
@ApplicationScoped
public class LoanAgent {
    
    @Inject
    ChatLanguageModel model;
    
    @Inject
    LoanTools tools;
    
    public String evaluate(int credit, double income, double loan) {
        return AiServices.builder(LoanEvaluator.class)
            .chatLanguageModel(model)
            .tools(tools)
            .build()
            .evaluate(credit, income, loan);
    }
}
```

**Pros:**
- ✓ Lightweight container (80MB vs 500MB+ Spring Boot)
- ✓ Fast startup (<1s vs 3-5s Spring)
- ✓ Cloud-native
- ✓ GraalVM compatible
- ✓ Lower memory footprint

**Cons:**
- ✗ Smaller ecosystem
- ✗ Less mature
- ✗ Steeper learning curve

**When to Use:** Cloud platforms, microservices, Kubernetes, serverless, cost-sensitive deployments

**Maturity:** 🟡 Emerging (growing adoption)

---

### 4. **JADE (Java Agent DEvelopment Framework)**
**Multi-Agent Specific Framework**

```java
import jade.core.Agent;
import jade.core.behaviours.CyclicBehaviour;
import jade.lang.acl.ACLMessage;

public class LoanOfficerAgent extends Agent {
    protected void setup() {
        addBehaviour(new CyclicBehaviour(this) {
            public void action() {
                ACLMessage msg = receive();
                if (msg != null) {
                    // Process loan application
                    ACLMessage reply = msg.createReply();
                    reply.setContent("APPROVED");
                    send(reply);
                } else {
                    block();
                }
            }
        });
    }
}
```

**Pros:**
- ✓ True multi-agent framework
- ✓ Agent-to-agent communication
- ✓ Established (20+ years)
- ✓ Great for swarms
- ✓ FIPA compliant

**Cons:**
- ✗ No LLM integration by default
- ✗ Legacy codebase
- ✗ Steep learning curve
- ✗ Not LLM-first

**When to Use:** Multi-agent simulations, swarms, agent communication research, legacy systems

**Maturity:** ✓ Mature but legacy

**Note:** Requires wrapping with LLM calls separately

---

### 5. **Custom Spring Boot + Anthropic SDK**
**Maximum Control + Java Standards**

```java
import com.anthropic.client.Anthropic;
import com.anthropic.models.*;

@RestController
public class LoanController {
    private final Anthropic client;
    
    public LoanController() {
        this.client = new Anthropic("sk-ant-...");
    }
    
    @PostMapping("/evaluate")
    public LoanDecision evaluate(@RequestBody LoanApplication app) {
        // Define tools
        List<Tool> tools = List.of(
            Tool.builder()
                .name("checkCredit")
                .description("Check credit score")
                .inputSchema(...)
                .build()
        );
        
        // Run agent loop manually
        MessageParam message = MessageParam.ofUserMessage(
            "Evaluate: " + app.toString()
        );
        
        List<MessageParam> messages = new ArrayList<>();
        messages.add(message);
        
        while (true) {
            Message response = client.messages().create(
                MessageCreateParams.builder()
                    .model("claude-3-5-sonnet-20241022")
                    .maxTokens(1024)
                    .tools(tools)
                    .messages(messages)
                    .build()
            );
            
            if (response.stopReason() == StopReason.END_TURN) {
                return parseLoanDecision(response);
            } else if (response.stopReason() == StopReason.TOOL_USE) {
                // Handle tool calls
                messages.add(MessageParam.ofAssistant(response));
                // ... process tool result
            }
        }
    }
}
```

**Pros:**
- ✓ Complete control
- ✓ Spring Boot standard
- ✓ No framework overhead
- ✓ Direct API access
- ✓ Testable

**Cons:**
- ✗ More boilerplate
- ✗ You manage everything
- ✗ Error handling needed

**When to Use:** Custom requirements, learning, specific optimizations, unique use cases

**Maturity:** ✓ Mature (direct SDK)

---

## Comparison Matrix: Java vs Python Frameworks

| Aspect | LangChain4j | Spring AI | Quarkus | JADE | Custom SDK |
|--------|---|---|---|---|---|
| **Best For** | General agents | Spring Boot | Cloud/K8s | Multi-agent | Custom |
| **LLM-First** | ✓ | ✓ | ✓ | ✗ | ✓ |
| **Ease** | ⭐⭐ | ⭐ | ⭐⭐ | ⭐ | ⭐⭐⭐ |
| **Enterprise** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Production** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Community** | Medium | Growing | Growing | Old | Large |
| **Startup Time** | ~2s | 3-5s | <1s | ~2s | ~2s |
| **Memory** | 300MB+ | 500MB+ | 100MB | 300MB+ | 300MB+ |
| **Vector DB Support** | ✓ | ✓ | ✓ | ✗ | Manual |
| **Observability** | ✓ | ✓ | ✓ | Basic | Manual |

---

## Java vs Python Comparison

### Performance
- **Java:** Compiled, JIT optimized, consistent
- **Python:** Interpreted, slower startup, but fine for LLM latency

### Ecosystem  
- **Python:** Richer AI/ML libraries
- **Java:** Better enterprise tooling, Spring Boot

### Deployment
- **Java:** Containerized (Docker), K8s native
- **Python:** FastAPI/Uvicorn, also cloud-ready

### Learning
- **Python:** Faster to learn agents
- **Java:** Steeper but stronger typing

---

## Recommendation: What Java Developers Should Use

### Scenario 1: "We're a Spring Boot Shop"
**Answer:** Spring AI + LangChain4j
```
Spring AI for core features
LangChain4j for advanced agents
```

### Scenario 2: "We need lightweight cloud deployment"  
**Answer:** Quarkus + LangChain4j
```
Ideal for Kubernetes
80MB containers
<1s startup
```

### Scenario 3: "We're building multi-agent systems"
**Answer:** JADE + LLM integration
```
Use JADE for agent framework
Call LLM SDK for each agent
```

### Scenario 4: "We need maximum control/performance"
**Answer:** Custom Spring Boot + Anthropic SDK
```
Write your own agent loop
Maximum optimization
```

### Scenario 5: "We want parity with Python"
**Answer:** LangChain4j
```
Closest to Python LangChain
Good documentation
Active community
```

---

## Migration Guide: Python → Java

If your team knows Python LangChain:

### Python LangChain
```python
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import tool

@tool
def check_credit(score: int) -> str:
    return "Good" if score >= 650 else "Poor"

agent = AgentExecutor.from_agent_and_tools(
    agent=create_tool_calling_agent(llm, tools),
    tools=[check_credit]
)
```

### Java Equivalent (LangChain4j)
```java
import dev.langchain4j.agent.tool.Tool;

class Tools {
    @Tool
    String checkCredit(int score) {
        return score >= 650 ? "Good" : "Poor";
    }
}

AiServices.builder(Agent.class)
    .chatLanguageModel(model)
    .tools(new Tools())
    .build()
```

**Migration effort:** Low (similar concepts)

---

## Cost Comparison: Java Frameworks

| Framework | Initial Setup | License | Support | Training |
|-----------|---|---|---|---|
| LangChain4j | ~2 hours | Open source | Community | Medium |
| Spring AI | ~1 hour | Open source | Community | Low |
| Quarkus | ~3 hours | Open source | Community | High |
| JADE | ~4 hours | Open source | Minimal | High |
| Custom SDK | Variable | N/A | N/A | High |

---

## Production Deployment in Java

### Docker with LangChain4j
```dockerfile
FROM gradle:8-jdk17 as build
WORKDIR /app
COPY . .
RUN gradle build

FROM openjdk:17-slim
COPY --from=build /app/build/libs/*.jar app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]
```

### Kubernetes with Quarkus
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
        image: myregistry/loan-agent:latest
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
```

---

## Final Recommendation

### For Most Java Teams: **LangChain4j**
- Most similar to Python LangChain
- Good documentation
- Active development
- Works with any Java framework

### For Spring Boot Teams: **Spring AI**
- Native integration
- Enterprise features
- Future-proof

### For Cloud-Native Teams: **Quarkus + LangChain4j**
- Lightweight containers
- Fast startup
- Kubernetes-optimized

### For Research/Multi-Agent: **JADE**
- True multi-agent framework
- Established standard
- Academic support

---

## Mixed Java/Python Teams

If you have both Java and Python developers:

**Recommended Architecture:**
```
Python:
- LangChain for prototyping
- DSPy for optimization
- Testing/research

Java:
- LangChain4j for production
- Spring Boot for APIs
- Deployment/operations

Shared:
- Claude API
- Same prompts
- Unified logging
```

**Unified Deployment:**
```
Python services → API
Java services → API
Orchestrate together
```

