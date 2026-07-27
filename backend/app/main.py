"""
Main FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.routers import auth_router, complaints_router, products_router, attachments_router, ai_router
import uvicorn

app = FastAPI(
    title="Pharma Complaint Management System",
    description="AI-Powered Customer Complaint Management System for Pharmaceutical Industry",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(complaints_router)
app.include_router(products_router)
app.include_router(attachments_router)
app.include_router(ai_router)


@app.on_event("startup")
async def startup_event():
    """
    Initialize database on startup.
    """
    init_db()


@app.get("/")
async def root():
    """
    Root endpoint.
    """
    return {
        "message": "Pharma Complaint Management System API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
