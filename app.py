from agno.agent import Agent
from agno.knowledge.embedder.google import GeminiEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.models.google import Gemini
from agno.vectordb.chroma import ChromaDb
from agno.vectordb.search import SearchType

import requests

# Baixa o markdown seguindo redirecionamentos
url = "https://docs.agno.com/introduction.md"

response = requests.get(url, allow_redirects=True)
response.raise_for_status()

with open("introduction.md", "w", encoding="utf-8") as f:
    f.write(response.text)

# Cria a base de conhecimento
knowledge = Knowledge(
    vector_db=ChromaDb(
        collection="docs",
        path="tmp/chromadb",
        persistent_client=True,
        search_type=SearchType.hybrid,
        embedder=GeminiEmbedder(id="gemini-embedding-001"),
    ),
)

# Insere o arquivo local
knowledge.insert(
    path="introduction.md",
    skip_if_exists=True,
)

# Cria o agente
agent = Agent(
    model=Gemini(id="gemini-3-flash-preview"),
    knowledge=knowledge,
    search_knowledge=True,
    markdown=True,
)

agent.print_response("What is Agno?", stream=True)