from app.services.rag import load_and_split_documents, create_vectorstore

urls = [
    "https://python.langchain.com/docs/introduction/",
    "https://python.langchain.com/docs/concepts/",
    "https://python.langchain.com/docs/concepts/agents/",
    "https://python.langchain.com/docs/concepts/retrieval/",
    "https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/"
]

print("Caricamento e pulizia documenti...")
chunks = load_and_split_documents(urls)
print(f"Chunk creati: {len(chunks)}")
print(f"\nPrimo chunk pulito:\n{chunks[0].page_content[:300]}")

print("\nCreazione vector store...")
vectorstore = create_vectorstore(chunks)
print(f"Vector store creato con {vectorstore._collection.count()} chunk")