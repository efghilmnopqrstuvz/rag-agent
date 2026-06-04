from app.services.rag import load_and_split_local_documents, create_vectorstore

print("Caricamento documenti locali...")
chunks = load_and_split_local_documents()
print(f"Chunk creati: {len(chunks)}")

print("Creazione vector store...")
vectorstore = create_vectorstore(chunks)
print(f"Indicizzati: {vectorstore._collection.count()} chunk")