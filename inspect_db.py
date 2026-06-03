from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma(persist_directory="data/chroma", embedding_function=embeddings)

docs = vectorstore.get()
print(f"Totale chunk nel vector store: {len(docs['ids'])}")
print(f"\n--- CHUNK 1 ---")
print(docs['documents'][0])
print(f"\n--- CHUNK 2 ---")
print(docs['documents'][1])