# Retrievers

A retriever is the component whose job is to take a query and return the documents most relevant to it. It is the bridge between the user's question and the knowledge stored in the system. While a vector store knows how to perform similarity search, a retriever is a more general abstraction: it presents a uniform interface for fetching relevant documents, regardless of how that fetching is actually done underneath.

## The Retriever Interface

A retriever implements the standard `Runnable` interface, which means it is invoked with a query and returns a list of `Document` objects. This uniformity is powerful: because a retriever is just another `Runnable`, it can be dropped directly into a pipeline alongside prompts, models, and parsers. The component that consumes the retriever does not need to know whether it is backed by a vector store, a keyword index, or a combination of several strategies.

## Configuring a Vector Store Retriever

The most common retriever is created directly from a vector store. When you turn a vector store into a retriever, you can configure how it behaves through search parameters. The most important of these is the number of documents to return, often written as `k`. Setting `k` to three, for example, instructs the retriever to return the three most similar chunks for each query. Choosing this number is itself a trade-off: returning more chunks gives the model more context but increases the risk of including irrelevant material and of exceeding the context window, while returning too few risks omitting the passage that actually contains the answer. Retrievers can also be configured with metadata filters, so that a search is restricted to documents matching certain criteria, and with the choice between standard similarity search and alternative search types.

## Limitations of Pure Similarity Search

A retriever based solely on vector similarity has a known weakness. Cosine similarity measures how close two vectors are in the embedding space, but geometric closeness does not guarantee that a chunk actually contains the answer to the question. A chunk can be semantically near a query — discussing the same general topic — without holding the specific information the user needs. This is why a naive retriever sometimes returns plausible-looking but unhelpful passages.

## Advanced Retrieval Strategies

Several techniques address this limitation:

- **Reranking** adds a second stage. The retriever first fetches a larger set of candidates, say ten chunks, and a dedicated reranking model then scores each candidate against the query for true relevance and keeps only the best few. Because the reranker explicitly evaluates the pair of query and passage together, it judges usefulness more precisely than similarity alone, promoting the chunks that genuinely answer the question and demoting those that are merely related.
- **Hybrid search** combines vector similarity with traditional keyword search. Vector search captures meaning, while keyword search guarantees that exact terms — names, codes, rare words — are matched. Merging the two often retrieves better results than either alone.
- **Multi-query retrieval** rephrases the original question into several variations and retrieves for each, broadening coverage when a single phrasing might miss relevant chunks.

## Retrievers in the RAG Pipeline

In the full pipeline, the retriever sits between the user's question and the prompt. The question goes in, the retriever returns the relevant chunks, and those chunks are inserted into the prompt as context alongside the original question. Improving the retriever — through better configuration, reranking, or hybrid search — is usually the single most effective way to raise the quality of a RAG system, because no amount of skill in the generation stage can compensate for retrieving the wrong context in the first place.
