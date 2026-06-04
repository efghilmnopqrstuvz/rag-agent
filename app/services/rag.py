import os
os.environ["USER_AGENT"] = "rag-agent/1.0"

import bs4
from langchain_community.document_loaders import WebBaseLoader, DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from flashrank import Ranker, RerankRequest

CHROMA_PATH = "data/chroma"

# --- Elementi condivisi tra endpoint di produzione e valutazione ---

# Prompt condiviso: endpoint ed eval DEVONO usare lo stesso,
# altrimenti l'eval non misura ciò che gira davvero in produzione.
RAG_PROMPT = ChatPromptTemplate.from_template("""
Answer the question based on the following retrieved context. If the answer is not contained within the context, say that the information needed to answer is not clearly provided in the context.

Context: {context}

Question: {question}

Answer:""")

TOP_N = 5  # scelto osservando il gap negli score del reranker (pertinenti >0.80, rumore <0.20)

# Il reranker viene caricato una sola volta e riusato (lazy singleton):
# ricaricarlo a ogni chiamata significherebbe rileggere il modello da disco ogni volta.
_ranker = None

def _get_ranker() -> Ranker:
    global _ranker
    if _ranker is None:
        _ranker = Ranker(model_name="ms-marco-MiniLM-L-12-v2")
    return _ranker


# --- Ingestion: caricamento e chunking ---

def load_and_split_documents(urls: list[str]) -> list:
    """Carica pagine web (solo il tag <main>) e le divide in chunk."""
    loader = WebBaseLoader(
        web_paths=urls,
        bs_kwargs={"parse_only": bs4.SoupStrainer("main")}
    )
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_documents(documents)


def load_and_split_local_documents(directory: str = "data/docs") -> list:
    """Carica tutti i file .md da una cartella locale e li divide in chunk."""
    loader = DirectoryLoader(
        directory,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_documents(documents)


# --- Vector store ---

def create_vectorstore(chunks: list) -> Chroma:
    """Vettorizza i chunk e crea il vector store da zero, salvando su disco."""
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )


def load_vectorstore() -> Chroma:
    """Ricarica un vector store già esistente da disco."""
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )


def add_documents(urls: list[str]) -> int:
    """Aggiunge nuovi documenti (da URL) al vector store esistente."""
    chunks = load_and_split_documents(urls)
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    vectorstore.add_documents(chunks)
    return len(chunks)


# --- Retrieval + rerank (condiviso) ---

def rerank_contexts(vectorstore: Chroma, question: str, top_n: int = TOP_N) -> list[str]:
    """
    Recupera i top 10 candidati via ricerca vettoriale, li riordina col reranker
    e restituisce i migliori top_n come lista di stringhe.
    Unica fonte di verità per il retrieval: usata sia dall'endpoint sia dall'eval.
    """
    base_retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
    docs = base_retriever.invoke(question)

    passages = [{"id": i, "text": doc.page_content} for i, doc in enumerate(docs)]
    reranked = _get_ranker().rerank(RerankRequest(query=question, passages=passages))

    return [p["text"] for p in reranked[:top_n]]


# --- Generazione ---

def get_rag_chain(vectorstore: Chroma):
    """Chain RAG per l'endpoint: restituisce solo la risposta (stringa)."""
    llm = OllamaLLM(model="llama3.2")

    chain = (
        {
            "context": RunnableLambda(lambda q: "\n\n".join(rerank_contexts(vectorstore, q))),
            "question": RunnablePassthrough(),
        }
        | RAG_PROMPT
        | llm
        | StrOutputParser()
    )
    return chain


def generate_answer(vectorstore: Chroma, question: str) -> tuple[str, list[str]]:
    """
    Per la valutazione: esegue il RAG e restituisce (risposta, lista_di_contesti).
    Riusa rerank_contexts e RAG_PROMPT — gli stessi dell'endpoint — così l'eval
    misura esattamente la pipeline di produzione.
    """
    contexts = rerank_contexts(vectorstore, question)
    llm = OllamaLLM(model="llama3.2")

    answer = (RAG_PROMPT | llm | StrOutputParser()).invoke({
        "context": "\n\n".join(contexts),
        "question": question,
    })
    return answer, contexts