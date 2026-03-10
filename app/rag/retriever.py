from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

emb = OllamaEmbeddings(model="nomic-embed-text")

vector = Chroma(
    persist_directory="./data",
    embedding_function=emb,
)

retriever = vector.as_retriever()


def search(query: str) -> str:

    docs = retriever.invoke(query)

    return "\n".join(d.page_content for d in docs)
