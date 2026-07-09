from fastapi import APIRouter

from app.api.models import (
    QueryRequest,
    QueryResponse,
    HealthResponse,
)

from app.agents.rag_agent import RAGAgent
from app.utils.config import settings


router = APIRouter()

agent = RAGAgent()


@router.get(
    "/health",
    response_model=HealthResponse,
)
def health():

    return HealthResponse(
        status="healthy",
        model=settings.OLLAMA_MODEL,
    )


@router.post(
    "/query",
    response_model=QueryResponse,
)
def query(
    request: QueryRequest,
):

    result = agent.ask(
        request.query
    )

    return QueryResponse(
        answer=result["answer"],
        citations=result["citations"],
    )