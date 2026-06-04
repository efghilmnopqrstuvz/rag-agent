# Vector Stores

A vector store is a specialized database designed to store embeddings and to search them efficiently. Where a traditional database retrieves rows by exact matches on values — for example, finding the record whose identifier equals a given number — a vector store retrieves by similarity, returning the stored vectors that are closest in meaning to a query vector. This capability is what makes semantic retrieval possible at scale.

## What a Vector Store Holds

For each chunk of text, a vector store keeps three things together: the embedding vector that represents the chunk, the original text of the chunk, and any metadata associated with it. Keeping the text alongside the vector is essential, because after a similarity search identifies the most relevant vectors, the application needs the underlying text to pass to the language model. The metadata enables filtering, so a search can be constrained to a subset of the collection.

## Similarity Search

The central operation of a vector store is similarity search. Given a query vector, the store finds the stored vectors with the highest similarity, typically measured by cosine similarity, and returns the corresponding chunks ranked from most to least similar. To make this fast even over large collections, vector stores use approximate nearest neighbor indexes, which trade a tiny amount of accuracy for a large gain in speed compared to comparing the query against every vector one by one.

## Common Vector Stores

Several vector stores are widely used, differing mainly in whether they are lightweight libraries or full services:

- **Chroma** is a complete, self-contained vector database with native persistence. It manages storage, indexing, and search in one tool and saves data to disk automatically, reloading it on restart. Its simple interface makes it a good fit for local development and small to medium applications.
- **FAISS** is a pure similarity-search library developed by Meta. It is extremely fast and lightweight but does only search; it has no native persistence, so the index must be saved and reloaded manually. It is popular for research and rapid prototyping.
- **Qdrant**, **Weaviate**, and **Pinecone** are production-grade vector databases, available as managed services or self-hosted, designed for large-scale, high-availability deployments.

## Persistence

Persistence is the ability to keep data on disk so that it survives a restart. A store with native persistence, like Chroma, handles this automatically: you tell it where to save, and it writes the database and the vector index to that location without any extra code. A library without native persistence, like FAISS, requires explicit calls to write the index to a file and to read it back later. This distinction matters for a web application whose backend starts and stops repeatedly, because re-embedding all documents on every restart would be slow and wasteful.

## The Standard Interface

In LangChain a vector store exposes a consistent set of operations. A method to create a store from a set of documents builds the index from scratch. A method to add documents inserts new chunks into an existing store incrementally, without rebuilding everything. A similarity-search method returns the closest chunks to a query. Finally, a method converts the store into a retriever, the abstraction that the rest of the retrieval pipeline consumes. This uniform interface means a vector store can be swapped for another with minimal changes to the surrounding code.
