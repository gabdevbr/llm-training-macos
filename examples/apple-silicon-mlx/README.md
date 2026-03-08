# 🍎 Fine-tuning no Apple Silicon com MLX

Fine-tune de LLM rodando **nativamente** no Apple Silicon (M1/M2/M3/M4) usando [MLX](https://github.com/ml-explore/mlx) da Apple.

## Por que MLX?

| Framework | Apple Silicon | NVIDIA | Memória |
|-----------|:---:|:---:|---------|
| **MLX** | ✅ Nativo | ❌ | Usa memória unificada |
| Unsloth | ❌ | ✅ | Precisa CUDA |
| PyTorch MPS | ⚠️ Parcial | ✅ | Limitado |

**MLX usa memória unificada** — CPU e GPU compartilham os mesmos 24/36/64GB. Sem cópia entre CPU↔GPU.

## Modelos Recomendados por RAM

| RAM | Modelo | Tamanho | Uso no Treino |
|-----|--------|---------|---------------|
| **16GB** | Qwen 2.5 3B 4-bit | ~2GB | ~8-10GB |
| **24GB** | **Qwen 2.5 7B 4-bit** ⭐ | ~4.5GB | ~13-15GB |
| **36GB** | Llama 3.1 8B 4-bit | ~5GB | ~16-18GB |
| **64GB+** | Qwen 2.5 14B 4-bit | ~9GB | ~25-30GB |

> ⭐ **Recomendado pra 24GB:** `mlx-community/Qwen2.5-7B-Instruct-4bit`
> Melhor custo-benefício. Qwen 2.5 7B supera Llama 3.1 8B em benchmarks,
> especialmente em português.

## Setup Rápido

```bash
# 1. Crie ambiente Python
python3 -m venv venv
source venv/bin/activate

# 2. Instale dependências
pip install mlx mlx-lm torch transformers datasets

# 3. Prepare seu dataset (formato JSONL)
# Cada linha: {"instruction": "pergunta", "response": "resposta"}
```

## Rodar Fine-tuning

```bash
# Modelo recomendado pra 24GB RAM
python3 scripts/train-mlx.py \
  --dataset dataset.jsonl \
  --model mlx-community/Qwen2.5-7B-Instruct-4bit \
  --epochs 3 \
  --batch_size 2 \
  --output ./models/meu-modelo

# Acompanhar log em tempo real (outro terminal):
tail -f ./models/meu-modelo/training.log
```

### Opções

| Flag | Default | Descrição |
|------|---------|-----------|
| `--dataset` | `dataset.jsonl` | Dataset JSONL |
| `--model` | `Qwen2.5-7B-Instruct-4bit` | Modelo base (Hugging Face) |
| `--epochs` | `3` | Épocas de treino |
| `--batch_size` | `2` | Exemplos por iteração |
| `--learning_rate` | `1e-5` | Taxa de aprendizado |
| `--lora_rank` | `16` | Rank do LoRA adapter |
| `--output` | `./models/skynet-v1` | Diretório de saída |

## Modelos Testados

### Qwen 2.5 7B Instruct 4-bit ⭐
```bash
--model mlx-community/Qwen2.5-7B-Instruct-4bit
```
- **Melhor opção pra 24GB**
- Excelente em português
- ~4.5GB download, ~15GB no treino

### Qwen 2.5 3B Instruct 4-bit
```bash
--model mlx-community/Qwen2.5-3B-Instruct-4bit
```
- Pra Macs com 16GB
- Mais rápido, menos preciso
- ~2GB download, ~8GB no treino

### Llama 3.2 3B Instruct 4-bit
```bash
--model mlx-community/Llama-3.2-3B-Instruct-4bit
```
- Alternativa Meta
- Bom pra inglês

### Qwen 2.5 14B Instruct 4-bit
```bash
--model mlx-community/Qwen2.5-14B-Instruct-4bit
```
- **Precisa 36GB+ RAM**
- Melhor qualidade
- ~9GB download

## Testar Modelo Treinado

```bash
# Gerar texto
python3 -m mlx_lm.generate \
  --model mlx-community/Qwen2.5-7B-Instruct-4bit \
  --adapter-path ./models/meu-modelo \
  --prompt "Quem é você?"

# Chat interativo
python3 -m mlx_lm.chat \
  --model mlx-community/Qwen2.5-7B-Instruct-4bit \
  --adapter-path ./models/meu-modelo
```

## Fundir Modelo (Opcional)

Cria modelo standalone (sem precisar do base + adapter separados):

```bash
python3 -m mlx_lm.fuse \
  --model mlx-community/Qwen2.5-7B-Instruct-4bit \
  --adapter-path ./models/meu-modelo \
  --save-path ./models/meu-modelo-fused
```

## Usar com Ollama

```bash
# 1. Funda o modelo (passo acima)
# 2. Crie Modelfile
cat > Modelfile << 'MODELFILE'
FROM ./models/meu-modelo-fused
SYSTEM "Você é um assistente pessoal treinado com dados específicos."
MODELFILE

# 3. Registre no Ollama
ollama create meu-modelo -f Modelfile

# 4. Use!
ollama run meu-modelo
```

## Benchmark: M4 Pro 24GB

| Métrica | Qwen 2.5 7B 4-bit |
|---------|-------------------|
| Download | ~4.5 GB |
| RAM no treino | ~13-15 GB |
| Velocidade | ~1.5 it/s |
| 204 iterações | ~2-3 horas |
| Geração | ~15-25 tok/s |

## Formato do Dataset

```jsonl
{"instruction": "Qual é seu nome?", "response": "Sou Skynet, assistente do Gab."}
{"instruction": "Quem é o Gab?", "response": "Gabriel Trevisani, CEO da Geovendas."}
{"instruction": "/contas", "response": "📋 CONTAS\n\n⚠️ ATRASADAS (10)..."}
```

## Troubleshooting

**OOM (Out of Memory)**
- Reduza `--batch_size` (de 2 pra 1)
- Use modelo menor (3B em vez de 7B)
- Feche apps pesados (Chrome, Xcode)

**Treino lento**
- Aumente `--batch_size` (se tiver RAM sobrando)
- Use `--grad_checkpoint` (troca velocidade por memória)

**Modelo não aprende**
- Aumente `--epochs` (de 3 pra 5-10)
- Aumente `--learning_rate` (de 1e-5 pra 5e-5)
- Verifique dataset (mínimo ~50 exemplos)
