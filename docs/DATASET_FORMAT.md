# Dataset Format Guide

Your dataset is the foundation of your fine-tuned model. Better data = better model.

## JSONL Format (Recommended)

**One JSON object per line:**

```json
{"instruction": "What's your name?", "response": "I'm an AI assistant trained on your context."}
{"instruction": "Who do you work for?", "response": "I work for Acme Corp, a SaaS company."}
```

**Why JSONL?**
- ✅ Easy to append new data
- ✅ Standard in ML (HuggingFace, LangChain)
- ✅ One error doesn't break file
- ✅ Efficient parsing

### Generate JSONL Programmatically

```python
import json

data = [
    {"instruction": "Q1", "response": "A1"},
    {"instruction": "Q2", "response": "A2"},
]

with open("dataset.jsonl", "w") as f:
    for item in data:
        f.write(json.dumps(item) + "\n")
```

## CSV Format

If you have a spreadsheet:

```csv
instruction,response
"How do I sign up?","Go to example.com and click Sign Up"
"What's your pricing?","We have 3 plans: Basic ($10), Pro ($50), Enterprise (custom)"
```

**Convert to JSONL:**
```bash
python3 scripts/csv-to-jsonl.py input.csv output.jsonl
```

## Markdown Format

Extract from your documentation:

```markdown
## FAQ

### How do I reset my password?

Go to Settings > Account > Reset Password. You'll receive an email within 5 minutes.

### What payment methods do you accept?

Credit cards, PayPal, and bank transfers.
```

**Convert to JSONL:**
```bash
python3 scripts/markdown-to-jsonl.py input.md output.jsonl
```

## What Makes Good Training Data

### ✅ DO:
- **Be specific:** "The company has 15 people" vs "we're medium-sized"
- **Include context:** "We use Python (backend) and React (frontend)"
- **Document decisions:** "We chose Postgres because..."
- **Cover diverse topics:** Mix different question types
- **Real examples:** Use actual conversations, emails, docs

### ❌ DON'T:
- Generic facts everyone knows
- Repeated information (wastes tokens)
- Sensitive data (passwords, API keys)
- Outdated information (will confuse model)
- Incomplete answers

## Example: Personal Assistant

```json
{"instruction": "Tell me about your family", "response": "I have a wife (Sarah) and 2 kids (7 and 10 years old). My parents live nearby. My brother works in tech in SF."}
{"instruction": "What's your health situation?", "response": "I take Metformin for Type 2 diabetes and Lexapro for anxiety. I exercise 3x/week and try to eat whole foods."}
{"instruction": "What are your main projects?", "response": "1. SideProject (SaaS, 2M ARR), 2. OpenSource (machine learning tools), 3. Writing (publish weekly)."}
{"instruction": "How do you make decisions?", "response": "I prioritize: impact on family, financial sustainability, learning opportunities. I prefer data-driven decisions but value gut feel too."}
```

## Example: Company KB

```json
{"instruction": "What's our org structure?", "response": "We have 3 departments: Engineering (8 people, led by Alice), Sales (4 people, led by Bob), Operations (2 people, led by Carol)."}
{"instruction": "What's our tech stack?", "response": "Backend: Python + FastAPI. Frontend: React + TypeScript. Database: PostgreSQL. Hosting: AWS. Monitoring: DataDog."}
{"instruction": "What's our product roadmap?", "response": "Q1: Mobile app beta. Q2: API redesign. Q3: Enterprise features. Q4: IPO planning."}
```

## Data Size

| Dataset Size | Quality | Training Time | Model Quality |
|---|---|---|---|
| 10-50 examples | Poor | Fast | Weak |
| 50-100 examples | Fair | 1h | Fair |
| **100-300 examples** | **Good** | **2-4h** | **Good** ← Start here |
| 300-1000 examples | Excellent | 4-8h | Excellent |
| 1000+ examples | Expert | 8h+ | Expert |

**Recommendation:** Start with 100-300 examples, then add 50-100 per month.

## Quality Checklist

- [ ] Each question is specific (not vague)
- [ ] Each answer is complete (not cut off)
- [ ] No duplicate questions
- [ ] No sensitive data (passwords, emails, PII)
- [ ] Covers all major topics you care about
- [ ] Grammar/spelling checked
- [ ] Consistent formatting
- [ ] At least 100 examples

## Tools

### CSV to JSONL
```bash
python3 scripts/csv-to-jsonl.py input.csv output.jsonl
```

### Markdown to JSONL
```bash
python3 scripts/markdown-to-jsonl.py input.md output.jsonl
```

### Validate Dataset
```bash
python3 scripts/validate-dataset.py dataset.jsonl
```

## Next Steps

Once you have your dataset:

```bash
python3 train.py --context-dir my-context
```

Good luck! 🚀
