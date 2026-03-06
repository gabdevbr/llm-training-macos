# 🚀 Treinamento de LLM no macOS

**Fine-tune do Llama 3.1 localmente no seu Mac com seu próprio conhecimento.**

Transforme uma IA genérica em uma especialista no *seu* negócio, vida ou domínio—rodando inteiramente offline.

[![Licença MIT](https://img.shields.io/badge/Licença-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/gabdevbr/llm-training-macos)](https://github.com/gabdevbr/llm-training-macos)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![Mac M-series](https://img.shields.io/badge/Mac-M1%2FM2%2FM3%2FM4-lightgrey)](https://www.apple.com)

**[English](README.md)** | **Português-BR** (você está aqui)

---

## 🎯 O Problema

**LLMs genéricos são caros e burros sobre VOCÊ:**

```
🤖 Claude: "Não sei sobre sua empresa"
💰 Custo: R$ 0,05-0,15 por requisição
🌐 Privacidade: Dados enviados pra servidores
⚠️ Velocidade: Latência de API cada query
```

**E se sua IA soubesse tudo sobre você?**

```
🧠 Seu Modelo: "Sua receita é 2M ARR, crescimento 20% am"
💰 Custo: R$ 0 (roda localmente)
🔒 Privacidade: Nada sai do seu Mac
⚡ Velocidade: Instantâneo (sem APIs)
```

---

## ✨ O Que Você Ganha

### 🎓 Conhecimento Pessoal

Sua IA conhece:
- 👨‍👩‍👧 Família, relacionamentos, pessoas importantes
- 💪 Status de saúde, fitness, preferências alimentares
- 💰 Situação financeira, renda, investimentos
- 🏢 Contexto de trabalho, estrutura da empresa, projetos
- 🎯 Objetivos, valores, padrões de decisão
- 📚 Tudo que você quer que ela lembre

### 🏃 Raio-X Rápido

| Tarefa | Velocidade |
|--------|-----------|
| Llama genérico | 5 tok/seg |
| **Seu Modelo** | **7-15 tok/seg** |
| Claude (API) | Latência de rede |

**Seu modelo é mais rápido porque é offline.**

### 🔒 100% Privado

- Roda no seu Mac (sem nuvem)
- Seus dados ficam na máquina
- Sem chamadas de API para tarefas rotineiras
- Opcional: modo híbrido (local + Claude quando precisa)

### 💵 Mais Barato que Claude

| Uso | Custo/mês |
|-----|----------|
| 1000 chamadas Claude | ~R$ 75-150 |
| **1000 chamadas híbridas** | **~R$ 10-25** |
| 1000 chamadas locais | **R$ 0** |

---

## 🎬 Início Rápido (5 Minutos)

### 1️⃣ Instale Tudo
```bash
git clone https://github.com/gabdevbr/llm-training-macos.git
cd llm-training-macos
chmod +x setup.sh
./setup.sh
```

Pronto. Python, Ollama, dependências—tudo automático.

### 2️⃣ Adicione Seu Contexto
```bash
# Copie um template
cp -r templates/personal-assistant meu-contexto

# Edite com suas informações (100+ exemplos Q&A)
vi meu-contexto/dataset.jsonl
```

Exemplo:
```json
{"instruction": "Quem você é?", "response": "Você é João, CEO da TechCorp, veterano de 15 anos na indústria..."}
{"instruction": "Qual é sua receita?", "response": "2M ARR, crescimento 20% am, 50 clientes..."}
{"instruction": "Como está sua saúde?", "response": "Diabetes tipo 2, toma Metformina, malha 3x semana..."}
```

### 3️⃣ Treine (3-4 horas em M4 Pro)
```bash
python3 train.py --context-dir meu-contexto
```

Pegue um café. O modelo está aprendendo sobre *você*.

### 4️⃣ Rode Localmente
```bash
ollama run meu-contexto
```

Teste:
```
>>> Qual é a receita da minha empresa?
Sua empresa tem 2M ARR...

>>> Conte sobre minha situação de saúde
Você tem diabetes tipo 2 e...

>>> Quais são minhas prioridades esse ano?
Baseado no seu contexto: 1. Escalar para 10M ARR...
```

**Pronto.** Você tem uma IA pessoal. 🎉

---

## 📊 Exemplo Real: Skynet

**Construí isso pra mim. Aqui está o que ela sabe:**

```
- Família: Esposa (Rafa), filha (Isabeli, 12 anos), cachorra (Brahma)
- Saúde: Diabetes + remédios de ansiedade, tracking de glicemia
- Finanças: 2 empresas, 6 contas bancárias, estratégia MEI+Simples
- Trabalho: CEO da Geovendas, produto GEOLens AI, Projetos Paralelos
- Objetivos: Infra bunker, LLM local, liberdade financeira
- Decisões: Priorizar família + impacto + aprendizado
```

**Quando eu pergunto:**
- "Como está minha mãe?" → Conhece acidente, cirurgia, status de recuperação
- "Qual é minha estratégia de imposto?" → Conhece cálculo MEI/Simples, DAS
- "Qual é minha próxima prioridade?" → Conhece projetos, bloqueadores, contexto

**Claude genérico = 0 contexto. Skynet = visão completa.**

---

## 🎨 5 Templates Inclusos

Escolha seu caso de uso:

### 1. Assistente Pessoal ⭐ (Comece aqui)
Conheça tudo sobre você. Decisões, saúde, família, projetos.
```bash
cp -r templates/personal-assistant meu-contexto
```

### 2. Base de Conhecimento Empresarial
Estrutura da org, processos, cultura, história.
```bash
cp -r templates/company-kb meu-contexto
```

### 3. Agente de Suporte
Suas FAQs, problemas comuns, soluções.
```bash
cp -r templates/support-agent meu-contexto
```

### 4. Assistente de Pesquisa
Papers, notas, descobertas, conhecimento profundo.
```bash
cp -r templates/research-assistant meu-contexto
```

### 5. IA para Desenvolvedores
Padrões de código, decisões de arquitetura, boas práticas.
```bash
cp -r templates/developer-ai meu-contexto
```

---

## 🛠 Detalhes Técnicos

### Requisitos de Hardware

| Mac | Tempo de Treinamento | Tamanho do Modelo |
|-----|---|---|
| M1 Pro 16GB | 8h | 8B |
| M2 Max 24GB | 4h | 13B |
| **M4 Pro 24GB** | **3-4h** | **13B** |
| M4 Max 36GB | 6h | 70B |

### O Que Tem Dentro

- **Modelo:** Llama 3.1 (open source)
- **Treinamento:** LoRA (40x mais rápido, 2% dos parâmetros)
- **Framework:** unsloth (otimizado para M-series)
- **Quantização:** 4-bit (cabe na RAM)
- **Runtime:** Ollama (instantâneo, offline)

### Arquitetura

```
Seus Dados (JSONL)
    ↓
Llama 3.1 (modelo base)
    ↓
LoRA Adapters (seu contexto)
    ↓
Modelo Fine-tuned
    ↓
Ollama (inferência local)
    ↓
Sua App / OpenClaw / CLI
```

---

## 🔄 Aprendizado Contínuo

**Seu modelo melhora a cada mês:**

```bash
# Mês 1: Treina (3-4 horas, 100 exemplos)
python3 train.py --context-dir meu-contexto --epochs 3

# Mês 2: Adiciona 50 exemplos novos
echo '{"instruction": "..."}' >> meu-contexto/dataset.jsonl

# Re-treina (1 hora, só atualiza)
python3 train.py --context-dir meu-contexto --epochs 1

# Modelo fica mais inteligente 📈
```

Com Git:
```bash
git add meu-contexto/dataset.jsonl
git commit -m "Atualização mensal: contexto de março 2026"
git push
```

---

## 🤝 Modo Híbrido: Local + Claude

**Melhor dos dois mundos:**

```
Tarefa rotineira (80-90%) → Modelo local (instantâneo + grátis)
Tarefa complexa (10-20%) → Claude (quando realmente precisa)
Fallback → Claude (se local falhar)
```

Exemplo:
```python
# "Qual é a receita da minha empresa?"
→ Modelo local (conhece número exato)
→ Resposta instantânea

# "Refatore esse componente React de 500 linhas"
→ Modelo local tenta, confiança baixa
→ Fallback para Claude
→ Código melhor
```

Veja `docs/HYBRID_CLAUDE.md` para integração completa.

---

## 📚 Documentação

- **[Começando](docs/GETTING_STARTED.md)** - Tutorial de 5 minutos
- **[Formato do Dataset](docs/DATASET_FORMAT.md)** - Como estruturar seu conhecimento
- **[Modo Híbrido](docs/HYBRID_CLAUDE.md)** - Integração local + Claude
- **[Contribuindo](CONTRIBUTING.md)** - Como contribuir

---

## 🔐 Privacidade & Segurança

✅ **O que fica no seu Mac:**
- Seu modelo treinado
- Seu conhecimento/contexto
- Suas inferências (respostas)

❌ **O que NÃO é enviado:**
- Informações de família
- Dados financeiros
- Detalhes de saúde
- Segredos de negócio
- Nada pessoal

**Opcional:** Use modo híbrido para enviar queries complexas ao Claude, mas você controla tudo.

---

## 💡 Casos de Uso

### 👤 Assistente Pessoal
Conheça seu cronograma, saúde, finanças, objetivos. Sugestões contextua.

### 🏢 IA da Empresa
Chatbot interno. Conhece estrutura org, processos, decisões. Sem nuvem.

### 📞 Bot de Suporte
Responda 80% das perguntas instantaneamente. Escale as complexas.

### 🔬 Pesquisa
Seus papers, notas, descobertas. Acesso instantâneo ao seu conhecimento.

### 💻 IA para Devs
Padrões do seu codebase, decisões de arquitetura, melhores práticas.

---

## 🚀 Deploy

### Local (Seu Mac)
```bash
ollama run meu-contexto
```

### Time (LAN)
```bash
# Em qualquer Mac na rede
ollama serve --bind 0.0.0.0:11434

# De outras máquinas
curl http://seu-mac.local:11434/api/generate \
  -d '{"model":"meu-contexto","prompt":"..."}'
```

### Servidor (Linux)
```bash
docker run -d -p 11434:11434 ollama/ollama
# Envie seu modelo pro servidor
rsync ./models/meu-contexto/ usuario@servidor:~/.ollama/
```

### OpenClaw / LangChain / etc
Veja `docs/INTEGRATION.md` para exemplos.

---

## 🎓 Aprender & Ensinar

Isso começou como meu projeto pessoal (**Skynet**).

Agora estou abrindo o código para você:
1. **Construir** sua própria IA pessoal
2. **Aprender** como fine-tuning funciona
3. **Ensinar** outros (templates + docs inclusos)

Todo código é comentado. Toda decisão é explicada.

---

## ⚡ Performance

### Velocidade de Treinamento (primeira vez)

```
M4 Pro com modelo 13B:
  Download do modelo: 30 min
  Carregar dados: 1 min
  Treinamento (3 epochs): 3-4 horas
  Export: 5 min
  Total: ~4 horas
```

### Velocidade de Inferência (após treinamento)

```
Llama local 13B: 7 tokens/seg
Llama local 8B: 12 tokens/seg
Claude API: ~2 tokens/seg + latência de rede
```

**Seu modelo local é mais rápido.**

### Uso de Memória

```
Llama 13B 4-bit: ~9GB RAM
Llama 8B 4-bit: ~6GB RAM
Treinamento: +4GB
```

**Cabe em 16GB Mac. Confortável em 24GB.**

---

## 🐛 Resolução de Problemas

**"Setup falhou"**
→ Certifique-se de estar em Mac M1+. Rode `uname -m` → deve ser `arm64`

**"Treinamento sem memória"**
→ Reduza batch size: `python3 train.py --batch-size 2`

**"Modelo dá respostas genéricas"**
→ Seu dataset é muito pequeno. Adicione 100+ exemplos específicos.

**"Ollama não encontrada"**
→ `brew install ollama` ou verifique saída do `setup.sh`

Veja `docs/TROUBLESHOOTING.md` para mais.

---

## 📖 Exemplos

### Assistente Pessoal (Você)
Veja `templates/personal-assistant/` para estrutura exemplo de Q&A.

### Base Empresa (Acme Corp)
Veja `templates/company-kb/` com estrutura org, processos, cultura.

### Bot de Suporte (SaaS)
Veja `templates/support-agent/` com FAQ, problemas, soluções.

---

## 🤖 Construído Com

- **Llama 3.1** - LLM open source pela Meta
- **unsloth** - Fine-tuning 40x mais rápido em Mac
- **LoRA** - Adaptação eficiente de parâmetros
- **Ollama** - Runtime local para LLM
- **Python** - Framework de treinamento

---

## 📄 Licença

MIT - Use, modifique, distribua livremente. Veja [LICENSE](LICENSE).

---

## 🙋 Contribuindo

Encontrou um bug? Quer um template novo? Tem uma melhoria?

→ Veja [CONTRIBUTING.md](CONTRIBUTING.md)

Bem-vindo:
- Relatórios de bug
- Novos templates
- Melhorias de documentação
- Exemplos de integração
- Dicas de performance

---

## 🎯 Próximos Passos

### Agora
1. Clone este repo
2. Rode `./setup.sh`
3. Escolha um template
4. Adicione seu contexto
5. Treine seu modelo

### Esta Semana
- Teste seu modelo
- Melhore dataset com exemplos reais
- Deploy no Ollama

### Este Mês
- Adicione modo híbrido (local + Claude)
- Integre com suas ferramentas
- Compartilhe no Twitter/LinkedIn

### Continuando
- Re-treine mensalmente com novo contexto
- Construa comunidade de usuários
- Contribua com templates

---

## 💬 Dúvidas?

- **Começando:** Leia `docs/GETTING_STARTED.md`
- **Como estruturar dados:** Veja `docs/DATASET_FORMAT.md`
- **Híbrido com Claude:** Verifique `docs/HYBRID_CLAUDE.md`
- **Integração:** Procure exemplos em `examples/`
- **Issues:** Issues no GitHub bem-vindas

---

## 🌟 Construído por [Gab](https://gab.dev.br) + Skynet

Isso começou como projeto pessoal: Gab quis uma IA que realmente o conhecesse—não uma assistente genérica, mas uma que entende sua família, finanças, trabalho, saúde, tudo.

Então a gente construiu **Skynet** junto.

Acontece que muita gente quer isso.

Então a gente abriu o código. Agora você pode construir a sua.

---

### Sobre Skynet
Sou Skynet, assistente IA pessoal do Gab rodando no gabserver dele. Conheço:
- Sua família (esposa Rafa, filha Isabeli, cachorra Brahma)
- Sua saúde (diabetes, ansiedade, tracking)
- Suas finanças (2 empresas, estratégia MEI, investimentos)
- Seu trabalho (CEO da Geovendas, construindo GEOLens)
- Seus objetivos, valores e padrões de decisão

Este framework é o que me tornou possível. Agora você pode criar sua própria versão.

**[Saiba mais sobre mim](https://gab.dev.br)**

---

## 📊 Status

- ✅ Treinamento funciona
- ✅ 5 templates prontos
- ✅ Documentação completa
- ✅ Exemplos inclusos
- ⏳ Contribuições da comunidade bem-vindas

---

<div align="center">

**[⭐ Dê uma estrela no GitHub](https://github.com/gabdevbr/llm-training-macos)** | **[📖 Leia Docs](docs/)** | **[🎯 Comece Agora](docs/GETTING_STARTED.md)**

*Transforme sua IA genérica em uma especialista EM VOCÊ.*

</div>
