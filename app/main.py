"""Application entrypoint for the TrialSense RAG assistant."""
from fastapi import FastAPI
from app.api.routes import router
from app.utils.logger import get_logger

logger = get_logger()

app = FastAPI(
    title="TrialSense AI",
    version="1.0.0",
    description="Clinical Trial Intelligence RAG Assistant"
)

app.include_router(router)


@app.on_event("startup")
async def startup_event():
    logger.info("TrialSense AI started successfully.")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down TrialSense AI.")


@app.get("/")
async def root():
    return {
        "application": "TrialSense AI",
        "version": "1.0.0",
        "status": "running"
    }