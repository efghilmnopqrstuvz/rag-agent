import json
from app.services.rag import load_vectorstore, generate_answer
from langchain_ollama import ChatOllama

# Il giudice: più capace del 3B generatore. temperature=0 per giudizi stabili e ripetibili.
judge = ChatOllama(model="llama3.1:8b", temperature=0)

# Le 4 domande con la rispettiva ground truth
eval_data = [
    {
        "question": "How do I configure a retriever in LangChain?",
        "ground_truth": "A retriever is configured from a vector store through search parameters. The most important is k, the number of chunks to return per query. Choosing k is a trade-off: more chunks give more context but risk noise and exceeding the context window, while too few may omit the relevant passage.",
    },
    {
        "question": "What is the difference between Chroma and FAISS?",
        "ground_truth": "Chroma is a complete vector database with native persistence that saves to disk automatically. FAISS is a pure similarity-search library by Meta, fast and lightweight but without native persistence, so the index must be saved and reloaded manually.",
    },
    {
        "question": "Why must the same embedding model be used for documents and queries?",
        "ground_truth": "Each embedding model defines its own vector space with its own geometry. Embedding documents with one model and queries with another puts their vectors in incompatible spaces, making similarity comparison meaningless.",
    },
    {
        "question": "What is a reranker and why does it improve retrieval?",
        "ground_truth": "A reranker is a second stage: a larger candidate set is retrieved by vector similarity, then a dedicated model scores each candidate against the query for true relevance and keeps only the best few. It judges usefulness more precisely than cosine similarity alone.",
    },
]


def judge_score(rubric: str) -> tuple[float, str]:
    """
    Manda al giudice una rubrica di valutazione e si fa restituire un punteggio 0-1.
    Chiediamo output in JSON e lo parsiamo; se il giudice sbaglia formato, torna NaN.
    """
    prompt = f"""You are a strict evaluator. {rubric}

Respond ONLY with a JSON object, nothing else, in this exact format:
{{"score": <number between 0 and 1>, "reason": "<one short sentence>"}}"""

    # judge è il modello llm che usiamo
    raw = judge.invoke(prompt).content
    try:
        # Il giudice a volte mette testo intorno al JSON: isoliamo il blocco { ... }
        start = raw.index("{")
        end = raw.rindex("}") + 1
        data = json.loads(raw[start:end])
        return float(data["score"]), data.get("reason", "")
    except (ValueError, KeyError, json.JSONDecodeError):
        return float("nan"), "parse error"


def evaluate_question(question: str, ground_truth: str, answer: str, contexts: list[str]) -> dict:
    """Calcola le 4 metriche per una singola domanda."""
    ctx = "\n\n".join(contexts)

    return {
        # GENERAZIONE — reference-free: confronta risposta col contesto
        "faithfulness": judge_score(
            f"Does the ANSWER only make claims supported by the CONTEXT? "
            f"1 = fully supported, 0 = hallucinated.\n\nCONTEXT:\n{ctx}\n\nANSWER:\n{answer}"
        ),
        # GENERAZIONE — reference-free: confronta risposta con domanda
        "answer_relevance": judge_score(
            f"Does the ANSWER directly address the QUESTION? "
            f"1 = fully on-point, 0 = off-topic.\n\nQUESTION:\n{question}\n\nANSWER:\n{answer}"
        ),
        # RETRIEVAL — il contesto recuperato è pertinente alla domanda?
        "context_relevance": judge_score(
            f"Is the CONTEXT relevant and sufficient to answer the QUESTION? "
            f"1 = highly relevant, 0 = irrelevant.\n\nQUESTION:\n{question}\n\nCONTEXT:\n{ctx}"
        ),
        # GENERAZIONE — reference-based: confronta risposta con la ground truth
        "answer_correctness": judge_score(
            f"Compared to the REFERENCE answer, is the ANSWER correct and complete? "
            f"1 = matches reference, 0 = wrong.\n\nREFERENCE:\n{ground_truth}\n\nANSWER:\n{answer}"
        ),
    }


def run_evaluation():
    vectorstore = load_vectorstore()
    all_scores = {"faithfulness": [], "answer_relevance": [], "context_relevance": [], "answer_correctness": []}

    for i, item in enumerate(eval_data, start=1):
        print(f"\n[{i}/{len(eval_data)}] {item['question']}")
        answer, contexts = generate_answer(vectorstore, item["question"])
        metrics = evaluate_question(item["question"], item["ground_truth"], answer, contexts)

        for name, (score, reason) in metrics.items():
            print(f"   {name:20s}: {score:.2f}  ({reason})")
            all_scores[name].append(score)

    # Media per metrica, ignorando gli eventuali NaN
    print("\n=== MEDIE COMPLESSIVE ===")
    for name, scores in all_scores.items():
        valid = [s for s in scores if s == s]  # s == s è False solo per NaN
        avg = sum(valid) / len(valid) if valid else float("nan")
        print(f"{name:20s}: {avg:.2f}")


if __name__ == "__main__":
    run_evaluation()