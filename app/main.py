from fastapi import FastAPI
from app.api.query import router as query_router

### Tutto segue questo ciclo:  richiesta HTTP → FastAPI → funzione Python → risposta JSON

# Crea l'istanza dell'applicazione FastAPI
# Il titolo e la versione appariranno nella documentazione automatica
app = FastAPI(
    title="RAG Agent API",
    version="0.1.0"
)

# Include il router — tutti gli endpoint definiti lì
# diventano parte dell'applicazione
app.include_router(query_router)

# Il nostro primo endpoint — solo per verificare che tutto funzioni
@app.get("/health")
def health_check():
    """Verifica che il server sia attivo."""
    return {"status": "ok"}

