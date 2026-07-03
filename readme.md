# Agente AGNO — Respondedor de FAQ

Assistente virtual que responde perguntas frequentes da universidade com base exclusivamente em documentos oficiais (PDFs), usando busca vetorial (RAG) e o modelo Gemini via AGNO.

O agente é instruído a nunca inventar informações, se a resposta não estiver nos documentos indexados ele informa isso claramente ao usuário.

## Funcionalidades

- Indexação automática de PDFs em um banco vetorial local
- Busca híbrida sobre os documentos
- Respostas geradas pelo Gemini, restritas ao conteúdo da base de conhecimento
- Interface web de chat construída com Reflex
- API em FastAPI que expõe o agente via endpoint

## Arquitetura

```text
documentos/          PDFs que compõem a base de conhecimento (FAQ, guias, etc.)
backend.py           API FastAPI que carrega o agente AGNO e expõe o endpoint /chat
app.py               Versão do agente para uso via terminal (CLI), sem API
frontend/            Aplicação Reflex (interface de chat web)
tmp/chromadb/        Banco vetorial persistido localmente (gerado automaticamente)
```

### Fluxo

1. Ao iniciar o backend, todos os PDFs em `documentos/` são indexados no ChromaDB (com embeddings do Gemini).
2. O frontend Reflex envia a pergunta do usuário para `POST /chat` no backend.
3. O agente AGNO busca os trechos mais relevantes na base de conhecimento e gera a resposta com o Gemini.
4. A resposta é exibida no chat em formato Markdown.

## Tecnologias

- AGNO — orquestração do agente e da base de conhecimento
- Google Gemini — modelo de linguagem e embeddings
- ChromaDB — banco de dados vetorial
- FastAPI — backend/API
- Reflex — frontend em Python

## Pré-requisitos

- Python 3.14.2
- Uma chave de API do Google Gemini 
- (Opcional) Bun — instalado automaticamente pelo Reflex na primeira execução do frontend

## Instalação

Clone o repositório e entre na pasta do projeto:

```bash
git clone https://github.com/Kenko2002/Agente-AGNO-Respondedor-de-FAQ.git
cd Agente-AGNO-Respondedor-de-FAQ
```

Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
```

No Windows:

```powershell
venv\Scripts\activate
```

Instale as dependências do backend:

```bash
pip install -r requirements.txt
```

Configure a chave de API: copie o arquivo de exemplo e preencha com sua chave do Gemini.

```bash
cp example.env .env
```

```env
GOOGLE_API_KEY=sua_chave_aqui
```

## Como rodar

O projeto é composto por dois processos que devem rodar em paralelo: o backend (API + agente) e o frontend (interface web).

### Terminal 1 — Backend (API)

```bash
uvicorn backend:app --reload --host 0.0.0.0 --port 8000
```

Na primeira execução, os PDFs em `documentos/` serão indexados automaticamente no ChromaDB (`tmp/chromadb/`). Isso pode levar alguns segundos.

### Terminal 2 — Frontend (Reflex)

```bash
cd frontend
reflex run
```

Por padrão, o frontend fica disponível em `http://localhost:3000` e se comunica com o backend em `http://localhost:8000`.

### Alternativa via terminal

Para testar o agente rapidamente sem subir o backend e o frontend, execute:

```bash
python app.py
```

## Adicionando novos documentos

Basta colocar novos arquivos `.pdf` dentro da pasta `documentos/` e reiniciar o backend.

Documentos já indexados não são reprocessados (`skip_if_exists=True`).

## Endpoint da API

### POST `/chat`

**Request**

```json
{
  "text": "Como solicitar a colação de grau?"
}
```

**Response**

```json
{
  "answer": "Resposta gerada com base nos documentos indexados..."
}
```
