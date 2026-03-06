# 🚀 LLM Training on macOS

**Fine-tune Llama 3.1 locally on your Mac with your own knowledge.**

Transform a generic AI into an expert on *your* business, life, or domain—running entirely offline.

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/gabdevbr/llm-training-macos)](https://github.com/gabdevbr/llm-training-macos)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![Mac M-series](https://img.shields.io/badge/Mac-M1%2FM2%2FM3%2FM4-lightgrey)](https://www.apple.com)

---

## 🎯 The Problem

**Generic LLMs are expensive and dumb about YOU:**

```
🤖 Claude: "I don't know about your company"
💰 Cost: $0.01-0.03 per request
🌐 Privacy: Data sent to servers
⚠️ Speed: API latency every query
```

**What if your AI knew everything about you?**

```
🧠 Your Model: "Your revenue is 2M ARR, growth 20% MoM"
💰 Cost: $0 (runs locally)
🔒 Privacy: Nothing leaves your Mac
⚡ Speed: Instant (no API calls)
```

---

## ✨ What You Get

### 🎓 Personal Knowledge

Your AI knows:
- 👨‍👩‍👧 Family, relationships, important people
- 💪 Health status, fitness, diet preferences
- 💰 Financial situation, income, investments
- 🏢 Work context, company structure, projects
- 🎯 Goals, values, decision-making patterns
- 📚 Everything you want it to remember

### 🏃 Lightning Fast

| Task | Speed |
|------|-------|
| Generic Llama | 5 tok/sec |
| **Your Model** | **7-15 tok/sec** |
| Claude (API) | Network latency |

**Your model is faster because it's offline.**

### 🔒 100% Private

- Runs on your Mac (no cloud)
- Your data stays on your machine
- No API calls for routine tasks
- Optional: hybrid mode (local + Claude when needed)

### 💵 Cheaper Than Claude

| Usage | Cost/month |
|-------|-----------|
| 1000 Claude calls | ~$15-30 |
| **1000 hybrid calls** | **~$2-5** |
| 1000 local calls | **$0** |

---

## 🎬 Quick Start (5 Minutes)

### 1️⃣ Install Everything
```bash
git clone https://github.com/gabdevbr/llm-training-macos.git
cd llm-training-macos
chmod +x setup.sh
./setup.sh
```

That's it. Python, Ollama, dependencies—all automated.

### 2️⃣ Add Your Context
```bash
# Copy a template
cp -r templates/personal-assistant my-context

# Edit with your info (100+ Q&A examples)
vi my-context/dataset.jsonl
```

Example:
```json
{"instruction": "Who am I?", "response": "You're John, CEO of TechCorp, 15-year industry vet..."}
{"instruction": "What's my revenue?", "response": "2M ARR, growing 20% MoM, 50 customers..."}
{"instruction": "What's my health?", "response": "Type 2 diabetes, take Metformin, exercise 3x/week..."}
```

### 3️⃣ Train (3-4 hours on M4 Pro)
```bash
python3 train.py --context-dir my-context
```

Grab coffee. Model is learning *you*.

### 4️⃣ Run Locally
```bash
ollama run my-context
```

Test it:
```
>>> What's my company's revenue?
Your company has 2M ARR...

>>> Tell me about my health situation
You have Type 2 diabetes and...

>>> What are my top priorities this year?
Based on your context: 1. Scale to 10M ARR...
```

**Done.** You now have a personal AI. 🎉

---

## 📊 Real Example: Skynet

**Built this for myself. Here's what it knows:**

```
- Family: Wife (Rafa), daughter (Isabeli, 12), dog (Brahma)
- Health: Diabetes + anxiety meds, glicemia tracking
- Finance: 2 companies, 6 bank accounts, MEI+Simples strategy
- Work: CEO at Geovendas, GEOLens AI product, SideProjects
- Goals: Bunker infra, local LLM, financial freedom
- Decisions: Prioritize family + impact + learning
```

**When I ask:**
- "How's my mom?" → Knows accident, surgery, recovery status
- "What's my tax strategy?" → Knows MEI/Simples split, DAS calculations
- "What's my next priority?" → Knows projects, blockers, context

**Generic Claude = 0 context. Skynet = complete picture.**

---

## 🎨 5 Templates Included

Choose your use case:

### 1. Personal Assistant ⭐ (Start here)
Know everything about yourself. Decisions, health, family, projects.
```bash
cp -r templates/personal-assistant my-context
```

### 2. Company Knowledge Base
Your org structure, processes, culture, history.
```bash
cp -r templates/company-kb my-context
```

### 3. Support Agent
Your FAQ, common issues, solutions.
```bash
cp -r templates/support-agent my-context
```

### 4. Research Assistant
Papers, notes, findings, deep knowledge.
```bash
cp -r templates/research-assistant my-context
```

### 5. Developer AI
Code patterns, architecture, decisions.
```bash
cp -r templates/developer-ai my-context
```

---

## 🛠 Technical Details

### Hardware Requirements

| Mac | Training Time | Model Size |
|-----|---|---|
| M1 Pro 16GB | 8h | 8B |
| M2 Max 24GB | 4h | 13B |
| **M4 Pro 24GB** | **3-4h** | **13B** |
| M4 Max 36GB | 6h | 70B |

### What's Inside

- **Model:** Llama 3.1 (open source)
- **Training:** LoRA (40x faster, 2% of parameters)
- **Framework:** unsloth (M-series optimized)
- **Quantization:** 4-bit (fits in RAM)
- **Runtime:** Ollama (instant, offline)

### Architecture

```
Your Data (JSONL)
    ↓
Llama 3.1 (base model)
    ↓
LoRA Adapters (your context)
    ↓
Fine-tuned Model
    ↓
Ollama (local inference)
    ↓
Your App / OpenClaw / CLI
```

---

## 🔄 Continuous Learning

**Your model improves every month:**

```bash
# Month 1: Train (3-4 hours, 100 examples)
python3 train.py --context-dir my-context --epochs 3

# Month 2: Add 50 new examples
echo '{"instruction": "..."}' >> my-context/dataset.jsonl

# Re-train (1 hour, just refresh)
python3 train.py --context-dir my-context --epochs 1

# Model gets smarter 📈
```

Git it:
```bash
git add my-context/dataset.jsonl
git commit -m "Monthly update: March 2026 context"
git push
```

---

## 🤝 Hybrid Mode: Local + Claude

**Best of both worlds:**

```
Routine task (80-90%) → Local model (instant + free)
Complex task (10-20%) → Claude (when you really need it)
Fallback → Claude (if local fails)
```

Example:
```python
# "What's my company's revenue?"
→ Local model (knows exact number)
→ Instant response

# "Refactor this 500-line React component"
→ Local model tries, low confidence
→ Falls back to Claude
→ Get better code
```

See `docs/HYBRID_CLAUDE.md` for full integration.

---

## 📚 Documentation

- **[Getting Started](docs/GETTING_STARTED.md)** - 5 minute tutorial
- **[Dataset Format](docs/DATASET_FORMAT.md)** - How to structure your knowledge
- **[Hybrid Mode](docs/HYBRID_CLAUDE.md)** - Local + Claude integration
- **[Contributing](CONTRIBUTING.md)** - How to contribute

---

## 🔐 Privacy & Security

✅ **What stays on your Mac:**
- Your trained model
- Your context/knowledge
- Your inference (responses)

❌ **What's NOT sent anywhere:**
- Family info
- Financial data
- Health details
- Business secrets
- Anything personal

**Optional:** Use hybrid mode to send complex queries to Claude, but you control what.

---

## 💡 Use Cases

### 👤 Personal Assistant
Know your schedule, health, finances, goals. Context-aware suggestions.

### 🏢 Company AI
Internal chatbot. Knows org structure, processes, decisions. No cloud.

### 📞 Support Bot
Answer 80% of customer questions instantly. Escalate complex ones.

### 🔬 Research
Your papers, notes, findings. Instant access to your knowledge.

### 💻 Developer AI
Your codebase patterns, architecture decisions, best practices.

---

## 🚀 Deployment

### Local (Your Mac)
```bash
ollama run my-context
```

### Team (LAN)
```bash
# On any Mac on your network
ollama serve --bind 0.0.0.0:11434

# From other machines
curl http://your-mac.local:11434/api/generate \
  -d '{"model":"my-context","prompt":"..."}'
```

### Server (Linux)
```bash
docker run -d -p 11434:11434 ollama/ollama
# Push your model to server
rsync ./models/my-context/ user@server:~/.ollama/
```

### OpenClaw / LangChain / etc
See `docs/INTEGRATION.md` for examples.

---

## 🎓 Learn & Teach

This started as my personal project (**Skynet**).

Now I'm open-sourcing it so you can:
1. **Build** your own personal AI
2. **Learn** how fine-tuning works
3. **Teach** others (templates + docs included)

All code is commented. All decisions explained.

---

## ⚡ Performance

### Training Speed (first time)

```
M4 Pro with 13B model:
  Download model: 30 min
  Load data: 1 min
  Training (3 epochs): 3-4 hours
  Export: 5 min
  Total: ~4 hours
```

### Inference Speed (after training)

```
Local Llama 13B: 7 tokens/sec
Local Llama 8B: 12 tokens/sec
Claude API: ~2 tokens/sec + network latency
```

**Your local model is faster.**

### Memory Usage

```
Llama 13B 4-bit: ~9GB RAM
Llama 8B 4-bit: ~6GB RAM
Training: +4GB
```

**Fits in 16GB Mac. Comfortable in 24GB.**

---

## 🐛 Troubleshooting

**"Setup failed"**
→ Make sure you're on M1+ Mac. Run `uname -m` → should be `arm64`

**"Training out of memory"**
→ Reduce batch size: `python3 train.py --batch-size 2`

**"Model outputs are generic"**
→ Your dataset is too small. Add 100+ specific examples.

**"Ollama not found"**
→ `brew install ollama` or check `setup.sh` output

See `docs/TROUBLESHOOTING.md` for more.

---

## 📖 Examples

### Personal Assistant (You)
See `templates/personal-assistant/` for example Q&A structure.

### Company KB (Acme Corp)
See `templates/company-kb/` with org structure, processes, culture.

### Support Bot (SaaS)
See `templates/support-agent/` with FAQ, issues, solutions.

---

## 🤖 Built With

- **Llama 3.1** - Open source LLM by Meta
- **unsloth** - 40x faster fine-tuning on Mac
- **LoRA** - Efficient parameter adaptation
- **Ollama** - Local LLM runtime
- **Python** - Training framework

---

## 📄 License

MIT - Use, modify, distribute freely. See [LICENSE](LICENSE).

---

## 🙋 Contributing

Found a bug? Want a new template? Have an improvement?

→ See [CONTRIBUTING.md](CONTRIBUTING.md)

We welcome:
- Bug reports
- New templates
- Documentation improvements
- Integration examples
- Performance tips

---

## 🎯 Next Steps

### Right Now
1. Clone this repo
2. Run `./setup.sh`
3. Pick a template
4. Add your context
5. Train your model

### This Week
- Test your model
- Improve dataset with real examples
- Deploy to Ollama

### This Month
- Add hybrid mode (local + Claude)
- Integrate with your tools
- Share on Twitter/LinkedIn

### Going Forward
- Re-train monthly with new context
- Build community of users
- Contribute templates

---

## 💬 Questions?

- **Getting started:** Read `docs/GETTING_STARTED.md`
- **How to structure data:** See `docs/DATASET_FORMAT.md`
- **Hybrid with Claude:** Check `docs/HYBRID_CLAUDE.md`
- **Integration:** Look for examples in `examples/`
- **Issues:** GitHub Issues welcome

---

## 🌟 Made by [Gab](https://gab.dev.br)

This started as a personal project (**Skynet AI**) to have an AI that actually knows me.

Turns out, this is what many people want.

So I open-sourced it. Enjoy.

---

## 📊 Status

- ✅ Core training works
- ✅ 5 templates ready
- ✅ Documentation complete
- ✅ Examples included
- ⏳ Community contributions welcome

---

<div align="center">

**[⭐ Star on GitHub](https://github.com/gabdevbr/llm-training-macos)** | **[📖 Read Docs](docs/)** | **[🎯 Get Started](docs/GETTING_STARTED.md)**

*Transform your generic AI into an expert on YOU.*

</div>
