# FAQ - Perguntas Frequentes

## Começando

### Q: Preciso ter GPU?
**A:** Não! O projeto é otimizado para **Apple Silicon (M1-M4)** que tem GPU integrada. Se tiver GPU dedicada (NVIDIA), ajude ainda mais. Se tiver CPU apenas, vai ser MUITO lento.

### Q: Qual é a RAM mínima?
**A:** 
- **Mínimo:** 16GB (apertado, com 8B model)
- **Recomendado:** 24GB (confortável, com 13B model)
- **Ideal:** 32GB+ (para 70B model)

### Q: Quanto espaço em disco preciso?
**A:**
- Modelo 8B: ~6GB
- Modelo 13B: ~13GB
- Modelo 70B: ~40GB
- Datasets: 100MB-1GB tipicamente
- **Total:** 20GB mínimo livre

### Q: Funciona em Windows/Linux?
**A:** 
- **Windows:** Com WSL2 + Ubuntu funciona
- **Linux:** Sim, instale `ollama` e rode direto
- **Mac:** Otimizado para M-series
- Mais fácil em **Mac ou Linux**

---

## Treinamento

### Q: Quanto tempo leva pra treinar?
**A:**
| Hardware | 8B Model | 13B Model |
|----------|----------|-----------|
| M1 Pro 16GB | 6-8h | 10-12h |
| M2 Max 24GB | 4-5h | 6-8h |
| **M4 Pro 24GB** | **2-3h** | **3-4h** |
| M4 Max 36GB | 2h | 3-4h |

Primeiros 30min = download do modelo.

### Q: Posso interromper e retomar?
**A:** Sim! LoRA salva checkpoints a cada 50 steps. Você pode:
```bash
python3 train.py --resume-from-checkpoint ./models/my-context/checkpoint-150
```

### Q: Quantos exemplos preciso no dataset?
**A:**
- **Mínimo:** 10-20 (funciona mas genérico)
- **Bom:** 50-100 (recomendado pra começar)
- **Excelente:** 200-500 (modelo muito especializado)
- **Expert:** 1000+ (necessário pra tarefas muito específicas)

### Q: Posso treinar enquanto uso o Mac normalmente?
**A:** Não recomendado. Treinar usa 80-90% da CPU. Melhor deixar a noite.

---

## Dataset

### Q: Qual formato de dados?
**A:** **JSONL** é padrão:
```json
{"instruction": "Q?", "response": "A"}
{"instruction": "Q?", "response": "A"}
```

Mas temos conversores:
- `scripts/csv-to-jsonl.py` para CSV
- Veja `docs/DATASET_FORMAT.md` para Markdown

### Q: Como estruturar boas perguntas/respostas?
**A:** Veja `docs/DATASET_FORMAT.md`. Resumo:
- ✅ Específicas: "Qual é minha receita?" vs "Como é meu negócio?"
- ✅ Longas: >50 chars de resposta
- ✅ Reais: Use dados verdadeiros
- ❌ Genéricas: Evite "Como funciona IA?"
- ❌ Vazias: Sem linhas em branco

### Q: Posso usar dados sensíveis?
**A:** **Não!** Nunca:
- Senhas, API keys
- Números de conta bancária
- Dados médicos privados
- Informações pessoais sensíveis

O modelo é offline (privado), mas é arriscado.

### Q: Como atualizar o modelo mensalmente?
**A:**
```bash
# 1. Adicione dados novos
echo '{"instruction":"...","response":"..."}' >> my-context/dataset.jsonl

# 2. Valide
python3 scripts/validate-dataset.py my-context/dataset.jsonl

# 3. Re-treina (rápido)
python3 train.py --context-dir my-context --epochs 1

# 4. Commit
git add my-context/dataset.jsonl
git commit -m "Monthly update"
```

---

## Usando o Modelo

### Q: Como testar localmente?
**A:**
```bash
ollama run my-context
```

Depois digite perguntas naturalmente. Type `exit` pra sair.

### Q: Qual é a latência (tempo de resposta)?
**A:**
- **Local (seu Mac):** 100-500ms
- **Claude API:** 1-3s + network latency
- **Ollama on server:** 500ms-2s dependendo do hardware

Local é **mais rápido**.

### Q: Posso usar múltiplos modelos?
**A:** Sim! Rode vários:
```bash
ollama pull llama2          # Outro modelo
ollama run my-context       # Seu modelo
ollama run llama2           # Em outro terminal
```

Fallback automático:
```python
if local_confidence < 0.7:
    use_claude()
```

---

## Deploy

### Q: Como colocar em produção?
**A:** Vários jeitos:
1. **Docker:** `docker-compose up`
2. **Linux server:** Instale Ollama + copie modelo
3. **Kubernetes:** Veja `docs/DEPLOYMENT.md`

### Q: Quanto custa rodar em servidor?
**A:**
- **VPS pequena (2GB):** Pode ser ok com 8B
- **VPS média (16GB):** Perfeito pro 13B = ~$50-100/mês
- **GPU cloud:** $200-500/mês (desnecessário se for CPU)

Local no Mac = **R$ 0** (seu equipamento).

### Q: Posso compartilhar o modelo?
**A:** **Sim!** Llama 3.1 é open source. Seus LoRA adapters também.

```bash
# Compartilhar modelo
git push seu-repo models/my-context/

# Alguém usa:
git clone seu-repo
ollama run my-context
```

---

## Problemas Comuns

### Q: "Out of Memory" durante treino
**A:**
```bash
# Opção 1: Batch size menor
python3 train.py --batch-size 2

# Opção 2: Modelo menor
python3 train.py --model-size 8b

# Opção 3: Epoch menor
python3 train.py --epochs 1
```

### Q: Modelo responde genérico
**A:**
- Dataset muito pequeno? Adicione mais exemplos
- Dados muito vagos? Seja mais específico
- Learning rate alto? Tente `--learning-rate 0.0001`

### Q: Ollama não encontra modelo
**A:**
```bash
# Limpar e recarregar
ollama delete my-context
ollama pull my-context

# Ou reiniciar daemon
killall ollama
ollama serve
```

### Q: Modelo lentíssimo
**A:**
```bash
# Aumentar thread count
export OLLAMA_NUM_THREAD=4

# Ou reduzir context size
python3 train.py --max-seq-length 1024
```

### Q: Git push falha
**A:**
```bash
# Modelo é grande, precisa Git LFS
git lfs install
git lfs track "models/my-context/*"
git add .gitattributes
git push
```

---

## Avançado

### Q: Posso usar outro modelo base (não Llama)?
**A:** Sim! Unsloth suporta:
- Mistral 7B
- Qwen
- Phi
- Yi

Mude `--model-name` em `train.py`.

### Q: Como fazer A/B testing?
**A:** Veja `docs/ADVANCED.md`. Resumo:
```bash
# Modelo A (baseline)
python3 train.py --context-dir my-context --output-dir models/a

# Modelo B (novo dataset)
python3 train.py --context-dir new-context --output-dir models/b

# Benchmark
python3 benchmark.py models/a models/b
```

### Q: Posso exportar pra formato diferente?
**A:** Sim, LoRA pode ser merged:
```python
model = model.merge_and_unload()
model.save_pretrained("merged-model/")
```

Depois use com transformers, vLLM, etc.

---

## Contribuindo

### Q: Posso contribuir com novos templates?
**A:** **Sim!** Veja `CONTRIBUTING.md`. Passos:
1. Fork
2. Crie `templates/seu-template/dataset.jsonl`
3. Adicione `templates/seu-template/README.md`
4. PR com descrição

### Q: Como reportar bugs?
**A:** GitHub Issues:
1. Descrição clara
2. Passos pra reproduzir
3. Logs do erro
4. Seu hardware/SO

---

## Financeiro

### Q: Quanto custa tudo?
**A:**
- **Seu Mac:** Já tá pago
- **Treinamento:** R$ 0 (seu computador)
- **Inference local:** R$ 0
- **Opcional Claude fallback:** ~R$ 10-50/mês dependendo uso
- **VPS produção:** $50-200/mês

**Total:** Gratuito pra começar. Opcional a partir do deploy.

### Q: Vale a pena vs Claude?
**A:** Se usar >100 queries/dia:

```
Claude: 100 * $0.01 = $1/dia = $30/mês
Local: $0
Economia: $30/mês

6 meses: $180 economizados
```

Mais rápido + privado também.

---

## Precisa de Mais?

- 📖 Leia `docs/GETTING_STARTED.md` pra começar
- 🛠️ Veja `examples/EXAMPLE_COMPLETE.md` pra case real
- 💬 Abra issue no GitHub pra dúvidas
- 🤝 Contribua com templates/improvements!

---

**Last updated:** 2026-03-06
