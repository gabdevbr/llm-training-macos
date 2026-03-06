# Advanced: Escalando Treinamento

Técnicas avançadas pra modelos maiores, datasets enormes, e otimizações de produção.

## Aumentar Escala

### 1. Treinar 70B Model

**Requerimentos:**
- Mac M4 Max 36GB+ RAM
- SSD rápido (200GB+ free)
- Tempo: 8-12 horas

**Comando:**
```bash
python3 train.py \
  --model-name "unsloth/llama-3.1-70b-bnb-4bit" \
  --context-dir my-context \
  --batch-size 2 \
  --max-seq-length 2048
```

**Resultado:** Modelo muito mais poderoso, roda com latência aceitável.

### 2. Múltiplos Datasets

Treinar com dados de múltiplas fontes:

```bash
# Combinar datasets
cat dataset1.jsonl dataset2.jsonl dataset3.jsonl > combined.jsonl

# Validar
python3 scripts/validate-dataset.py combined.jsonl

# Treinar
python3 train.py --context-dir . --dataset combined.jsonl
```

### 3. Distributed Training

Treinar em múltiplos Macs simultaneamente:

```python
# dist_train.py
import torch.distributed as dist
import torch.multiprocessing as mp

def train_distributed(rank, world_size):
    dist.init_process_group("nccl", rank=rank, world_size=world_size)
    # Training code aqui
    dist.destroy_process_group()

if __name__ == "__main__":
    mp.spawn(train_distributed, args=(torch.cuda.device_count(),), 
             nprocs=torch.cuda.device_count())
```

## Otimizações

### 1. Quantização Avançada

```python
# 2-bit quantization (ainda mais rápido)
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/llama-3.1-70b-bnb-2bit",  # 2-bit em vez de 4-bit
    max_seq_length=4096,
    load_in_2bit=True,
)
```

**Tradeoff:** Menos memória, qualidade levemente menor.

### 2. Adapters Maiores

```python
# LoRA com rank maior = mais flexibilidade
model = FastLanguageModel.get_peft_model(
    model,
    r=64,  # Era 16, agora 64 (4x maior)
    lora_alpha=32,
    lora_dropout=0.1,
)
```

**Efeito:** Treinamento mais lento, modelo melhor.

### 3. Learning Rate Scheduler

```python
from torch.optim.lr_scheduler import CosineAnnealingLR

scheduler = CosineAnnealingLR(optimizer, T_max=num_epochs)

for epoch in range(num_epochs):
    train()
    scheduler.step()
```

**Efeito:** Converge mais rápido, menos overfitting.

## Datasets Gigantes

### 1. Streaming Dataset

Para datasets maiores que RAM:

```python
from datasets import load_dataset

# Não carrega tudo em memória
dataset = load_dataset("json", data_files="huge-dataset.jsonl", 
                       streaming=True)

# Processa em chunks
for batch in dataset.iter(batch_size=32):
    # Train com batch
    pass
```

### 2. Data Augmentation

Multiplicar exemplos:

```python
def augment_example(instruction, response):
    """Cria variações do mesmo exemplo"""
    return [
        {"instruction": instruction, "response": response},
        {"instruction": f"Explique: {instruction}", 
         "response": f"Explicando: {response}"},
        {"instruction": f"Por que {instruction.lower()}?",
         "response": f"Motivo: {response}"},
    ]
```

**Uso:**
```bash
python3 augment.py dataset.jsonl > augmented.jsonl
# Treina com dataset 3x maior
```

## Avaliação & Benchmark

### 1. Custom Evaluation

```python
def evaluate_model(model, tokenizer, test_dataset):
    """Avalia qualidade do modelo"""
    scores = []
    
    for example in test_dataset:
        prompt = f"[INST] {example['instruction']} [/INST]"
        output = generate(model, tokenizer, prompt)
        
        # Score: similarity com expected response
        similarity = cosine_similarity(output, example['response'])
        scores.append(similarity)
    
    return {
        "avg_similarity": sum(scores) / len(scores),
        "min_similarity": min(scores),
        "max_similarity": max(scores),
    }
```

### 2. Benchmark Público

Compare com outros modelos:

```bash
# Usar HuggingFace benchmark
python3 -m lm_eval \
  --model ollama:my-context \
  --tasks hellaswag,arc_easy,mmlu \
  --batch_size 4
```

## Continuous Learning

### 1. Weekly Retraining Cron

```bash
#!/bin/bash
# retrain.sh

cd /path/to/llm-training-macos

# Pull latest data
git pull

# Train
python3 train.py \
  --context-dir my-context \
  --epochs 1

# Push novo modelo
git add models/my-context/
git commit -m "Weekly retrain: $(date)"
git push
```

Setup cron:
```bash
crontab -e
# 0 2 * * 0 /path/to/retrain.sh  # Toda segunda 2am
```

### 2. A/B Testing

Treinar 2 versões, comparar:

```bash
# Versão A (baseline)
python3 train.py --context-dir my-context \
  --output-dir models/model-a

# Versão B (novo dataset)
cp my-context/dataset.jsonl dataset-new.jsonl
python3 train.py --context-dir . \
  --dataset dataset-new.jsonl \
  --output-dir models/model-b

# Benchmark both
python3 benchmark.py models/model-a models/model-b
```

## Production Monitoring

### 1. Error Tracking

```python
import sentry_sdk

sentry_sdk.init("your-dsn")

try:
    response = generate_response(prompt)
except Exception as e:
    sentry_sdk.capture_exception(e)
    return fallback_response()
```

### 2. Performance Metrics

```python
import prometheus_client

generation_time = prometheus_client.Histogram(
    'generation_time_seconds',
    'Time to generate response'
)

with generation_time.time():
    response = generate_response(prompt)
```

### 3. Quality Monitoring

```python
# Log respostas fracas pra retreinar depois
def log_if_low_quality(prompt, response, confidence):
    if confidence < 0.6:
        with open('low_quality_responses.jsonl', 'a') as f:
            f.write(json.dumps({
                "instruction": prompt,
                "response": response,
                "confidence": confidence
            }) + '\n')
```

## Troubleshooting Avançado

### Out of Memory mid-training?

```python
# Reducir batch size dinamicamente
try:
    train(batch_size=8)
except RuntimeError as e:
    if "out of memory" in str(e):
        train(batch_size=4)  # Retry com batch menor
```

### Modelo converge lentamente?

```python
# Aumentar learning rate
python3 train.py --learning-rate 0.0005  # Era 0.0002
```

### Overfitting (memoriza em vez de aprender)?

```python
# Reduzir LoRA rank ou aumentar dropout
python3 train.py --lora-rank 8 --dropout 0.2
```

## Próximos Passos

1. ✅ Modelo 13B treinado
2. ⏳ Experimente 70B (se tiver hardware)
3. ⏳ Setup weekly retraining
4. ⏳ A/B testing de novas estratégias
5. ⏳ Monitoring + alertas em produção

---

**Agora você é expert!** 🚀
