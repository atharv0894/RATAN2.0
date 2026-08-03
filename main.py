"""
FastAPI application entry point.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.config.logging import configure_logging, get_logger
from app.api.routes import ingest, query, documents, health

configure_logging(debug=settings.debug)
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown events."""
    logger.info(
        "Starting %s v%s | provider=%s | model=%s",
        settings.app_title, settings.app_version,
        settings.llm_provider, settings.groq_model,
    )
    # Eagerly initialise singletons so first request isn't slow
    from app.embeddings.embedding_model import get_embedding_model
    from app.vectorstore.qdrant_client import get_qdrant_client
    from app.llm.provider_factory import ProviderFactory
    get_embedding_model()
    get_qdrant_client()
    ProviderFactory.get_provider()
    logger.info("All services initialised — ready.")
    yield
    logger.info("Shutting down.")


app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    description="Production-ready RAG backend powered by Groq + Qdrant.",
    lifespan=lifespan,
)

# CORS — adjust origins for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router)
app.include_router(ingest.router)
app.include_router(query.router)
app.include_router(documents.router)


@app.get("/", include_in_schema=False)
async def root():
    return {"message": f"{settings.app_title} is running.", "docs": "/docs"}
