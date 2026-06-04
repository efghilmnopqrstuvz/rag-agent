# Text Splitters and Chunking

Once documents have been loaded, they must be broken into smaller pieces before they can be embedded and stored. This step is called chunking, and the components that perform it are text splitters. Chunking is one of the most consequential design decisions in a RAG system, because the size and boundaries of chunks determine what the retriever can find and how much useful context reaches the model.

## Why Chunking Is Necessary

There are two reasons documents cannot be embedded whole. First, embedding models and LLMs have a limited context window — a maximum amount of text they can process at once. Second, and more subtly, a single embedding vector can only capture so much meaning. If an entire long document is collapsed into one vector, that vector becomes a blurry average of every topic the document covers, and it will match poorly against a specific question. Smaller chunks produce sharper, more specific vectors that retrieve more precisely.

## The Core Trade-off

Choosing a chunk size is a balancing act. Chunks that are too large are less specific: they dilute the relevant information among unrelated text and risk exceeding the context window when several are combined. Chunks that are too small are too fragmented: they may lose the surrounding context needed to make sense of a passage, splitting a single idea across multiple pieces. A common starting point is a chunk size of around one thousand characters, which is then tuned based on the documents and the questions being asked.

## Chunk Overlap

To reduce the risk of cutting an idea exactly at a boundary, splitters allow a configurable overlap between adjacent chunks. With an overlap of, say, two hundred characters, the end of one chunk is repeated at the start of the next. This means that a sentence or concept that falls near a boundary still appears intact in at least one chunk, preserving local context that would otherwise be lost.

## Splitting Strategies

Different splitters take different approaches:

- **RecursiveCharacterTextSplitter** is the most widely used. Rather than cutting blindly every N characters, it tries a hierarchy of separators: first it attempts to split on paragraph breaks, then on sentences, then on words, descending only as far as needed to fit the target size. This respects the natural structure of the text and keeps related content together.
- **CharacterTextSplitter** splits on a single separator and is simpler but less structure-aware.
- **Token-based splitters** measure size in model tokens rather than characters, which aligns chunk size precisely with the model's context limits.
- **Semantic chunking** is a more advanced approach that does not split by fixed size at all. Instead it embeds the text as it goes and detects where the meaning shifts, cutting a new chunk when the topic changes. This produces more coherent chunks but is slower and more expensive, because it must run the embedding model during the splitting step itself.

## Choosing a Strategy

There is no universally best chunking method; the right choice is a trade-off for the situation. Recursive character splitting is a strong, fast default that works well in the large majority of projects. Semantic chunking is worth adopting when chunk coherence is critical and the extra cost is justified. In an interview, the strongest answer to "why did you choose this chunking approach" is not "because it is the best," but a clear explanation of the trade-off you made for your specific data and constraints.
