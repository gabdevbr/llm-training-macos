#!/bin/bash
set -e

echo "🚀 LLM Training macOS Setup"
echo "=========================="
echo ""

# Check if running on macOS
if [[ ! "$OSTYPE" == "darwin"* ]]; then
    echo "❌ This script is for macOS only"
    exit 1
fi

# Check if M1/M2/M3/M4
ARCH=$(uname -m)
if [[ "$ARCH" != "arm64" ]]; then
    echo "⚠️  Warning: This is optimized for Apple Silicon (M1/M2/M3/M4)"
    echo "   Your Mac is: $ARCH"
    echo "   May still work, but slower"
fi

echo "📦 Step 1: Installing Homebrew packages..."

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install Python 3.11
if ! command -v python3.11 &> /dev/null; then
    echo "Installing Python 3.11..."
    brew install python@3.11
else
    echo "✓ Python 3.11 already installed"
fi

# Install Ollama
if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    brew install ollama
    echo "⚠️  After installation, you may need to:"
    echo "   1. Open Ollama app from Applications"
    echo "   2. Or run: ollama serve"
else
    echo "✓ Ollama already installed"
fi

# Create virtualenv
echo ""
echo "📦 Step 2: Creating Python virtual environment..."

if [ ! -d "venv" ]; then
    python3.11 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

source venv/bin/activate

echo ""
echo "📦 Step 3: Installing Python dependencies..."
echo "(This may take 5-10 minutes...)"

pip install --upgrade pip setuptools wheel

# Install unsloth + dependencies
pip install -q \
    "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git" \
    "xformers==0.0.26.post1" \
    "torch==2.2.1" \
    "transformers==4.39.0" \
    "datasets==2.18.0" \
    "bitsandbytes==0.43.1" \
    "peft==0.10.0" \
    "trl==0.8.1"

echo ""
echo "✅ Installation complete!"
echo ""
echo "📝 Next steps:"
echo ""
echo "1. Copy a template or create your own context:"
echo "   cp -r templates/personal-assistant my-context"
echo ""
echo "2. Edit your dataset:"
echo "   vi my-context/dataset.jsonl"
echo ""
echo "3. Train your model (3-4 hours on M4 Pro):"
echo "   python3 train.py --context-dir my-context"
echo ""
echo "4. Run locally:"
echo "   ollama run my-context"
echo ""
echo "For more help, see: docs/GETTING_STARTED.md"

# === MLX (Apple Silicon) ===
echo ""
echo "🍎 Detectando Apple Silicon..."
if [[ $(uname -m) == "arm64" ]] && [[ $(uname -s) == "Darwin" ]]; then
    echo "   ✅ Apple Silicon detectado!"
    echo "   Instalando MLX..."
    pip install mlx mlx-lm
    echo "   ✅ MLX instalado!"
    echo ""
    echo "   Para treinar com MLX:"
    echo "   python3 scripts/train-mlx.py --dataset dataset.jsonl"
else
    echo "   ℹ️ Não é Apple Silicon — usando unsloth/CUDA"
fi
