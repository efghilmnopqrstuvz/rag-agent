from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

class AddDocumentsRequest(BaseModel):
    urls: list[str]