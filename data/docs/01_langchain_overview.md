# LangChain Overview

LangChain is a framework for building applications powered by large language models (LLMs). Its core idea is to provide a set of standard, composable building blocks so that developers do not have to reinvent common patterns such as connecting to a model, retrieving relevant context, parsing structured output, or orchestrating multi-step reasoning. Instead of writing glue code from scratch, you assemble well-defined components into a pipeline.

## The LangChain Ecosystem

LangChain is not a single library but a family of packages, each with a clear responsibility:

- **langchain-core** contains the base abstractions and the LangChain Expression Language (LCEL). Every component — models, prompts, retrievers, parsers — implements a common `Runnable` interface. This is what makes components interchangeable and composable.
- **langchain** contains higher-level constructs built on top of core, such as chains and agent abstractions.
- **langchain-community** holds third-party integrations contributed by the community, for example loaders and vector store wrappers.
- **Partner packages** are dedicated integrations maintained for specific providers, such as `langchain-openai`, `langchain-ollama`, and `langchain-chroma`. These are kept separate so that a change in one provider does not destabilize the rest of the framework.
- **LangGraph** is a lower-level orchestration framework for building stateful, multi-step, and multi-agent workflows as graphs.
- **LangSmith** is the observability and evaluation platform used to trace, debug, and measure the quality of LLM applications.

## Why the Modular Design Matters

The separation into packages is a direct response to a practical problem: the LLM ecosystem changes quickly. New models, vector stores, and tools appear constantly. By isolating integrations into their own packages, LangChain lets the stable core evolve slowly while volatile integrations evolve independently. In practice this is also why import paths change between versions — components are frequently moved to more appropriate packages as the framework matures.

## The Runnable Interface

The unifying concept across the whole framework is the `Runnable`. Anything that can take an input and produce an output — a prompt template, a model, a retriever, a parser, or an entire chain — is a `Runnable`. Every `Runnable` exposes the same methods, most importantly `invoke` for a single input, `batch` for many inputs, and `stream` for incremental output. Because they share this interface, Runnables can be connected together with the pipe operator to form pipelines, and any piece can be swapped for another without rewriting the surrounding code.

## Where LangChain Fits in a RAG Application

In a Retrieval Augmented Generation system, LangChain provides the components for every stage: loaders to ingest documents, text splitters to break them into chunks, embedding models to vectorize them, vector stores to index and search them, retrievers to fetch relevant context, prompt templates to assemble that context with the user question, and output parsers to clean the model's response. The same framework then provides agents and LangGraph when the application needs to go beyond a single retrieval step and reason over multiple tools or coordinate several agents.
