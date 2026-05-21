# 7C Hub News

Sistema de agregação, curadoria e distribuição automatizada de notícias de tecnologia.

## Estrutura do Projeto

- **collector (Go):** Coleta notícias de múltiplas fontes.
- **processor (Python):** Processamento de IA para tradução, resumo e ranqueamento.
- **deliverer (Python):** Entrega do boletim via WhatsApp/Telegram.

## Como Executar

O sistema é executado em três etapas sequenciais:

### 1. Coletor (Go)
Coleta notícias das fontes configuradas em `sources.yaml` e gera um arquivo intermediário `output/news.json`.

```bash
# Navegue até o diretório do coletor
cd collector
# Execute a coleta (o binário lê o sources.yaml na raiz)
go run main.go -config ../sources.yaml -output ../output/news.json
# Retorne à raiz
cd ..
```

### 2. Processador (Python)
Processa as notícias coletadas (tradução, resumo e seleção) e gera o boletim em `output/bulletin.txt`.

**Configuração Prévia:**
Crie um arquivo `.env` na raiz (ou dentro de `processor/`) com as chaves de API necessárias (veja `processor/.env.example`).

```bash
# Instale as dependências
pip install -r processor/requirements.txt

# Execute como módulo a partir da raiz do projeto
python3 -m processor.main
```

### 3. Entregador (Python)
Envia o boletim gerado para o Telegram.

**Configuração Prévia:**
Garanta que `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID` estejam no seu arquivo `.env`.

```bash
# Instale as dependências
pip install -r deliverer/requirements.txt

# Execute como módulo a partir da raiz do projeto
python3 -m deliverer.main --input output/bulletin.txt
```

---

*Nota: Para execução automatizada, consulte o workflow do GitHub Actions em `.github/workflows/daily_news.yml`.*
