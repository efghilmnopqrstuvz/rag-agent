# Chains and LCEL

A chain is a sequence of steps that processes an input and produces an output, where each step feeds into the next. Chains are how LangChain composes individual components — retrievers, prompts, models, parsers — into a complete application. The modern way to build them is the LangChain Expression Language, usually abbreviated LCEL.

## The LangChain Expression Language

LCEL lets you connect components using the pipe operator, borrowed from the way shell commands are chained together. Reading left to right, the output of each component becomes the input of the next. A typical retrieval chain reads as: take the question, retrieve context and pass the question through, assemble them into a prompt, send the prompt to the model, and parse the model's output into a clean string. Expressed this way, the structure of the application is visible at a glance, and each stage can be understood and tested independently.

## Everything Is a Runnable

LCEL works because every component implements the same `Runnable` interface. A prompt template, a model, a retriever, and a parser are all Runnables, and a chain built from them is itself a Runnable. This recursive property means chains can be nested inside other chains, and any chain can be invoked, batched, or streamed with the same methods as a single component. It also means any stage can be replaced — swapping one model for another, or one retriever for another — without touching the rest of the chain.

## Key Building Blocks

A few special Runnables make composition flexible:

- **RunnablePassthrough** passes its input forward unchanged. It is used when a value, such as the original question, needs to be carried along to a later stage at the same time as it is being used by another stage. In a retrieval chain, the question is sent to the retriever to fetch context and simultaneously passed through so it can be placed into the prompt.
- **RunnableLambda** wraps an ordinary function so it can participate in a chain as a Runnable. This is how custom logic — for example, a function that retrieves and then reranks documents — is inserted into an otherwise standard pipeline.
- **RunnableParallel** runs several Runnables on the same input at once and collects their outputs into a dictionary. The mapping of inputs at the start of a retrieval chain, where context and question are produced together, is an example of running steps in parallel.

## The Common Methods

Because a chain is a Runnable, it exposes the standard execution methods. `invoke` runs the chain on a single input and returns the result. `batch` runs it efficiently over a list of inputs. `stream` returns the output incrementally as it is produced, which is what enables a response to appear token by token rather than all at once. Asynchronous variants exist for each, allowing chains to be used in high-concurrency servers.

## Why LCEL Replaced Older Chain Classes

Earlier versions of LangChain provided pre-packaged chain classes for common tasks, such as a ready-made question-answering chain. These were convenient but rigid: customizing their behavior meant working around a fixed structure, and they hid the actual flow of data. LCEL replaced them with explicit composition. The trade-off is a little more code to write the chain yourself, in exchange for full transparency and control over every step — which is why, when asked in an interview how a chain is structured, describing an explicit LCEL pipeline is the modern and expected answer.
