# Agents and Tool Calling

An agent is an application in which a language model decides what to do, rather than following a fixed sequence of steps written by a developer. Where a chain runs the same predetermined pipeline every time, an agent uses the model's reasoning to choose actions dynamically: which tool to use, what input to give it, and whether to act again or to respond. This flexibility lets a single system handle a wide range of requests that a rigid chain could not.

## Tools

A tool is a capability the agent can invoke — a function the model is allowed to call. Examples include querying a RAG system, performing a calculation, calling an external API, or looking something up in a database. Each tool is defined with three things: a name, a description written in natural language, and a specification of the arguments it accepts. The description is the most important part, because the model reads it to decide when the tool is appropriate. A clear, accurate description is what allows the model to match a user's request to the right capability.

## Tool Calling

Tool calling is the mechanism by which a model selects a tool and produces the arguments to call it with. Given a user request and the list of available tools, the model does not execute anything itself; instead it outputs a structured request indicating which tool to call and with what arguments. The application then runs the actual tool and returns the result to the model. This separation is deliberate: the model decides, but the application controls execution, which keeps the system safe and predictable. Modern chat models are specifically trained to produce these structured tool calls reliably.

## The Agent Loop

An agent operates in a loop. The model receives the user's request and the available tools and decides on an action. If it chooses a tool, the application executes it and feeds the result back to the model. The model then reconsiders: it may call another tool, use the new information, or conclude that it has enough to answer. This cycle of reasoning and acting continues until the model produces a final response. The pattern of interleaving reasoning with actions is the foundation of how agents solve multi-step problems.

## Memory and State

Because an interaction may span several steps, an agent needs to keep track of what has happened. Conversation memory holds the history of the exchange so the model has context for each new decision. This connects to a property of stateless systems: when an application is built on a stateless protocol, the server does not remember previous requests on its own, so the conversation state must be supplied explicitly with each call. Managing this state correctly is what allows an agent to carry context across a multi-turn conversation.

## Composing an Agent

Building an agent means assembling a model, a set of tools, a prompt that frames the agent's behavior, and any additional logic that shapes how it operates. The model provides the reasoning, the tools provide the capabilities, and the prompt establishes the agent's role and constraints. A RAG system fits naturally into this picture as one tool among several: the agent can choose to consult the RAG when a question calls for retrieved knowledge, while using other tools for calculations or external lookups. This is how a question-answering system grows from a single retrieval chain into a flexible assistant that decides for itself how to handle each request.

## Error Handling

A robust agent must cope with failures: a tool may return an error, produce unexpected output, or time out. Well-designed agents handle these cases gracefully, retrying, choosing an alternative, or reporting the problem rather than crashing. Anticipating tool failures is part of what separates a demonstration agent from one that can be relied upon in production.
