# Le domande di valutazione e le risposte di riferimento (ground truth)
eval_dataset = [
    {
        "question": "How do I configure a retriever in LangChain?",
        "ground_truth": "A retriever is configured from a vector store through search parameters. The most important is k, the number of chunks to return per query. Choosing k is a trade-off: more chunks give more context but risk noise and exceeding the context window, while too few may omit the relevant passage. Retrievers can also use metadata filters and a choice of search type.",
    },
    {
        "question": "What is the difference between Chroma and FAISS?",
        "ground_truth": "Chroma is a complete vector database with native persistence that manages storage, indexing and search and saves to disk automatically. FAISS is a pure similarity-search library by Meta, fast and lightweight but without native persistence, so the index must be saved and reloaded manually.",
    },
    {
        "question": "Why must the same embedding model be used for documents and queries?",
        "ground_truth": "Each embedding model defines its own vector space with its own geometry. Embedding documents with one model and queries with another puts their vectors in incompatible spaces, making similarity comparison meaningless. The same model must be used for both so comparisons are valid.",
    },
    {
        "question": "What is a reranker and why does it improve retrieval?",
        "ground_truth": "A reranker is a second stage: a larger candidate set is retrieved by vector similarity, then a dedicated model scores each candidate against the query for true relevance and keeps only the best few. It improves retrieval because it evaluates the query-passage pair explicitly, judging usefulness more precisely than cosine similarity alone.",
    },
]

# il codice qua sotto permette di stampare le domande solo se questo codice è eseguito direttamente, se da un altro codice provano ad importare questo la parte sotto non viene runnata.
if __name__ == "__main__":
    print(f"Dataset di valutazione: {len(eval_dataset)} domande")
    for item in eval_dataset:
        print("-", item["question"])