# VISUAL DESIGN SYSTEM
## Production AI Bootcamp

---

## 🎨 COLOR PALETTE

### **Semantic Background Colors**

Each content type has a specific background color that signals its purpose to learners.

```
WHITE (#ffffff)
├─ Use for: Basic tutorials, how-to guides, code examples
├─ Signal: "This is practical, hands-on instruction"
├─ Text color: Dark Gray (#333333)
├─ Border: None
├─ Examples:
│  ├─ "How to set up Docker"
│  ├─ "Tool documentation"
│  ├─ "Step-by-step examples"
│  └─ "Code snippets"

LIGHT GRAY (#f5f5f5)
├─ Use for: Problem definitions, "why we need this"
├─ Signal: "This is conceptual, helps you understand the why"
├─ Text color: Dark Gray (#333333)
├─ Border left: 4px Gray (#999999)
├─ Examples:
│  ├─ "Why you need a verifier layer"
│  ├─ "How agents fail in production"
│  ├─ "Design pattern introduction"
│  └─ "Architecture discussion"
├─ Icon: 💡 (lightbulb concept)

LIGHT BLUE (#f0f4ff)
├─ Use for: CCA-F certification content
├─ Signal: "This is exam/certification relevant"
├─ Text color: Dark Blue (#0066cc)
├─ Border left: 4px Blue (#0066cc)
├─ Examples:
│  ├─ "Domain 1: Architecture (27%)"
│  ├─ "Key concepts for exam"
│  ├─ "Certification mapping"
│  └─ "Practice questions"
├─ Icon: 📋 (clipboard/exam)

LIGHT GREEN (#f0fff4)
├─ Use for: Working solutions, best practices
├─ Signal: "This is production-ready, recommended approach"
├─ Text color: Dark Green (#226b26)
├─ Border left: 4px Green (#28a745)
├─ Examples:
│  ├─ "Production checklist"
│  ├─ "Best practice implementation"
│  ├─ "Success case study"
│  └─ "Recommended architecture"
├─ Icon: ✅ (checkmark)

LIGHT RED (#f8d7da)
├─ Use for: Problems, warnings, what NOT to do
├─ Signal: "Watch out, this is a trap or common mistake"
├─ Text color: Dark Red (#721c24)
├─ Border left: 4px Red (#dc3545)
├─ Examples:
│  ├─ "Common pitfalls"
│  ├─ "What went wrong"
│  ├─ "Debugging this error"
│  └─ "Don't do this"
├─ Icon: ⚠️ (warning)

LIGHT YELLOW (#fff3cd)
├─ Use for: Tips, important notes
├─ Signal: "Pay attention, this is important context"
├─ Text color: Dark Gray (#856404)
├─ Border left: 4px Yellow (#ffc107)
├─ Examples:
│  ├─ "Pro tip:"
│  ├─ "Important note:"
│  ├─ "Watch out:"
│  └─ "Remember:"
├─ Icon: 🔔 (bell/notification)
```

### **Text Colors**

```
Headlines:
├─ h1: Dark Gray (#333333), 36px, Bold
├─ h2: Dark Gray (#333333), 28px, Bold
├─ h3: Dark Gray (#333333), 22px, Bold
└─ h4: Dark Gray (#333333), 18px, Semi-bold

Body Text:
├─ Primary: Dark Gray (#333333), 16px
├─ Secondary: Medium Gray (#666666), 14px
└─ Subtle: Light Gray (#999999), 13px

Links:
├─ Normal: Blue (#0066cc), underlined
├─ Hover: Dark Blue (#004a99), underlined
└─ Visited: Purple (#663399)

Code:
├─ Text: Black (#000000)
├─ Background: Light Gray (#f5f5f5)
├─ Border: Light Gray (#e0e0e0)
└─ Syntax: Standard highlights (red for strings, blue for keywords)

Accent Colors:
├─ Blue (#667eea) - for emphasis
├─ Green (#48c774) - for success
└─ Orange (#ff9800) - for warning
```

---

## 📐 TYPOGRAPHY

### **Font Stack**

```css
/* Headlines */
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;

/* Body */
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;

/* Code */
font-family: "Courier New", Courier, Monaco, "Andale Mono", monospace;
```

### **Font Sizes**

```
h1: 36px, line-height 1.3, bold, letter-spacing -0.01em
h2: 28px, line-height 1.4, bold, letter-spacing -0.005em
h3: 22px, line-height 1.4, semi-bold
h4: 18px, line-height 1.5, semi-bold
p:  16px, line-height 1.8, regular
small: 14px, line-height 1.6, regular
code: 12px, line-height 1.5, monospace

Bold text: 600 weight
Regular text: 400 weight
Light text: 300 weight
```

### **Spacing**

```
Margins:
├─ Between sections: 48px (large)
├─ Between subsections: 32px (medium)
├─ Between paragraphs: 16px (small)
└─ Between inline: 8px (tiny)

Padding:
├─ Card/box padding: 20px all
├─ List item padding: 12px vertical
└─ Code block padding: 16px all
```

---

## 🧩 COMPONENT LIBRARY

### **1. Concept Box (GRAY)**

```html
<div class="concept-box">
  <div class="concept-header">💡 Why We Need This</div>
  <div class="concept-body">
    <p>Explanation of the problem and why this concept matters</p>
    <p>Usually includes a scenario or pain point</p>
  </div>
</div>
```

**Styling:**
```css
.concept-box {
  background-color: #f5f5f5;
  border-left: 4px solid #999999;
  padding: 20px;
  margin: 32px 0;
  border-radius: 4px;
}

.concept-header {
  font-size: 16px;
  font-weight: 600;
  color: #333333;
  margin-bottom: 12px;
}

.concept-body {
  font-size: 14px;
  color: #333333;
  line-height: 1.8;
}
```

### **2. Success/Best Practice Box (GREEN)**

```html
<div class="success-box">
  <div class="success-header">✅ Production Solution</div>
  <div class="success-body">
    <p>This is the recommended approach for production</p>
    <p>Here's why it's better than alternatives</p>
  </div>
</div>
```

**Styling:**
```css
.success-box {
  background-color: #f0fff4;
  border-left: 4px solid #28a745;
  padding: 20px;
  margin: 32px 0;
  border-radius: 4px;
}

.success-header {
  font-size: 16px;
  font-weight: 600;
  color: #226b26;
  margin-bottom: 12px;
}

.success-body {
  font-size: 14px;
  color: #226b26;
  line-height: 1.8;
}
```

### **3. Warning Box (RED)**

```html
<div class="warning-box">
  <div class="warning-header">⚠️ Common Pitfall</div>
  <div class="warning-body">
    <p>Many people make this mistake</p>
    <p>Here's what happens and how to avoid it</p>
  </div>
</div>
```

**Styling:**
```css
.warning-box {
  background-color: #f8d7da;
  border-left: 4px solid #dc3545;
  padding: 20px;
  margin: 32px 0;
  border-radius: 4px;
}

.warning-header {
  font-size: 16px;
  font-weight: 600;
  color: #721c24;
  margin-bottom: 12px;
}

.warning-body {
  font-size: 14px;
  color: #721c24;
  line-height: 1.8;
}
```

### **4. Note Box (YELLOW)**

```html
<div class="note-box">
  <div class="note-header">🔔 Important Note</div>
  <div class="note-body">
    <p>Pay special attention to this detail</p>
  </div>
</div>
```

**Styling:**
```css
.note-box {
  background-color: #fff3cd;
  border-left: 4px solid #ffc107;
  padding: 20px;
  margin: 32px 0;
  border-radius: 4px;
}

.note-header {
  font-size: 16px;
  font-weight: 600;
  color: #856404;
  margin-bottom: 12px;
}

.note-body {
  font-size: 14px;
  color: #856404;
  line-height: 1.8;
}
```

### **5. Certification Box (BLUE)**

```html
<div class="cert-box">
  <div class="cert-header">📋 CCA-F Domain 3: Prompting</div>
  <div class="cert-body">
    <p>This content maps to certification exam domain 3</p>
    <p><strong>Coverage:</strong> 20% of exam</p>
  </div>
</div>
```

**Styling:**
```css
.cert-box {
  background-color: #f0f4ff;
  border-left: 4px solid #0066cc;
  padding: 20px;
  margin: 32px 0;
  border-radius: 4px;
}

.cert-header {
  font-size: 16px;
  font-weight: 600;
  color: #0066cc;
  margin-bottom: 12px;
}

.cert-body {
  font-size: 14px;
  color: #0066cc;
  line-height: 1.8;
}
```

### **6. Code Block**

```html
<div class="code-block">
  <div class="code-header">
    <span class="language">python</span>
    <button class="copy-btn">Copy</button>
  </div>
  <pre><code class="language-python">
# Your code here
def evaluate_loan(application):
    pass
  </code></pre>
</div>
```

**Styling:**
```css
.code-block {
  background-color: #f5f5f5;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  margin: 20px 0;
  overflow: hidden;
}

.code-header {
  background-color: #e0e0e0;
  padding: 12px 16px;
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  font-weight: 600;
}

.code-header .language {
  color: #333333;
}

.code-header .copy-btn {
  background-color: #667eea;
  color: white;
  border: none;
  padding: 4px 12px;
  border-radius: 3px;
  cursor: pointer;
  font-size: 12px;
}

pre {
  padding: 16px;
  overflow-x: auto;
  margin: 0;
}

code {
  font-family: "Courier New", Monaco;
  font-size: 12px;
  line-height: 1.5;
  color: #000000;
}
```

### **7. Comparison Table**

```html
<table class="comparison-table">
  <tr>
    <th>Aspect</th>
    <th>Approach A</th>
    <th>Approach B</th>
  </tr>
  <tr>
    <td>Speed</td>
    <td class="positive">Fast</td>
    <td class="negative">Slow</td>
  </tr>
  <tr>
    <td>Cost</td>
    <td class="negative">$100/mo</td>
    <td class="positive">$20/mo</td>
  </tr>
</table>
```

**Styling:**
```css
.comparison-table {
  width: 100%;
  border-collapse: collapse;
  margin: 24px 0;
}

.comparison-table th {
  background-color: #e8e8e8;
  padding: 12px;
  text-align: left;
  font-weight: 600;
  border-bottom: 2px solid #999999;
}

.comparison-table td {
  padding: 12px;
  border-bottom: 1px solid #e0e0e0;
}

.comparison-table tr:nth-child(even) {
  background-color: #fafafa;
}

.comparison-table td.positive {
  background-color: #f0fff4;
  color: #226b26;
  font-weight: 600;
}

.comparison-table td.negative {
  background-color: #f8d7da;
  color: #721c24;
  font-weight: 600;
}
```

### **8. Learning Path Timeline**

```html
<div class="timeline">
  <div class="timeline-item completed">
    <div class="timeline-marker"></div>
    <div class="timeline-content">
      <h4>Week 1: Foundations</h4>
      <p>Understand 5 engineering disciplines</p>
    </div>
  </div>
  <div class="timeline-item current">
    <div class="timeline-marker"></div>
    <div class="timeline-content">
      <h4>Week 2: Evolution Story</h4>
      <p>See why each layer exists</p>
    </div>
  </div>
  <div class="timeline-item future">
    <div class="timeline-marker"></div>
    <div class="timeline-content">
      <h4>Week 3: Loan Application</h4>
      <p>Build real use case</p>
    </div>
  </div>
</div>
```

**Styling:**
```css
.timeline {
  position: relative;
  padding: 20px 0;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 15px;
  top: 0;
  bottom: 0;
  width: 2px;
  background-color: #e0e0e0;
}

.timeline-item {
  margin-bottom: 40px;
  position: relative;
  padding-left: 50px;
}

.timeline-marker {
  position: absolute;
  left: 0;
  top: 0;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: #e0e0e0;
  border: 3px solid white;
}

.timeline-item.completed .timeline-marker {
  background-color: #28a745;
}

.timeline-item.current .timeline-marker {
  background-color: #0066cc;
}

.timeline-item.future .timeline-marker {
  background-color: #999999;
}

.timeline-content h4 {
  margin-top: 0;
  margin-bottom: 8px;
}

.timeline-content p {
  margin: 0;
  color: #666666;
}
```

---

## 📄 PAGE LAYOUTS

### **Learning Module Page**

```
┌─────────────────────────────────────────┐
│ BREADCRUMB: Foundations > Harness...   │
├─────────────────────────────────────────┤
│ H1: Topic Title                         │
│ Estimated time: 15 minutes              │
├─────────────────────────────────────────┤
│ [GRAY BOX]                              │
│ Why we need this                        │
│ (Problem setup)                         │
├─────────────────────────────────────────┤
│ [WHITE BG]                              │
│ Learning content                        │
│ - Explanation                           │
│ - Concepts                              │
│ - Diagrams                              │
├─────────────────────────────────────────┤
│ [CODE BLOCK]                            │
│ Example code                            │
├─────────────────────────────────────────┤
│ [GREEN BOX]                             │
│ Best practice / Key takeaway            │
├─────────────────────────────────────────┤
│ NAVIGATION                              │
│ ← Previous | Next →                     │
├─────────────────────────────────────────┤
│ PROGRESS: Week 1 of 16 (6%)             │
└─────────────────────────────────────────┘
```

### **Problem/Solution Pattern**

```
┌──────────────────────────────────┐
│ THE PROBLEM (RED BOX)            │
├──────────────────────────────────┤
│ ❌ What doesn't work             │
│ • Broken code example            │
│ • Why it fails                   │
│ • What error you get             │
├──────────────────────────────────┤
│ THE ROOT CAUSE (GRAY BOX)        │
├──────────────────────────────────┤
│ 💡 Why this breaks               │
│ Explanation of root cause        │
├──────────────────────────────────┤
│ THE SOLUTION (GREEN BOX)         │
├──────────────────────────────────┤
│ ✅ What works                    │
│ • Fixed code example             │
│ • Why this is better             │
│ • How to test it                 │
├──────────────────────────────────┤
│ WHAT THIS TEACHES YOU            │
│ Key learnings from this pattern  │
└──────────────────────────────────┘
```

### **Comparison/Decision Page**

```
┌────────────────────────────────────────┐
│ H2: Choose Between Option A & B        │
├────────────────────────────────────────┤
│ [COMPARISON TABLE]                     │
│ Shows tradeoffs side-by-side           │
├────────────────────────────────────────┤
│ [GREEN BOX]                            │
│ When to use Option A                   │
│ - Use case 1                           │
│ - Use case 2                           │
│ - Best for: High performance needs     │
├────────────────────────────────────────┤
│ [GREEN BOX]                            │
│ When to use Option B                   │
│ - Use case 1                           │
│ - Use case 2                           │
│ - Best for: Rapid development          │
├────────────────────────────────────────┤
│ [BLUE BOX - CERTIFICATION]             │
│ Exam tip: Questions about this         │
└────────────────────────────────────────┘
```

---

## 🚫 DESIGN ANTI-PATTERNS (Never Do These)

```
❌ Dark backgrounds
   (Poor accessibility, hard on eyes)

❌ Light text on light backgrounds
   (Impossible to read)

❌ Monospace fonts for body text
   (Feels like terminal, hard to read)

❌ Neon colors
   (Looks unprofessional, hard on eyes)

❌ Inconsistent spacing
   (Looks unprofessional)

❌ Too many different fonts
   (Confusing hierarchy)

❌ Justified text in body
   (Creates weird spacing)

❌ More than 3 colors in one section
   (Visual noise)

❌ Auto-playing audio/video
   (Annoying, unprofessional)

❌ Hover-only important information
   (Mobile users can't access)
```

---

## 🎬 Interactive Components

### **Code Playgrounds** (Embedded)
- Click to run code
- See output in real-time
- Modify and experiment
- Save your version

### **Quizzes** (End of section)
- 3-5 questions per section
- Immediate feedback
- Explanation for correct/incorrect
- Track progress

### **Diagrams** (Interactive)
- Hover to highlight
- Click to zoom
- Click paths to trace flow
- Desktop + mobile optimized

### **Tabs** (For comparisons)
- Framework comparisons
- Before/after code
- Different approaches

---

## 📱 RESPONSIVE DESIGN

```
Desktop (>1024px):
├─ Sidebar navigation (20%)
├─ Main content (60%)
└─ Right sidebar resources (20%)

Tablet (768px-1024px):
├─ Sidebar collapses to hamburger
├─ Main content (80%)
└─ Right sidebar moves below

Mobile (<768px):
├─ Full width content
├─ Navigation in header/footer
├─ Stacked boxes
└─ Touch-friendly buttons (48px min)
```

---

## ✨ VISUAL HIERARCHY QUICK START

**Use this order to create consistent pages:**

1. **Hero Section** (Big image + title)
2. **Problem/Concept** (GRAY box - why this matters)
3. **Content** (WHITE bg - explanation)
4. **Example** (Code block - show it works)
5. **Best Practice** (GREEN box - recommended way)
6. **Warning** (RED box - what to avoid)
7. **Key Takeaway** (Summary)
8. **Next Steps** (What to do now)

---

**Status:** Visual design system complete and ready for implementation
