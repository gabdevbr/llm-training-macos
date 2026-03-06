# Getting Started in 5 Minutes

## Prerequisites

- Mac with Apple Silicon (M1/M2/M3/M4)
- 16GB RAM (24GB recommended)
- 20GB free disk space

## Step 1: Clone & Setup (5 min)

```bash
# Clone the repo
git clone https://github.com/gab-dev/llm-training-macos.git
cd llm-training-macos

# Run automated setup
chmod +x setup.sh
./setup.sh

# This installs:
# - Python 3.11
# - Ollama
# - All dependencies
```

After setup, activate virtual environment:
```bash
source venv/bin/activate
```

## Step 2: Choose Your Template (1 min)

Pick one based on your use case:

```bash
# Option A: Personal assistant (recommended for first time)
cp -r templates/personal-assistant my-context

# Option B: Company knowledge base
cp -r templates/company-kb my-context

# Option C: Support agent
cp -r templates/support-agent my-context

# Option D: Start from scratch
mkdir my-context
cat > my-context/dataset.jsonl << 'EOF'
{"instruction": "Who are you?", "response": "I'm YOUR AI assistant"}
EOF
```

## Step 3: Add Your Context (5-30 min)

Edit `my-context/dataset.jsonl` with YOUR information:

```json
{"instruction": "Tell me about yourself", "response": "I'm [YOUR NAME]..."}
{"instruction": "What do you do?", "response": "I work at [COMPANY]..."}
{"instruction": "What are your main projects?", "response": "1. [PROJECT1] 2. [PROJECT2]..."}
```

**Tips:**
- 50+ examples = fair model
- 100+ examples = good model
- 200+ examples = excellent model
- Start with 100, add more monthly

See `docs/DATASET_FORMAT.md` for full guide.

## Step 4: Train Your Model (3-4 hours)

```bash
python3 train.py --context-dir my-context
```

Or with specific parameters:
```bash
python3 train.py \
  --context-dir my-context \
  --model-size 13b \
  --epochs 3 \
  --batch-size 4
```

This will:
1. Download Llama 3.1 (first time only)
2. Load your data
3. Fine-tune with LoRA (40x faster)
4. Save checkpoints every 50 steps
5. Export to Ollama format

**On M4 Pro:** ~3-4 hours for 13B model

## Step 5: Test Locally (2 min)

In another terminal:

```bash
ollama serve  # Start Ollama daemon (if not running)
```

Then:
```bash
ollama run my-context
```

Test it:
```
>>> Who am I?
# Your model should answer with your context

>>> What's my company?
# Should have detailed knowledge

>>> Tell me a joke
# Should match your personality
```

Type `exit` to quit.

## Step 6: Deploy (Optional)

### Deploy to Another Mac
```bash
rsync -avz ./models/my-context/ user@other-mac:~/.ollama/models/
```

### Deploy to Server
```bash
# Copy to server
rsync -avz ./models/my-context/ user@server:~/.ollama/models/

# On server, start Ollama API
ollama serve

# Call from anywhere
curl -X POST http://server:11434/api/generate \
  -d '{"model":"my-context", "prompt":"Who am I?"}'
```

## What Next?

### ✅ Immediate
- [x] Setup complete
- [x] Model trained
- [x] Testing locally

### 📚 Learning
- Read `docs/DATASET_FORMAT.md` for data tips
- Read `docs/HYBRID_CLAUDE.md` for Claude integration
- Check `CONTRIBUTING.md` if want to contribute

### 🚀 Advanced
- Integrate with OpenClaw: see `docs/OPENCLAW_INTEGRATION.md`
- Set up CI/CD: see `docs/DEPLOYMENT.md`
- Scale training: see `docs/ADVANCED.md`

### 📈 Next Month
- Add 50-100 new context lines
- Re-train with `--epochs 1` (1 hour)
- Push improvements to git

## Troubleshooting

### "Out of memory"
```bash
python3 train.py --batch-size 2 --model-size 8b
```

### "Setup.sh not executable"
```bash
chmod +x setup.sh
./setup.sh
```

### "Ollama not found"
```bash
# Install via Homebrew
brew install ollama
# Then start daemon
ollama serve
```

### "Model outputs are generic"
- Add more specific examples to dataset.jsonl
- Increase --epochs (try 5 instead of 3)
- Check data quality (see DATASET_FORMAT.md)

### "Training very slow"
```bash
# Use 8B instead of 13B
python3 train.py --context-dir my-context --model-size 8b
```

## Questions?

- Check `README.md` for overview
- See `docs/` folder for detailed guides
- Open a GitHub issue
- Check Discussions for Q&A

## Success Criteria

You're ready when:
- ✅ Model runs locally (`ollama run my-context`)
- ✅ Responds to questions about YOUR context
- ✅ Gives different answers than generic Llama
- ✅ Matches your personality/style

**Welcome!** 🚀 You now have a personal AI.
