import math
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from app.services.rag import load_vectorstore, rerank_contexts

# Vector store caricato una volta sola (stesso pattern lazy del reranker)
_vectorstore = None

def _get_vectorstore():
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = load_vectorstore()
    return _vectorstore


# --- I TOOL (le "mani": eseguono, non ragionano) ---

@tool
def search_langchain_docs(query: str) -> str:
    """Search the LangChain and LangGraph documentation knowledge base.
    Use this tool for any question about LangChain or LangGraph: concepts,
    components, retrievers, embeddings, vector stores, chains, agents,
    or multi-agent systems. Returns the most relevant documentation passages."""
    contexts = rerank_contexts(_get_vectorstore(), query)
    return "\n\n".join(contexts)


@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression and return the numeric result.
    Use this tool for any arithmetic or math question, e.g. "47 * 89" or
    "sqrt(144) + 10". The input must be a valid Python math expression."""
    try:
        allowed = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
        return str(eval(expression, {"__builtins__": {}}, allowed))
    except Exception as e:
        return f"Error: {e}"


# --- L'AGENTE (il "cervello" + l'orchestratore) ---

def build_agent():
    """Crea l'agente: il modello (cervello) + i tool (mani).
    create_agent costruisce internamente il loop di orchestrazione (su LangGraph)."""
    llm = ChatOllama(model="llama3.1:8b", temperature=0)
    return create_agent(llm, tools=[search_langchain_docs, calculator])


def run_agent(question: str) -> str:
    """Esegue l'agente su una domanda e mostra quale tool ha scelto."""
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})

    # Ispezioniamo i messaggi per VEDERE il routing: quali tool ha chiamato l'agente
    for msg in result["messages"]:
        tool_calls = getattr(msg, "tool_calls", None)
        if tool_calls:
            for tc in tool_calls:
                print(f"   → tool scelto: {tc['name']}  args={tc['args']}")

    # L'ultimo messaggio è la risposta finale composta dall'agente
    return result["messages"][-1].content


if __name__ == "__main__":
    domande = [
        "How does reranking improve retrieval in LangChain?",  # dovrebbe → search_langchain_docs
        "What is 47 * 89?",                                    # dovrebbe → calculator
    ]
    for q in domande:
        print(f"\nDOMANDA: {q}")
        risposta = run_agent(q)
        print(f"RISPOSTA: {risposta}")