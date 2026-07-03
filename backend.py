from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from agno.agent import Agent
from agno.models.google import Gemini
from agno.knowledge.embedder.google import GeminiEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from agno.vectordb.search import SearchType

from pathlib import Path

app = FastAPI()

# Libera requisições do frontend para a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

knowledge = Knowledge(
    vector_db=ChromaDb(
        collection="docs",
        path="tmp/chromadb",
        persistent_client=True,
        search_type=SearchType.hybrid,
        embedder=GeminiEmbedder(id="gemini-embedding-001"),
    ),
)

# Indexa todos os PDFs presentes na pasta "documentos"
for pdf in Path("documentos").rglob("*.pdf"):
    print(f"Indexando: {pdf}")

    knowledge.insert(
        path=str(pdf),
        skip_if_exists=True,
    )

# Configuração do agente responsável por responder às perguntas

agent = Agent(
    model=Gemini(id="gemini-3-flash-preview"),
    knowledge=knowledge,
    search_knowledge=True,
    markdown=True,
    instructions=[
        """
        Você é um assistente virtual da Universidade.

        Responda APENAS utilizando informações encontradas nos documentos da base de conhecimento.

        Regras obrigatórias:

        - Nunca invente informações.
        - Nunca faça suposições.
        - Nunca utilize conhecimento próprio que não esteja nos documentos.
        - Se a resposta não estiver presente nos documentos, informe isso claramente.
        - Não tente completar informações ausentes.
        - Seja objetivo e cite apenas o que puder ser confirmado pelos documentos.

        Caso a informação não seja encontrada, responda exatamente:

        "Não encontrei essa informação nos documentos disponíveis. Caso necessário, entre em contato com a secretaria ou consulte os canais oficiais da universidade."

        Sempre responda em Markdown bem formatado.
        """
    ]
)

# Endpoint responsável por receber a pergunta e retornar a resposta do agente

class Question(BaseModel):
    text: str

@app.post("/chat")
def chat(q: Question):
    try:
        response = agent.run(q.text)
        return {"answer": response.content}
    except Exception as e:
        return {"answer": f"Erro: {str(e)}"}