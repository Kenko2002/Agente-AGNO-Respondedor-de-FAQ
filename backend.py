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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Knowledge (mesma coisa que você já tem)
knowledge = Knowledge(
    vector_db=ChromaDb(
        collection="docs",
        path="tmp/chromadb",
        persistent_client=True,
        search_type=SearchType.hybrid,
        embedder=GeminiEmbedder(id="gemini-embedding-001"),
    ),
)

for pdf in Path("documentos").rglob("*.pdf"):
    print(f"Indexando: {pdf}")

    knowledge.insert(
        path=str(pdf),
        skip_if_exists=True,
    )

agent = Agent(
    model=Gemini(id="gemini-3-flash-preview"),
    knowledge=knowledge,
    search_knowledge=True,
    markdown=True,
)

class Question(BaseModel):
    text: str

@app.post("/chat")
def chat(q: Question):
    try:
        response = agent.run(q.text)
        return {"answer": response.content}
    except Exception as e:
        return {"answer": f"Erro: {str(e)}"}