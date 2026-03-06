# Hybrid Mode: Local LLM + Claude

Run routine tasks on your local model, fall back to Claude for complex work.

## Why Hybrid?

**Local Llama (your model):**
- ✅ Fast (instant)
- ✅ Private (no API)
- ✅ Cheap (free)
- ❌ Limited to your context
- ❌ Sometimes generic

**Claude:**
- ✅ Powerful reasoning
- ✅ Code generation
- ✅ Creative writing
- ✅ Complex analysis
- ❌ Expensive ($)
- ❌ API calls

**Hybrid = Best of both:**
- Routine tasks → Local (fast + cheap)
- Complex tasks → Claude (powerful)
- Fallback when local fails

## Architecture

```
User Request
    ↓
Local Llama generates response
    ↓
Evaluate confidence/complexity
    ├─ High confidence + simple → Return local response
    └─ Low confidence + complex → Send to Claude API
    ↓
Cache response locally for future use
```

## Implementation

### Python + OpenAI API

```python
import anthropic
from ollama import Client

local_client = Client(host="localhost:11434")
claude = anthropic.Anthropic()

def answer(question: str) -> str:
    # Try local model first
    local_response = local_client.generate(
        model="my-context",
        prompt=question,
        stream=False
    )
    
    # Is answer good enough?
    confidence = evaluate_confidence(local_response)
    
    if confidence < 0.7 or is_complex(question):
        # Fall back to Claude for better answer
        claude_response = claude.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            messages=[{"role": "user", "content": question}]
        )
        return claude_response.content[0].text
    
    return local_response

def evaluate_confidence(response: str) -> float:
    """Simple confidence scoring"""
    # Check for hedging language
    unsure_phrases = ["i'm not sure", "i don't know", "unclear"]
    if any(phrase in response.lower() for phrase in unsure_phrases):
        return 0.3
    
    # Check length (too short = low confidence)
    if len(response) < 50:
        return 0.4
    
    return 0.8

def is_complex(question: str) -> bool:
    """Detect complex questions"""
    complex_keywords = [
        "refactor", "optimize", "design", "architecture",
        "algorithm", "explain", "analyze"
    ]
    return any(keyword in question.lower() for keyword in complex_keywords)
```

### JavaScript / Node.js

```javascript
const Anthropic = require("@anthropic-ai/sdk");

const client = new Anthropic();

async function answerQuestion(question) {
  try {
    // Try local model first
    const localResponse = await fetch("http://localhost:11434/api/generate", {
      method: "POST",
      body: JSON.stringify({
        model: "my-context",
        prompt: question,
        stream: false
      })
    }).then(r => r.json());
    
    const confidence = evaluateConfidence(localResponse.response);
    
    if (confidence < 0.7 || isComplex(question)) {
      // Fall back to Claude
      const message = await client.messages.create({
        model: "claude-opus-4-6",
        max_tokens: 1024,
        messages: [{ role: "user", content: question }]
      });
      
      return message.content[0].text;
    }
    
    return localResponse.response;
  } catch (error) {
    console.error("Error:", error);
    // Always fall back to Claude if local fails
    const message = await client.messages.create({
      model: "claude-opus-4-6",
      max_tokens: 1024,
      messages: [{ role: "user", content: question }]
    });
    return message.content[0].text;
  }
}

function evaluateConfidence(response) {
  const unsurePhrases = ["not sure", "don't know", "unclear"];
  if (unsurePhrases.some(p => response.toLowerCase().includes(p))) {
    return 0.3;
  }
  if (response.length < 50) return 0.4;
  return 0.8;
}

function isComplex(question) {
  const keywords = ["code", "refactor", "design", "algorithm"];
  return keywords.some(k => question.toLowerCase().includes(k));
}
```

## Cost Analysis

**1000 requests/month:**

| Approach | Cost | Speed |
|----------|------|-------|
| Claude only | ~$15-30 | ✅ Fast |
| Hybrid | ~$3-5 | ✅✅ Faster |
| Local only | $0 | ❌ Sometimes slow |

Hybrid is **best ROI**: 80-90% requests local (free), 10-20% Claude (when needed).

## Configuration

### Confidence Threshold
```python
# Stricter (more Claude calls, better quality)
CONFIDENCE_THRESHOLD = 0.8

# More trusting (fewer Claude calls, cheaper)
CONFIDENCE_THRESHOLD = 0.6
```

### Fallback Strategy
```python
# Always use best tool
if is_code_task(question):
    use_claude()
elif is_personal_context(question):
    use_local()
else:
    use_hybrid()
```

## Monitoring

Track which model answers what:

```python
import json
from datetime import datetime

def log_request(question, model_used, confidence):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "model": model_used,
        "confidence": confidence
    }
    
    with open("requests.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
```

**Analyze monthly:**
```bash
grep '"model": "claude"' requests.jsonl | wc -l  # Count Claude calls
# If > 30%, consider improving local model
```

## Production Setup

### Docker Compose

```yaml
version: '3'
services:
  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
  
  api:
    build: .
    ports:
      - "3000:3000"
    depends_on:
      - ollama
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OLLAMA_HOST=http://ollama:11434

volumes:
  ollama_data:
```

### Environment Variables
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export OLLAMA_HOST="http://localhost:11434"
export CONFIDENCE_THRESHOLD="0.7"
```

## Best Practices

1. **Start with local:** Try local first, fall back only when needed
2. **Monitor confidence:** Track which queries go to Claude
3. **Improve dataset:** If same query fails locally repeatedly, add to dataset
4. **Cache responses:** Remember answers to avoid repeated API calls
5. **Set budgets:** Limit Claude spending (e.g., $5/month max)

## Troubleshooting

**"Local model always used, never improves"**
→ Increase CONFIDENCE_THRESHOLD or add more training data

**"Claude called too much"**
→ Decrease CONFIDENCE_THRESHOLD or improve local dataset

**"Local response is generic"**
→ Your dataset lacks specific examples. Add more context.

**"Ollama not running"**
→ `ollama serve` in another terminal, or check Docker

## Next Steps

1. Set up Ollama locally
2. Train your model
3. Implement hybrid logic above
4. Monitor for 2 weeks
5. Tune thresholds based on usage

**Happy hybriding!** 🚀
