from fastapi import APIRouter
from app.models.query import QueryRequest, QueryResponse

# APIRouter funziona esattamente come app, ma è un "sotto-router"
# che viene poi incluso nel main
router = APIRouter()

@router.post("/query")
def query(request: QueryRequest) -> QueryResponse:
    """Riceve una domanda e restituisce una risposta (placeholder)."""
    return QueryResponse(answer=f"Hai chiesto: {request.question}")