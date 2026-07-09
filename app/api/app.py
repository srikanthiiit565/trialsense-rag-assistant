"""FastAPI application and router inclusion."""
from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="TrialSense AI",
    version="1.0",
    description="Clinical Trial Intelligence RAG Assistant",
)

app.include_router(router)
