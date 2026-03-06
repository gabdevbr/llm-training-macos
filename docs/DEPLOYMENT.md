# Deployment & CI/CD

Deploy seu modelo fine-tuned para produção.

## Opções de Deploy

### 1. Máquina Local (Mac)

Já está rodando:
```bash
ollama run my-context
```

**Vantagem:** Simples, privado, zero custo  
**Desvantagem:** Só você tem acesso

### 2. Rede Local (LAN)

Compartilhe com seu time no mesmo Wi-Fi:

```bash
# No seu Mac
ollama serve --bind 0.0.0.0:11434
```

**Acesso remoto:**
```bash
curl http://seu-mac.local:11434/api/generate \
  -d '{"model":"my-context","prompt":"..."}'
```

**Vantagem:** Rápido, time inteiro acessa  
**Desvantagem:** Só funciona na LAN

### 3. Servidor Remoto (VPS/AWS)

Deploy em servidor Linux:

#### A. Requisitos

- Linux (Ubuntu 20.04+)
- Docker instalado
- 16GB RAM mínimo
- 50GB disk free

#### B. Setup via Docker

```bash
# No servidor
docker run -d -p 11434:11434 \
  -v ollama_data:/root/.ollama \
  ollama/ollama

# Copiar modelo do Mac
scp -r ~/.ollama/models/my-context \
  user@seu-servidor:/root/.ollama/models/

# Puxar modelo
docker exec $(docker ps -q) \
  ollama pull my-context
```

#### C. API Endpoint

Seu modelo agora está em:
```
https://api.seu-servidor.com:11434
```

Use em produção:
```bash
curl https://api.seu-servidor.com:11434/api/generate \
  -d '{"model":"my-context","prompt":"..."}'
```

### 4. Kubernetes (Escala)

Para múltiplas instâncias:

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ollama-model
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: ollama
        image: ollama/ollama
        ports:
        - containerPort: 11434
        volumeMounts:
        - name: models
          mountPath: /root/.ollama
      volumes:
      - name: models
        persistentVolumeClaim:
          claimName: ollama-models
```

Deploy:
```bash
kubectl apply -f deployment.yaml
```

---

## CI/CD Pipeline

### Setup GitHub Actions

Arquivo: `.github/workflows/train.yml`

```yaml
name: Auto-train on dataset update

on:
  push:
    paths:
      - 'my-context/dataset.jsonl'

jobs:
  train:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m venv venv
          source venv/bin/activate
          pip install -r requirements.txt
      
      - name: Validate dataset
        run: python scripts/validate-dataset.py my-context/dataset.jsonl
      
      - name: Train model
        run: python train.py --context-dir my-context --epochs 1
      
      - name: Upload model
        uses: actions/upload-artifact@v3
        with:
          name: trained-model
          path: models/my-context/
```

### Workflow

```
1. Você adiciona dados ao dataset.jsonl
2. Faz push no GitHub
3. GitHub Actions:
   - Valida dataset
   - Treina modelo (1h)
   - Salva artefato
4. Você baixa modelo novo
5. Deploy em produção
```

---

## Monitoring & Logging

### Health Check

```bash
# Verificar se modelo está online
curl http://localhost:11434/api/tags

# Response:
# {"models":[{"name":"my-context:latest",...}]}
```

### Logs

```bash
# Docker logs
docker logs <container-id>

# Seu Mac
ollama serve &
tail -f ~/.ollama/logs/server.log
```

### Prometheus Metrics

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'ollama'
    static_configs:
      - targets: ['localhost:11434']
```

---

## Segurança em Produção

### API Key

Proteja seu endpoint:

```javascript
const express = require('express');
const app = express();

const VALID_KEY = process.env.API_KEY;

app.post('/api/generate', (req, res) => {
  const key = req.headers['x-api-key'];
  
  if (!key || key !== VALID_KEY) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  
  // Chamar Ollama
  // ...
});
```

Uso:
```bash
curl -H "X-API-Key: seu-secret-key" \
  http://localhost:11434/api/generate
```

### Rate Limiting

```javascript
const rateLimit = require("express-rate-limit");

const limiter = rateLimit({
  windowMs: 1 * 60 * 1000, // 1 minuto
  max: 60 // 60 requests/min
});

app.use('/api/', limiter);
```

### HTTPS

```bash
# Gerar certificado self-signed
openssl req -x509 -newkey rsa:4096 \
  -keyout key.pem -out cert.pem -days 365
```

```javascript
const https = require('https');
const fs = require('fs');

const options = {
  key: fs.readFileSync('key.pem'),
  cert: fs.readFileSync('cert.pem')
};

https.createServer(options, app).listen(11434);
```

---

## Performance Tuning

### Batch Requests

Economize latência:

```bash
# Lento: 10 requests sequenciais
for i in 1..10; do
  curl http://localhost:11434/api/generate ...
done

# Rápido: 10 requests em paralelo
for i in 1..10; do
  curl ... &
done
wait
```

### Caching

```javascript
const NodeCache = require("node-cache");
const cache = new NodeCache({ stdTTL: 3600 }); // 1h

app.post('/api/generate', (req, res) => {
  const key = req.body.prompt;
  
  if (cache.has(key)) {
    return res.json(cache.get(key));
  }
  
  // Gerar resposta
  const result = await generateResponse(req.body);
  cache.set(key, result);
  
  res.json(result);
});
```

### Load Balancing

```yaml
# docker-compose com 3 instâncias
services:
  ollama-1:
    image: ollama/ollama
    ports: ["11435:11434"]
  
  ollama-2:
    image: ollama/ollama
    ports: ["11436:11434"]
  
  ollama-3:
    image: ollama/ollama
    ports: ["11437:11434"]
  
  nginx:
    image: nginx
    ports: ["11434:80"]
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

`nginx.conf`:
```
upstream ollama {
  server ollama-1:11434;
  server ollama-2:11434;
  server ollama-3:11434;
}

server {
  listen 80;
  location / {
    proxy_pass http://ollama;
  }
}
```

---

## Troubleshooting

**Modelo muito lento**
- Aumentar RAM
- Usar GPU se disponível
- Load balancer com múltiplas instâncias

**Out of memory**
- Reduzir batch_size
- Usar modelo 8B em vez de 13B

**Modelo não carrega**
```bash
# Limpar cache
ollama delete my-context
ollama pull my-context
```

---

## Próximos Passos

1. ✅ Treinar modelo localmente
2. ✅ Deploy em produção
3. ⏳ Setup CI/CD (auto-treina em updates)
4. ⏳ Monitoring + alertas
5. ⏳ Escalar com load balancer

---

**Pronto pra produção!** 🚀
