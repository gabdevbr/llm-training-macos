# LLM Training on macOS

**Fine-tune Llama 3.1 locally on your Mac with your own context using LoRA.**

Transform a generic AI assistant into an expert on *your* knowledge domain—whether that's personal life, company processes, or specialized domains.

```bash
# 1. Clone
git clone https://github.com/gab-dev/llm-training-macos.git
cd llm-training-macos

# 2. Setup (automatically installs everything)
./setup.sh

# 3. Add your context (JSONL, CSV, or Markdown)
# Edit my-context/dataset.jsonl with your data

# 4. Train (3-4 hours on M-series Mac)
python3 train.py --context-dir my-context

# 5. Run locally
ollama run my-context
```

**That's it.** Your AI now knows *you*.

---

## Why This?

**Generic LLMs:**
- Know everything about everything
- Know nothing about *you*
- Same response for everyone
- Expensive API calls

**Your Fine-tuned Model:**
- ✅ Knows your context, values, patterns
- ✅ Runs locally (private, fast, cheap)
- ✅ Improves monthly with your data
- ✅ Can fallback to Claude for heavy lifting
- ✅ Hybrid: local for routine tasks, Claude for complex ones

**Real example:** Skynet (AI assistant for Gab)
- Knows his family situation, health, finances, company
- Answers "What's your mom's status?" instantly with full context
- Handles routine tasks locally
- Calls Claude when code refactoring is needed

---

## What You Get

### ⚡ Fast Training
- **M1/M2 Max:** 3-4 hours (8B model), 6-8 hours (13B model)
- **M4 Pro:** 1.5-2 hours (8B), 3-4 hours (13B)
- M-series Metal optimization = no CUDA needed

### 🔒 Privacy
- Model runs locally (no API calls for routine tasks)
- Your data stays on your machine
- Optional: hybrid mode (local + Claude fallback)

### 📈 Continuous Learning
- Add new context monthly
- Re-train in 1 hour
- Model improves over time

### 🎯 Templates Included
5 ready-to-use examples:
1. **Personal Assistant** ← Start here (Skynet example)
2. **Company Knowledge Base** (internal docs)
3. **Support Agent** (customer FAQs)
4. **Research Assistant** (papers + notes)
5. **Developer AI** (code patterns)

---

## Requirements

- **Mac:** M1/M2/M3/M4 (Apple Silicon)
- **RAM:** 16GB minimum (24GB recommended)
- **Disk:** 20GB free (for models + training data)
- **Python:** 3.10+ (installed via Homebrew)
- **Ollama:** For running the model locally

---

## Quick Start (5 min)

### 1. Install Requirements
```bash
./setup.sh
```

This installs:
- Python 3.11
- Ollama
- unsloth (40x faster fine-tuning)
- transformers, datasets, torch

### 2. Choose Your Template
```bash
# Option A: Start with Skynet (personal assistant)
cp -r templates/personal-assistant my-context

# Option B: Start with company KB
cp -r templates/company-kb my-context

# Option C: Start from scratch
mkdir my-context
# Then create: my-context/dataset.jsonl (see format below)
```

### 3. Add Your Data
Edit `my-context/dataset.jsonl`:
```json
{"instruction": "Who is your owner?", "response": "I'm Gabriel's AI assistant..."}
{"instruction": "What's your company?", "response": "Geovendas, a SaaS platform..."}
```

(See `docs/DATASET_FORMAT.md` for full spec)

### 4. Train
```bash
python3 train.py \
  --context-dir my-context \
  --model-size 13b \
  --epochs 3
```

Grab a coffee. This takes 3-4 hours.

### 5. Test Locally
```bash
ollama run my-context
```

```
>>> What's my company's structure?
# Your model responds with real context
```

---

## Dataset Format

### JSONL (JavaScript Object Notation Lines)
Simplest format. One JSON object per line:

```json
{"instruction": "How many employees?", "response": "We have 12 people across 4 teams..."}
{"instruction": "What's the revenue?", "response": "2M ARR, growing 20% MoM..."}
```

**Why JSONL?**
- Easy to generate programmatically
- Scales to 100k+ examples
- Standard in ML (HuggingFace, LangChain, etc)

### CSV
If you have a spreadsheet:

```csv
instruction,response
"How old are you?","I'm 35 years old"
"What's your job?","I'm a CEO at Geovendas"
```

Script included: `scripts/csv-to-jsonl.py`

### Markdown
Extract from your documentation:

```markdown
## Company FAQ

### How big is the team?
We have 12 people across 4 teams...

### What's the revenue?
2M ARR, growing 20% MoM...
```

Script: `scripts/markdown-to-jsonl.py`

---

## Templates Overview

### 1. Personal Assistant (Recommended first)
```
templates/personal-assistant/
├── dataset.jsonl        (100+ examples about YOU)
├── README.md           (how to customize)
└── example-topics.txt  (what to include)
```
Perfect for: Family, health, finances, preferences, decisions.
**Your use case.** Start here.

### 2. Company Knowledge Base
```
templates/company-kb/
├── dataset.jsonl       (org structure, processes, history)
└── example-structure.txt
```
Perfect for: Internal wiki, org chart, team docs.

### 3. Support Agent
```
templates/support-agent/
├── dataset.jsonl       (FAQs, common issues)
└── example-issues.txt
```
Perfect for: Customer support, helpdesk.

### 4. Research Assistant
```
templates/research-assistant/
├── dataset.jsonl       (papers, notes, findings)
└── example-topics.txt
```
Perfect for: Academic, research, deep dives.

### 5. Developer AI
```
templates/developer-ai/
├── dataset.jsonl       (code patterns, architecture)
└── example-code.txt
```
Perfect for: Codebases, architecture patterns, dev decisions.

---

## Hybrid Mode: Local + Claude

Run routine tasks locally, fall back to Claude for complex work:

```python
# In your OpenClaw integration
response = await llama_local.generate(prompt)
if confidence(response) < 0.7 or "complex" in prompt:
    response = await claude.generate(prompt)
```

See `docs/HYBRID_CLAUDE.md` for full integration.

---

## Performance by Hardware

| Mac | Model | Train Time | Inference |
|-----|-------|-----------|-----------|
| M1 Pro 16GB | 8B | 8h | 5 tok/s |
| M2 Max 24GB | 8B | 4h | 8 tok/s |
| M2 Max 24GB | 13B | 8h | 4 tok/s |
| M4 Pro 24GB | 8B | 2h | 12 tok/s |
| **M4 Pro 24GB** | **13B** | **3-4h** | **7 tok/s** |
| M4 Max 36GB | 70B | 6h | 15 tok/s |

---

## Training Parameters

```bash
python3 train.py \
  --context-dir my-context        # Your data directory
  --model-size 13b                # 8b, 13b, or 70b
  --epochs 3                      # How many times through data
  --batch-size 4                  # Examples per iteration
  --learning-rate 0.0002          # LoRA learning rate
  --max-seq-length 2048           # Max tokens per example
```

**Recommendations:**
- First time? Use `13b` (best quality vs speed tradeoff)
- Limited RAM? Use `8b`
- Want best result? Use `70b` (takes 10-12h)
- Monthly updates? Use `--epochs 1` (1 hour retraining)

---

## Deployment

### Local (Ollama)
```bash
ollama run my-context
```

### Server (OpenClaw)
```bash
rsync -avz ./models/my-context/ user@server:~/.ollama/models/
ollama serve  # On server
```

### Docker
```bash
docker run -d -p 11434:11434 ollama/ollama
# Then push your model
```

See `docs/DEPLOYMENT.md` for full guide.

---

## What Your Dataset Should Include

**Personal Assistant (Skynet example):**
- ✅ Family relationships + key info
- ✅ Health status, medications
- ✅ Financial situation, income
- ✅ Work/company info
- ✅ Preferences, values, decisions
- ✅ Projects, goals, context

**Company KB:**
- ✅ Org structure, team members
- ✅ Processes, how things work
- ✅ History, major decisions
- ✅ Financial metrics
- ✅ Technical architecture
- ✅ Company values, culture

**Size:** 100-500 examples for good results. 1000+ for excellent.

---

## Continuous Learning

### Monthly Retraining
```bash
# 1. Add new context lines to dataset.jsonl
echo '{"instruction": "...", "response": "..."}' >> my-context/dataset.jsonl

# 2. Retrain (1 epoch = 1 hour)
python3 train.py --context-dir my-context --epochs 1

# 3. Deploy
ollama run my-context
```

### Version Control
```bash
git add my-context/dataset.jsonl
git commit -m "Monthly update: March 2026"
git push
```

Your model improves every month.

---

## Troubleshooting

**"Out of memory"**
```bash
python3 train.py --batch-size 2  # Reduce batch size
# or
python3 train.py --model-size 8b  # Use smaller model
```

**"Training very slow"**
```bash
python3 train.py --model-size 8b  # 8B is faster than 13B
```

**"Model responses are generic"**
- Dataset too small? Add 100+ examples
- Learning rate too high? Try `--learning-rate 0.0001`
- Epochs too low? Try `--epochs 5`

See `docs/TROUBLESHOOTING.md` for more.

---

## Examples in the Wild

- **Skynet** (Personal AI): Knows Gab's family, health, finances, company
- **Company AI**: Knows internal org structure, processes, decisions
- **Support Bot**: Knows all FAQs, can answer 80% of tickets

---

## Contributing

Found a bug? Want to add a template? PRs welcome!

See `CONTRIBUTING.md` for guidelines.

---

## License

MIT — Use, modify, distribute freely.

---

## Next Steps

1. **Clone** this repo
2. **Run** `./setup.sh`
3. **Pick a template** or create your own
4. **Add your context** to `dataset.jsonl`
5. **Train** with `python3 train.py`
6. **Deploy** with Ollama

**Questions?** See `docs/` folder.

---

## Made by [Gab](https://gab.dev.br)

This started as a personal project (Skynet AI assistant) and grew into a framework. 

If you build something cool with this, let me know! 🚀

---

**Happy training!**
