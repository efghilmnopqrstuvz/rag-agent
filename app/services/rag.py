import os
os.environ["USER_AGENT"] = "rag-agent/1.0"

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
import bs4

# Cartella dove Chroma salverà i dati su disco
CHROMA_PATH = "data/chroma"


############################################################################################################################################################################################################ 

# Qui definiamo tutte le funzioni per caricare, pulire, splittare e vettorizzare i documenti.

############################################################################################################################################################################################################ 

def load_and_split_documents(urls: list[str]) -> list:
    """
    Carica documenti da una lista di URL, pulisce il testo
    estraendo solo il contenuto principale, e divide in chunk.
    """
    loader = WebBaseLoader(
    web_paths=urls,
    bs_kwargs={
        "parse_only": bs4.SoupStrainer("main")
        }
    )
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    
    chunks = text_splitter.split_documents(documents)
    return chunks

def create_vectorstore(chunks: list) -> Chroma:
    """
    Vettorizza i chunk e li salva in Chroma.
    """
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    
    return vectorstore

def load_vectorstore() -> Chroma:
    """
    Carica un vector store già esistente da disco.
    """
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    vectorstore = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )
    
    return vectorstore

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def add_documents(urls: list[str]) -> int:
    """
    Aggiunge nuovi documenti al vector store esistente.
    Non ricrea tutto da zero — aggiunge solo i nuovi chunk.
    Restituisce il numero di chunk aggiunti.
    """
    # Carica e splitta i nuovi documenti
    chunks = load_and_split_documents(urls)
    
    # Carica il vector store esistente
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )
    
    # Aggiunge i nuovi chunk a quelli già esistenti
    vectorstore.add_documents(chunks)
    
    return len(chunks)

from langchain_community.document_loaders import DirectoryLoader, TextLoader

def load_and_split_local_documents(directory: str = "data/docs") -> list:
    """
    Carica tutti i file .md da una cartella locale e li divide in chunk.
    """
    loader = DirectoryLoader(
        directory,
        glob="**/*.md",                       # tutti i .md, anche in eventuali sottocartelle
        loader_cls=TextLoader,                # legge testo semplice, niente parsing pesante
        loader_kwargs={"encoding": "utf-8"}   # importante su Windows per evitare errori di encoding
    )
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(documents)
    return chunks


############################################################################################################################################################################################################ 

# Qui definiamo la chain RAG completa, con un reranker manuale (FlashRank).

############################################################################################################################################################################################################ 

from flashrank import Ranker, RerankRequest

# question (stringa)
#     ↓
# base_retriever.invoke() → vettorizza + cerca
#     ↓
# docs (lista di 10 Document)
#     ↓
# passages (lista di 10 dizionari per flashrank)
#     ↓
# reranked (stessi 10, riordinati per rilevanza)
#     ↓
# top 3 → contesto per l'LLM

def get_rag_chain(vectorstore: Chroma):
    """
    Costruisce la chain RAG completa con reranker manuale:
    domanda → retrieval (top 10) → rerank (top 3) → LLM → risposta
    """
    llm = OllamaLLM(model="llama3.2")
    ranker = Ranker(model_name="ms-marco-MiniLM-L-12-v2")
    
    base_retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
    # Quanti chunk passare all'LLM dopo il reranking.
    # Scelto a 5 osservando il gap negli score del reranker:
    # i chunk pertinenti stanno >0.80, il rumore crolla <0.20.
    TOP_N = 5
    
    def retrieve_and_rerank(question: str) -> str:
        docs = base_retriever.invoke(question)
        docs = base_retriever.invoke(question)

        # DEBUG — cosa pesca la ricerca vettoriale PRIMA del reranking
        # print("\n=== TOP 10 DAL VECTOR SEARCH (pre-rerank) ===")
        for i, doc in enumerate(docs):
            source = doc.metadata.get("source", "?")
        #     print(f"{i+1}. {source} | {doc.page_content[:70].strip()}")
        # print("=============================================\n")
        
        passages = [{"id": i, "text": doc.page_content} for i, doc in enumerate(docs)]
        rerank_request = RerankRequest(query=question, passages=passages)
        reranked = ranker.rerank(rerank_request)

        # DEBUG — punteggio del reranker su tutti i 10 candidati, con la fonte
        # print("\n=== RANKING COMPLETO (post-rerank) ===")
        for r in reranked:
            source = docs[r["id"]].metadata.get("source", "?")
        #     print(f"score={r['score']:.4f} | {source} | {r['text'][:60].strip()}")
        # print("======================================\n")

        # print(type(reranked[0]))
        # print(reranked[0])
        
        top_k = reranked[:TOP_N]
        context = "\n\n".join([p["text"] for p in top_k])
    
        return context
    
    prompt = ChatPromptTemplate.from_template("""
    Answer the question based on the following retrieved context. If the answer is not contained within the context, say that the information needed to answer are not clearly provided in the context. 
    
    Context: {context}
    
    Question: {question}
    
    Answer:""")
    
    from langchain_core.runnables import RunnableLambda
    
    chain = (
        {
            "context": RunnableLambda(lambda x: retrieve_and_rerank(x)),
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain