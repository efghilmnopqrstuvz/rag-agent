# Embedding Models

An embedding model converts a piece of text into a vector — a list of numbers that represents the meaning of that text as a point in a high-dimensional space. Embeddings are the foundation of semantic search and therefore of retrieval in a RAG system. They allow a machine to measure how similar two pieces of text are in meaning, not merely whether they share the same words.

## How Embeddings Capture Meaning

The key property of a good embedding model is that texts with similar meaning are mapped to nearby points in the vector space, while unrelated texts are mapped far apart. This is learned during training on large amounts of text. As a result, the question "how do I store vectors" and a passage about "saving embeddings to a database" can be recognized as related even though they share almost no words, because their vectors lie close together.

## The Vector Space

Each embedding model defines its own vector space, with its own number of dimensions and its own internal geometry. This has a critical practical consequence: the same model must be used to embed both the documents and the user's query. If documents are embedded with one model and the query with another, their vectors live in incompatible spaces, and comparing them produces meaningless results. The rule is therefore absolute — the embedding model must be consistent across the entire pipeline.

## Measuring Similarity

Once text is represented as vectors, similarity is measured geometrically. The most common metric is cosine similarity, which measures the angle between two vectors rather than the distance between them. Two vectors pointing in the same direction have a cosine similarity close to one and are considered very similar; vectors at right angles are unrelated. Cosine similarity is popular because it focuses on the direction of meaning and is not distorted by the length of the text. Other metrics such as the dot product are also used depending on the model and store.

## Dedicated Embedding Models versus Generative Models

It is important to distinguish embedding models from generative models. A generative model such as a chat LLM is designed to produce text. A dedicated embedding model is designed to produce vectors and is typically much smaller and faster. Although some generative models can be coaxed into producing embeddings, the result is usually inferior and inefficient — and some servers will refuse the request outright because the model was not started in embedding mode. For retrieval, a purpose-built embedding model is both more accurate and far lighter, which matters especially when running locally without a GPU.

## Trade-offs in Choosing an Embedding Model

Selecting an embedding model involves balancing three factors: quality, cost, and speed. Larger models generally produce higher-quality embeddings but are slower and, when accessed via an API, more expensive. Smaller models are faster and cheaper but may capture meaning less precisely. Language coverage is also a factor: many embedding models are trained predominantly on English, so a knowledge base and queries in English often retrieve more reliably than the same content in other languages. The right choice depends on the accuracy the application requires and the resources available to run it.
