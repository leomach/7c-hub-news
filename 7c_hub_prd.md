# 📰 Documento de Requisitos de Produto (PRD)
## Agregador de Notícias — 7C Hub
**Versão:** 1.0.0
**Data:** Março de 2026
**Status:** Em Definição
**Autor:** Comunidade 7C Hub

---

## Sumário

1. [Visão Geral e Contexto](#1-visão-geral-e-contexto)
2. [Objetivos e Métricas de Sucesso](#2-objetivos-e-métricas-de-sucesso)
3. [Personas e Casos de Uso](#3-personas-e-casos-de-uso)
4. [Arquitetura do Sistema](#4-arquitetura-do-sistema)
5. [Stack Tecnológica Detalhada](#5-stack-tecnológica-detalhada)
6. [Fontes de Dados](#6-fontes-de-dados)
7. [Requisitos Funcionais](#7-requisitos-funcionais)
8. [Requisitos Não Funcionais](#8-requisitos-não-funcionais)
9. [Modelo de Dados](#9-modelo-de-dados)
10. [Módulo Coletor (Go)](#10-módulo-coletor-go)
11. [Módulo Processador (Python)](#11-módulo-processador-python)
12. [Módulo Entregador (Python)](#12-módulo-entregador-python)
13. [Curadoria e Ranking com IA](#13-curadoria-e-ranking-com-ia)
14. [Formatação do Boletim](#14-formatação-do-boletim)
15. [Pipeline de Automação (CI/CD)](#15-pipeline-de-automação-cicd)
16. [Configuração e Extensibilidade](#16-configuração-e-extensibilidade)
17. [Tratamento de Erros e Resiliência](#17-tratamento-de-erros-e-resiliência)
18. [Segurança](#18-segurança)
19. [Estrutura de Diretórios do Repositório](#19-estrutura-de-diretórios-do-repositório)
20. [Roadmap e Fases de Entrega](#20-roadmap-e-fases-de-entrega)
21. [Glossário](#21-glossário)

---

## 1. Visão Geral e Contexto

### 1.1. Problema

A comunidade 7C Hub é formada por desenvolvedores, estudantes e entusiastas de tecnologia da região de Garanhuns e do agreste pernambucano. Manter-se atualizado sobre o ecossistema tech — que abrange tanto tendências globais quanto movimentações locais — é uma tarefa que exige tempo e esforço individual. Hoje, cada membro precisa consumir dezenas de fontes diferentes por conta própria, o que resulta em:

- **Fragmentação de informação:** Membros ficam desatualizados sobre acontecimentos relevantes.
- **Sobrecarga de feeds:** Excesso de notícias sem filtro ou curadoria relevante para o perfil da comunidade.
- **Desconexão regional:** Notícias de Pernambuco, Recife e Garanhuns raramente chegam de forma consolidada.
- **Barreira de idioma:** Grande parte do conteúdo técnico de ponta está em inglês, excluindo membros com menor proficiência.

### 1.2. Solução Proposta

O **7C Hub News** é um sistema de agregação, curadoria e distribuição automatizada de notícias de tecnologia. O sistema opera diariamente, coletando conteúdo de múltiplas fontes, aplicando inteligência artificial para tradução, resumo e ranqueamento por relevância, e entregando um boletim diário formatado para WhatsApp — o canal de comunicação principal da comunidade.

### 1.3. Escopo

**Dentro do escopo (v1.0):**
- Coleta automatizada de RSS feeds e APIs públicas
- Tradução automática de conteúdo em inglês
- Sumarização com IA
- Curadoria e ranqueamento por engajamento estimado
- Formatação otimizada para WhatsApp
- Entrega via bot no Telegram (canal privado do admin)
- Execução automatizada via GitHub Actions (segunda a sexta)

**Fora do escopo (v1.0):**
- Interface web ou painel administrativo
- Envio direto para WhatsApp (API oficial paga)
- Personalização de boletim por usuário
- Histórico pesquisável de notícias anteriores
- Aprendizado contínuo baseado em feedback dos leitores

---

## 2. Objetivos e Métricas de Sucesso

### 2.1. Objetivos de Negócio

| # | Objetivo | Descrição |
|---|----------|-----------|
| O1 | Engajamento da comunidade | Aumentar a frequência de interações no grupo de WhatsApp relacionadas a tecnologia |
| O2 | Acessibilidade de conteúdo | Eliminar a barreira do idioma inglês para notícias internacionais |
| O3 | Identidade regional | Fortalecer o senso de pertencimento ao ecossistema tech de Pernambuco |
| O4 | Custo zero | Operar exclusivamente com serviços gratuitos |
| O5 | Autonomia operacional | Funcionar sem intervenção manual diária |

### 2.2. KPIs (Key Performance Indicators)

| Métrica | Meta para v1.0 | Como medir |
|---------|----------------|------------|
| Taxa de entrega do boletim | ≥ 95% dos dias úteis | Logs do GitHub Actions |
| Tempo total de execução do pipeline | ≤ 3 minutos | Logs de tempo do Actions |
| Número de notícias curadas por boletim | 6 a 8 itens | Contagem no output final |
| Falhas de fonte recuperáveis | ≤ 2 fontes por execução sem interromper o pipeline | Logs de erro |
| Custo mensal de infraestrutura | R$ 0,00 | Monitoramento de uso das APIs |

---

## 3. Personas e Casos de Uso

### 3.1. Personas

**Persona 1 — O Admin (Curador)**
- Nome fictício: Lucas, 27 anos, líder técnico da comunidade 7C Hub
- Responsabilidades: Configurar o sistema, adicionar/remover fontes, monitorar falhas, copiar e colar o boletim no WhatsApp
- Necessidades: Um boletim pronto para uso, sem edição manual. Alertas rápidos em caso de falha.

**Persona 2 — O Membro Júnior**
- Nome fictício: Ana, 20 anos, estudante de ADS no IFPE Garanhuns
- Características: Lê em português, tem interesse em web dev e IA, não tem tempo para acompanhar feeds
- Necessidades: Conteúdo em português, linguagem acessível, resumos curtos e diretos

**Persona 3 — O Membro Sênior**
- Nome fictício: Carlos, 34 anos, desenvolvedor back-end com 10 anos de experiência
- Características: Lê inglês, quer profundidade técnica, se interessa por arquitetura de sistemas e open source
- Necessidades: Links originais para leitura completa, títulos fiéis ao conteúdo técnico

### 3.2. Casos de Uso Principais

**UC01 — Execução do Pipeline Diário**
- **Ator:** Sistema (GitHub Actions via Cron)
- **Fluxo:** O GitHub Actions dispara o workflow às 07h00 → Módulo Go coleta notícias → Módulo Python processa e curadora → Módulo Python entrega via Telegram
- **Pós-condição:** Boletim disponível no canal privado do Telegram

**UC02 — Admin publica o boletim**
- **Ator:** Admin (Lucas)
- **Fluxo:** Lucas recebe a mensagem no Telegram → Copia o texto → Cola no grupo do WhatsApp
- **Pré-condição:** Boletim entregue com sucesso pelo sistema

**UC03 — Admin adiciona nova fonte**
- **Ator:** Admin (Lucas)
- **Fluxo:** Lucas edita o arquivo `sources.yaml` adicionando a nova fonte com tipo, URL e categoria → Faz push para o repositório → Na próxima execução, a fonte é incluída automaticamente
- **Pós-condição:** Nova fonte ativa no próximo ciclo

**UC04 — Falha em fonte externa**
- **Ator:** Sistema
- **Fluxo:** Uma fonte retorna erro HTTP 5xx → O sistema loga o erro, marca a fonte como indisponível → O pipeline continua com as demais fontes → O boletim é gerado sem a fonte com falha → Um alerta é enviado ao admin via Telegram

---

## 4. Arquitetura do Sistema

### 4.1. Visão Macro

O sistema é composto por três módulos independentes executados em sequência dentro de um pipeline do GitHub Actions:

```
┌─────────────────────────────────────────────────────────┐
│                   GitHub Actions (Cron)                  │
│                 Seg-Sex, 07h00 (BRT)                    │
└─────────────────────┬───────────────────────────────────┘
                      │
          ┌───────────▼──────────┐
          │   MÓDULO COLETOR     │
          │       (Go)           │
          │                      │
          │  - RSS Feeds         │
          │  - APIs REST         │
          │  - Concorrência      │
          │  - Deduplicação      │
          │       ↓              │
          │   news.json          │
          └───────────┬──────────┘
                      │
          ┌───────────▼──────────┐
          │  MÓDULO PROCESSADOR  │
          │      (Python)        │
          │                      │
          │  - Lê news.json      │
          │  - Tradução (LLM)    │
          │  - Sumarização (LLM) │
          │  - Curadoria/Rank    │
          │  - Formatação WA     │
          │       ↓              │
          │  bulletin.txt        │
          └───────────┬──────────┘
                      │
          ┌───────────▼──────────┐
          │  MÓDULO ENTREGADOR   │
          │      (Python)        │
          │                      │
          │  - Lê bulletin.txt   │
          │  - Telegram Bot API  │
          │  - Alerta de erros   │
          └──────────────────────┘
```

### 4.2. Fluxo de Dados Detalhado

```
Fontes Externas
    │
    ├── RSS (XML)      ─┐
    ├── API JSON       ─┼──► Coletor (Go) ──► news.json
    └── Google Alerts  ─┘
                              │
                              ▼
                        Processador (Python)
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
              LLM API             Regras de Filtro
         (Tradução/Resumo)        (Data, Score, Dedup)
                    │                   │
                    └─────────┬─────────┘
                              │
                              ▼
                        bulletin.txt
                              │
                              ▼
                      Entregador (Python)
                              │
                              ▼
                       Telegram Bot API
                              │
                              ▼
                    Canal Privado do Admin
                              │
                              ▼
                    [Admin copia e cola]
                              │
                              ▼
                    Grupo WhatsApp 7C Hub
```

### 4.3. Comunicação entre Módulos

Os módulos se comunicam exclusivamente via arquivos no sistema de arquivos temporário do runner do GitHub Actions. Não há comunicação de rede entre módulos. Esta decisão garante:

- **Simplicidade:** Cada módulo pode ser testado isoladamente com fixtures
- **Rastreabilidade:** O arquivo intermediário `news.json` pode ser inspecionado em caso de debug
- **Independência de linguagem:** Go e Python não precisam de nenhum protocolo compartilhado

---

## 5. Stack Tecnológica Detalhada

### 5.1. Módulo Coletor — Go

| Componente | Tecnologia | Justificativa |
|-----------|------------|---------------|
| Linguagem | Go 1.22+ | Goroutines nativas para coleta concorrente; binário único sem dependências de runtime |
| Parser RSS | `github.com/mmcdole/gofeed` | Biblioteca consolidada que suporta RSS 1.0, 2.0 e Atom |
| HTTP Client | `net/http` nativo | Suficiente para o caso de uso; permite configurar timeouts facilmente |
| Serialização | `encoding/json` nativo | Sem dependência externa para escrita do `news.json` |
| Configuração | `gopkg.in/yaml.v3` | Leitura do arquivo `sources.yaml` |
| Logs | `log/slog` (stdlib) | Logging estruturado nativo do Go 1.21+ |

### 5.2. Módulo Processador — Python

| Componente | Tecnologia | Justificativa |
|-----------|------------|---------------|
| Linguagem | Python 3.11+ | Ecossistema rico para IA/LLM; bibliotecas maduras |
| Cliente LLM | `openai` SDK (compatível com Gemini) | SDK oficial; suporta múltiplos providers via configuração de `base_url` |
| Variáveis de ambiente | `python-dotenv` | Leitura segura de `.env` e GitHub Secrets |
| Configuração | `PyYAML` | Leitura do mesmo `sources.yaml` usado pelo coletor |
| Validação de dados | `pydantic` v2 | Tipagem e validação do schema do `news.json` |
| Utilitários de data | `python-dateutil` | Parse robusto de datas dos feeds (formatos variados) |
| Testes | `pytest` | Testes unitários dos módulos de processamento |

### 5.3. Módulo Entregador — Python

| Componente | Tecnologia | Justificativa |
|-----------|------------|---------------|
| Cliente Telegram | `python-telegram-bot` ou `httpx` puro | Simplicidade; apenas um `sendMessage` é necessário |
| Retry/Backoff | `tenacity` | Retry automático com backoff exponencial para falhas de rede |

### 5.4. Infraestrutura

| Componente | Tecnologia | Justificativa |
|-----------|------------|---------------|
| Automação | GitHub Actions | Free tier generoso (2.000 min/mês); integração nativa com repositório |
| Secrets | GitHub Encrypted Secrets | Armazenamento seguro de chaves de API |
| Versionamento | Git + GitHub | Controle de versão e histórico de mudanças nas configurações |
| Artefatos de Debug | GitHub Actions Artifacts | Upload opcional do `news.json` para inspeção |

### 5.5. Provedores de LLM (Intercambiáveis)

| Provider | Modelo Recomendado | Limite Gratuito | Endpoint Compatível |
|----------|--------------------|-----------------|---------------------|
| Google Gemini | `gemini-1.5-flash` | 1.500 req/dia | `generativelanguage.googleapis.com` |
| OpenAI | `gpt-4o-mini` | $5 de crédito inicial | `api.openai.com` |
| Groq | `llama-3.1-8b-instant` | 14.400 req/dia | `api.groq.com/openai/v1` |
| Mistral | `mistral-small-latest` | Tier gratuito disponível | `api.mistral.ai/v1` |

> **Nota de arquitetura:** O módulo processador usa a interface OpenAI-compatível para todos os providers. A troca de LLM é feita alterando apenas `LLM_PROVIDER`, `LLM_BASE_URL` e `LLM_MODEL` no arquivo de configuração, sem alterar o código.

---

## 6. Fontes de Dados

### 6.1. Fontes Internacionais (Inglês)

| # | Fonte | Tipo | URL / Endpoint | Prioridade |
|---|-------|------|----------------|------------|
| F01 | Hacker News Top Stories | API REST | `https://hacker-news.firebaseio.com/v0/topstories.json` | Alta |
| F02 | TechCrunch | RSS Feed | `https://techcrunch.com/feed/` | Alta |
| F03 | The Verge | RSS Feed | `https://www.theverge.com/rss/index.xml` | Alta |
| F04 | Dev.to (AI tag) | RSS Feed | `https://dev.to/feed/tag/ai` | Média |
| F05 | Dev.to (webdev tag) | RSS Feed | `https://dev.to/feed/tag/webdev` | Média |
| F06 | Medium (Software Engineering) | RSS Feed | `https://medium.com/feed/tag/software-engineering` | Baixa |
| F07 | GitHub Blog | RSS Feed | `https://github.blog/feed/` | Média |
| F08 | InfoQ | RSS Feed | `https://www.infoq.com/feed/?variant=rss` | Média |

**Hacker News — Detalhes de Coleta:**
1. Buscar array de IDs via `GET /v0/topstories.json` (retorna até 500 IDs)
2. Pegar os primeiros 30 IDs
3. Para cada ID, buscar `GET /v0/item/{id}.json` de forma concorrente (goroutines)
4. Filtrar apenas itens com `type: "story"` e com `url` preenchido
5. Usar `score` como critério de relevância

### 6.2. Fontes Nacionais (Português)

| # | Fonte | Tipo | URL / Endpoint | Prioridade |
|---|-------|------|----------------|------------|
| F09 | TabNews | API REST | `https://www.tabnews.com.br/api/v1/contents?strategy=relevant&per_page=15` | Alta |
| F10 | G1 Tecnologia | RSS Feed | `https://g1.globo.com/rss/g1/tecnologia/` | Alta |
| F11 | Tecnoblog | RSS Feed | `https://tecnoblog.net/feed/` | Média |
| F12 | Olhar Digital | RSS Feed | `https://olhardigital.com.br/feed/` | Baixa |
| F13 | Filipe Deschamps (YouTube) | RSS Feed | `https://www.youtube.com/feeds/videos.xml?channel_id=UCU5JicSrEM5A63jkJ2QvGYw` | Média |

**TabNews — Detalhes de Coleta:**
- A API REST retorna um array de objetos JSON com `title`, `slug`, `published_at`, `tabcoins` (equivalente a upvotes)
- Usar `tabcoins` como critério de relevância (similar ao score do HN)
- URL do conteúdo: `https://www.tabnews.com.br/{owner_username}/{slug}`

### 6.3. Fontes Regionais (Pernambuco / Garanhuns)

| # | Fonte | Tipo | URL / Endpoint | Prioridade |
|---|-------|------|----------------|------------|
| F14 | Google Alerts — Pernambuco Tech | RSS Feed | `https://www.google.com/alerts/feeds/{ID}/tecnologia-pernambuco` | Alta |
| F15 | Google Alerts — Garanhuns | RSS Feed | `https://www.google.com/alerts/feeds/{ID}/tecnologia-garanhuns` | Alta |
| F16 | Porto Digital (Blog) | RSS Feed | `https://www.portodigital.org/feed` | Média |
| F17 | Diario de Pernambuco (Tecnologia) | RSS Feed | `https://www.diariodepernambuco.com.br/tecnologia/rss` | Baixa |

**Configuração dos Google Alerts:**
Para cada alerta, criar uma query específica:
- Alerta 1: `"tecnologia" OR "inovação" OR "startup" ("Pernambuco" OR "Recife")`
- Alerta 2: `"tecnologia" OR "programação" OR "desenvolvimento" "Garanhuns"`
- Alerta 3: `"Porto Digital" OR "CESAR" OR "SOFTEX"`

> **Observação:** Os feeds do Google Alerts necessitam de criação manual pelo admin. O ID do feed é único por conta Google. O link do RSS deve ser obtido pelo admin e adicionado ao `sources.yaml`.

### 6.4. Categorias e Cotas por Boletim

| Categoria | Cota Padrão | Cota Mínima | Descrição |
|-----------|-------------|-------------|-----------|
| Global | 3 notícias | 2 | Fontes internacionais (F01–F08) |
| Nacional | 2 notícias | 1 | Fontes nacionais (F09–F13) |
| Regional | 1 notícia | 0 | Fontes regionais (F14–F17) |
| **Total** | **6 notícias** | **3** | Mínimo para publicação do boletim |

> Se uma categoria não atingir a cota mínima (ex: sem notícias regionais no dia), o sistema preenche com notícias da categoria de maior prioridade disponível e registra um aviso no log.

---

## 7. Requisitos Funcionais

### RF01 — Coleta de Conteúdo

**Descrição:** O sistema deve consumir feeds RSS (formato XML) e APIs REST (formato JSON) para extrair, no mínimo, os seguintes campos de cada notícia:
- `title` (string, obrigatório)
- `url` (string, obrigatório, válido)
- `published_at` (datetime com timezone, obrigatório)
- `source_name` (string, nome da fonte)
- `source_category` (enum: `global | national | regional`)
- `summary` (string, opcional — texto de prévia disponível no feed)
- `relevance_score` (float, calculado pelo coletor)

**Critérios de aceite:**
- O coletor deve processar todas as fontes ativas em paralelo (goroutines)
- Timeout por fonte: 10 segundos
- Fontes com falha não devem interromper o processamento das demais
- O arquivo `news.json` deve ser salvo mesmo em caso de falha parcial

---

### RF02 — Filtro Temporal

**Descrição:** O sistema deve priorizar notícias publicadas nas últimas 24 horas. Notícias com mais de 48 horas devem ser descartadas.

**Regras detalhadas:**
- Janela primária: 0–24h → incluídas com prioridade total
- Janela secundária: 24h–48h → incluídas apenas se necessário para completar a cota mínima
- Acima de 48h: descartadas incondicionalmente
- Referência de tempo: `UTC-3 (BRT)` no momento da execução

**Critérios de aceite:**
- Notícias sem data de publicação devem ser descartadas (campo `published_at` ausente ou malformado)
- O filtro deve ser aplicado antes de qualquer chamada à LLM para economizar tokens

---

### RF03 — Tradução Automática

**Descrição:** O sistema deve detectar o idioma de cada notícia e traduzir automaticamente títulos e resumos das fontes em inglês para português brasileiro.

**Regras detalhadas:**
- Detecção de idioma: verificar o campo `source_language` no `sources.yaml`; se ausente, assumir `en` para fontes globais e `pt` para nacionais/regionais
- Tradução: feita via prompt para a LLM configurada
- Conteúdo já em português: não deve ser enviado para tradução (economia de tokens)
- Nomes próprios, termos técnicos e nomes de produtos devem ser preservados na língua original (ex: "React", "OpenAI", "GitHub Copilot")

**Prompt de tradução (template):**
```
Traduza o seguinte título e resumo de notícia de tecnologia para português brasileiro.
Preserve nomes próprios, termos técnicos e nomes de produtos em inglês.
Retorne SOMENTE um JSON com os campos "title" e "summary", sem explicações adicionais.

Título original: {title}
Resumo original: {summary}
```

**Critérios de aceite:**
- A tradução deve ser realizada em batch (múltiplos itens por chamada) para minimizar o número de requisições à LLM
- Em caso de falha na tradução de um item, usar o texto original (fallback)

---

### RF04 — Sumarização

**Descrição:** O sistema deve gerar um resumo em português de no máximo 2 frases (aproximadamente 280 caracteres) para cada notícia curada.

**Regras detalhadas:**
- O resumo deve ser gerado pela LLM a partir do título + prévia disponível no feed
- Tom: informativo, objetivo, sem clickbait
- Público-alvo: desenvolvedor de software com nível júnior a sênior
- O resumo deve responder: "O que aconteceu e por que isso importa para um dev?"

**Prompt de sumarização (template):**
```
Você é um curador de notícias de tecnologia para uma comunidade de desenvolvedores brasileiros.
Gere um resumo de no máximo 2 frases (máx 280 caracteres) para a notícia abaixo.
O resumo deve ser informativo, objetivo e relevante para desenvolvedores de software.
Responda SOMENTE com o texto do resumo, sem introdução nem aspas.

Título: {title}
Prévia: {summary_or_description}
```

**Critérios de aceite:**
- Resumo não deve ultrapassar 300 caracteres
- Se o resumo gerado ultrapassar o limite, truncar na última frase completa
- O resumo não deve começar com "Esta notícia" ou "Neste artigo"

---

### RF05 — Formatação para WhatsApp

**Descrição:** O sistema deve gerar um texto final formatado com a sintaxe de rich text do WhatsApp, pronto para cópia e cola sem edição manual.

**Regras detalhadas:**
- Negrito: `*texto*`
- Itálico: `_texto_`
- Código: `` `código` ``
- Não usar Markdown padrão (`**`, `__`, `##`) — incompatível com WhatsApp
- Limite total da mensagem: ≤ 3.500 caracteres (evitar truncamento pelo WhatsApp)
- Emojis padronizados por categoria (ver seção 14)

**Critérios de aceite:**
- A mensagem deve ser testada manualmente pelo admin antes do primeiro deploy em produção
- O sistema deve calcular o comprimento da mensagem final e logar um aviso se ultrapassar 3.000 caracteres

---

### RF06 — Entrega via Telegram

**Descrição:** O sistema deve enviar a mensagem processada para um chat específico do Telegram via Bot API.

**Regras detalhadas:**
- Método: `POST https://api.telegram.org/bot{TOKEN}/sendMessage`
- Parâmetros obrigatórios: `chat_id`, `text`, `parse_mode: "HTML"` ou `"MarkdownV2"`
- O token do bot deve ser lido de variável de ambiente (`TELEGRAM_BOT_TOKEN`)
- O chat ID deve ser lido de variável de ambiente (`TELEGRAM_CHAT_ID`)
- Timeout da requisição: 15 segundos
- Retry: até 3 tentativas com backoff exponencial (2s, 4s, 8s)

**Critérios de aceite:**
- Uma mensagem de sucesso deve ser logada após confirmação da API do Telegram
- Em caso de falha após 3 tentativas, o job do GitHub Actions deve terminar com exit code 1 (falha visível no painel do Actions)

---

### RF07 — Curadoria Inteligente com IA

**Descrição:** O sistema deve usar a LLM para pontuar e ranquear as notícias coletadas, selecionando as que têm maior potencial de engajamento para o perfil da comunidade 7C Hub.

**Perfil da comunidade para curadoria:**
- Desenvolvedores back-end, front-end e fullstack
- Estudantes de computação (IFPE, UPE, UFPE)
- Interesse em: IA/ML, web dev, open source, mercado de trabalho tech, ecossistema local
- Temas de alto engajamento: lançamentos de ferramentas, controvérsias do setor, oportunidades de emprego/carreira, novidades do ecossistema local

**Regras de ranqueamento:**

Score final de cada notícia = `(score_llm × 0.4) + (score_fonte × 0.3) + (score_temporal × 0.2) + (score_original × 0.1)`

Onde:
- `score_llm`: 1–10, retornado pela LLM (relevância para o perfil da comunidade)
- `score_fonte`: peso fixo por fonte (ex: HN Top = 1.0, G1 = 0.8, fonte regional = 1.2)
- `score_temporal`: 1.0 se < 12h, 0.8 se 12–24h, 0.5 se 24–48h
- `score_original`: normalização do score nativo da fonte (HN score, TabCoins) para 0–1

**Prompt de curadoria (template):**
```
Você é curador de notícias para uma comunidade de desenvolvedores de software do interior de Pernambuco, Brasil.
Avalie as notícias abaixo e atribua uma nota de 1 a 10 para cada uma, considerando:
- Relevância técnica para desenvolvedores (back-end, front-end, IA, infraestrutura)
- Novidade e impacto no mercado de tecnologia
- Interesse para estudantes e profissionais em início de carreira
- Conexão com o ecossistema tech brasileiro ou nordestino (bônus se houver)

Retorne SOMENTE um JSON array, onde cada objeto contém "id" e "score". Sem explicações.

Notícias:
{json_news_list}
```

---

### RF08 — Deduplicação

**Descrição:** O sistema deve detectar e remover notícias duplicadas ou muito similares antes do processamento pela LLM.

**Regras:**
- Duas notícias são consideradas duplicatas se:
  - Têm a mesma URL (após normalização: remover parâmetros UTM, trailing slash)
  - Têm títulos com similaridade > 85% (usando algoritmo de Levenshtein ou similaridade de cosseno com TF-IDF simples)
- Em caso de duplicata, manter a versão da fonte com maior prioridade

---

### RF09 — Notificação de Erros ao Admin

**Descrição:** Em caso de falha crítica no pipeline, o sistema deve enviar uma notificação de erro ao admin via Telegram, antes de encerrar.

**Erros críticos (que bloqueiam o boletim):**
- Falha na API da LLM após todos os retries
- Número de notícias coletadas abaixo do mínimo absoluto (< 3)
- Falha no envio da mensagem ao Telegram após todos os retries

**Formato da notificação de erro:**
```
⚠️ *7C Hub News — Erro no Pipeline*

Data: {data_hora}
Etapa: {nome_do_modulo}
Erro: {mensagem_de_erro_resumida}

Verifique os logs do GitHub Actions:
{link_para_o_run}
```

---

## 8. Requisitos Não Funcionais

### RNF01 — Custo Zero

- Todas as APIs externas devem ser utilizadas dentro dos tiers gratuitos
- O GitHub Actions free tier (2.000 min/mês para repositórios públicos) é suficiente para ~22 execuções/mês de ≤ 3 min cada (= 66 min/mês)
- Nenhuma dependência de serviços pagos de terceiros (ex: sem Heroku pago, sem AWS)
- Monitoramento mensal de uso das APIs pelo admin

### RNF02 — Automação e Confiabilidade

- O pipeline deve executar automaticamente de segunda a sexta, às 07h00 BRT (10h00 UTC)
- A janela de tolerância de atraso é de ±30 minutos (variação natural do scheduler do GitHub Actions)
- O sistema não deve exigir qualquer intervenção manual para execuções bem-sucedidas
- Logs de execução devem ser mantidos pelo menos 30 dias (retenção padrão do GitHub Actions)

### RNF03 — Manutenibilidade e Extensibilidade

- **Adição de fonte:** Requer apenas edição do `sources.yaml`, sem alteração de código
- **Troca de LLM:** Requer apenas alteração de 3 variáveis de ambiente (`LLM_PROVIDER`, `LLM_BASE_URL`, `LLM_MODEL`)
- **Ajuste de cotas:** Configurável via `sources.yaml` (campo `quotas`)
- **Ajuste de prompts:** Configurável via arquivos `.txt` em `config/prompts/`, sem alterar código Python
- **Cobertura de testes:** ≥ 70% nas funções críticas do processador (tradução, curadoria, formatação)

### RNF04 — Performance

- Tempo máximo de execução total do pipeline: 5 minutos
- Módulo Coletor (Go): ≤ 60 segundos para todas as fontes
- Módulo Processador (Python): ≤ 3 minutos (inclui chamadas à LLM)
- Módulo Entregador (Python): ≤ 30 segundos

### RNF05 — Observabilidade

- Cada módulo deve logar: início, fim, duração, número de itens processados e erros encontrados
- O formato de log deve ser estruturado (JSON lines) para facilitar filtragem no GitHub Actions
- Os artefatos `news.json` e `bulletin.txt` devem ser disponibilizados como artefatos do GitHub Actions para debug (retenção de 7 dias)

### RNF06 — Segurança

- Nenhuma chave de API deve ser commitada no repositório
- Todas as credenciais devem ser armazenadas como GitHub Encrypted Secrets
- O repositório pode ser público (o código não contém dados sensíveis)
- O `TELEGRAM_CHAT_ID` do canal privado do admin é sensível e deve ser tratado como secret

---

## 9. Modelo de Dados

### 9.1. Schema do `news.json`

```json
{
  "generated_at": "2026-03-25T10:00:00Z",
  "pipeline_version": "1.0.0",
  "sources_attempted": 17,
  "sources_succeeded": 15,
  "total_raw_items": 142,
  "items": [
    {
      "id": "hn-43210987",
      "title": "Announcing Rust 2.0: What's New",
      "url": "https://blog.rust-lang.org/2026/03/25/rust-2.html",
      "published_at": "2026-03-25T08:30:00Z",
      "source_id": "hackernews",
      "source_name": "Hacker News",
      "source_category": "global",
      "source_language": "en",
      "original_score": 847,
      "summary_original": "The Rust programming language team announced version 2.0...",
      "title_pt": null,
      "summary_pt": null,
      "llm_score": null,
      "final_score": null,
      "selected": false,
      "processing_status": "raw"
    }
  ],
  "errors": [
    {
      "source_id": "medium-sw-eng",
      "error_type": "timeout",
      "message": "Request timed out after 10s",
      "timestamp": "2026-03-25T10:00:45Z"
    }
  ]
}
```

### 9.2. Schema do `bulletin.txt`

Arquivo de texto plano contendo a mensagem final formatada para WhatsApp, incluindo um cabeçalho de metadados comentado:

```
# 7C Hub News — 2026-03-25
# Itens: 6 | Global: 3 | Nacional: 2 | Regional: 1
# Chars: 2847 | LLM: gemini-1.5-flash | Duração: 127s
---
[MENSAGEM FORMATADA PARA WHATSAPP ABAIXO]
```

---

## 10. Módulo Coletor (Go)

### 10.1. Estrutura de Pacotes

```
collector/
├── main.go               # Entry point; orquestra a coleta
├── config/
│   └── loader.go         # Carrega e valida o sources.yaml
├── fetcher/
│   ├── rss.go            # Coleta e parseia feeds RSS/Atom
│   ├── rest.go           # Coleta APIs REST (HN, TabNews)
│   └── hackernews.go     # Lógica específica do HN (busca paralela de items)
├── model/
│   └── news_item.go      # Struct NewsItem e métodos de normalização
├── dedup/
│   └── dedup.go          # Deduplicação por URL
├── output/
│   └── writer.go         # Serializa para news.json
└── go.mod
```

### 10.2. Fluxo de Execução do Coletor

1. Carregar `sources.yaml`; falhar rápido se inválido
2. Criar um `chan NewsItem` com buffer de 500
3. Para cada fonte ativa no YAML, lançar uma goroutine com `go fetch(source, ch, wg)`
4. Aguardar todas as goroutines com `wg.Wait()`, depois fechar o canal
5. Coletar todos os itens do canal
6. Aplicar filtro temporal (remover itens > 48h)
7. Aplicar deduplicação por URL normalizada
8. Calcular `original_score` normalizado por fonte
9. Serializar e salvar em `output/news.json`
10. Logar sumário: `fontes_tentadas`, `fontes_ok`, `fontes_erro`, `itens_coletados`, `itens_apos_filtro`

### 10.3. Configuração de Fontes (sources.yaml)

```yaml
# sources.yaml
metadata:
  version: "1.0"
  last_updated: "2026-03-25"

settings:
  max_age_hours: 48
  fetch_timeout_seconds: 10
  max_concurrent_fetches: 10

quotas:
  global: 3
  national: 2
  regional: 1
  minimum_total: 3

sources:
  - id: hackernews
    name: "Hacker News"
    type: rest_hackernews
    enabled: true
    category: global
    language: en
    weight: 1.0
    config:
      top_stories_limit: 30

  - id: techcrunch
    name: "TechCrunch"
    type: rss
    enabled: true
    category: global
    language: en
    weight: 0.9
    url: "https://techcrunch.com/feed/"
    config:
      max_items: 10

  - id: tabnews
    name: "TabNews"
    type: rest_tabnews
    enabled: true
    category: national
    language: pt
    weight: 1.0
    config:
      strategy: relevant
      per_page: 15

  - id: google_alerts_pernambuco
    name: "Google Alerts — Pernambuco Tech"
    type: rss
    enabled: true
    category: regional
    language: pt
    weight: 1.2
    url: "https://www.google.com/alerts/feeds/XXXXXX/YYYYYY"
    config:
      max_items: 5

llm:
  provider: "gemini"
  base_url: "https://generativelanguage.googleapis.com/v1beta/openai"
  model: "gemini-1.5-flash"
  max_tokens: 1000
  temperature: 0.3

prompts_dir: "config/prompts/"
```

---

## 11. Módulo Processador (Python)

### 11.1. Estrutura de Pacotes

```
processor/
├── main.py                  # Entry point; orquestra o processamento
├── config/
│   └── settings.py          # Pydantic Settings; lê .env e sources.yaml
├── models/
│   └── news_item.py         # Pydantic models para NewsItem e NewsOutput
├── llm/
│   ├── client.py            # Cliente LLM genérico (OpenAI-compatible)
│   ├── translator.py        # Lógica de tradução em batch
│   ├── summarizer.py        # Lógica de sumarização
│   └── curator.py           # Lógica de ranqueamento/curadoria
├── pipeline/
│   ├── filter.py            # Filtro temporal e de qualidade
│   ├── dedup.py             # Deduplicação por similaridade de título
│   ├── ranker.py            # Cálculo do score final e seleção
│   └── formatter.py         # Formatação do boletim para WhatsApp
├── prompts/                 # Templates de prompts (arquivos .txt)
│   ├── translate.txt
│   ├── summarize.txt
│   └── curate.txt
├── tests/
│   ├── test_filter.py
│   ├── test_formatter.py
│   └── fixtures/
│       └── sample_news.json
├── requirements.txt
└── .env.example
```

### 11.2. Arquivo `.env.example`

```env
# LLM Configuration
LLM_PROVIDER=gemini
LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai
LLM_MODEL=gemini-1.5-flash
LLM_API_KEY=your_api_key_here

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Pipeline
INPUT_FILE=output/news.json
OUTPUT_FILE=output/bulletin.txt
LOG_LEVEL=INFO
```

### 11.3. Pipeline de Processamento (main.py)

```python
# Pseudocódigo do fluxo principal
def main():
    settings = load_settings()
    news_items = load_news_json(settings.input_file)
    
    # Etapa 1: Filtros iniciais (sem LLM)
    items = filter_by_age(news_items, max_hours=48)
    items = deduplicate_by_url(items)
    items = deduplicate_by_title_similarity(items, threshold=0.85)
    
    log(f"Após filtros: {len(items)} itens")
    
    # Etapa 2: Tradução (apenas itens em inglês)
    items_en = [i for i in items if i.source_language == "en"]
    items_pt = [i for i in items if i.source_language == "pt"]
    translated = batch_translate(items_en, llm_client)
    items = translated + items_pt
    
    # Etapa 3: Curadoria com LLM
    items = llm_curate_and_score(items, llm_client)
    
    # Etapa 4: Sumarização dos top candidatos
    top_candidates = select_top_candidates(items, quota_multiplier=2)
    top_candidates = batch_summarize(top_candidates, llm_client)
    
    # Etapa 5: Seleção final por cota e score
    selected = select_by_quota(top_candidates, quotas=settings.quotas)
    
    # Etapa 6: Formatação
    bulletin = format_bulletin(selected, date=today())
    
    # Etapa 7: Salvar
    save_bulletin(bulletin, settings.output_file)
    log_summary(selected)
```

---

## 12. Módulo Entregador (Python)

### 12.1. Estrutura

```
deliverer/
├── main.py          # Entry point; lê bulletin.txt e envia
├── telegram.py      # Wrapper da Telegram Bot API
└── requirements.txt # Apenas httpx e tenacity
```

### 12.2. Lógica de Envio

- O Telegram limita mensagens a 4.096 caracteres
- Se `bulletin.txt` ultrapassar 4.000 caracteres, o entregador deve dividir em partes e enviar como mensagens sequenciais no mesmo chat
- Cada parte deve ser identificada no cabeçalho: `*7C Hub News (1/2)*`

### 12.3. Telegram Bot — Setup

1. Criar bot via `@BotFather` no Telegram → obtém `BOT_TOKEN`
2. Criar canal ou grupo privado
3. Adicionar o bot ao canal/grupo como administrador
4. Obter o `CHAT_ID` via `GET /getUpdates` após enviar uma mensagem no canal
5. Adicionar ambos como GitHub Secrets

---

## 13. Curadoria e Ranking com IA

### 13.1. Estratégia de Curadoria em Duas Camadas

**Camada 1 — Filtros Heurísticos (sem LLM, no coletor):**
- Filtro temporal: 0–48h
- Score mínimo nativo: HN score > 50, TabCoins > 5
- Filtro de domínio: bloquear domínios de baixa qualidade (lista negra em `sources.yaml`)
- Filtro de comprimento de título: mínimo 20, máximo 200 caracteres

**Camada 2 — Ranqueamento por LLM (no processador):**
- Avaliar a lista filtrada (até 50 itens) em uma única chamada batch
- Obter score 1–10 por item
- Calcular score final ponderado (fórmula na seção RF07)
- Selecionar candidatos por cota (top 2× da cota por categoria, depois filtrar para o boletim)

### 13.2. Categorias de Alto Engajamento (para o perfil da comunidade)

A LLM deve pontuar mais alto notícias sobre:
- Lançamentos de linguagens de programação, frameworks ou ferramentas populares
- Mudanças em plataformas usadas por devs (GitHub, npm, Docker Hub, Vercel)
- Notícias sobre IA generativa aplicada ao desenvolvimento de software
- Oportunidades de emprego e mercado de trabalho tech no Brasil
- Controvérsias e debates técnicos da comunidade dev (ex: "Is X dead?")
- Projetos open source com grande tração
- Notícias sobre ecossistema tech de Pernambuco, Recife ou Garanhuns

---

## 14. Formatação do Boletim

### 14.1. Template do Boletim

```
🗞 *7C Hub News* — {dia_da_semana}, {data_formatada}
━━━━━━━━━━━━━━━━━━━━

🌍 *MUNDO*

1️⃣ *{titulo_noticia_1}*
_{resumo_em_2_frases}_
🔗 {url_curta}

2️⃣ *{titulo_noticia_2}*
_{resumo_em_2_frases}_
🔗 {url_curta}

3️⃣ *{titulo_noticia_3}*
_{resumo_em_2_frases}_
🔗 {url_curta}

━━━━━━━━━━━━━━━━━━━━
🇧🇷 *BRASIL*

4️⃣ *{titulo_noticia_4}*
_{resumo_em_2_frases}_
🔗 {url_curta}

5️⃣ *{titulo_noticia_5}*
_{resumo_em_2_frases}_
🔗 {url_curta}

━━━━━━━━━━━━━━━━━━━━
📍 *PERNAMBUCO & REGIÃO*

6️⃣ *{titulo_noticia_6}*
_{resumo_em_2_frases}_
🔗 {url_curta}

━━━━━━━━━━━━━━━━━━━━
_Boletim gerado automaticamente pelo 7C Hub News Bot_ 🤖
```

### 14.2. Regras de Formatação

| Elemento | Formato WhatsApp | Exemplo |
|----------|-----------------|---------|
| Título da seção | `*TEXTO EM MAIÚSCULO*` | `*MUNDO*` |
| Título da notícia | `*Título da Notícia*` | `*Rust 2.0 é anunciado*` |
| Resumo | `_texto em itálico_` | `_O time do Rust anunciou..._` |
| Separador | `━━━━━━━━━━━━━━━━━━━━` | — |
| Link | URL completa sem markdown | `https://...` |
| Numeração | Emojis numéricos | `1️⃣ 2️⃣ ... 6️⃣` |

### 14.3. Data em Português

```python
DIAS_SEMANA = {
    0: "Segunda-feira", 1: "Terça-feira", 2: "Quarta-feira",
    3: "Quinta-feira", 4: "Sexta-feira"
}
MESES = {
    1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril",
    5: "maio", 6: "junho", 7: "julho", 8: "agosto",
    9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro"
}
# Exemplo: "Terça-feira, 25 de março de 2026"
```

---

## 15. Pipeline de Automação (CI/CD)

### 15.1. Arquivo `.github/workflows/daily_news.yml`

```yaml
name: 7C Hub Daily News

on:
  schedule:
    - cron: '0 10 * * 1-5'  # 10:00 UTC = 07:00 BRT, Seg-Sex
  workflow_dispatch:          # Permite execução manual (útil para testes)

env:
  GO_VERSION: '1.22'
  PYTHON_VERSION: '3.11'

jobs:
  collect:
    name: 📡 Coletar Notícias
    runs-on: ubuntu-latest
    outputs:
      news_count: ${{ steps.collect.outputs.news_count }}
    steps:
      - uses: actions/checkout@v4

      - name: Setup Go
        uses: actions/setup-go@v5
        with:
          go-version: ${{ env.GO_VERSION }}
          cache: true

      - name: Build e Executar Coletor
        id: collect
        run: |
          cd collector
          go build -o ../bin/collector .
          cd ..
          ./bin/collector --config sources.yaml --output output/news.json
          echo "news_count=$(cat output/news.json | python3 -c 'import sys,json; d=json.load(sys.stdin); print(len(d["items"]))')" >> $GITHUB_OUTPUT

      - name: Upload news.json como Artefato
        uses: actions/upload-artifact@v4
        with:
          name: news-json-${{ github.run_id }}
          path: output/news.json
          retention-days: 7

  process:
    name: 🧠 Processar com IA
    runs-on: ubuntu-latest
    needs: collect
    steps:
      - uses: actions/checkout@v4

      - name: Download news.json
        uses: actions/download-artifact@v4
        with:
          name: news-json-${{ github.run_id }}
          path: output/

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'

      - name: Instalar dependências
        run: pip install -r processor/requirements.txt

      - name: Executar Processador
        env:
          LLM_API_KEY: ${{ secrets.LLM_API_KEY }}
          LLM_BASE_URL: ${{ secrets.LLM_BASE_URL }}
          LLM_MODEL: ${{ secrets.LLM_MODEL }}
        run: python processor/main.py --input output/news.json --output output/bulletin.txt

      - name: Upload bulletin.txt como Artefato
        uses: actions/upload-artifact@v4
        with:
          name: bulletin-${{ github.run_id }}
          path: output/bulletin.txt
          retention-days: 7

  deliver:
    name: 📨 Enviar para Telegram
    runs-on: ubuntu-latest
    needs: process
    steps:
      - uses: actions/checkout@v4

      - name: Download bulletin.txt
        uses: actions/download-artifact@v4
        with:
          name: bulletin-${{ github.run_id }}
          path: output/

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'

      - name: Instalar dependências
        run: pip install -r deliverer/requirements.txt

      - name: Enviar Boletim
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        run: python deliverer/main.py --input output/bulletin.txt

  notify_failure:
    name: 🚨 Notificar Falha
    runs-on: ubuntu-latest
    needs: [collect, process, deliver]
    if: failure()
    steps:
      - uses: actions/checkout@v4
      - name: Enviar alerta de falha
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
          GITHUB_RUN_URL: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
        run: python deliverer/notify_failure.py
```

---

## 16. Configuração e Extensibilidade

### 16.1. Como Adicionar uma Nova Fonte

1. Abrir `sources.yaml`
2. Adicionar um novo objeto na lista `sources`:
```yaml
- id: minha_nova_fonte
  name: "Nome da Fonte"
  type: rss            # ou rest_custom
  enabled: true
  category: national   # global | national | regional
  language: pt         # en | pt
  weight: 0.8
  url: "https://exemplo.com/feed.xml"
  config:
    max_items: 10
```
3. Fazer `git commit` e `git push`
4. A nova fonte será incluída na próxima execução

### 16.2. Como Trocar a LLM

Alterar os GitHub Secrets (sem alterar código):
- `LLM_API_KEY`: nova chave de API
- `LLM_BASE_URL`: endpoint base da nova LLM (compatível com OpenAI)
- `LLM_MODEL`: nome do modelo

**Exemplos de configuração por provider:**

| Provider | LLM_BASE_URL | LLM_MODEL |
|----------|-------------|-----------|
| Gemini | `https://generativelanguage.googleapis.com/v1beta/openai` | `gemini-1.5-flash` |
| Groq | `https://api.groq.com/openai/v1` | `llama-3.1-8b-instant` |
| OpenAI | `https://api.openai.com/v1` | `gpt-4o-mini` |
| Mistral | `https://api.mistral.ai/v1` | `mistral-small-latest` |

### 16.3. Como Ajustar os Prompts

Os prompts ficam em arquivos `.txt` em `processor/prompts/`. Para ajustar o comportamento da IA:
1. Editar o arquivo `.txt` correspondente (`translate.txt`, `summarize.txt`, `curate.txt`)
2. As variáveis são substituídas com a sintaxe `{variavel}`
3. Fazer commit e push

---

## 17. Tratamento de Erros e Resiliência

### 17.1. Estratégia por Tipo de Falha

| Falha | Impacto | Estratégia |
|-------|---------|------------|
| Fonte RSS indisponível | Uma fonte a menos | Log + continuar; sem interrupção |
| API do HN lenta | Coleta parcial do HN | Timeout de 10s por item; usar apenas os coletados |
| Rate limit da LLM | Processamento pausado | Retry com backoff exponencial (3 tentativas) |
| Falha total da LLM | Sem resumos nem curadoria | Fallback: usar título original + prévia do feed |
| Boletim abaixo do mínimo | Não publicar | Enviar alerta ao admin e encerrar com falha |
| Telegram indisponível | Boletim não entregue | Retry 3x; encerrar com falha e logar |

### 17.2. Fallback de Sumarização

Quando a LLM falha, o processador usa o campo `summary_original` do feed (geralmente os primeiros 200 caracteres da descrição do item). Se não existir, usa apenas o título. O boletim é marcado com `⚠️ _Boletim gerado sem IA (modo fallback)_`.

---

## 18. Segurança

### 18.1. Gestão de Secrets

| Secret | Onde armazenar | Quem tem acesso |
|--------|----------------|-----------------|
| `LLM_API_KEY` | GitHub Encrypted Secret | Apenas o runner do Actions |
| `TELEGRAM_BOT_TOKEN` | GitHub Encrypted Secret | Apenas o runner do Actions |
| `TELEGRAM_CHAT_ID` | GitHub Encrypted Secret | Apenas o runner do Actions |

### 18.2. Proteção do Código

- O repositório pode ser **público** — o código não contém nenhuma informação sensível
- O arquivo `.env` deve estar no `.gitignore`
- O arquivo `.env.example` deve ser commitado (sem valores reais)
- PRs de terceiros não têm acesso aos secrets (comportamento padrão do GitHub)

### 18.3. Validação de Inputs

- URLs das fontes devem ser validadas no `sources.yaml` antes da execução (evitar SSRF)
- O conteúdo dos feeds é tratado como dado não-confiável; apenas campos específicos são extraídos
- Nenhum código externo é executado a partir do conteúdo das notícias

---

## 19. Estrutura de Diretórios do Repositório

```
7c-hub-news/
├── .github/
│   └── workflows/
│       └── daily_news.yml
├── collector/               # Módulo Go
│   ├── main.go
│   ├── config/
│   ├── fetcher/
│   ├── model/
│   ├── dedup/
│   ├── output/
│   └── go.mod
├── processor/               # Módulo Python (processamento com IA)
│   ├── main.py
│   ├── config/
│   ├── models/
│   ├── llm/
│   ├── pipeline/
│   ├── prompts/
│   │   ├── translate.txt
│   │   ├── summarize.txt
│   │   └── curate.txt
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
├── deliverer/               # Módulo Python (entrega via Telegram)
│   ├── main.py
│   ├── telegram.py
│   ├── notify_failure.py
│   └── requirements.txt
├── output/                  # Arquivos intermediários (gerados, no .gitignore)
│   ├── news.json
│   └── bulletin.txt
├── sources.yaml             # ⭐ Arquivo central de configuração
├── .gitignore
├── README.md
└── CONTRIBUTING.md
```

---

## 20. Roadmap e Fases de Entrega

### Fase 1 — MVP (2–3 semanas)

**Objetivo:** Pipeline funcional de ponta a ponta, mesmo que manual.

- [ ] Setup do repositório e estrutura de diretórios
- [ ] `sources.yaml` com fontes iniciais (HN, TechCrunch, TabNews, G1, Google Alerts)
- [ ] Módulo Coletor Go: RSS + API HN + API TabNews
- [ ] Módulo Processador Python: tradução + sumarização (sem curadoria por LLM ainda)
- [ ] Módulo Entregador Python: envio via Telegram
- [ ] GitHub Actions workflow básico (trigger manual + cron)
- [ ] Teste end-to-end com execução manual

**Critério de conclusão:** Boletim chegando no Telegram, sendo colado no WhatsApp e fazendo sentido.

---

### Fase 2 — Curadoria e Qualidade (1–2 semanas)

**Objetivo:** Implementar a curadoria inteligente e melhorar a qualidade do conteúdo.

- [ ] Implementar RF07: curadoria com LLM e score final ponderado
- [ ] Implementar deduplicação por similaridade de título (RF08)
- [ ] Implementar notificações de erro (RF09)
- [ ] Adicionar testes unitários para `filter.py` e `formatter.py`
- [ ] Ajuste fino dos prompts baseado em feedback da comunidade

**Critério de conclusão:** Curadoria notavelmente melhor em relação à Fase 1; zero erros silenciosos.

---

### Fase 3 — Robustez e Manutenibilidade (1 semana)

**Objetivo:** Sistema pronto para operar de forma autônoma por meses sem intervenção.

- [ ] Implementar fallback de sumarização (sem LLM)
- [ ] Tratamento completo de todos os tipos de falha (seção 17)
- [ ] Documentação completa do README e CONTRIBUTING
- [ ] Validação do `sources.yaml` via schema ao iniciar o coletor
- [ ] Logs estruturados em JSON lines em todos os módulos

**Critério de conclusão:** Pipeline executa 5 dias seguidos sem falha e com boletins de qualidade.

---

### Fase 4 — Evoluções Futuras (backlog)

| Feature | Prioridade | Complexidade |
|---------|------------|--------------|
| Painel web de configuração simples | Baixa | Alta |
| Envio direto no WhatsApp (via Baileys/WPPConnect) | Média | Alta |
| Histórico de boletins em GitHub Pages | Média | Baixa |
| Feedback da comunidade via reações no Telegram | Baixa | Média |
| Personalização de tópicos por membro | Baixa | Alta |
| Detecção automática de novas fontes regionais | Baixa | Alta |

---

## 21. Glossário

| Termo | Definição |
|-------|-----------|
| **RSS** | Really Simple Syndication — formato XML para distribuição de conteúdo atualizado de sites |
| **Feed** | Fluxo de conteúdo publicado por uma fonte em formato RSS ou Atom |
| **LLM** | Large Language Model — modelo de linguagem de grande escala (ex: Gemini, GPT-4) |
| **Pipeline** | Sequência de etapas automatizadas de processamento de dados |
| **Curadoria** | Processo de seleção e organização de conteúdo com base em critérios de qualidade e relevância |
| **Boletim** | Mensagem compilada com as notícias selecionadas, formatada para WhatsApp |
| **Score** | Pontuação numérica atribuída a uma notícia para ranking |
| **BRT** | Brasília Time — fuso horário UTC-3 |
| **Cron** | Sintaxe para agendamento de tarefas recorrentes em sistemas Unix |
| **Webhook** | Mecanismo de comunicação onde um servidor envia dados para outro via HTTP POST |
| **Goroutine** | Unidade de execução concorrente leve da linguagem Go |
| **Deduplicação** | Processo de identificação e remoção de registros duplicados |
| **Tier gratuito** | Nível de uso de um serviço de software que não gera cobrança financeira |
| **GitHub Actions** | Plataforma de CI/CD integrada ao GitHub para automação de workflows |
| **TabCoins** | Sistema de pontuação do TabNews, equivalente a upvotes |

---

*Documento gerado para o projeto 7C Hub News — Comunidade 7C Hub, Garanhuns/PE*
*Versão 1.0.0 — Março de 2026*
