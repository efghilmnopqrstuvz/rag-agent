from fastapi import FastAPI
from app.models.query import QueryRequest, QueryResponse

### Tutto segue questo ciclo:  richiesta HTTP → FastAPI → funzione Python → risposta JSON

# Crea l'istanza dell'applicazione FastAPI
# Il titolo e la versione appariranno nella documentazione automatica
app = FastAPI(
    title="RAG Agent API",
    version="0.1.0"
)

# Il nostro primo endpoint — solo per verificare che tutto funzioni
@app.get("/health")
def health_check():
    """Verifica che il server sia attivo."""
    return {"status": "ok"}

@app.post("/query")
def query(request: QueryRequest) -> QueryResponse:
    """Riceve una domanda e restituisce una risposta."""
    # Per ora, rispondiamo con un messaggio di esempio
    answer = f"Hai chiesto:'{request.question}'"
    return QueryResponse(answer=answer)