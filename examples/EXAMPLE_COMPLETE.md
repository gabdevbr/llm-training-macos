# Exemplo Completo: Do Início ao Fim

## Cenário

Você é CEO de uma startup tech. Quer uma IA que conhece sua empresa, processos, valores.

## Passo 1: Criar Dataset

### Dados Básicos

Arquivo: `my-company/dataset.jsonl`

```json
{"instruction": "Qual é nossa missão?", "response": "Nossa missão é democratizar IA para pequenas empresas. Acreditamos que toda empresa merece acesso a ferramentas de IA sem custo proibitivo."}
{"instruction": "Qual é nossa estrutura de time?", "response": "Temos 12 pessoas: 6 engineers, 3 sales, 2 ops, 1 CEO. Cada um tem responsabilidade clara e KPIs específicos."}
{"instruction": "Qual é nosso maior problema agora?", "response": "Customer retention em 3 meses é 60%. Precisamos melhorar onboarding e suporte pós-venda."}
{"instruction": "Quais são nossas receitas?", "response": "MRR atual é $15k. Crescimento: 15% ao mês. Runway: 18 meses."}
{"instruction": "Qual é nossa tech stack?", "response": "Frontend: React + TypeScript. Backend: Python + FastAPI. DB: PostgreSQL. Hosting: AWS. Monitoramento: DataDog."}
```

### Validar Dataset

```bash
python3 scripts/validate-dataset.py my-company/dataset.jsonl
```

Output:
```
✅ Dataset excelente!
   Total: 5 linhas
```

## Passo 2: Treinar Modelo

### Setup

```bash
source venv/bin/activate
```

### Treinar

```bash
python3 train.py \
  --context-dir my-company \
  --model-size 13b \
  --epochs 3 \
  --batch-size 4
```

Output:
```
✅ Modelo configurado: unsloth/llama-3.1-13b-bnb-4bit
   LoRA rank: 16, dropout: 0.05
✅ Carregou 5 exemplos do dataset
🚀 Iniciando treino...
   Epochs: 3
   Batch size: 4
   Learning rate: 0.0002
   Salva em: ./models/my-company
...
[Espera 3-4 horas no M4 Pro]
...
✅ Treino concluído!
   Modelo salvo em: ./models/my-company
```

## Passo 3: Testar Localmente

### Rodar

```bash
ollama run my-company
```

### Teste 1: Contexto Pessoal

```
>>> Qual é nossa missão?
Nossa missão é democratizar IA para pequenas empresas. Acreditamos que toda empresa merece acesso a ferramentas de IA sem custo proibitivo.
```

✅ **Funciona!** Respondeu com exatidão a partir dos dados.

### Teste 2: Inferência Lógica

```
>>> Qual deve ser nossa próxima prioridade?
Based on your context, as a startup with 60% retention rate and $15k MRR, your priority should be:
1. Improve customer onboarding (reduce churn)
2. Accelerate MRR growth to extend runway
3. Build retention metrics and feedback loops

You mentioned needing better post-sale support, so starting there would directly impact retention.
```

✅ **Funciona!** Raciocinou a partir do contexto.

## Passo 4: Deploy

### Para o Time (LAN)

```bash
ollama serve --bind 0.0.0.0:11434
```

Acesso:
```bash
curl http://seu-mac.local:11434/api/generate \
  -d '{"model":"my-company","prompt":"Qual é nossa receita?"}'
```

### Para Servidor

```bash
# Copiar modelo
rsync -avz ./models/my-company/ user@server:~/.ollama/models/

# No servidor
ollama serve
```

## Passo 5: Melhorar Mensalmente

### Adicionar Dados Novos

```bash
# Adicione novas linhas ao dataset
echo '{"instruction": "Qual é nosso NPS?", "response": "NPS atual é 45. Meta: 60 até Q3."}' >> my-company/dataset.jsonl
```

### Re-treinar (Rápido)

```bash
python3 train.py --context-dir my-company --epochs 1
```

Output:
```
✅ Treino concluído em 1 hora!
   Modelo melhorado: agora conhece NPS
```

## Resultados

| Métrica | Valor |
|---------|-------|
| Tempo de treinamento | 3-4h (M4 Pro) |
| Tamanho do modelo | ~13GB em disco |
| Latência de resposta | <1 segundo (local) |
| Custo total | R$ 0 |
| Privacidade | 100% offline |

## Próximos Passos

1. **Expanda dataset:** Adicione 100+ exemplos (processos, decisões, histórico)
2. **Integre com ferramentas:** OpenClaw, LangChain, etc
3. **Híbrido:** Use Claude pra decisões estratégicas complexas
4. **Monitore:** Track quais perguntas o modelo falha, melhore dados

---

**Pronto!** Você tem uma IA interna da sua empresa. 🚀
