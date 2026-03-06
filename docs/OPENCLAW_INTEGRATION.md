# OpenClaw Integration

Integre seu modelo fine-tuned com OpenClaw para automação completa.

## O que é OpenClaw?

OpenClaw é um framework open source para automação e orquestração de IA. Combina com seu modelo local pra máxima eficiência.

## Setup

### 1. Instale OpenClaw
```bash
# No seu Mac ou servidor
npm install -g openclaw
openclaw gateway start
```

### 2. Configure Ollama
```bash
ollama serve  # Em outro terminal
```

### 3. Crie script de integração

Arquivo: `openclaw-integration.js`

```javascript
const Anthropic = require("@anthropic-ai/sdk");

const claude = new Anthropic();

async function handleQuery(question) {
  // 1. Tenta modelo local
  console.log("🤖 Tentando modelo local...");
  
  try {
    const localResponse = await fetch("http://localhost:11434/api/generate", {
      method: "POST",
      body: JSON.stringify({
        model: "my-context",
        prompt: question,
        stream: false
      })
    }).then(r => r.json());
    
    // 2. Avalia confiança
    const confidence = evaluateConfidence(localResponse.response);
    console.log(`   Confiança: ${(confidence * 100).toFixed(0)}%`);
    
    if (confidence > 0.7) {
      console.log("✅ Resposta local OK");
      return localResponse.response;
    }
  } catch (err) {
    console.log("   Modelo local offline, usando Claude");
  }
  
  // 3. Fallback para Claude
  console.log("📡 Usando Claude...");
  const message = await claude.messages.create({
    model: "claude-3-5-sonnet-20241022",
    max_tokens: 1024,
    messages: [{ role: "user", content: question }]
  });
  
  return message.content[0].text;
}

function evaluateConfidence(response) {
  // Simples: se resposta é muito curta, confiança baixa
  if (response.length < 50) return 0.4;
  
  // Se tem "não sei" ou "unclear", confiança baixa
  if (/não sei|unclear|don't know/i.test(response)) {
    return 0.3;
  }
  
  return 0.85;
}

// Export para OpenClaw
module.exports = { handleQuery };
```

## Uso com OpenClaw

### Criar Cron Job

```bash
openclaw cron create \
  --name "daily-briefing" \
  --schedule "0 7 * * *" \
  --script "openclaw-integration.js"
```

### Exemplo: Briefing Diário

```bash
// Script: briefing.js
const { handleQuery } = require("./openclaw-integration");

async function briefing() {
  const agenda = await handleQuery("Qual é minha agenda hoje?");
  const tasks = await handleQuery("Quais são minhas prioridades?");
  const weather = await handleQuery("Como está o tempo?");
  
  return `
📅 Agenda: ${agenda}
🎯 Prioridades: ${tasks}
🌤️ Clima: ${weather}
  `;
}

module.exports = { briefing };
```

### Executar

```bash
# Manual
node briefing.js

# Via cron
openclaw cron create --script "briefing.js" --schedule "0 7 * * *"
```

## Mensagens no Telegram/Mattermost

```javascript
const { message } = require("openclaw");

async function dailyBriefing() {
  const briefing = await generateBriefing();
  
  // Enviar via Telegram
  await message.send({
    channel: "telegram",
    target: "@seu-usuario",
    text: briefing
  });
}
```

## Orquestração Completa

```
OpenClaw Gateway
    ↓
Seu Script (Node.js)
    ↓
├─ Modelo Local (90% das queries)
│  └─ Instant + free
└─ Claude API (10% quando precisa)
   └─ Complex reasoning
    ↓
Resultado
    ↓
Telegram / Mattermost / Webhook
```

## Configuração de Produção

### Docker

```dockerfile
FROM node:18

WORKDIR /app
COPY . .

RUN npm install -g openclaw
RUN npm install

CMD ["openclaw", "gateway", "start"]
```

### Docker Compose

```yaml
version: "3"
services:
  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
  
  openclaw:
    build: .
    ports:
      - "3000:3000"
    depends_on:
      - ollama
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}

volumes:
  ollama_data:
```

Rodar:
```bash
docker-compose up -d
```

## Exemplos de Queries

### Contexto Pessoal
```javascript
const response = await handleQuery(
  "Qual foi minha receita esse mês?"
);
// Usa modelo local (90% confiança)
// Resposta: instant, free, privada
```

### Código Complexo
```javascript
const response = await handleQuery(
  "Refatore esse componente React"
);
// Usa Claude (confiança baixa no local)
// Resposta: melhor qualidade
```

## Monitoramento

Crie dashboard:

```javascript
const log = {
  localQueries: 0,
  claudeQueries: 0,
  totalCost: 0,
  avgLatency: 0
};

async function handleQuery(question) {
  const start = Date.now();
  
  try {
    const local = await callLocal(question);
    if (confidence(local) > 0.7) {
      log.localQueries++;
      log.avgLatency = (Date.now() - start);
      return local;
    }
  } catch {}
  
  log.claudeQueries++;
  log.totalCost += 0.02; // ~$0.02 por Claude call
  
  return await callClaude(question);
}
```

## Troubleshooting

**"Modelo local offline"**
```bash
ollama serve &
# Verifique: curl http://localhost:11434/api/tags
```

**"Rate limit Claude"**
```javascript
// Implemente backoff
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
for (let i = 0; i < 3; i++) {
  try {
    return await callClaude(question);
  } catch {
    await sleep(1000 * Math.pow(2, i)); // Exponential backoff
  }
}
```

**"Modelo local responde genérico"**
- Dataset muito pequeno
- Fine-tune com menos dados
- Aumente batch_size ou learning_rate

## Próximos Passos

1. Setup Ollama + OpenClaw
2. Teste integração local
3. Deploy em produção (Docker)
4. Configure crons diários
5. Monitore custos/performance

---

**Pronto!** Seu modelo agora é parte de um sistema completo. 🚀
