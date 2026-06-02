from fastapi import APIRouter
from app.models.query import QueryRequest, QueryResponse, AddDocumentsRequest
from app.services.rag import load_vectorstore, get_rag_chain, add_documents

router = APIRouter()

# Carica il vector store e la chain una volta sola all'avvio
# Non vogliamo ricaricarli ad ogni richiesta — sarebbe lentissimo
vectorstore = load_vectorstore()
chain = get_rag_chain(vectorstore)

@router.post("/query")
def query(request: QueryRequest) -> QueryResponse:
    """Riceve una domanda e restituisce una risposta basata sui documenti."""
    result = chain.invoke(request.question)
    return QueryResponse(answer=result)

@router.post("/documents")
def add_docs(request: AddDocumentsRequest):
    """Aggiunge nuovi documenti al vector store."""
    count = add_documents(request.urls)
    return {"message": f"Aggiunti {count} chunk al vector store"}