from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.database import SessionLocal
from app.core.init_db import init_user_groups
from app.api.v1 import auth, redirect


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database
    db = SessionLocal()
    try:
        init_user_groups(db)
    finally:
        db.close()
    yield
    # Shutdown (if needed)


app = FastAPI(
    title="Online Cinema API",
    description="API for Online Cinema Platform",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(redirect.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Welcome to Online Cinema API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

