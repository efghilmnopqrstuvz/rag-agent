# Prompts and Output Parsers

The prompt is the instruction given to a language model, and the output parser is the component that turns the model's raw response into a usable form. Together they sit at the two ends of the model call: the prompt shapes what goes in, and the parser shapes what comes out. In a RAG system, the prompt is where retrieved context and the user's question are combined before generation.

## Prompt Templates

Rather than building prompt strings by hand, LangChain uses prompt templates. A template is a reusable pattern with placeholders that are filled in at runtime. For example, a template for retrieval-augmented generation might contain a placeholder for the retrieved context and another for the user's question, with instructions around them telling the model to answer based only on the provided context. When the chain runs, the actual context and question are substituted into the placeholders to produce the final prompt. Templates make prompts consistent, testable, and easy to modify in one place.

## Chat Prompt Templates and Message Roles

Modern chat models do not take a single block of text; they take a sequence of messages, each with a role. The main roles are the system message, which sets the model's overall behavior and instructions; the human message, which carries the user's input; and the assistant message, which represents the model's own prior responses in a conversation. A chat prompt template assembles these messages with placeholders, allowing a system instruction to be combined with dynamic user input. Using roles correctly is important: instructions placed in the system message tend to be followed more reliably than the same instructions buried in user text.

## Grounding the Model in Context

A central technique in RAG prompting is instructing the model to answer using only the retrieved context, and to acknowledge when the context does not contain the answer. This grounding reduces hallucination — the tendency of a model to invent plausible but false information. When the retrieved context is poor or irrelevant, a well-written prompt makes the model more likely to say it cannot answer rather than fabricate one, which is far safer in a production system. The quality of grounding therefore depends both on the prompt and on the quality of the retrieved context feeding into it.

## Output Parsers

A language model does not simply return a clean string. Its raw output is a structured object that includes the generated content along with metadata such as token counts and other information. An output parser extracts the part the application actually needs. The simplest, a string output parser, pulls out just the generated text and returns it as a plain string, which is what most chat-style responses require.

## Structured Output

Sometimes an application needs the model to return data in a precise shape — for instance, a set of fields with specific types rather than free-form prose. Structured output parsers address this by instructing the model to produce output in a defined schema and then validating and parsing that output into a typed object. Many models support this directly through a dedicated structured-output capability, which constrains the generation to match the requested schema. Structured output is essential when the model's response must be consumed by other code rather than read by a human, such as extracting entities, classifying input, or producing arguments for a tool call.

## Prompts and Parsers in the Pipeline

In an LCEL chain, the prompt template and the output parser bracket the model. The flow is: inputs are assembled by the prompt template into a final prompt, the prompt is sent to the model, and the model's raw response is handed to the parser, which returns clean output. Because both are ordinary Runnables, they slot into the pipeline like any other stage, and either can be changed without disturbing the rest.
