from dotenv import load_dotenv
load_dotenv()

from agno.agent import Agent
from agno.knowledge.embedder.google import GeminiEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.models.google import Gemini
from agno.vectordb.chroma import ChromaDb
from agno.vectordb.search import SearchType
from pathlib import Path

pdf_path = Path("documentos")

# Garantir que a pasta exista
if not pdf_path.exists():
    raise FileNotFoundError("Pasta 'documentos' não encontrada.")

# Lista PDFs dentro da pasta
pdfs = list(pdf_path.glob("*.pdf"))

# Se não existir PDF, interrompe
if not pdfs:
    raise FileNotFoundError("Nenhum PDF encontrado na pasta 'documentos'.")

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

# Indexa todos os PDFs
for pdf in pdfs:
    print(f"Indexando: {pdf}")

    knowledge.insert(
        path=str(pdf),
        skip_if_exists=True,
    )

# Cria o agente
agent = Agent(
    model=Gemini(id="gemini-3-flash-preview"),
    knowledge=knowledge,
    search_knowledge=True,
    markdown=True,
)

while True:
    pergunta = input("\nVocê: ")

    if not pergunta.strip():
        continue

    if pergunta.lower() in ["sair", "exit", "quit"]:
        print("Encerrando...")
        break

    print("\nAgente:")
    agent.print_response(pergunta, stream=True)
