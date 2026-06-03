import os
os.environ["USER_AGENT"] = "rag-agent/1.0"

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
import bs4

# Cartella dove Chroma salverà i dati su disco
CHROMA_PATH = "data/chroma"

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

def get_rag_chain(vectorstore: Chroma):
    """
    Costruisce la chain RAG completa con LCEL:
    domanda → retrieval → prompt augmentation → LLM → risposta
    """
    llm = OllamaLLM(model="llama3.2")
    
    # Il prompt che combina contesto e domanda
    prompt = ChatPromptTemplate.from_template("""
    Rispondi alla domanda basandoti solo sul contesto fornito.
    
    Contesto: {context}
    
    Domanda: {question}
    
    Risposta:""")
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    # La chain LCEL — leggi come una pipeline
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain